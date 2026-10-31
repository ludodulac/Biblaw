#!/usr/bin/env python3
"""BIBLAW 064-12/A — source PDF ciblée ; aucune authentification automatique ni modification du corpus."""
from __future__ import annotations
import collections
import json
import re
import unicodedata
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[
    ("book-23-psalm-145-note-001",2020),
    ("book-23-psalm-146-note-001",2023),
    ("book-24-psalm-141-note-001",2134),
    ("book-26-psalm-169-note-001",2361),
    ("book-26-psalm-172-note-001",2373),
]
PAGES=[2019,2020,2021,2022,2023,2024,2133,2134,2135,2360,2361,2362,2372,2373,2374]
assert len(set(PAGES))==15 and len(TARGETS)==5

def tok(s):
    s = unicodedata.normalize("NFD", str(s or "").casefold())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("œ", "oe").replace("æ", "ae")
    return re.findall(r"[a-z0-9]+", s)

def read(path):
    return json.loads(path.read_text(encoding="utf8"))

dash = r"[-‐‑‒–—−]"
start = re.compile(rf"^\s*(\d{{1,2}})\s*{dash}\s*", re.U)

def lines_of(page):
    out = []
    for block in page.get_text("dict", sort=True)["blocks"]:
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans: continue
            text = "".join(s["text"] for s in spans).strip()
            if not text: continue
            out.append({
                "text":text,
                "x":round(min(s["bbox"][0] for s in spans), 1),
                "y":round(min(s["bbox"][1] for s in spans), 1),
                "size":round(max(s["size"] for s in spans), 2),
            })
    return out

def candidates(lines, page_number):
    out = []
    for i, line in enumerate(lines):
        m = start.match(line["text"])
        if not m or not 7 <= line["size"] <= 10.5 or line["x"] > 115: continue
        words = [line["text"][m.end():]]
        y = line["y"]
        for tail in lines[i+1:]:
            if tail["y"] <= y: continue
            if tail["y"]-y > 16: break
            if not (7 <= tail["size"] <= 10.5 and 43 <= tail["x"] <= 120): break
            if start.match(tail["text"]): break
            words.append(tail["text"])
            y=tail["y"]
        out.append({
            "page":page_number,"marker":int(m.group(1)),
            "fontSize":line["size"],"x":line["x"],"startY":line["y"],
            "endY":y,"text":" ".join(words).strip(),
        })
    return out


pdf=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
assert len(pdf)==4744,len(pdf)
page_data={}
for number in PAGES:
    lines=lines_of(pdf[number-1])
    assert lines,number
    page_data[number]={"lines":lines,"footnoteCandidates":candidates(lines,number)}
rows=[]
for id,page in TARGETS:
    bk,ps,n=map(int,re.fullmatch(r"book-(\d+)-psalm-(\d+)-note-(\d+)",id).groups())
    note=read(ROOT/f"data/notes/books/book-{bk:02d}/{id}.json")
    psalm=read(ROOT/f"data/corpus/books/book-{bk:02d}/psalm-{ps:03d}.json")
    assert id==note["id"] and note["recordType"]=="note"
    assert note["source"]["pdfPage"]==page
    assert psalm["id"]==note["appliesTo"]["recordId"]
    opts=[]
    for found in page_data[page]["footnoteCandidates"]:
        pt=tok(found["text"]);nt=tok(note["text"]);prefix=0
        for a,b in zip(pt,nt):
            if a!=b:break
            prefix+=1
        opts.append({**found,"wordTokens":len(pt),"matchedPrefixTokens":prefix,"tokensExactlyEqual":pt==nt,"printedTokensPrefixOfNote":bool(pt and nt[:len(pt)]==pt),"noteTokensPrefixOfPrinted":bool(nt and pt[:len(nt)]==nt)})
    opts.sort(key=lambda x:(x["matchedPrefixTokens"],x["tokensExactlyEqual"]),reverse=True)
    row={"id":id,"PDFPage":page,"canonicalPsalm":psalm["id"],"canonicalPsalmPages":psalm["source"]["pdfPages"],"psalmNoteIds":psalm["noteIds"],"reciprocal":id in psalm["noteIds"],"printedMarkerInJSON":note["appliesTo"]["marker"],"ordinalInID":n,"extractedText":note["text"],"wordTokens":len(tok(note["text"])),"bestPrinted":opts[0] if opts else None,"allCandidates":opts,"otherNoteIdsSamePsalm":[v for v in psalm["noteIds"] if v!=id],"technicalStatus":note.get("validation",{}).get("status"),"editorialVerdict":"NOT_ASSESSED_BY_SCRIPT"}
    rows.append(row)
# Garde ciblée fondée sur les limites relues sur les images du PDF original.
by_id={r["id"]:r for r in rows}
expected=[
    ("book-23-psalm-145-note-001",263,30,False),
    ("book-23-psalm-146-note-001",15,15,True),
    ("book-24-psalm-141-note-001",440,50,False),
    ("book-26-psalm-169-note-001",386,24,False),
    ("book-26-psalm-172-note-001",11,11,True),
]
for id,source_tokens,printed_tokens,is_exact in expected:
    r=by_id[id]; f=r["bestPrinted"]
    assert r["reciprocal"] and r["PDFPage"] in r["canonicalPsalmPages"]
    assert r["wordTokens"]==source_tokens and f["wordTokens"]==printed_tokens
    assert f["marker"]==1 and r["printedMarkerInJSON"]==1
    assert f["matchedPrefixTokens"]==printed_tokens
    assert f["tokensExactlyEqual"]==is_exact
assert any("Pr. 41." in l["text"] for l in page_data[2020]["lines"])
assert any(l["text"].startswith("Dans l’enracinement") for l in page_data[2021]["lines"])
assert any("Pr. 36." in l["text"] for l in page_data[2135]["lines"])
assert any("Pr. 54." in l["text"] for l in page_data[2361]["lines"])
assert any(l["text"].startswith("Tu prendras la statue") for l in page_data[2362]["lines"])
print("BIBLAW-064-12-A-GUARD","2/5 exact notes","3/5 composites avec prières préservées")

folder=ROOT/"reports/notes-064-12-proof/A"
folder.mkdir(parents=True,exist_ok=True)
(folder/"note-proof.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for p in PAGES:
    pix=pdf[p-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    pix.save(folder/f"pdf-page-{p}.png")
    (folder/f"pdf-page-{p}-layout.json").write_text(json.dumps(page_data[p],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for row in rows:
    x=row["bestPrinted"]
    print("BIBLAW-064-12-A",row["id"],"page",row["PDFPage"],"sourceTokens",row["wordTokens"],"printedTokens",x["wordTokens"] if x else None,"prefix",x["matchedPrefixTokens"] if x else None,"exact",x["tokensExactlyEqual"] if x else False,"marker",x["marker"] if x else None,"reciprocal",row["reciprocal"])
print("BIBLAW-064-12-A-EVIDENCE",len(rows),"notes",len(PAGES),"PDF pages; no editorial verdict and no original data changed")
