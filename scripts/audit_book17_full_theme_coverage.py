#!/usr/bin/env python3
"""Livre 17 Michaël : contrôle de 821 versets, 83 liens historiques et 301 nouveaux liens."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"data/thematic-index"
CORPUS=ROOT/"data/corpus/books/book-17"
NUMBERS=set(range(105,131))
HISTORICAL=83
ADDED=301
VERSES=821

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    book=load(INDEX/"books/book-17.json")
    baseline=load(INDEX/"audits/book17-original-relations.json")
    canonical={x["themeId"]:x["canonicalLabel"] for x in load(INDEX/"theme-search-index.json")["themes"]}
    assert book["book"]["number"]==17 and book["book"]["archangel"]=="michael"
    assert baseline["book"]==17 and baseline["archangel"]=="michael"
    assert baseline["originalRelationCount"]==HISTORICAL
    assert len(book["psalmAnalyses"])==len(NUMBERS)
    audit=book["method"]["themeCoverageAudits"][-1]
    assert audit["scope"]=="book-17-psalms-105-130"
    assert audit["originalRelationCount"]==HISTORICAL and audit["addedRelationCount"]==ADDED
    assert audit["verifiedVerseCount"]==VERSES and audit["sourcePsalmsModified"] is False
    stats={"psalms":0,"verses":0,"historical":0,"added":0}
    seen_psalms=set()
    nonstandard=[]
    for p in book["psalmAnalyses"]:
        n=p["number"]
        assert n in NUMBERS and n not in seen_psalms,n
        seen_psalms.add(n)
        src=load(CORPUS/f"psalm-{n:03d}.json")
        assert src["id"]==p["recordId"] and src["title"]==p["title"] and src["archangel"]=="michael",n
        num_list=[x["number"] for x in src["verses"]]
        assert num_list and num_list==sorted(num_list) and len(set(num_list))==len(num_list),(n,"numbering")
        if num_list!=list(range(1,len(num_list)+1)):
            nonstandard.append([n,num_list[0],num_list[-1]])
        valid=set(num_list)
        stats["verses"]+=len(valid)
        stats["psalms"]+=1
        frozen=baseline["psalms"][str(n)]
        seen=set()
        for rel in p["themes"]:
            tid=rel["themeId"]
            assert tid not in seen,(n,tid,"duplicate")
            seen.add(tid)
            assert tid in canonical,(n,tid,"noncanonical")
            assert rel["label"]==canonical[tid],(n,tid,"canonical label")
            assert rel["importance"] in {"central","important","related"}
            assert rel["directness"] in {"direct","symbolic","editorial","indirect","contextual"}
            refs=rel["verseNumbers"]
            assert refs and len(refs)==len(set(refs)) and set(refs)<=valid,(n,tid,"invalid refs",refs)
            if tid in frozen:
                assert rel==frozen[tid],(n,tid,"historical relation changed")
                stats["historical"]+=1
            else:
                assert rel["teaching"].startswith("La Bible essénienne enseigne que "),(n,tid,"prefix")
                assert len(rel["teaching"])>65,(n,tid,"empty summary")
                stats["added"]+=1
        assert set(frozen).issubset(seen),(n,"original link lost")
    assert seen_psalms==NUMBERS
    assert stats["historical"]==HISTORICAL,stats
    assert stats["added"]==ADDED,stats
    assert stats["verses"]==VERSES,stats
    assert nonstandard==audit["sourceVerseNumberingNotes"],nonstandard
    print(f"BOOK17 PASS: {stats['psalms']} psalms (105-130), {VERSES} verses, "
          f"{HISTORICAL} historical identical, {ADDED} new, {HISTORICAL+ADDED} total")

if __name__=="__main__":
    main()
