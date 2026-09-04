#!/usr/bin/env python3
"""Build the software-facing thematic directory from editorial book analyses.

The source of truth remains data/thematic-index/books/book-*.json. This script derives a
cross-book index that can be regenerated at any time and must never be hand-edited.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
OUT = ROOT / "data/thematic-index/theme-directory.json"
WEIGHT = {"central": 3, "important": 2, "related": 1}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(data):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


themes = {}
for path in sorted(BOOKS.glob("book-*.json")):
    book_data = load(path)
    book = book_data.get("book", {})
    archangel = book.get("archangel")
    for psalm in book_data.get("psalmAnalyses", []):
        for rel in psalm.get("themes", []):
            theme_id = rel.get("themeId")
            label = rel.get("label")
            if not theme_id or not label:
                continue
            entry = themes.setdefault(theme_id, {
                "id": theme_id,
                "label": label,
                "occurrences": [],
                "archangels": defaultdict(lambda: {"score": 0, "occurrenceCount": 0}),
            })
            importance = rel.get("importance", "related")
            score = WEIGHT.get(importance, 1)
            occurrence = {
                "recordId": psalm.get("recordId"),
                "bookNumber": book.get("number"),
                "bookTitle": book.get("title"),
                "archangel": archangel,
                "psalmNumber": psalm.get("number"),
                "psalmTitle": psalm.get("title"),
                "importance": importance,
                "directness": rel.get("directness"),
                "verseNumbers": rel.get("verseNumbers", []),
                "teaching": rel.get("teaching"),
                "score": score,
            }
            entry["occurrences"].append(occurrence)
            if archangel:
                entry["archangels"][archangel]["score"] += score
                entry["archangels"][archangel]["occurrenceCount"] += 1

result = []
for theme_id, entry in themes.items():
    occurrences = sorted(
        entry["occurrences"],
        key=lambda x: (-x["score"], x.get("bookNumber") or 9999, x.get("psalmNumber") or 9999),
    )
    archangels = [
        {"id": aid, **stats}
        for aid, stats in sorted(entry["archangels"].items(), key=lambda kv: (-kv[1]["score"], kv[0]))
    ]
    result.append({
        "id": theme_id,
        "label": entry["label"],
        "score": sum(x["score"] for x in occurrences),
        "occurrenceCount": len(occurrences),
        "centralPsalmCount": sum(1 for x in occurrences if x["importance"] == "central"),
        "archangels": archangels,
        "topPsalms": occurrences[:12],
        "occurrences": occurrences,
    })

result.sort(key=lambda x: (x["label"].casefold(), x["id"]))
write({
    "schemaVersion": 1,
    "generatedFrom": "data/thematic-index/books/book-*.json",
    "manualEditingAllowed": False,
    "themeCount": len(result),
    "themes": result,
})
print(f"Built thematic directory with {len(result)} themes")
