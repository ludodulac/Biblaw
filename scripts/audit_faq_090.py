#!/usr/bin/env python3
"""Audit the five new owner-provided answers and their public Psalm references."""
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

base=load("data/faq-public-085.json")
assert base["version"]==5 and len(base["questions"])==25
book_data=load("data/faq-090-books.json")
books=book_data["verifiedPsalms"]
assert book_data["version"]==1 and len(books)==15

public=load("data/browser-search-catalog.json")
by_id={r["id"]:r for r in public["records"]}
assert len([r for r in public["records"] if r["recordType"]=="note"])==11

pattern=re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
all_ids=set()
count=0
for k in range(1,6):
    q=load(f"data/faq-090-{k}.json")
    assert q["id"]==f"faq-presence-dieu-{k}"
    assert len(q["title"])>15 and len(q["answer"])>1000
    matches=list(pattern.finditer(q["answer"]))
    assert len(matches)==q["answer"].count("(psaume ")==4, q["id"]
    references=[]
    for m in matches:
        number=int(m.group(1))
        arch=unicodedata.normalize("NFD",m.group(2))
        arch="".join(c for c in arch if not unicodedata.combining(c)).lower()
        book=books[f"{arch}:{number}"]
        ident=f"book-{book:02}-psalm-{number:03}"
        verses=[]
        def expand(match):
            start,end=map(int,match.groups())
            assert end>=start and end-start<=100
            verses.extend(range(start,end+1))
            return ""
        remaining=re.sub(r"(\d+)\s+à\s+(\d+)",expand,m.group(3))
        verses.extend(map(int,re.findall(r"\d+",remaining)))
        verses=sorted(set(verses))
        assert verses
        record=by_id[ident]
        assert record["recordType"]=="psalm"
        assert record["archangel"]==arch and record["number"]==number
        assert set(verses)<={int(v["number"]) for v in record["verses"]}
        original=load(f"data/corpus/books/book-{book:02}/psalm-{number:03}.json")
        assert original["id"]==ident and original["archangel"]==arch
        assert set(verses)<={int(v["number"]) for v in original["verses"]}
        references.append({"label":m.group(0),"recordId":ident,"archangel":arch,"number":number,"verses":verses})
        count+=1
        all_ids.add(ident)
    if q.get("references"):
        assert q["references"]==references, "Wrong stored verse references"

assert count==20 and len(all_ids)==15,(count,len(all_ids))
assert len(base["questions"])+5==30
print(f"FAQ 090 PASS: 5 exact answers, {count} linked citations, {len(all_ids)} verified public Psalms, 11 public notes unchanged")
