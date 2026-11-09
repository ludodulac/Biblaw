#!/usr/bin/env python3
"""Sentinelle du livre 27 : 26 psaumes, 746 versets JSON, 312+201 liens."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-27"
NUMBERS = set(range(154, 180))
HISTORICAL, ADDED, VERSES = 312, 201, 746
TRUNCATED_TITLES = {
    160: "Ne prenez pas d’engagements à la",
    165: "Connaissez-vous le nom et la",
    173: "Avant d’aller vers les D ieux,",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(INDEX / "books/book-27.json")
    frozen = load(INDEX / "audits/book27-original-relations.json")
    parts = [
        load(INDEX / "audits/book27-enrichment-relations-part1.json"),
        load(INDEX / "audits/book27-enrichment-relations-part2.json"),
    ]
    added = {}
    for part in parts:
        assert part["book"] == 27 and part["archangel"] == "raphael"
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate part")
            added[n] = themes
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    assert book["book"]["number"] == frozen["book"] == 27
    assert book["book"]["archangel"] == frozen["archangel"] == "raphael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED
    assert len(book["psalmAnalyses"]) == len(NUMBERS)

    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-27-psalms-154-179"
    assert (audit["originalRelationCount"], audit["addedRelationCount"],
            audit["verifiedVerseCount"]) == (HISTORICAL, ADDED, VERSES)
    assert audit["sourcePsalmsModified"] is False
    stats = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    seen_psalms = set()
    nonstandard = []
    for analysis in book["psalmAnalyses"]:
        n = analysis["number"]
        assert n in NUMBERS and n not in seen_psalms, n
        seen_psalms.add(n)
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == analysis["recordId"]
        assert src["title"] == analysis["title"]
        assert src["archangel"] == "raphael"
        nums = [v["number"] for v in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "invalid verse numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        stats["psalms"] += 1
        stats["verses"] += len(nums)
        original, new = frozen["psalms"][str(n)], added[str(n)]
        assert not (set(original) & set(new)), (n, "historical collision")
        seen = set()
        for rel in analysis["themes"]:
            tid = rel["themeId"]
            assert tid not in seen, (n, tid, "duplicate")
            seen.add(tid)
            assert tid in canonical, (n, tid, "noncanonical id")
            assert rel["importance"] in {"central", "important", "related"}
            assert rel["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            nums = rel["verseNumbers"]
            assert nums and len(nums) == len(set(nums)) and set(nums) <= valid, (n, tid, "invalid refs")
            if tid in original:
                assert rel == original[tid], (n, tid, "historical relation changed")
                stats["historical"] += 1
            elif tid in new:
                assert rel == new[tid], (n, tid, "new relation changed")
                assert rel["label"] == canonical[tid]
                assert rel["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(rel["teaching"]) >= 75
                stats["added"] += 1
            else:
                raise AssertionError((n, tid, "unaccounted relation"))
        assert seen == set(original) | set(new), (n, "missing or additional relations")
    assert seen_psalms == NUMBERS
    assert stats == {
        "psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED
    }, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"] == []
    for n, title in TRUNCATED_TITLES.items():
        assert load(CORPUS / f"psalm-{n:03d}.json")["title"] == title
        assert str(n) in audit["documentaryCaveats"][0]
    print(
        f"BOOK27 PASS: 26 psalms (154–179), {VERSES} extracted verses, "
        f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total, "
        "3 pre-existing truncated titles flagged"
    )


if __name__ == "__main__":
    main()
