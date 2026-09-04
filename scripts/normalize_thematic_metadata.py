#!/usr/bin/env python3
"""Keep thematic book metadata synchronized with the corpus and apply explicit evidence repairs.

Titles are documentary metadata and are always copied from the structured psalm corpus.
Evidence repairs are explicit editorial decisions, never inferred from keywords.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
CORPUS = ROOT / "data/corpus/books"

EVIDENCE_REPAIRS = {
    ("book-03-psalm-020", "enthousiasme"): [2, 4, 6],
    ("book-03-psalm-020", "flamme"): [2, 4, 6],
}

changed_files = 0
for path in sorted(BOOKS.glob("book-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    book_no = data.get("book", {}).get("number")
    changed = False
    if not isinstance(book_no, int):
        continue
    for psalm in data.get("psalmAnalyses", []):
        number = psalm.get("number")
        if isinstance(number, int):
            source_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{number:03d}.json"
            if source_path.exists():
                source = json.loads(source_path.read_text(encoding="utf-8"))
                source_title = source.get("title")
                if source_title and psalm.get("title") != source_title:
                    psalm["title"] = source_title
                    changed = True
        record_id = psalm.get("recordId")
        for rel in psalm.get("themes", []):
            key = (record_id, rel.get("themeId"))
            if key in EVIDENCE_REPAIRS and rel.get("verseNumbers") != EVIDENCE_REPAIRS[key]:
                rel["verseNumbers"] = EVIDENCE_REPAIRS[key]
                changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Normalized thematic metadata in {changed_files} book files")
