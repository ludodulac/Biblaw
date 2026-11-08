#!/usr/bin/env python3
"""Audit Psalm-theme evidence for Book 1/21-22 and Book 2/1-10.

The baseline thematic relations are immutable. All new relations must cite actual source
verses and survive both canonical and browser-facing deterministic projections. Existing
Book 1 audit records must remain in place, and each new theme must be searchable.
"""
from __future__ import annotations
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books"
BASELINE = {
    (1,21): "douceur protection ame mere pere nature sens-de-la-vie",
    (1,22): "chemin amour pensee responsabilite montagne ame cendre eau ecole-essenienne",
    (2,1): "trois-mondes eau aura corps coeur",
    (2,2): "consecration alliance verite monde-divin",
    (2,3): "relations guerison eau chaleur",
    (2,4): "service action mere",
    (2,5): "communaute realisation individualite-et-collectivite",
    (2,6): "arbre grandeur ancetres",
    (2,7): "lune etoiles fees sommeil ame",
    (2,8): "vie eau meditation mere tradition-de-la-lumiere",
    (2,9): "engagement vie-interieure conviction",
    (2,10): "creation perle perfection",
}
ADDED = {
    (1,21): "amour fraternite priere vertus guerison souffrance beaute joie corps lumiere sagesse",
    (1,22): "chaleur coeur volonte evolution respect lumiere conscience purification courage conviction consecration benediction feu fidelite",
    (2,1): "preparation purification purete fecondation alliance conscience meditation maitrise-de-soi lumiere monde-divin incarnation echange",
    (2,2): "conscience illusion communication-avec-le-divin symboles plante coeur authenticite lumiere",
    (2,3): "echange harmonie conscience action maladie communication confiance",
    (2,4): "amour chaleur relations purete impersonnalite attention enfant ecole-essenienne meditation guerison",
    (2,5): "union association creation guerison action accomplissement chaine-magique conscience ecole-essenienne",
    (2,6): "racines fruit beaute bonheur joie tradition lumiere conscience",
    (2,7): "soleil preparation conscience lumiere celebration source nuit mystere monde-divin receptivite",
    (2,8): "simplicite harmonie joie bonheur purete silence purification abondance baguette-magique anges organisation alliance sagesse corps conscience union celebration immobilite chemin partage maitrise-de-soi",
    (2,9): "meditation liberte conscience eau lumiere opacite discernement dogmatisme serpent communication",
    (2,10): "transformation sagesse souffrance joie amour pensee attention symboles grandeur accomplissement",
}
SENTINELS = {
    (1,21): {2: "guérison et une protection",12: "être qui souffre"},
    (1,22): {9: "cendre",13: "je vous consacre"},
    (2,1): {2: "3 mondes",7: "féconde l'homme"},
    (2,2): {8: "interprètes",10: "la plante"},
    (2,3): {2: "base fondamentale de la guérison",7: "non-communication"},
    (2,4): {6: "de pureté",8: "médite cet enseignement"},
    (2,5): {1: "chaîne magique",3: "la chaîne de la communauté"},
    (2,6): {1: "semblable à un arbre",4: "état intérieur de bonheur"},
    (2,7): {2: "des étoiles et des fées",10: "une lampe"},
    (2,8): {18: "La simplicité est une vertu",21: "baguette magique",37: "maîtrise"},
    (2,9): {8: "d'opacité",10: "principes dogmatiques"},
    (2,10): {2: "l'huître qui crée une perle",4: "en sagesse"},
}
NEW_THEMES = {
    "chaine-magique": "Chaîne magique",
    "nuit": "Nuit",
    "mystere": "Mystère",
    "partage": "Partage",
    "dogmatisme": "Dogmatisme",
}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c)).casefold()
    value = value.replace("œ", "oe").replace("æ", "ae")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

def terms(value):
    return set(value.split()) if value else set()

def main():
    books = {i: read(INDEX / f"books/book-{i:02d}.json") for i in (1,2)}
    directory = read(INDEX / "theme-directory.json")
    public = read(INDEX / "theme-directory-public.json")
    runtime = read(INDEX / "theme-search-runtime.json")
    d_by_id = {t["id"]: t for t in directory["themes"]}
    p_by_id = {t["id"]: t for t in public["themes"]}
    assert set(d_by_id)==set(p_by_id)
    assert len(d_by_id)==runtime["themeCount"]==public["themeCount"]==directory["themeCount"] and len(d_by_id)>=1265
    assert len(BASELINE)==len(ADDED)==len(SENTINELS)==12
    old_count = new_count = verse_count = 0

    for (bookno,num), baseline in BASELINE.items():
        psalm = next((p for p in books[bookno]["psalmAnalyses"] if p["number"]==num),None)
        src = read(CORPUS / f"book-{bookno:02d}" / f"psalm-{num:03d}.json")
        assert psalm is not None and psalm["recordId"]==src["id"] == f"book-{bookno:02d}-psalm-{num:03d}"
        assert psalm["title"]==src["title"]
        valid = {int(v["number"]):v["text"] for v in src["verses"]}
        verse_count += len(valid)
        for verse,needle in SENTINELS[(bookno,num)].items():
            assert norm(needle) in norm(valid[verse]), (bookno,num,verse,needle)

        historical=terms(baseline)
        additions=terms(ADDED[(bookno,num)])
        assert historical.isdisjoint(additions),(bookno,num,"duplicated relation")
        rels=psalm["themes"]
        by_id={t["themeId"]:t for t in rels}
        assert len(by_id)==len(rels),(bookno,num,"duplicate themeId")
        assert set(by_id)==historical|additions,(bookno,num,sorted(set(by_id)^(historical|additions)))
        old_count+=len(historical)
        new_count+=len(additions)
        for tid,rel in by_id.items():
            anchors=rel["verseNumbers"]
            assert anchors and all(v in valid for v in anchors),(bookno,num,tid,"invalid verse")
            assert rel["teaching"] and rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            if tid in additions:
                assert rel["teaching"].startswith("La Bible essénienne"),(bookno,num,tid)
            for theme_map in (d_by_id,p_by_id):
                occurrences=[o for o in theme_map[tid]["occurrences"] if o["recordId"]==src["id"]]
                assert len(occurrences)==1,(bookno,num,tid,"missing or duplicate public projection")
                for field in ("verseNumbers","importance","teaching"):
                    assert occurrences[0][field]==rel[field],(bookno,num,tid,field,"drift")

    assert verse_count==153,verse_count
    assert old_count==54,old_count
    assert new_count==130,new_count
    assert len(NEW_THEMES)==5
    for tid,label in NEW_THEMES.items():
        assert tid in d_by_id and tid in p_by_id
        entry=runtime["aliases"].get(norm(label))
        assert entry and tid in entry["themeIds"],(tid,label)
    assert "baguette-magique" in runtime["aliases"][norm("Baguette magique")]["themeIds"]
    ps8 = next(p for p in books[2]["psalmAnalyses"] if p["number"]==8)
    assert any(t["themeId"]=="baguette-magique" and 21 in t["verseNumbers"] for t in ps8["themes"])
    assert "conte" not in runtime["aliases"], "Do not mislabel Psalm 2/7 as a tale on lexical proximity"

    audits1 = books[1]["method"]["themeCoverageAudits"]
    audits2 = books[2]["method"]["themeCoverageAudits"]
    assert [a["scope"] for a in audits1]==[
        "book-01-psalms-001-010","book-01-psalms-011-020","book-01-psalms-021-022"
    ]
    assert audits1[2]["verifiedVerseCount"]==30 and audits1[2]["addedRelationCount"]==25
    assert audits2[0]["scope"]=="book-02-psalms-001-010"
    assert audits2[0]["verifiedVerseCount"]==123 and audits2[0]["addedRelationCount"]==105
    print("BIBLAW BOOK 01 FINISH + BOOK 02/1-10 PASS: 12 Psalms, 153 unchanged verses, 54 original + 130 new verse-anchored relations; 1265 themes, 5 new public search topics.")


if __name__=="__main__":
    main()
