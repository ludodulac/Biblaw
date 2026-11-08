#!/usr/bin/env python3
"""Livre 13 Michaël : applique des liens thématiques étayés par les versets sans modifier le corpus."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
THEMATIC = ROOT / "data/thematic-index"
BOOK = THEMATIC / "books/book-13.json"
BASE = THEMATIC / "audits/book13-original-relations.json"
CORPUS = ROOT / "data/corpus/books/book-13"
PARTS = ROOT / "scripts/book13-work"
NUMBERS = range(77, 105)
HISTORICAL = 86
ADDED = 319

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

book = load(BOOK)
assert book["book"]["number"] == 13 and book["book"]["archangel"] == "michael"
psalms = {p["number"]: p for p in book["psalmAnalyses"]}
assert sorted(psalms) == list(NUMBERS)
if not BASE.exists():
    baseline = {str(n): {rel["themeId"]: rel for rel in p["themes"]} for n,p in psalms.items()}
    assert sum(map(len, baseline.values())) == HISTORICAL
    save(BASE, {"book": 13, "archangel": "michael",
                "originalRelationCount": HISTORICAL, "psalms": baseline})
original = load(BASE)
assert original["originalRelationCount"] == HISTORICAL
for n,p in psalms.items():
    frozen = original["psalms"][str(n)]
    assert len(p["themes"]) == len(frozen), (n,"book already enriched")
    for tid,old in frozen.items():
        assert next((rel for rel in p["themes"] if rel["themeId"] == tid),None) == old, (n,tid,"historical changed")

verse_refs = {}
verse_total = 0
for n,p in psalms.items():
    src=load(CORPUS / f"psalm-{n:03d}.json")
    assert src["id"] == p["recordId"]
    assert src["title"] == p["title"]
    assert src["archangel"] == "michael"
    valid={v["number"] for v in src["verses"]}
    assert valid == set(range(1,len(valid)+1)),n
    verse_total += len(valid)
    verse_refs[n] = valid

part_files = sorted(PARTS.glob("part*.json"))
assert len(part_files)==3,part_files
new_count=0
for part in part_files:
    for n,tid,refs,label,teaching,directness,importance in load(part):
        assert n in psalms and refs and len(refs)==len(set(refs))
        assert set(refs) <= verse_refs[n],(n,tid,refs)
        assert label and len(teaching)>20
        assert not any(rel["themeId"]==tid for rel in psalms[n]["themes"]),(n,tid,"duplicate")
        psalms[n]["themes"].append({
            "themeId":tid,"label":label,"importance":importance,
            "directness":directness,"verseNumbers":refs,
            "teaching":"La Bible essénienne enseigne que "+teaching
        })
        new_count+=1
assert new_count==ADDED,new_count
book["method"].setdefault("themeCoverageAudits",[]).append({
    "scope":"book-13-psalms-077-104",
    "reviewedOn":"2026-11-08",
    "source":"data/corpus/books/book-13/psalm-077.json through psalm-104.json",
    "approach":"conservative-editorial-verse-evidence",
    "originalRelationCount":HISTORICAL,
    "addedRelationCount":ADDED,
    "verifiedVerseCount":verse_total,
    "sourcePsalmsModified":False
})
book["bookSynthesis"]["centralAxis"]=(
    "Synthèse d'indexation descriptive et non exclusive : le livre 13 de l'Archange "
    "Michaël, « Le lien avec les Anges », enseigne une relation vivante et respectueuse "
    "avec les Anges, l'authenticité de l'engagement, le discernement des mondes et des "
    "influences, l'éveil de la conscience, la purification de la pensée, le travail "
    "sur la peur et sur l'orgueil, la continuité entre prière, parole et actes, "
    "le respect des règnes, la réalisation d'une œuvre commune, la fidélité à la "
    "Ronde des Archanges et la préservation de la flamme."
)
book["bookSynthesis"]["majorThemes"]=[
    "anges","alliance-angelique","vertus-angeliques","conscience",
    "discernement","respect","purete","authenticite","engagement",
    "coherence-interieure","pensee","priere","parole-donnee",
    "feu","flamme","temple","ronde-des-archanges","fidelite",
    "fraternite","union","soutien-mutuel","oeuvre","nature-vivante",
    "regnes","mere","usurpateur","peur","orgueil","justice",
    "sagesse-vecue","legerete","eternite","service-du-monde-divin"
]
save(BOOK,book)
print(f"BOOK13 EDITORIAL: 28 psalms, {verse_total} verses, {HISTORICAL} historical unchanged, {ADDED} new, {HISTORICAL+ADDED} total")
