#!/usr/bin/env python3
"""Sentinelle du livre 25 de Michaël : 26 psaumes, 881 versets, 312+208 relations."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-25"
NUMBERS = set(range(165, 191))
HISTORICAL, ADDED, VERSES = 312, 208, 881


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    book = load(INDEX / "books/book-25.json")
    frozen = load(INDEX / "audits/book25-original-relations.json")
    parts = [
        load(INDEX / "audits/book25-enrichment-relations-part1.json"),
        load(INDEX / "audits/book25-enrichment-relations-part2.json"),
    ]
    added = {}
    for part in parts:
        assert part["book"] == 25 and part["archangel"] == "michael"
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate part")
            added[n] = themes
    canonical = {
        x["themeId"]: x["canonicalLabel"]
        for x in load(INDEX / "theme-search-index.json")["themes"]
    }
    assert book["book"]["number"] == frozen["book"] == 25
    assert book["book"]["archangel"] == frozen["archangel"] == "michael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED
    assert len(book["psalmAnalyses"]) == 26

    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-25-psalms-165-190"
    assert (audit["originalRelationCount"], audit["addedRelationCount"],
            audit["verifiedVerseCount"]) == (HISTORICAL, ADDED, VERSES)
    assert audit["sourcePsalmsModified"] is False

    stats = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    nonstandard = []
    seen_psalms = set()
    for analysis in book["psalmAnalyses"]:
        n = analysis["number"]
        assert n in NUMBERS and n not in seen_psalms, n
        seen_psalms.add(n)
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == analysis["recordId"]
        assert src["title"] == analysis["title"]
        assert src["archangel"] == "michael"
        nums = [v["number"] for v in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "invalid verse numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        stats["psalms"] += 1
        stats["verses"] += len(nums)

        historical, enriched = frozen["psalms"][str(n)], added[str(n)]
        assert not (set(historical) & set(enriched)), (n, "historical collision")
        seen = set()
        for relation in analysis["themes"]:
            tid = relation["themeId"]
            assert tid not in seen, (n, tid, "duplicate")
            seen.add(tid)
            assert tid in canonical, (n, tid, "noncanonical id")
            assert relation["importance"] in {"central", "important", "related"}
            assert relation["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = relation["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "bad verses")
            if tid in historical:
                assert relation == historical[tid], (n, tid, "historical relation changed")
                stats["historical"] += 1
            elif tid in enriched:
                assert relation == enriched[tid], (n, tid, "enriched relation changed")
                assert relation["label"] == canonical[tid]
                assert relation["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(relation["teaching"]) >= 75
                stats["added"] += 1
            else:
                raise AssertionError((n, tid, "unaccounted relation"))
        assert seen == set(historical) | set(enriched), (n, "missing/excess")
    assert seen_psalms == NUMBERS
    assert stats == {
        "psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED
    }, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"]
    assert load(CORPUS / "psalm-180.json")["title"].endswith("pour")
    print(
        f"BOOK25 PASS: 26 psalms (165–190), {VERSES} verses, "
        f"{HISTORICAL} preserved, {ADDED} added, {HISTORICAL + ADDED} total"
    )


if __name__ == "__main__":
    main()
