#!/usr/bin/env python3
"""Réapplique l'enrichissement éditorial de Raphaël, livre 23 (psaumes 128-153).

À exécuter APRÈS finalize_books23_25_semantic.py. Le livre 23 conserve
333 relations historiques et reçoit 239 relations additionnelles, toutes
référencées aux versets du JSON extrait du PDF (sans relecture indépendante
de toutes les pages PDF).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-23.json"
BASELINE = INDEX / "audits/book23-original-relations.json"
PARTS = [
    INDEX / "audits/book23-enrichment-relations-part1.json",
    INDEX / "audits/book23-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-23"
NUMBERS = set(range(128, 154))
HISTORICAL = 333
ADDED = 239
VERSES = 866


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(BOOK_PATH)
    baseline = load(BASELINE)
    additions = [load(p) for p in PARTS]
    assert book["book"]["number"] == baseline["book"] == 23
    assert book["book"]["archangel"] == baseline["archangel"] == "raphael"
    assert baseline["originalRelationCount"] == HISTORICAL
    assert set(map(int, baseline["psalms"])) == NUMBERS
    assert all(p["book"] == 23 and p["archangel"] == "raphael" for p in additions)

    added = {}
    for part in additions:
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "psalm repeated across enrichment parts")
            added[n] = themes
    assert set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED

    canonical = {
        item["themeId"]: item["canonicalLabel"]
        for item in load(INDEX / "theme-search-index.json")["themes"]
    }
    psalms = book["psalmAnalyses"]
    assert len(psalms) == len(NUMBERS) and {p["number"] for p in psalms} == NUMBERS

    old_count = new_count = verse_count = 0
    nonstandard = []
    for psalm in psalms:
        n = psalm["number"]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"] and source["title"] == psalm["title"]
        assert source["archangel"] == "raphael"
        numbers = [v["number"] for v in source["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "verse numbering")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)

        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate original theme")
        for tid, original in baseline["psalms"][str(n)].items():
            assert existing.get(tid) == original, (n, tid, "historical relation altered")
            assert set(original["verseNumbers"]) <= valid, (n, tid)
            old_count += 1
        for tid, relation in added[str(n)].items():
            assert relation["themeId"] == tid and relation["label"] == canonical[tid], (n, tid)
            refs = relation["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid)
            assert relation["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(relation["teaching"]) >= 75, (n, tid)
            assert tid not in baseline["psalms"][str(n)], (n, tid, "historical collision")
            if tid in existing:
                assert existing[tid] == relation, (n, tid, "enrichment conflict")
            else:
                psalm["themes"].append(relation)
                existing[tid] = relation
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (old_count, new_count, verse_count)
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Liaisons documentaires vers les numéros de versets du corpus JSON existant, "
        "issu du PDF. Les affirmations religieuses, biologiques ou relatives à "
        "l'après-mort sont des doctrines du texte, pas des faits extérieurs établis. "
        "Aucune nouvelle comparaison exhaustive et indépendante au PDF original."
    )
    audit = {
        "scope": "book-23-psalms-128-153",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-23/psalm-128.json through psalm-153.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Psaume 128: le corpus existant utilise la renumérotation 1-34, "
            "provenant des numéros imprimés 49-82 (décalage 48), déjà auditée "
            "en amont et documentée dans method.numberingNote."
        ],
    }
    method["themeCoverageAudits"] = [
        item for item in method.get("themeCoverageAudits", [])
        if item.get("scope") != audit["scope"]
    ] + [audit]
    out = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != out:
        BOOK_PATH.write_text(out, encoding="utf-8")
    print(f"BOOK23 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} verses, "
          f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total")


if __name__ == "__main__":
    main()
