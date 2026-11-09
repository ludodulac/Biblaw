#!/usr/bin/env python3
"""Applique de manière idempotente l'enrichissement du livre 27 (Raphaël).

312 associations anciennes restent rigoureusement identiques. 201 relations
supplémentaires citent les numéros des 746 versets dans le corpus JSON
préexistant issu du PDF. Ce travail n'est pas une nouvelle relecture
indépendante du PDF original.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
BOOK_PATH = INDEX / "books/book-27.json"
BASELINE = INDEX / "audits/book27-original-relations.json"
PARTS = [
    INDEX / "audits/book27-enrichment-relations-part1.json",
    INDEX / "audits/book27-enrichment-relations-part2.json",
]
CORPUS = ROOT / "data/corpus/books/book-27"
NUMBERS = set(range(154, 180))
HISTORICAL, ADDED, VERSES = 312, 201, 746

TRUNCATED_TITLES = {
    160: "Ne prenez pas d’engagements à la",
    165: "Connaissez-vous le nom et la",
    173: "Avant d’aller vers les D ieux,",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book, frozen = load(BOOK_PATH), load(BASELINE)
    parts = [load(p) for p in PARTS]
    assert book["book"]["number"] == frozen["book"] == 27
    assert book["book"]["archangel"] == frozen["archangel"] == "raphael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == NUMBERS
    assert all(p["book"] == 27 and p["archangel"] == "raphael" for p in parts)
    additions = {}
    for part in parts:
        for n, themes in part["psalms"].items():
            assert n not in additions, (n, "duplicate additions")
            additions[n] = themes
    assert set(map(int, additions)) == NUMBERS
    assert sum(map(len, additions.values())) == ADDED
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
        assert src["archangel"] == "raphael"
        nums = [v["number"] for v in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "incorrect verse order")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        verse_count += len(nums)

        original, new = frozen["psalms"][str(n)], additions[str(n)]
        existing = {t["themeId"]: t for t in psalm["themes"]}
        assert len(existing) == len(psalm["themes"]), (n, "duplicated index theme")
        for tid, rel in original.items():
            assert existing.get(tid) == rel, (n, tid, "historical relation altered")
            assert set(rel["verseNumbers"]) <= valid, (n, tid, "original invalid verse")
            old_count += 1
        for tid, rel in new.items():
            assert rel["themeId"] == tid and rel["label"] == canonical[tid], (n, tid)
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid)
            assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
            assert len(rel["teaching"]) >= 75, (n, tid)
            assert tid not in original, (n, tid, "historical collision")
            if tid in existing:
                assert existing[tid] == rel, (n, tid, "new relation conflict")
            else:
                psalm["themes"].append(rel)
                existing[tid] = rel
            new_count += 1

    assert (old_count, new_count, verse_count) == (HISTORICAL, ADDED, VERSES), (
        old_count, new_count, verse_count
    )
    assert nonstandard == [], nonstandard
    for n, title in TRUNCATED_TITLES.items():
        assert load(CORPUS / f"psalm-{n:03d}.json")["title"] == title

    method = book["method"]
    method["interpretiveScope"] = "descriptive-indexing-non-exclusive"
    method["interpretivePolicy"] = (
        "Références vérifiées dans les fichiers JSON issus de l'extraction PDF "
        "déjà présente ; pas de nouvelle comparaison indépendante et intégrale "
        "avec le PDF. Les affirmations sur la spiritualité, l'au-delà, la "
        "résurrection ou la guérison sont décrites comme doctrine du texte, "
        "et non comme des faits scientifiques établis."
    )
    audit = {
        "scope": "book-27-psalms-154-179",
        "reviewedOn": "2026-11-09",
        "source": "data/corpus/books/book-27/psalm-154.json through psalm-179.json",
        "approach": "conservative-editorial-verse-evidence-in-extracted-json",
        "originalRelationCount": HISTORICAL,
        "addedRelationCount": ADDED,
        "verifiedVerseCount": VERSES,
        "sourcePsalmsModified": False,
        "sourceVerseNumberingNotes": nonstandard,
        "documentaryCaveats": [
            "Trois titres existants paraissent tronqués dans le corpus JSON : "
            "psaume 160 (« Ne prenez pas d’engagements à la »), "
            "psaume 165 (« Connaissez-vous le nom et la »), "
            "psaume 173 (« Avant d’aller vers les D ieux, »). "
            "Ces titres ont été conservés sans invention et requièrent "
            "une comparaison avec le PDF original."
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
        f"BOOK27 ENRICHMENT OK: {len(psalms)} psalms, {VERSES} extracted verses, "
        f"{HISTORICAL} historical, {ADDED} added, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
