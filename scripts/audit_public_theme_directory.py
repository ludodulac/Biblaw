#!/usr/bin/env python3
"""Verify that the compact public theme directory is an exact lossless runtime projection."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/thematic-index/theme-directory.json"
PUBLIC = ROOT / "data/thematic-index/theme-directory-public.json"
THEME_FIELDS = ("id", "label", "score", "occurrenceCount")
OCCURRENCE_FIELDS = ("recordId", "archangel", "importance", "verseNumbers", "teaching", "score")


def project(item: dict, fields: tuple[str, ...]) -> dict:
    return {key: item[key] for key in fields if key in item}


def fail(message: str) -> None:
    raise SystemExit(f"Public theme directory audit failed: {message}")


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    source_themes = source.get("themes", [])
    public_themes = public.get("themes", [])
    if public.get("themeCount") != len(source_themes) or len(public_themes) != len(source_themes):
        fail("theme count differs from canonical directory")

    expected_relations = sum(len(theme.get("occurrences", [])) for theme in source_themes)
    if public.get("relationCount") != expected_relations:
        fail("relation count differs from canonical directory")

    for source_theme, public_theme in zip(source_themes, public_themes, strict=True):
        expected_theme = project(source_theme, THEME_FIELDS)
        expected_occurrences = [project(item, OCCURRENCE_FIELDS) for item in source_theme.get("occurrences", [])]
        if project(public_theme, THEME_FIELDS) != expected_theme:
            fail(f"theme projection differs for {source_theme.get('id')}")
        if public_theme.get("occurrences", []) != expected_occurrences:
            fail(f"occurrence projection differs for {source_theme.get('id')}")
        allowed = set(THEME_FIELDS) | {"occurrences"}
        extra = set(public_theme) - allowed
        if extra:
            fail(f"unexpected public theme fields for {source_theme.get('id')}: {sorted(extra)}")
        for occurrence in public_theme.get("occurrences", []):
            extra = set(occurrence) - set(OCCURRENCE_FIELDS)
            if extra:
                fail(f"unexpected public occurrence fields for {source_theme.get('id')}: {sorted(extra)}")

    source_size = SOURCE.stat().st_size
    public_size = PUBLIC.stat().st_size
    if public_size >= source_size:
        fail(f"compact projection is not smaller ({public_size} >= {source_size})")
    print(f"Public theme directory OK: {len(public_themes)} themes, {expected_relations} relations, {public_size}/{source_size} bytes ({public_size/source_size:.1%})")


if __name__ == "__main__":
    main()
