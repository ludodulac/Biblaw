#!/usr/bin/env python3
"""Build compact reading packs for every extracted canonical book.

Packs are derived from the psalm corpus and include book metadata, Psalm titles,
verse text and editorial notes. Prayers are intentionally excluded from the current
thematic-indexing scope. Packs are stable semantic-analysis inputs, not editorial
conclusions.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"
OUT = ROOT / "data/thematic-index/source-packs"
CHUNK_SIZE = 4


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def available_book_numbers() -> list[int]:
    numbers = []
    for path in CORPUS.glob("book-*"):
        match = re.fullmatch(r"book-(\d+)", path.name)
        if not match or not (path / "book.json").exists():
            continue
        numbers.append(int(match.group(1)))
    return sorted(numbers)


book_numbers = available_book_numbers()
if not book_numbers:
    raise RuntimeError("No extracted canonical books found")

if OUT.exists():
    shutil.rmtree(OUT)

manifest = {
    "scope": "all-extracted-canonical-books",
    "bookNumbers": book_numbers,
    "prayersIncluded": False,
    "books": [],
}

for book_no in book_numbers:
    book_dir = CORPUS / f"book-{book_no:02d}"
    book = read(book_dir / "book.json")
    psalms = []
    for path in sorted(book_dir.glob("psalm-*.json")):
        psalm = read(path)
        notes = []
        for note_id in psalm.get("noteIds", []):
            note_path = NOTES / f"book-{book_no:02d}" / f"{note_id}.json"
            if note_path.exists():
                note = read(note_path)
                notes.append({
                    "id": note.get("id"),
                    "marker": note.get("appliesTo", {}).get("marker"),
                    "verse": note.get("appliesTo", {}).get("verse"),
                    "text": note.get("text"),
                    "pdfPage": note.get("source", {}).get("pdfPage"),
                })
        psalms.append({
            "recordId": psalm["id"],
            "number": psalm["number"],
            "title": psalm["title"],
            "pdfPages": psalm.get("source", {}).get("pdfPages", []),
            "verses": [
                {
                    "number": v.get("number"),
                    **({"sourceNumber": v.get("sourceNumber")} if v.get("sourceNumber") is not None else {}),
                    "text": v.get("text", ""),
                    "sourcePages": v.get("sourcePages", []),
                }
                for v in psalm.get("verses", [])
            ],
            "notes": notes,
        })

    pack_paths = []
    for index in range(0, len(psalms), CHUNK_SIZE):
        part = index // CHUNK_SIZE + 1
        chunk = psalms[index:index + CHUNK_SIZE]
        path = OUT / f"book-{book_no:02d}" / f"part-{part:03d}.json"
        write(path, {
            "book": {
                "number": book_no,
                "title": book.get("title"),
                "archangel": book.get("archangel"),
                "pdfPages": book.get("source", {}).get("pdfPages", []),
            },
            "scope": {"psalmsOnly": True, "notesIncluded": True, "prayersIncluded": False},
            "psalms": chunk,
        })
        pack_paths.append(path.relative_to(ROOT).as_posix())
    manifest["books"].append({
        "bookNumber": book_no,
        "title": book.get("title"),
        "archangel": book.get("archangel"),
        "psalmCount": len(psalms),
        "packs": pack_paths,
    })

write(OUT / "manifest.json", manifest)
print(f"Built thematic source packs for {len(manifest['books'])} books: {book_numbers[0]}-{book_numbers[-1]}")
