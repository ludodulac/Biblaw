#!/usr/bin/env python3
"""Livre 17 Michaël : enrichir le repérage thématique sans altérer les textes du corpus."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"data/thematic-index"
BOOK=INDEX/"books/book-17.json"
BASELINE=INDEX/"audits/book17-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-17"
PARTS=ROOT/"scripts/book17-work"
NUMBERS=range(105,131)
HISTORICAL=83
ADDED=301

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

book=load(BOOK)
assert book["book"]["number"]==17 and book["book"]["archangel"]=="michael"
psalms={p["number"]:p for p in book["psalmAnalyses"]}
assert sorted(psalms)==list(NUMBERS)
if not BASELINE.exists():
    originals={str(n):{rel["themeId"]:rel for rel in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len,originals.values()))==HISTORICAL
    save(BASELINE,{"book":17,"archangel":"michael","originalRelationCount":HISTORICAL,"psalms":originals})
original=load(BASELINE)
assert original["book"]==17 and original["archangel"]=="michael"
assert original["originalRelationCount"]==HISTORICAL
for n,p in psalms.items():
    historical=original["psalms"][str(n)]
    assert len(p["themes"])==len(historical),(n,"previously enriched")
    for tid,rel in historical.items():
        assert next((x for x in p["themes"] if x["themeId"]==tid),None)==rel,(n,tid,"original changed")

valid={}
total_verses=0
nonstandard=[]
for n,p in psalms.items():
    src=load(CORPUS/f"psalm-{n:03d}.json")
    assert src["id"]==p["recordId"] and src["title"]==p["title"],n
    assert src["archangel"]=="michael",n
    numbers=[v["number"] for v in src["verses"]]
    assert numbers and numbers==sorted(numbers) and len(numbers)==len(set(numbers)),n
    if numbers!=list(range(1,len(numbers)+1)):
        nonstandard.append([n,numbers[0],numbers[-1]])
    valid[n]=set(numbers)
    total_verses+=len(numbers)
assert total_verses==821,(total_verses,"corpus verse count")
assert not nonstandard,nonstandard
canonical={t["themeId"]:t["canonicalLabel"] for t in load(INDEX/"theme-search-index.json")["themes"]}
parts=sorted(PARTS.glob("part*.json"))
assert [p.name for p in parts]==["part1.json","part2.json","part3.json"]
added=0
for part in parts:
    for n,tid,refs,label,teaching,directness,importance in load(part):
        assert n in psalms and tid in canonical,(n,tid,"noncanonical")
        assert label==canonical[tid],(n,tid,"incorrect label")
        assert refs and len(refs)==len(set(refs)) and set(refs)<=valid[n],(n,tid,refs)
        assert len(teaching)>20 and isinstance(teaching,str),(n,tid,"missing teaching")
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
    "scope":"book-17-psalms-105-130",
    "reviewedOn":"2026-11-09",
    "source":"data/corpus/books/book-17/psalm-105.json through psalm-130.json",
    "approach":"conservative-editorial-verse-evidence",
    "originalRelationCount":HISTORICAL,
    "addedRelationCount":ADDED,
    "verifiedVerseCount":total_verses,
    "sourcePsalmsModified":False,
    "sourceVerseNumberingNotes":nonstandard
})
book["bookSynthesis"]["centralAxis"]=(
    "Synthèse d'indexation descriptive et non exclusive : le livre 17 de Michaël, "
    "« L'heure du choix », développe la fidélité et la renaissance de l'âme, le "
    "discernement de l'authenticité face aux apparences artificielles, la relation "
    "au Père et à la Mère et la responsabilité envers les règnes, la stabilité "
    "de la tradition et l'équilibre des trois intelligences, l'enseignement des "
    "fruits mûrs et de la flamme sacrée, la vérité incarnée plutôt qu'une pureté "
    "proclamée, la mémoire des ancêtres et l'arbre de Vie, la royauté généreuse "
    "au service du Bien commun, la formation du corps céleste par les œuvres, "
    "la constance face à la technologie, la construction des quatre cultes et "
    "des quatre Sceaux, la pratique vivante de l'Enseignement, les exigences "
    "d'une alliance pure avec le monde divin, le cercle de la Ronde des Archanges, "
    "le choix conscient de conserver son âme, la terre vivante de la Mère, "
    "la distinction du vrai et de son imitation, la conscience comme flamme "
    "perpétuelle, le rôle d'intermédiaire entre les mondes, la dénonciation de "
    "la cruauté envers les règnes, les Évangiles esséniens vécus au quotidien, "
    "la légèreté et l'ouverture de la porte du culte du feu."
)
book["bookSynthesis"]["majorThemes"]=[
    "fidelite","renaissance","connaissance-de-soi","authenticite","discernement",
    "monde-artificiel","vigilance","pere-et-mere","interdependance","regnes",
    "responsabilite-envers-les-regnes","stabilite","tradition-de-la-lumiere",
    "equilibre-des-mondes","trois-intelligences","nutrition","fruit",
    "flamme-sacree","verite","coherence-interieure","enracinement","ancetres",
    "arbre-de-la-vie","generosite","bien-commun","corps-celeste","eternite",
    "constance","technologie","quatre-cultes","quatre-sceaux","sagesse-vecue",
    "vie-interieure","receptivite","ronde-des-archanges","choix","ame",
    "mere","terre-consacree","imitation","flamme-de-la-conscience",
    "intermediaire-des-mondes","pardon-et-reparation","evangiles-esseniens",
    "legerete","culte-du-feu","liberation-des-regnes"
]
assert all(tid in canonical for tid in book["bookSynthesis"]["majorThemes"])
save(BOOK,book)
print(f"BOOK17 EDITORIAL: {len(psalms)} psalms, {total_verses} verses, {HISTORICAL} historical unchanged, {ADDED} added, {HISTORICAL+ADDED} total")
