#!/usr/bin/env python3
"""Livre 13 (Michaël), psaumes 77–104 : conservation des relations et preuves verset par verset."""
from __future__ import annotations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-13.json"
BASELINE=THEMATIC/"audits/book13-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-13"
NUMBERS=set(range(77,105))
HISTORICAL=86
ADDED=319

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book=load(BOOK)
    original=load(BASELINE)
    assert book["book"]["number"]==13
    assert book["book"]["archangel"]=="michael"
    assert original["archangel"]=="michael" and original["originalRelationCount"]==HISTORICAL
    assert len(book["psalmAnalyses"])==len(NUMBERS)
    audit=book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"]=="book-13-psalms-077-104"
    assert audit["originalRelationCount"]==HISTORICAL and audit["addedRelationCount"]==ADDED
    assert audit["sourcePsalmsModified"] is False
    totals={"psalms":0,"verses":0,"historical":0,"added":0}
    seen_psalms=set()
    for p in book["psalmAnalyses"]:
        n=p["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==p["recordId"]
        assert src["archangel"]=="michael"
        assert src["title"]==p["title"]
        valid={v["number"] for v in src["verses"]}
        assert valid==set(range(1,len(valid)+1)),(n,"missing verses")
        totals["psalms"]+=1
        totals["verses"]+=len(valid)
        historical=original["psalms"][str(n)]
        seen_themes=set()
        for rel in p["themes"]:
            tid=rel["themeId"]
            assert tid not in seen_themes,(n,tid,"duplicate")
            seen_themes.add(tid)
            assert rel["label"].strip()
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,refs)
            if tid in historical:
                assert rel==historical[tid],(n,tid,"historical relation changed")
                totals["historical"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid)
                assert len(rel["teaching"])>65,(n,tid,"teaching too short")
                totals["added"]+=1
        assert set(historical).issubset(seen_themes),(n,"historical links lost")
    assert seen_psalms==NUMBERS
    assert totals["historical"]==HISTORICAL,totals
    assert totals["added"]==ADDED,totals
    assert totals["verses"]==audit["verifiedVerseCount"],totals
    print(f"BOOK13 PASS: {totals['psalms']} psalms (77–104), {totals['verses']} verses, "
          f"{HISTORICAL} historical unchanged, {ADDED} added, {HISTORICAL+ADDED} total")

if __name__=="__main__":
    main()
