#!/usr/bin/env python3
"""Build a compact browser payload from validated thematic search/connection data.

The full editorial directory and full co-occurrence graph remain the auditable sources. This file
contains only lookup aliases and a small set of navigational neighbors for the web UI.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "data/thematic-index/theme-search-index.json"
CONNECTIONS = ROOT / "data/thematic-index/theme-connections.json"
OUT = ROOT / "data/thematic-index/theme-search-runtime.json"
TOP_NEIGHBORS = 8


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


search = load(SEARCH)
connections = load(CONNECTIONS)

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

payload = {
    "schemaVersion": 1,
    "purpose": "browser-search-navigation",
    "semanticMerging": False,
    "connectionMeaning": "psalm-cooccurrence-only",
    "themeCount": search.get("themeCount", 0),
    "aliasCount": len(aliases),
    "ambiguousAliasCount": sum(1 for item in aliases.values() if item["ambiguous"]),
    "topNeighborsPerTheme": TOP_NEIGHBORS,
    "aliases": aliases,
    "neighbors": neighbors,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
print(f"Built thematic browser runtime: {payload['themeCount']} themes, {payload['aliasCount']} aliases")
