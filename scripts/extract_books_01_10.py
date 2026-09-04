#!/usr/bin/env python3
"""Extract books 1-10 from the source PDF into structured corpus records.

Psalm numbering continues by Archangel across successive books. Real headings are
selected from the expected Archangel sequence and anchored to a nearby verse 1 reset,
which rejects introduction/prose numbers and tolerates imperfect PDF typography.
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
    value = re.sub(r"^([A-ZÀ-ÖØ-Ý])\s+([a-zà-öø-ÿ])", r"\1\2", value)
    for a, b in (("M ichaël", "Michaël"), ("R aphaël", "Raphaël"), ("G abriel", "Gabriel"), ("O uriel", "Ouriel")):
        value = value.replace(a, b)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([’'])\s+", r"\1", value)
    value = re.sub(r"\s+-\s*", "-", value)
    value = re.sub(r"\s+d\s+[’']", " d’", value)
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


def page_bounds(text: str, page: int) -> tuple[int, int] | None:
    marker = re.search(rf"\[\[PAGE {page}\]\]", text)
    if not marker:
        return None
    nxt = re.search(r"\[\[PAGE \d+\]\]", text[marker.end():])
    return marker.end(), marker.end() + (nxt.start() if nxt else len(text) - marker.end())


def raw_heading_candidates(text: str, first_page: int) -> list[dict]:
    """Detect numbered title lines. Numbered verses use `N.` and are excluded."""
    out = []
    offset = 0
    lines = text.splitlines(True)
    for i, raw_line in enumerate(lines):
        s = re.sub(r"\s+", " ", raw_line).strip()
        m = re.match(r"^(\d{1,3})\s+(?![.])(.{2,160})$", s)
        if m:
            title = m.group(2).strip()
            low = title.lower()
            if "livre " not in low and "note des hiérogrammates" not in low and not title.startswith("-") and len(title.split()) <= 24:
                out.append({"number": int(m.group(1)), "title": clean_title(title), "offset": offset, "page": page_at(text, offset, first_page), "basis": "numbered-line"})
        elif re.fullmatch(r"\s*\d{1,3}\s*", raw_line):
            number = int(raw_line.strip())
            for j in range(i + 1, min(i + 4, len(lines))):
                nxt = re.sub(r"\s+", " ", lines[j]).strip()
                if not nxt or nxt.startswith("[[PAGE"):
                    continue
                if len(nxt.split()) <= 24 and not re.match(r"^\d{1,3}[.]\s", nxt):
                    out.append({"number": number, "title": clean_title(nxt), "offset": offset, "page": page_at(text, offset, first_page), "basis": "split-number-title"})
                break
        offset += len(raw_line)
    return out


def add_inventory_candidates(text: str, book: dict, candidates: list[dict]) -> None:
    """Use the earlier page inventory as a fallback locator for typographically odd titles."""
    for item in book.get("psalmHeadingCandidates", []):
        number = item.get("number")
        page = item.get("pdfPage")
        if not isinstance(number, int) or not isinstance(page, int):
            continue
        bounds = page_bounds(text, page)
        if not bounds:
            continue
        start, end = bounds
        page_text_value = text[start:end]
        line_match = re.search(rf"(?m)^\s*{number}\s+(?![.])([^\n]+)$", page_text_value)
        if not line_match:
            continue
        absolute = start + line_match.start()
        candidates.append({
            "number": number,
            "title": clean_title(item.get("titleCandidate") or line_match.group(1)),
            "offset": absolute,
            "page": page,
            "basis": "inventory-page-anchor",
        })


def verse_one_distance(text: str, offset: int, limit: int = 3500) -> int | None:
    window = text[offset:min(len(text), offset + limit)]
    m = re.search(r"(?m)^\s*1\.\s+", window)
    return m.start() if m else None


def infer_missing_heading(text: str, number: int, lower_offset: int, upper_offset: int | None, first_page: int) -> dict | None:
    """Recover a missing heading from a verse-1 reset between adjacent known psalms."""
    end = upper_offset if upper_offset is not None else len(text)
    window = text[lower_offset:end]
    resets = list(re.finditer(r"(?m)^\s*1\.\s+", window))
    if not resets:
        return None
    # If the previous psalm is correctly bounded, the next verse-1 reset belongs to the missing psalm.
    reset = resets[-1] if len(resets) > 1 else resets[0]
    absolute_reset = lower_offset + reset.start()
    before = text[max(lower_offset, absolute_reset - 1000):absolute_reset]
    lines = [re.sub(r"\s+", " ", x).strip() for x in before.splitlines()]
    lines = [x for x in lines if x and not x.startswith("[[PAGE") and not re.match(r"^\d{1,3}\.\s", x)]
    title = None
    title_offset = absolute_reset
    for line in reversed(lines[-8:]):
        m = re.match(rf"^{number}\s+(?![.])(.+)$", line)
        if m:
            title = clean_title(m.group(1)); break
    if not title and lines:
        candidate = lines[-1]
        if len(candidate.split()) <= 24 and not candidate.endswith((".", ";")):
            title = clean_title(re.sub(rf"^{number}\s+", "", candidate))
    if not title:
        return None
    # Locate the beginning of that title line approximately.
    local = text.rfind(title.split()[0], max(lower_offset, absolute_reset - 1000), absolute_reset)
    if local >= 0:
        title_offset = local
    return {"number": number, "title": title, "offset": title_offset, "page": page_at(text, title_offset, first_page), "basis": "verse-one-reset-inference"}


def choose_headings(text: str, candidates: list[dict], expected_start: int, first_page: int) -> list[dict]:
    by_number: dict[int, list[dict]] = {}
    for h in candidates:
        if h["number"] >= expected_start:
            key = (h["number"], h["offset"])
            if not any((x["number"], x["offset"]) == key for x in by_number.get(h["number"], [])):
                by_number.setdefault(h["number"], []).append(h)

    chosen: list[dict] = []
    prev_offset = -1
    number = expected_start
    misses = 0
    max_candidate = max(by_number, default=expected_start - 1)
    while number <= max_candidate:
        options = [h for h in by_number.get(number, []) if h["offset"] > prev_offset]
        if options:
            # True psalm headings are followed closely by verse 1. Prefer the smallest distance.
            scored = []
            for h in options:
                d = verse_one_distance(text, h["offset"])
                scored.append((d is None, d if d is not None else 10**9, h["offset"], h))
            h = min(scored, key=lambda x: x[:3])[3]
            chosen.append(h)
            prev_offset = h["offset"]
            misses = 0
        else:
            misses += 1
            if chosen and misses >= 4:
                break
        number += 1

    # Recover single internal gaps from verse-1 resets between known neighbors.
    changed = True
    while changed:
        changed = False
        chosen.sort(key=lambda h: h["number"])
        numbers = [h["number"] for h in chosen]
        for n in range(expected_start, max(numbers, default=expected_start - 1) + 1):
            if n in numbers or n - 1 not in numbers or n + 1 not in numbers:
                continue
            prev = next(h for h in chosen if h["number"] == n - 1)
            nxt = next(h for h in chosen if h["number"] == n + 1)
            inferred = infer_missing_heading(text, n, prev["offset"], nxt["offset"], first_page)
            if inferred:
                chosen.append(inferred); changed = True; break
    return sorted(chosen, key=lambda h: h["offset"])


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
selected = [b for b in inventory["books"] if 1 <= b["bookNumber"] <= 10]
report = []
next_expected = {"michael": 1, "gabriel": 1, "raphael": 1, "ouriel": 1}

for book in selected:
    book_no = book["bookNumber"]
    first, last = book["pdfPages"]
    raw_pages = page_text(first, last)
    archangel = detect_archangel(raw_pages)
    if archangel not in next_expected:
        raise RuntimeError(f"Unable to determine Archangel for book {book_no}")
    expected_start = next_expected[archangel]
    text = "".join(f"\n[[PAGE {page_no}]]\n{clean_page(book_no, page_no, raw)}" for page_no, raw in raw_pages)

    candidates = raw_heading_candidates(text, first)
    add_inventory_candidates(text, book, candidates)
    chosen = choose_headings(text, candidates, expected_start, first)
    if not chosen:
        raise RuntimeError(f"No psalm headings found for book {book_no} from expected {expected_start}")

    book_dir = ROOT / "data/corpus/books" / f"book-{book_no:02d}"
    note_dir = ROOT / "data/notes/books" / f"book-{book_no:02d}"
    book_dir.mkdir(parents=True, exist_ok=True); note_dir.mkdir(parents=True, exist_ok=True)
    for stale in book_dir.glob("psalm-*.json"): stale.unlink()
    for stale in note_dir.glob("*.json"): stale.unlink()

    extracted_psalms = []
    all_notes = []
    for i, h in enumerate(chosen):
        start = h["offset"]
        end = chosen[i + 1]["offset"] if i + 1 < len(chosen) else len(text)
        segment = text[start:end]
        segment_body = segment.split("\n", 1)[1] if "\n" in segment else ""
        note_pattern = re.compile(r"(?ms)^\s*(\d+)\s*-\s+(.*?)(?=^\s*\d+\s*-\s+|\Z)")
        notes = [{"marker": int(nm.group(1)), "text": unwrap(strip_markers(nm.group(2))), "page": page_at(segment_body, nm.start(), h["page"])} for nm in note_pattern.finditer(segment_body)]
        body = note_pattern.sub("", segment_body)
        verse_matches = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", body))
        verses = []
        for vi, vm in enumerate(verse_matches):
            vend = verse_matches[vi + 1].start() if vi + 1 < len(verse_matches) else len(body)
            vtext = unwrap(strip_markers(body[vm.end():vend]))
            if vtext:
                verses.append({"number": int(vm.group(1)), "text": vtext, "sourcePages": [page_at(body, vm.start(), h["page"])]})
        if not verses or verses[0]["number"] != 1:
            continue

        note_ids = []
        for ni, note in enumerate(notes, 1):
            note_id = f"book-{book_no:02d}-psalm-{h['number']:03d}-note-{ni:03d}"
            note_ids.append(note_id); all_notes.append(note_id)
            write_json(note_dir / f"{note_id}.json", {
                "id": note_id, "recordType": "note", "archangel": archangel, "bookNumber": book_no,
                "appliesTo": {"recordId": f"book-{book_no:02d}-psalm-{h['number']:03d}", "marker": note["marker"], "verse": None},
                "text": note["text"], "source": {"document": PDF.name, "pdfPage": note["page"]},
                "validation": {"status": "machine-extracted-needs-review"},
            })
        pages_used = sorted({p for v in verses for p in v["sourcePages"]})
        write_json(book_dir / f"psalm-{h['number']:03d}.json", {
            "id": f"book-{book_no:02d}-psalm-{h['number']:03d}", "recordType": "psalm", "archangel": archangel,
            "book": {"number": book_no, "title": book.get("title")}, "number": h["number"], "title": h["title"],
            "source": {"document": PDF.name, "pdfPages": pages_used}, "verses": verses, "noteIds": note_ids,
            "extraction": {"headingBasis": h.get("basis")},
            "validation": {"status": "machine-extracted-needs-review", "checks": {"verseCount": len(verses), "verseSequenceStartsAtOne": True}},
        })
        extracted_psalms.append({"number": h["number"], "title": h["title"], "verses": len(verses), "pages": pages_used, "notes": len(note_ids), "headingBasis": h.get("basis")})

    if extracted_psalms:
        next_expected[archangel] = max(p["number"] for p in extracted_psalms) + 1
    write_json(book_dir / "book.json", {
        "id": f"book-{book_no:02d}", "recordType": "book", "number": book_no, "title": book.get("title"), "archangel": archangel,
        "source": {"document": PDF.name, "pdfPages": [first, last]},
        "psalmIds": [f"book-{book_no:02d}-psalm-{p['number']:03d}" for p in extracted_psalms], "noteIds": all_notes,
        "numbering": {"expectedStart": expected_start, "nextExpected": next_expected[archangel]},
        "validation": {"status": "machine-extracted-needs-review"},
    })
    report.append({"bookNumber": book_no, "title": book.get("title"), "archangel": archangel, "expectedStart": expected_start, "pdfPages": [first, last], "psalms": extracted_psalms, "noteCount": len(all_notes)})

write_json(REPORT, {"source": PDF.name, "scope": "books-01-10", "status": "machine-extracted-needs-review", "books": report})
print(f"Extracted {len(report)} books with verse-one anchored headings")
