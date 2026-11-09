#!/usr/bin/env python3
"""Sentinelle du livre 23 : 26 psaumes, 866 versets, 333+239 relations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-23"
NUMBERS = set(range(128, 154))
HISTORICAL, ADDED, VERSES = 333, 239, 866


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(INDEX / "books/book-23.json")
    original = load(INDEX / "audits/book23-original-relations.json")
    parts = [
        load(INDEX / "audits/book23-enrichment-relations-part1.json"),
        load(INDEX / "audits/book23-enrichment-relations-part2.json"),
    ]
    merged = {}
    for part in parts:
        assert part["book"] == 23 and part["archangel"] == "raphael"
        for n, themes in part["psalms"].items():
            assert n not in merged, (n, "duplicate audit psalm")
            merged[n] = themes

    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    assert book["book"]["number"] == original["book"] == 23
    assert book["book"]["archangel"] == original["archangel"] == "raphael"
    assert set(map(int, original["psalms"])) == set(map(int, merged)) == NUMBERS
    assert original["originalRelationCount"] == HISTORICAL
    assert len(book["psalmAnalyses"]) == len(NUMBERS)
    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-23-psalms-128-153"
    assert audit["originalRelationCount"] == HISTORICAL
    assert audit["addedRelationCount"] == ADDED
    assert audit["verifiedVerseCount"] == VERSES
    assert audit["sourcePsalmsModified"] is False
    assert "décalage" in book["method"]["numberingNote"]

    seen_psalms = set()
    nonstandard = []
    stats = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    for analysis in book["psalmAnalyses"]:
        n = analysis["number"]
        assert n in NUMBERS and n not in seen_psalms, n
        seen_psalms.add(n)
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == analysis["recordId"]
        assert source["title"] == analysis["title"]
        assert source["archangel"] == "raphael"
        nums = [v["number"] for v in source["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        stats["psalms"] += 1
        stats["verses"] += len(nums)

        historic = original["psalms"][str(n)]
        enriched = merged[str(n)]
        assert not (set(historic) & set(enriched)), (n, "overlapping historical theme")
        seen = set()
        for relation in analysis["themes"]:
            tid = relation["themeId"]
            assert tid not in seen, (n, tid, "duplicate")
            seen.add(tid)
            assert tid in canonical, (n, tid, "unknown canonical theme")
            assert relation["importance"] in {"central", "important", "related"}
            assert relation["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = relation["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid verse evidence")
            if tid in historic:
                assert relation == historic[tid], (n, tid, "historical relation changed")
                stats["historical"] += 1
            elif tid in enriched:
                assert relation == enriched[tid], (n, tid, "new relation changed")
                assert relation["label"] == canonical[tid], (n, tid, "noncanonical label")
                assert relation["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(relation["teaching"]) >= 75
                stats["added"] += 1
            else:
                raise AssertionError((n, tid, "unaudited relation"))
        assert seen == set(historic) | set(enriched), (n, "missing or excess relations")
    assert seen_psalms == NUMBERS
    assert stats == {"psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED}, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"]
    ps128 = load(CORPUS / "psalm-128.json")
    assert [v["number"] for v in ps128["verses"]] == list(range(1, 35))
    print("BOOK23 PASS: 26 psalms (128–153), 866 verses, 333 historical identical, "
          "239 new, 572 total; Psalm 128 numbering caveat recorded")


if __name__ == "__main__":
    main()
