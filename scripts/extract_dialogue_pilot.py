#!/usr/bin/env python3
"""Extract the rich dialogue pilot: Michael psalm 105 and its adjacent prayer."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"


def pages(first: int, last: int) -> str:
    return subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def unwrap(value: str) -> str:
    value = re.sub(r"-\n\s*", "", value)
    value = re.sub(r"\n\s*", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def remove_page_furniture(value: str) -> str:
    kept = []
    for line in value.splitlines():
        stripped = line.strip()
        if re.match(r"^Livre 17 \|", stripped, re.I):
            continue
        if stripped in {"1071", "1072", "1073"}:
            continue
        kept.append(line)
    return "\n".join(kept)


def main() -> None:
    raw = remove_page_furniture(pages(1071, 1073))
    footnote_match = re.search(
        r"(?m)^1 - Dans les premières éditions.*?(?=\n\s*10\.)",
        raw,
        re.S,
    )
    if not footnote_match:
        raise RuntimeError("Editorial note 1 was not found")
    footnote = unwrap(footnote_match.group(0).removeprefix("1 - "))
    raw_without_note = raw[: footnote_match.start()] + raw[footnote_match.end() :]

    title = re.search(r"105\s+Aux infidèles", raw_without_note, re.I)
    prayer_marker = re.search(r"(?m)^\s*Pr\.\s*1\.\s*", raw_without_note)
    if not title or not prayer_marker:
        raise RuntimeError("Psalm or prayer boundary was not found")

    psalm_body = raw_without_note[title.end() : prayer_marker.start()]
    verse_matches = list(re.finditer(r"(?m)^\s*(\d{1,2})\.\s+", psalm_body))
    verses = []
    for index, match in enumerate(verse_matches):
        number = int(match.group(1))
        end = verse_matches[index + 1].start() if index + 1 < len(verse_matches) else len(psalm_body)
        speaker = "olivier-manitara" if number == 9 else "archangel-michael"
        role = "question" if number == 9 else ("answer" if number >= 10 else "teaching")
        verses.append(
            {
                "number": number,
                "speakerId": speaker,
                "speechRole": role,
                "text": unwrap(psalm_body[match.end() : end]),
                "sourcePages": [1071] if number <= 9 else [1072],
            }
        )
    if [item["number"] for item in verses] != list(range(1, 20)):
        raise RuntimeError("Expected verses 1 through 19")

    prayer_text = unwrap(raw_without_note[prayer_marker.end() :])
    psalm = {
        "id": "michael-psalm-105",
        "recordType": "psalm",
        "archangel": "michael",
        "book": {"number": 17, "title": "L’heure du choix"},
        "number": 105,
        "title": "Aux infidèles",
        "source": {
            "document": "Bible essénienne (classée par livres).pdf",
            "printedPages": [1071, 1072],
        },
        "verses": verses,
        "noteIds": ["michael-psalm-105-note-001"],
        "prayerIds": ["michael-book-17-prayer-001"],
        "contextIds": ["michael-book-17-introduction"],
        "temporalMentions": [],
        "validation": {
            "status": "machine-extracted-needs-human-review",
            "checks": {
                "verseSequenceComplete": True,
                "verseCount": 19,
                "speakerBoundarySupportedByEditorialNote": True,
            },
        },
    }
    prayer = {
        "id": "michael-book-17-prayer-001",
        "recordType": "master-prayer",
        "archangel": "michael",
        "bookNumber": 17,
        "number": 1,
        "speakerId": "olivier-manitara",
        "text": prayer_text,
        "source": {
            "document": "Bible essénienne (classée par livres).pdf",
            "printedPages": [1072, 1073],
        },
        "appliesToPsalmId": "michael-psalm-105",
        "attachment": {
            "basis": "editorial-adjacency",
            "description": "The prayer is printed immediately after psalm 105 and before psalm 106.",
        },
        "validation": {"status": "machine-extracted-needs-human-review"},
    }
    note = {
        "id": "michael-psalm-105-note-001",
        "recordType": "note",
        "archangel": "michael",
        "appliesTo": {"recordId": "michael-psalm-105", "verse": 9, "marker": 1},
        "text": footnote,
        "source": {
            "document": "Bible essénienne (classée par livres).pdf",
            "printedPage": 1071,
        },
        "editorialMeaning": "Confirms that verse 9 is a question by Olivier Manitara and that such questions were preserved as verses.",
        "temporalMentions": [{"value": "2009-2010", "kind": "edition-period"}],
        "validation": {"status": "machine-extracted-needs-human-review"},
    }

    outputs = {
        ROOT / "data/corpus/michael/psalm-105.json": psalm,
        ROOT / "data/prayers/michael-book-17-prayer-001.json": prayer,
        ROOT / "data/notes/michael-psalm-105-note-001.json": note,
    }
    for path, value in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
