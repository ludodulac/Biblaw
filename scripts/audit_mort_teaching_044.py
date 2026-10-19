#!/usr/bin/env python3
"""Read-only evidence export for the first 20 Mort results in BIBLAW's UI ordering."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/"evidence-044-mort-top20.json"
records={}
for f in sorted((ROOT/"data/thematic-index/books").glob("book-*.json")):
    d=json.loads(f.read_text(encoding="utf-8"))
    for p in d.get("psalmAnalyses",[]):
        for t in p.get("themes",[]):
            if t.get("themeId")=="mort":
                records[p["recordId"]]={"recordId":p["recordId"],"book":d["book"]["number"],"archangel":d["book"]["archangel"],"psalm":p["number"],"title":p["title"],"importance":t["importance"],"score":t.get("score",1),"indexedVerses":t["verseNumbers"],"editorialTeaching":t["teaching"]}
rank={"central":0,"important":1,"related":2}
ordered=sorted(records.values(),key=lambda p:(rank.get(p["importance"],3),p["psalm"],p["recordId"]))
if len(ordered)!=161:raise RuntimeError(f"Expected 161 indexed Mort psalms, got {len(ordered)}")
for p in ordered[:20]:
    f=ROOT/"data/corpus/books"/f'book-{p["book"]:02d}'/f'psalm-{p["psalm"]:03d}.json'
    corpus=json.loads(f.read_text(encoding="utf-8"))
    if corpus["id"]!=p["recordId"]:raise RuntimeError("canonical record mismatch")
    nums=set(p["indexedVerses"])
    p["indexedVerseTexts"]=[{"number":v["number"],"text":v["text"]} for v in corpus["verses"] if v["number"] in nums]
    if len(p["indexedVerseTexts"])!=len(nums):raise RuntimeError("missing verse")
    p["allVerses"]=[{"number":v["number"],"text":v["text"]} for v in corpus["verses"]]
    p["relevanceCategory"]="UNREVIEWED"
    p["question"]="Que devient l'homme après la mort ?"
    p["note"]="Mort theme relevance does not imply after-death answer; human review required."
data={"mission":"BIBLAW-044","question":"Que devient l'homme après la mort ?","sorting":"importance central/important/related, then psalm number, then record id, matching js/biblaw.js thematicItems","indexedMortPsalms":len(ordered),"first20":ordered[:20]}
out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"indexedMortPsalms":len(ordered),"first20":[{"id":p["recordId"],"importance":p["importance"],"verses":p["indexedVerses"]} for p in ordered[:20]]},ensure_ascii=False))
