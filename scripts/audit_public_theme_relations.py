#!/usr/bin/env python3
"""Audit the public presentation view of validated theme relations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
CANONICAL = INDEX / "theme-relations-validated.json"
PUBLIC = INDEX / "theme-relations-public.json"
DIRECTORY = INDEX / "theme-directory-public.json"
ALLOWED_RELATION_FIELDS = {"sourceThemeId", "targetThemeId", "relationType"}


def triple(relation: dict) -> tuple[str, str, str]:
    return relation["sourceThemeId"], relation["targetThemeId"], relation["relationType"]


def main() -> None:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    directory = json.loads(DIRECTORY.read_text(encoding="utf-8"))

    assert canonical.get("publicSearchEffect") is False
    assert public.get("presentationOnly") is True
    assert public.get("publicSearchEffect") is False
    assert public.get("manualEditingAllowed") is False
    assert public.get("generatedFrom") == "data/thematic-index/theme-relations-validated.json"

    canonical_relations = canonical.get("relations", [])
    public_relations = public.get("relations", [])
    assert public.get("relationCount") == len(public_relations) == len(canonical_relations)
    assert [triple(item) for item in public_relations] == [triple(item) for item in canonical_relations]

    theme_ids = {theme["id"] for theme in directory.get("themes", [])}
    for relation in public_relations:
        assert set(relation) == ALLOWED_RELATION_FIELDS, f"unexpected public relation fields: {set(relation) - ALLOWED_RELATION_FIELDS}"
        assert relation["sourceThemeId"] in theme_ids
        assert relation["targetThemeId"] in theme_ids

    serialized = json.dumps(public, ensure_ascii=False).lower()
    for forbidden in ("evidencebythemeid", "versenumbers", "teaching", "validation", "human-approved", "note"):
        assert forbidden not in serialized, f"private editorial field leaked into public relation view: {forbidden}"

    print(f"Public relation presentation boundary OK: {len(public_relations)} relations; no evidence or validation notes exposed")


if __name__ == "__main__":
    main()
