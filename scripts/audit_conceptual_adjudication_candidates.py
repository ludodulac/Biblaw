#!/usr/bin/env python3
"""Audit that conceptual-adjudication candidates remain questions, not semantic claims."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
QUEUE = INDEX / "conceptual-adjudication-candidates.json"
DIRECTORY = INDEX / "theme-directory.json"
VALIDATED = INDEX / "theme-relations-validated.json"

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
directory = json.loads(DIRECTORY.read_text(encoding="utf-8"))
validated = json.loads(VALIDATED.read_text(encoding="utf-8"))
by_id = {t["id"]: t for t in directory.get("themes", [])}

assert queue["status"] == "review-questions-only"
assert queue["semanticClaim"] is False
assert queue["requiresHumanCorpusReview"] is True
assert queue["publicSearchEffect"] is False
policy = queue["policy"]
for key in (
    "automaticMergeAllowed",
    "automaticRenameAllowed",
    "automaticAliasAllowed",
    "automaticRelationCreationAllowed",
    "rarityIsSemanticEvidence",
    "lexicalContainmentIsSemanticEvidence",
    "cooccurrenceIsSemanticEvidence",
    "discoveryPriorityIsSemanticConfidence",
):
    assert policy[key] is False, key

ids = []
positive_pairs = set()
for c in queue["candidates"]:
    assert c["status"] == "question-only"
    assert "relationType" not in c and "proposedRelationType" not in c and "confidence" not in c
    ids.append(c["candidateId"])
    assert len(c["themes"]) == 2
    pair = tuple(sorted(t["themeId"] for t in c["themes"]))
    for t in c["themes"]:
        assert t["themeId"] in by_id
        assert t["representativeOccurrences"], f"candidate without corpus context: {c['candidateId']}"
        for o in t["representativeOccurrences"]:
            assert o["recordId"]
            assert o["verseNumbers"], f"missing verse provenance: {c['candidateId']}"
            assert str(o["teaching"] or "").strip(), f"missing teaching provenance: {c['candidateId']}"
    assert set(c["adjudicationQuestion"]["allowedOutcomes"]) == set(queue["allowedFinalAdjudications"])
    if any(s["kind"] == "validated-relation-positive-control" for s in c["discoverySignals"]):
        positive_pairs.add(pair)
        assert c.get("calibration", {}).get("mustNotBeReinferred") is True

assert len(ids) == len(set(ids)), "duplicate candidate ids"
expected_positive = {
    tuple(sorted((r["sourceThemeId"], r["targetThemeId"])))
    for r in validated.get("relations", [])
}
assert positive_pairs == expected_positive, (positive_pairs, expected_positive)

negative = {x["control"]: x for x in queue["rejectedDiscoverySignals"]}
assert "rarity-alone" in negative
assert negative["rarity-alone"]["example"]["themeId"] == "abondance"
assert "lexical-substring-without-second-canonical-theme" in negative
assembly = negative["lexical-substring-without-second-canonical-theme"]["example"]
assert assembly["existingTheme"]["themeId"] == "sainte-assemblee"
assert not assembly["genericRuntimeAlias"] or "sainte-assemblee" not in assembly["genericRuntimeAlias"].get("themeIds", [])

assert queue["stats"]["candidateCount"] == len(queue["candidates"])
assert queue["stats"]["positiveControlCount"] == len(expected_positive)
assert queue["stats"]["rejectedNegativeControlCount"] == 2

print(
    f"Candidate boundary audit OK: {len(ids)} review questions; "
    f"{len(expected_positive)} validated positive controls; 2 negative controls; no semantic promotion"
)
