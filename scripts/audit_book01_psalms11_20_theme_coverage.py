#!/usr/bin/env python3
"""Guard corpus-grounded theme additions in Book 01, Psalms 11–20.

The original 60 relations must remain intact; each additional relation must have exact Psalm
verse evidence, and complete generated canonical + public indexes must match that evidence.
No Psalm prose, prayer, private note or FAQ content is altered by this check.
"""
from __future__ import annotations
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
SOURCE = ROOT / "data/corpus/books/book-01"

BASELINE = {
  11: "responsabilite actes heredite bien-commun sens-de-la-vie feu",
  12: "cerf force peur feu culte chemin",
  13: "regard jugement amour fraternite aigle discernement",
  14: "fidelite experience chemin lumiere",
  15: "amour association mage corps temple-interieur",
  16: "respect regnes plante pierre animal montagne amour",
  17: "joie action priere liberation aigle lumiere",
  18: "livre-de-la-vie symboles vegetaux pierre animal destinee pensee chemin",
  19: "mere amour jugement authenticite corps confiance",
  20: "mage creation homme-et-femme feu regard resurrection",
}
ADDED = {
  11: "conscience beaute descendance harmonie immortalite creation evolution",
  12: "biche courage transformation royaute fidelite protection",
  13: "beaute joie soleil verite christ cathares amitie",
  14: "accomplissement bonheur engagement doute couple",
  15: "heredite transformation purete amitie fraternite union lumiere",
  16: "preparation vertus equilibre guerison responsabilite douceur",
  17: "bonheur meditation amour conscience royaute celebration conviction musique",
  18: "experience incarnation orientation union memoire maitrise-de-soi transmission",
  19: "conscience joie bonheur peur fraternite abondance enfant christ verite maladie",
  20: "union lumiere semence corps pensee conscience evolution",
}
SENTINELS = {
  11: {2: "beauté divine", 8: "descendance"},
  12: {2: "biche", 4: "roi"},
  13: {9: "Cathares", 5: "amitié"},
  14: {4: "couple", 11: "bonheur"},
  15: {6: "ami", 7: "associer"},
  16: {2: "préparez", 8: "guérit"},
  17: {6: "musiques", 10: "Célébrez"},
  18: {4: "prochaines vies", 6: "pensée juste"},
  19: {4: "maladies", 11: "tous les enfants"},
  20: {2: "s'unir", 4: "évolution"},
}
NEW_THEMES = {
    "evolution": "Évolution",
    "cathares": "Cathares",
    "amitie": "Amitié",
    "couple": "Couple",
    "maladie": "Maladie",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c)).casefold()
    value = value.replace("œ", "oe").replace("æ", "ae")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

def terms(text):
    return set(text.split()) if text else set()

def check():
    book = load(INDEX / "books/book-01.json")
    assert len(book["psalmAnalyses"]) == 22
    by_number = {p["number"]: p for p in book["psalmAnalyses"][10:20]}
    assert set(by_number) == set(range(11, 21))
    directory = load(INDEX / "theme-directory.json")
    public = load(INDEX / "theme-directory-public.json")
    runtime = load(INDEX / "theme-search-runtime.json")
    d_by_id = {t["id"]: t for t in directory["themes"]}
    p_by_id = {t["id"]: t for t in public["themes"]}
    assert set(d_by_id) == set(p_by_id)
    assert runtime["themeCount"] == directory["themeCount"] == public["themeCount"] == len(d_by_id)

    base_count = 0
    new_count = 0
    verse_count = 0
    for n in range(11,21):
        a = by_number[n]
        src = load(SOURCE / f"psalm-{n:03d}.json")
        assert a["recordId"] == src["id"] == f"book-01-psalm-{n:03d}"
        assert a["title"] == src["title"]
        verses = {int(v["number"]):v["text"] for v in src["verses"]}
        verse_count += len(verses)
        for number,phrase in SENTINELS[n].items():
            assert norm(phrase) in norm(verses[number]), (n,number,phrase)
        before = terms(BASELINE[n])
        extra = terms(ADDED[n])
        assert before.isdisjoint(extra), (n,"duplicate intent")
        rels = a["themes"]
        current = {t["themeId"]:t for t in rels}
        assert len(current)==len(rels), (n,"duplicate themeId")
        assert set(current)==before|extra, (n,sorted(set(current)^(before|extra)))
        base_count+=len(before)
        new_count+=len(extra)
        for tid,rel in current.items():
            anchors = rel["verseNumbers"]
            assert anchors and all(int(v) in verses for v in anchors), (n,tid,anchors)
            assert rel["importance"] in {"central","important","related"}, (n,tid)
            assert rel["directness"] in {"direct","symbolic","contextual","editorial","indirect"}, (n,tid)
            assert rel["teaching"], (n,tid)
            if tid in extra:
                assert rel["teaching"].startswith("La Bible essénienne"), (n,tid)
            for d in (d_by_id,p_by_id):
                assert tid in d, (n,tid,"missing theme in derivative")
                selected = [o for o in d[tid]["occurrences"] if o["recordId"]==a["recordId"]]
                assert len(selected)==1, (n,tid,"missing or repeated occurrence")
                occ=selected[0]
                for field in ("importance","verseNumbers","teaching"):
                    assert occ[field]==rel[field], (n,tid,field,"projection drift")

    assert verse_count==92, verse_count
    assert base_count==60, base_count
    assert new_count==70, new_count
    assert len(d_by_id)>=1260, len(d_by_id)
    for tid,label in NEW_THEMES.items():
        assert tid in d_by_id
        entry=runtime["aliases"].get(norm(label))
        assert entry and tid in entry["themeIds"], (tid,label,"unsearchable")
    records = book["method"].get("themeCoverageAudits",[])
    assert len(records)>=2 and records[0]["scope"]=="book-01-psalms-001-010"
    assert records[1]["scope"]=="book-01-psalms-011-020"
    assert records[1]["addedRelationCount"]==70
    print("BIBLAW BOOK 01/11-20 PASS: 10 source Psalms, 92 verses unchanged, 60 original and 70 new anchored relations; 5 new searchable themes; public runtime integrity preserved.")


if __name__=="__main__":
    check()
