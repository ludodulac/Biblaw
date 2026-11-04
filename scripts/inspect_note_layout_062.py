#!/usr/bin/env python3
"""BIBLAW-062: focused PDF layout inspection for 72 still-uncertain note IDs.
Uses archived mission 061 evidence as the ONLY candidate list (no re-audit).
Read-only: outputs page layout, punctuation and source evidence; never publishes.
"""
import json,re,sys,unicodedata,collections
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
EVID=Path(sys.argv[1])
pdf=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
reports=json.loads(EVID.read_text(encoding="utf8"))
FIXED={"book-05-psalm-036-note-001","book-22-psalm-150-note-001",
"book-44-psalm-285-note-002","book-44-psalm-285-note-003","book-44-psalm-285-note-004"}
notes=[r for r in reports if r["id"] not in FIXED]
assert len(reports)==77 and len(notes)==72
def norm(t):
 t=unicodedata.normalize("NFD",str(t or "").casefold())
 t="".join(c for c in t if unicodedata.category(c)!="Mn")
 return " ".join(re.findall(r"[a-z0-9]+",t.replace("œ","oe").replace("æ","ae")))
def sample_layout(r):
 page=r["pdf_page_declared"]
 if not isinstance(page,int):return []
 out=[]
 for n in [page-1,page,page+1]:
  if n<1 or n>len(pdf):continue
  p=pdf[n-1];bits=[]
  for b in p.get_text("dict",sort=True)["blocks"]:
   for l in b.get("lines",[]):
    for s in l["spans"]:
     t=s.get("text","").strip()
     if t:bits.append({"text":t,"x":round(s["bbox"][0],1),
     "y":round(s["bbox"][1],1),"size":round(s["size"],1)})
  q=norm(r["source_note_text"]);keys=q.split()
  anchors=[norm(" ".join(keys[k:k+5])) for k in [0,max(0,len(keys)//2),max(0,len(keys)-7)]]
  matches=[]
  for ix,el in enumerate(bits):
   tt=norm(" ".join(x["text"] for x in bits[max(0,ix-1):ix+6]))
   if any(a and (a in tt or (" ".join(a.split()[:3]) in tt)) for a in anchors):
    matches.append({"n":ix,"context":bits[max(0,ix-1):ix+6]})
  out.append({"page":n,"height":round(p.rect.height,1),"blockCount":len(bits),
    "topSamples":bits[:3],"endSamples":bits[-7:],"matchingContexts":matches[:6]})
 return out
for i,r in enumerate(notes):
 r["062_layout_samples"]=sample_layout(r)
 r["062_note_count"]=len(notes)
 # Results remain pending until rigorous boundary and typographical confirmation.
 r["062_status"]="INCERTAINE"
rout=ROOT/"reports/notes-062"
rout.mkdir(parents=True,exist_ok=True)
(rout/"layout-evidence.json").write_text(json.dumps(notes,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BIBLAW_062_SELECTED "+json.dumps({"from_061":len(reports),
 "corrected_061_excluded":len(FIXED),"target":len(notes),
 "missing_page_layout":sum(not r["062_layout_samples"] for r in notes)}))
# Print 12 representative notes, including different books, to read real typography.
selected=[]
for r in notes:
 if len(selected)>=13:break
 if (r["id"] in {"book-07-psalm-035-note-001","book-18-psalm-111-note-001",
 "book-34-psalm-243-note-001","book-23-psalm-133-note-001",
 "book-26-psalm-181-note-002","book-16-psalm-086-note-002"} or
 (len(selected)<3 and r["id"].startswith("book-01"))):
  selected.append(r)
if len(selected)<8:selected+=notes[:8-len(selected)]
for r in selected:
 context=[]
 for page in r["062_layout_samples"]:
  context+=page["matchingContexts"][:2]
 print("BIBLAW_062_SAMPLE "+json.dumps({"id":r["id"],"pdf":r["pdf_page_declared"],
 "textStart":r["source_note_text"][:230],"textEnd":r["source_note_text"][-125:],
 "flags":r["flags_from_060"],"context":context[:5]},ensure_ascii=False))
print("BIBLAW_062_READ_ONLY")
