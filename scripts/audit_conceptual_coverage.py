#!/usr/bin/env python3
"""Measure conceptual coverage signals without inferring semantic identity.

This audit answers a deliberately limited question: what does the current thematic
infrastructure *measure*, and which semantic situations remain unadjudicated?
It must never merge, rename, promote or relate themes automatically.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
OUT = INDEX / "conceptual-coverage-audit.json"


def load(name: str):
    return json.loads((INDEX / name).read_text(encoding="utf-8"))


def by_id(directory: dict) -> dict[str, dict]:
    return {theme["id"]: theme for theme in directory.get("themes", [])}


validation = load("validation-report.json")
quality = load("theme-quality-audit.json")
directory = load("theme-directory.json")
runtime = load("theme-search-runtime.json")
relations = load("theme-relations-validated.json")
themes = by_id(directory)

assert validation["status"] == "passed"
assert quality["status"] == "review-candidates-generated"
assert runtime["semanticMerging"] is False
assert runtime["connectionMeaning"] == "psalm-cooccurrence-only"
assert directory["themeCount"] == len(themes)

stats = quality["stats"]
assert stats["themeCount"] == directory["themeCount"] == runtime["themeCount"]
assert stats["themeRelationCount"] == validation["stats"]["themeRelations"]
assert stats["relationsWithoutVerseNumbers"] == 0
assert stats["relationsWithoutTeaching"] == 0

# Contrastive panel. These are observations and already-validated semantic facts only.
mort = themes["mort"]
abondance = themes["abondance"]
assert mort["occurrenceCount"] == 161
assert abondance["occurrenceCount"] == 1

validated = relations.get("relations", [])
validated_types = {}
for relation in validated:
    validated_types.setdefault(relation["relationType"], 0)
    validated_types[relation["relationType"]] += 1

corps_components = sorted(
    relation["sourceThemeId"]
    for relation in validated
    if relation["targetThemeId"] == "corps-ame-esprit" and relation["relationType"] == "component_of"
)
assert corps_components == ["ame", "corps", "esprit"]

alliance_light = runtime["aliases"].get("alliance de lumiere")
assert alliance_light and alliance_light["ambiguous"] is True
assert set(alliance_light["themeIds"]) == {"alliance", "alliance-de-lumiere"}
assert not any(
    {r["sourceThemeId"], r["targetThemeId"]} == {"alliance", "alliance-de-lumiere"}
    for r in validated
)

assembly = runtime["aliases"].get("assemblee")
sacred_assembly = runtime["aliases"].get("sainte assemblee")
assert not assembly or "sainte-assemblee" not in assembly.get("themeIds", [])
assert sacred_assembly and sacred_assembly.get("themeIds") == ["sainte-assemblee"]

report = {
    "schemaVersion": 1,
    "status": "measured-not-semantically-exhaustive",
    "purpose": "reproducible conceptual-coverage diagnosis; no automatic semantic inference",
    "sources": {
        "canonicalPsalmAnalyses": "data/thematic-index/books/book-*.json via validation-report.json",
        "generatedThemeDirectory": "data/thematic-index/theme-directory.json",
        "generatedQualityAudit": "data/thematic-index/theme-quality-audit.json",
        "searchRuntime": "data/thematic-index/theme-search-runtime.json",
        "validatedSemanticRelations": "data/thematic-index/theme-relations-validated.json",
    },
    "measurements": {
        "analyzedBooks": validation["stats"]["books"],
        "analyzedPsalms": validation["stats"]["psalmAnalyses"],
        "themePsalmRelations": validation["stats"]["themeRelations"],
        "indexedThemeIds": stats["themeCount"],
        "singletonThemeIds": stats["singletonThemeCount"],
        "rareThemeIdsOccurrenceLTE2": stats["rareThemeCountOccurrenceLTE2"],
        "contextualLabelVariationCandidates": stats["sameIdMultipleLabelsCount"],
        "explicitNormalizedLabelAmbiguities": stats["sameNormalizedLabelMultipleIdsCount"],
        "validatedCrossThemeRelations": len(validated),
        "validatedRelationTypes": validated_types,
    },
    "measurementMeaning": {
        "indexedThemeIds": "distinct themeId values observed in canonical Psalm analyses; not a proof of fully normalized concepts",
        "singletonThemeIds": "themeIds occurring in one Psalm; rarity alone is neither an error nor evidence for merging",
        "rareThemeIdsOccurrenceLTE2": "themeIds occurring in at most two Psalms; review signal only",
        "validatedCrossThemeRelations": "human-approved semantic relations; the only cross-id semantic claims counted here",
        "exhaustiveness": "Psalm-analysis coverage is measured; conceptual exhaustiveness is not currently proven",
    },
    "contrastivePanel": [
        {
            "case": "mort",
            "kind": "transversal",
            "observation": {"themeId": "mort", "indexedPsalms": mort["occurrenceCount"]},
            "diagnosis": "well represented as an indexed theme; this count does not prove all semantic formulations of death are captured",
        },
        {
            "case": "abondance",
            "kind": "rare-negative-control",
            "observation": {"themeId": "abondance", "indexedPsalms": abondance["occurrenceCount"]},
            "diagnosis": "singleton status alone creates no semantic defect and must not trigger consolidation",
        },
        {
            "case": "corps-ame-esprit",
            "kind": "composite-positive-control",
            "observation": {"validatedComponents": corps_components},
            "diagnosis": "component relations are accepted only because explicit corpus-grounded, human-approved relations exist",
        },
        {
            "case": "alliance-de-lumiere",
            "kind": "nearby-formulations-unresolved",
            "observation": {"searchAlias": "alliance de lumiere", "themeIds": sorted(alliance_light["themeIds"]), "ambiguous": True},
            "diagnosis": "lexical/contextual overlap is preserved as ambiguity because no validated cross-theme relation adjudicates these ids",
        },
        {
            "case": "sainte-assemblee",
            "kind": "lexical-containment-negative-control",
            "observation": {"specificAliasThemeIds": sacred_assembly["themeIds"], "genericAssemblyRedirectsToSpecific": False},
            "diagnosis": "the presence of 'assemblée' inside 'Sainte Assemblée' does not create a broader/equivalent relation automatically",
        },
    ],
    "genericDefectClasses": [
        "concept potentially absent from analyses",
        "one concept potentially split across multiple themeIds or labels",
        "missing lexical alias for an already-established concept",
        "unadjudicated broader/specific relation",
        "unadjudicated component relation",
        "mere cooccurrence or lexical proximity that must remain non-semantic",
        "no defect: rare or specific theme is legitimately distinct",
    ],
    "firstResponsibleGap": {
        "layer": "between canonical Psalm theme analysis and cross-theme concept mapping",
        "finding": "the repository can prove Psalm coverage and individual theme evidence, but most cross-theme semantic status is intentionally unknown; only explicitly validated relations may bridge distinct themeIds",
        "nextRuleToProve": "candidate generation may surface possible cross-id fragmentation, but equivalence/generalization/component/related status must be justified from corpus evidence and cannot be inferred from rarity, lexical containment or cooccurrence",
        "automaticMergeAllowed": False,
        "publicSearchChange": False,
    },
}

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report["measurements"], ensure_ascii=False, indent=2))
