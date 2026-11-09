#!/usr/bin/env python3
"""Enrichissement idempotent du livre 32 — « La Nouvelle Alliance » (Ouriel).

Gèle les 312 relations historiques et ajoute 182 liens thématiques étayés
par les versets du corpus JSON déjà extrait du PDF. L'examen des JSON n'est
pas une nouvelle relecture indépendante de l'intégralité du PDF original.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-32"
BOOK_PATH = INDEX / "books/book-32.json"
BASELINE = INDEX / "audits/book32-original-relations.json"
PARTS = [INDEX / f"audits/book32-enrichment-relations-part{n}.json" for n in (1, 2, 3)]
NUMBERS = set(range(182, 208))
HISTORICAL, ADDED, VERSES = 312, 182, 821

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book, frozen = load(BOOK_PATH), load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 32
    assert book["book"]["archangel"] == frozen["archangel"] == "ouriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 32 and p["archangel"] == "ouriel" for p in parts)
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
        assert src["archangel"] == "ouriel"
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
    assert nonstandard == [[182, 28, 50]], nonstandard
    if restored_historical:
        print("Restored protected historical baseline relations:", restored_historical)
    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Relations descriptives vérifiées dans les JSON déjà extraits du PDF. "
        "Aucune nouvelle comparaison exhaustive indépendante avec le PDF original. "
        "Les énoncés doctrinaux, notamment spirituels ou liés à la guérison, "
        "ne constituent pas des affirmations médicalement ou scientifiquement validées. "
        "Cette indexation reste non exclusive."
    )
    audit = {
        "scope": "book-32-psalms-182-207",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-32/psalm-182.json through psalm-207.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Les versets ont été contrôlés dans les JSON extraits du PDF, "
            "sans nouvelle relecture indépendante de l'intégralité du PDF original.",
            "Les descriptions spirituelles et les passages évoquant la guérison "
            "sont rapportés comme doctrine interne du texte, sans validation médicale.",
            "Certains titres du corpus extrait ont des espacements atypiques "
            "(comme « Œ uvrez » et « D ieu ») : les originaux sont conservés."
        ],
    }
    method["themeCoverageAudits"] = [
        a for a in method.get("themeCoverageAudits", [])
        if a.get("scope") != audit["scope"]
    ] + [audit]
    output = json.dumps(book, ensure_ascii=False, indent=2) + "\n"
    if BOOK_PATH.read_text(encoding="utf-8") != output:
        BOOK_PATH.write_text(output, encoding="utf-8")
    print(f"BOOK32 ENRICHMENT OK: 26 psalms, {VERSES} extracted verses, "
          f"{HISTORICAL} historical + {ADDED} new = {HISTORICAL + ADDED}")

if __name__ == "__main__":
    main()
