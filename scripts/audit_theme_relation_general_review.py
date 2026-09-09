#!/usr/bin/env python3
"""Audit the noncanonical diverse general relation review batch."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "data/thematic-index/reviews/theme-relations-general-review.json"
BOOKS = ROOT / "data/thematic-index/books"
EXPECTED_COMPONENT_PAIRS = {
    ("corps", "corps-ame-esprit"),
    ("ame", "corps-ame-esprit"),
    ("esprit", "corps-ame-esprit"),
    ("terre", "terre-eau-air-feu"),
    ("eau", "terre-eau-air-feu"),
    ("air", "terre-eau-air-feu"),
    ("feu", "terre-eau-air-feu"),
    ("pratique", "pratique-et-conscience"),
    ("conscience", "pratique-et-conscience"),
    ("pensee", "maitrise-pensee-parole"),
    ("parole", "maitrise-pensee-parole"),
}
EXPECTED_MODIFIER_REJECTIONS = {
    ("lumiere", "apparences-et-fausse-lumiere"),
    ("dieux", "idoles-et-faux-dieux"),
}
EXPECTED_DEFERRED = {"maitrise", "esprit-et-corps", "eau-et-air"}


def build_attested() -> dict[tuple[str, str], set[int]]:
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
    data = json.loads(REVIEW.read_text(encoding="utf-8"))
    assert data.get("recordType") == "theme-relation-review-batch"
    assert data.get("status") == "proposed-review-decisions"
    assert data.get("semanticClaim") is False
    assert data.get("requiresHumanApproval") is True
    assert data.get("publicSearchEffect") is False
    assert set(data.get("deferredCandidateIds") or []) == EXPECTED_DEFERRED

    attested = build_attested()
    decisions = data.get("decisions") or []
    assert len(decisions) == 13, f"expected 13 decisions, got {len(decisions)}"

    seen_pairs: set[tuple[str, str]] = set()
    component_pairs: set[tuple[str, str]] = set()
    rejected_pairs: set[tuple[str, str]] = set()
    evidence_ref_count = 0

    for decision in decisions:
        candidate = decision.get("candidate") or {}
        source_id = candidate.get("sourceThemeId")
        target_id = candidate.get("targetThemeId")
        pair = (source_id, target_id)
        assert source_id and target_id and pair not in seen_pairs
        seen_pairs.add(pair)
        assert candidate.get("candidateRelationType") == "component_candidate"
        assert candidate.get("candidateBasis") == "normalized-meaningful-token-subset"

        proposed = decision.get("proposedRelation") or {}
        assert {proposed.get("sourceThemeId"), proposed.get("targetThemeId")} == {source_id, target_id}
        disposition = decision.get("candidateDisposition")
        relation_type = proposed.get("relationType")

        if pair in EXPECTED_COMPONENT_PAIRS:
            assert disposition == "accepted", f"component sentinel not accepted: {pair}"
            assert relation_type == "component_of", f"component sentinel retyped: {pair}"
            component_pairs.add(pair)
        elif pair in EXPECTED_MODIFIER_REJECTIONS:
            assert disposition == "rejected", f"modifier false-positive not rejected: {pair}"
            assert relation_type == "related_to", f"modifier false-positive type changed: {pair}"
            rejected_pairs.add(pair)
        else:
            raise AssertionError(f"unexpected decision pair: {pair}")

        evidence = decision.get("evidenceByThemeId") or {}
        assert set(evidence) == {source_id, target_id}, f"evidence keys mismatch: {pair}"
        for theme_id, refs in evidence.items():
            assert refs, f"missing evidence: {theme_id} / {pair}"
            for ref in refs:
                record_id = ref.get("recordId")
                verses = set(ref.get("verseNumbers") or [])
                key = (theme_id, record_id)
                assert key in attested, f"unattested evidence: {key} / {pair}"
                assert verses and verses <= attested[key], f"invalid verses: {key} / {pair}"
                evidence_ref_count += 1

        assert decision.get("reviewNote")
        assert decision.get("semanticClaim") is False
        assert decision.get("requiresHumanApproval") is True
        assert decision.get("relationStatus") != "relation_validated"

    assert component_pairs == EXPECTED_COMPONENT_PAIRS
    assert rejected_pairs == EXPECTED_MODIFIER_REJECTIONS
    assert not (seen_pairs & {(item, "") for item in EXPECTED_DEFERRED})

    print(
        "General theme relation review OK: "
        f"{len(decisions)} proposed decision(s); {len(component_pairs)} component_of acceptance(s); "
        f"{len(rejected_pairs)} modifier-driven rejection(s); {evidence_ref_count} attested evidence refs; "
        f"deferred={sorted(EXPECTED_DEFERRED)}; no validated relation and no public search effect"
    )


if __name__ == "__main__":
    main()
