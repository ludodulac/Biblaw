#!/usr/bin/env python3
"""Applique de manière idempotente l'enrichissement éditorial du livre 22 de Gabriel.

À exécuter APRÈS finalize_book22_semantic.py. Les 470 relations historiques
restent identiques ; les 206 nouvelles relations sont conservées avec leur
provenance verset par verset (corpus JSON déjà extrait, sans relecture PDF).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-22.json"
BASELINE = INDEX / "audits/book22-original-relations.json"
PARTS = [
    INDEX / "audits/book22-enrichment-relations-part1.json",
    INDEX / "audits/book22-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-22"
NUMBERS = set(range(138, 164))
HISTORICAL = 470
ADDED = 206
VERSES = 884


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(BOOK_PATH)
    baseline = load(BASELINE)
    additions = [load(p) for p in PARTS]
    assert book["book"]["number"] == baseline["book"] == 22
    assert book["book"]["archangel"] == baseline["archangel"] == "gabriel"
    assert baseline["originalRelationCount"] == HISTORICAL
    assert set(map(int, baseline["psalms"])) == NUMBERS
    assert all(p["book"] == 22 and p["archangel"] == "gabriel" for p in additions)
    union = {}
    for part in additions:
        for n, themes in part["psalms"].items():
            assert n not in union, (n, "part overlap")
            union[n] = themes
    assert set(map(int, union)) == NUMBERS
    assert sum(map(len, union.values())) == ADDED

    canonical = {
        item["themeId"]: item["canonicalLabel"]
        for item in load(INDEX / "theme-search-index.json")["themes"]
    }
    analyses = book["psalmAnalyses"]
    assert len(analyses) == len(NUMBERS) and {p["number"] for p in analyses} == NUMBERS
    old_count = new_count = verse_count = 0
    nonstandard = []
    for psalm in analyses:
        n = psalm["number"]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"] and source["title"] == psalm["title"]
        assert source["archangel"] == "gabriel"
        nums = [v["number"] for v in source["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        verse_count += len(nums)
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate relation")
        for tid, frozen in baseline["psalms"][str(n)].items():
            assert existing.get(tid) == frozen, (n, tid, "historical relation modified")
            assert set(frozen["verseNumbers"]) <= valid, (n, tid)
            old_count += 1
        for tid, new in union[str(n)].items():
            assert new["themeId"] == tid and new["label"] == canonical[tid], (n, tid)
            refs = new["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid)
            assert new["teaching"].startswith("La Bible essénienne enseigne que ")
            assert len(new["teaching"]) >= 75, (n, tid, "explanation too short")
            assert tid not in baseline["psalms"][str(n)], (n, tid, "historic collision")
            if tid in existing:
                assert existing[tid] == new, (n, tid, "conflicting enrichment")
            else:
                psalm["themes"].append(new)
                existing[tid] = new
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (old_count, new_count, verse_count)
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Références vérifiées dans le corpus JSON préexistant issu du PDF. "
        "Pas de nouvelle comparaison indépendante avec le PDF original ; "
        "les affirmations spirituelles restent décrites comme enseignements du corpus."
    )
    audit = {
        "scope": "book-22-psalms-138-163",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-22/psalm-138.json through psalm-163.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "sourceTextLimitations": [
            "Psaume 155, verset 21 : fin tronquée dans le corpus JSON extrait "
            "(se termine par « après la »). Aucune nouvelle relation ne s'appuie "
            "sur ce verset ; relecture PDF indépendante encore nécessaire."
        ],
    }
    method["themeCoverageAudits"] = [
        x for x in method.get("themeCoverageAudits", [])
        if x.get("scope") != audit["scope"]
    ] + [audit]
    out = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != out:
        BOOK_PATH.write_text(out, encoding="utf-8")
    print(f"BOOK22 ENRICHMENT OK: {len(analyses)} psalms, {VERSES} verses, "
          f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total")


if __name__ == "__main__":
    main()
