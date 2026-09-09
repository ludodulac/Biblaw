#!/usr/bin/env python3
"""Audit the noncanonical semantic relation review pilot.

The pilot must stay review-only: no validated relation, no semantic claim and no
public search effect. It must also prove that structural candidates can be both
retyped and rejected rather than automatically accepted as components.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/thematic-index/reviews/theme-relations-pilot.json"
ALLOWED_RELATION_TYPES = {
    "equivalent_to",
    "variant_of",
    "broader_than",
    "component_of",
    "related_to",
}
ALLOWED_DISPOSITIONS = {"retyped", "rejected"}


def main() -> None:
    data = json.loads(PILOT.read_text(encoding="utf-8"))
    assert data.get("recordType") == "theme-relation-review-pilot"
    assert data.get("status") == "proposed-review-decisions"
    assert data.get("semanticClaim") is False
    assert data.get("requiresHumanApproval") is True
    assert data.get("publicSearchEffect") is False

    decisions = data.get("decisions") or []
    assert decisions, "review pilot must contain decisions"

    dispositions: set[str] = set()
    proposed_types: set[str] = set()
    ids: set[str] = set()

    for item in decisions:
        item_id = item.get("id")
        assert item_id and item_id not in ids, f"duplicate or missing decision id: {item_id!r}"
        ids.add(item_id)

        candidate = item.get("candidate") or {}
        proposed = item.get("proposedRelation") or {}
        evidence = item.get("evidence") or {}
        disposition = item.get("candidateDisposition")

        assert candidate.get("sourceThemeId") and candidate.get("targetThemeId")
        assert candidate.get("candidateRelationType") == "component_candidate"
        assert candidate.get("candidateBasis") == "normalized-meaningful-token-subset"
        assert disposition in ALLOWED_DISPOSITIONS
        dispositions.add(disposition)

        assert proposed.get("sourceThemeId") and proposed.get("targetThemeId")
        relation_type = proposed.get("relationType")
        assert relation_type in ALLOWED_RELATION_TYPES, f"invalid relation type in {item_id}: {relation_type}"
        proposed_types.add(relation_type)

        assert evidence.get("sourceOccurrences"), f"missing source evidence in {item_id}"
        assert evidence.get("targetOccurrences"), f"missing target evidence in {item_id}"
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
        f"{len(decisions)} proposed decisions; dispositions={sorted(dispositions)}; "
        f"types={sorted(proposed_types)}; no validated relation and no public search effect"
    )


if __name__ == "__main__":
    main()
