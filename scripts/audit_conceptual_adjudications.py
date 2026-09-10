#!/usr/bin/env python3
"""Audit traceable conceptual adjudications without promoting semantic claims automatically."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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

    require(store.get("schemaVersion") == 1, "adjudication schemaVersion must be 1")
    require(store.get("recordType") == "conceptual-adjudications", "unexpected adjudication store type")
    require(store.get("status") == "canonical-editorial-review-log", "adjudication store must be editorial")
    require(store.get("generated") is False, "adjudication store must never be generated")
    require(store.get("publicSearchEffect") is False, "adjudications must not affect public search")
    require(set(store.get("allowedDecisions", [])) == ALLOWED_DECISIONS, "decision vocabulary drift")

    ids: set[str] = set()
    approved_count = 0
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

        passages = record.get("passagesConsulted") or {}
        require(set(passages) == set(theme_ids), f"{record_id}: passagesConsulted must cover both themes")
        for theme_id in theme_ids:
            refs = passages.get(theme_id)
            require(isinstance(refs, list) and refs, f"{record_id}: missing consulted passage for {theme_id}")
            for ref in refs:
                source = occurrences.get((theme_id, ref.get("recordId")))
                require(source is not None, f"{record_id}: unattested passage {theme_id}/{ref.get('recordId')}")
                verses = ref.get("verseNumbers")
                require(isinstance(verses, list) and verses, f"{record_id}: verseNumbers required")
                require(set(verses).issubset(source["verseNumbers"]), f"{record_id}: unattested verse number")
                require(ref.get("teaching") == source["teaching"], f"{record_id}: teaching drift")

        decision = record.get("decision")
        require(decision in ALLOWED_DECISIONS, f"{record_id}: invalid decision {decision}")
        review = record.get("review") or {}
        mapping = record.get("canonicalMapping")
        justification = record.get("humanJustification")

        provenance = record.get("provenance") or {}
        artifact = provenance.get("candidateArtifact") or {}
        require(artifact.get("workflowRunId"), f"{record_id}: candidate workflow provenance required")
        require(artifact.get("artifactName") == "conceptual-adjudication-candidates", f"{record_id}: candidate artifact name required")
        require(str(artifact.get("artifactDigest") or "").startswith("sha256:"), f"{record_id}: candidate digest required")
        require(provenance.get("canonicalSources"), f"{record_id}: canonical sources required")

        if review.get("status") == "human-approved":
            approved_count += 1
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
        else:
            require(review.get("status") == "needs-human-review", f"{record_id}: unsupported review status")
            require(mapping is None, f"{record_id}: unapproved adjudication must not map to canonical relation")
            require(justification is None, f"{record_id}: do not fabricate human justification before review")
            require(decision == "UNRESOLVED", f"{record_id}: pending human review must remain UNRESOLVED")
            unresolved_count += 1

    require(approved_count >= 1, "pilot must retain at least one traceable human-approved calibration case")
    require(unresolved_count >= 1, "pilot must prove UNRESOLVED is preserved without canonical promotion")
    print(
        f"Conceptual adjudications OK: {len(ids)} record(s); {approved_count} human-approved; "
        f"{unresolved_count} unresolved; public search effect remains false"
    )


if __name__ == "__main__":
    main()
