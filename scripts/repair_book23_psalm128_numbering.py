#!/usr/bin/env python3
"""Repair the audited numbering of Raphael Psalm 128.

The PDF extraction correctly captured the text of Psalm 128 but inherited an
editorial +48 numbering offset: source labels 49..82 correspond to Psalm verses
1..34. The question spoken between verses 22 and 23 remains embedded at the end
of the verse-22 text, as in the existing corpus representation; it is not
counted as an additional verse.

This repair is deliberately guarded by the exact Psalm identity, the expected
contiguous source numbering, the known opening text, and the question boundary.
It never invents or rewrites Psalm text.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/corpus/books/book-23/psalm-128.json"

EXPECTED_SOURCE_NUMBERS = list(range(49, 83))
OPENING = "L’homme ne peut pas vivre sans intelligence ni sans âme."
QUESTION_START = "Père Raphaël, comme tu le dis"
ANSWER_START = "Vous devez entrer dans l’étude, la dévotion, le rite et l’œuvre"


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data.get("id") != "book-23-psalm-128" or data.get("title") != "Ne sois pas un rêveur":
        raise RuntimeError("Unexpected Psalm 128 identity")

    verses = data.get("verses", [])
    nums = [v.get("number") for v in verses]

    # Idempotence: accept an already repaired canonical record only after
    # checking its documentary invariants.
    if nums == list(range(1, 35)):
        if not verses[0].get("text", "").startswith(OPENING):
            raise RuntimeError("Psalm 128 repaired opening-text guard failed")
        if QUESTION_START not in verses[21].get("text", ""):
            raise RuntimeError("Psalm 128 repaired question boundary guard failed")
        if not verses[22].get("text", "").startswith(ANSWER_START):
            raise RuntimeError("Psalm 128 repaired answer boundary guard failed")
        print("Book 23 Psalm 128 numbering already repaired: verses 1-34")
        return

    if nums != EXPECTED_SOURCE_NUMBERS:
        raise RuntimeError(f"Unexpected Psalm 128 source numbering: {nums}")
    if not verses[0].get("text", "").startswith(OPENING):
        raise RuntimeError("Psalm 128 opening-text guard failed")
    if QUESTION_START not in verses[21].get("text", ""):
        raise RuntimeError("Psalm 128 question is not at source verse 70 / canonical verse 22")
    if not verses[22].get("text", "").startswith(ANSWER_START):
        raise RuntimeError("Psalm 128 answer is not at source verse 71 / canonical verse 23")

    for verse in verses:
        verse["number"] -= 48

    extraction = data.setdefault("extraction", {})
    extraction["headingBasis"] = "audited-explicit-heading-with-corrected-verse-offset"
    extraction["sourceNumberingPreserved"] = False
    extraction["sourceFirstVerse"] = 49
    extraction["sourceVerseOffsetCorrected"] = 48
    extraction["questionBoundaryAudited"] = {
        "afterVerse": 22,
        "beforeVerse": 23,
        "countedAsVerse": False,
        "representation": "embedded-at-end-of-preceding-verse-text"
    }

    validation = data.setdefault("validation", {})
    validation["status"] = "machine-extracted-source-boundary-audited-numbering-corrected"
    validation["checks"] = {
        "verseCount": 34,
        "verseSequenceStartsAtOne": True,
        "verseSequenceContiguous": True,
        "questionCount": 1,
        "questionNotCountedAsVerse": True
    }

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Repaired book 23 Psalm 128: source labels 49-82 -> canonical verses 1-34; question remains between 22 and 23")


if __name__ == "__main__":
    main()
