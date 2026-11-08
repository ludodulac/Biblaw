#!/usr/bin/env python3
"""Livre 15 de Raphaël : appliquer les liens éditoriaux sourcés sans altérer les psaumes."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-15.json"
BASE=THEMATIC/"audits/book15-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-15"
PARTS=ROOT/"scripts/book15-work"
HISTORICAL=84
ADDED=310
NUMBERS=range(75,102)

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

book=load(BOOK)
assert book["book"]["number"]==15 and book["book"]["archangel"]=="raphael"
psalms={p["number"]:p for p in book["psalmAnalyses"]}
assert sorted(psalms)==list(NUMBERS)
if not BASE.exists():
    frozen={str(n):{rel["themeId"]:rel for rel in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len,frozen.values()))==HISTORICAL
    save(BASE,{"book":15,"archangel":"raphael","originalRelationCount":HISTORICAL,"psalms":frozen})
baseline=load(BASE)
assert baseline["originalRelationCount"]==HISTORICAL
for n,p in psalms.items():
    original=baseline["psalms"][str(n)]
    assert len(p["themes"])==len(original),(n,"unexpected preexisting enrichment")
    for tid,rel in original.items():
        assert next((x for x in p["themes"] if x["themeId"]==tid),None)==rel,(n,tid,"historical modified")

valid_verses={}
verse_total=0
non_standard_ranges=[]
for n,p in psalms.items():
    src=load(CORPUS/f"psalm-{n:03d}.json")
    assert src["id"]==p["recordId"],(n,"record")
    assert src["title"]==p["title"],(n,"title")
    assert src["archangel"]=="raphael",(n,"archangel")
    nums=[v["number"] for v in src["verses"]]
    assert nums and len(nums)==len(set(nums)) and nums==sorted(nums),(n,"duplicate or disordered verse")
    # Le psaume 75 commence au verset 15 dans le corpus : conserver cette numérotation.
    if nums!=list(range(1,len(nums)+1)):
        non_standard_ranges.append([n,nums[0],nums[-1]])
    valid_verses[n]=set(nums)
    verse_total+=len(nums)

canonical={t["themeId"]:t["canonicalLabel"] for t in load(THEMATIC/"theme-search-index.json")["themes"]}
parts=sorted(PARTS.glob("part*.json"))
assert len(parts)==3,parts
added=0
for part in parts:
    for n,tid,refs,label,teaching,directness,importance in load(part):
        assert n in psalms and tid in canonical,(n,tid,"invalid canonical theme")
        assert label==canonical[tid],(n,tid,"label")
        assert refs and len(refs)==len(set(refs)) and set(refs)<=valid_verses[n],(n,tid,refs)
        assert isinstance(teaching,str) and len(teaching)>20
        assert directness in {"direct","symbolic","editorial","indirect","contextual"}
        assert importance in {"central","important","related"}
        assert not any(t["themeId"]==tid for t in psalms[n]["themes"]),(n,tid,"duplicate")
        psalms[n]["themes"].append({
            "themeId":tid,"label":label,"importance":importance,
            "directness":directness,"verseNumbers":refs,
            "teaching":"La Bible essénienne enseigne que "+teaching
        })
        added+=1
assert added==ADDED,added
book["method"].setdefault("themeCoverageAudits",[]).append({
    "scope":"book-15-psalms-075-101",
    "reviewedOn":"2026-11-08",
    "source":"data/corpus/books/book-15/psalm-075.json through psalm-101.json",
    "approach":"conservative-editorial-verse-evidence",
    "originalRelationCount":HISTORICAL,
    "addedRelationCount":ADDED,
    "verifiedVerseCount":verse_total,
    "sourcePsalmsModified":False,
    "sourceVerseNumberingNotes":non_standard_ranges
})
book["bookSynthesis"]["centralAxis"]=(
    "Synthèse d'indexation descriptive et non exclusive : le livre 15 de Raphaël, "
    "« Prends ta vie en mains », invite à reconnaître la Lumière aux œuvres et non aux "
    "apparences, à vivre la vérité par des actes, à préserver la mémoire du divin "
    "figurée par la pierre verte, à construire une grandeur d'âme et un corps conscient, "
    "à tenir les engagements jusqu'à leur aboutissement, à cultiver la stabilité de "
    "l'arbre qui accueille l'oiseau et les pensées qui guérissent auprès de la forêt "
    "et des sylphes, à maîtriser ses pensées, à unir fraternité et œuvre commune, "
    "à rendre l'invisible vivant, à changer de monde par le voyage intérieur, à "
    "accueillir la Lumière dans un temple d'harmonie, à retrouver la mémoire des "
    "facultés supérieures, à devenir un panier réceptif aux fruits, à agir dans "
    "la générosité, à ne porter que l'essentiel figuré par l'escargot, "
    "à vivre ensemble dans les Villages Esséniens et à contempler la marguerite de Raphaël."
)
book["bookSynthesis"]["majorThemes"]=[
    "oeuvre","lumiere","realisme","illusion","verite","actes",
    "pierre-verte","memoire","protection-du-divin","grandeur-d-ame",
    "consecration","nature","maitre","soutien-mutuel","conscience",
    "corps-d-immortalite","oiseau","arbre","stabilite","guerison","sylphes",
    "foret","pensee","lois-de-la-pensee","coherence-interieure",
    "symboles-esseniens","pere-et-mere","forme-et-essence",
    "union","fraternite","pensee-creatrice","voyage-interieur",
    "harmonie","receptivite","generosite","don-de-soi","detachement",
    "escargot","villages-esseniens","marguerite","fleur","ronde-des-archanges"
]
assert all(t in canonical for t in book["bookSynthesis"]["majorThemes"])
save(BOOK,book)
print(f"BOOK15 EDITORIAL: {len(psalms)} psalms, {verse_total} verses, {HISTORICAL} historic links unchanged, {ADDED} new, {HISTORICAL+ADDED} total; non-standard numbering: {non_standard_ranges}")
