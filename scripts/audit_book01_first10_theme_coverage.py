#!/usr/bin/env python3
"""Corpus-grounded regression test for BIBLAW Book 01, Psalms 1–10.

The canonical Psalm texts are never changed here. This fixture preserves every pre-audit
theme ID and verifies 40 additional verse-anchored, editorially reviewed relations,
as well as the generated browser-facing thematic search projections.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/thematic-index/books/book-01.json"
CORPUS = ROOT / "data/corpus/books/book-01"
INDEX = ROOT / "data/thematic-index"
BASELINE = {
    1: "present temps",
    2: "mondes coeur nature anges arbre eau animal monde-artificiel",
    3: "preparation perfection attention action monde-subtil alliance",
    4: "ideal feu anges tradition-de-la-lumiere temple pierre ecole-de-dieu",
    5: "communication-avec-le-divin vertus corps lois-spirituelles anges priere impersonnalite",
    6: "liberation ombre anges resurrection equilibre",
    7: "chambre-secrete intimite flamme pere aura hierarchie-divine",
    8: "illusion discernement terre-et-mere monde-invisible tortue echange",
    9: "semence terre-interieure vertus connaissance-de-soi guerison cerf royaute ame",
    10: "pierre immobilite receptivite patience paix feu",
}
# Complete, reviewed additions. Each relationship has exact verse anchors in the canonical file.
ADDED = {
    1: "",
    2: "beaute vie soleil-interieur",
    3: "conscience union harmonie",
    4: "joie baguette-magique celebration transformation opportunite bonheur",
    5: "purete correspondances sagesse affinite",
    6: "lumiere liberte anti-fanatisme conscience",
    7: "corps-de-lumiere initiation benediction union",
    8: "amour responsabilite pollution ecologie acceptation-de-la-vie-terrestre conscience",
    9: "incarnation but-de-la-vie desir ecole-de-dieu perfection",
    10: "maitrise-de-soi guerison alliance communication-avec-le-divin lumiere",
}
EVIDENCE_SENTINELS = {
    2: {6: "beauté"},
    3: {6: "union avec Dieu"},
    4: {3: "baguette magique", 2: "célébration"},
    5: {14: "loi de correspondance"},
    6: {5: "fanatiques"},
    7: {16: "corps de Lumière"},
    8: {7: "poubelle", 4: "accepte pas ses conditions"},
    9: {17: "incarnation", 13: "désir profond"},
    10: {5: "maîtrise de soi", 12: "guérison"},
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    s = s.replace("œ", "oe").replace("æ", "ae")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def words(value: str) -> set[str]:
    return set(value.split()) if value else set()


def check() -> None:
    book = load(BOOK)
    assert book["book"]["number"] == 1
    assert len(book["psalmAnalyses"]) == 22
    analyses = {p["number"]: p for p in book["psalmAnalyses"][:10]}
    assert set(analyses) == set(range(1, 11))

    public = load(INDEX / "theme-directory-public.json")
    directory = load(INDEX / "theme-directory.json")
    runtime = load(INDEX / "theme-search-runtime.json")
    public_by_id = {t["id"]: t for t in public["themes"]}
    canonical_by_id = {t["id"]: t for t in directory["themes"]}
    assert public["themeCount"] == len(public_by_id) == directory["themeCount"]
    assert set(public_by_id) == set(canonical_by_id)
    assert runtime["themeCount"] == len(public_by_id)

    total_baseline = total_added = verse_count = 0
    for n in range(1, 11):
        analysis = analyses[n]
        source = load(CORPUS / f"psalm-{n:03d}.json")
        assert analysis["recordId"] == source["id"] == f"book-01-psalm-{n:03d}"
        verses = {v["number"]: v["text"] for v in source["verses"]}
        verse_count += len(verses)
        for vno, phrase in EVIDENCE_SENTINELS.get(n, {}).items():
            assert norm(phrase) in norm(verses[vno]), (n, vno, phrase)

        base = words(BASELINE[n])
        extra = words(ADDED[n])
        found = {t["themeId"]: t for t in analysis["themes"]}
        assert len(found) == len(analysis["themes"]), f"duplicate theme in {n}"
        assert base.isdisjoint(extra), f"repeated preexisting theme in {n}"
        assert set(found) == base | extra, (n, sorted(set(found) ^ (base | extra)))
        total_baseline += len(base)
        total_added += len(extra)
        for id_, rel in found.items():
            anchors = rel["verseNumbers"]
            assert anchors and all(v in verses for v in anchors), (n, id_, anchors)
            assert rel["teaching"].strip(), (n, id_)
            assert rel["importance"] in {"central", "important", "related"}
            assert rel["directness"] in {"direct", "symbolic", "editorial", "contextual", "indirect"}
            if id_ in extra:
                assert rel["teaching"].startswith("La Bible essénienne"), (n, id_)
            expected = [(t, o) for t in (public_by_id[id_], canonical_by_id[id_])
                        for o in t["occurrences"] if o["recordId"] == analysis["recordId"]]
            assert len(expected) == 2, (n, id_, len(expected))
            for _, occ in expected:
                assert occ["verseNumbers"] == anchors, (n, id_, "verse drift")
                assert occ["teaching"] == rel["teaching"], (n, id_, "text drift")
                assert occ["importance"] == rel["importance"], (n, id_, "rank drift")

    assert verse_count == 103, verse_count
    assert total_baseline == 61, total_baseline
    assert total_added == 40, total_added
    assert len(public["themes"]) >= 1255
    for theme_id, label in (
        ("baguette-magique", "Baguette magique"),
        ("celebration", "Célébration"),
        ("acceptation-de-la-vie-terrestre", "Acceptation de la vie terrestre"),
    ):
        assert theme_id in public_by_id
        assert theme_id in runtime["aliases"][norm(label)]["themeIds"]

    print(
        "BIBLAW FIRST-10-THEMES PASS: 10 Psalms, 103 unchanged source verses, "
        "61 baseline + 40 checked new canonical relations; complete site projections and "
        "3 new search themes accessible."
    )


if __name__ == "__main__":
    check()
