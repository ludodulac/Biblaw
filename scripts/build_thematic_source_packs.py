#!/usr/bin/env python3
"""Build compact reading packs for thematic analysis of books 1-10.

Packs are derived from the validated psalm corpus and include book metadata, psalm
titles, verse text and editorial notes. Prayers are intentionally excluded from the
current thematic-indexing scope. Packs are not editorial conclusions; they are a
stable input format for semantic analysis.
"""
from __future__ import annotations

import json
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


if OUT.exists():
    shutil.rmtree(OUT)

manifest = {"scope": "books-01-10", "prayersIncluded": False, "books": []}
for book_no in range(1, 11):
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
print(f"Built thematic source packs for {len(manifest['books'])} books")
