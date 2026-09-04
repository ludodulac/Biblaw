#!/usr/bin/env python3
"""Split a psalm when the source embeds the next psalm heading inside numbered text.

Some source layouts preserve a clear next-psalm title but continue the preceding verse
numbering instead of resetting cleanly. We keep the printed numbers as sourceNumber
metadata and expose normalized verse numbers for the new psalm.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus/books"
REPORT = ROOT / "data/pilot/books-01-10-extraction-report.json"


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def title_like(value: str) -> bool:
    letters = [c for c in value if c.isalpha()]
    if len(letters) < 5:
        return False
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters) >= 0.85


def normalize_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if title_like(value):
        value = value.lower()
        value = value[:1].upper() + value[1:]
    return value


created = []
for book_dir in sorted(CORPUS.glob("book-*")):
    book_path = book_dir / "book.json"
    if not book_path.exists():
        continue
    book = json.loads(book_path.read_text(encoding="utf-8"))
    existing_numbers = {
        json.loads(p.read_text(encoding="utf-8")).get("number")
        for p in book_dir.glob("psalm-*.json")
    }
    changes = []
    for psalm_path in sorted(book_dir.glob("psalm-*.json")):
        psalm = json.loads(psalm_path.read_text(encoding="utf-8"))
        current_number = psalm.get("number")
        target_number = current_number + 1 if isinstance(current_number, int) else None
        if target_number in existing_numbers:
            continue
        verses = psalm.get("verses", [])
        split_index = None
        embedded_title = None
        for idx, verse in enumerate(verses):
            text = verse.get("text", "")
            m = re.match(r"^\s*(\d{1,3})\s+(.+?)\s*$", text)
            if not m:
                continue
            if int(m.group(1)) == target_number and title_like(m.group(2)):
                split_index = idx
                embedded_title = normalize_title(m.group(2))
                break
        if split_index is None or split_index + 1 >= len(verses):
            continue

        before = verses[:split_index]
        after = verses[split_index + 1:]
        if not before or not after:
            continue

        new_verses = []
        for normalized_number, source_verse in enumerate(after, 1):
            new_verse = {
                "number": normalized_number,
                "sourceNumber": source_verse.get("number"),
                "text": source_verse.get("text", ""),
                "sourcePages": source_verse.get("sourcePages", []),
            }
            new_verses.append(new_verse)

        psalm["verses"] = before
        psalm["source"]["pdfPages"] = sorted({p for v in before for p in v.get("sourcePages", [])})
        psalm.setdefault("extraction", {})["embeddedNextPsalmDetected"] = target_number
        psalm["validation"] = {
            "status": "machine-extracted-needs-review",
            "checks": {"verseCount": len(before), "verseSequenceStartsAtOne": before[0].get("number") == 1},
        }
        write(psalm_path, psalm)

        new_id = f"book-{book['number']:02d}-psalm-{target_number:03d}"
        new_path = book_dir / f"psalm-{target_number:03d}.json"
        new_record = {
            "id": new_id,
            "recordType": "psalm",
            "archangel": book.get("archangel"),
            "book": {"number": book.get("number"), "title": book.get("title")},
            "number": target_number,
            "title": embedded_title,
            "source": {
                "document": psalm.get("source", {}).get("document"),
                "pdfPages": sorted({p for v in new_verses for p in v.get("sourcePages", [])}),
            },
            "verses": new_verses,
            "noteIds": [],
            "extraction": {
                "headingBasis": "embedded-numbered-heading",
                "sourceHeadingContainer": psalm.get("id"),
                "sourceHeadingPrintedVerseNumber": verses[split_index].get("number"),
                "sourceVerseNumbersPreservedAs": "sourceNumber",
            },
            "validation": {
                "status": "machine-extracted-needs-review",
                "checks": {"verseCount": len(new_verses), "verseSequenceStartsAtOne": True},
            },
        }
        write(new_path, new_record)
        existing_numbers.add(target_number)
        changes.append(target_number)
        created.append({"bookNumber": book.get("number"), "psalmNumber": target_number, "title": embedded_title})

    if changes:
        ids = []
        for path in sorted(book_dir.glob("psalm-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            ids.append((data["number"], data["id"]))
        book["psalmIds"] = [record_id for _, record_id in sorted(ids)]
        book.setdefault("extraction", {})["embeddedHeadingsNormalized"] = sorted(changes)
        write(book_path, book)

if REPORT.exists() and created:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["embeddedHeadingNormalizations"] = created
    for change in created:
        for book in report.get("books", []):
            if book.get("bookNumber") != change["bookNumber"]:
                continue
            book.setdefault("normalizations", []).append(change)
    write(REPORT, report)

print(f"Normalized {len(created)} embedded psalm heading(s)")
