#!/usr/bin/env python3
"""Applique sans altération l'enrichissement thématique de Ouriel, livre 24.

Les 312 relations de référence sont figées à l'identique. 205 nouvelles
relations documentaires sont ajoutées et justifiées par des numéros de
versets des JSON déjà extraits du PDF. Aucune relecture indépendante du
PDF original n'est impliquée.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-24.json"
BASELINE = INDEX / "audits/book24-original-relations.json"
PARTS = [
    INDEX / "audits/book24-enrichment-relations-part1.json",
    INDEX / "audits/book24-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-24"
NUMBERS = set(range(130, 156))
HISTORICAL, ADDED, VERSES = 312, 205, 709


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    book = load(BOOK_PATH)
    frozen = load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 24
    assert book["book"]["archangel"] == frozen["archangel"] == "ouriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 24 and p["archangel"] == "ouriel" for p in parts)

    added = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate psalm in enrichment")
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
        assert source["archangel"] == "ouriel"
        numbers = [v["number"] for v in source["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "invalid verse sequence")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)

        original = frozen["psalms"][str(n)]
        new = added[str(n)]
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate relation")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical relation altered")
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "historical verses")
            old_count += 1
        for tid, rel in new.items():
            assert rel["themeId"] == tid and rel["label"] == canonical[tid], (n, tid)
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "verse refs")
            assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(rel["teaching"]) >= 75, (n, tid, "brief explanation")
            assert tid not in original, (n, tid, "historical collision")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "enrichment disagreement")
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
        "Contrôle des références dans les JSON issus de l'extraction du PDF ; "
        "pas de nouvelle comparaison indépendante avec le PDF original. "
        "Les affirmations spirituelles, de réincarnation ou de guérison sont des "
        "doctrines internes au corpus et non des faits extérieurs établis."
    )
    audit = {
        "scope": "book-24-psalms-130-155",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-24/psalm-130.json through psalm-155.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
    }
    method["themeCoverageAudits"] = [
        x for x in method.get("themeCoverageAudits", [])
        if x.get("scope") != audit["scope"]
    ] + [audit]
    out = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != out:
        BOOK_PATH.write_text(out, encoding="utf-8")
    print(
        f"BOOK24 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} verses, "
        f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
