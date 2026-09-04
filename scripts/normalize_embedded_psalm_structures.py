#!/usr/bin/env python3
"""Normalize deterministic structures accidentally absorbed into Psalm verses.

Handled documentary patterns:
1. an internal numbered list that resets to 1 and then returns to the next Psalm verse;
2. a printed prayer marker ("Pr. N.") appended to the final Psalm verse;
3. the heading/cartouche of the following book appended to the final Psalm verse;
4. a printed editorial footnote block ("N - ...") appended to a verse while its
   marker N is attached to an earlier word in the Psalm.

The operation is structural only: no semantic/editorial guess is needed.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"
PRAYERS = ROOT / "data/prayers"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def infer_list_label(text: str, count: int) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    m = re.search(rf"\b{count}\s+([^:;.]+?)(?:\s*:|$)", compact, flags=re.IGNORECASE)
    if m:
        return f"{count} {m.group(1).strip()}"
    return f"Liste numérotée de {count} éléments"


def normalize_numbered_lists(record: dict) -> bool:
    verses = record.get("verses", [])
    if not isinstance(verses, list) or len(verses) < 4:
        return False
    changed = False
    while True:
        found = None
        for start in range(1, len(verses)):
            previous_number = verses[start - 1].get("number")
            if not isinstance(previous_number, int) or previous_number < 2 or verses[start].get("number") != 1:
                continue
            expected = 1
            end = start
            while end < len(verses) and verses[end].get("number") == expected:
                expected += 1
                end += 1
            count = expected - 1
            if count < 2 or end >= len(verses) or verses[end].get("number") != previous_number + 1:
                continue
            found = (start, end, previous_number, count)
            break
        if found is None:
            break
        start, end, after_verse, count = found
        items = verses[start:end]
        preceding = verses[start - 1]
        record.setdefault("embeddedLists", []).append({
            "afterVerse": after_verse,
            "label": infer_list_label(preceding.get("text", ""), count),
            "itemCount": count,
            "items": [{"number": item.get("number"), "text": item.get("text", ""), "sourcePages": item.get("sourcePages", [])} for item in items],
            "normalizationBasis": "number-reset-followed-by-main-sequence-resumption",
        })
        verses = verses[:start] + verses[end:]
        record["verses"] = verses
        record.setdefault("extraction", {})["embeddedNumberedListNormalized"] = True
        changed = True
    return changed


def normalize_inline_footnotes(record: dict) -> bool:
    verses = record.get("verses", [])
    if not verses:
        return False
    archangel = record.get("archangel")
    book_no = record.get("book", {}).get("number")
    psalm_id = record.get("id")
    if not archangel or not isinstance(book_no, int) or not psalm_id:
        return False

    existing_ids = list(record.get("noteIds", []))
    changed = False
    created = 0
    # Footnote blocks in the PDF text are separated from the Psalm sentence and
    # begin with a small marker followed by a dash. We only detach one when the
    # same marker can be located earlier as a superscript-like digit attached to
    # a word, which prevents ordinary numbered prose from being misclassified.
    footnote_re = re.compile(r"\s+(\d{1,2})\s*[\-‑–]\s+(.+)$", re.DOTALL)
    while True:
        candidate = None
        for host_index, host in enumerate(verses):
            text = host.get("text", "")
            m = footnote_re.search(text)
            if not m:
                continue
            marker = int(m.group(1))
            marker_re = re.compile(rf"(?<=[^\W\d_]){marker}(?=\W|$)", re.UNICODE)
            source_index = None
            for i in range(host_index, -1, -1):
                if marker_re.search(verses[i].get("text", "")):
                    source_index = i
                    break
            if source_index is None:
                continue
            candidate = (host_index, source_index, marker, m)
            break
        if candidate is None:
            break

        host_index, source_index, marker, m = candidate
        host = verses[host_index]
        source_verse = verses[source_index]
        footnote_text = m.group(2).strip()
        host["text"] = host.get("text", "")[:m.start()].rstrip()
        marker_re = re.compile(rf"(?<=[^\W\d_]){marker}(?=\W|$)", re.UNICODE)
        source_verse["text"] = marker_re.sub("", source_verse.get("text", ""), count=1)

        next_index = len(existing_ids) + created + 1
        note_id = f"{psalm_id}-note-{next_index:03d}"
        note = {
            "id": note_id,
            "recordType": "note",
            "archangel": archangel,
            "bookNumber": book_no,
            "appliesTo": {"recordId": psalm_id, "marker": marker, "verse": source_verse.get("number")},
            "text": footnote_text,
            "source": {
                "document": record.get("source", {}).get("document"),
                "pdfPage": (host.get("sourcePages") or source_verse.get("sourcePages") or [None])[0],
            },
            "validation": {"status": "machine-extracted-needs-review"},
        }
        write_json(NOTES / f"book-{book_no:02d}" / f"{note_id}.json", note)
        record.setdefault("noteIds", []).append(note_id)
        record.setdefault("extraction", {})["inlineEditorialFootnoteNormalized"] = True
        created += 1
        changed = True
    return changed


def normalize_appended_prayer(record: dict) -> bool:
    verses = record.get("verses", [])
    if not verses:
        return False
    final = verses[-1]
    text = final.get("text", "")
    match = re.search(r"\s+Pr\.\s*(\d+)\.\s+", text)
    if not match:
        return False
    prayer_number = int(match.group(1))
    psalm_text = text[: match.start()].strip()
    prayer_text = text[match.end() :].strip()
    if not psalm_text or not prayer_text:
        return False
    final["text"] = psalm_text
    archangel = record.get("archangel")
    book_no = record.get("book", {}).get("number")
    psalm_id = record.get("id")
    if not archangel or not isinstance(book_no, int) or not psalm_id:
        raise RuntimeError(f"Incomplete Psalm metadata for appended prayer in {psalm_id!r}")
    prayer_id = f"{archangel}-book-{book_no:02d}-prayer-{prayer_number:03d}"
    pages = sorted({p for p in final.get("sourcePages", []) if isinstance(p, int)})
    prayer = {
        "id": prayer_id,
        "recordType": "master-prayer",
        "archangel": archangel,
        "bookNumber": book_no,
        "number": prayer_number,
        "speakerId": "olivier-manitara",
        "text": prayer_text,
        "source": {"document": record.get("source", {}).get("document"), "printedPages": pages},
        "appliesToPsalmId": psalm_id,
        "attachment": {"basis": "printed-prayer-marker-and-editorial-adjacency", "description": f"Prayer {prayer_number} is printed immediately after {psalm_id} and begins with marker 'Pr. {prayer_number}.'\."},
        "validation": {"status": "machine-extracted-needs-human-review"},
    }
    write_json(PRAYERS / f"{prayer_id}.json", prayer)
    prayer_ids = record.setdefault("prayerIds", [])
    if prayer_id not in prayer_ids:
        prayer_ids.append(prayer_id)
    record.setdefault("extraction", {})["appendedPrayerNormalized"] = True
    return True


def normalize_appended_book_heading(record: dict) -> bool:
    verses = record.get("verses", [])
    if not verses:
        return False
    final = verses[-1]
    text = final.get("text", "")
    match = re.search(r"\s+L\s*I\s*V\s*R\s*E\s+\d+\b", text, flags=re.IGNORECASE)
    if not match:
        return False
    psalm_text = text[: match.start()].strip()
    if not psalm_text:
        return False
    final["text"] = psalm_text
    record.setdefault("extraction", {})["appendedNextBookHeadingNormalized"] = True
    return True


changed_records = 0
lists_moved = 0
footnotes_split = 0
prayers_split = 0
book_headings_stripped = 0
for path in sorted(BOOKS.glob("book-*/psalm-*.json")):
    record = json.loads(path.read_text(encoding="utf-8"))
    before_lists = len(record.get("embeddedLists", []))
    changed_list = normalize_numbered_lists(record)
    lists_moved += max(0, len(record.get("embeddedLists", [])) - before_lists)
    changed_footnotes = normalize_inline_footnotes(record)
    footnotes_split += int(changed_footnotes)
    changed_prayer = normalize_appended_prayer(record)
    prayers_split += int(changed_prayer)
    changed_heading = normalize_appended_book_heading(record)
    book_headings_stripped += int(changed_heading)
    if changed_list or changed_footnotes or changed_prayer or changed_heading:
        write_json(path, record)
        changed_records += 1

print(
    f"Normalized {changed_records} Psalms: {lists_moved} embedded numbered lists, "
    f"{footnotes_split} Psalms with detached editorial footnotes, {prayers_split} appended prayers, "
    f"{book_headings_stripped} appended next-book headings"
)
