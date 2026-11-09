#!/usr/bin/env python3
"""Sentinelle du livre 22 : 26 psaumes, 884 versets, 470+206 relations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-22"
NUMBERS = set(range(138, 164))
HISTORICAL, ADDED, VERSES = 470, 206, 884


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    book = load(INDEX / "books/book-22.json")
    original = load(INDEX / "audits/book22-original-relations.json")
    parts = [
        load(INDEX / "audits/book22-enrichment-relations-part1.json"),
        load(INDEX / "audits/book22-enrichment-relations-part2.json"),
    ]
    merged = {}
    for part in parts:
        assert part["book"] == 22 and part["archangel"] == "gabriel"
        for n, themes in part["psalms"].items():
            assert n not in merged, (n, "duplicate audit psalm")
            merged[n] = themes
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    assert book["book"]["number"] == original["book"] == 22
    assert book["book"]["archangel"] == original["archangel"] == "gabriel"
    assert set(map(int, original["psalms"])) == set(map(int, merged)) == NUMBERS
    assert original["originalRelationCount"] == HISTORICAL
    assert len(book["psalmAnalyses"]) == 26
    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-22-psalms-138-163"
    assert audit["originalRelationCount"] == HISTORICAL
    assert audit["addedRelationCount"] == ADDED
    assert audit["verifiedVerseCount"] == VERSES
    assert audit["sourcePsalmsModified"] is False

    seen_psalms = set()
    nonstandard = []
    stats = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    for analysis in book["psalmAnalyses"]:
        n = analysis["number"]
        assert n in NUMBERS and n not in seen_psalms
        seen_psalms.add(n)
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == analysis["recordId"]
        assert source["title"] == analysis["title"]
        assert source["archangel"] == "gabriel"
        nums = [v["number"] for v in source["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "nonunique numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        stats["psalms"] += 1
        stats["verses"] += len(nums)
        historic = original["psalms"][str(n)]
        enriched = merged[str(n)]
        assert not (set(historic) & set(enriched)), n
        seen = set()
        for relation in analysis["themes"]:
            tid = relation["themeId"]
            assert tid not in seen, (n, tid, "duplicate theme")
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
                raise AssertionError((n, tid, "unaccounted relation"))
        assert seen == set(historic) | set(enriched), (n, "missing or excess relations")
    assert seen_psalms == NUMBERS
    assert stats == {"psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED}, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"]
    assert not any(21 in rel["verseNumbers"] for rel in merged["155"].values())
    assert source_155_21_is_truncated()
    print("BOOK22 PASS: 26 psalms (138–163), 884 verses, 470 historical identical, "
          "206 new, 676 total; Psalm 155:21 extraction limitation flagged")


def source_155_21_is_truncated():
    source = load(CORPUS / "psalm-155.json")
    return next(v["text"] for v in source["verses"] if v["number"] == 21).rstrip().endswith("après la")


if __name__ == "__main__":
    main()
