#!/usr/bin/env python3
"""Keep thematic book metadata synchronized with the corpus and apply explicit repairs.

Titles and note links are documentary metadata and are copied from the structured Psalm corpus.
Evidence and thematic repairs below are explicit editorial decisions grounded in cited verses,
never inferred automatically from keyword frequency or lexical similarity. Legacy enum aliases
are normalized mechanically so book files cannot fail validation because a semantically equivalent
historical value was used.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
CORPUS = ROOT / "data/corpus/books"

EVIDENCE_REPAIRS = {
    ("book-03-psalm-020", "enthousiasme"): [2, 4, 6],
    ("book-03-psalm-020", "flamme"): [2, 4, 6],
}

# Explicit, corpus-grounded thematic additions. These relations are intentionally narrow:
# they are anchored only where the expression is itself part of the teaching, rather than
# being created for every literal occurrence of the words.
THEME_RELATION_REPAIRS = {
    "book-29-psalm-197": {
        "themeId": "sainte-assemblee",
        "label": "Sainte Assemblée",
        "importance": "important",
        "directness": "direct",
        "verseNumbers": [16, 28],
        "teaching": "Dans ce psaume, la sainte assemblée est explicitement présentée comme le cadre religieux uni autour de la flamme vivante de l’Alliance, associé aux rites, à la méditation, à l’étude et à la protection contre le feu de la destruction (v.16, 28).",
    },
    "book-29-psalm-211": {
        "themeId": "sainte-assemblee",
        "label": "Sainte Assemblée",
        "importance": "important",
        "directness": "direct",
        "verseNumbers": [24, 32],
        "teaching": "Le psaume relie directement l’assemblée à l’espace sacré de l’église et à l’œuvre de créer sur terre la sainte assemblée dans le cadre de la religion de la Lumière (v.24, 32).",
    },
    "book-29-psalm-212": {
        "themeId": "sainte-assemblee",
        "label": "Sainte Assemblée",
        "importance": "central",
        "directness": "direct",
        "verseNumbers": [4, 9, 16, 20, 25, 26, 27, 28, 31],
        "teaching": "Ce psaume a pour sujet explicite les fondements de la sainte assemblée. Il la décrit comme un cercle devant être constitué avec clarté, pureté et discernement et, aux v.27-28, comme l’église, la maison et le corps de Dieu sur la terre ouvrant un espace à sa présence.",
    },
}

IMPORTANCE_ALIASES = {
    "supporting": "related",
    "secondary": "related",
}

changed_files = 0
for path in sorted(BOOKS.glob("book-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    book_no = data.get("book", {}).get("number")
    changed = False
    if not isinstance(book_no, int):
        continue
    for psalm in data.get("psalmAnalyses", []):
        number = psalm.get("number")
        if isinstance(number, int):
            source_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{number:03d}.json"
            if source_path.exists():
                source = json.loads(source_path.read_text(encoding="utf-8"))
                source_title = source.get("title")
                if source_title and psalm.get("title") != source_title:
                    psalm["title"] = source_title
                    changed = True
                source_notes = list(source.get("noteIds", []))
                # Every editorial note attached to a Psalm is contextual evidence.
                if source_notes:
                    if psalm.get("notesUsed") != source_notes:
                        psalm["notesUsed"] = source_notes
                        changed = True
                elif "notesUsed" in psalm and psalm.get("notesUsed"):
                    psalm.pop("notesUsed", None)
                    changed = True
        record_id = psalm.get("recordId")
        themes = psalm.setdefault("themes", [])
        for rel in themes:
            importance = rel.get("importance")
            if importance in IMPORTANCE_ALIASES:
                rel["importance"] = IMPORTANCE_ALIASES[importance]
                changed = True
            key = (record_id, rel.get("themeId"))
            if key in EVIDENCE_REPAIRS and rel.get("verseNumbers") != EVIDENCE_REPAIRS[key]:
                rel["verseNumbers"] = EVIDENCE_REPAIRS[key]
                changed = True

        repair = THEME_RELATION_REPAIRS.get(record_id)
        if repair:
            existing = next((rel for rel in themes if rel.get("themeId") == repair["themeId"]), None)
            if existing is None:
                themes.append(dict(repair))
                changed = True
            elif any(existing.get(key) != value for key, value in repair.items()):
                existing.update(repair)
                changed = True

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Normalized thematic metadata in {changed_files} book files")
