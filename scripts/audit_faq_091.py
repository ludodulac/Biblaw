#!/usr/bin/env python3
"""091 — audit the nine complete owner-provided FAQ answers and cited Psalm verses."""
import json, re, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
base=load("data/faq-public-085.json")
assert base["version"]==5 and len(base["questions"])==25
b090=load("data/faq-090-books.json")["verifiedPsalms"]
old=[load(f"data/faq-090-{i}.json") for i in range(1,6)]
assert len(old)==5
bookdata=load("data/faq-091-books.json")
books=bookdata["verifiedPsalms"]
assert bookdata["version"]==1 and len(books)==24
catalog=load("data/browser-search-catalog.json")
records={r["id"]:r for r in catalog["records"]}
assert len([r for r in records.values() if r["recordType"]=="note"])==11
pattern=re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
all_ids=set()
links=0
for i in range(1,10):
    q=load(f"data/faq-091-{i}.json")
    assert q["id"]==f"faq-priere-paix-{i}", i
    assert len(q["answer"])>1000 and len(q["title"])>15
    found=list(pattern.finditer(q["answer"]))
    assert len(found)==(3 if i==1 else 4)==q["answer"].count("(psaume "), q["id"]
    for m in found:
        number=int(m.group(1))
        norm=unicodedata.normalize("NFD",m.group(2))
        arch="".join(ch for ch in norm if not unicodedata.combining(ch)).lower()
        book=books[f"{arch}:{number}"]
        rid=f"book-{book:02d}-psalm-{number:03d}"
        verses=[]
        def expand(x):
            lo,hi=map(int,x.groups())
            assert lo>0 and hi>=lo and hi-lo<=100
            verses.extend(range(lo,hi+1))
            return ""
        tail=re.sub(r"(\d+)\s+à\s+(\d+)",expand,m.group(3))
        verses.extend(map(int,re.findall(r"\d+",tail)))
        assert verses
        ps=records[rid]
        assert ps["recordType"]=="psalm" and ps["archangel"]==arch and ps["number"]==number
        assert set(verses)<={int(v["number"]) for v in ps["verses"]}
        source=load(f"data/corpus/books/book-{book:02d}/psalm-{number:03d}.json")
        assert source["id"]==rid and source["archangel"]==arch
        assert set(verses)<={int(v["number"]) for v in source["verses"]}
        links+=1
        all_ids.add(rid)
assert links==35 and len(all_ids)==24,(links,len(all_ids))
assert len(base["questions"])+len(old)+9==39
print(f"FAQ 091 PASS: 9 exact answers, {links} linked references, {len(all_ids)} verified public Psalms, 11 public notes unchanged")
