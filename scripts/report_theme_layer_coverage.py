#!/usr/bin/env python3
"""Report overlap between editorial theme files and the generated search theme index.

FAST and read-only. This prevents relation work from silently treating editorial
consolidation records as if every one were a searchable theme id.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH_INDEX = ROOT / "data/thematic-index/theme-search-index.json"
EDITORIAL_DIR = ROOT / "data/thematic-index/themes"


def main() -> None:
    search_data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))
    search_ids = {
        item["themeId"]
        for item in search_data.get("themes", [])
        if item.get("themeId")
    }

    editorial_ids: set[str] = set()
    malformed: list[str] = []
    for path in sorted(EDITORIAL_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        theme_id = data.get("id")
        if not theme_id:
            malformed.append(path.name)
            continue
        editorial_ids.add(theme_id)

    overlap = sorted(editorial_ids & search_ids)
    editorial_only = sorted(editorial_ids - search_ids)

    payload = {
        "schemaVersion": 1,
        "recordType": "theme-layer-coverage-report",
        "semanticClaim": False,
        "searchThemeCount": len(search_ids),
        "editorialThemeFileCount": len(editorial_ids),
        "overlapCount": len(overlap),
        "editorialOnlyCount": len(editorial_only),
        "editorialOnlyThemeIds": editorial_only,
        "malformedEditorialFiles": malformed,
        "interpretation": (
            "Editorial theme files are consolidation/research records and must not be "
            "assumed to be one-to-one with generated search theme ids."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
