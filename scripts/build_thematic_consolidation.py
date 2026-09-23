#!/usr/bin/env python3
"""Build a deterministic, documentary-only thematic consolidation.

No semantic inference is performed here. The generator only orders and exposes
canonical thematic relations already present in data/thematic-index.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index/theme-search-index.json"
RUNTIME = ROOT / "data/thematic-index/theme-search-runtime.json"
BOOKS = ROOT / "data/thematic-index/books"
IMPORTANCE_RANK = {"central": 0, "important": 1, "related": 2}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def documentary_dossier(theme_id: str):
    rows = []
    for path in sorted(BOOKS.glob("book-*.json")):
        book = load_json(path)
        book_meta = book["book"]
        for psalm in book.get("psalmAnalyses", []):
            for relation in psalm.get("themes", []):
                if relation.get("themeId") != theme_id:
                    continue
                rows.append({
                    "themeId": theme_id,
                    "recordId": psalm["recordId"],
                    "book": {
                        "number": book_meta["number"],
                        "title": book_meta["title"],
                        "archangel": book_meta.get("archangel"),
                    },
                    "psalmNumber": psalm["number"],
                    "psalmTitle": psalm["title"],
                    "importance": relation["importance"],
                    "directness": relation.get("directness"),
                    "verseNumbers": relation.get("verseNumbers", []),
                    "teaching": relation.get("teaching"),
                    "provenance": {
                        "sourceFile": str(path.relative_to(ROOT)),
                        "recordId": psalm["recordId"],
                        "verseNumbers": relation.get("verseNumbers", []),
                        "notesUsed": psalm.get("notesUsed", []),
                    },
                })
    return rows

def evidence_key(row):
    return (
        IMPORTANCE_RANK.get(row["importance"], 99),
        -len(row["verseNumbers"]),
        row["recordId"],
    )

def theme_meta(theme_id: str):
    index = load_json(INDEX)
    hit = next((x for x in index["themes"] if x["themeId"] == theme_id), None)
    if not hit:
        return {"themeId": theme_id, "label": theme_id, "aliases": []}
    return {
        "themeId": theme_id,
        "label": hit["canonicalLabel"],
        "aliases": hit.get("normalizedAliases", []),
    }

def related_themes(theme_id: str):
    runtime = load_json(RUNTIME)
    return [
        {
            "themeId": x["themeId"],
            "label": x["label"],
            "score": x["score"],
            "sharedPsalmCount": x["sharedPsalmCount"],
            "relationType": "documentary-co-presence",
            "semanticEquivalence": False,
        }
        for x in runtime.get("neighbors", {}).get(theme_id, [])
    ]

def consolidate(theme_id: str, evidence_limit=12, essential_limit=10):
    dossier = documentary_dossier(theme_id)
    counts = {"central": 0, "important": 0, "related": 0}
    for row in dossier:
        if row["importance"] in counts:
            counts[row["importance"]] += 1

    ordered = sorted(dossier, key=evidence_key)
    principal = ordered[:evidence_limit]
    essentials = ordered[:essential_limit]

    def compact(row):
        return {
            "recordId": row["recordId"],
            "bookNumber": row["book"]["number"],
            "psalmNumber": row["psalmNumber"],
            "psalmTitle": row["psalmTitle"],
            "importance": row["importance"],
            "directness": row["directness"],
            "verseNumbers": row["verseNumbers"],
            "teaching": row["teaching"],
            "sourceRef": row["provenance"],
        }

    source_refs = []
    seen = set()
    for row in principal + essentials:
        key = (row["recordId"], tuple(row["verseNumbers"]))
        if key not in seen:
            seen.add(key)
            source_refs.append(row["provenance"])

    return {
        "schemaVersion": 1,
        "purpose": "experimental-documentary-thematic-consolidation",
        "theme": theme_meta(theme_id),
        "documentaryStats": {"totalRelations": len(dossier), **counts},
        "principalEvidence": [compact(x) for x in principal],
        "candidateEssentialPsalms": {
            "selectionRule": "importance central > important > related; then descending count of documented verseNumbers; then recordId ascending for deterministic tie-breaking",
            "editorialSelection": False,
            "items": [compact(x) for x in essentials],
        },
        "relatedThemes": related_themes(theme_id),
        "sourceRefs": source_refs,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("theme_id")
    p.add_argument("-o", "--output")
    args = p.parse_args()
    result = consolidate(args.theme_id)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
