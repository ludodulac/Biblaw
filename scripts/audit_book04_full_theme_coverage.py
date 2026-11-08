#!/usr/bin/env python3
"""Book 4 (Ouriel) complete verse-grounded thematic coverage regression.

Only the canonical thematic associations may change. The original 77 links
are frozen verbatim by an immutable snapshot; the 299 additions have to be
supported by a verse that exists in the untouched psalm corpus.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/thematic-index"
BOOK = BASE / "books/book-04.json"
SNAPSHOT = BASE / "audits/book04-original-relations.json"
CORPUS = ROOT / "data/corpus/books/book-04"
EXPECTED_PALMS = 24
EXPECTED_VERSES = 300
EXPECTED_ORIGINAL = 77
EXPECTED_ADDED = 299

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book = load(BOOK)
    baseline = load(SNAPSHOT)
    assert book["book"]["number"] == 4
    assert book["book"]["archangel"] == "ouriel"
    assert len(book["psalmAnalyses"]) == EXPECTED_PALMS
    assert baseline["originalRelationCount"] == EXPECTED_ORIGINAL
    assert book["method"]["themeCoverageAudits"][-1]["addedRelationCount"] == EXPECTED_ADDED
    assert book["method"]["themeCoverageAudits"][-1]["verifiedVerseCount"] == EXPECTED_VERSES
    original = added = verse_count = 0
    seen_psalms = set()
    for psalm in book["psalmAnalyses"]:
        n = psalm["number"]
        assert n not in seen_psalms and 1 <= n <= EXPECTED_PALMS
        seen_psalms.add(n)
        text = load(CORPUS / f"psalm-{n:03d}.json")
        assert text["id"] == psalm["recordId"]
        assert text["title"] == psalm["title"]
        assert text["archangel"] == "ouriel"
        verses = {verse["number"] for verse in text["verses"]}
        assert verses == set(range(1, len(verses) + 1)), f"Psalm {n}: invalid verse sequence"
        verse_count += len(verses)
        old = baseline["psalms"][str(n)]
        encountered = set()
        for theme in psalm["themes"]:
            theme_id = theme["themeId"]
            assert theme_id not in encountered, f"Psalm {n}: duplicate theme {theme_id}"
            encountered.add(theme_id)
            assert theme["label"].strip()
            assert theme["importance"] in {"central", "important", "secondary"}
            assert theme["directness"] in {"direct", "symbolic", "editorial"}
            refs = theme["verseNumbers"]
            assert refs and len(refs) == len(set(refs)) and set(refs) <= verses, (
                f"Psalm {n}, {theme_id}: invalid verse references {refs}"
            )
            assert theme["teaching"].strip()
            if theme_id in old:
                assert theme == old[theme_id], f"Psalm {n}: historical relation modified: {theme_id}"
                original += 1
            else:
                assert theme["teaching"].startswith("La Bible essénienne enseigne que "), (
                    f"Psalm {n}, {theme_id}: non-attributed new formulation"
                )
                added += 1
        assert set(old).issubset(encountered)
    assert seen_psalms == set(range(1, EXPECTED_PALMS + 1))
    assert verse_count == EXPECTED_VERSES, verse_count
    assert original == EXPECTED_ORIGINAL and added == EXPECTED_ADDED, (original, added)
    print(f"BOOK04 PASS: {len(seen_psalms)} psalms, {verse_count} verses, "
          f"{original} historical relations preserved, {added} new relations verified, "
          f"{original+added} relations total; source psalms untouched by this audit.")

if __name__ == "__main__":
    main()
