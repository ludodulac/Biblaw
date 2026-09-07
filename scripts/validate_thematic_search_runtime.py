#!/usr/bin/env python3
"""Validate the compact thematic browser runtime against its canonical generated sources.

The runtime is only a projection for browser lookup/navigation. It must not create theme identity,
resolve ambiguity, or turn co-occurrence into a semantic relation. Validation therefore compares
its aliases and neighbors exactly with projections of the already-validated search index and
co-occurrence graph.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "data/thematic-index/theme-search-index.json"
CONNECTIONS = ROOT / "data/thematic-index/theme-connections.json"
RUNTIME = ROOT / "data/thematic-index/theme-search-runtime.json"
TOP_NEIGHBORS = 8


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def expected_projection(search: dict, connections: dict) -> tuple[dict, dict]:
    aliases = {
        item["queryKey"]: {
            "themeIds": item.get("themeIds", []),
            "ambiguous": bool(item.get("ambiguous")),
        }
        for item in search.get("aliases", [])
    }
    neighbors = {}
    for item in connections.get("themes", []):
        tid = item.get("themeId")
        if not tid:
            continue
        neighbors[tid] = [
            {
                "themeId": link.get("themeId"),
                "label": link.get("label"),
                "score": link.get("score", 0),
                "sharedPsalmCount": link.get("sharedPsalmCount", 0),
            }
            for link in item.get("topConnections", [])[:TOP_NEIGHBORS]
        ]
    return aliases, neighbors


def validate(path: Path = RUNTIME) -> list[str]:
    search = load(SEARCH)
    connections = load(CONNECTIONS)
    runtime = load(path)
    errors: list[str] = []

    if search.get("semanticMerging") is not False:
        errors.append("search source must keep semanticMerging=false")
    if connections.get("relationshipType") != "psalm-cooccurrence":
        errors.append("connection source must remain psalm-cooccurrence")
    if connections.get("semanticClaim") is not False:
        errors.append("connection source must keep semanticClaim=false")

    expected_aliases, expected_neighbors = expected_projection(search, connections)
    theme_ids = {item.get("themeId") for item in search.get("themes", []) if item.get("themeId")}

    expected_scalars = {
        "schemaVersion": 1,
        "purpose": "browser-search-navigation",
        "semanticMerging": False,
        "connectionMeaning": "psalm-cooccurrence-only",
        "themeCount": len(theme_ids),
        "aliasCount": len(expected_aliases),
        "ambiguousAliasCount": sum(1 for item in expected_aliases.values() if item["ambiguous"]),
        "topNeighborsPerTheme": TOP_NEIGHBORS,
    }
    for key, expected in expected_scalars.items():
        if runtime.get(key) != expected:
            errors.append(f"{key}: expected {expected!r}, got {runtime.get(key)!r}")

    if runtime.get("aliases") != expected_aliases:
        errors.append("runtime aliases differ from validated search-index projection")
    if runtime.get("neighbors") != expected_neighbors:
        errors.append("runtime neighbors differ from validated co-occurrence projection")

    for query_key, item in (runtime.get("aliases") or {}).items():
        ids = item.get("themeIds") or []
        if any(tid not in theme_ids for tid in ids):
            errors.append(f"alias {query_key!r} references noncanonical theme id")
        if bool(item.get("ambiguous")) != (len(ids) > 1):
            errors.append(f"alias {query_key!r} ambiguity flag does not match its themeIds")

    for source_id, links in (runtime.get("neighbors") or {}).items():
        if source_id not in theme_ids:
            errors.append(f"neighbors contain noncanonical source theme {source_id}")
        if len(links) > TOP_NEIGHBORS:
            errors.append(f"theme {source_id} exceeds {TOP_NEIGHBORS} runtime neighbors")
        for link in links:
            if link.get("themeId") not in theme_ids:
                errors.append(f"theme {source_id} links to noncanonical theme {link.get('themeId')}")

    return errors


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else RUNTIME
    errors = validate(path)
    runtime = load(path)
    report = {
        "status": "failed" if errors else "passed",
        "themeCount": runtime.get("themeCount"),
        "aliasCount": runtime.get("aliasCount"),
        "ambiguousAliasCount": runtime.get("ambiguousAliasCount"),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
