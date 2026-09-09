#!/usr/bin/env python3
"""Report exact normalized aliases shared by multiple search-layer theme IDs.

This is a FAST, read-only diagnostic. A shared normalized alias is only a review
signal: it does not establish semantic equivalence and must not resolve an
ambiguity automatically.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH_INDEX = ROOT / "data/thematic-index/theme-search-index.json"


def main() -> None:
    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))
    themes = data.get("themes") or []
    by_alias: dict[str, list[dict[str, object]]] = defaultdict(list)

    for theme in themes:
        theme_id = theme.get("themeId")
        label = theme.get("canonicalLabel")
        occurrence_count = theme.get("occurrenceCount")
        for alias in set(theme.get("normalizedAliases") or []):
            if alias:
                by_alias[alias].append(
                    {
                        "themeId": theme_id,
                        "canonicalLabel": label,
                        "occurrenceCount": occurrence_count,
                    }
                )

    collisions = []
    for alias, members in sorted(by_alias.items()):
        distinct_ids = {item["themeId"] for item in members}
        if len(distinct_ids) < 2:
            continue
        collisions.append(
            {
                "normalizedAlias": alias,
                "themeCount": len(distinct_ids),
                "themes": sorted(members, key=lambda item: str(item["themeId"])),
                "semanticClaim": False,
                "requiresHumanValidation": True,
            }
        )

    declared_count = data.get("ambiguousAliasCount")
    if declared_count is not None and declared_count != len(collisions):
        raise SystemExit(
            "Alias ambiguity drift: "
            f"theme-search-index declares {declared_count}, derived collisions={len(collisions)}"
        )

    print(
        json.dumps(
            {
                "schemaVersion": 1,
                "recordType": "theme-alias-collision-report",
                "semanticClaim": False,
                "declaredAmbiguousAliasCount": declared_count,
                "collisionCount": len(collisions),
                "collisions": collisions,
                "interpretation": (
                    "An exact normalized alias shared by distinct theme IDs is a review signal only. "
                    "It may indicate equivalence, historical fragmentation, contextual variation, or a real ambiguity."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()