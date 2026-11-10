#!/usr/bin/env python3
"""Contrôle durable du livre 41 de Michaël : 26 psaumes, 974 versets, 312 + 182 liens."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-41"
NUMBERS = set(range(270, 296))
HISTORICAL, ADDED, VERSES = 312, 182, 974

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book = load(INDEX / "books/book-41.json")
    frozen = load(INDEX / "audits/book41-original-relations.json")
    pieces = [load(INDEX / f"audits/book41-enrichment-relations-part{n}.json") for n in (1, 2, 3)]
    assert book["book"]["number"] == frozen["book"] == 41
    assert book["book"]["archangel"] == frozen["archangel"] == "michael"
    assert frozen["originalRelationCount"] == HISTORICAL
    additions = {}
    for piece in pieces:
        assert piece["book"] == 41 and piece["archangel"] == "michael"
        for n, themes in piece["psalms"].items():
            assert n not in additions, (n, "duplicate part")
            additions[n] = themes
    assert set(map(int, frozen["psalms"])) == set(map(int, additions)) == NUMBERS
    assert sum(map(len, additions.values())) == ADDED
    canonical = {
        t["themeId"]: t["canonicalLabel"]
        for t in load(INDEX / "theme-search-index.json")["themes"]
    }
    checks = [
        a for a in book["method"].get("themeCoverageAudits", [])
        if a.get("scope") == "book-41-psalms-270-295"
    ]
    assert len(checks) == 1
    check = checks[0]
    assert (check["originalRelationCount"], check["addedRelationCount"],
            check["verifiedVerseCount"]) == (HISTORICAL, ADDED, VERSES)
    assert check["sourcePsalmsModified"] is False
    counts = {"psalms": 0, "verses": 0, "historical": 0, "added": 0}
    seen_psalms, nonstandard = set(), []
    for analysis in book["psalmAnalyses"]:
        n = analysis["number"]
        assert n in NUMBERS and n not in seen_psalms, (n, "duplicate/missing")
        seen_psalms.add(n)
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert src["id"] == analysis["recordId"] and src["title"] == analysis["title"]
        assert src["archangel"] == "michael"
        nums = [v["number"] for v in src["verses"]]
        assert nums and nums == sorted(set(nums)), (n, "unsorted verse numbers")
        if nums != list(range(1, len(nums) + 1)):
            nonstandard.append([n, nums[0], nums[-1]])
        valid = set(nums)
        counts["psalms"] += 1
        counts["verses"] += len(nums)
        original, new = frozen["psalms"][str(n)], additions[str(n)]
        assert not set(original) & set(new), (n, "historical collision")
        seen = set()
        for rel in analysis["themes"]:
            tid = rel["themeId"]
            assert tid not in seen and tid in canonical, (n, tid, "duplicate/noncanonical")
            seen.add(tid)
            assert rel["importance"] in {"central", "important", "related"}
            assert rel["directness"] in {"direct", "symbolic", "editorial", "indirect", "contextual"}
            refs = rel["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= valid, (n, tid, "bad verses")
            if tid in original:
                assert rel == original[tid], (n, tid, "historical changed")
                counts["historical"] += 1
            elif tid in new:
                assert rel == new[tid], (n, tid, "enrichment changed")
                assert rel["label"] == canonical[tid]
                assert rel["teaching"].startswith("La Bible essénienne enseigne que ")
                assert len(rel["teaching"]) >= 75
                # La présence du verset exact dans l'explication empêche une
                # citation attribuée au mauvais psaume ou un contenu inventé.
                verse_texts = [
                    v["text"].strip() for v in src["verses"]
                    if v["number"] in refs
                ]
                assert any(f"« {txt} »" in rel["teaching"] for txt in verse_texts), (
                    n, tid, "citation not faithful to source JSON"
                )
                counts["added"] += 1
            else:
                raise AssertionError((n, tid, "unexpected thematic relation"))
        assert seen == set(original) | set(new), (n, "missing/excess")
    assert seen_psalms == NUMBERS
    assert counts == {"psalms": 26, "verses": VERSES, "historical": HISTORICAL, "added": ADDED}, counts
    assert nonstandard == check["sourceVerseNumberingNotes"] == []
    assert "indépendante" in check["documentaryCaveats"][0]
    print(f"BOOK41 PASS: 26 psalms 270–295, {VERSES} extracted verses, "
          f"{HISTORICAL} historical + {ADDED} new = {HISTORICAL + ADDED}.")
if __name__ == "__main__":
    main()
