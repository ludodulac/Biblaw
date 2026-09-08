#!/usr/bin/env python3
"""FAST regression audit for structural theme-relation candidates.

This audit deliberately validates only candidate generation. It must never promote a
candidate to a semantic relation or mutate canonical/generated data.
"""
from __future__ import annotations

import json
from pathlib import Path

from report_theme_relation_candidates import build_candidates

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index/theme-search-index.json"

EXPECTED_COMPONENTS = {
    "union-pere-nature": {"union", "pere", "nature"},
    "alliance-de-lumiere": {"alliance", "lumiere"},
    "nature-vivante": {"nature"},
    "union-et-soutien-mutuel": {"union", "soutien-mutuel"},
}


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    assert data.get("semanticMerging") is False

    report = build_candidates(data.get("themes", []), set(EXPECTED_COMPONENTS))
    by_target = {item["themeId"]: item for item in report}
    assert set(by_target) == set(EXPECTED_COMPONENTS)

    for target_id, expected_ids in EXPECTED_COMPONENTS.items():
        candidates = by_target[target_id]["candidates"]
        observed_ids = {candidate["themeId"] for candidate in candidates}
        missing = expected_ids - observed_ids
        assert not missing, f"{target_id}: missing expected component candidate(s): {sorted(missing)}"
        for candidate in candidates:
            assert candidate["relationType"] == "component_candidate"
            assert candidate["relationStatus"] == "relation_candidate"
            assert candidate["semanticClaim"] is False
            assert candidate["requiresHumanValidation"] is True

    print(
        "Theme relation candidates OK: "
        "licorne/union-Père-nature + alliance + nature + soutien-mutuel sentinels; "
        "all remain non-semantic candidates"
    )


if __name__ == "__main__":
    main()
