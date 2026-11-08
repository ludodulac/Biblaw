#!/usr/bin/env python3
"""One-time editorial application for book 10 (Gabriel); canonical corpus remains immutable."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-10.json"
BASE=THEMATIC/"audits/book10-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-10"
PARTS=ROOT/"scripts/book10-work"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

book=load(BOOK)
assert book["book"]["number"]==10 and book["book"]["archangel"]=="gabriel"
psalms={p["number"]:p for p in book["psalmAnalyses"]}
assert sorted(psalms)==list(range(55,82)),sorted(psalms)
if not BASE.exists():
    frozen={str(n):{t["themeId"]:t for t in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len,frozen.values()))==55,"Unexpected historical relation count"
    save(BASE,{"book":10,"archangel":"gabriel","originalRelationCount":55,"psalms":frozen})
baseline=load(BASE)
assert baseline["originalRelationCount"]==55
for n,p in psalms.items():
    for tid,relation in baseline["psalms"][str(n)].items():
        assert next((x for x in p["themes"] if x["themeId"]==tid),None)==relation,("historical difference",n,tid)

valid_verses={}
verse_count=0
for n,p in psalms.items():
    source=load(CORPUS/f"psalm-{n:03d}.json")
    assert source["id"]==p["recordId"] and source["archangel"]=="gabriel"
    assert source["title"]==p["title"]
    refs={v["number"] for v in source["verses"]}
    assert refs==set(range(1,len(refs)+1)),n
    valid_verses[n]=refs
    verse_count+=len(refs)

files=sorted(PARTS.glob("part*.json"))
assert len(files)==3,[str(p) for p in files]
relation_count=0
for path in files:
    for n,theme_id,refs,label,teaching,directness,importance in load(path):
        assert n in psalms and set(refs)<=valid_verses[n],(n,theme_id,refs)
        assert refs and len(set(refs))==len(refs)
        assert label.strip() and len(teaching)>35
        assert not any(rel["themeId"]==theme_id for rel in psalms[n]["themes"]),(n,theme_id,"duplicate")
        psalms[n]["themes"].append({
            "themeId":theme_id,
            "label":label,
            "importance":importance,
            "directness":directness,
            "verseNumbers":refs,
            "teaching":"La Bible essénienne enseigne que "+teaching
        })
        relation_count+=1
assert relation_count==336,relation_count
book["method"].setdefault("themeCoverageAudits",[]).append({
    "scope":"book-10-psalms-055-081",
    "reviewedOn":"2026-11-08",
    "source":"data/corpus/books/book-10/psalm-055.json through psalm-081.json",
    "approach":"conservative-editorial-verse-evidence",
    "originalRelationCount":55,
    "addedRelationCount":relation_count,
    "verifiedVerseCount":verse_count,
    "sourcePsalmsModified":False
})
book["bookSynthesis"]["centralAxis"]="Synthèse descriptive et non exclusive : le livre 10 de Gabriel invite à renouer avec la Source et la Mère, purifier les paroles et les actes, accueillir la paix du voile bleu, vivre la bonté et la générosité, donner un corps aux engagements, achever les œuvres commencées et porter ensemble la bénédiction et la sanctification."
book["bookSynthesis"]["majorThemes"]=["source","mere","eau","conscience","reconciliation-des-mondes","priere","parole","engagement","purete","paix","bonte","generosite","amour","sagesse","actes","responsabilite","legerete","bapteme","quatre-sceaux","nation-essenienne"]
save(BOOK,book)
print(f"BOOK10 EDITORIAL: 27 psalms, {verse_count} verses, 55 historical preserved, {relation_count} added, {55+relation_count} total")
