#!/usr/bin/env python3
"""061: Check only 77 IDs from 060 artifact against original PDF. Read-only."""
import json, sys, re, csv, unicodedata, difflib
from pathlib import Path
from collections import Counter
import fitz

ROOT=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1])
pdf=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
out=ROOT/"reports/notes-061"
out.mkdir(parents=True,exist_ok=True)
def data(p): return json.loads(Path(p).read_text(encoding="utf8"))
def norm(text):
    s=unicodedata.normalize("NFD",str(text or "").lower())
    s="".join(c for c in s if unicodedata.category(c)!="Mn")
    return re.findall(r"[a-z0-9]+",s.replace("œ","oe").replace("æ","ae"))
def align(note,page):
    a,b=norm(note),norm(page)
    if not a or not b:return (0.0,0,[])
    matches=difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks()[:-1]
    longest=max((m.size for m in matches),default=0)
    covered=sum(m.size for m in matches)
    left=[];pos=0
    for m in matches:
        if m.a-pos>=4:left.append(" ".join(a[pos:m.a]))
        pos=m.a+m.size
    if len(a)-pos>=4:left.append(" ".join(a[pos:]))
    return (round(covered/len(a),3),longest,left[:8])
previous=data(source)
if len(previous)!=280:raise SystemExit("Wrong 060 artifact, abort")
blocking={"missing_canonical_psalm","no_reciprocal_note_id","archangel_mismatch",
    "book_number_mismatch","id_does_not_match_filename","record_type_not_note",
    "invalid_source_marker","different_provenance_document",
    "invalid_pdf_source_page","pdf_page_outside_psalm_source",
    "empty_or_very_short_text","possible_section_text_contamination",
    "published_note_text_differs"}
target=[x for x in previous if not x["is_published"] and
    (x["pdf_text_coverage"]<0.8 or (set(x["review_flags"]) & blocking))]
if len(target)!=77:raise SystemExit("Expected exactly 77 targeted IDs, got "+str(len(target)))
if len(pdf)!=4744:raise SystemExit("Original PDF not 4744 pages")
cache={}
def page(i):
    if i not in cache:cache[i]=pdf[i].get_text(sort=True) if 0<=i<len(pdf) else ""
    return cache[i]
rows=[]
for old in target:
    n=data(ROOT/old["path"]); nid=n["id"]; psid=n.get("appliesTo",{}).get("recordId","")
    match=re.fullmatch(r"book-(\d+)-psalm-(\d+)",psid)
    sp=(ROOT/"data/corpus/books"/("book-"+match[1])/("psalm-"+match[2]+".json")) if match else Path("/nonexistent")
    ps=data(sp) if sp.is_file() else {}
    pdfpage=n.get("source",{}).get("pdfPage")
    options=[]
    if isinstance(pdfpage,int):
        for num in range(max(1,pdfpage-2),min(len(pdf),pdfpage+2)+1):
            text=page(num-1)
            cov,long,missing=align(n.get("text",""),text)
            options.append({"pdfPage":num,"coverage":cov,"longestWords":long,
                "missingNoteSegments":missing,
                "pdfExcerpt":text[:2200]})
    options.sort(key=lambda x:(x["coverage"],x["longestWords"]),reverse=True)
    best=options[0] if options else {}
    marker=n.get("appliesTo",{}).get("marker")
    result={
      "id":nid,"source_file":old["path"],"target_psalm":psid,
      "source_note_text":n.get("text",""),
      "pdf_page_declared":pdfpage,"best_pdf_page":best.get("pdfPage"),
      "best_pdf_coverage":best.get("coverage",0),
      "best_contiguous_pdf_words":best.get("longestWords",0),
      "source_marker":marker,"note_ordinal":int(nid.split("-note-")[-1]),
      "reciprocal_note_id":nid in (ps.get("noteIds") or []),
      "psalm_archangel_matches":n.get("archangel")==ps.get("archangel"),
      "psalm_pdf_pages":(ps.get("source") or {}).get("pdfPages",[]),
      "pdf_page_candidates":options,
      "flags_from_060":old["review_flags"],
      "needs_visual_verification":True,
      "source_modified":False,
    }
    rows.append(result)
if len({r["id"] for r in rows})!=77:raise SystemExit("Duplicate IDs in 060 target subset")
(out/"per-note-proof.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
with (out/"index.csv").open("w",newline="",encoding="utf8") as f:
    keys=["id","source_file","target_psalm","pdf_page_declared","best_pdf_page",
        "best_pdf_coverage","best_contiguous_pdf_words","source_marker",
        "note_ordinal","reciprocal_note_id","psalm_archangel_matches","flags_from_060"]
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
    for r in rows:w.writerow({k:";".join(r[k]) if isinstance(r[k],list) else r[k] for k in keys})
weak=[r for r in rows if r["best_pdf_coverage"]<.8]
missing=[r for r in rows if not r["reciprocal_note_id"]]
contaminated=[r for r in rows if re.search(r"autres textes|table des matières|sommaire des textes",r["source_note_text"],re.I)]
summary={"source":"060 artifact run 39389492831; PDF from GitHub",
 "notes_targeted":77,"pdf_examined":77,
 "notes_with_pdf_word_coverage_at_least_80pct":77-len(weak),
 "notes_with_pdf_word_coverage_below_80pct":len(weak),
 "notes_missing_reciprocal_psalm_link":len(missing),
 "notes_with_section_contamination_signal":len(contaminated),
 "notes_corrected":0,"notes_still_pending_source_visual_review":77,
 "corpus_modified":False,"published":False,
 "flags":dict(Counter(z for r in rows for z in r["flags_from_060"]))}
(out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(out/"RAPPORT.md").write_text(
 "# Mission 061 — revue des 77 notes signalées par 060\n\n"
 "Sélection strictement reprise du rapport 060, sans nouvel audit général.\n\n"
 "Chaque entrée de per-note-proof.json comporte identifiant, rattachement,\n"
 "numéro de note, pages PDF examinées, extraits et comparaison des mots.\n\n"
 "La concordance textuelle ne permet pas, seule, de délimiter une note\n"
 "ou de corriger son appel de note; conserver les incertaines hors catalogue.\n\n"
 +json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BIBLAW_061_RESULTS "+json.dumps(summary,ensure_ascii=False))
for r in sorted(rows,key=lambda x:(x["best_pdf_coverage"],x["id"]))[:14]:
    top=r["pdf_page_candidates"][0] if r["pdf_page_candidates"] else {}
    print("BIBLAW_061_EXAMPLE "+json.dumps({"id":r["id"],"pdf":r["best_pdf_page"],
      "coverage":r["best_pdf_coverage"],"flags":r["flags_from_060"],
      "unmatched":top.get("missingNoteSegments",[])[:2],
      "note_tail":r["source_note_text"][-230:]},ensure_ascii=False))
print("BIBLAW_061_NO_PUBLICATION_NO_SOURCE_EDIT")
