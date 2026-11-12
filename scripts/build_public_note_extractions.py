#!/usr/bin/env python3
"""Project the 280 archived note transcriptions into an explicitly labelled public index.

This is NOT an authentication of any archival transcription. No source file is
modified, no archive source path is exposed, and the eleven separately published
notes retain their editorial text. The interface must disclose the status.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data" / "notes" / "books"
CATALOG = ROOT / "data" / "catalog.json"
DEFAULT_OUTPUT = ROOT / "_site" / "data" / "notes-extracted-public.json"
NAME = re.compile(r"^book-(\d{2})-psalm-(\d{3})-note-(\d{3})\.json$")
EXPECTED_NOTE_COUNT = 280
EXPECTED_PUBLISHED_COUNT = 11


def generate(output: Path = DEFAULT_OUTPUT) -> dict:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    published_paths = {
        path for path in catalog["records"]
        if path.startswith("data/notes/") and path.endswith(".json")
    }
    assert len(published_paths) == EXPECTED_PUBLISHED_COUNT, "Existing public notes must remain unchanged"
    published_ids = {Path(path).stem for path in published_paths}
    archived_paths = sorted(ARCHIVE.glob("book-*/*.json"))
    assert len(archived_paths) == EXPECTED_NOTE_COUNT, (
        f"Expected {EXPECTED_NOTE_COUNT} extracted note files, got {len(archived_paths)}"
    )
    records = []
    seen = set()
    for path in archived_paths:
        match = NAME.fullmatch(path.name)
        assert match, f"Unexpected note file: {path}"
        book, psalm, note_number = map(int, match.groups())
        assert path.parent.name == f"book-{book:02d}", f"Wrong book directory: {path}"
        item = json.loads(path.read_text(encoding="utf-8"))
        assert item.get("id") == path.stem, f"Mismatched note ID: {path}"
        assert item.get("recordType") == "note" and item.get("bookNumber") == book
        assert item["id"] not in seen, f"Duplicate note ID: {item['id']}"
        seen.add(item["id"])
        applies = item.get("appliesTo") or {}
        assert applies.get("recordId") == f"book-{book:02d}-psalm-{psalm:03d}"
        assert (marker := applies.get("marker")) is None or isinstance(marker, int)
        verse = applies.get("verse")
        assert verse is None or (isinstance(verse, int) and verse > 0)
        source = item.get("source") or {}
        assert source.get("document") == "Bible essénienne (classée par livres).pdf"
        page = source.get("pdfPage")
        assert isinstance(page, int) and page > 0
        assert item.get("validation", {}).get("status"), "Missing original review status"
        publication_status = "published" if item["id"] in published_ids else "unverified"
        if publication_status == "published":
            original = json.loads((ROOT / "data" / "notes" / (item["id"] + ".json")).read_text(encoding="utf-8"))
            assert original.get("id") == item["id"]
            assert original.get("recordType") == "note"
            text = original.get("text") or original.get("summary") or ""
        else:
            text = item.get("text") or ""
        assert isinstance(text, str) and text.strip(), f"Empty note transcription: {path}"
        records.append({
            "id": item["id"],
            "recordType": "note",
            "bookNumber": book,
            "psalmNumber": psalm,
            "noteNumber": note_number,
            "archangel": item.get("archangel") or "",
            "appliesTo": {
                "recordId": applies["recordId"],
                "marker": marker,
                "verse": verse,
            },
            "sourcePdfPage": page,
            "text": text.strip(),
            "publicationStatus": publication_status,
        })
    assert seen >= published_ids, "All 11 public notes should have an archived note counterpart"
    books = sorted({item["bookNumber"] for item in records})
    assert len(books) == 41, f"Unexpected archived book count: {len(books)}"
    published = sum(item["publicationStatus"] == "published" for item in records)
    assert published == EXPECTED_PUBLISHED_COUNT
    counts = Counter(item["bookNumber"] for item in records)
    payload = {
        "schemaVersion": 1,
        "purpose": "public-navigation-of-archived-note-extractions-not-documentary-validation",
        "archiveCount": len(records),
        "alreadyPublishedCount": published,
        "needsReviewCount": len(records) - published,
        "bookCount": len(books),
        "perBookCounts": {str(book): counts[book] for book in books},
        "warning": "Les transcriptions signalées « à vérifier » proviennent d’une extraction automatique et peuvent comporter des erreurs. Consultez la page PDF source indiquée.",
        "notes": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = generate()
    print(f"NOTES_ARCHIVE_PUBLIC_PASS archived={result['archiveCount']} "
          f"published={result['alreadyPublishedCount']} "
          f"unverified={result['needsReviewCount']} books={result['bookCount']}")
