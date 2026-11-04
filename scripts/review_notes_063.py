#!/usr/bin/env python3
"""MISSION 063: source-grounded focused review of 30 + 3 still-uncertain notes.
No repeated 060/061/062 audit; IDs come from the approved 062 decision table.
Evidence: original PDF page typography, notes' printed numbers, canonical links.
NO CORPUS EDITS, NO AUTOPUBLICATION.
"""
from pathlib import Path
from collections import Counter
import difflib, json, re, sys, unicodedata
import fitz

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"Bible essénienne (classée par livres).pdf"
REPORT_062=ROOT/"reports/notes-062/decisions.json"
OUT=ROOT/"reports/notes-063"
OUT.mkdir(parents=True,exist_ok=True)
B44=[f"book-44-psalm-285-note-{i:03d}" for i in (2,3,4)]
previous=json.loads(REPORT_062.read_text(encoding="utf8"))["notes"]
uncertain=[v for v in previous if v["status"]=="INCERTAINE"]
assert len(uncertain)==30
targets=[v["id"] for v in uncertain]+B44
assert len(targets)==33 and len(set(targets))==33
doc=fitz.open(SOURCE);assert len(doc)==4744

def folded(value):
    v=unicodedata.normalize("NFD",str(value or "").casefold())
    v="".join(c for c in v if unicodedata.category(c)!="Mn")
    return v.replace("œ","oe").replace("æ","ae")
def tokens(text):
    return re.findall(r"[a-z0-9]+",folded(text))
def clean(text):return " ".join(tokens(text))
def word_ratio(a,b):
    a=tokens(a);b=tokens(b)
    if not a or not b:return 0.0
    return round(difflib.SequenceMatcher(None,a,b,autojunk=False).ratio(),3)
def get_spans(index):
    result=[]
    for block in doc[index].get_text("dict",sort=True)["blocks"]:
        for line in block.get("lines",[]):
            allspans=line.get("spans",[])
            if not allspans:continue
            text="".join(s["text"] for s in allspans).strip()
            if text:
                result.append({"text":text,"size":round(max(s["size"] for s in allspans),2),
                    "x":round(min(s["bbox"][0] for s in allspans),2),
                    "y":round(min(s["bbox"][1] for s in allspans),2)})
    return result
cache={}
def spans(page):
    if not 1<=page<=len(doc):return []
    if page not in cache:cache[page]=get_spans(page-1)
    return cache[page]
def printed_notes(page):
    items=spans(page);found=[]
    for i,line in enumerate(items):
        if not (line["x"]<75 and 7<=line["size"]<=10.3):continue
        m=re.match(r"^\s*(\d{1,2})\s*[-–—]\s*",line["text"])
        if not m:continue
        body=[line["text"][m.end():].strip()];last_y=line["y"]
        for following in items[i+1:]:
            if following["y"]<=last_y:continue
            if following["y"]-last_y>15.5:break
            if not (7<=following["size"]<=10.3 and 52<=following["x"]<=110):break
            if re.match(r"^\s*\d{1,2}\s*[-–—]\s*",following["text"]):break
            body.append(following["text"]);last_y=following["y"]
        found.append({"page":page,"marker":int(m[1]),"y":line["y"],
            "fontSize":line["size"],"marginLeft":line["x"],
            "text":" ".join(body).strip()})
    return found

rows=[]
for id in targets:
    book,psalm,num=map(int,re.fullmatch(r"book-(\d+)-psalm-(\d+)-note-(\d+)",id).groups())
    path=ROOT/"data/notes/books"/f"book-{book:02d}"/(id+".json")
    note=json.loads(path.read_text(encoding="utf8"))
    assert note["id"]==id and note["recordType"]=="note"
    target=note.get("appliesTo",{}).get("recordId","")
    canonical=ROOT/"data/corpus/books"/f"book-{book:02d}"/f"psalm-{psalm:03d}.json"
    p=json.loads(canonical.read_text(encoding="utf8")) if canonical.is_file() else {}
    sourcepage=note.get("source",{}).get("pdfPage")
    canonical_pages=(p.get("source") or {}).get("pdfPages") or []
    candidates=sorted(set(range(max(1,sourcepage-6),min(len(doc),sourcepage+6)+1))
        |{n for n in canonical_pages if isinstance(n,int) and 1<=n<=len(doc)}) if isinstance(sourcepage,int) else []
    layout=[]
    for page in candidates:
        for entry in printed_notes(page):
            # Both the first and the last words matter. A matching footnote
            # number only is NOT evidence of a relationship to this Psalm.
            beginning=" ".join(tokens(note["text"])[:min(16,len(tokens(note["text"])))])
            head=" ".join(tokens(entry["text"])[:min(16,len(tokens(entry["text"])))])
            likeness=word_ratio(beginning,head)
            score=word_ratio(note["text"],entry["text"])
            layout.append({**entry,"head_similarity":likeness,
                "whole_similarity":score,"relative_page":entry["page"]-sourcepage,
                "page_in_target_psalm":entry["page"] in canonical_pages})
    layout.sort(key=lambda x:(x["head_similarity"],x["whole_similarity"],
        -abs(x["relative_page"])),reverse=True)
    credible=[x for x in layout if x["head_similarity"]>=.84]
    best=credible[0] if credible else None
    exact=best and clean(best["text"])==clean(note["text"])
    mismatch=best and (best["marker"]!=num or
        best["marker"]!=note.get("appliesTo",{}).get("marker"))
    continuations=[]
    # Show precisely the PDF lines after a printed footnote and the first
    # text lines on the following page. This prevents trimming cross-page
    # authentic prose as if it were a stray Psalm.
    if best:
        page_spans=spans(best["page"])
        x=next((i for i,l in enumerate(page_spans)
            if abs(l["y"]-best["y"])<.2 and
              re.match(r"^\s*\d{1,2}\s*[-–—]",l["text"])),None)
        if x is not None:
            continuations=page_spans[x:x+24]
    notes_in_source=[]
    for pg in sorted(set([sourcepage-1,sourcepage,sourcepage+1]+canonical_pages[:3])) if isinstance(sourcepage,int) else []:
        if 1<=pg<=len(doc):
            notes_in_source.extend([{"page":n["page"],"marker":n["marker"],
                "head":n["text"][:115],"tail":n["text"][-115:]} for n in printed_notes(pg)])
    psalm_notes=p.get("noteIds") or []
    rows.append({"id":id,"path":str(path.relative_to(ROOT)),"pdfPage":sourcepage,
        "pdfPagesOfProposedPsalm":canonical_pages,
        "sourceMarker":note.get("appliesTo",{}).get("marker"),
        "idOrdinal":num,"targetPsalm":target,
        "reciprocalPsalm":id in psalm_notes,
        "psalmOtherNoteIds":psalm_notes,
        "sourceText":note["text"],"sourceTextChars":len(note["text"]),
        "bestPrint":best,"exactTextPrint":bool(exact),"printedOrdinalDisagrees":bool(mismatch),
        "candidatePrintedNotes":layout[:6],"allMarkersNearSource":notes_in_source[:28],
        "followingTypographicLines":continuations[:20],
        "nextPageFirstLines":spans(best["page"]+1)[:15] if best else [],
        "status":"INCERTAINE","sourceModified":False,
        "initialAnomaly":next((r.get("initial_anomaly","") for r in uncertain if r["id"]==id),
             "061 : livre 44 / psaume 285, lien non confirmé")})
assert len(rows)==33 and len({r["id"] for r in rows})==33
(OUT/"targeted-pdf-evidence.json").write_text(
 json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
summary=Counter()
for r in rows:
 if r["bestPrint"]:summary["printed_head_detected"]+=1
 if r["exactTextPrint"]:summary["original_text_equals_printed_footnote"]+=1
 if r["reciprocalPsalm"]:summary["reciprocal_psalm_id"]+=1
 if r["printedOrdinalDisagrees"]:summary["printed_marker_disagrees"]+=1
print("BIBLAW_063_SUMMARY "+json.dumps({"targeted":33,"previous_uncertain":30,
    "special_book44":3,**summary,"publication":0,"sourceEdits":0},ensure_ascii=False))
for r in rows:
 b=r["bestPrint"] or {}
 print("BIBLAW_063_NOTE "+json.dumps({"id":r["id"],"pdf":r["pdfPage"],
  "psalm_pdf":r["pdfPagesOfProposedPsalm"],"otherNoteIds":r["psalmOtherNoteIds"],
  "marker":r["sourceMarker"],"printedMarker":b.get("marker"),
  "printedPdf":b.get("page"),"font":b.get("fontSize"),
  "head":b.get("head_similarity"),"similarity":b.get("whole_similarity"),
  "equal":r["exactTextPrint"],"reciprocal":r["reciprocalPsalm"],
  "srcChars":r["sourceTextChars"],"start":r["sourceText"][:135],
  "end":r["sourceText"][-125:],"pdfEnd":b.get("text","")[-195:],
  "adjacentMarkers":r["allMarkersNearSource"][:6]},ensure_ascii=False))
print("BIBLAW_063_EVIDENCE_ONLY")
