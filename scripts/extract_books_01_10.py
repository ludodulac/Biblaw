#!/usr/bin/env python3
"""Extract books 1-10 from the source PDF into structured corpus records.

This stage is documentary, not thematic. It preserves book title, detected Archangel,
psalm titles, verse text, page references and editorial notes. Prayers are deliberately
not indexed thematically and are not required for this extraction phase.
"""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
INVENTORY = ROOT / "data/pilot/book-inventory.json"
REPORT = ROOT / "data/pilot/books-01-10-extraction-report.json"
ARCHANGELS = {"michaël":"michael","raphaël":"raphael","gabriel":"gabriel","ouriel":"ouriel"}


def unwrap(value: str) -> str:
    value = re.sub(r"-\n\s*", "", value)
    value = re.sub(r"\n\s*", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    # pdftotext often separates a decorative initial: "V is" -> "Vis".
    value = re.sub(r"^([A-ZÀ-ÖØ-Ý])\s+([a-zà-öø-ÿ])", r"\1\2", value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([’'])\s+", r"\1", value)
    value = re.sub(r"\s+-\s*", "-", value)
    return value.strip()


def page_text(first: int, last: int) -> list[tuple[int, str]]:
    raw = subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return [(first + i, page) for i, page in enumerate(raw.split("\f")) if page.strip()]


def detect_archangel(pages: list[tuple[int, str]]) -> str | None:
    counts = Counter()
    for _, page in pages:
        for name, slug in ARCHANGELS.items():
            counts[slug] += len(re.findall(rf"(?i)Archange\s+{re.escape(name)}", page))
    return counts.most_common(1)[0][0] if counts and counts.most_common(1)[0][1] else None


def clean_page(book_no: int, page_no: int, raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        s = line.strip()
        if re.search(rf"(?i)\bLivre\s+{book_no}\s*\|", s):
            continue
        if s == str(page_no):
            continue
        lines.append(line)
    return "\n".join(lines)


def page_at(text: str, offset: int, default: int) -> int:
    found = list(re.finditer(r"\[\[PAGE (\d+)\]\]", text[:offset]))
    return int(found[-1].group(1)) if found else default


def strip_markers(value: str) -> str:
    return re.sub(r"\[\[PAGE \d+\]\]", "", value)


def plausible_heading(line: str):
    s = re.sub(r"\s+", " ", line).strip()
    m = re.match(r"^(\d{1,3})\s+(.{3,120})$", s)
    if not m:
        return None
    number = int(m.group(1))
    title = m.group(2).strip()
    if not re.match(r"^[A-ZÀ-ÖØ-ÝŒÉÈÊÂÎÔÛÇL’']", title):
        return None
    low = title.lower()
    if "livre " in low or "note des hiérogrammates" in low or title.startswith("-"):
        return None
    if len(title.split()) > 18 or title.endswith((".", ";", ":")):
        return None
    return number, clean_title(title)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
selected = [b for b in inventory["books"] if 1 <= b["bookNumber"] <= 10]
report = []

for book in selected:
    book_no = book["bookNumber"]
    first, last = book["pdfPages"]
    raw_pages = page_text(first, last)
    archangel = detect_archangel(raw_pages)
    cleaned_pages = []
    for page_no, raw in raw_pages:
        cleaned_pages.append(f"\n[[PAGE {page_no}]]\n{clean_page(book_no, page_no, raw)}")
    text = "".join(cleaned_pages)

    headings = []
    offset = 0
    for line in text.splitlines(True):
        candidate = plausible_heading(line)
        if candidate:
            number, title = candidate
            headings.append({"number": number, "title": title, "offset": offset, "page": page_at(text, offset, first)})
        offset += len(line)

    # Keep one plausible heading per psalm number, preferring the first occurrence whose
    # numbering is compatible with the surrounding sequence. This rejects most prose false positives.
    by_number = {}
    for h in headings:
        by_number.setdefault(h["number"], []).append(h)
    chosen = []
    prev_offset = -1
    max_candidate = max(by_number, default=0)
    for number in range(1, max_candidate + 1):
        options = [h for h in by_number.get(number, []) if h["offset"] > prev_offset]
        if not options:
            continue
        h = options[0]
        chosen.append(h)
        prev_offset = h["offset"]
    chosen.sort(key=lambda h: h["offset"])

    # Remove any candidate that lands before the first real numbered teaching block and then
    # immediately conflicts with a later same-number candidate. This matters in introductions.
    filtered = []
    seen_numbers = set()
    for h in chosen:
        if h["number"] in seen_numbers:
            continue
        seen_numbers.add(h["number"])
        filtered.append(h)
    chosen = filtered

    book_dir = ROOT / "data/corpus/books" / f"book-{book_no:02d}"
    note_dir = ROOT / "data/notes/books" / f"book-{book_no:02d}"
    extracted_psalms = []
    all_notes = []

    for i, h in enumerate(chosen):
        start = h["offset"]
        end = chosen[i + 1]["offset"] if i + 1 < len(chosen) else len(text)
        segment = text[start:end]
        # Remove heading line itself.
        segment_body = segment.split("\n", 1)[1] if "\n" in segment else ""

        note_pattern = re.compile(r"(?ms)^\s*(\d+)\s*-\s+(.*?)(?=^\s*\d+\s*-\s+|\Z)")
        notes = []
        for nm in note_pattern.finditer(segment_body):
            notes.append({"marker": int(nm.group(1)), "text": unwrap(strip_markers(nm.group(2))), "page": page_at(segment_body, nm.start(), h["page"])})
        body = note_pattern.sub("", segment_body)

        verse_matches = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", body))
        verses = []
        for vi, vm in enumerate(verse_matches):
            vnum = int(vm.group(1))
            vend = verse_matches[vi + 1].start() if vi + 1 < len(verse_matches) else len(body)
            vtext = unwrap(strip_markers(body[vm.end():vend]))
            if not vtext:
                continue
            verses.append({"number": vnum, "text": vtext, "sourcePages": [page_at(body, vm.start(), h["page"])]})

        if not verses:
            continue

        note_ids = []
        for ni, note in enumerate(notes, 1):
            note_id = f"book-{book_no:02d}-psalm-{h['number']:03d}-note-{ni:03d}"
            note_ids.append(note_id)
            record = {
                "id": note_id,
                "recordType": "note",
                "archangel": archangel,
                "bookNumber": book_no,
                "appliesTo": {"recordId": f"book-{book_no:02d}-psalm-{h['number']:03d}", "marker": note["marker"], "verse": None},
                "text": note["text"],
                "source": {"document": PDF.name, "pdfPage": note["page"]},
                "validation": {"status": "machine-extracted-needs-review"},
            }
            write_json(note_dir / f"{note_id}.json", record)
            all_notes.append(note_id)

        pages_used = sorted({p for v in verses for p in v["sourcePages"]})
        psalm = {
            "id": f"book-{book_no:02d}-psalm-{h['number']:03d}",
            "recordType": "psalm",
            "archangel": archangel,
            "book": {"number": book_no, "title": book.get("title")},
            "number": h["number"],
            "title": h["title"],
            "source": {"document": PDF.name, "pdfPages": pages_used},
            "verses": verses,
            "noteIds": note_ids,
            "validation": {
                "status": "machine-extracted-needs-review",
                "checks": {"verseCount": len(verses), "verseSequenceStartsAtOne": verses[0]["number"] == 1},
            },
        }
        write_json(book_dir / f"psalm-{h['number']:03d}.json", psalm)
        extracted_psalms.append({"number": h["number"], "title": h["title"], "verses": len(verses), "pages": pages_used, "notes": len(note_ids)})

    book_record = {
        "id": f"book-{book_no:02d}",
        "recordType": "book",
        "number": book_no,
        "title": book.get("title"),
        "archangel": archangel,
        "source": {"document": PDF.name, "pdfPages": [first, last]},
        "psalmIds": [f"book-{book_no:02d}-psalm-{p['number']:03d}" for p in extracted_psalms],
        "noteIds": all_notes,
        "validation": {"status": "machine-extracted-needs-review"},
    }
    write_json(book_dir / "book.json", book_record)
    report.append({"bookNumber": book_no, "title": book.get("title"), "archangel": archangel, "pdfPages": [first, last], "psalms": extracted_psalms, "noteCount": len(all_notes)})

write_json(REPORT, {"source": PDF.name, "scope": "books-01-10", "status": "machine-extracted-needs-review", "books": report})
print(f"Extracted {len(report)} books -> data/corpus/books/book-01..book-10")
