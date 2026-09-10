#!/usr/bin/env python3
"""Build a conservative queue of conceptual-adjudication questions.

A candidate is NOT a semantic relation, confidence score, merge proposal, alias, or search rule.
It is only a prioritized question for human/corpus review. Discovery heuristics may decide what
is worth looking at; they never decide SAME / VARIANT / MORE GENERAL / MORE SPECIFIC /
COMPONENT / RELATED / NONE.
"""
from __future__ import annotations

import itertools
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
DIRECTORY = INDEX / "theme-directory.json"
RUNTIME = INDEX / "theme-search-runtime.json"
VALIDATED = INDEX / "theme-relations-validated.json"
OUT = INDEX / "conceptual-adjudication-candidates.json"

IMPORTANCE_RANK = {"central": 0, "important": 1, "related": 2}
ALLOWED_DECISIONS = [
    "same_or_equivalent",
    "variant",
    "more_general_or_more_specific",
    "component",
    "related",
    "no_relation",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    text = text.replace("œ", "oe").replace("æ", "ae")
    text = re.sub(r"[’'`´]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def tokens(value: object) -> tuple[str, ...]:
    return tuple(norm(value).split())


def representative_occurrences(theme: dict, limit: int = 3) -> list[dict]:
    values = sorted(
        theme.get("occurrences", []),
        key=lambda o: (
            IMPORTANCE_RANK.get(o.get("importance"), 9),
            -(o.get("score") or 0),
            o.get("bookNumber", 9999),
            o.get("psalmNumber", 9999),
            o.get("recordId", ""),
        ),
    )[:limit]
    return [
        {
            "recordId": o.get("recordId"),
            "bookNumber": o.get("bookNumber"),
            "bookTitle": o.get("bookTitle"),
            "archangel": o.get("archangel"),
            "psalmNumber": o.get("psalmNumber"),
            "psalmTitle": o.get("psalmTitle"),
            "importance": o.get("importance"),
            "directness": o.get("directness"),
            "verseNumbers": o.get("verseNumbers", []),
            "teaching": o.get("teaching"),
        }
        for o in values
    ]


def theme_summary(theme: dict) -> dict:
    return {
        "themeId": theme.get("id"),
        "label": theme.get("label"),
        "occurrenceCount": theme.get("occurrenceCount", len(theme.get("occurrences", []))),
        "centralPsalmCount": theme.get("centralPsalmCount", 0),
        "representativeOccurrences": representative_occurrences(theme),
    }


def corpus_contrast(a: dict, b: dict) -> dict:
    a_ids = {o.get("recordId") for o in a.get("occurrences", []) if o.get("recordId")}
    b_ids = {o.get("recordId") for o in b.get("occurrences", []) if o.get("recordId")}
    shared = sorted(a_ids & b_ids)
    a_only = sorted(a_ids - b_ids)
    b_only = sorted(b_ids - a_ids)
    return {
        "sharedPsalmCount": len(shared),
        "sharedRecordIdsSample": shared[:8],
        "firstThemeOnlyPsalmCount": len(a_only),
        "firstThemeOnlyRecordIdsSample": a_only[:8],
        "secondThemeOnlyPsalmCount": len(b_only),
        "secondThemeOnlyRecordIdsSample": b_only[:8],
        "interpretationRule": "distribution differences are review evidence only; they do not determine a semantic relation",
    }


def pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def lexical_reason(a: dict, b: dict) -> dict | None:
    """Return a review-priority signal only; never a semantic interpretation."""
    la, lb = norm(a.get("label")), norm(b.get("label"))
    ta, tb = tokens(a.get("label")), tokens(b.get("label"))
    if not la or not lb or la == lb:
        return None
    compact_a, compact_b = la.replace(" ", ""), lb.replace(" ", "")
    if compact_a + "s" == compact_b or compact_b + "s" == compact_a:
        return {
            "kind": "surface-number-nearness",
            "detail": "labels differ only by a simple trailing-s surface form; corpus review required",
            "priority": 55,
        }
    sa, sb = set(ta), set(tb)
    if sa and sb and (sa < sb or sb < sa):
        shorter, longer = (ta, tb) if len(ta) < len(tb) else (tb, ta)
        if len(shorter) <= 2 and len(longer) <= 5:
            return {
                "kind": "existing-theme-token-containment",
                "detail": "one existing theme label is lexically contained in another existing theme label; this does not imply hierarchy or componenthood",
                "priority": 45,
            }
    return None


def candidate_record(a: dict, b: dict, priority: int, signals: list[dict], instruction: str, prompts: list[str], calibration: dict | None = None) -> dict:
    key = pair_key(a["id"], b["id"])
    record = {
        "candidateId": f"review--{key[0]}--{key[1]}",
        "status": "question-only",
        "priority": priority,
        "discoverySignals": signals,
        "themes": [theme_summary(a), theme_summary(b)],
        "corpusContrast": corpus_contrast(a, b),
        "adjudicationQuestion": {
            "allowedOutcomes": ALLOWED_DECISIONS,
            "instruction": instruction,
        },
        "counterEvidencePrompts": prompts,
    }
    if calibration is not None:
        record["calibration"] = calibration
    return record


def main() -> None:
    directory = load(DIRECTORY)
    runtime = load(RUNTIME)
    validated = load(VALIDATED)
    themes = directory.get("themes", [])
    by_id = {t["id"]: t for t in themes}
    candidates = []
    seen = set()

    for rel in sorted(validated.get("relations", []), key=lambda r: r["id"]):
        a_id, b_id = rel["sourceThemeId"], rel["targetThemeId"]
        if a_id not in by_id or b_id not in by_id:
            continue
        key = pair_key(a_id, b_id)
        seen.add(key)
        candidates.append(candidate_record(
            by_id[a_id], by_id[b_id], 100,
            [{"kind": "validated-relation-positive-control", "detail": "pair is already human-approved and is included only to calibrate candidate discoverability"}],
            "Re-read both corpus contexts before deciding; discovery signals are not semantic evidence.",
            [
                "Do the two themes remain independently meaningful in their own Psalm contexts?",
                "Would replacing one label by the other alter the teaching of any cited passage?",
                "Does the whole/part or general/specific reading hold across the cited contexts rather than from the label alone?",
            ],
            {
                "knownValidatedRelationId": rel["id"],
                "knownValidatedRelationType": rel["relationType"],
                "mustNotBeReinferred": True,
            },
        ))

    for alias, record in sorted(runtime.get("aliases", {}).items()):
        ids = [x for x in record.get("themeIds", []) if x in by_id]
        if not record.get("ambiguous") or len(ids) < 2:
            continue
        for a_id, b_id in itertools.combinations(sorted(ids), 2):
            key = pair_key(a_id, b_id)
            if key in seen:
                continue
            seen.add(key)
            candidates.append(candidate_record(
                by_id[a_id], by_id[b_id], 90,
                [{"kind": "explicit-search-ambiguity", "detail": f"runtime alias {alias!r} maps to both existing theme ids"}],
                "Determine from corpus contexts whether the ids are equivalent, variants, hierarchical, compositional, related, or correctly distinct.",
                [
                    "Do representative passages assign different roles, objects, domains or consequences to the two themes?",
                    "Is the shared wording merely contextual or lexical rather than conceptual?",
                    "Would merging the ids incorrectly add Psalms from one meaning to the other?",
                ],
            ))

    lexical = []
    for a, b in itertools.combinations(themes, 2):
        key = pair_key(a["id"], b["id"])
        if key in seen:
            continue
        signal = lexical_reason(a, b)
        if not signal:
            continue
        volume = min(a.get("occurrenceCount", 0), 20) + min(b.get("occurrenceCount", 0), 20)
        lexical.append((-(signal["priority"]), -volume, key, a, b, signal))

    for _, _, key, a, b, signal in sorted(lexical)[:24]:
        seen.add(key)
        candidates.append(candidate_record(
            a, b, signal["priority"], [signal],
            "Lexical proximity only selected this pair for reading; it provides zero semantic conclusion.",
            [
                "Do the supporting passages teach materially different things despite similar labels?",
                "Is one label a qualified state or domain rather than a synonym?",
                "Is apparent inclusion just wording, with no corpus evidence for hierarchy or componenthood?",
            ],
        ))

    candidates.sort(key=lambda c: (-c["priority"], c["candidateId"]))

    abundance = by_id.get("abondance")
    sacred_assembly = by_id.get("sainte-assemblee")
    assembly_alias = runtime.get("aliases", {}).get("assemblee")
    rejected = [
        {
            "control": "rarity-alone",
            "example": theme_summary(abundance) if abundance else {"themeId": "abondance", "missing": True},
            "rejectedSignal": "singleton/rare occurrence count",
            "reason": "rarity alone identifies no second concept and provides no semantic evidence for merging, aliasing or relation creation",
        },
        {
            "control": "lexical-substring-without-second-canonical-theme",
            "example": {
                "existingTheme": theme_summary(sacred_assembly) if sacred_assembly else {"themeId": "sainte-assemblee", "missing": True},
                "genericSearchForm": "assemblee",
                "genericRuntimeAlias": assembly_alias,
            },
            "rejectedSignal": "the word 'assemblée' occurs inside the label 'Sainte Assemblée'",
            "reason": "a substring must not invent a missing generic canonical concept or redirect the generic query to the specific theme",
        },
    ]

    report = {
        "schemaVersion": 1,
        "recordType": "conceptual-adjudication-candidate-queue",
        "status": "review-questions-only",
        "generated": True,
        "generatedFrom": [
            "data/thematic-index/theme-directory.json",
            "data/thematic-index/theme-search-runtime.json",
            "data/thematic-index/theme-relations-validated.json",
        ],
        "semanticClaim": False,
        "requiresHumanCorpusReview": True,
        "publicSearchEffect": False,
        "candidateMeaning": "prioritized question for corpus review; never a weak/probable semantic relation",
        "allowedFinalAdjudications": ALLOWED_DECISIONS,
        "policy": {
            "automaticMergeAllowed": False,
            "automaticRenameAllowed": False,
            "automaticAliasAllowed": False,
            "automaticRelationCreationAllowed": False,
            "rarityIsSemanticEvidence": False,
            "lexicalContainmentIsSemanticEvidence": False,
            "cooccurrenceIsSemanticEvidence": False,
            "discoveryPriorityIsSemanticConfidence": False,
        },
        "stats": {
            "candidateCount": len(candidates),
            "positiveControlCount": sum(any(s["kind"] == "validated-relation-positive-control" for s in c["discoverySignals"]) for c in candidates),
            "explicitAmbiguityCandidateCount": sum(any(s["kind"] == "explicit-search-ambiguity" for s in c["discoverySignals"]) for c in candidates),
            "lexicalReviewCandidateCount": sum(any(s["kind"] in {"surface-number-nearness", "existing-theme-token-containment"} for s in c["discoverySignals"]) for c in candidates),
            "rejectedNegativeControlCount": len(rejected),
        },
        "candidates": candidates,
        "rejectedDiscoverySignals": rejected,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Conceptual adjudication queue: {len(candidates)} questions; "
        f"{report['stats']['positiveControlCount']} positive controls; "
        f"{report['stats']['explicitAmbiguityCandidateCount']} runtime ambiguities; "
        f"{report['stats']['lexicalReviewCandidateCount']} lexical review questions; "
        f"{len(rejected)} negative controls"
    )


if __name__ == "__main__":
    main()
