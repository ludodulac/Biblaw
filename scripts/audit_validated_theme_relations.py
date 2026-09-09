#!/usr/bin/env python3
"""FAST audit for the canonical validated theme-relation store.

The canonical store is allowed to be empty. To avoid a vacuous green audit, this
script also runs small in-memory negative self-tests against the same validator.
It never writes data and never changes public search artifacts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data/thematic-index/theme-relations-validated.json"
SEARCH_INDEX = ROOT / "data/thematic-index/theme-search-index.json"
BOOKS_DIR = ROOT / "data/thematic-index/books"

ALLOWED_RELATION_TYPES = {
    "equivalent_to",
    "variant_of",
    "broader_than",
    "component_of",
    "related_to",
}
SYMMETRIC_RELATION_TYPES = {"equivalent_to", "related_to"}
DIRECTIONAL_RELATION_TYPES = {"variant_of", "broader_than", "component_of"}


class AuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def load_search_theme_ids() -> set[str]:
    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))
    return {
        item["themeId"]
        for item in data.get("themes", [])
        if isinstance(item, dict) and item.get("themeId")
    }


def load_occurrences() -> dict[tuple[str, str], dict[str, Any]]:
    occurrences: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(BOOKS_DIR.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for psalm in data.get("psalmAnalyses", []):
            record_id = psalm.get("recordId")
            if not record_id:
                continue
            for theme in psalm.get("themes", []):
                theme_id = theme.get("themeId")
                if not theme_id:
                    continue
                key = (theme_id, record_id)
                require(key not in occurrences, f"duplicate theme occurrence in analyses: {key}")
                occurrences[key] = {
                    "verseNumbers": set(theme.get("verseNumbers") or []),
                    "teaching": theme.get("teaching"),
                }
    return occurrences


def validate_relations(
    relations: list[dict[str, Any]],
    search_theme_ids: set[str],
    occurrences: dict[tuple[str, str], dict[str, Any]],
) -> None:
    ids: set[str] = set()
    stored_keys: set[tuple[str, str, str]] = set()
    directional_pairs: set[tuple[str, str, str]] = set()

    for relation in relations:
        relation_id = relation.get("id")
        require(bool(relation_id), "validated relation missing id")
        require(relation_id not in ids, f"duplicate validated relation id: {relation_id}")
        ids.add(relation_id)

        require(relation.get("schemaVersion") == 1, f"{relation_id}: schemaVersion must be 1")
        source = relation.get("sourceThemeId")
        target = relation.get("targetThemeId")
        require(bool(source) and bool(target), f"{relation_id}: missing relation endpoint")
        require(source != target, f"{relation_id}: self relation is not allowed")
        require(source in search_theme_ids, f"{relation_id}: source theme is outside search layer: {source}")
        require(target in search_theme_ids, f"{relation_id}: target theme is outside search layer: {target}")

        relation_type = relation.get("relationType")
        require(
            relation_type in ALLOWED_RELATION_TYPES,
            f"{relation_id}: invalid relation type: {relation_type}",
        )
        require(
            relation.get("relationStatus") == "relation_validated",
            f"{relation_id}: canonical store accepts relation_validated only",
        )
        require(relation.get("semanticClaim") is True, f"{relation_id}: semanticClaim must be true")

        validation = relation.get("validation") or {}
        require(
            validation.get("status") == "human-approved",
            f"{relation_id}: validation.status must be human-approved",
        )
        note = validation.get("note")
        require(isinstance(note, str) and note.strip(), f"{relation_id}: validation note is required")

        evidence = relation.get("evidenceByThemeId")
        require(isinstance(evidence, dict), f"{relation_id}: evidenceByThemeId must be an object")
        require(
            set(evidence) == {source, target},
            f"{relation_id}: evidenceByThemeId must contain exactly both endpoints",
        )

        for theme_id in (source, target):
            refs = evidence.get(theme_id)
            require(isinstance(refs, list) and refs, f"{relation_id}: missing evidence for {theme_id}")
            seen_records: set[str] = set()
            for ref in refs:
                record_id = ref.get("recordId") if isinstance(ref, dict) else None
                require(bool(record_id), f"{relation_id}: evidence for {theme_id} missing recordId")
                require(
                    record_id not in seen_records,
                    f"{relation_id}: duplicate evidence record {record_id} for {theme_id}",
                )
                seen_records.add(record_id)

                canonical = occurrences.get((theme_id, record_id))
                require(
                    canonical is not None,
                    f"{relation_id}: {theme_id} is not attested in {record_id}",
                )
                verse_numbers = ref.get("verseNumbers")
                require(
                    isinstance(verse_numbers, list) and verse_numbers,
                    f"{relation_id}: evidence for {theme_id}/{record_id} needs verseNumbers",
                )
                require(
                    all(isinstance(number, int) for number in verse_numbers),
                    f"{relation_id}: verseNumbers must be integers for {theme_id}/{record_id}",
                )
                require(
                    set(verse_numbers).issubset(canonical["verseNumbers"]),
                    f"{relation_id}: unattested verse number for {theme_id}/{record_id}",
                )
                require(
                    ref.get("teaching") == canonical["teaching"],
                    f"{relation_id}: teaching drift for {theme_id}/{record_id}",
                )

        if relation_type in SYMMETRIC_RELATION_TYPES:
            left, right = sorted((source, target))
            key = (relation_type, left, right)
            require(key not in stored_keys, f"{relation_id}: duplicated symmetric relation {left}/{right}")
            stored_keys.add(key)
        else:
            key = (relation_type, source, target)
            reverse = (relation_type, target, source)
            require(key not in stored_keys, f"{relation_id}: duplicate directional relation {source}/{target}")
            require(
                reverse not in directional_pairs,
                f"{relation_id}: contradictory reverse {relation_type} relation {target}/{source}",
            )
            stored_keys.add(key)
            directional_pairs.add(key)


def expect_failure(
    label: str,
    relations: list[dict[str, Any]],
    search_theme_ids: set[str],
    occurrences: dict[tuple[str, str], dict[str, Any]],
) -> None:
    try:
        validate_relations(relations, search_theme_ids, occurrences)
    except AuditError:
        return
    raise AuditError(f"validator self-test did not reject: {label}")


def run_self_tests() -> int:
    themes = {"a", "b"}
    occurrences = {
        ("a", "psalm-a"): {"verseNumbers": {1, 2}, "teaching": "Teaching A"},
        ("b", "psalm-b"): {"verseNumbers": {3, 4}, "teaching": "Teaching B"},
    }
    valid = {
        "schemaVersion": 1,
        "id": "a--b--related",
        "sourceThemeId": "a",
        "targetThemeId": "b",
        "relationType": "related_to",
        "relationStatus": "relation_validated",
        "semanticClaim": True,
        "evidenceByThemeId": {
            "a": [{"recordId": "psalm-a", "verseNumbers": [1], "teaching": "Teaching A"}],
            "b": [{"recordId": "psalm-b", "verseNumbers": [3], "teaching": "Teaching B"}],
        },
        "validation": {"status": "human-approved", "note": "Reviewed test relation."},
    }
    validate_relations([valid], themes, occurrences)

    candidate = json.loads(json.dumps(valid))
    candidate["id"] = "candidate"
    candidate["relationStatus"] = "relation_candidate"
    candidate["semanticClaim"] = False
    expect_failure("candidate in validated store", [candidate], themes, occurrences)

    missing_theme = json.loads(json.dumps(valid))
    missing_theme["id"] = "missing-theme"
    missing_theme["targetThemeId"] = "c"
    missing_theme["evidenceByThemeId"] = {
        "a": missing_theme["evidenceByThemeId"]["a"],
        "c": missing_theme["evidenceByThemeId"]["b"],
    }
    expect_failure("endpoint outside search layer", [missing_theme], themes, occurrences)

    bad_verse = json.loads(json.dumps(valid))
    bad_verse["id"] = "bad-verse"
    bad_verse["evidenceByThemeId"]["a"][0]["verseNumbers"] = [999]
    expect_failure("unattested verse", [bad_verse], themes, occurrences)

    reversed_duplicate = json.loads(json.dumps(valid))
    reversed_duplicate["id"] = "b--a--related"
    reversed_duplicate["sourceThemeId"] = "b"
    reversed_duplicate["targetThemeId"] = "a"
    expect_failure("reversed symmetric duplicate", [valid, reversed_duplicate], themes, occurrences)

    return 5


def main() -> None:
    store = json.loads(STORE.read_text(encoding="utf-8"))
    require(store.get("schemaVersion") == 1, "validated store schemaVersion must be 1")
    require(store.get("recordType") == "validated-theme-relations", "unexpected validated store type")
    require(store.get("status") == "canonical-editorial-source", "validated store must be editorial source")
    require(store.get("generated") is False, "validated store must never be generated")
    require(store.get("endpointLayer") == "theme-search-index", "validated endpoints must use search theme layer")
    require(store.get("publicSearchEffect") is False, "validated relation layer must not affect public search yet")

    relations = store.get("relations")
    require(isinstance(relations, list), "validated store relations must be a list")

    search_theme_ids = load_search_theme_ids()
    occurrences = load_occurrences()
    validate_relations(relations, search_theme_ids, occurrences)
    self_test_count = run_self_tests()

    print(
        "Validated theme relation store OK: "
        f"{len(relations)} canonical relation(s); {len(search_theme_ids)} search-layer themes; "
        f"{self_test_count} validator self-tests passed; public search effect remains false"
    )


if __name__ == "__main__":
    main()
