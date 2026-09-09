#!/usr/bin/env python3
"""Audit the noncanonical semantic relation review pilot.

The pilot must stay review-only: no validated relation, no semantic claim and no
public search effect. It must also prove that structural candidates can be both
retyped and rejected rather than automatically accepted as components.

Every evidence reference is checked against the existing per-book thematic analyses.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/thematic-index/reviews/theme-relations-pilot.json"
BOOKS = ROOT / "data/thematic-index/books"
ALLOWED_RELATION_TYPES = {
    "equivalent_to",
    "variant_of",
    "broader_than",
    "component_of",
    "related_to",
}
ALLOWED_DISPOSITIONS = {"retyped", "rejected"}


def build_attested_occurrences() -> dict[tuple[str, str], set[int]]:
    attested: dict[tuple[str, str], set[int]] = {}
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for analysis in data.get("psalmAnalyses") or []:
            record_id = analysis.get("recordId")
            if not record_id:
                continue
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if theme_id:
                    attested[(theme_id, record_id)] = set(theme.get("verseNumbers") or [])
    return attested


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    assert data.get("recordType") == "theme-relation-review-pilot"
    assert data.get("status") == "proposed-review-decisions"
    assert data.get("semanticClaim") is False
    assert data.get("requiresHumanApproval") is True
    assert data.get("publicSearchEffect") is False
    assert data.get("evidencePolicy"), "pilot must explain evidence orientation"

    decisions = data.get("decisions") or []
    assert decisions, "review pilot must contain decisions"
    attested = build_attested_occurrences()

    dispositions: set[str] = set()
    proposed_types: set[str] = set()
    ids: set[str] = set()
    evidence_reference_count = 0

    for item in decisions:
        item_id = item.get("id")
        assert item_id and item_id not in ids, f"duplicate or missing decision id: {item_id!r}"
        ids.add(item_id)

        candidate = item.get("candidate") or {}
        proposed = item.get("proposedRelation") or {}
        evidence_by_theme = item.get("evidenceByThemeId") or {}
        disposition = item.get("candidateDisposition")

        candidate_ids = {candidate.get("sourceThemeId"), candidate.get("targetThemeId")}
        proposed_ids = {proposed.get("sourceThemeId"), proposed.get("targetThemeId")}
        assert None not in candidate_ids
        assert None not in proposed_ids
        assert candidate_ids == proposed_ids, f"proposed relation changes theme pair in {item_id}"

        assert candidate.get("candidateRelationType") == "component_candidate"
        assert candidate.get("candidateBasis") == "normalized-meaningful-token-subset"
        assert disposition in ALLOWED_DISPOSITIONS
        dispositions.add(disposition)

        relation_type = proposed.get("relationType")
        assert relation_type in ALLOWED_RELATION_TYPES, f"invalid relation type in {item_id}: {relation_type}"
        proposed_types.add(relation_type)

        assert set(evidence_by_theme) == candidate_ids, (
            f"evidence keys must match reviewed theme ids in {item_id}: "
            f"expected {sorted(candidate_ids)}, got {sorted(evidence_by_theme)}"
        )
        for theme_id, refs in evidence_by_theme.items():
            assert refs, f"missing evidence for {theme_id} in {item_id}"
            for ref in refs:
                record_id = ref.get("recordId")
                verses = set(ref.get("verseNumbers") or [])
                key = (theme_id, record_id)
                assert key in attested, f"unattested evidence {theme_id} / {record_id} in {item_id}"
                assert verses, f"empty verse evidence for {theme_id} / {record_id} in {item_id}"
                assert verses <= attested[key], (
                    f"verse evidence not present in thematic analysis for {theme_id} / {record_id} in {item_id}"
                )
                evidence_reference_count += 1

        assert item.get("reviewNote"), f"missing review note in {item_id}"
        assert item.get("semanticClaim") is False
        assert item.get("requiresHumanApproval") is True
        assert item.get("relationStatus") != "relation_validated"

    assert "retyped" in dispositions, "pilot must demonstrate candidate retyping"
    assert "rejected" in dispositions, "pilot must demonstrate candidate rejection"
    assert "broader_than" in proposed_types, "pilot should cover general/specific reasoning"
    assert "related_to" in proposed_types, "pilot should cover distinct-but-related reasoning"
    assert "variant_of" in proposed_types, "pilot should cover contextual variation reasoning"

    print(
        "Theme relation review pilot OK: "
        f"{len(decisions)} proposed decisions; {evidence_reference_count} attested evidence refs; "
        f"dispositions={sorted(dispositions)}; types={sorted(proposed_types)}; "
        "no validated relation and no public search effect"
    )


if __name__ == "__main__":
    main()
