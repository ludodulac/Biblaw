#!/usr/bin/env python3
"""Livre 12 (Ouriel), psaumes 52 à 77 : contrôle des versets et des relations historiques."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-12.json"
BASELINE=THEMATIC/"audits/book12-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-12"
NUMBERS=set(range(52,78))
HISTORICAL=79
ADDED=314

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    current=load(BOOK)
    baseline=load(BASELINE)
    assert current["book"]["number"]==12
    assert current["book"]["archangel"]=="ouriel"
    assert baseline["originalRelationCount"]==HISTORICAL
    assert baseline["archangel"]=="ouriel"
    assert len(current["psalmAnalyses"])==len(NUMBERS)
    audit=current["method"]["themeCoverageAudits"][-1]
    assert audit["scope"]=="book-12-psalms-052-077"
    assert audit["originalRelationCount"]==HISTORICAL
    assert audit["addedRelationCount"]==ADDED
    assert audit["sourcePsalmsModified"] is False
    counts={"historical":0,"added":0,"verses":0}
    seen_psalms=set()
    for p in current["psalmAnalyses"]:
        n=p["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==p["recordId"]
        assert src["archangel"]=="ouriel"
        assert src["title"]==p["title"]
        valid={v["number"] for v in src["verses"]}
        assert valid==set(range(1,len(valid)+1)),(n,"verses")
        counts["verses"]+=len(valid)
        historical=baseline["psalms"][str(n)]
        seen_themes=set()
        for relation in p["themes"]:
            tid=relation["themeId"]
            assert tid not in seen_themes,(n,tid,"duplicate")
            seen_themes.add(tid)
            assert relation["label"].strip(),(n,tid)
            assert relation["importance"] in {"central","important","related"}
            assert relation["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=relation["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,"invalid verses",refs)
            if tid in historical:
                assert relation==historical[tid],(n,tid,"historical change")
                counts["historical"]+=1
            else:
                assert relation["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"attribution")
                assert len(relation["teaching"])>65,(n,tid,"insufficient teaching")
                counts["added"]+=1
        assert set(historical).issubset(seen_themes),(n,"historical theme missing")
    assert seen_psalms==NUMBERS
    assert counts["historical"]==HISTORICAL,counts
    assert counts["added"]==ADDED,counts
    assert counts["verses"]==audit["verifiedVerseCount"],counts
    print(f"BOOK12 PASS: 26 psalms (52–77), {counts['verses']} verses, "
          f"{HISTORICAL} historical unchanged, {ADDED} added, {HISTORICAL+ADDED} total.")

if __name__=="__main__":
    main()
