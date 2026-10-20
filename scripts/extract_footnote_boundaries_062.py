#!/usr/bin/env python3
"""062 evidence-based identification of true PDF footnote boundaries for 72 notes.
Consumes ONLY 061 evidence; inspects original PDF page typography, marker and
canonical source page/reciprocal links. Does not modify source texts.
"""
import fitz,json,re,sys,unicodedata,difflib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
all061=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
five={"book-05-psalm-036-note-001","book-22-psalm-150-note-001","book-44-psalm-285-note-002","book-44-psalm-285-note-003","book-44-psalm-285-note-004"}
rows=[r for r in all061 if r["id"] not in five]
assert len(rows)==72
doc=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
def norm(value):
 t=unicodedata.normalize("NFD",str(value or "").lower())
 t="".join(c for c in t if unicodedata.category(c)!="Mn")
 return " ".join(re.findall(r"[a-z0-9]+",t.replace("œ","oe").replace("æ","ae")))
def get_lines(page):
 out=[]
 for block in page.get_text("dict",sort=True)["blocks"]:
  for line in block.get("lines",[]):
   spans=line.get("spans",[])
   if not spans:continue
   out.append({"text":"".join(s["text"] for s in spans).strip(),
     "font":round(max(s["size"] for s in spans),1),
     "x":round(min(s["bbox"][0] for s in spans),1),
     "y":round(min(s["bbox"][1] for s in spans),1)})
 return out
result=[]
for rec in rows:
 note_id=rec["id"]
 obj=json.loads((ROOT/rec["source_file"]).read_text(encoding="utf8"))
 text=obj.get("text","")
 target=obj.get("appliesTo",{}).get("recordId","")
 m=re.match(r"book-(\d+)-psalm-(\d+)",target)
 ppath=ROOT/"data/corpus/books"/("book-"+m[1])/("psalm-"+m[2]+".json") if m else None
 ps=json.loads(ppath.read_text(encoding="utf8")) if ppath and ppath.exists() else {}
 candidates=[]
 p=obj.get("source",{}).get("pdfPage")
 for number in range(max(1,p-2),min(len(doc),p+2)+1) if isinstance(p,int) else []:
  spans=get_lines(doc[number-1])
  # Printed numbered notes have smaller body type and left margin ~56.7.
  starts=[i for i,s in enumerate(spans) if s["x"]<66 and 7.5<=s["font"]<=10
    and re.match(r"^\s*\d{1,2}\s*[-–—]\s*",s["text"])]
  for idx in starts:
   match=re.match(r"^\s*(\d{1,2})\s*[-–—]\s*",spans[idx]["text"])
   block=[spans[idx]["text"][match.end():]]
   start_y=spans[idx]["y"];yy=start_y
   for k in range(idx+1,len(spans)):
    s=spans[k]
    if s["y"]<=yy:continue
    if s["y"]-yy>14.5:break
    if not 7.5<=s["font"]<=10 or not 53<=s["x"]<=82:break
    if re.match(r"^\s*\d{1,2}\s*[-–—]\s*",s["text"]):break
    block.append(s["text"]);yy=s["y"]
   foot=" ".join(block).strip()
   head=norm(" ".join(norm(text).split()[:9]))
   pdf_head=norm(" ".join(norm(foot).split()[:9]))
   sim=difflib.SequenceMatcher(None,head,pdf_head,autojunk=False).ratio()
   # Compare not only a few words: a real note must be anchored and cover
   # its own footnote block without invading another verse/section.
   complete_ratio=difflib.SequenceMatcher(None,norm(text),norm(foot),autojunk=False).ratio()
   candidates.append({"pdfPage":number,"marker":int(match[1]),"pdfNote":foot,
    "firstTextSimilarity":round(sim,3),"completeTextSimilarity":round(complete_ratio,3),
    "fontSize":spans[idx]["font"],"leftMargin":spans[idx]["x"],
    "topY":start_y,"lines":len(block),"noteFootnoteWords":len(norm(foot).split())})
 candidates.sort(key=lambda c:(c["firstTextSimilarity"],c["completeTextSimilarity"],c["noteFootnoteWords"]),reverse=True)
 best=candidates[0] if candidates else None
 first=(norm(best["pdfNote"]).split()[:9] if best else [])
 actual_first=norm(text).split()[:9]
 first_exact=bool(first and first==actual_first)
 # Candidate source prefix must match printed footnote. Multiple spaces,
 # line-end soft hyphens and OCR reading-order issues disqualify automatic
 # correction; they do not disprove authenticity.
 identical=bool(best and norm(best["pdfNote"])==norm(text))
 possible_spillover=bool(best and len(norm(text).split())>best["noteFootnoteWords"]+5 and first_exact)
 infos={"id":note_id,"pdf_page_declared":p,"original_060_flags":rec["flags_from_060"],
   "psalm":target,"canonical_note_id_present":note_id in (ps.get("noteIds") or []),
   "canonical_psalm_pdf_pages":(ps.get("source") or {}).get("pdfPages",[]),
   "best":best,"first_9_words_exact":first_exact,
   "identical_normalized_text":identical,"probable_extraction_spillover":possible_spillover,
   "requires_manual_boundary_confirmation":True}
 result.append(infos)
out=ROOT/"reports/notes-062"
out.mkdir(parents=True,exist_ok=True)
(out/"footnote-boundaries.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
counts=collections.Counter()
for r in result:
 if not r["best"]:counts["no_footnote_marker"]+=1
 elif r["first_9_words_exact"]:counts["footnote_start_confirmed"]+=1
 if r["identical_normalized_text"]:counts["full_exact_match"]+=1
 if r["probable_extraction_spillover"]:counts["probably_spillover"]+=1
 if r["best"] and r["best"]["marker"]!=r["best"]["marker"]:counts["marker_mismatch"]+=1
print("BIBLAW_062_FOOTNOTES "+json.dumps({"reviewed":len(result),**counts},ensure_ascii=False))
for r in result:
 b=r["best"] or {}
 print("BIBLAW_062_ROW "+json.dumps({"id":r["id"],"page":b.get("pdfPage"),
    "marker":b.get("marker"),"first":b.get("firstTextSimilarity"),
    "exact":r["first_9_words_exact"],"whole":r["identical_normalized_text"],
    "spill":r["probable_extraction_spillover"],"words":b.get("noteFootnoteWords"),
    "pdfTail":b.get("pdfNote","")[-160:],"originalFlags":r["original_060_flags"]},ensure_ascii=False))
print("BIBLAW_062_UNPUBLISHED")
