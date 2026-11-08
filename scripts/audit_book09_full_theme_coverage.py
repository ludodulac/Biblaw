#!/usr/bin/env python3
"""Book 9 (Michaël), psalms 48–76: verse-grounded coverage and historical preservation audit."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
THEMATIC=ROOT/"data/thematic-index"
BOOK=THEMATIC/"books/book-09.json"
BASELINE=THEMATIC/"audits/book09-original-relations.json"
CORPUS=ROOT/"data/corpus/books/book-09"
NUMBERS=set(range(48,77))
HISTORICAL=82
ADDED=274

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    current=load(BOOK);frozen=load(BASELINE)
    assert current["book"]["number"]==9
    assert current["book"]["archangel"]=="michael"
    assert frozen["originalRelationCount"]==HISTORICAL
    assert len(current["psalmAnalyses"])==len(NUMBERS)
    a=current["method"]["themeCoverageAudits"][-1]
    assert a["scope"]=="book-09-psalms-048-076"
    assert a["originalRelationCount"]==HISTORICAL
    assert a["addedRelationCount"]==ADDED
    assert a["sourcePsalmsModified"] is False
    counts={"original":0,"added":0,"verses":0}
    seen_psalms=set()
    for psalm in current["psalmAnalyses"]:
        n=psalm["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        source=load(CORPUS/f"psalm-{n:03d}.json")
        assert source["id"]==psalm["recordId"]
        assert source["title"]==psalm["title"]
        assert source["archangel"]=="michael"
        valid={v["number"] for v in source["verses"]}
        assert valid==set(range(1,len(valid)+1))
        counts["verses"]+=len(valid)
        original=frozen["psalms"][str(n)]
        seen=set()
        for rel in psalm["themes"]:
            tid=rel["themeId"]
            assert tid not in seen,(n,tid,"duplicate")
            seen.add(tid)
            assert rel["label"].strip()
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,"invalid refs",refs)
            if tid in original:
                assert rel==original[tid],(n,tid,"historic metadata altered")
                counts["original"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"attribution")
                assert len(rel["teaching"])>65,(n,tid,"unsubstantiated label")
                counts["added"]+=1
        assert set(original).issubset(seen),(n,"missing original")
    assert seen_psalms==NUMBERS
    assert counts["original"]==HISTORICAL and counts["added"]==ADDED,counts
    assert counts["verses"]==a["verifiedVerseCount"],counts
    print(f"BOOK09 PASS: {len(seen_psalms)} psalms (48–76), {counts['verses']} verses, "
          f"{HISTORICAL} historical unchanged, {ADDED} additions, {HISTORICAL+ADDED} total.")

if __name__=="__main__":
    main()
