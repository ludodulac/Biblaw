#!/usr/bin/env python3
"""Build the compact thematic directory consumed by the public browser UI.

The canonical editorial directory remains data/thematic-index/theme-directory.json. This derivative
keeps only fields that js/biblaw.js actually needs at runtime, so the browser does not download
editorial/indexing metadata that is already represented elsewhere. No relation, evidence verse,
teaching, importance or score is inferred or rewritten.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/thematic-index/theme-directory.json"
OUT = ROOT / "data/thematic-index/theme-directory-public.json"
THEME_FIELDS = ("id", "label", "score", "occurrenceCount")
OCCURRENCE_FIELDS = ("recordId", "bookNumber", "archangel", "importance", "verseNumbers", "teaching", "score")


def project(item: dict, fields: tuple[str, ...]) -> dict:
    return {key: item[key] for key in fields if key in item}


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    themes = []
    relation_count = 0
    for theme in source.get("themes", []):
        public_theme = project(theme, THEME_FIELDS)
        occurrences = [project(occurrence, OCCURRENCE_FIELDS) for occurrence in theme.get("occurrences", [])]
        public_theme["occurrences"] = occurrences
        relation_count += len(occurrences)
        themes.append(public_theme)

    result = {
        "schemaVersion": 1,
        "generatedFrom": "data/thematic-index/theme-directory.json",
        "manualEditingAllowed": False,
        "themeCount": len(themes),
        "relationCount": relation_count,
        "themes": themes,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Built public thematic directory with {len(themes)} themes and {relation_count} relations ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
