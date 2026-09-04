#!/usr/bin/env python3
"""Recover psalm text that resumes after a bottom-of-page footnote.

`pdftotext -layout` can place a footnote after a partial verse and then continue the
main text on the next PDF page. The base extractor historically attached everything
following `N - ...` to the note, so the continuation and later numbered verses vanished
from the psalm record.

This normalizer is documentary rather than heuristic: a case is repaired only when
1) a note contains a verse-like number equal to the next expected psalm verse, and
2) that same numbered verse is found in the source PDF on the page(s) immediately after
   the footnote and before the next psalm heading.
The note itself is re-read from its printed footnote line on the source page.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"
VERSE_LIKE = re.compile(r"(?:^|\s)(\d{1,3})\.\s+[A-ZÀ-ÖØ-ÝÉÈÊÎÔÛÇ]")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unwrap(value: str) -> str:
    value = re.sub(r"-\n\s*", "", value)
    value = re.sub(r"\n\s*", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def pdf_pages(first: int, last: int) -> list[tuple[int, str]]:
    raw = subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return [(first + i, page) for i, page in enumerate(raw.split("\f")) if page.strip()]


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


def source_note_text(book_no: int, page_no: int, marker: int) -> str | None:
    pages = pdf_pages(page_no, page_no)
    if not pages:
        return None
    text = clean_page(book_no, page_no, pages[0][1])
    m = re.search(rf"(?ms)^\s*{marker}\s*-\s+(.*?)(?=^\s*\d+\s*-\s+|\Z)", text)
    return unwrap(m.group(1)) if m else None


def next_psalm_start(book_no: int, psalm_no: int, fallback: int) -> tuple[int, int | None]:
    book_dir = CORPUS / f"book-{book_no:02d}"
    candidates = []
    for p in book_dir.glob("psalm-*.json"):
        d = read(p)
        if isinstance(d.get("number"), int) and d["number"] > psalm_no:
            pages = d.get("source", {}).get("pdfPages", [])
            if pages:
                candidates.append((d["number"], pages[0]))
    if not candidates:
        return fallback + 2, None
    number, page = min(candidates)
    return page, number


def source_resume(book_no: int, psalm_no: int, note_page: int, expected: int) -> tuple[str, int, list[dict]] | None:
    next_page, next_number = next_psalm_start(book_no, psalm_no, note_page)
    first = note_page + 1
    last = max(first, next_page)
    pages = pdf_pages(first, last)
    if not pages:
        return None

    chunks = []
    for page_no, raw in pages:
        chunks.append(f"\n[[PAGE {page_no}]]\n{clean_page(book_no, page_no, raw)}")
    text = "".join(chunks)

    # Do not cross into the next psalm, even when it starts on the same page.
    if next_number is not None:
        heading = re.search(rf"(?m)^\s*{next_number}\s+(?![.]).+$", text)
        if heading:
            text = text[:heading.start()]

    expected_match = re.search(rf"(?m)^\s*{expected}\.\s+", text)
    if not expected_match:
        return None

    continuation_raw = re.sub(r"\[\[PAGE \d+\]\]", "", text[:expected_match.start()])
    continuation = unwrap(continuation_raw)
    matches = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", text[expected_match.start():]))
    verses = []
    base = expected_match.start()
    for i, vm in enumerate(matches):
        absolute_start = base + vm.start()
        absolute_end = base + (matches[i + 1].start() if i + 1 < len(matches) else len(text) - base)
        number = int(vm.group(1))
        if verses and number != verses[-1]["number"] + 1:
            break
        if not verses and number != expected:
            break
        body_start = base + vm.end()
        body = re.sub(r"\[\[PAGE \d+\]\]", "", text[body_start:absolute_end])
        value = unwrap(body)
        if value:
            verses.append({"number": number, "text": value, "sourcePages": [page_at(text, absolute_start, first)]})
    return continuation, first, verses


repairs = []
unresolved = []

for note_path in sorted(NOTES.glob("book-*/*.json")):
    note = read(note_path)
    match = VERSE_LIKE.search(note.get("text", ""))
    if not match:
        continue

    applies = note.get("appliesTo", {})
    record_id = applies.get("recordId")
    book_no = note.get("bookNumber")
    marker = applies.get("marker")
    note_page = note.get("source", {}).get("pdfPage")
    if not record_id or not isinstance(book_no, int) or not isinstance(marker, int) or not isinstance(note_page, int):
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "reason": "missing-note-metadata"})
        continue

    psalm_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{int(record_id.rsplit('-', 1)[-1]):03d}.json"
    if not psalm_path.exists():
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "reason": "missing-psalm"})
        continue
    psalm = read(psalm_path)
    current_numbers = [v.get("number") for v in psalm.get("verses", []) if isinstance(v.get("number"), int)]
    if not current_numbers:
        continue
    expected = max(current_numbers) + 1
    verse_like = int(match.group(1))
    if verse_like != expected:
        # A number inside an editorial note is harmless unless it is exactly the next
        # missing verse. It is retained as note content.
        continue

    resume = source_resume(book_no, psalm.get("number"), note_page, expected)
    if not resume:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "expectedVerse": expected, "reason": "next-verse-not-confirmed-in-source"})
        continue
    continuation, resume_page, recovered = resume
    if not recovered or recovered[0]["number"] != expected:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "expectedVerse": expected, "reason": "source-recovery-empty"})
        continue

    # Re-read the actual bottom-of-page note so resumed main text is never kept in it.
    clean_note = source_note_text(book_no, note_page, marker)
    if not clean_note:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "reason": "cannot-recover-source-note"})
        continue
    note["text"] = clean_note

    last_verse = max(psalm["verses"], key=lambda v: v.get("number", 0))
    if continuation:
        last_text = last_verse.get("text", "").rstrip()
        # Append only when the source continuation is not already present.
        if continuation not in last_text:
            last_verse["text"] = unwrap(last_text + " " + continuation)
            pages = set(last_verse.get("sourcePages", [])); pages.add(resume_page)
            last_verse["sourcePages"] = sorted(pages)

    existing = {v.get("number"): v for v in psalm.get("verses", [])}
    for verse in recovered:
        existing[verse["number"]] = verse
    psalm["verses"] = [existing[n] for n in sorted(existing) if isinstance(n, int)]
    psalm.setdefault("extraction", {})["resumedVerseAfterFootnoteNormalized"] = True
    psalm.setdefault("validation", {}).setdefault("checks", {})["verseCount"] = len(psalm["verses"])
    pages = sorted({p for v in psalm["verses"] for p in v.get("sourcePages", [])})
    psalm.setdefault("source", {})["pdfPages"] = pages

    write(psalm_path, psalm)
    write(note_path, note)
    repairs.append({"recordId": record_id, "noteId": note.get("id"), "recoveredVerses": [v["number"] for v in recovered]})

# Guardrail: a note that still contains exactly the next missing verse must not pass.
remaining = []
for note_path in sorted(NOTES.glob("book-*/*.json")):
    note = read(note_path)
    found = VERSE_LIKE.search(note.get("text", ""))
    if not found:
        continue
    record_id = note.get("appliesTo", {}).get("recordId")
    book_no = note.get("bookNumber")
    if not record_id or not isinstance(book_no, int):
        continue
    try:
        number = int(record_id.rsplit('-', 1)[-1])
    except ValueError:
        continue
    psalm_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{number:03d}.json"
    if not psalm_path.exists():
        continue
    psalm = read(psalm_path)
    nums = [v.get("number") for v in psalm.get("verses", []) if isinstance(v.get("number"), int)]
    if nums and int(found.group(1)) == max(nums) + 1:
        remaining.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "nextMissingVerse": max(nums) + 1})

print(json.dumps({"repaired": repairs, "unresolved": unresolved, "remaining": remaining}, ensure_ascii=False, indent=2))
if unresolved or remaining:
    raise SystemExit("Footnote/main-text recovery still has unresolved documentary cases")
