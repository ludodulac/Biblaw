#!/usr/bin/env python3
"""Apply the validated dialogue rule to machine-extracted Michaël book 17 records.

Numbered Olivier questions are recognized conservatively as direct addresses that
begin with "Père", "Ô Père" or "Ô mon Père" and contain an interrogative. This
avoids treating an Archangel verse that merely mentions the Père and ends with a
rhetorical question as a change of speaker.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CORPUS = DATA / "corpus" / "michael"
REPORT = DATA / "pilot" / "book-17-extraction-report.json"
DIRECT_ADDRESS = re.compile(r"(?i)^(?:ô\s+)?(?:mon\s+)?père(?:\s+michaël)?(?:\b|\s*[,!:])")


def is_olivier_question(text: str) -> bool:
    text = text.strip()
    return "?" in text and bool(DIRECT_ADDRESS.search(text))


def main() -> None:
    normalized_counts: dict[int, int] = {}

    for number in range(106, 131):
        path = CORPUS / f"psalm-{number:03d}.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        verses = record.get("verses", [])
        existing_interludes = [
            d for d in record.get("dialogueSegments", [])
            if d.get("numbering") == "unnumbered-interlude"
        ]

        in_answer = False
        numbered = []
        for verse in verses:
            text = verse.get("text", "")
            if is_olivier_question(text):
                verse["speakerId"] = "olivier-manitara"
                verse["speechRole"] = "question"
                in_answer = True
                numbered.append({
                    "speakerId": "olivier-manitara",
                    "speechRole": "question",
                    "text": text,
                    "numbering": "numbered-verse",
                    "verseNumber": verse["number"],
                    "positionAfterVerse": verse["number"] - 1,
                    "recognitionBasis": [
                        "direct-address-to-father-at-verse-start",
                        "interrogative-form",
                        "editorial-rule-questions-addressed-to-archangel",
                    ],
                    "sourcePages": verse.get("sourcePages", []),
                })
            else:
                verse["speakerId"] = "archangel-michael"
                verse["speechRole"] = "answer" if in_answer else "teaching"

        dialogues = existing_interludes + numbered
        dialogues.sort(key=lambda d: (
            d.get("positionAfterVerse") if d.get("positionAfterVerse") is not None else -1,
            0 if d.get("numbering") == "unnumbered-interlude" else 1,
        ))
        for index, dialogue in enumerate(dialogues, 1):
            dialogue["id"] = f"michael-psalm-{number:03d}-dialogue-{index:03d}"
        record["dialogueSegments"] = dialogues
        normalized_counts[number] = len(dialogues)

        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for item in report.get("records", []):
        number = item.get("psalm")
        if number in normalized_counts:
            item["questions"] = normalized_counts[number]
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(REPORT.relative_to(ROOT))


if __name__ == "__main__":
    main()
