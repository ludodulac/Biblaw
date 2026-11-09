#!/usr/bin/env python3
"""Applique sans perte les thèmes supplémentaires du livre 26 de Gabriel.

Les 312 associations originales sont figées à l'identique. Les 207 liens
supplémentaires sont étayés par des numéros de versets des fichiers JSON
issus de l'extraction du PDF. Cela ne constitue pas une comparaison
indépendante avec le PDF original.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-26.json"
BASELINE = INDEX / "audits/book26-original-relations.json"
PARTS = [
    INDEX / "audits/book26-enrichment-relations-part1.json",
    INDEX / "audits/book26-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-26"
NUMBERS = set(range(164, 190))
HISTORICAL, ADDED, VERSES = 312, 207, 846


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    book = load(BOOK_PATH)
    frozen = load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 26
    assert book["book"]["archangel"] == frozen["archangel"] == "gabriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 26 and p["archangel"] == "gabriel" for p in parts)

    additions = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in additions, (n, "duplicate psalm in additions")
            additions[n] = themes
    assert set(map(int, additions)) == NUMBERS
    assert sum(map(len, additions.values())) == ADDED

    canonical = {
        entry["themeId"]: entry["canonicalLabel"]
        for entry in load(INDEX / "theme-search-index.json")["themes"]
    }
    psalms = book["psalmAnalyses"]
    assert len(psalms) == len(NUMBERS) and {p["number"] for p in psalms} == NUMBERS

    old_count = new_count = verse_count = 0
    nonstandard = []
    for psalm in psalms:
        n = psalm["number"]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"] and source["title"] == psalm["title"]
        assert source["archangel"] == "gabriel"
        numbers = [v["number"] for v in source["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "invalid verse sequence")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)

        original, new = frozen["psalms"][str(n)], additions[str(n)]
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicate theme")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical association changed")
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "invalid historical verse")
            old_count += 1
        for tid, rel in new.items():
            assert rel["themeId"] == tid and rel["label"] == canonical[tid], (n, tid)
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid refs")
            assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(rel["teaching"]) >= 75, (n, tid)
            assert tid not in original, (n, tid, "historical collision")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "conflicting enrichment")
            else:
                psalm["themes"].append(rel)
                existing[tid] = rel
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (
        old_count, new_count, verse_count
    )
    assert nonstandard == [[186, 23, 50]], nonstandard
    assert "Pr. 70." in load(CORPUS / "psalm-186.json")["verses"][-1]["text"]

    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Références contrôlées dans les JSON préexistants issus du PDF, "
        "sans nouvelle comparaison intégrale indépendante avec le PDF. "
        "Les énoncés spirituels et affirmations sur la santé sont décrits "
        "comme doctrine du corpus, pas comme des faits établis."
    )
    audit = {
        "scope": "book-26-psalms-164-189",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-26/psalm-164.json through psalm-189.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Le psaume 186 ne possède dans l'extraction JSON que 28 versets "
            "numérotés 23 à 50 ; les versets 1 à 22 sont absents de cette entrée. "
            "Le verset 50 contient également du texte de prière repéré par "
            "« Pr. 70. ». Aucune nouvelle association n'utilise le verset 50. "
            "Vérification dans le PDF original nécessaire avant de considérer "
            "ce psaume comme intégralement extrait."
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
        f"BOOK26 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} extracted verses, "
        f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
