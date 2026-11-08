#!/usr/bin/env python3
"""Audit permanent : Livre 14 Gabriel, intégrité des 88 relations originales, références des 330 ajouts."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/thematic-index"
CORPUS=ROOT/"data/corpus/books/book-14"
NUMBERS=set(range(82,111))
HISTORICAL=88
ADDED=330

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    book=load(DATA/"books/book-14.json")
    original=load(DATA/"audits/book14-original-relations.json")
    canonical={t["themeId"]:t["canonicalLabel"] for t in load(DATA/"theme-search-index.json")["themes"]}
    assert book["book"]["number"]==14 and book["book"]["archangel"]=="gabriel"
    assert original["archangel"]=="gabriel" and original["originalRelationCount"]==HISTORICAL
    assert len(book["psalmAnalyses"])==len(NUMBERS)
    last=book["method"]["themeCoverageAudits"][-1]
    assert last["scope"]=="book-14-psalms-082-110"
    assert last["originalRelationCount"]==HISTORICAL and last["addedRelationCount"]==ADDED
    assert last["sourcePsalmsModified"] is False
    counts={"psalms":0,"verses":0,"old":0,"new":0}
    seen_psalms=set()
    for analysis in book["psalmAnalyses"]:
        n=analysis["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==analysis["recordId"]
        assert src["title"]==analysis["title"]
        assert src["archangel"]=="gabriel"
        valid={v["number"] for v in src["verses"]}
        assert valid==set(range(1,len(valid)+1)),n
        counts["psalms"]+=1
        counts["verses"]+=len(valid)
        original_themes=original["psalms"][str(n)]
        seen_ids=set()
        for rel in analysis["themes"]:
            tid=rel["themeId"]
            assert tid not in seen_ids,(n,tid,"duplicate")
            seen_ids.add(tid)
            assert tid in canonical,(n,tid,"unknown theme")
            assert rel["label"]==canonical[tid],(n,tid,"label")
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,"invalid verse",refs)
            if tid in original_themes:
                assert rel==original_themes[tid],(n,tid,"original changed")
                counts["old"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"attribution")
                assert len(rel["teaching"])>65,(n,tid,"teaching")
                counts["new"]+=1
        assert set(original_themes).issubset(seen_ids),(n,"original relation lost")
    assert seen_psalms==NUMBERS
    assert counts["old"]==HISTORICAL,counts
    assert counts["new"]==ADDED,counts
    assert counts["verses"]==last["verifiedVerseCount"],counts
    print(f"BOOK14 PASS: {counts['psalms']} psalms (82-110), {counts['verses']} verses, "
          f"{HISTORICAL} originals unchanged, {ADDED} additions, {HISTORICAL+ADDED} total")

if __name__=="__main__":
    main()
