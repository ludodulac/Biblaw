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
Every child command is time-bounded and reports elapsed time; descriptive editorial-review scripts
are deliberately kept outside validation paths unless they contain deterministic assertions.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
AREAS = ("corpus", "thematic", "search", "ui")
CHECK_STEP_TIMEOUT_SECONDS = int(os.environ.get("BIBLAW_CHECK_STEP_TIMEOUT_SECONDS", "1800"))
SLOW_STEP_SECONDS = float(os.environ.get("BIBLAW_SLOW_STEP_SECONDS", "120"))


def require_tools(*tools: str) -> None:
    """Fail before expensive work when a selected validation path lacks a required executable."""
    missing = [tool for tool in tools if shutil.which(tool) is None]
    if missing:
        hints = {
            "pdftotext": "install Poppler (package poppler-utils on Ubuntu/Debian)",
            "node": "install Node.js",
            "git": "install Git and run the command inside a Git checkout",
        }
        detail = "; ".join(f"{tool}: {hints.get(tool, 'install this executable')}" for tool in missing)
        raise SystemExit(f"Missing validation dependency: {detail}")


def execute(parts: list[str], label: str) -> None:
    print(f"\n=== START {label} (timeout={CHECK_STEP_TIMEOUT_SECONDS}s) ===", flush=True)
    started = time.perf_counter()
    try:
        subprocess.run(parts, cwd=ROOT, check=True, timeout=CHECK_STEP_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - started
        print(
            f"::error::Biblaw check step timed out: {label} exceeded "
            f"{CHECK_STEP_TIMEOUT_SECONDS}s after {elapsed:.1f}s",
            flush=True,
        )
        raise
    elapsed = time.perf_counter() - started
    print(f"--- DONE {label}: {elapsed:.3f}s", flush=True)
    if elapsed > SLOW_STEP_SECONDS:
        print(
            f"::warning::Slow Biblaw check step: {label} took {elapsed:.1f}s "
            f"(threshold {SLOW_STEP_SECONDS:.0f}s)",
            flush=True,
        )


def run_script(script: str, *args: str) -> None:
    label = f"{script} {' '.join(args)}".strip()
    execute([sys.executable, str(SCRIPTS / script), *args], label)


def run_command(*parts: str) -> None:
    execute(list(parts), " ".join(parts))


def fast(area: str) -> None:
    if area == "thematic":
        run_script("normalize_known_theme_identifiers.py", "--check")
        run_script("validate_thematic_index.py")
    elif area == "search":
        run_command("node", "--check", "js/biblaw.js")
        run_script("audit_public_theme_directory.py")
        run_script("validate_thematic_search_runtime.py")
        run_script("audit_production_search_queries.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "ui":
        run_command("node", "--check", "js/biblaw.js")
        run_script("audit_public_ui_contract.py")
        run_script("audit_public_theme_directory.py")
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
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "corpus":
        # Corpus metadata/evidence can propagate into thematic books and all downstream projections.
        # Rebuild those deterministic derivatives, but do not replay deep semantic/PDF passes.
        run_script("rebuild_thematic_derivatives.py")
        generated = True
        run_script("audit_production_search_queries.py")
        run_script("audit_psalm_number_search.py")
        run_script("audit_browser_search_indexes.py")
    elif area == "search":
        fast("search")
        run_script("audit_public_ui_contract.py")
        run_script("audit_theme_directory_ui.py")
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
    run_script("audit_public_theme_directory.py")
    run_script("audit_theme_directory_ui.py")
    run_script("audit_production_search_queries.py")
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

    print(
        f"Biblaw check guardrails: step_timeout={CHECK_STEP_TIMEOUT_SECONDS}s "
        f"slow_threshold={SLOW_STEP_SECONDS:.0f}s",
        flush=True,
    )

    if args.level == "FULL":
        if args.area:
            parser.error("FULL is repository-wide; do not pass --area")
        require_tools("pdftotext", "node", "git")
        full()
        return

    if not args.area:
        parser.error(f"{args.level} requires --area ({', '.join(AREAS)})")

    if args.area in {"search", "ui"}:
        require_tools("node")
    if args.level == "TARGETED" and args.area in {"thematic", "corpus"}:
        require_tools("git")

    if args.level == "FAST":
        fast(args.area)
    else:
        targeted(args.area)
    print(f"\n{args.level} Biblaw check OK for area={args.area}")


if __name__ == "__main__":
    main()
