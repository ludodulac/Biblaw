#!/usr/bin/env python3
"""Audit that structural-risk diagnostics prioritize review without making semantic decisions."""
from __future__ import annotations

from report_theme_relation_candidate_risks import build_risk_report


def main() -> None:
    report = build_risk_report()
    assert report.get("recordType") == "theme-relation-candidate-risk-report"
    assert report.get("semanticClaim") is False
    assert report.get("automaticDisposition") is False

    targets = report.get("targets") or []
    assert targets, "risk report must expose review targets"
    by_id = {item["themeId"]: item for item in targets}

    opposition_sentinels = {
        "discernement-contre-imitation",
        "concret-contre-abstraction",
    }
    for theme_id in opposition_sentinels:
        item = by_id.get(theme_id)
        assert item, f"missing opposition sentinel: {theme_id}"
        assert item.get("reviewPriority") == "review-first"
        assert "negation-or-opposition-marker" in (item.get("riskMarkers") or [])
        assert item.get("automaticDisposition") is False
        assert item.get("semanticClaim") is False
        assert item.get("requiresHumanValidation") is True

    relational_sentinels = {
        "union-pere-nature",
        "dialogue-avec-la-nature",
    }
    for theme_id in relational_sentinels:
        item = by_id.get(theme_id)
        assert item, f"missing relational sentinel: {theme_id}"
        assert item.get("reviewPriority") == "review-next"
        assert "negation-or-opposition-marker" not in (item.get("riskMarkers") or [])
        assert item.get("automaticDisposition") is False

    for item in targets:
        assert item.get("reviewPriority") in {"review-first", "review-next"}
        assert item.get("automaticDisposition") is False
        assert item.get("semanticClaim") is False
        assert item.get("requiresHumanValidation") is True
        for candidate in item.get("candidates") or []:
            assert candidate.get("relationStatus") == "relation_candidate"
            assert candidate.get("semanticClaim") is False
            assert candidate.get("requiresHumanValidation") is True

    first_count = sum(1 for item in targets if item.get("reviewPriority") == "review-first")
    next_count = sum(1 for item in targets if item.get("reviewPriority") == "review-next")
    assert first_count >= 2, "expected at least the two known opposition cases"
    assert next_count >= 1, "expected relational-word review cases"

    print(
        "Theme relation candidate risk priority OK: "
        f"{len(targets)} risk target(s); review-first={first_count}; review-next={next_count}; "
        "no automatic semantic disposition"
    )


if __name__ == "__main__":
    main()
