#!/usr/bin/env python3
"""Sentinelle permanente du livre 28 : 26 psaumes, 835 versets et 312+207 thèmes."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-28"
NUMBERS = set(range(156, 182))
HISTORICAL, ADDED, VERSES = 312, 207, 835


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(INDEX / "books/book-28.json")
    frozen = load(INDEX / "audits/book28-original-relations.json")
    parts = [
        load(INDEX / "audits/book28-enrichment-relations-part1.json"),
        load(INDEX / "audits/book28-enrichment-relations-part2.json"),
    ]
    added = {}
    for part in parts:
        assert part["book"] == 28 and part["archangel"] == "ouriel"
        for n, themes in part["psalms"].items():
            assert n not in added, (n, "duplicate part")
            added[n] = themes
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    assert book["book"]["number"] == frozen["book"] == 28
    assert book["book"]["archangel"] == frozen["archangel"] == "ouriel"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == set(map(int, added)) == NUMBERS
    assert sum(map(len, added.values())) == ADDED
    assert len(book["psalmAnalyses"]) == len(NUMBERS)

    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-28-psalms-156-181"
    assert (audit["originalRelationCount"], audit["addedRelationCount"],
            audit["verifiedVerseCount"]) == (HISTORICAL, ADDED, VERSES)
    assert audit["sourcePsalmsModified"] is False
    assert any("177" in note for note in audit["documentaryCaveats"])

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
        assert src["archangel"] == "ouriel"
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
            assert tid in canonical, (n, tid, "noncanonical identifier")
            assert rel["importance"] in {"central", "important", "related"}
            assert rel["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid verses")
            if tid in original:
                assert rel == original[tid], (n, tid, "historical relation changed")
                stats["historical"] += 1
            elif tid in new:
                assert rel == new[tid], (n, tid, "enriched relation changed")
                assert rel["label"] == canonical[tid]
                assert rel["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(rel["teaching"]) >= 75
                stats["added"] += 1
            else:
                raise AssertionError((n, tid, "unaudited relation"))
        assert seen == set(original) | set(new), (n, "missing or excess relations")

    assert seen_psalms == NUMBERS
    assert stats == {
        "psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED
    }, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"] == []
    assert "thérapies esséniennes" in load(CORPUS / "psalm-177.json")["title"].lower()
    print(
        f"BOOK28 PASS: 26 psalms (156–181), {VERSES} extracted verses, "
        f"{HISTORICAL} historical, {ADDED} new, {HISTORICAL + ADDED} total. "
        "Medical-doctrine scope caveat recorded."
    )


if __name__ == "__main__":
    main()
