#!/usr/bin/env python3
"""Enrichissement idempotent du livre 29 — « La religion du 21ème siècle » (Michaël).

Préserve strictement les 327 associations historiques et ajoute 191 liens
éditoriaux vers des versets existants. Corpus de référence : JSON déjà issu
de l'extraction PDF, et non nouvelle relecture indépendante du PDF papier.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-29"
BOOK_PATH = INDEX / "books/book-29.json"
BASELINE = INDEX / "audits/book29-original-relations.json"
PARTS = [
    INDEX / "audits/book29-enrichment-relations-part1.json",
    INDEX / "audits/book29-enrichment-relations-part2.json",
]
NUMBERS = set(range(191, 218))
HISTORICAL, ADDED, VERSES = 327, 191, 935

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book, frozen = load(BOOK_PATH), load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 29
    assert book["book"]["archangel"] == frozen["archangel"] == "michael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 29 and p["archangel"] == "michael" for p in parts)
    added = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate enrichment part")
            added[n] = themes
    assert set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED
    canonical = {
        theme["themeId"]: theme["canonicalLabel"]
        for theme in load(INDEX / "theme-search-index.json")["themes"]
    }
    analyses = book["psalmAnalyses"]
    assert len(analyses) == 27 and {a["number"] for a in analyses} == NUMBERS
    old_count = new_count = verse_count = 0
    nonstandard = []
    for analysis in analyses:
        n = analysis["number"]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == analysis["recordId"]
        assert source["title"] == analysis["title"]
        assert source["archangel"] == "michael"
        numbers = [v["number"] for v in source["verses"]]
        assert numbers and numbers == sorted(set(numbers))
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)
        original, additions = frozen["psalms"][str(n)], added[str(n)]
        existing = {r["themeId"]: r for r in analysis["themes"]}
        assert len(existing) == len(analysis["themes"]), (n, "duplicate themes")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical relation changed")
            assert set(rel["verseNumbers"]) <= valid
            old_count += 1
        for tid, rel in additions.items():
            assert tid not in original, (n, tid, "historical collision")
            assert rel["themeId"] == tid and rel["label"] == canonical[tid]
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid)
            assert rel["teaching"].startswith("La Bible essénienne enseigne que ")
            assert len(rel["teaching"]) >= 75, (n, tid, "too short")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "new theme changed")
            else:
                analysis["themes"].append(rel)
                existing[tid] = rel
            new_count += 1
    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES)
    assert not nonstandard, nonstandard
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Liens descriptifs vérifiés sur le corpus JSON extrait du PDF ; "
        "aucune nouvelle comparaison intégrale indépendante avec le PDF original. "
        "Les énoncés spirituels et magiques sont rapportés comme doctrine de ce texte, "
        "sans validation factuelle ou scientifique extérieure. "
        "Cette indexation ne prétend pas épuiser les interprétations possibles."
    )
    audit = {
        "scope": "book-29-psalms-191-217",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-29/psalm-191.json through psalm-217.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Les citations ont été contrôlées dans les JSON déjà extraits du PDF, "
            "sans nouvelle relecture indépendante du PDF original.",
            "Les enseignements sont classés comme représentations doctrinales du corpus, "
            "et non comme faits médicalement ou scientifiquement démontrés.",
            "Des espacements insolites subsistent dans certains titres extraits, "
            "comme « D ieu » et « A nge » ; les originaux n'ont pas été corrigés."
        ],
    }
    method["themeCoverageAudits"] = [
        x for x in method.get("themeCoverageAudits", [])
        if x.get("scope") != audit["scope"]
    ] + [audit]
    out = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != out:
        BOOK_PATH.write_text(out, encoding="utf-8")
    print(f"BOOK29 ENRICHMENT OK: 27 psalms, {VERSES} extracted verses, "
          f"{HISTORICAL} historical + {ADDED} new = {HISTORICAL + ADDED}")

if __name__ == "__main__":
    main()
