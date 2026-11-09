#!/usr/bin/env python3
"""Réapplique de façon déterministe les relations éditoriales du livre 19.

Le pipeline de génération reconstruit les analyses initiales de Raphaël : cette étape
doit donc être exécutée APRES finalize_book19_semantic.py. Aucune relation historique
n'est modifiée et les relations de l'enrichissement demeurent explicitement sourcées.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-19.json"
BASELINE_PATH = INDEX / "audits/book19-original-relations.json"
ADDITIONS_PATH = INDEX / "audits/book19-enrichment-relations.json"
CORPUS = ROOT / "data/corpus/books/book-19"
PSALMS = set(range(102, 128))
HISTORICAL = 401
ADDED = 292
VERSES = 817

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book = load(BOOK_PATH)
    baseline = load(BASELINE_PATH)
    additions = load(ADDITIONS_PATH)
    assert book["book"]["number"] == baseline["book"] == additions["book"] == 18
    assert book["book"]["archangel"] == baseline["archangel"] == additions["archangel"] == "raphael"
    assert baseline["originalRelationCount"] == HISTORICAL
    assert set(map(int, baseline["psalms"])) == PSALMS
    assert set(map(int, additions["psalms"])) == PSALMS

    old_count = new_count = verse_count = 0
    nonstandard = []
    psalms = book["psalmAnalyses"]
    assert len(psalms) == len(PSALMS) and {p["number"] for p in psalms} == PSALMS
    for psalm in psalms:
        n = psalm["number"]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"] and source["title"] == psalm["title"]
        assert source["archangel"] == "raphael"
        numbers = [verse["number"] for verse in source["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "numbering")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)

        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate original")
        for tid, frozen in baseline["psalms"][str(n)].items():
            assert existing.get(tid) == frozen, (n, tid, "historical relation changed")
            assert set(frozen["verseNumbers"]) <= valid
            old_count += 1

        for tid, relation in additions["psalms"][str(n)].items():
            assert relation["themeId"] == tid
            assert relation["verseNumbers"] and len(set(relation["verseNumbers"])) == len(relation["verseNumbers"])
            assert set(relation["verseNumbers"]) <= valid, (n, tid, "invalid verse reference")
            assert relation["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(relation["teaching"]) > 65, (n, tid)
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
        "Relations et explications ancrées dans les numéros de versets du corpus JSON préexistant ; "
        "elles n'épuisent pas les lectures possibles et ne constituent pas une vérification indépendante du PDF."
    )
    audit = {
        "scope": "book-19-psalms-102-127",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-19/psalm-102.json through psalm-127.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard
    }
    method["themeCoverageAudits"] = [
        item for item in method.get("themeCoverageAudits", [])
        if item.get("scope") != audit["scope"]
    ] + [audit]
    # Idempotence : ne pas réécrire lorsque le document final est déjà identique.
    updated = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != updated:
        BOOK_PATH.write_text(updated, encoding="utf-8")
    print(f"BOOK19 ENRICHMENT OK: {len(psalms)} psaumes, {VERSES} versets, "
          f"{HISTORICAL} relations historiques et {ADDED} nouvelles, "
          f"{HISTORICAL + ADDED} total")

if __name__ == "__main__":
    main()
