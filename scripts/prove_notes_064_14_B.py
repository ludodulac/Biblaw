#!/usr/bin/env python3
"""BIBLAW 064-14/B: empreintes, images et limites de notes du PDF original.
Ne change jamais les textes, les statuts canoniques ni ne prononce un verdict automatique.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[
 ("book-29-psalm-200-note-001",2757),
 ("book-29-psalm-212-note-001",2814),
 ("book-29-psalm-216-note-001",2830),
 ("book-29-psalm-216-note-003",2831),
 ("book-29-psalm-217-note-001",2833),
]
PAGES=[2756,2757,2758,2813,2814,2815,2829,2830,2831,2832,2833,2834]
assert len(TARGETS)==5 and len(set(x for x,_ in TARGETS))==5
assert len(PAGES)==len(set(PAGES))
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
    for f in page_data[page]["footnoteCandidates"]:
        pt=tok(f["text"]);nt=tok(note["text"]);prefix=0
        for a,b in zip(pt,nt):
            if a!=b:break
            prefix+=1
        opts.append({**f,"wordTokens":len(pt),"matchedPrefixTokens":prefix,
            "tokensExactlyEqual":pt==nt,
            "printedTokensPrefixOfNote":bool(pt and nt[:len(pt)]==pt),
            "noteTokensPrefixOfPrinted":bool(nt and pt[:len(nt)]==nt)})
    opts.sort(key=lambda f:(f["matchedPrefixTokens"],f["tokensExactlyEqual"]),reverse=True)
    rows.append({"id":id,"PDFPage":page,
        "canonicalPsalm":psalm["id"],"canonicalPsalmPages":psalm["source"]["pdfPages"],
        "pdfPageWithinCanonical":page in psalm["source"]["pdfPages"],
        "psalmNoteIds":psalm["noteIds"],"reciprocal":id in psalm["noteIds"],
        "printedMarkerInJSON":note["appliesTo"]["marker"],"ordinalInID":n,
        "extractedText":note["text"],"wordTokens":len(tok(note["text"])),
        "bestPrinted":opts[0] if opts else None,"allCandidates":opts,
        "otherNoteIdsSamePsalm":[v for v in psalm["noteIds"] if v!=id],
        "technicalStatus":note.get("validation",{}).get("status"),
        "editorialVerdict":"NOT_ASSESSED_BY_SCRIPT"})
# Gardes documentaires B : comparaisons physiques ciblées, sans validation automatique.
by_id={r["id"]:r for r in rows}
for id,num in [
    ("book-29-psalm-200-note-001",45),
    ("book-29-psalm-216-note-001",28),
    ("book-29-psalm-217-note-001",151),
]:
    r=by_id[id]; f=r["bestPrinted"]
    assert r["reciprocal"] and r["pdfPageWithinCanonical"]
    assert r["wordTokens"]==num and f and f["tokensExactlyEqual"]
    assert f["marker"]==r["printedMarkerInJSON"]==1
r212=by_id["book-29-psalm-212-note-001"]
assert not r212["pdfPageWithinCanonical"] and r212["PDFPage"]==2814
assert r212["wordTokens"]==193 and r212["bestPrinted"]["wordTokens"]==4
assert r212["bestPrinted"]["printedTokensPrefixOfNote"]
assert any("Pr. 102" in x["text"] for x in page_data[2814]["lines"])
r216=by_id["book-29-psalm-216-note-003"]; f216=r216["bestPrinted"]
assert r216["PDFPage"]==2831 and r216["pdfPageWithinCanonical"] and r216["reciprocal"]
assert r216["wordTokens"]==77 and f216["wordTokens"]==78
assert f216["matchedPrefixTokens"]==66 and not f216["tokensExactlyEqual"]
assert "audelà" in r216["extractedText"]
competing=read(ROOT/"data/notes/books/book-29/book-29-psalm-216-note-002.json")
assert competing["source"]["pdfPage"]==2831
assert competing["id"] in r216["psalmNoteIds"]
assert tok(competing["text"])[:66]==tok(r216["extractedText"])[:66]
assert len(tok(competing["text"]))>r216["wordTokens"]
assert len(r216["allCandidates"])==1
print("BIBLAW-064-14-B-GUARD","3 exact notes","212 prayer composite","216/002-003 competing printed occurrence")

folder=ROOT/"reports/notes-064-14-proof/B"
folder.mkdir(parents=True,exist_ok=True)
(folder/"note-proof.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for p in PAGES:
    pix=pdf[p-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    pix.save(folder/f"pdf-page-{p}.png")
    (folder/f"pdf-page-{p}-layout.json").write_text(json.dumps(page_data[p],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for row in rows:
    f=row["bestPrinted"]
    print("BIBLAW-064-14-B",row["id"],"PDF",row["PDFPage"],
        "insidePsalm",row["pdfPageWithinCanonical"],"sourceTokens",row["wordTokens"],
        "printedTokens",f["wordTokens"] if f else None,
        "prefix",f["matchedPrefixTokens"] if f else None,
        "exact",f["tokensExactlyEqual"] if f else None,
        "marker",f["marker"] if f else None,"reciprocal",row["reciprocal"],
        "possibleOtherIDs",row["otherNoteIdsSamePsalm"])
print("SOURCE GUARD: no canonical note, psalm, prayer or publication change; editorial judgement reserved")
