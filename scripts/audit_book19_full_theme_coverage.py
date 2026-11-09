#!/usr/bin/env python3
"""Contrôle pérenne du livre 19 Raphaël : 26 psaumes, 817 versets, 401+292 relations."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-19"
NUMBERS = set(range(102, 128))
HISTORICAL, ADDED, VERSES = 401, 292, 817

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book = load(INDEX / "books/book-19.json")
    frozen = load(INDEX / "audits/book19-original-relations.json")
    added = load(INDEX / "audits/book19-enrichment-relations.json")
    canonical = {x["themeId"]: x["canonicalLabel"]
                 for x in load(INDEX / "theme-search-index.json")["themes"]}
    assert book["book"]["number"] == frozen["book"] == added["book"] == 18
    assert book["book"]["archangel"] == frozen["archangel"] == added["archangel"] == "raphael"
    assert frozen["originalRelationCount"] == HISTORICAL
    assert set(map(int, frozen["psalms"])) == set(map(int, added["psalms"])) == NUMBERS
    assert len(book["psalmAnalyses"]) == len(NUMBERS)
    audit = book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"] == "book-19-psalms-102-127"
    assert audit["originalRelationCount"] == HISTORICAL
    assert audit["addedRelationCount"] == ADDED and audit["verifiedVerseCount"] == VERSES
    assert audit["sourcePsalmsModified"] is False

    stats = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    seen_psalms = set()
    nonstandard = []
    for psalm in book["psalmAnalyses"]:
        n = psalm["number"]
        assert n in NUMBERS and n not in seen_psalms, n
        seen_psalms.add(n)
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == psalm["recordId"] and src["title"] == psalm["title"]
        assert src["archangel"] == "raphael", n
        nums = [x["number"] for x in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        stats["psalms"] += 1
        stats["verses"] += len(nums)

        historical = frozen["psalms"][str(n)]
        enriched = added["psalms"][str(n)]
        assert not (set(historical) & set(enriched)), (n, "overlapping source")
        seen = set()
        for rel in psalm["themes"]:
            tid = rel["themeId"]
            assert tid not in seen, (n, tid, "duplicate")
            seen.add(tid)
            assert tid in canonical, (n, tid, "noncanonical theme")
            assert rel["label"] == canonical[tid], (n, tid, "canonical label")
            assert rel["importance"] in {"central", "important", "related"}
            assert rel["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid verses")
            if tid in historical:
                assert rel == historical[tid], (n, tid, "historical relation modified")
                stats["historical"] += 1
            elif tid in enriched:
                assert rel == enriched[tid], (n, tid, "enrichment relation modified")
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "), (n, tid)
                assert len(rel["teaching"]) > 65, (n, tid)
                stats["added"] += 1
            else:
                raise AssertionError((n, tid, "relation without audited provenance"))
        assert seen == set(historical) | set(enriched), (n, "missing or excess relations")
    assert seen_psalms == NUMBERS
    assert stats == {"psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED}, stats
    assert nonstandard == audit["sourceVerseNumberingNotes"], nonstandard
    print(f"BOOK19 PASS: 26 psalms (102–127), {VERSES} verses, "
          f"{HISTORICAL} historical identical, {ADDED} new, {HISTORICAL+ADDED} total")

if __name__ == "__main__":
    main()
