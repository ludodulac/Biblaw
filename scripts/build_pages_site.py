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
    "css/biblaw-light.css",
    "css/theme-index.css",
    "css/theme-entry.css",
    "css/validation.css",
    "js/theme-suggestion-engine.js",
    "js/biblaw-pdf.js",
    "js/biblaw-faq.js",
    "js/biblaw-autocomplete.js",
    "js/biblaw.js",
    "js/theme-relations.js",
    "js/theme-entry.js",
    "js/theme-rubrics.js",
    "js/validation.js",
    "data/browser-search-catalog.json",
    "data/note-themes-public-073.json",
    "data/faq-public-085.json",
    "data/faq-090-1.json",
    "data/faq-090-2.json",
    "data/faq-090-3.json",
    "data/faq-090-4.json",
    "data/faq-090-5.json",
    "data/faq-090-books.json",
    "data/faq-091-1.json",
    "data/faq-091-2.json",
    "data/faq-091-3.json",
    "data/faq-091-4.json",
    "data/faq-091-5.json",
    "data/faq-091-6.json",
    "data/faq-091-7.json",
    "data/faq-091-8.json",
    "data/faq-091-9.json",
    "data/faq-091-books.json",
    "data/faq-092.json",
    "data/lexical-expansion-runtime.json",
    "data/linguistic-sense-browser-runtime.json",
    "data/linguistic-grammar-browser-runtime.json",
    "data/thematic-index/theme-directory-public.json",
    "data/thematic-index/theme-relations-public.json",
    "data/thematic-index/theme-rubrics-public.json",
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
