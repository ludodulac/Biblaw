#!/usr/bin/env python3
"""Mission 061: evidence for only five verified extraction boundaries; read-only."""
import difflib
import json
import re
import unicodedata
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
PDF=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
cases=[
 ("05","036",1,270,"meilleur fruit"),
 ("22","150",1,1849,"se propager dans tous les mondes"),
 ("44","285",2,4653,"autres textes de l'Archange Michaël"),
 ("44","285",3,4720,"autres textes de l'Archange Raphaël"),
 ("44","285",4,4724,"autres textes de l'Archange Ouriel"),
]
def norm(text):
    s=unicodedata.normalize("NFD",str(text).lower())
    s="".join(c for c in s if unicodedata.category(c)!="Mn")
    s=s.replace("œ","oe").replace("æ","ae")
    return " ".join(re.findall(r"[a-z0-9]+",s))
def coverage(note,page):
    a,b=norm(note).split(),norm(page).split()
    if not a or not b:return 0,0
    blocks=difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks()
    return round(sum(m.size for m in blocks)/len(a),3),max(m.size for m in blocks)
assert len(PDF)==4744
catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf8"))
assert len([r for r in catalog["records"] if r.startswith("data/notes/")])==11
for book,psalm,n,page_num,unwanted in cases:
    nid=f"book-{book}-psalm-{psalm}-note-{n:03d}"
    path=ROOT/"data/notes/books"/f"book-{book}"/(nid+".json")
    item=json.loads(path.read_text(encoding="utf8"))
    assert item["id"]==nid and item["recordType"]=="note"
    assert item.get("validation",{}).get("status")=="machine-extracted-needs-review"
    assert unwanted not in item["text"].lower()
    results=[]
    for number in range(page_num-2,page_num+3):
        if number<1 or number>len(PDF):continue
        page=PDF[number-1].get_text(sort=True)
        cv,longest=coverage(item["text"],page)
        results.append((cv,longest,number))
    best=max(results)
    print("CORRECTED_061_PDF_ATTESTATION",
          nid,"best_page",best[2],"coverage",best[0],
          "longest_matching_word_run",best[1],"source_page",page_num)
    # PDF extraction is noisy but the retained note must match the original.
    assert best[0]>=0.63 and best[1]>=9,(nid,best)
assert len(cases)==5
print("BIBLAW_061_CONFIRMED_PDF_PREFIXES_PASS count=5 catalog_not_modified=True")
