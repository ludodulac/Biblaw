#!/usr/bin/env python3
"""Livre 16 Ouriel : enrichissement thématique fondé sur les versets, sans altération du corpus."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-16.json"
BASELINE=THEMATIC/"audits/book16-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-16"
PARTS=ROOT/"scripts/book16-work"
NUMBERS=range(78,104)
HISTORICAL=79
ADDED=303

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

book=load(BOOK)
assert book["book"]["number"]==16 and book["book"]["archangel"]=="ouriel"
psalms={p["number"]:p for p in book["psalmAnalyses"]}
assert sorted(psalms)==list(NUMBERS)
if not BASELINE.exists():
    frozen={str(n):{rel["themeId"]:rel for rel in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len,frozen.values()))==HISTORICAL
    save(BASELINE,{"book":16,"archangel":"ouriel","originalRelationCount":HISTORICAL,"psalms":frozen})
original=load(BASELINE)
assert original["originalRelationCount"]==HISTORICAL and original["archangel"]=="ouriel"
for n,p in psalms.items():
    frozen=original["psalms"][str(n)]
    assert len(p["themes"])==len(frozen),(n,"unexpected preexisting enrichment")
    for tid,rel in frozen.items():
        assert next((x for x in p["themes"] if x["themeId"]==tid),None)==rel,(n,tid,"historical modified")

verse_map={}
verse_total=0
nonstandard=[]
for n,p in psalms.items():
    src=load(CORPUS/f"psalm-{n:03d}.json")
    assert src["id"]==p["recordId"] and src["title"]==p["title"],n
    assert src["archangel"]=="ouriel",n
    nums=[v["number"] for v in src["verses"]]
    assert nums and len(nums)==len(set(nums)) and nums==sorted(nums),n
    if nums!=list(range(1,len(nums)+1)):
        nonstandard.append([n,nums[0],nums[-1]])
    verse_map[n]=set(nums)
    verse_total+=len(nums)

canonical={t["themeId"]:t["canonicalLabel"] for t in load(THEMATIC/"theme-search-index.json")["themes"]}
parts=sorted(PARTS.glob("part*.json"))
assert len(parts)==3,parts
added=0
for part in parts:
    for n,tid,refs,label,teaching,directness,importance in load(part):
        assert n in psalms and tid in canonical,(n,tid,"unknown theme")
        assert label==canonical[tid],(n,tid,"canonical label")
        assert refs and len(refs)==len(set(refs)) and set(refs)<=verse_map[n],(n,tid,"invalid verse refs")
        assert isinstance(teaching,str) and len(teaching)>20,(n,tid,"missing explanation")
        assert directness in {"direct","symbolic","editorial","indirect","contextual"}
        assert importance in {"central","important","related"}
        assert not any(x["themeId"]==tid for x in psalms[n]["themes"]),(n,tid,"duplicate")
        psalms[n]["themes"].append({
            "themeId":tid,"label":label,"importance":importance,
            "directness":directness,"verseNumbers":refs,
            "teaching":"La Bible essénienne enseigne que "+teaching
        })
        added+=1
assert added==ADDED,added
book["method"].setdefault("themeCoverageAudits",[]).append({
    "scope":"book-16-psalms-078-103",
    "reviewedOn":"2026-11-08",
    "source":"data/corpus/books/book-16/psalm-078.json through psalm-103.json",
    "approach":"conservative-editorial-verse-evidence",
    "originalRelationCount":HISTORICAL,
    "addedRelationCount":ADDED,
    "verifiedVerseCount":verse_total,
    "sourcePsalmsModified":False,
    "sourceVerseNumberingNotes":nonstandard
})
book["bookSynthesis"]["centralAxis"]=(
    "Synthèse d'indexation descriptive et non exclusive : le livre 16 d'Ouriel, "
    "« Ouvrez les portes d'un autre futur », relie l'authenticité des actes à la pureté "
    "des pensées, la vérité vécue à la royauté intérieure, la sublimation des influences "
    "à la méditation et à la légèreté, la mission collective à la fraternité et au "
    "respect des règnes, la mise en ordre des deux mondes à la paix intérieure, "
    "l'édification d'une terre et d'une civilisation nouvelles à l'engagement concret, "
    "la fidélité éprouvée au passage d'un cycle, la coupe de sagesse à son assimilation "
    "vivante, la guérison du regard à la fleur et aux règnes de la Mère, "
    "l'abondance au soin des dons déjà reçus, la recherche de Dieu à l'incarnation "
    "dans la vie, la décision au temps présent, le discernement au refus des illusions, "
    "le pardon et la réparation à l'ouverture d'un chemin, le dauphin à un modèle "
    "d'harmonie et de langage, et le passage de la porte à l'allègement de l'être."
)
book["bookSynthesis"]["majorThemes"]=[
    "coherence-interieure","purete","verite","stabilite","royaute","maitre",
    "alchimie-interieure","sublimation","meditation","concentration","legerete",
    "ame-collective","nation-essenienne","union","respect-des-regnes",
    "ordre","discernement","detente","paix","eau","futur","terre-essenienne",
    "oeuvre-collective","epreuve","fidelite","ronde-des-archanges","coupe",
    "sagesse-vecue","regard","interdependance","fleur","lois-de-la-subtilite",
    "nouvelle-civilisation","abondance","fructification","incarnation-du-divin",
    "present","decision","actes","intention","terre-consacree",
    "discernement-magique","pardon-et-reparation","dauphin","langage-universel",
    "passage-de-la-porte","preparation"
]
assert all(t in canonical for t in book["bookSynthesis"]["majorThemes"])
save(BOOK,book)
print(f"BOOK16 EDITORIAL: {len(psalms)} psalms, {verse_total} verses, {HISTORICAL} historical untouched, {ADDED} new, {HISTORICAL+ADDED} total; special numbering: {nonstandard}")
