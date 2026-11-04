#!/usr/bin/env python3
"""064-02: immutable targeted PDF evidence for the next 10 notes (two sets of five).
This script never modifies biblical records or makes editorial verdicts.
Only PDF source pages 268, 314, 318, 325, 334, 357, 369, 378 are read.
"""
from __future__ import annotations
import collections
import json
import re
import unicodedata
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ("book-05-psalm-035-note-001", 268),
    ("book-06-psalm-034-note-001", 314),
    ("book-06-psalm-036-note-001", 318),
    ("book-06-psalm-040-note-002", 325),
    ("book-06-psalm-040-note-003", 325),
    ("book-06-psalm-045-note-001", 334),
    ("book-07-psalm-024-note-001", 357),
    ("book-07-psalm-024-note-002", 357),
    ("book-07-psalm-029-note-001", 369),
    ("book-07-psalm-032-note-001", 378),
]
PAGES = sorted(set(p for _, p in TARGETS))
assert PAGES == [268,314,318,325,334,357,369,378]


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
assert len(pdf)==4744, len(pdf)
assert len(TARGETS)==10 and len(set(x for x,_ in TARGETS))==10
page_data={}
for number in PAGES:
    pg=pdf[number-1]
    ln=lines_of(pg)
    page_data[number]={"lines":ln,"footnoteCandidates":candidates(ln,number)}
    assert ln,number

by_group={"A":[],"B":[]}
for idx,(id,expected_page) in enumerate(TARGETS):
    b,p,n=map(int,re.fullmatch(r"book-(\d+)-psalm-(\d+)-note-(\d+)",id).groups())
    note=read(ROOT/f"data/notes/books/book-{b:02d}/{id}.json")
    psalm=read(ROOT/f"data/corpus/books/book-{b:02d}/psalm-{p:03d}.json")
    assert note["id"]==id and note["recordType"]=="note" and psalm["id"]==note["appliesTo"]["recordId"]
    assert note["source"]["pdfPage"]==expected_page
    found=[]
    for f in page_data[expected_page]["footnoteCandidates"]:
        w=tok(f["text"]); note_words=tok(note["text"])
        common=0
        for a,bword in zip(w,note_words):
            if a!=bword:break
            common+=1
        found.append({**f,"wordTokens":len(w),"matchedPrefixTokens":common,
            "tokensExactlyEqual":w==note_words,
            "printedTokensPrefixOfNote": bool(w and note_words[:len(w)]==w),
            "noteTokensPrefixOfPrinted":bool(note_words and w[:len(note_words)]==note_words)})
    found.sort(key=lambda x:(x["matchedPrefixTokens"],x["tokensExactlyEqual"]),reverse=True)
    best=found[0] if found else None
    row={"id":id,"PDFPage":expected_page,"canonicalPsalm":psalm["id"],
       "canonicalPsalmPages":psalm["source"]["pdfPages"],"psalmNoteIds":psalm["noteIds"],
       "reciprocal":id in psalm["noteIds"],"printedMarkerInJSON":note["appliesTo"]["marker"],
       "ordinalInID":n,"extractedText":note["text"],"wordTokens":len(tok(note["text"])),
       "bestPrinted":best,"allCandidates":found,
       "otherNoteIdsSamePsalm": [v for v in psalm["noteIds"] if v!=id],
       "technicalStatus":note.get("validation",{}).get("status"),
       "editorialVerdict":"NOT_ASSESSED_BY_SCRIPT"}
    by_group["A" if idx<5 else "B"].append(row)

for group in ("A","B"):
    folder=ROOT/f"reports/notes-064-02-proof/{group}"
    folder.mkdir(parents=True,exist_ok=True)
    rows=by_group[group]
    assert len(rows)==5
    (folder/"note-proof.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    for n in sorted(set(r["PDFPage"] for r in rows)):
        pg=pdf[n-1]
        pix=pg.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
        pix.save(folder/f"pdf-page-{n}.png")
        (folder/f"pdf-page-{n}-layout.json").write_text(
          json.dumps(page_data[n],indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("BIBLAW-064-02-EVIDENCE",group,"notes=",len(rows),"pages=",sorted(set(r["PDFPage"] for r in rows)),
       "exactPrint=",sum(bool(r["bestPrinted"] and r["bestPrinted"]["tokensExactlyEqual"]) for r in rows))
# Report potential identity collisions; script never resolves them by itself.
by_text = collections.defaultdict(list)
for group in ("A", "B"):
    for row in by_group[group]:
        by_text[tuple(tok(row["extractedText"]))].append(row["id"])
for duplicates in by_text.values():
    if len(duplicates)>1:
        print("BIBLAW-064-02-DUPLICATE-EXTRACTED-TEXT",json.dumps(duplicates))
print("SOURCE GUARD: original note files, psalms and catalog unchanged; no verdict assigned")
