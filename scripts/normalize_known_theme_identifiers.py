#!/usr/bin/env python3
"""Normalize a small, reviewed set of technical theme-id variants.

This script does NOT infer semantic equivalence. Every mapping below was reviewed against
corpus-internal Psalm contexts, verse anchors and teachings. It changes identifiers only;
labels, importance, directness, verseNumbers and teaching remain untouched.

Use --check in CI to fail if a reviewed legacy identifier is reintroduced.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data" / "thematic-index" / "books"

# Reviewed technical duplicates only. Do not add entries from lexical similarity alone.
LEGACY_TO_CANONICAL = {
    "corps-deau": "corps-d-eau",
    "corps-dimmortalite": "corps-d-immortalite",
    "microcosme-macrocosme": "microcosme-et-macrocosme",
    "royaut-e-interieure": "royaute-interieure",
    "royauté-interieure": "royaute-interieure",
}

EXPECTED_LABEL = {
    "corps-d-eau": "Corps d’eau",
    "corps-d-immortalite": "Corps d’immortalité",
    "microcosme-et-macrocosme": "Microcosme et macrocosme",
    "royaute-interieure": "Royauté intérieure",
}


def validate_book(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for psalm in data.get("psalmAnalyses", []):
        seen: set[str] = set()
        for rel in psalm.get("themes", []):
            theme_id = rel.get("themeId")
            if theme_id in LEGACY_TO_CANONICAL:
                raise AssertionError(f"legacy themeId remains in {path.name}: {theme_id}")
            if theme_id in EXPECTED_LABEL:
                expected = EXPECTED_LABEL[theme_id]
                if rel.get("label") != expected:
                    raise AssertionError(
                        f"unexpected label for {theme_id} in {path.name} / {psalm.get('recordId')}: "
                        f"{rel.get('label')!r} != {expected!r}"
                    )
            if theme_id:
                if theme_id in seen:
                    raise AssertionError(
                        f"duplicate themeId {theme_id} in one Psalm after normalization: "
                        f"{path.name} / {psalm.get('recordId')}"
                    )
                seen.add(theme_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting legacy ids")
    args = parser.parse_args()

    changed_files: list[str] = []
    replacements = 0

    for path in sorted(BOOKS.glob("book-*.json")):
        text = path.read_text(encoding="utf-8")
        original = text
        found_legacy: list[str] = []
        for legacy, canonical in LEGACY_TO_CANONICAL.items():
            needle = f'"themeId": "{legacy}"'
            count = text.count(needle)
            if not count:
                continue
            found_legacy.extend([legacy] * count)
            if not args.check:
                text = text.replace(needle, f'"themeId": "{canonical}"')
                replacements += count

        if args.check and found_legacy:
            raise AssertionError(
                f"reviewed legacy theme ids in {path.name}: {', '.join(found_legacy)}"
            )

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files.append(path.name)

        if not args.check:
            validate_book(path)

    if args.check:
        for path in sorted(BOOKS.glob("book-*.json")):
            validate_book(path)
        print("Known theme identifier guard OK: no reviewed legacy identifiers remain")
    else:
        print(
            f"Known theme identifier normalization: replacements={replacements}, "
            f"changedFiles={len(changed_files)} {changed_files}"
        )


if __name__ == "__main__":
    main()
