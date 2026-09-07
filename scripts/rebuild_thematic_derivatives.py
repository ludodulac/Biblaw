#!/usr/bin/env python3
"""Rebuild only deterministic derivatives of already-canonical thematic book data.

Use this after a targeted edit to data/thematic-index/books/book-XX.json or to a downstream
search/index generator when the PDF-derived corpus and deep semantic generation logic did not
change. It deliberately does NOT replay PDF repairs, extraction, completion, or deep semantic
passes. Changes to those upstream layers require scripts/run_canonical_thematic_pipeline.py.

Order matters: canonical source validity is checked before derived search/runtime artefacts are
published. Generated files are rebuilt from their sources and never hand-edited here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> None:
    print(f"\n=== {script} {' '.join(args)} ===", flush=True)
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    # Guards / canonical metadata synchronization. These are deterministic and corpus-internal.
    run("normalize_known_theme_identifiers.py", "--check")
    run("sync_thematic_documentary_status.py")
    run("normalize_thematic_metadata.py")
    run("build_book_contexts.py")

    # Fail as early as possible on an inadmissible canonical relation.
    run("validate_thematic_index.py")

    # Rebuild the complete downstream projection chain from the validated canonical books.
    run("build_thematic_directory.py")
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
