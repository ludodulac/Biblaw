#!/usr/bin/env python3
"""BIBLAW 064-17/B: empreintes, images et limites de notes du PDF original.
Ne change jamais les textes, les statuts canoniques ni ne prononce un verdict automatique.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[
 ("book-32-psalm-197-note-001",3174),
 ("book-32-psalm-197-note-002",3175),
 ("book-32-psalm-199-note-001",3181),
 ("book-32-psalm-203-note-002",3201),
 ("book-32-psalm-205-note-001",3212),
]
PAGES=[3173,3174,3175,3176,3180,3181,3182,3183,3199,3200,3201,3202,3211,3212,3213]
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
# Garde documentaire B : le script ne juge jamais les notes automatiquement.
byid={r["id"]:r for r in rows}
expected={
 "book-32-psalm-197-note-001":8,
 "book-32-psalm-197-note-002":14,
 "book-32-psalm-199-note-001":24,
 "book-32-psalm-203-note-002":29,
 "book-32-psalm-205-note-001":272,
}
for id,n in expected.items():
    r=byid[id];p=r["bestPrinted"]
    assert r["reciprocal"] and r["pdfPageWithinCanonical"]
    assert r["wordTokens"]==n and p and p["marker"]==r["printedMarkerInJSON"]==1
    assert len(r["allCandidates"])==1
    if id not in ("book-32-psalm-199-note-001",):
        assert p["wordTokens"]==n and p["tokensExactlyEqual"]
r=byid["book-32-psalm-199-note-001"];f=r["bestPrinted"]
assert f["wordTokens"]==21 and f["printedTokensPrefixOfNote"]
continuation=[x for x in page_data[3182]["lines"] if x["text"]=="à l’Enseignement." and x["size"]==9 and x["y"]>600]
assert len(continuation)==1 and len(tok(continuation[0]["text"]))==3
assert tok(r["extractedText"])==tok(f["text"]+" "+continuation[0]["text"])
r203=byid["book-32-psalm-203-note-002"]
assert r203["extractedText"].endswith("Thomas Sagesse.")
assert len(tok(r203["extractedText"]))==29
assert any("Pr. 93" in x["text"] for x in page_data[3202]["lines"])
other=read(ROOT/"data/notes/books/book-32/book-32-psalm-203-note-001.json")
assert other["source"]["pdfPage"]==3199 and other["text"]!=r203["extractedText"]
assert byid["book-32-psalm-197-note-001"]["PDFPage"]!=byid["book-32-psalm-197-note-002"]["PDFPage"]
print("BIBLAW-064-17-B-GUARD","3 exact","1 cross-page completion 21+3","1 clipped prayer composite 259->29","distinct markers")

folder=ROOT/"reports/notes-064-17-proof/B"
folder.mkdir(parents=True,exist_ok=True)
(folder/"note-proof.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for p in PAGES:
    pix=pdf[p-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    pix.save(folder/f"pdf-page-{p}.png")
    (folder/f"pdf-page-{p}-layout.json").write_text(json.dumps(page_data[p],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for row in rows:
    f=row["bestPrinted"]
    print("BIBLAW-064-17-B",row["id"],"PDF",row["PDFPage"],
        "insidePsalm",row["pdfPageWithinCanonical"],"sourceTokens",row["wordTokens"],
        "printedTokens",f["wordTokens"] if f else None,
        "prefix",f["matchedPrefixTokens"] if f else None,
        "exact",f["tokensExactlyEqual"] if f else None,
        "marker",f["marker"] if f else None,"reciprocal",row["reciprocal"],
        "possibleOtherIDs",row["otherNoteIdsSamePsalm"])
print("SOURCE GUARD: no canonical note, psalm, prayer or publication change; editorial judgement reserved")
