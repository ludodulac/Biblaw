#!/usr/bin/env python3
"""Audit traceable conceptual adjudications without promoting semantic claims automatically."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from normalize_known_theme_identifiers import LEGACY_TO_CANONICAL

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
ADJUDICATIONS = INDEX / "theme-adjudications.json"
VALIDATED = INDEX / "theme-relations-validated.json"
BOOKS_DIR = INDEX / "books"

ALLOWED_DECISIONS = {
    "SAME",
    "VARIANT",
    "MORE_GENERAL_SPECIFIC",
    "COMPONENT",
    "RELATED",
    "NO_RELATION",
    "UNRESOLVED",
}
DECISION_TO_RELATION = {
    "SAME": "equivalent_to",
    "VARIANT": "variant_of",
    "MORE_GENERAL_SPECIFIC": "broader_than",
    "COMPONENT": "component_of",
    "RELATED": "related_to",
}


class AuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def load_occurrences() -> dict[tuple[str, str], dict[str, Any]]:
    occurrences: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(BOOKS_DIR.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for psalm in data.get("psalmAnalyses", []):
            record_id = psalm.get("recordId")
            for theme in psalm.get("themes", []):
                theme_id = theme.get("themeId")
                if not record_id or not theme_id:
                    continue
                occurrences[(theme_id, record_id)] = {
                    "verseNumbers": set(theme.get("verseNumbers") or []),
                    "teaching": theme.get("teaching"),
                }
    return occurrences


def main() -> None:
    store = json.loads(ADJUDICATIONS.read_text(encoding="utf-8"))
    validated_store = json.loads(VALIDATED.read_text(encoding="utf-8"))
    validated = {r["id"]: r for r in validated_store.get("relations", [])}
    occurrences = load_occurrences()
    canonical_theme_ids = {theme_id for theme_id, _ in occurrences}

    require(store.get("schemaVersion") == 1, "adjudication schemaVersion must be 1")
    require(store.get("recordType") == "conceptual-adjudications", "unexpected adjudication store type")
    require(store.get("status") == "canonical-editorial-review-log", "adjudication store must be editorial")
    require(store.get("generated") is False, "adjudication store must never be generated")
    require(store.get("publicSearchEffect") is False, "adjudications must not affect public search")
    require(set(store.get("allowedDecisions", [])) == ALLOWED_DECISIONS, "decision vocabulary drift")

    ids: set[str] = set()
    approved_count = 0
    normalization_count = 0
    unresolved_count = 0
    for record in store.get("records", []):
        record_id = record.get("id")
        require(bool(record_id) and record_id not in ids, f"invalid/duplicate adjudication id: {record_id}")
        ids.add(record_id)

        themes = record.get("themes") or []
        require(len(themes) == 2, f"{record_id}: exactly two themes are required")
        theme_ids = [t.get("themeId") for t in themes]
        require(all(theme_ids) and len(set(theme_ids)) == 2, f"{record_id}: invalid theme pair")
        require(bool(str(record.get("candidateId") or "").strip()), f"{record_id}: candidateId is required")
        require(bool(str(record.get("triggeringQuestion") or "").strip()), f"{record_id}: triggering question is required")
        require(record.get("discoverySignals"), f"{record_id}: discovery signals are required")
        require(record.get("corpusForRelation") is not None, f"{record_id}: corpusForRelation is required")
        require(record.get("corpusAgainstOrRefuting") is not None, f"{record_id}: corpusAgainstOrRefuting is required")

        decision = record.get("decision")
        require(decision in ALLOWED_DECISIONS, f"{record_id}: invalid decision {decision}")
        review = record.get("review") or {}
        review_status = review.get("status")
        mapping = record.get("canonicalMapping")
        justification = record.get("humanJustification")
        is_identifier_normalization = review_status == "ai-assisted-user-approved"
        legacy_theme_id = record.get("legacyThemeId")
        canonical_theme_id = record.get("canonicalThemeId")

        passages = record.get("passagesConsulted") or {}
        require(set(passages) == set(theme_ids), f"{record_id}: passagesConsulted must cover both themes")
        for theme_id in theme_ids:
            refs = passages.get(theme_id)
            require(isinstance(refs, list) and refs, f"{record_id}: missing consulted passage for {theme_id}")
            for ref in refs:
                lookup_theme_id = canonical_theme_id if is_identifier_normalization and theme_id == legacy_theme_id else theme_id
                source = occurrences.get((lookup_theme_id, ref.get("recordId")))
                require(source is not None, f"{record_id}: unattested passage {theme_id}/{ref.get('recordId')}")
                verses = ref.get("verseNumbers")
                require(isinstance(verses, list) and verses, f"{record_id}: verseNumbers required")
                require(set(verses).issubset(source["verseNumbers"]), f"{record_id}: unattested verse number")
                require(ref.get("teaching") == source["teaching"], f"{record_id}: teaching drift")

        provenance = record.get("provenance") or {}
        require(provenance.get("canonicalSources"), f"{record_id}: canonical sources required")

        if review_status == "human-approved":
            approved_count += 1
            artifact = provenance.get("candidateArtifact") or {}
            require(artifact.get("workflowRunId"), f"{record_id}: candidate workflow provenance required")
            require(artifact.get("artifactName") == "conceptual-adjudication-candidates", f"{record_id}: candidate artifact name required")
            require(str(artifact.get("artifactDigest") or "").startswith("sha256:"), f"{record_id}: candidate digest required")
            require(isinstance(justification, str) and justification.strip(), f"{record_id}: human justification required")
            require(decision not in {"UNRESOLVED"}, f"{record_id}: unresolved cannot be human-approved as a semantic relation")
            if decision == "NO_RELATION":
                require(mapping is None, f"{record_id}: NO_RELATION must not map to canonical relation")
            else:
                require(isinstance(mapping, dict), f"{record_id}: positive human decision needs canonical mapping")
                require(mapping.get("relationType") == DECISION_TO_RELATION[decision], f"{record_id}: decision/relation mapping mismatch")
                validated_id = mapping.get("validatedRelationId")
                require(validated_id in validated, f"{record_id}: mapped validated relation missing")
                relation = validated[validated_id]
                require(relation.get("relationType") == mapping.get("relationType"), f"{record_id}: validated relation type mismatch")
                require(relation.get("sourceThemeId") == mapping.get("sourceThemeId"), f"{record_id}: validated source mismatch")
                require(relation.get("targetThemeId") == mapping.get("targetThemeId"), f"{record_id}: validated target mismatch")
        elif is_identifier_normalization:
            normalization_count += 1
            require(decision == "VARIANT", f"{record_id}: ai-assisted-user-approved is restricted to VARIANT identifier normalization")
            require(record.get("resolution") == "identifier-normalization", f"{record_id}: ai-assisted-user-approved requires identifier-normalization")
            require(bool(legacy_theme_id) and bool(canonical_theme_id) and legacy_theme_id != canonical_theme_id, f"{record_id}: explicit distinct legacy/canonical ids required")
            require(set(theme_ids) == {legacy_theme_id, canonical_theme_id}, f"{record_id}: adjudicated themes must match legacy/canonical ids")
            require(LEGACY_TO_CANONICAL.get(legacy_theme_id) == canonical_theme_id, f"{record_id}: exact normalization mapping is not reviewed in LEGACY_TO_CANONICAL")
            require(legacy_theme_id not in canonical_theme_ids, f"{record_id}: legacy themeId still exists in canonical books")
            require(canonical_theme_id in canonical_theme_ids, f"{record_id}: canonical themeId is not attested in canonical books")
            require(mapping is None, f"{record_id}: identifier normalization must not create a permanent semantic relation")
            require(justification is None, f"{record_id}: identifier normalization must not claim independent human justification")
            require(isinstance(record.get("approvalJustification"), str) and record["approvalJustification"].strip(), f"{record_id}: approvalJustification required")
            decision_provenance = provenance.get("decisionProvenance") or {}
            require(decision_provenance.get("type") == "ai-assisted-user-approved", f"{record_id}: exact ai-assisted-user-approved provenance required")
            require(decision_provenance.get("preparedBy") == "openai-chatgpt", f"{record_id}: AI preparation provenance required")
            require(decision_provenance.get("approvedBy") == "user", f"{record_id}: user approval provenance required")
            require(bool(decision_provenance.get("approvedOn")), f"{record_id}: approval date required")
            for relation in validated.values():
                require(
                    legacy_theme_id not in {relation.get("sourceThemeId"), relation.get("targetThemeId")},
                    f"{record_id}: legacy id must not be kept alive by a validated semantic relation",
                )
        else:
            require(review_status == "needs-human-review", f"{record_id}: unsupported review status")
            artifact = provenance.get("candidateArtifact") or {}
            require(artifact.get("workflowRunId"), f"{record_id}: candidate workflow provenance required")
            require(artifact.get("artifactName") == "conceptual-adjudication-candidates", f"{record_id}: candidate artifact name required")
            require(str(artifact.get("artifactDigest") or "").startswith("sha256:"), f"{record_id}: candidate digest required")
            require(mapping is None, f"{record_id}: unapproved adjudication must not map to canonical relation")
            require(justification is None, f"{record_id}: do not fabricate human justification before review")
            require(decision == "UNRESOLVED", f"{record_id}: pending human review must remain UNRESOLVED")
            unresolved_count += 1

    require(approved_count >= 1, "pilot must retain at least one traceable human-approved calibration case")
    require(unresolved_count >= 1, "pilot must prove UNRESOLVED is preserved without canonical promotion")
    print(
        f"Conceptual adjudications OK: {len(ids)} record(s); {approved_count} human-approved semantic; "
        f"{normalization_count} ai-assisted-user-approved identifier normalization; {unresolved_count} unresolved; "
        "public search effect remains false"
    )


if __name__ == "__main__":
    main()
