#!/usr/bin/env python3
"""FAST regression audit for structural theme-relation candidates.

This audit deliberately validates only candidate generation. It must never promote a
candidate to a semantic relation or mutate canonical/generated data.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from report_theme_relation_candidates import audited_composite_ids, build_candidates

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index/theme-search-index.json"

EXPECTED_COMPONENTS = {
    "union-pere-nature": {"union", "pere", "nature"},
    "alliance-de-lumiere": {"alliance", "lumiere"},
    "nature-vivante": {"nature"},
    "union-et-soutien-mutuel": {"union", "soutien-mutuel"},
}


def assert_candidate_contract(candidates: list[dict]) -> None:
    for candidate in candidates:
        assert candidate["relationType"] == "component_candidate"
        assert candidate["relationStatus"] == "relation_candidate"
        assert candidate["semanticClaim"] is False
        assert candidate["requiresHumanValidation"] is True


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    assert data.get("semanticMerging") is False
    records = data.get("themes", [])

    sentinel_report = build_candidates(records, set(EXPECTED_COMPONENTS))
    by_target = {item["themeId"]: item for item in sentinel_report}
    assert set(by_target) == set(EXPECTED_COMPONENTS)

    for target_id, expected_ids in EXPECTED_COMPONENTS.items():
        candidates = by_target[target_id]["candidates"]
        observed_ids = {candidate["themeId"] for candidate in candidates}
        missing = expected_ids - observed_ids
        assert not missing, f"{target_id}: missing expected component candidate(s): {sorted(missing)}"
        assert_candidate_contract(candidates)

    audited_ids = audited_composite_ids()
    batch_report = build_candidates(records, audited_ids)
    for target in batch_report:
        assert_candidate_contract(target["candidates"])

    relation_count = sum(len(target["candidates"]) for target in batch_report)
    singleton_with_candidates = sum(
        1 for target in batch_report if target.get("occurrenceCount", 0) == 1
    )
    candidate_degree = Counter(len(target["candidates"]) for target in batch_report)
    stats = {
        "auditedCompositeThemeCount": len(audited_ids),
        "compositeThemesWithComponentCandidates": len(batch_report),
        "compositeThemesWithoutComponentCandidates": len(audited_ids) - len(batch_report),
        "componentRelationCandidateCount": relation_count,
        "singletonCompositeThemesWithCandidates": singleton_with_candidates,
        "candidateCountPerTarget": dict(sorted(candidate_degree.items())),
    }

    print(
        "Theme relation candidates OK: "
        "licorne/union-Père-nature + alliance + nature + soutien-mutuel sentinels; "
        "all batch relations remain non-semantic candidates"
    )
    print(json.dumps(stats, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
