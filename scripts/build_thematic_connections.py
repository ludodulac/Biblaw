#!/usr/bin/env python3
"""Build neutral theme-to-theme connections from shared indexed Psalms.

A connection means only that two editorial themes co-occur in one or more Psalms. It does not assert
synonymy, causality, doctrinal equivalence or a privileged interpretation.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
OUT = ROOT / "data/thematic-index/theme-connections.json"
WEIGHT = {"central": 3, "important": 2, "related": 1}
TOP_NEIGHBORS = 30
TOP_SHARED_PSALMS = 8


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


directory = load(DIRECTORY)
meta = {t["id"]: {"label": t.get("label"), "score": t.get("score", 0)} for t in directory.get("themes", [])}
edges = {}

for path in sorted(BOOKS.glob("book-*.json")):
    data = load(path)
    book = data.get("book", {})
    archangel = book.get("archangel")
    for psalm in data.get("psalmAnalyses", []):
        # Keep at most one relation per theme id in a Psalm, preferring strongest importance.
        rels = {}
        for rel in psalm.get("themes", []):
            tid = rel.get("themeId")
            if not tid:
                continue
            score = WEIGHT.get(rel.get("importance", "related"), 1)
            if tid not in rels or score > rels[tid]["weight"]:
                rels[tid] = {"weight": score, "importance": rel.get("importance", "related")}
        for a, b in combinations(sorted(rels), 2):
            key = (a, b)
            edge = edges.setdefault(key, {
                "themeA": a,
                "themeB": b,
                "score": 0,
                "sharedPsalmCount": 0,
                "archangels": Counter(),
                "sharedPsalms": [],
            })
            wa, wb = rels[a]["weight"], rels[b]["weight"]
            contribution = wa * wb
            edge["score"] += contribution
            edge["sharedPsalmCount"] += 1
            if archangel:
                edge["archangels"][archangel] += 1
            edge["sharedPsalms"].append({
                "recordId": psalm.get("recordId"),
                "bookNumber": book.get("number"),
                "bookTitle": book.get("title"),
                "archangel": archangel,
                "psalmNumber": psalm.get("number"),
                "psalmTitle": psalm.get("title"),
                "themeAImportance": rels[a]["importance"],
                "themeBImportance": rels[b]["importance"],
                "contribution": contribution,
            })

neighbors = defaultdict(list)
for (a, b), edge in edges.items():
    shared = sorted(edge["sharedPsalms"], key=lambda x: (-x["contribution"], x.get("bookNumber") or 9999, x.get("psalmNumber") or 9999))
    compact = {
        "score": edge["score"],
        "sharedPsalmCount": edge["sharedPsalmCount"],
        "archangels": [{"id": aid, "sharedPsalmCount": count} for aid, count in sorted(edge["archangels"].items(), key=lambda kv: (-kv[1], kv[0]))],
        "topSharedPsalms": shared[:TOP_SHARED_PSALMS],
    }
    neighbors[a].append({"themeId": b, "label": meta.get(b, {}).get("label"), **compact})
    neighbors[b].append({"themeId": a, "label": meta.get(a, {}).get("label"), **compact})

records = []
for tid in sorted(meta):
    ranked = sorted(neighbors.get(tid, []), key=lambda x: (-x["score"], -x["sharedPsalmCount"], (x.get("label") or "").casefold(), x["themeId"]))
    records.append({
        "themeId": tid,
        "label": meta[tid].get("label"),
        "connectionCount": len(ranked),
        "topConnections": ranked[:TOP_NEIGHBORS],
    })

OUT.write_text(json.dumps({
    "schemaVersion": 1,
    "relationshipType": "psalm-cooccurrence",
    "semanticClaim": False,
    "description": "Themes are connected only because they co-occur in indexed Psalms; scores rank repeated/strong co-occurrence for navigation.",
    "scoring": {"central": 3, "important": 2, "related": 1, "pairContribution": "importanceWeightA * importanceWeightB"},
    "themeCount": len(records),
    "undirectedEdgeCount": len(edges),
    "topConnectionsPerTheme": TOP_NEIGHBORS,
    "themes": records,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Built neutral thematic connections: {len(records)} themes, {len(edges)} undirected co-occurrence edges")
