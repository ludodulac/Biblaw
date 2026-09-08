#!/usr/bin/env python3
"""Rebuild only deterministic derivatives of already-canonical thematic book data.

Use this after a targeted edit to data/thematic-index/books/book-XX.json or to a downstream
search/index generator when the PDF-derived corpus and deep semantic generation logic did not
change. It deliberately does NOT replay PDF repairs, extraction, completion, or deep semantic
passes. Changes to those upstream layers require scripts/run_canonical_thematic_pipeline.py.

Order matters: canonical source validity is checked before derived search/runtime artefacts are
published. Generated files are rebuilt from their sources and never hand-edited here. Each stage is
time-bounded and reports elapsed time so a TARGETED run cannot silently stall for hours.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE_TIMEOUT_SECONDS = int(os.environ.get("BIBLAW_TARGETED_STAGE_TIMEOUT_SECONDS", "600"))
SLOW_STEP_SECONDS = float(os.environ.get("BIBLAW_SLOW_STEP_SECONDS", "120"))


def run(script: str, *args: str) -> None:
    command = [sys.executable, str(ROOT / "scripts" / script), *args]
    label = f"{script} {' '.join(args)}".strip()
    print(f"\n=== START {label} (timeout={STAGE_TIMEOUT_SECONDS}s) ===", flush=True)
    started = time.perf_counter()
    try:
        subprocess.run(command, cwd=ROOT, check=True, timeout=STAGE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - started
        print(
            f"::error::Targeted step timed out: {label} exceeded "
            f"{STAGE_TIMEOUT_SECONDS}s after {elapsed:.1f}s",
            flush=True,
        )
        raise
    elapsed = time.perf_counter() - started
    print(f"--- DONE {label}: {elapsed:.3f}s", flush=True)
    if elapsed > SLOW_STEP_SECONDS:
        print(
            f"::warning::Slow targeted step: {label} took {elapsed:.1f}s "
            f"(threshold {SLOW_STEP_SECONDS:.0f}s)",
            flush=True,
        )


def main() -> None:
    print(
        f"Targeted rebuild guardrails: stage_timeout={STAGE_TIMEOUT_SECONDS}s "
        f"slow_threshold={SLOW_STEP_SECONDS:.0f}s",
        flush=True,
    )
    # Guards / canonical metadata synchronization. These are deterministic and corpus-internal.
    run("normalize_known_theme_identifiers.py", "--check")
    run("sync_thematic_documentary_status.py")
    run("normalize_thematic_metadata.py")
    run("build_book_contexts.py")

    # Fail as early as possible on an inadmissible canonical relation.
    run("validate_thematic_index.py")

    # Rebuild the complete downstream projection chain from the validated canonical books.
    run("build_thematic_directory.py")
    run("build_public_theme_directory.py")
    run("audit_public_theme_directory.py")
    run("audit_thematic_search_quality.py")
    run("build_thematic_search_index.py")
    run("validate_thematic_search_index.py")
    run("build_thematic_connections.py")
    run("validate_thematic_connections.py")
    run("build_thematic_search_runtime.py")
    run("validate_thematic_search_runtime.py")
    run("build_browser_search_catalog.py")

    # Production-boundary checks catch stale bundle/legacy attachment regressions immediately.
    run("audit_corpus_attachments.py")
    run("audit_legacy_psalm_references.py")

    print("\nTargeted thematic derivative rebuild OK")


if __name__ == "__main__":
    main()
