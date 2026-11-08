#!/usr/bin/env python3
"""Book 7 (Raphael), psalms 24–48: verse-grounded editorial thematic coverage audit.

The source texts remain immutable. A snapshot of the 79 historical links ensures
they are retained without changing any of their metadata.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMATIC = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-07"
BOOK = THEMATIC / "books/book-07.json"
BASELINE = THEMATIC / "audits/book07-original-relations.json"
NUMBERS = set(range(24,49))
ORIGINAL = 79
ADDED = 421
VERSES = 454

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    current = load(BOOK)
    frozen = load(BASELINE)
    assert current["book"]["number"] == 7
    assert current["book"]["archangel"] == "raphael"
    assert frozen["originalRelationCount"] == ORIGINAL
    assert len(current["psalmAnalyses"]) == len(NUMBERS)
    review = current["method"]["themeCoverageAudits"][-1]
    assert review["scope"] == "book-07-psalms-024-048"
    assert review["originalRelationCount"] == ORIGINAL
    assert review["addedRelationCount"] == ADDED
    assert review["verifiedVerseCount"] == VERSES
    historical_count = new_count = verse_count = 0
    observed_psalms = set()
    for psalm in current["psalmAnalyses"]:
        n = psalm["number"]
        assert n in NUMBERS and n not in observed_psalms
        observed_psalms.add(n)
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert source["id"] == psalm["recordId"]
        assert source["title"] == psalm["title"]
        assert source["archangel"] == "raphael"
        valid_verses = {v["number"] for v in source["verses"]}
        assert valid_verses == set(range(1, len(valid_verses)+1)), n
        verse_count += len(valid_verses)
        original_themes = frozen["psalms"][str(n)]
        seen = set()
        for t in psalm["themes"]:
            key = t["themeId"]
            assert key not in seen, (n,key,"duplicate")
            seen.add(key)
            assert t["label"].strip()
            assert t["importance"] in {"central", "important", "secondary"}
            assert t["directness"] in {"direct", "symbolic", "editorial"}
            refs=t["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid_verses,(n,key,"verses",refs)
            assert t["teaching"].strip()
            if key in original_themes:
                assert t == original_themes[key], (n,key,"historical link modified")
                historical_count += 1
            else:
                assert t["teaching"].startswith("La Bible essénienne enseigne que "), (n,key,"attribution")
                new_count += 1
        assert set(original_themes).issubset(seen), (n,"historical links missing")
    assert observed_psalms == NUMBERS
    assert verse_count == VERSES, verse_count
    assert historical_count == ORIGINAL and new_count == ADDED, (historical_count,new_count)
    print(f"BOOK05 PASS: {len(observed_psalms)} psalms (24–48), {verse_count} verses, "
          f"{historical_count} original links unchanged, {new_count} new links, "
          f"{historical_count+new_count} total.")

if __name__ == "__main__":
    main()
