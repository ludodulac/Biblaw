#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from build_linguistic_user_confirmed_gold import ROOT, build, render
GOLD_DIR=ROOT/"data/linguistic/gold";GLOB="*-sense-gold.json"
SEMANTIC=ROOT/"data/linguistic-sense-runtime.json";BROWSER=ROOT/"data/linguistic-sense-browser-runtime.json"
def load(path):
    with Path(path).open(encoding="utf-8") as h:return json.load(h)
def key(target):return (target["normalizedForm"],target["lemma"],target["partOfSpeech"])
def main():
    semantic=load(SEMANTIC);browser=load(BROWSER)
    smap={key(t):t for t in semantic["targets"]};bmap={key(t):t for t in browser["targets"]}; discovered=0
    for path in sorted(GOLD_DIR.glob(GLOB)):
        gold=load(path);p=gold.get("provenance",{})
        if p.get("validationType")!="user-confirmed":continue
        discovered+=1;source=p["sourceReview"];rebuilt=render(build(ROOT/source,p["reviewMission"],p["confirmationMission"]))
        assert rebuilt==path.read_bytes(),f"{path}: gold reconstruction differs"
        k=key(gold["target"]);assert k in smap,f"{path}: missing semantic runtime target";assert k in bmap,f"{path}: missing browser runtime target"
        st=smap[k];bt=bmap[k];validated=[e for e in gold["entries"] if e["adjudicationStatus"]=="VALIDATED"];uncertain=[e for e in gold["entries"] if e["adjudicationStatus"]=="UNCERTAIN"]
        assert len(st["validated"])==len(validated);assert len(st["uncertain"])==len(uncertain)
        expected={s["senseId"]:0 for s in st["senses"]}
        for e in validated:expected[e["senseId"]]+=1
        actual={s["senseId"]:s["occurrenceCount"] for s in bt["senses"]}
        assert actual==expected,f"{path}: browser sense counts differ";assert bt["uncertainOccurrenceCount"]==len(uncertain)
        assert gold["counts"]=={**expected,"UNCERTAIN":len(uncertain)},f"{path}: gold counts differ"
    assert discovered>0,"no user-confirmed semantic gold found"
    print(f"PASS userConfirmedGolds={discovered}")
if __name__=="__main__":main()
