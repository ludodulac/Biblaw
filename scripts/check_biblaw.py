#!/usr/bin/env python3
"""Run proportional Biblaw checks without weakening the canonical FULL gate.

Examples:
  python scripts/check_biblaw.py FAST --area thematic
  python scripts/check_biblaw.py TARGETED --area search
  python scripts/check_biblaw.py TARGETED --area thematic
  python scripts/check_biblaw.py FULL

FAST is non-destructive and intended for short edit loops.
TARGETED may rebuild only the deterministic artefacts belonging to the selected area.
FULL replays the canonical pipeline and then the production/UI regression audits.
Generated TARGETED/FULL paths finish with a compact diff against the current git baseline.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
AREAS = ("corpus", "thematic", "search", "ui")


def run_script(script: str, *args: str) -> None:
    print(f"\n=== {script} {' '.join(args)} ===", flush=True)
    subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=ROOT, check=True)


def run_command(*parts: str) -> None:
    print(f"\n=== {' '.join(parts)} ===", flush=True)
    subprocess.run(list(parts), cwd=ROOT, check=True)


def fast(area: str) -> None:
    if area == "thematic":
        run_script("normalize_known_theme_identifiers.py", "--check")
        run_script("validate_thematic_index.py")
    elif area == "search":
        run_command("node", "--check", "js/biblaw.js")
        run_script("validate_thematic_search_runtime.py")
        run_script("audit_production_search_queries.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "ui":
        run_command("node", "--check", "js/biblaw.js")
        run_script("audit_public_ui_contract.py")
        run_script("audit_theme_directory_ui.py")
    elif area == "corpus":
        # A corpus edit can invalidate a canonical theme's verse evidence before the UI changes.
        run_script("validate_thematic_index.py")
        run_script("audit_corpus_attachments.py")
        run_script("audit_legacy_psalm_references.py")


def targeted(area: str) -> None:
    generated = False
    if area == "thematic":
        run_script("rebuild_thematic_derivatives.py")
        generated = True
        run_script("audit_production_search_queries.py")
        run_script("audit_assembly_theme_context.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "corpus":
        # Corpus metadata/evidence can propagate into thematic books and all downstream projections.
        # Rebuild those deterministic derivatives, but do not replay deep semantic/PDF passes.
        run_script("rebuild_thematic_derivatives.py")
        generated = True
        run_script("audit_production_search_queries.py")
        run_script("audit_assembly_theme_context.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "search":
        fast("search")
        run_script("audit_public_ui_contract.py")
        run_script("audit_theme_directory_ui.py")
        run_script("audit_assembly_theme_context.py")
    elif area == "ui":
        fast("ui")
        run_script("audit_production_search_queries.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")

    if generated:
        run_script("report_biblaw_diff.py")


def full() -> None:
    # Match the canonical workflow's reviewed technical normalization before replaying generators.
    run_script("normalize_known_theme_identifiers.py")
    run_script("normalize_known_theme_identifiers.py", "--check")
    run_script("run_canonical_thematic_pipeline.py")
    run_script("normalize_known_theme_identifiers.py", "--check")

    # FULL means canonical generation plus the final production/search/UI contracts.
    run_command("node", "--check", "js/biblaw.js")
    run_script("audit_public_ui_contract.py")
    run_script("audit_theme_directory_ui.py")
    run_script("audit_production_search_queries.py")
    run_script("audit_assembly_theme_context.py")
    run_script("audit_psalm_number_search.py")
    run_script("audit_browser_search_indexes.py")
    run_script("audit_corpus_attachments.py")
    run_script("audit_legacy_psalm_references.py")
    run_script("report_biblaw_diff.py")
    print("\nFULL Biblaw validation OK")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("level", choices=("FAST", "TARGETED", "FULL"))
    parser.add_argument("--area", choices=AREAS)
    args = parser.parse_args()

    if args.level == "FULL":
        if args.area:
            parser.error("FULL is repository-wide; do not pass --area")
        full()
        return

    if not args.area:
        parser.error(f"{args.level} requires --area ({', '.join(AREAS)})")
    if args.level == "FAST":
        fast(args.area)
    else:
        targeted(args.area)
    print(f"\n{args.level} Biblaw check OK for area={args.area}")


if __name__ == "__main__":
    main()
