#!/usr/bin/env python3
"""Rank unreviewed structural relation candidates by evidence readiness only.

This FAST/TARGETED read-only queue does not estimate semantic truth. It reuses the
186 audited composite targets and the existing per-book thematic analyses, removes
candidate pairs already covered by explicit review decisions, and orders the rest
by how easy they are to inspect with attested evidence already present.

The displayed primary queue is diversified across source themes so a highly frequent
source cannot monopolize the next manual review batch. This is a review-sampling
policy only, not a semantic score.
"""
from __future__ import annotations

import json
from pathlib import Path

from report_theme_relation_candidates import INDEX, audited_composite_ids, build_candidates

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
REVIEW_FILES = [
    ROOT / "data/thematic-index/reviews/theme-relations-pilot.json",
    ROOT / "data/thematic-index/reviews/theme-relations-risk-review.json",
    ROOT / "data/thematic-index/reviews/theme-relations-general-review.json",
]


def reviewed_pairs() -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for path in REVIEW_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        for decision in data.get("decisions") or []:
            candidate = decision.get("candidate") or {}
            source_id = candidate.get("sourceThemeId")
            target_id = candidate.get("targetThemeId")
            if source_id and target_id:
                pairs.add((source_id, target_id))
    return pairs


def evidence_summary() -> dict[str, dict[str, int | bool]]:
    summary: dict[str, dict[str, int | bool]] = {}
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for analysis in data.get("psalmAnalyses") or []:
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if not theme_id:
                    continue
                row = summary.setdefault(
                    theme_id,
                    {"occurrenceCount": 0, "attestedEvidenceCount": 0, "strongEvidenceCount": 0},
                )
                row["occurrenceCount"] = int(row["occurrenceCount"]) + 1
                has_evidence = bool(theme.get("verseNumbers")) and bool(theme.get("teaching"))
                if has_evidence:
                    row["attestedEvidenceCount"] = int(row["attestedEvidenceCount"]) + 1
                is_strong = (
                    has_evidence
                    and theme.get("directness") == "direct"
                    and theme.get("importance") in {"central", "important"}
                )
                if is_strong:
                    row["strongEvidenceCount"] = int(row["strongEvidenceCount"]) + 1
    return summary


def readiness(left: dict, right: dict) -> str:
    if int(left.get("strongEvidenceCount", 0)) > 0 and int(right.get("strongEvidenceCount", 0)) > 0:
        return "ready-high"
    if int(left.get("attestedEvidenceCount", 0)) > 0 and int(right.get("attestedEvidenceCount", 0)) > 0:
        return "ready-standard"
    return "needs-evidence"


def diversify_by_source(items: list[dict], limit: int) -> list[dict]:
    """Take at most one pair per source theme in the primary displayed queue."""
    selected = []
    seen_sources: set[str] = set()
    for item in items:
        source_id = item["sourceThemeId"]
        if source_id in seen_sources:
            continue
        selected.append(item)
        seen_sources.add(source_id)
        if len(selected) >= max(limit, 0):
            break
    return selected


def build_queue(limit: int = 20) -> dict:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    records = index.get("themes") or []
    candidates = build_candidates(records, audited_composite_ids())
    evidence = evidence_summary()
    done = reviewed_pairs()

    all_items = []
    for target in candidates:
        target_id = target["themeId"]
        target_evidence = evidence.get(target_id, {})
        for candidate in target.get("candidates") or []:
            source_id = candidate["themeId"]
            pair = (source_id, target_id)
            if pair in done:
                continue
            source_evidence = evidence.get(source_id, {})
            tier = readiness(source_evidence, target_evidence)
            all_items.append(
                {
                    "sourceThemeId": source_id,
                    "sourceLabel": candidate.get("label"),
                    "targetThemeId": target_id,
                    "targetLabel": target.get("label"),
                    "candidateBasis": candidate.get("candidateBasis"),
                    "relationStatus": "relation_candidate",
                    "semanticClaim": False,
                    "requiresHumanValidation": True,
                    "reviewReadiness": tier,
                    "readinessBasis": {
                        "sourceStrongEvidenceCount": int(source_evidence.get("strongEvidenceCount", 0)),
                        "targetStrongEvidenceCount": int(target_evidence.get("strongEvidenceCount", 0)),
                        "sourceAttestedEvidenceCount": int(source_evidence.get("attestedEvidenceCount", 0)),
                        "targetAttestedEvidenceCount": int(target_evidence.get("attestedEvidenceCount", 0)),
                    },
                    "sourceOccurrenceCount": int(source_evidence.get("occurrenceCount", 0)),
                    "targetOccurrenceCount": int(target_evidence.get("occurrenceCount", 0)),
                }
            )

    order = {"ready-high": 0, "ready-standard": 1, "needs-evidence": 2}
    all_items.sort(
        key=lambda item: (
            order[item["reviewReadiness"]],
            item["targetOccurrenceCount"],
            -item["sourceOccurrenceCount"],
            item["targetThemeId"],
            item["sourceThemeId"],
        )
    )

    counts = {tier: sum(1 for item in all_items if item["reviewReadiness"] == tier) for tier in order}
    primary_items = diversify_by_source(all_items, limit)
    return {
        "schemaVersion": 1,
        "recordType": "theme-relation-review-queue",
        "semanticClaim": False,
        "automaticDisposition": False,
        "sourceCandidateScope": "theme-quality-audit.reviewCandidates.compositeLabels",
        "reviewedPairCount": len(done),
        "unreviewedCandidatePairCount": len(all_items),
        "readinessCounts": counts,
        "primaryQueueDiversityPolicy": "max-one-pair-per-source-theme",
        "items": primary_items,
        "interpretation": (
            "Review readiness measures availability of attested corpus evidence only. It does not score semantic plausibility, "
            "similarity, correctness or expected relation type. Within a readiness tier, rarer target formulations are surfaced first; "
            "the displayed primary queue then keeps at most one pair per source theme to avoid frequency-driven review bias."
        ),
    }


def main() -> None:
    print(json.dumps(build_queue(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
