#!/usr/bin/env python3
"""Validate documentary theme rubrics without making semantic judgments."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "thematic-index" / "theme-rubrics.json"
BOOKS = ROOT / "data" / "thematic-index" / "books"
ALLOWED_STATUSES = {"proposed", "validated", "rejected", "unresolved"}
REQUIRED_VALIDATED_PROVENANCE = {"type", "preparedBy", "approvedBy", "approvedOn"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_occurrences():
    by_record: dict[str, set[str]] = {}
    canonical_theme_ids: set[str] = set()
    for path in sorted(BOOKS.glob("book-*.json")):
        data = load_json(path)
        for psalm in data.get("psalmAnalyses", []):
            record_id = psalm.get("recordId")
            if not record_id:
                continue
            themes = {theme.get("themeId") for theme in psalm.get("themes", []) if theme.get("themeId")}
            by_record[record_id] = themes
            canonical_theme_ids.update(themes)
    return by_record, canonical_theme_ids


def validate(data: dict) -> None:
    assert data.get("schemaVersion") == 1, "theme-rubrics schemaVersion must be 1"
    rubrics = data.get("rubrics")
    assert isinstance(rubrics, list), "theme-rubrics rubrics must be a list"

    occurrences_by_record, canonical_theme_ids = canonical_occurrences()
    rubric_ids: set[str] = set()

    for rubric in rubrics:
        rubric_id = rubric.get("rubricId")
        theme_id = rubric.get("themeId")
        label = rubric.get("label")
        record_ids = rubric.get("recordIds")
        status = rubric.get("validationStatus")

        assert isinstance(rubric_id, str) and rubric_id.strip(), "rubricId is required"
        assert rubric_id not in rubric_ids, f"duplicate rubricId: {rubric_id}"
        rubric_ids.add(rubric_id)
        assert rubric_id not in canonical_theme_ids, f"rubricId must not be a canonical themeId: {rubric_id}"

        assert isinstance(theme_id, str) and theme_id in canonical_theme_ids, f"unknown parent themeId: {theme_id}"
        assert isinstance(label, str) and label.strip(), f"label is required for {rubric_id}"
        assert status in ALLOWED_STATUSES, f"invalid validationStatus for {rubric_id}: {status}"
        assert isinstance(record_ids, list) and record_ids, f"recordIds must be a non-empty list for {rubric_id}"
        assert len(record_ids) == len(set(record_ids)), f"duplicate recordId inside rubric {rubric_id}"

        for record_id in record_ids:
            assert isinstance(record_id, str) and record_id in occurrences_by_record, f"unknown recordId in {rubric_id}: {record_id}"
            assert theme_id in occurrences_by_record[record_id], (
                f"rubric {rubric_id} references {record_id}, but that canonical analysis has no occurrence of theme {theme_id}"
            )

        if status == "validated":
            provenance = rubric.get("decisionProvenance")
            assert isinstance(provenance, dict), f"validated rubric {rubric_id} requires decisionProvenance"
            missing = REQUIRED_VALIDATED_PROVENANCE - provenance.keys()
            assert not missing, f"validated rubric {rubric_id} is missing provenance fields: {sorted(missing)}"
            for field in REQUIRED_VALIDATED_PROVENANCE:
                assert isinstance(provenance[field], str) and provenance[field].strip(), (
                    f"validated rubric {rubric_id} has empty provenance field: {field}"
                )


if __name__ == "__main__":
    validate(load_json(SOURCE))
    print("Theme rubrics contract OK")
