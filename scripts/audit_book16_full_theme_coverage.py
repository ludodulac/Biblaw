#!/usr/bin/env python3
"""Audit pérenne du livre 16 Ouriel : versets, index canonique et 79 relations historiques inchangées."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"data/thematic-index"
CORPUS=ROOT/"data/corpus/books/book-16"
NUMBERS=set(range(78,104))
HISTORICAL=79
ADDED=303

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book=load(INDEX/"books/book-16.json")
    base=load(INDEX/"audits/book16-original-relations.json")
    canonical={x["themeId"]:x["canonicalLabel"] for x in load(INDEX/"theme-search-index.json")["themes"]}
    assert book["book"]["number"]==16 and book["book"]["archangel"]=="ouriel"
    assert base["originalRelationCount"]==HISTORICAL and base["archangel"]=="ouriel"
    assert len(book["psalmAnalyses"])==len(NUMBERS)
    audit=book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"]=="book-16-psalms-078-103"
    assert audit["originalRelationCount"]==HISTORICAL and audit["addedRelationCount"]==ADDED
    assert audit["sourcePsalmsModified"] is False
    stats={"psalms":0,"verses":0,"old":0,"new":0}
    seen_psalms=set()
    nonstandard=[]
    for p in book["psalmAnalyses"]:
        n=p["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==p["recordId"] and src["title"]==p["title"] and src["archangel"]=="ouriel",n
        nums=[x["number"] for x in src["verses"]]
        assert nums and nums==sorted(nums) and len(nums)==len(set(nums)),(n,"source numbering")
        if nums!=list(range(1,len(nums)+1)):
            nonstandard.append([n,nums[0],nums[-1]])
        valid=set(nums)
        stats["psalms"]+=1
        stats["verses"]+=len(valid)
        original=base["psalms"][str(n)]
        seen_themes=set()
        for rel in p["themes"]:
            tid=rel["themeId"]
            assert tid not in seen_themes,(n,tid,"duplicate")
            seen_themes.add(tid)
            assert tid in canonical,(n,tid,"unknown canonical theme")
            assert rel["label"]==canonical[tid],(n,tid,"label changed")
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,refs)
            if tid in original:
                assert rel==original[tid],(n,tid,"historical relation modified")
                stats["old"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"prefix")
                assert len(rel["teaching"])>65,(n,tid,"summary too short")
                stats["new"]+=1
        assert set(original).issubset(seen_themes),(n,"historical theme missing")
    assert seen_psalms==NUMBERS
    assert stats["old"]==HISTORICAL,stats
    assert stats["new"]==ADDED,stats
    assert stats["verses"]==audit["verifiedVerseCount"],stats
    assert nonstandard==audit["sourceVerseNumberingNotes"],(nonstandard,audit)
    print(f"BOOK16 PASS: {stats['psalms']} psalms (78–103), {stats['verses']} verses, "
          f"{HISTORICAL} historical unchanged, {ADDED} added, {HISTORICAL+ADDED} total, "
          f"special numbering: {nonstandard}")

if __name__=="__main__":
    main()
