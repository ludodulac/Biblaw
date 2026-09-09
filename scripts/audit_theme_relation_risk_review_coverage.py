#!/usr/bin/env python3
"""Audit semantic review coverage for every structurally risky candidate pair.

This audit joins the existing pilot and the dedicated risk-review batch. It proves
that each lexical candidate emitted for the 10 grammar-risk targets has an explicit
review proposal, while keeping every proposal noncanonical and human-gated.
"""
from __future__ import annotations

import json
from pathlib import Path

from report_theme_relation_candidate_risks import build_risk_report

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
REVIEW_FILES = [
    ROOT / "data/thematic-index/reviews/theme-relations-pilot.json",
    ROOT / "data/thematic-index/reviews/theme-relations-risk-review.json",
]
ALLOWED_RELATION_TYPES = {
    "equivalent_to",
    "variant_of",
    "broader_than",
    "component_of",
    "related_to",
}
ALLOWED_DISPOSITIONS = {"accepted", "retyped", "rejected"}


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
    risk_report = build_risk_report()
    risk_targets = risk_report.get("targets") or []
    assert len(risk_targets) == 10, f"expected 10 structural-risk targets, got {len(risk_targets)}"

    expected_pairs: set[tuple[str, str]] = set()
    for target in risk_targets:
        target_id = target["themeId"]
        for candidate in target.get("candidates") or []:
            expected_pairs.add((candidate["themeId"], target_id))

    attested = build_attested_occurrences()
    reviewed_pairs: dict[tuple[str, str], dict] = {}
    reviewed_target_ids: set[str] = set()
    review_decision_count = 0

    for path in REVIEW_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data.get("status") == "proposed-review-decisions", f"unexpected status in {path.name}"
        assert data.get("semanticClaim") is False, f"review batch made semantic claim: {path.name}"
        assert data.get("requiresHumanApproval") is True, f"review batch lost human gate: {path.name}"
        assert data.get("publicSearchEffect") is False, f"review batch affects public search: {path.name}"

        for decision in data.get("decisions") or []:
            candidate = decision.get("candidate") or {}
            source_id = candidate.get("sourceThemeId")
            target_id = candidate.get("targetThemeId")
            pair = (source_id, target_id)
            if pair not in expected_pairs:
                continue

            assert pair not in reviewed_pairs, f"duplicate review of structural-risk pair: {pair}"
            assert candidate.get("candidateRelationType") == "component_candidate"
            assert candidate.get("candidateBasis") == "normalized-meaningful-token-subset"
            assert decision.get("candidateDisposition") in ALLOWED_DISPOSITIONS
            assert decision.get("semanticClaim") is False
            assert decision.get("requiresHumanApproval") is True
            assert decision.get("relationStatus") != "relation_validated"

            proposed = decision.get("proposedRelation") or {}
            assert {proposed.get("sourceThemeId"), proposed.get("targetThemeId")} == {source_id, target_id}
            assert proposed.get("relationType") in ALLOWED_RELATION_TYPES

            evidence = decision.get("evidenceByThemeId") or {}
            assert set(evidence) == {source_id, target_id}, f"evidence keys mismatch for {pair}"
            for theme_id, refs in evidence.items():
                assert refs, f"missing evidence for {theme_id} in {pair}"
                for ref in refs:
                    record_id = ref.get("recordId")
                    verses = set(ref.get("verseNumbers") or [])
                    key = (theme_id, record_id)
                    assert key in attested, f"unattested evidence {key} for {pair}"
                    assert verses and verses <= attested[key], f"invalid verse evidence {key} for {pair}"

            assert decision.get("reviewNote"), f"missing review note for {pair}"
            reviewed_pairs[pair] = decision
            reviewed_target_ids.add(target_id)
            review_decision_count += 1

    missing_pairs = sorted(expected_pairs - set(reviewed_pairs))
    extra_pairs = sorted(set(reviewed_pairs) - expected_pairs)
    assert not missing_pairs, f"structural-risk candidate pair(s) not reviewed: {missing_pairs}"
    assert not extra_pairs, f"unexpected structural-risk reviewed pair(s): {extra_pairs}"

    expected_target_ids = {item["themeId"] for item in risk_targets}
    assert reviewed_target_ids == expected_target_ids, (
        f"risk target coverage mismatch: missing={sorted(expected_target_ids - reviewed_target_ids)}"
    )

    component_acceptances = [
        pair for pair, decision in reviewed_pairs.items()
        if (decision.get("proposedRelation") or {}).get("relationType") == "component_of"
    ]
    assert not component_acceptances, (
        "grammar-risk candidates must not be accepted as component_of in the reviewed risk set; "
        f"found {component_acceptances}"
    )

    print(
        "Structural-risk review coverage OK: "
        f"{len(expected_target_ids)} target(s); {len(expected_pairs)} candidate pair(s); "
        f"{review_decision_count} explicit review decision(s); 0 component_of acceptance; "
        "all remain proposed and human-gated"
    )


if __name__ == "__main__":
    main()
