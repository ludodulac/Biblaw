#!/usr/bin/env python3
"""Audit deterministic rebuild and source traceability of the semantic graph."""
from __future__ import annotations

import hashlib
import json

from build_theme_semantic_graph import TARGET, build_payload, render


def main() -> None:
    first = build_payload()
    second = build_payload()
    first_bytes = render(first).encode("utf-8")
    second_bytes = render(second).encode("utf-8")

    if first_bytes != second_bytes:
        raise SystemExit("Semantic graph generator is not deterministic across two fresh builds")
    if first.get("contradictions"):
        raise SystemExit(
            "Explicit semantic review sources contain contradictions: "
            + json.dumps(first["contradictions"], ensure_ascii=False)
        )
    for edge in first.get("edges") or []:
        source = edge.get("source") or {}
        if not source.get("file") or not source.get("recordType") or source.get("relationId") != edge.get("id"):
            raise SystemExit(f"Untraceable generated edge: {edge!r}")
    if not TARGET.exists():
        raise SystemExit(f"Missing generated graph: {TARGET}")
    committed = TARGET.read_bytes()
    if committed != first_bytes:
        raise SystemExit(
            "Committed graph differs from a fresh deterministic rebuild. "
            "Run: python scripts/build_theme_semantic_graph.py --write"
        )

    print(json.dumps({
        "schemaVersion": 1,
        "recordType": "theme-semantic-graph-audit",
        "status": "ok",
        "semanticClaim": False,
        "publicSearchEffect": False,
        "twoFreshBuildsByteIdentical": True,
        "committedGraphByteIdenticalToFreshBuild": True,
        "allEdgesTraceable": True,
        "contradictionCount": 0,
        "sha256": hashlib.sha256(first_bytes).hexdigest(),
        **first["coverage"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
