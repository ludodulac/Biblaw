#!/usr/bin/env python3
"""Report bounded corpus evidence for a small set of theme ids.

This is a TARGETED, read-only review aid. It scans the existing per-book thematic
analyses and returns a small number of attested occurrences (psalm, verses,
importance, directness, teaching) for each requested theme id.

It does not infer, validate, persist, merge, rename or expose any theme relation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"


def collect(theme_ids: set[str], max_occurrences: int) -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = {theme_id: [] for theme_id in sorted(theme_ids)}

    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        for analysis in data.get("psalmAnalyses") or []:
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if theme_id not in found or len(found[theme_id]) >= max_occurrences:
                    continue
                found[theme_id].append({
                    "recordId": analysis.get("recordId"),
                    "bookNumber": book.get("number"),
                    "psalmNumber": analysis.get("number"),
                    "psalmTitle": analysis.get("title"),
                    "label": theme.get("label"),
                    "importance": theme.get("importance"),
                    "directness": theme.get("directness"),
                    "verseNumbers": theme.get("verseNumbers") or [],
                    "teaching": theme.get("teaching"),
                })

    return found


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report bounded attested context for theme-relation human review."
    )
    parser.add_argument(
        "--theme",
        action="append",
        dest="themes",
        required=True,
        help="Theme id to inspect; repeat for several ids.",
    )
    parser.add_argument(
        "--max-occurrences",
        type=int,
        default=3,
        help="Maximum occurrences returned per theme (default: 3).",
    )
    args = parser.parse_args()
    if args.max_occurrences < 1 or args.max_occurrences > 10:
        parser.error("--max-occurrences must be between 1 and 10")

    theme_ids = set(args.themes)
    evidence = collect(theme_ids, args.max_occurrences)
    missing = sorted(theme_id for theme_id, rows in evidence.items() if not rows)

    payload = {
        "schemaVersion": 1,
        "recordType": "theme-relation-review-context",
        "semanticClaim": False,
        "source": "data/thematic-index/books/book-*.json",
        "requestedThemeIds": sorted(theme_ids),
        "maxOccurrencesPerTheme": args.max_occurrences,
        "missingThemeIds": missing,
        "themes": [
            {"themeId": theme_id, "occurrences": evidence[theme_id]}
            for theme_id in sorted(theme_ids)
        ],
        "interpretation": (
            "Evidence for human semantic review only. Presence, shared wording or "
            "cooccurrence does not validate a relation."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
