#!/usr/bin/env python3
"""Recover psalm text around footnotes and keep editorial notes out of verses.

Handles two deterministic pdftotext layout cases:
1. main psalm text resumes after a bottom-of-page footnote;
2. an editorial footnote itself continues at the top of the next PDF page before
   the next numbered verse, while that continuation was accidentally appended to
   a later psalm verse by the base extractor.

Repairs are source-backed: the PDF page layout must confirm the expected verse or
continued note text before corpus JSON is changed.
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


def continued_note_prefix(book_no: int, psalm_no: int, note_page: int) -> str:
    """Return PDF-confirmed note continuation before the first next-page verse.

    A continued footnote has no new marker on the next page and appears before the
    next numbered psalm verse. We only accept it when that next numbered verse is
    exactly one greater than a verse already present in the psalm. This prevents a
    page header or a new psalm title from being interpreted as note text.
    """
    psalm_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{psalm_no:03d}.json"
    if not psalm_path.exists():
        return ""
    psalm = read(psalm_path)
    nums = {v.get("number") for v in psalm.get("verses", []) if isinstance(v.get("number"), int)}
    pages = pdf_pages(note_page + 1, note_page + 1)
    if not pages:
        return ""
    text = clean_page(book_no, note_page + 1, pages[0][1])
    first_verse = re.search(r"(?m)^\s*(\d{1,3})\.\s+", text)
    if not first_verse:
        return ""
    number = int(first_verse.group(1))
    if number not in nums or (number - 1) not in nums:
        return ""
    prefix = unwrap(text[:first_verse.start()])
    # Reject headings / substantial blocks; a footnote continuation is a short
    # sentence fragment at the top of the immediately following page.
    if not prefix or len(prefix) > 500 or re.search(r"(?i)\b(psaume|livre)\b", prefix):
        return ""
    return prefix


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

# Pass 1: recover main text accidentally swallowed by a footnote.
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
    psalm_no = int(record_id.rsplit('-', 1)[-1])
    psalm_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{psalm_no:03d}.json"
    if not psalm_path.exists():
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "reason": "missing-psalm"})
        continue
    psalm = read(psalm_path)
    current_numbers = [v.get("number") for v in psalm.get("verses", []) if isinstance(v.get("number"), int)]
    if not current_numbers:
        continue
    expected = max(current_numbers) + 1
    if int(match.group(1)) != expected:
        continue
    resume = source_resume(book_no, psalm.get("number"), note_page, expected)
    if not resume:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "expectedVerse": expected, "reason": "next-verse-not-confirmed-in-source"})
        continue
    continuation, resume_page, recovered = resume
    if not recovered or recovered[0]["number"] != expected:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "expectedVerse": expected, "reason": "source-recovery-empty"})
        continue
    clean_note = source_note_text(book_no, note_page, marker)
    if not clean_note:
        unresolved.append({"path": str(note_path.relative_to(ROOT)), "recordId": record_id, "reason": "cannot-recover-source-note"})
        continue
    note["text"] = clean_note
    last_verse = max(psalm["verses"], key=lambda v: v.get("number", 0))
    if continuation:
        last_text = last_verse.get("text", "").rstrip()
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
    psalm.setdefault("source", {})["pdfPages"] = sorted({p for v in psalm["verses"] for p in v.get("sourcePages", [])})
    write(psalm_path, psalm); write(note_path, note)
    repairs.append({"recordId": record_id, "noteId": note.get("id"), "recoveredVerses": [v["number"] for v in recovered]})

# Pass 2: recover a footnote continued at the top of the next page and remove that
# exact source-backed fragment if the extractor appended it to a psalm verse.
for note_path in sorted(NOTES.glob("book-*/*.json")):
    note = read(note_path)
    applies = note.get("appliesTo", {})
    record_id = applies.get("recordId")
    book_no = note.get("bookNumber")
    marker = applies.get("marker")
    note_page = note.get("source", {}).get("pdfPage")
    if not record_id or not isinstance(book_no, int) or not isinstance(marker, int) or not isinstance(note_page, int):
        continue
    psalm_no = int(record_id.rsplit('-', 1)[-1])
    prefix = continued_note_prefix(book_no, psalm_no, note_page)
    if not prefix:
        continue
    base_note = source_note_text(book_no, note_page, marker)
    if not base_note:
        continue
    full_note = unwrap(base_note + " " + prefix)
    psalm_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{psalm_no:03d}.json"
    psalm = read(psalm_path)
    removed_from = []
    for verse in psalm.get("verses", []):
        text = verse.get("text", "")
        if prefix in text:
            cleaned = unwrap(text.replace(prefix, " "))
            if cleaned != text:
                verse["text"] = cleaned
                removed_from.append(verse.get("number"))
    if note.get("text") != full_note or removed_from:
        note["text"] = full_note
        note.setdefault("validation", {})["continuedAcrossPageNormalized"] = True
        psalm.setdefault("extraction", {})["continuedFootnoteNormalized"] = True
        write(note_path, note); write(psalm_path, psalm)
        repairs.append({"recordId": record_id, "noteId": note.get("id"), "continuedNotePage": note_page + 1, "removedFromVerses": removed_from})

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
