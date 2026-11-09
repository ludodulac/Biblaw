#!/usr/bin/env python3
"""Sentinelle permanente du livre 29 (191–217) : 935 versets et 327+191 liens."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-29"
NUMBERS = set(range(191, 218))
HISTORICAL, ADDED, VERSES = 327, 191, 935

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book = load(INDEX / "books/book-29.json")
    frozen = load(INDEX / "audits/book29-original-relations.json")
    pieces = [load(INDEX / f"audits/book29-enrichment-relations-part{n}.json") for n in (1, 2)]
    assert book["book"]["number"] == frozen["book"] == 29
    assert book["book"]["archangel"] == frozen["archangel"] == "michael"
    assert frozen["originalRelationCount"] == HISTORICAL
    additions = {}
    for piece in pieces:
        assert piece["book"] == 29 and piece["archangel"] == "michael"
        for n, themes in piece["psalms"].items():
            assert n not in additions, (n, "duplicate piece")
            additions[n] = themes
    assert set(map(int, frozen["psalms"])) == set(map(int, additions)) == NUMBERS
    assert sum(map(len, additions.values())) == ADDED
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    audits = [x for x in book["method"].get("themeCoverageAudits", []) if x.get("scope") == "book-29-psalms-191-217"]
    assert len(audits) == 1
    audit = audits[0]
    assert (audit["originalRelationCount"], audit["addedRelationCount"],
            audit["verifiedVerseCount"]) == (HISTORICAL, ADDED, VERSES)
    assert audit["sourcePsalmsModified"] is False
    counts = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    seen_psalms = set()
    nonstandard = []
    for psalm in book["psalmAnalyses"]:
        n = psalm["number"]
        assert n in NUMBERS and n not in seen_psalms, n
        seen_psalms.add(n)
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"] and source["title"] == psalm["title"]
        assert source["archangel"] == "michael"
        nums = [v["number"] for v in source["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "bad numbering")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        counts["psalms"] += 1
        counts["verses"] += len(nums)
        original, new = frozen["psalms"][str(n)], additions[str(n)]
        assert not set(original) & set(new), n
        seen = set()
        for relation in psalm["themes"]:
            tid = relation["themeId"]
            assert tid not in seen, (n, tid, "duplicate")
            seen.add(tid)
            assert tid in canonical
            assert relation["importance"] in {"central", "important", "related"}
            assert relation["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = relation["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "invalid verses")
            if tid in original:
                assert relation == original[tid], (n, tid, "historical changed")
                counts["historical"] += 1
            elif tid in new:
                assert relation == new[tid], (n, tid, "addition changed")
                assert relation["label"] == canonical[tid]
                assert relation["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(relation["teaching"]) >= 75
                counts["added"] += 1
            else:
                raise AssertionError((n, tid, "unexpected theme"))
        assert seen == set(original) | set(new), (n, "missing/excess")
    assert seen_psalms == NUMBERS
    assert counts == {"psalms": 27, "verses": VERSES, "historical": HISTORICAL, "added": ADDED}, counts
    assert nonstandard == audit["sourceVerseNumberingNotes"] == []
    assert "indépendante" in audit["documentaryCaveats"][0]
    print(f"BOOK29 PASS: 27 psalms 191–217, {VERSES} extracted verses, "
          f"{HISTORICAL} historical + {ADDED} new = {HISTORICAL + ADDED}.")
if __name__ == "__main__":
    main()
