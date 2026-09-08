#!/usr/bin/env python3
"""Report structural theme-relation candidates without making semantic claims.

This is a FAST, read-only diagnostic. It reads the generated thematic search index and
suggests only *candidate components* when the meaningful tokens of one theme label are
a strict subset of another theme label.

A candidate is never a validated relation, synonym, broader/narrower claim or merge.
Human review must use Psalm context, verse evidence and teachings before promotion.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index/theme-search-index.json"

# Connective/function words carry expression structure but are not useful as standalone
# conceptual components. Keep this intentionally small and deterministic.
STOPWORDS = {
    "a", "au", "aux", "avec", "dans", "de", "des", "du", "en", "et",
    "l", "la", "le", "les", "par", "pour", "sur", "un", "une",
}


def meaningful_tokens(record: dict) -> frozenset[str]:
    aliases = record.get("normalizedAliases") or []
    normalized = aliases[0] if aliases else ""
    return frozenset(token for token in normalized.split() if token not in STOPWORDS)


def build_candidates(records: list[dict], target_ids: set[str] | None = None) -> list[dict]:
    by_id = {record["themeId"]: record for record in records if record.get("themeId")}
    targets = [
        record for record in records
        if record.get("themeId") and (not target_ids or record["themeId"] in target_ids)
    ]
    output = []

    for target in targets:
        target_tokens = meaningful_tokens(target)
        if len(target_tokens) < 2:
            continue

        candidates = []
        for component in records:
            if component.get("themeId") == target.get("themeId"):
                continue
            component_tokens = meaningful_tokens(component)
            if not component_tokens or not component_tokens < target_tokens:
                continue
            candidates.append({
                "themeId": component["themeId"],
                "label": component.get("canonicalLabel"),
                "relationType": "component_candidate",
                "relationStatus": "relation_candidate",
                "semanticClaim": False,
                "requiresHumanValidation": True,
                "candidateBasis": "normalized-meaningful-token-subset",
                "sharedTokens": sorted(component_tokens),
                "targetOccurrenceCount": target.get("occurrenceCount", 0),
                "componentOccurrenceCount": component.get("occurrenceCount", 0),
            })

        if candidates:
            candidates.sort(
                key=lambda item: (
                    -len(item["sharedTokens"]),
                    -item["componentOccurrenceCount"],
                    item["themeId"],
                )
            )
            output.append({
                "themeId": target["themeId"],
                "label": target.get("canonicalLabel"),
                "occurrenceCount": target.get("occurrenceCount", 0),
                "candidates": candidates,
            })

    missing = sorted((target_ids or set()) - set(by_id))
    if missing:
        raise SystemExit(f"Unknown theme id(s): {', '.join(missing)}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report structural relation candidates; never validates semantic relations."
    )
    parser.add_argument(
        "--theme",
        action="append",
        dest="themes",
        help="Theme id to inspect; repeat for several. Omit to inspect all composite themes.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum target themes printed when --theme is omitted (default: 20).",
    )
    args = parser.parse_args()

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    assert data.get("semanticMerging") is False, "candidate audit requires the non-merging search index"
    records = data.get("themes", [])
    target_ids = set(args.themes) if args.themes else None
    report = build_candidates(records, target_ids)

    if target_ids is None:
        report.sort(key=lambda item: (-len(item["candidates"]), item["themeId"]))
        report = report[: max(args.limit, 0)]

    payload = {
        "schemaVersion": 1,
        "recordType": "theme-relation-candidate-report",
        "generatedFrom": "data/thematic-index/theme-search-index.json",
        "semanticClaim": False,
        "validationPolicy": (
            "Candidates are structural prompts for review only. Validate against Psalm context, "
            "verse evidence and teachings before recording any semantic relation."
        ),
        "targets": report,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
