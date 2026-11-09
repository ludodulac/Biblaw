#!/usr/bin/env python3
"""Enrichissement idempotent du livre 38 — « Les 22 étapes de l’Initiation » (Gabriel).

Gèle les 312 relations historiques et ajoute 182 liens thématiques étayés
par les versets du corpus JSON déjà extrait du PDF. L'examen des JSON n'est
pas une nouvelle relecture indépendante de l'intégralité du PDF original.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-38"
BOOK_PATH = INDEX / "books/book-38.json"
BASELINE = INDEX / "audits/book38-original-relations.json"
PARTS = [INDEX / f"audits/book38-enrichment-relations-part{n}.json" for n in (1, 2, 3)]
NUMBERS = set(range(244, 270))
HISTORICAL, ADDED, VERSES = 312, 182, 980

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book, frozen = load(BOOK_PATH), load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 38
    assert book["book"]["archangel"] == frozen["archangel"] == "gabriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 38 and p["archangel"] == "gabriel" for p in parts)
    additions = {}
    for piece in parts:
        for n, themes in piece["psalms"].items():
            assert n not in additions, (n, "duplicate enrichment psalm")
            additions[n] = themes
    assert set(map(int, additions)) == NUMBERS
    assert sum(map(len, additions.values())) == ADDED
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    analyses = book["psalmAnalyses"]
    assert len(analyses) == 26 and {p["number"] for p in analyses} == NUMBERS
    original_count = added_count = verse_count = 0
    nonstandard = []
    restored_historical = []
    for analysis in analyses:
        n = analysis["number"]
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == analysis["recordId"] and src["title"] == analysis["title"], n
        assert src["archangel"] == "gabriel"
        numbers = [v["number"] for v in src["verses"]]
        assert numbers and numbers == sorted(set(numbers)), (n, "verse order")
        if numbers != list(range(1, len(numbers) + 1)):
            nonstandard.append([n, numbers[0], numbers[-1]])
        valid = set(numbers)
        verse_count += len(numbers)
        original, new = frozen["psalms"][str(n)], additions[str(n)]
        assert not set(original) & set(new), (n, "historical theme collision")
        existing = {rel["themeId"]: rel for rel in analysis["themes"]}
        assert len(existing) == len(analysis["themes"]), (n, "duplicate existing theme")
        for tid, rel in original.items():
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "invalid original verse")
            # Rebuild scripts can normalize historical entries. Our frozen baseline
            # is authoritative and must be restored exactly if that happens.
            if existing.get(tid) != rel:
                restored_historical.append((n, tid))
                if tid in existing:
                    for ix, candidate in enumerate(analysis["themes"]):
                        if candidate["themeId"] == tid:
                            analysis["themes"][ix] = rel
                            break
                else:
                    analysis["themes"].append(rel)
                existing[tid] = rel
            original_count += 1
        for tid, rel in new.items():
            assert tid not in original, (n, tid, "colliding relation")
            assert rel["themeId"] == tid and rel["label"] == canonical[tid]
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid verse")
            assert rel["teaching"].startswith("La Bible essénienne enseigne que ")
            assert len(rel["teaching"]) >= 75, (n, tid, "explanation too short")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "enrichment changed")
            else:
                analysis["themes"].append(rel)
                existing[tid] = rel
            added_count += 1
    assert (original_count, added_count, verse_count) == (HISTORICAL, ADDED, VERSES), (
        original_count, added_count, verse_count
    )
    assert nonstandard == [[260, 23, 54]], nonstandard
    if restored_historical:
        print("Restored protected historical baseline relations:", restored_historical)
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Relations documentaires descriptives vérifiées dans les JSON extraits du PDF, "
        "sans relecture indépendante intégrale du PDF original. "
        "Les enseignements sur les 22 commandements, les mondes subtils, la mort, "
        "la sexualité et la nature sont présentés comme doctrine du texte. "
        "Les propos sur la santé, les substances, l'électricité, les implants ou "
        "la guérison ne constituent ni faits médicaux établis ni conseils médicaux. "
        "Cette indexation reste non exclusive."
    )
    audit = {
        "scope": "book-38-psalms-244-269",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-38/psalm-244.json through psalm-269.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Les versets sont contrôlés dans les JSON extraits du PDF, sans nouvelle relecture indépendante de l'intégralité du PDF original.",
            "Les passages sur les traitements, drogues, électricité, implants et santé, ainsi que la vie après la mort, sont documentés comme positions doctrinales non validées scientifiquement ou médicalement.",
            "La numérotation canonique du psaume 260 commence à 23 et finit à 54 : elle est conservée sans renumérotation.",
        ],
    }
    method["themeCoverageAudits"] = [
        a for a in method.get("themeCoverageAudits", [])
        if a.get("scope") != audit["scope"]
    ] + [audit]
    output = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != output:
        BOOK_PATH.write_text(output, encoding="utf-8")
    print(f"BOOK38 ENRICHMENT OK: 26 psalms, {VERSES} extracted verses, "
          f"{HISTORICAL} historical + {ADDED} new = {HISTORICAL + ADDED}")

if __name__ == "__main__":
    main()
