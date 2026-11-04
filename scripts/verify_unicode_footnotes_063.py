#!/usr/bin/env python3
"""BIBLAW 063 — validate printed footnote boundaries, including Unicode hyphen.
Target 30 previously uncertain notes plus 3 book-44 notes. Reuse 062 decisions
and mission-063 source-layout evidence; DO NOT edit notes or publish anything.
"""
import fitz,json,re,unicodedata,collections
from pathlib import Path

R=Path(__file__).resolve().parents[1]
prior=json.loads((R/"reports/notes-062/decisions.json").read_text(encoding="utf8"))["notes"]
uncertain=[x for x in prior if x["status"]=="INCERTAINE"]
special=[f"book-44-psalm-285-note-{i:03d}" for i in (2,3,4)]
ids=[x["id"] for x in uncertain]+special
assert len(ids)==33 and len(set(ids))==33
pdf=fitz.open(R/"Bible essénienne (classée par livres).pdf")
assert len(pdf)==4744
dash=r"[-‐‑‒–—−]"
noteStart=re.compile(rf"^\s*(\d{{1,2}})\s*{dash}\s*",re.U)
def tokens(s):
 s=unicodedata.normalize("NFD",str(s or "").casefold())
 s="".join(x for x in s if unicodedata.category(x)!="Mn")
 s=s.replace("œ","oe").replace("æ","ae")
 return re.findall(r"[a-z0-9]+",s)
def raw_tokens(text):
 out=[]
 for m in re.finditer(r"[^\W_]+",str(text or ""),re.U):
  tok=tokens(m.group())
  if tok:
   for v in tok:out.append((v,m.start(),m.end()))
 return out
def pdf_spans(n):
 result=[]
 for bl in pdf[n-1].get_text("dict",sort=True)["blocks"]:
  for line in bl.get("lines",[]):
   spans=line.get("spans",[])
   if not spans:continue
   s="".join(v["text"] for v in spans).strip()
   if s:
    result.append({"text":s,"y":min(v["bbox"][1] for v in spans),
      "x":min(v["bbox"][0] for v in spans),
      "size":max(v["size"] for v in spans)})
 return result
cache={}
def spans(p):
 if p not in cache:cache[p]=pdf_spans(p)
 return cache[p]
def footnotes(page):
 lines=spans(page);out=[]
 for ix,ln in enumerate(lines):
  m=noteStart.match(ln["text"])
  if not m or ln["size"]>10.5 or ln["size"]<7 or ln["x"]>85:continue
  body=[ln["text"][m.end():]]
  last_y=ln["y"]
  for li in lines[ix+1:]:
   if li["y"]<=last_y:continue
   if li["y"]-last_y>15.5:break
   if not (7<=li["size"]<=10.5 and 50<=li["x"]<=115):break
   if noteStart.match(li["text"]):break
   body.append(li["text"]);last_y=li["y"]
  text=" ".join(body).strip()
  if text:out.append({"page":page,"marker":int(m[1]),"text":text,
   "fontSize":round(ln["size"],2),"startY":round(ln["y"],1),
   "startX":round(ln["x"],1),"lines":len(body)})
 return out
rows=[]
for id in ids:
 b,p,n=map(int,re.fullmatch(r"book-(\d+)-psalm-(\d+)-note-(\d+)",id).groups())
 path=R/"data/notes/books"/f"book-{b:02d}"/(id+".json")
 j=json.loads(path.read_text(encoding="utf8"))
 assert j["id"]==id
 target=R/"data/corpus/books"/f"book-{b:02d}"/f"psalm-{p:03d}.json"
 psalm=json.loads(target.read_text(encoding="utf8"))
 source=j["text"];sourceTokens=raw_tokens(source);sourceWords=[x[0] for x in sourceTokens]
 page=j["source"].get("pdfPage")
 canonPages=psalm["source"]["pdfPages"]
 candidates=[]
 for pp in sorted(set(range(max(1,page-6),min(len(pdf),page+6)+1))|set(canonPages)):
  for printed in footnotes(pp):
   w=tokens(printed["text"])
   ncommon=0
   for a,bb in zip(sourceWords,w):
    if a!=bb:break
    ncommon+=1
   prefix=round(ncommon/max(1,min(12,len(w),len(sourceWords))),3)
   # Only accept concrete shared beginning (both long or short note).
   if ncommon>=min(3,len(w)) and prefix>=.85:
    endIndex=sourceTokens[ncommon][1] if ncommon<len(sourceTokens) else len(source)
    recovered=source[:endIndex].rstrip()
    candidates.append({**printed,"printedWords":len(w),
     "commonStartWords":ncommon,"sourceWords":len(sourceWords),
     "prefixConfidence":prefix,
     "printedFullyInSource":ncommon==len(w),
     "pdfFootnoteEndsSentence":bool(re.search(r'[.!?。»”)"\]]\s*$',printed["text"])),
     "prefixFromSource":recovered,"wordExact":tokens(recovered)==w,
     "pdfPageInCanonicalPsalm":pp in canonPages,
     "markerMatchesPrintedSource":printed["marker"]==j["appliesTo"]["marker"],
     "sourceSpilloverCharacters":len(source)-len(recovered)})
 candidates.sort(key=lambda x:(x["commonStartWords"],x["prefixConfidence"],
    x["printedFullyInSource"],-abs(x["page"]-page)),reverse=True)
 best=candidates[0] if candidates else None
 rows.append({"id":id,"sourceFile":str(path.relative_to(R)),
  "sourcePdfPage":page,"printedMarkerRecorded":j["appliesTo"]["marker"],
  "ordinalInId":n,"sourcePsalm":j["appliesTo"]["recordId"],
  "canonicalPsalmPdfPages":canonPages,"reciprocal":id in psalm.get("noteIds",[]),
  "originalText":source,"best":best,
  "alternates":candidates[:4],"status":"INCERTAINE"})
# If one PDF page, same marker and exact note text is claimed by multiple
# JSON records, none can be validated independently until numbering resolved.
groups=collections.defaultdict(list)
for row in rows:
 b=row["best"]
 if b:groups[(b["page"],b["marker"],tuple(tokens(b["text"])))].append(row["id"])
counter=collections.Counter()
for row in rows:
 b=row["best"]
 duplicates=groups.get((b["page"],b["marker"],tuple(tokens(b["text"]))),[]) if b else []
 row["samePrintedNoteClaimedBy"]=duplicates
 allow=bool(b and row["reciprocal"] and len(duplicates)==1
    and b["pdfPageInCanonicalPsalm"] and b["markerMatchesPrintedSource"]
    and b["printedFullyInSource"] and b["wordExact"] and
    b["pdfFootnoteEndsSentence"] and b["fontSize"]<=10.5)
 row["proofComplete"]=allow
 if allow:
  row["status"]="VALIDÉE" if b["sourceSpilloverCharacters"]==0 else "CORRIGÉE ET VALIDÉE"
  row["correctedTextProof"]=b["prefixFromSource"]
 else:row["status"]="INCERTAINE"
 counter[row["status"]]+=1
out=R/"reports/notes-063";out.mkdir(exist_ok=True,parents=True)
(out/"unicode-footnote-decisions.json").write_text(
 json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BIBLAW_063_UNICODE_SUMMARY "+json.dumps({"targeted":len(rows),
 "valid":counter["VALIDÉE"],"corrected_candidate":counter["CORRIGÉE ET VALIDÉE"],
 "uncertain":counter["INCERTAINE"],"auto_edits":0,"published":0}))
for row in rows:
 b=row["best"] or {}
 print("BIBLAW_063_UNICODE_ROW "+json.dumps({"id":row["id"],"status":row["status"],
   "pdf":b.get("page"),"original":row["sourcePdfPage"],
   "marker":b.get("marker"),"font":b.get("fontSize"),
   "end":b.get("text","")[-105:],"words":b.get("printedWords"),
   "startWords":b.get("commonStartWords"),
   "prefixExact":b.get("printedFullyInSource"),"endsSentence":b.get("pdfFootnoteEndsSentence"),
   "spill":b.get("sourceSpilloverCharacters"),"reciprocal":row["reciprocal"],
   "onPsalm":b.get("pdfPageInCanonicalPsalm"),"duplicateWith":row["samePrintedNoteClaimedBy"]},
 ensure_ascii=False))
print("BIBLAW_063_UNICODE_READ_ONLY")
