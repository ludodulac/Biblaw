#!/usr/bin/env python3
"""FAST audit for noncanonical semantic theme case studies.

The case studies are review material only. This audit verifies that they stay
noncanonical, use only the contracted relation vocabulary, and cite real theme
occurrences/verses from the existing thematic analyses. It never promotes a
relation or rebuilds the corpus.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "data/thematic-index/reviews"
BOOKS = ROOT / "data/thematic-index/books"

ALLOWED_TYPES = {
    "equivalent_to",
    "variant_of",
    "broader_than",
    "component_of",
    "related_to",
}


def load_attestations() -> dict[tuple[str, str], set[int]]:
    attested: dict[tuple[str, str], set[int]] = {}
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for analysis in data.get("psalmAnalyses") or []:
            record_id = analysis.get("recordId")
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if not record_id or not theme_id:
                    continue
                attested[(theme_id, record_id)] = set(theme.get("verseNumbers") or [])
    return attested


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    paths = sorted(REVIEWS.glob("case-*.json"))
    require(bool(paths), "No semantic case studies found")
    attested = load_attestations()

    case_count = 0
    assessment_count = 0
    relation_types: set[str] = set()
    ids: set[str] = set()

    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        prefix = path.name
        case_count += 1

        require(data.get("schemaVersion") == 1, f"{prefix}: schemaVersion must be 1")
        require(data.get("recordType") == "theme-semantic-case-study", f"{prefix}: bad recordType")
        require(data.get("status") == "proposed-review-decisions", f"{prefix}: bad status")
        require(data.get("semanticClaim") is False, f"{prefix}: semanticClaim must stay false")
        require(data.get("requiresHumanApproval") is True, f"{prefix}: requiresHumanApproval must stay true")
        require(data.get("publicSearchEffect") is False, f"{prefix}: publicSearchEffect must stay false")
        require(bool(data.get("anchorThemeId")), f"{prefix}: missing anchorThemeId")

        assessments = data.get("relationAssessments") or []
        require(bool(assessments), f"{prefix}: no relation assessments")

        for assessment in assessments:
            assessment_count += 1
            relation_id = assessment.get("id")
            require(bool(relation_id), f"{prefix}: assessment missing id")
            require(relation_id not in ids, f"Duplicate semantic case relation id: {relation_id}")
            ids.add(relation_id)

            source = assessment.get("sourceThemeId")
            target = assessment.get("targetThemeId")
            relation_type = assessment.get("proposedRelationType")
            require(source and target and source != target, f"{prefix}/{relation_id}: invalid endpoints")
            require(relation_type in ALLOWED_TYPES, f"{prefix}/{relation_id}: invalid relation type {relation_type}")
            require(assessment.get("semanticClaim") is False, f"{prefix}/{relation_id}: semanticClaim must stay false")
            relation_types.add(relation_type)

            evidence = assessment.get("evidenceByThemeId") or {}
            require(set(evidence) == {source, target}, f"{prefix}/{relation_id}: evidence keys must match endpoints")

            for theme_id, refs in evidence.items():
                require(bool(refs), f"{prefix}/{relation_id}: missing evidence for {theme_id}")
                for ref in refs:
                    record_id = ref.get("recordId")
                    verses = ref.get("verseNumbers") or []
                    key = (theme_id, record_id)
                    require(key in attested, f"{prefix}/{relation_id}: unattested {theme_id} in {record_id}")
                    require(bool(verses), f"{prefix}/{relation_id}: empty verse evidence for {theme_id}/{record_id}")
                    require(all(isinstance(v, int) for v in verses), f"{prefix}/{relation_id}: non-integer verse number")
                    require(set(verses) <= attested[key], f"{prefix}/{relation_id}: verse evidence drift for {theme_id}/{record_id}")

    # Boundary sentinels established by corpus review. These protect relation
    # shape, not semantic validation: every case remains human-approval-only.
    sentinels = {
        "case-pierre--pierre-verte": ("pierre", "pierre-verte", "broader_than"),
        "case-pensee--pensee-vivante": ("pensee", "pensee-vivante", "broader_than"),
    }
    found: dict[str, tuple[str, str, str]] = {}
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for assessment in data.get("relationAssessments") or []:
            rid = assessment.get("id")
            if rid in sentinels:
                found[rid] = (
                    assessment.get("sourceThemeId"),
                    assessment.get("targetThemeId"),
                    assessment.get("proposedRelationType"),
                )
    require(found == sentinels, f"Semantic boundary sentinel drift: expected {sentinels}, got {found}")

    print(json.dumps({
        "schemaVersion": 1,
        "recordType": "theme-semantic-case-study-audit",
        "caseStudyCount": case_count,
        "relationAssessmentCount": assessment_count,
        "proposedRelationTypes": sorted(relation_types),
        "semanticClaim": False,
        "publicSearchEffect": False,
        "status": "ok",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
