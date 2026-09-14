#!/usr/bin/env python3
"""Normalize a small, reviewed set of technical theme-id variants.

This script does NOT infer semantic equivalence. Every mapping below was reviewed against
corpus-internal Psalm contexts, verse anchors and teachings. It changes identifiers only;
labels, importance, directness, verseNumbers and teaching remain untouched.

If normalization makes two relations share one id inside the same Psalm, one is removed only
when the complete relations are otherwise identical. Any non-identical collision fails loudly.
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
    "ange": "anges",
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


def validate_data(data: dict, path: Path) -> None:
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
                        f"duplicate themeId {theme_id} in one Psalm: "
                        f"{path.name} / {psalm.get('recordId')}"
                    )
                seen.add(theme_id)


def normalize_data(data: dict, path: Path) -> tuple[int, int]:
    replacements = 0
    duplicates_removed = 0

    for psalm in data.get("psalmAnalyses", []):
        normalized: list[dict] = []
        by_id: dict[str, dict] = {}
        for original_rel in psalm.get("themes", []):
            rel = dict(original_rel)
            old_id = rel.get("themeId")
            new_id = LEGACY_TO_CANONICAL.get(old_id, old_id)
            if new_id != old_id:
                rel["themeId"] = new_id
                replacements += 1

            if new_id and new_id in by_id:
                existing = by_id[new_id]
                if existing == rel:
                    duplicates_removed += 1
                    continue
                raise AssertionError(
                    "non-identical relations would collide during reviewed id normalization: "
                    f"{path.name} / {psalm.get('recordId')} / {new_id}"
                )

            normalized.append(rel)
            if new_id:
                by_id[new_id] = rel

        psalm["themes"] = normalized

    validate_data(data, path)
    return replacements, duplicates_removed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting legacy ids")
    args = parser.parse_args()

    changed_files: list[str] = []
    replacements = 0
    duplicates_removed = 0

    for path in sorted(BOOKS.glob("book-*.json")):
        original = path.read_text(encoding="utf-8")
        data = json.loads(original)

        if args.check:
            validate_data(data, path)
            continue

        file_replacements, file_duplicates = normalize_data(data, path)
        replacements += file_replacements
        duplicates_removed += file_duplicates
        if file_replacements or file_duplicates:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed_files.append(path.name)

    if args.check:
        print("Known theme identifier guard OK: no reviewed legacy identifiers remain")
    else:
        print(
            f"Known theme identifier normalization: replacements={replacements}, "
            f"identicalDuplicatesRemoved={duplicates_removed}, "
            f"changedFiles={len(changed_files)} {changed_files}"
        )


if __name__ == "__main__":
    main()
