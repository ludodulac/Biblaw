#!/usr/bin/env python3
"""Emit one compact attested occurrence for each theme in the next general review batch.

Read-only diagnostic. Selection prefers direct central/important occurrences with
verse evidence and a teaching, then falls back to any attested occurrence. The
report contains no semantic relation decision.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
THEME_IDS = [
    "corps", "ame", "esprit", "corps-ame-esprit",
    "terre", "eau", "air", "feu", "terre-eau-air-feu",
    "lumiere", "apparences-et-fausse-lumiere",
    "dieux", "idoles-et-faux-dieux",
    "pratique", "conscience", "pratique-et-conscience",
    "pensee", "parole", "maitrise-pensee-parole",
]


def rank(theme: dict) -> tuple[int, int, int]:
    has_evidence = bool(theme.get("verseNumbers")) and bool(theme.get("teaching"))
    strong = (
        has_evidence
        and theme.get("directness") == "direct"
        and theme.get("importance") in {"central", "important"}
    )
    importance_rank = {"central": 0, "important": 1, "related": 2}.get(theme.get("importance"), 3)
    return (0 if strong else 1 if has_evidence else 2, importance_rank, 0 if theme.get("directness") == "direct" else 1)


def main() -> None:
    occurrences: dict[str, list[dict]] = {theme_id: [] for theme_id in THEME_IDS}
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for analysis in data.get("psalmAnalyses") or []:
            record_id = analysis.get("recordId")
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if theme_id not in occurrences:
                    continue
                occurrences[theme_id].append({
                    "recordId": record_id,
                    "bookNumber": analysis.get("bookNumber"),
                    "psalmNumber": analysis.get("psalmNumber"),
                    "importance": theme.get("importance"),
                    "directness": theme.get("directness"),
                    "verseNumbers": theme.get("verseNumbers") or [],
                    "teaching": theme.get("teaching") or "",
                })

    selected = {}
    missing = []
    for theme_id in THEME_IDS:
        rows = occurrences[theme_id]
        if not rows:
            missing.append(theme_id)
            continue
        rows.sort(key=lambda row: (rank(row), row.get("bookNumber") or 999, row.get("psalmNumber") or 999))
        selected[theme_id] = rows[0]

    payload = {
        "schemaVersion": 1,
        "recordType": "theme-relation-general-evidence-report",
        "semanticClaim": False,
        "selectionPolicy": "prefer-direct-central-or-important-with-verses-and-teaching",
        "requestedThemeCount": len(THEME_IDS),
        "selectedThemeCount": len(selected),
        "missingThemeIds": missing,
        "themes": selected,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
