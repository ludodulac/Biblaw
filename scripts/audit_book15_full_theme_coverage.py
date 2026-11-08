#!/usr/bin/env python3
"""Livre 15 (Raphaël) : contrôle des 27 psaumes et de l'intégrité des relations thématiques."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"data/thematic-index"
CORPUS=ROOT/"data/corpus/books/book-15"
NUMBERS=set(range(75,102))
HISTORICAL=84
ADDED=310

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book=load(INDEX/"books/book-15.json")
    base=load(INDEX/"audits/book15-original-relations.json")
    canonical={x["themeId"]:x["canonicalLabel"] for x in load(INDEX/"theme-search-index.json")["themes"]}
    assert book["book"]["number"]==15 and book["book"]["archangel"]=="raphael"
    assert base["originalRelationCount"]==HISTORICAL and base["archangel"]=="raphael"
    assert len(book["psalmAnalyses"])==len(NUMBERS)
    audit=book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"]=="book-15-psalms-075-101"
    assert audit["originalRelationCount"]==HISTORICAL and audit["addedRelationCount"]==ADDED
    assert audit["sourcePsalmsModified"] is False
    totals={"psalms":0,"verses":0,"old":0,"new":0}
    nonstandard=[]
    seen=set()
    for p in book["psalmAnalyses"]:
        n=p["number"]
        assert n in NUMBERS and n not in seen,n
        seen.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==p["recordId"],n
        assert src["title"]==p["title"],n
        assert src["archangel"]=="raphael",n
        nums=[v["number"] for v in src["verses"]]
        assert nums and nums==sorted(nums) and len(nums)==len(set(nums)),(n,"numbering")
        if nums!=list(range(1,len(nums)+1)):
            nonstandard.append([n,nums[0],nums[-1]])
        valid=set(nums)
        totals["psalms"]+=1
        totals["verses"]+=len(valid)
        original=base["psalms"][str(n)]
        seen_ids=set()
        for rel in p["themes"]:
            tid=rel["themeId"]
            assert tid not in seen_ids,(n,tid,"duplicate")
            seen_ids.add(tid)
            assert tid in canonical,(n,tid,"noncanonical")
            assert rel["label"]==canonical[tid],(n,tid,"canonical label mismatch")
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,"bad refs",refs)
            if tid in original:
                assert rel==original[tid],(n,tid,"historic modified")
                totals["old"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"prefix")
                assert len(rel["teaching"])>65,(n,tid,"short description")
                totals["new"]+=1
        assert set(original).issubset(seen_ids),(n,"historic theme lost")
    assert seen==NUMBERS
    assert totals["old"]==HISTORICAL,totals
    assert totals["new"]==ADDED,totals
    assert totals["verses"]==audit["verifiedVerseCount"],totals
    assert nonstandard==audit["sourceVerseNumberingNotes"],(nonstandard,audit)
    print(f"BOOK15 PASS: {totals['psalms']} psalms (75–101), {totals['verses']} verses, "
          f"{HISTORICAL} original unchanged, {ADDED} added, {HISTORICAL+ADDED} total, "
          f"source numbering exceptions: {nonstandard}")

if __name__=="__main__":
    main()
