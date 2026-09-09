#!/usr/bin/env python3
"""Audit that the relation review queue ranks evidence availability, not semantics."""
from __future__ import annotations

from report_theme_relation_review_queue import build_queue, reviewed_pairs


def main() -> None:
    report = build_queue(limit=30)
    assert report.get("recordType") == "theme-relation-review-queue"
    assert report.get("semanticClaim") is False
    assert report.get("automaticDisposition") is False
    assert report.get("reviewedPairCount") == len(reviewed_pairs())
    assert report.get("primaryQueueDiversityPolicy") == "max-one-pair-per-source-theme"

    items = report.get("items") or []
    assert items, "review queue must expose unreviewed candidate pairs"
    done = reviewed_pairs()
    order = {"ready-high": 0, "ready-standard": 1, "needs-evidence": 2}
    previous_key = None
    seen_sources: set[str] = set()

    for item in items:
        pair = (item.get("sourceThemeId"), item.get("targetThemeId"))
        assert pair not in done, f"already reviewed pair leaked into queue: {pair}"
        assert item.get("relationStatus") == "relation_candidate"
        assert item.get("semanticClaim") is False
        assert item.get("requiresHumanValidation") is True
        assert item.get("reviewReadiness") in order
        source_id = item.get("sourceThemeId")
        assert source_id not in seen_sources, f"source theme monopolizes primary queue: {source_id}"
        seen_sources.add(source_id)

        basis = item.get("readinessBasis") or {}
        if item["reviewReadiness"] == "ready-high":
            assert basis.get("sourceStrongEvidenceCount", 0) > 0
            assert basis.get("targetStrongEvidenceCount", 0) > 0
        elif item["reviewReadiness"] == "ready-standard":
            assert basis.get("sourceAttestedEvidenceCount", 0) > 0
            assert basis.get("targetAttestedEvidenceCount", 0) > 0

        key = (
            order[item["reviewReadiness"]],
            item.get("targetOccurrenceCount", 0),
            -item.get("sourceOccurrenceCount", 0),
            item.get("targetThemeId"),
            item.get("sourceThemeId"),
        )
        if previous_key is not None:
            assert previous_key <= key, "review queue ordering is not deterministic"
        previous_key = key

    counts = report.get("readinessCounts") or {}
    assert sum(counts.values()) == report.get("unreviewedCandidatePairCount")
    assert counts.get("ready-high", 0) > 0, "expected evidence-ready unreviewed candidates"
    assert len(seen_sources) >= 6, "primary queue should expose varied source themes"

    print(
        "Theme relation review queue OK: "
        f"reviewed={report['reviewedPairCount']}; unreviewed={report['unreviewedCandidatePairCount']}; "
        f"primarySources={len(seen_sources)}; readiness={counts}; queue remains non-semantic"
    )


if __name__ == "__main__":
    main()
