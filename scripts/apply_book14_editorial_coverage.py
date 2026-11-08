#!/usr/bin/env python3
"""Livre 14 de Gabriel : enrichissement thématique précis sans altération du corpus source."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-14.json"
BASELINE=THEMATIC/"audits/book14-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-14"
PARTS=ROOT/"scripts/book14-work"
HISTORICAL=88
ADDED=330
NUMBERS=range(82,111)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

book=load(BOOK)
assert book["book"]["number"]==14 and book["book"]["archangel"]=="gabriel"
psalms={p["number"]:p for p in book["psalmAnalyses"]}
assert sorted(psalms)==list(NUMBERS)
if not BASELINE.exists():
    original={str(n):{t["themeId"]:t for t in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len,original.values()))==HISTORICAL
    save(BASELINE,{"book":14,"archangel":"gabriel","originalRelationCount":HISTORICAL,"psalms":original})
frozen=load(BASELINE)
assert frozen["originalRelationCount"]==HISTORICAL and frozen["archangel"]=="gabriel"
for n,p in psalms.items():
    old=frozen["psalms"][str(n)]
    assert len(p["themes"])==len(old),(n,"already enriched")
    for tid,relation in old.items():
        assert next((x for x in p["themes"] if x["themeId"]==tid),None)==relation,(n,tid,"historical changed")
verses={}
verse_total=0
for n,p in psalms.items():
    src=load(CORPUS/f"psalm-{n:03d}.json")
    assert src["id"]==p["recordId"] and src["title"]==p["title"]
    assert src["archangel"]=="gabriel"
    valid={v["number"] for v in src["verses"]}
    assert valid==set(range(1,len(valid)+1)),n
    verses[n]=valid
    verse_total+=len(valid)
canonical={t["themeId"]:t["canonicalLabel"] for t in load(THEMATIC/"theme-search-index.json")["themes"]}
parts=sorted(PARTS.glob("part*.json"))
assert len(parts)==3,parts
added=0
for file in parts:
    for n,tid,refs,label,teaching,directness,importance in load(file):
        assert n in psalms and tid in canonical,(n,tid,"unknown")
        assert label==canonical[tid],(n,tid,"canonical label changed")
        assert refs and len(refs)==len(set(refs)) and set(refs)<=verses[n],(n,tid,"invalid references")
        assert len(teaching)>20 and isinstance(teaching,str)
        assert directness in {"direct","symbolic","editorial","indirect","contextual"}
        assert importance in {"central","important","related"}
        assert not any(t["themeId"]==tid for t in psalms[n]["themes"]),(n,tid,"duplicate")
        psalms[n]["themes"].append({
          "themeId":tid,
          "label":label,
          "importance":importance,
          "directness":directness,
          "verseNumbers":refs,
          "teaching":"La Bible essénienne enseigne que "+teaching
        })
        added+=1
assert added==ADDED,added
book["method"].setdefault("themeCoverageAudits",[]).append({
  "scope":"book-14-psalms-082-110",
  "reviewedOn":"2026-11-08",
  "source":"data/corpus/books/book-14/psalm-082.json through psalm-110.json",
  "approach":"conservative-editorial-verse-evidence",
  "originalRelationCount":HISTORICAL,
  "addedRelationCount":ADDED,
  "verifiedVerseCount":verse_total,
  "sourcePsalmsModified":False
})
book["bookSynthesis"]["centralAxis"]=(
  "Synthèse d'indexation descriptive et non exclusive : le livre 14 de Gabriel, "
  "« La maîtrise du corps », développe l'éveil à l'eau qui unit les êtres, la responsabilité "
  "des pensées et des relations, la construction d'un corps intérieur, la maîtrise du corps, "
  "le savoir rendu vivant par les actes, la tradition et l'œuvre collective, le regard de Gabriel, "
  "le tissage des relations, l'assimilation et le choix d'une communauté, la préparation et la "
  "discipline, les pièges de la clairvoyance, le serpent de la sagesse, le service discret, "
  "la famille, le nénuphar et le message de la Biche."
)
book["bookSynthesis"]["majorThemes"]=[
  "eau","interdependance","conscience","corps","corps-interieur","maitrise-de-soi",
  "meditation","discipline","preparation","savoir-vivant","anges","oeuvre",
  "union","corps-collectif","tradition","tissage-des-relations","guerison-des-relations",
  "regard","nature-vivante","fleur","responsabilite","purete","assimilation",
  "individualite-consciente","quatre-sceaux","clairvoyance","discernement",
  "serpent-de-la-sagesse","serpent-de-la-destruction","nenuphar","biche",
  "famille","soutien-mutuel","nation-essenienne","ronde-des-archanges",
  "oeuvre-commune","respect-des-regnes"
]
assert all(t in canonical for t in book["bookSynthesis"]["majorThemes"])
save(BOOK,book)
print(f"BOOK14 EDITORIAL: {len(psalms)} psalms, {verse_total} verses, {HISTORICAL} historical unchanged, {ADDED} added, {HISTORICAL+ADDED} total")
