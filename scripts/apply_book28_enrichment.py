#!/usr/bin/env python3
"""Enrichissement idempotent du livre 28, « Le vrai corps du Christ » (Ouriel).

Conserve les 312 relations thématiques préexistantes à l'identique ;
ajoute 207 relations étayées par les références des 835 versets présents
dans le corpus JSON issu du PDF. Ce n'est pas une nouvelle comparaison
indépendante avec le PDF original.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-28.json"
BASELINE = INDEX / "audits/book28-original-relations.json"
PARTS = [
    INDEX / "audits/book28-enrichment-relations-part1.json",
    INDEX / "audits/book28-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-28"
NUMBERS = set(range(156, 182))
HISTORICAL, ADDED, VERSES = 312, 207, 835


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    book, frozen = load(BOOK_PATH), load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 28
    assert book["book"]["archangel"] == frozen["archangel"] == "ouriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 28 and p["archangel"] == "ouriel" for p in parts)
    added = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicated psalm across addition parts")
            added[n] = themes
    assert set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED

    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    psalms = book["psalmAnalyses"]
    assert len(psalms) == len(NUMBERS) and {p["number"] for p in psalms} == NUMBERS
    old_count = new_count = verse_count = 0
    nonstandard = []
    for psalm in psalms:
        n = psalm["number"]
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == psalm["recordId"] and src["title"] == psalm["title"]
        assert src["archangel"] == "ouriel"
        nums = [v["number"] for v in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "incorrect verse order")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        verse_count += len(nums)

        original, new = frozen["psalms"][str(n)], added[str(n)]
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate original theme")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical relation altered")
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "invalid original evidence")
            old_count += 1
        for tid, rel in new.items():
            assert rel["themeId"] == tid and rel["label"] == canonical[tid], (n, tid)
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid)
            assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(rel["teaching"]) >= 75, (n, tid, "brief explanation")
            assert tid not in original, (n, tid, "historical theme collision")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "conflicting enrichment")
            else:
                psalm["themes"].append(rel)
                existing[tid] = rel
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (
        old_count, new_count, verse_count
    )
    assert not nonstandard, nonstandard
    # À conserver comme doctrine religieuse, sans inventer d'efficacité médicale.
    ps177 = load(CORPUS / "psalm-177.json")
    assert "thérapies esséniennes" in ps177["title"].lower()

    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Références contrôlées dans les JSON déjà issus de l'extraction PDF. "
        "Aucune nouvelle relecture intégrale indépendante du PDF original. "
        "Les propos spirituels, relatifs au karma et aux thérapies esséniennes "
        "sont conservés en tant que doctrines internes du texte, sans "
        "présenter des effets médicaux comme scientifiquement établis."
    )
    audit = {
        "scope": "book-28-psalms-156-181",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-28/psalm-156.json through psalm-181.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Le psaume 177 « Les 4 fondements des thérapies esséniennes » "
            "présente des explications de maladie et de guérison propres "
            "à la doctrine du texte ; elles ne sont pas une validation "
            "médicale de thérapies et ne remplacent pas les soins de santé.",
            "Quelques titres issus de l'extraction comportent des espaces "
            "insolites (p. ex. « D ieu » et « N ation E ssénienne »). "
            "Ils sont conservés pour ne pas modifier le corpus primaire "
            "sans contrôle de la source PDF."
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
        f"BOOK28 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} extracted verses, "
        f"{HISTORICAL} historical, {ADDED} added, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
