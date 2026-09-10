#!/usr/bin/env python3
"""Build the minimal GitHub Pages payload from an explicit production allow-list.

The repository contains large canonical, audit and research artefacts that are required for CI but
not by the browser. Publishing the repository root wastes upload time and exposes internal working
files. This staging step copies only assets referenced by the public search UI and the directly
accessible editorial validation workshop.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"

PUBLIC_FILES = (
    ".nojekyll",
    "index.html",
    "validation.html",
    "Bible essénienne (classée par livres).pdf",
    "css/biblaw.css",
    "css/theme-index.css",
    "css/validation.css",
    "js/biblaw.js",
    "js/theme-relations.js",
    "js/validation.js",
    "data/browser-search-catalog.json",
    "data/thematic-index/theme-directory-public.json",
    "data/thematic-index/theme-relations-public.json",
    "data/thematic-index/theme-search-runtime.json",
)

FORBIDDEN_PREFIXES = (
    ".github/",
    "progression/",
    "scripts/",
    "schemas/",
    "data/corpus/",
    "data/prayers/",
    "data/notes/",
    "data/thematic-index/books/",
    "data/thematic-index/source-packs/",
)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    total = 0
    for relative in PUBLIC_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"Missing Pages production asset: {relative}")
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        total += target.stat().st_size

    staged = sorted(str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file())
    assert staged == sorted(PUBLIC_FILES), "Pages staging contains a file outside the explicit allow-list"
    assert not any(path.startswith(FORBIDDEN_PREFIXES) for path in staged), "internal repository data leaked into Pages staging"
    assert "data/thematic-index/theme-relations-validated.json" not in staged, "canonical relation evidence leaked into Pages staging"

    print(f"Pages staging OK: {len(staged)} files, {total / (1024 * 1024):.1f} MiB")
    for path in staged:
        print(f"  {path}")


if __name__ == "__main__":
    main()
