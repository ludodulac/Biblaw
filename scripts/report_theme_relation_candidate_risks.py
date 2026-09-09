#!/usr/bin/env python3
"""Flag lexical relation candidates whose target wording carries structural risk.

This FAST, read-only diagnostic reuses the existing candidate generator. It does
not decide that a candidate is wrong; it only identifies cases where discarded
function words, negation or opposition markers can materially change meaning.

Priority is deliberately coarse and procedural: it only controls review order.
It never predicts or validates a semantic relation type.
"""
from __future__ import annotations

import json
from collections import Counter

from report_theme_relation_candidates import (
    INDEX,
    audited_composite_ids,
    build_candidates,
)

NEGATION_OR_OPPOSITION = {
    "non", "sans", "contre", "absence", "refus", "rejet", "opposition", "negation",
}
RELATIONAL_MARKERS = {
    "avec", "vers", "entre", "au", "aux", "dans", "par", "pour", "sans", "contre",
}


def alias_tokens(record: dict) -> list[str]:
    aliases = record.get("normalizedAliases") or []
    return aliases[0].split() if aliases else []


def build_risk_report() -> dict:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    assert data.get("semanticMerging") is False
    records = data.get("themes") or []
    by_id = {record.get("themeId"): record for record in records if record.get("themeId")}

    candidate_targets = build_candidates(records, audited_composite_ids())
    risks = []
    marker_counts: Counter[str] = Counter()
    priority_counts: Counter[str] = Counter()

    for target in candidate_targets:
        record = by_id[target["themeId"]]
        raw_tokens = set(alias_tokens(record))
        negation = sorted(raw_tokens & NEGATION_OR_OPPOSITION)
        relational = sorted(raw_tokens & RELATIONAL_MARKERS)
        if not negation and not relational:
            continue

        risk_markers = []
        if negation:
            risk_markers.append("negation-or-opposition-marker")
            marker_counts["negation-or-opposition-marker"] += 1
        if relational:
            risk_markers.append("relational-function-word-dropped-by-component-tokenization")
            marker_counts["relational-function-word-dropped-by-component-tokenization"] += 1

        priority_tier = "review-first" if negation else "review-next"
        priority_counts[priority_tier] += 1

        risks.append(
            {
                "themeId": target["themeId"],
                "label": target.get("label"),
                "occurrenceCount": target.get("occurrenceCount", 0),
                "reviewPriority": priority_tier,
                "automaticDisposition": False,
                "riskMarkers": risk_markers,
                "structuralTokens": sorted(set(negation + relational)),
                "candidateCount": len(target.get("candidates") or []),
                "candidates": target.get("candidates") or [],
                "semanticClaim": False,
                "requiresHumanValidation": True,
            }
        )

    risks.sort(
        key=lambda item: (
            0 if item["reviewPriority"] == "review-first" else 1,
            -item["candidateCount"],
            item["themeId"],
        )
    )

    return {
        "schemaVersion": 1,
        "recordType": "theme-relation-candidate-risk-report",
        "semanticClaim": False,
        "automaticDisposition": False,
        "auditedCompositeThemeCount": len(audited_composite_ids()),
        "riskTargetCount": len(risks),
        "riskMarkerCounts": dict(sorted(marker_counts.items())),
        "reviewPriorityCounts": dict(sorted(priority_counts.items())),
        "targets": risks[:30],
        "interpretation": (
            "Risk markers only prioritize human review. review-first means wording contains a negation/opposition marker; "
            "review-next means another relational function word may have been lost by token-subset candidate generation. "
            "Neither tier predicts, rejects or validates a semantic relation."
        ),
    }


def main() -> None:
    print(json.dumps(build_risk_report(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
