#!/usr/bin/env python3
"""Validate the derived theme co-occurrence graph without semantic interpretation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
CONNECTIONS = ROOT / "data/thematic-index/theme-connections.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


directory = load(DIRECTORY)
connections = load(CONNECTIONS)
errors = []
canonical = {t.get("id") for t in directory.get("themes", []) if t.get("id")}
records = {t.get("themeId"): t for t in connections.get("themes", []) if t.get("themeId")}

if connections.get("relationshipType") != "psalm-cooccurrence":
    errors.append("relationshipType must be psalm-cooccurrence")
if connections.get("semanticClaim") is not False:
    errors.append("semanticClaim must be false")
if connections.get("themeCount") != len(canonical):
    errors.append(f"themeCount mismatch: {connections.get('themeCount')} != {len(canonical)}")
if set(records) != canonical:
    missing = sorted(canonical - set(records))
    extra = sorted(set(records) - canonical)
    if missing:
        errors.append(f"missing themes in graph: {missing[:20]}")
    if extra:
        errors.append(f"unknown themes in graph: {extra[:20]}")

for tid, record in records.items():
    seen = set()
    last_key = None
    for link in record.get("topConnections", []):
        other = link.get("themeId")
        if other == tid:
            errors.append(f"self-link for {tid}")
        if other not in canonical:
            errors.append(f"unknown neighbor {other} from {tid}")
        if other in seen:
            errors.append(f"duplicate neighbor {other} from {tid}")
        seen.add(other)
        if link.get("sharedPsalmCount", 0) < 1 or link.get("score", 0) < 1:
            errors.append(f"non-positive connection {tid} -> {other}")
        for psalm in link.get("topSharedPsalms", []):
            if psalm.get("contribution", 0) < 1:
                errors.append(f"non-positive contribution {tid} -> {other}")
        key = (-link.get("score", 0), -link.get("sharedPsalmCount", 0), (link.get("label") or "").casefold(), other or "")
        if last_key is not None and key < last_key:
            errors.append(f"connection order is unstable for {tid}")
            break
        last_key = key

print(json.dumps({
    "status": "passed" if not errors else "failed",
    "themeCount": len(canonical),
    "undirectedEdgeCount": connections.get("undirectedEdgeCount"),
    "errors": errors,
}, ensure_ascii=False, indent=2))
if errors:
    sys.exit(1)
