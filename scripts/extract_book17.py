#!/usr/bin/env python3
"""Extract Michaël book 17 (psalms 105-130) into reviewable JSON records."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
FIRST_PAGE, LAST_PAGE = 1071, 1194
TITLES = {
    105: "Aux infidèles",
    106: "Comment discerner le vrai du faux",
    107: "Ne te laisse pas séduire par un monde artificiel",
    108: "Honore ton Père et ta Mère",
    109: "L’homme-girouette",
    110: "L’équilibre des mondes",
    111: "Dans la nutrition, les plus grands secrets de l’univers",
    112: "N’attendez pas d’être purs, soyez vrais",
    113: "Retrouve la terre de ta tradition",
    114: "Les rois de la Lumière",
    115: "Comment former ton corps d’éternité",
    116: "Les dangers de l’intelligence technologique",
    117: "Une œuvre primordiale pour l’humanité",
    118: "5 questions fondamentales à se poser",
    119: "La grande règle pour s’approcher du monde divin",
    120: "Le cercle du Bien commun",
    121: "L’heure du choix",
    122: "Le temple vivant de la Mère",
    123: "Le vrai et l’imitation du vrai",
    124: "La flamme perpétuelle de la conscience",
    125: "Le monde divin envoie son Fils",
    126: "Enlever le masque de l’hypocrisie",
    127: "Dites non à la barbarie des hommes",
    128: "Les Évangiles esséniens, une sagesse à vivre",
    129: "Ne pesez pas sur le monde, allégez votre vie",
    130: "La porte du culte du feu",
}


def unwrap(value: str) -> str:
    value = re.sub(r"-\n\s*", "", value)
    value = re.sub(r"\n\s*", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_pages() -> list[tuple[int, str]]:
    result = subprocess.run(
        ["pdftotext", "-layout", "-f", str(FIRST_PAGE), "-l", str(LAST_PAGE), str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return [(FIRST_PAGE + index, page) for index, page in enumerate(result.split("\f")) if page.strip()]


def clean_page(page: int, raw: str) -> tuple[str, list[dict]]:
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("Livre 17 |") or stripped == str(page):
            continue
        lines.append(line)
    text = "\n".join(lines)
    notes = []
    pattern = re.compile(r"(?ms)^\s*(\d+)\s*-\s+(.*?)(?=^\s*\d+\s*-\s+|\Z)")
    for match in pattern.finditer(text):
        notes.append({"marker": int(match.group(1)), "text": unwrap(match.group(2)), "page": page})
    return pattern.sub("", text), notes


def page_at(segment: str, offset: int, default: int = FIRST_PAGE) -> int:
    markers = list(re.finditer(r"\[\[PAGE (\d+)\]\]", segment[:offset]))
    return int(markers[-1].group(1)) if markers else default


def without_markers(value: str) -> str:
    return re.sub(r"\[\[PAGE \d+\]\]", "", value)


def temporal_mentions(value: str, verse: int | None = None) -> list[dict]:
    found = []
    for year in re.findall(r"\b(?:19|20)\d{2}(?:-\d{2,4})?\b", value):
        found.append({"value": year, "kind": "year-or-period", "verse": verse})
    months = "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"
    for month in re.findall(rf"(?i)\b(?:{months})\b", value):
        found.append({"value": month.lower(), "kind": "month", "verse": verse})
    return found


def write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


pages, page_notes = [], []
for page_number, raw_page in extract_pages():
    cleaned, notes = clean_page(page_number, raw_page)
    pages.append(f"\n[[PAGE {page_number}]]\n{cleaned}")
    page_notes.extend(notes)
book = "".join(pages)

headings = []
for match in re.finditer(r"(?m)^\s*(10[5-9]|11\d|12\d|130)\s+(?![.])[^\n]+$", book):
    number = int(match.group(1))
    if number in TITLES and not any(item[0] == number for item in headings):
        headings.append((number, match.start(), match.end()))
headings.sort(key=lambda item: item[1])
if [item[0] for item in headings] != list(range(105, 131)):
    raise RuntimeError(f"Psalm headings incomplete: {[item[0] for item in headings]}")

summary = []
for index, (number, start, heading_end) in enumerate(headings):
    segment_end = headings[index + 1][1] if index + 1 < len(headings) else len(book)
    segment = book[start:segment_end]
    start_page = page_at(book, start)
    prayer_match = re.search(r"(?m)^\s*Pr\.\s*(\d+)\.\s*", segment)
    body_end = prayer_match.start() if prayer_match else len(segment)
    body = segment[heading_end - start:body_end]

    interludes = []
    cue_pattern = re.compile(r"(?ims)(Olivier Manitara demanda(?: alors)?[^:]{0,180}:)\s*(.*?)(?=^\s*\d{1,3}\.\s+)")
    for cue in list(cue_pattern.finditer(body)):
        before = body[:cue.start()]
        previous = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", before))
        after = re.search(r"(?m)^\s*(\d{1,3})\.\s+", body[cue.end():])
        interludes.append({
            "id": f"michael-psalm-{number:03d}-dialogue-{len(interludes)+1:03d}",
            "speakerId": "olivier-manitara",
            "speechRole": "question",
            "text": unwrap(without_markers(cue.group(2))),
            "numbering": "unnumbered-interlude",
            "verseNumber": None,
            "positionAfterVerse": int(previous[-1].group(1)) if previous else None,
            "positionBeforeVerse": int(after.group(1)) if after else None,
            "editorialCue": unwrap(cue.group(1)),
            "sourcePages": [page_at(segment, cue.start(), start_page)],
        })
    body = cue_pattern.sub("", body)

    verse_matches = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+", body))
    verses, dialogues = [], list(interludes)
    for verse_index, match in enumerate(verse_matches):
        verse_number = int(match.group(1))
        end = verse_matches[verse_index + 1].start() if verse_index + 1 < len(verse_matches) else len(body)
        verse_text = unwrap(without_markers(body[match.end():end]))
        if not verse_text:
            continue
        is_question = bool(re.search(r"(?i)^[^?!.]{0,120}\bpère\b", verse_text)) and "?" in verse_text
        role = "question" if is_question else "teaching"
        if dialogues and any(d.get("positionBeforeVerse") == verse_number for d in dialogues):
            role = "answer"
        elif any(v["speechRole"] == "question" for v in verses):
            role = "answer"
        verse_page = page_at(body, match.start(), start_page)
        verses.append({"number": verse_number, "speakerId": "olivier-manitara" if is_question else "archangel-michael", "speechRole": role, "text": verse_text, "sourcePages": [verse_page]})
        if is_question:
            dialogues.append({
                "id": f"michael-psalm-{number:03d}-dialogue-{len(dialogues)+1:03d}",
                "speakerId": "olivier-manitara", "speechRole": "question", "text": verse_text,
                "numbering": "numbered-verse", "verseNumber": verse_number, "positionAfterVerse": verse_number - 1,
                "recognitionBasis": ["address-to-father", "interrogative-form", "editorial-rule-questions-addressed-to-archangel"],
                "sourcePages": [verse_page],
            })
    numbers = [verse["number"] for verse in verses]
    sequence_complete = numbers == list(range(1, max(numbers, default=0) + 1))

    psalm_end_page = max((p for verse in verses for p in verse["sourcePages"]), default=start_page)
    related_notes = [note for note in page_notes if start_page <= note["page"] <= psalm_end_page]
    note_ids, note_records = [], []
    for note_index, note in enumerate(related_notes, 1):
        note_id = f"michael-psalm-{number:03d}-note-{note_index:03d}"
        candidates = [v["number"] for v in verses if re.search(rf"\w{note['marker']}(?:\W|$)", v["text"])]
        temporal = [{"value": value, "kind": "year-or-period"} for value in re.findall(r"\b(?:19|20)\d{2}(?:-\d{2,4})?\b", note["text"])]
        note_records.append({
            "id": note_id, "recordType": "note", "archangel": "michael",
            "appliesTo": {"recordId": f"michael-psalm-{number:03d}", "verse": candidates[0] if len(candidates) == 1 else None, "marker": note["marker"]},
            "text": note["text"], "source": {"document": PDF.name, "printedPage": note["page"]},
            "temporalMentions": temporal, "validation": {"status": "machine-extracted-needs-human-review"},
        })
        note_ids.append(note_id)

    prayer_ids = []
    if prayer_match:
        prayer_number = int(prayer_match.group(1))
        prayer_page = page_at(segment, prayer_match.start(), start_page)
        prayer_raw = segment[prayer_match.end():]
        prayer_text = unwrap(without_markers(prayer_raw))
        prayer_pages = {prayer_page}
        for page_match in re.finditer(r"(?s)\[\[PAGE (\d+)\]\](.*?)(?=\[\[PAGE|\Z)", prayer_raw):
            if without_markers(page_match.group(2)).strip():
                prayer_pages.add(int(page_match.group(1)))
        prayer_id = f"michael-book-17-prayer-{prayer_number:03d}"
        prayer_ids.append(prayer_id)
        prayer_record = {
            "id": prayer_id, "recordType": "master-prayer", "archangel": "michael", "bookNumber": 17,
            "number": prayer_number, "speakerId": "olivier-manitara", "text": prayer_text,
            "source": {"document": PDF.name, "printedPages": sorted(prayer_pages)},
            "appliesToPsalmId": f"michael-psalm-{number:03d}",
            "attachment": {"basis": "editorial-adjacency", "description": f"La prière {prayer_number} est imprimée immédiatement après le psaume {number}."},
            "temporalMentions": temporal_mentions(prayer_text),
            "validation": {"status": "machine-extracted-needs-human-review"},
        }
        if number != 105:
            write(ROOT / "data/prayers" / f"{prayer_id}.json", prayer_record)

    psalm_temporal = [mention for verse in verses for mention in temporal_mentions(verse["text"], verse["number"])]
    psalm = {
        "id": f"michael-psalm-{number:03d}", "recordType": "psalm", "archangel": "michael",
        "book": {"number": 17, "title": "L’heure du choix"}, "number": number, "title": TITLES[number],
        "source": {"document": PDF.name, "printedPages": list(range(start_page, psalm_end_page + 1))},
        "verses": verses, "dialogueSegments": sorted(dialogues, key=lambda d: (d.get("positionAfterVerse") or 0, d["id"])),
        "noteIds": note_ids, "prayerIds": prayer_ids, "contextIds": ["michael-book-17-introduction"], "temporalMentions": psalm_temporal,
        "validation": {"status": "machine-extracted-needs-human-review", "checks": {"verseSequenceComplete": sequence_complete, "verseCount": len(verses), "prayerDetectedByAdjacency": bool(prayer_match)}},
    }
    if number != 105:
        write(ROOT / "data/corpus/michael" / f"psalm-{number:03d}.json", psalm)
        for note_record in note_records:
            write(ROOT / "data/notes" / f"{note_record['id']}.json", note_record)
    summary.append({"psalm": number, "pages": [start_page, psalm_end_page], "verses": len(verses), "sequenceComplete": sequence_complete, "questions": len(dialogues), "notes": len(note_records), "prayer": int(prayer_match.group(1)) if prayer_match else None})

write(ROOT / "data/pilot/book-17-extraction-report.json", {"book": 17, "archangel": "michael", "status": "machine-extracted-needs-human-review", "records": summary})

catalog_paths = []
for pattern in ("corpus/**/*.json", "prayers/*.json", "notes/*.json", "themes/*.json"):
    catalog_paths.extend(f"data/{path.relative_to(ROOT / 'data').as_posix()}" for path in (ROOT / "data").glob(pattern))
write(ROOT / "data/catalog.json", {"version": 1, "records": sorted(set(catalog_paths))})
