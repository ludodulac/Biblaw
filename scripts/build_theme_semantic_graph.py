#!/usr/bin/env python3
"""Build the noncanonical semantic graph from explicit semantic review files only.

Deliberately dumb by design:
- no inference
- no semantic normalization
- no merging of themes or relation claims
- no lexical heuristics
- no public-search side effect

Every emitted edge is copied from one explicit review decision and keeps a source
file + relation id trace. The graph is generated deterministically so it can be
deleted and rebuilt byte-for-byte.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "data/thematic-index/reviews"
TARGET = REVIEWS / "theme-semantic-graph-prototype.json"

SOURCE_RECORD_TYPES = {
    "theme-semantic-case-study": "relationAssessments",
    "theme-semantic-boundary-review": "decisions",
}


def iter_source_files() -> list[Path]:
    sources: list[Path] = []
    for path in sorted(REVIEWS.glob("*.json")):
        if path == TARGET:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("recordType") in SOURCE_RECORD_TYPES:
            sources.append(path)
    return sources


def extract_relation(record_type: str, item: dict) -> tuple[str, str, str, str, dict]:
    relation_id = item.get("id")
    source = item.get("sourceThemeId")
    target = item.get("targetThemeId")
    relation_type = item.get("proposedRelationType")
    evidence = item.get("evidenceByThemeId") or {}
    if not all([relation_id, source, target, relation_type]):
        raise SystemExit(f"Malformed explicit semantic review relation: {item!r}")
    if set(evidence) != {source, target}:
        raise SystemExit(
            f"{relation_id}: evidence keys must exactly match explicit endpoints; "
            f"got {sorted(evidence)}, expected {sorted([source, target])}"
        )
    return relation_id, source, target, relation_type, evidence


def build_payload() -> dict:
    source_files = iter_source_files()
    edges: list[dict] = []
    node_records: dict[str, set[str]] = defaultdict(set)
    endpoint_types: dict[tuple[str, str], set[str]] = defaultdict(set)
    relation_ids: dict[str, list[dict]] = defaultdict(list)

    source_manifest: list[dict] = []
    for path in source_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        record_type = data["recordType"]
        collection_key = SOURCE_RECORD_TYPES[record_type]
        items = data.get(collection_key) or []
        source_manifest.append({
            "file": path.name,
            "recordType": record_type,
            "relationCount": len(items),
        })

        for item in items:
            relation_id, source, target, relation_type, evidence = extract_relation(record_type, item)
            edge = {
                "id": relation_id,
                "sourceThemeId": source,
                "targetThemeId": target,
                "proposedRelationType": relation_type,
                "source": {
                    "file": path.name,
                    "recordType": record_type,
                    "relationId": relation_id,
                },
                "semanticClaim": False,
            }
            edges.append(edge)
            endpoint_types[(source, target)].add(relation_type)
            relation_ids[relation_id].append(edge)
            for theme_id, refs in evidence.items():
                for ref in refs:
                    record_id = ref.get("recordId")
                    if not record_id:
                        raise SystemExit(f"{path.name}/{relation_id}: missing evidence recordId")
                    node_records[theme_id].add(record_id)

    contradictions: list[dict] = []
    for (source, target), relation_types in sorted(endpoint_types.items()):
        if len(relation_types) > 1:
            contradictions.append({
                "kind": "same-ordered-endpoints-multiple-types",
                "sourceThemeId": source,
                "targetThemeId": target,
                "proposedRelationTypes": sorted(relation_types),
            })
    for relation_id, claims in sorted(relation_ids.items()):
        signatures = {
            (c["sourceThemeId"], c["targetThemeId"], c["proposedRelationType"])
            for c in claims
        }
        if len(signatures) > 1:
            contradictions.append({
                "kind": "same-relation-id-multiple-claims",
                "relationId": relation_id,
                "claims": [
                    {"sourceThemeId": s, "targetThemeId": t, "proposedRelationType": r}
                    for s, t, r in sorted(signatures)
                ],
            })

    edges.sort(key=lambda e: (
        e["source"]["file"], e["id"], e["sourceThemeId"],
        e["targetThemeId"], e["proposedRelationType"],
    ))
    nodes = [
        {"themeId": theme_id, "evidenceRecordIds": sorted(record_ids)}
        for theme_id, record_ids in sorted(node_records.items())
    ]

    return {
        "schemaVersion": 1,
        "recordType": "theme-semantic-graph-prototype",
        "status": "generated-from-explicit-review-relations",
        "generated": True,
        "semanticClaim": False,
        "requiresHumanApproval": True,
        "publicSearchEffect": False,
        "generator": "scripts/build_theme_semantic_graph.py",
        "policy": {
            "reviewFilesAreOnlyRelationSources": True,
            "sourceRecordTypes": sorted(SOURCE_RECORD_TYPES),
            "inference": False,
            "themeMerging": False,
            "semanticNormalization": False,
            "lexicalHeuristics": False,
            "automaticRelationTyping": False,
            "automaticPromotion": False,
            "canonicalValidatedStore": "data/thematic-index/theme-relations-validated.json",
        },
        "sourceManifest": source_manifest,
        "nodes": nodes,
        "edges": edges,
        "contradictions": contradictions,
        "coverage": {
            "sourceFileCount": len(source_manifest),
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
            "proposedRelationTypes": sorted({e["proposedRelationType"] for e in edges}),
            "equivalentToPositiveCases": sum(e["proposedRelationType"] == "equivalent_to" for e in edges),
            "contradictionCount": len(contradictions),
        },
    }


def render(payload: dict) -> str:
    # Canonical generated bytes: sorted keys, compact separators, UTF-8 text, final newline.
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write the generated graph to its repository target.")
    mode.add_argument("--check", action="store_true", help="Fail unless the committed graph is byte-identical to a fresh rebuild.")
    args = parser.parse_args()

    payload = build_payload()
    if payload["contradictions"]:
        print(json.dumps({"status": "contradictions", "contradictions": payload["contradictions"]}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    rendered = render(payload)
    if args.write:
        TARGET.write_text(rendered, encoding="utf-8")
        print(f"wrote {TARGET.relative_to(ROOT)}")
        return
    if args.check:
        if not TARGET.exists():
            raise SystemExit(f"Missing generated graph: {TARGET.relative_to(ROOT)}")
        if TARGET.read_text(encoding="utf-8") != rendered:
            raise SystemExit(
                "Generated semantic graph is stale or non-reproducible. "
                "Run: python scripts/build_theme_semantic_graph.py --write"
            )
        print(json.dumps({"status": "ok", "byteIdenticalToFreshRebuild": True, **payload["coverage"]}, ensure_ascii=False, indent=2))
        return
    print(rendered, end="")


if __name__ == "__main__":
    main()
