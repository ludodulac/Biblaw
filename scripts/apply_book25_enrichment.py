#!/usr/bin/env python3
"""Enrichissement idempotent du livre 25 de Michaël — Les clés de la maîtrise.

Le fichier de référence garantit les 312 associations historiques strictement
inchangées. Les 208 nouvelles relations sont reliées aux versets présents
dans le corpus JSON issu du PDF (sans relecture indépendante du PDF).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-25.json"
BASELINE = INDEX / "audits/book25-original-relations.json"
PARTS = [
    INDEX / "audits/book25-enrichment-relations-part1.json",
    INDEX / "audits/book25-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-25"
NUMBERS = set(range(165, 191))
HISTORICAL, ADDED, VERSES = 312, 208, 881


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    book = load(BOOK_PATH)
    frozen = load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 25
    assert book["book"]["archangel"] == frozen["archangel"] == "michael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 25 and p["archangel"] == "michael" for p in parts)

    added = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate psalm in additions")
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
        assert source["archangel"] == "michael"
        numbers = [v["number"] for v in source["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "invalid verse sequence")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)

        original, new = frozen["psalms"][str(n)], added[str(n)]
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate theme")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical relation changed")
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "invalid original verse")
            old_count += 1
        for tid, rel in new.items():
            assert rel["themeId"] == tid and rel["label"] == canonical[tid], (n, tid)
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "verse refs")
            assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(rel["teaching"]) >= 75, (n, tid, "brief teaching")
            assert tid not in original, (n, tid, "collision with historical association")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "conflicting enrichment")
            else:
                psalm["themes"].append(rel)
                existing[tid] = rel
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (
        old_count, new_count, verse_count
    )
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Numéros de versets contrôlés dans les JSON préexistants, issus de "
        "l'extraction du PDF. Pas de relecture indépendante intégrale du PDF. "
        "Les énoncés spirituels, les déclarations sur la mort ou les pratiques "
        "de guérison sont indexés comme doctrine du corpus, non comme faits démontrés."
    )
    audit = {
        "scope": "book-25-psalms-165-190",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-25/psalm-165.json through psalm-190.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Le titre du psaume 180 dans le corpus JSON est possiblement tronqué : "
            "« Réapproprie-toi ta pensée pour ». Il n'a pas été modifié. "
            "Vérification du titre contre le PDF original recommandée."
        ],
    }
    method["themeCoverageAudits"] = [
        x for x in method.get("themeCoverageAudits", [])
        if x.get("scope") != audit["scope"]
    ] + [audit]
    out = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != out:
        BOOK_PATH.write_text(out, encoding="utf-8")
    print(
        f"BOOK25 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} verses, "
        f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
