#!/usr/bin/env python3
"""063 follow-up: inspect ONLY 13 ambiguous starts and 3 separate book-44 notes.
Reader output reproduces actual original PDF typography near source pages;
no repeated audits, no changes to any source.
"""
import fitz,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ev=json.loads(Path("reports/notes-062/decisions.json").read_text(encoding="utf8"))
unc=[r for r in ev["notes"] if r["status"]=="INCERTAINE"]
note_ids=[
"book-08-psalm-050-note-001","book-16-psalm-086-note-002",
"book-20-psalm-104-note-001","book-20-psalm-109-note-001","book-20-psalm-124-note-002",
"book-21-psalm-150-note-001","book-23-psalm-133-note-003",
"book-28-psalm-158-note-001","book-30-psalm-193-note-001",
"book-31-psalm-201-note-002","book-31-psalm-201-note-003",
"book-32-psalm-203-note-001","book-36-psalm-233-note-001",
"book-44-psalm-285-note-001","book-44-psalm-285-note-002",
"book-44-psalm-285-note-003","book-44-psalm-285-note-004"]
assert len(unc)==30 and len(note_ids)==17
pdf=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
def spans(pg):
 ret=[]
 for block in pdf[pg-1].get_text("dict",sort=True)["blocks"]:
  for line in block.get("lines",[]):
   s=line.get("spans",[])
   if not s:continue
   text="".join(x["text"] for x in s).strip()
   if text:ret.append({"text":text,"x":round(min(x["bbox"][0] for x in s),1),
       "y":round(min(x["bbox"][1] for x in s),1),
       "size":round(max(x["size"] for x in s),1)})
 return ret
records=[]
for ident in note_ids:
 book=ident[5:7]
 v=json.loads((ROOT/"data/notes/books"/("book-"+book)/(ident+".json")).read_text(encoding="utf8"))
 base=v["source"]["pdfPage"]
 pages=sorted(set([base-1,base,base+1]))
 if ident.startswith("book-44"):
  pages=list(range(max(1,base-2),min(4744,base+1)+1))
 report={"id":ident,"sourcePage":base,"sourceTextStart":v["text"][:140],
  "sourceTextEnd":v["text"][-140:],"pages":[]}
 for pg in pages:
  rows=spans(pg)
  bottom=[x for x in rows if x["y"]>450 and x["size"]<11]
  superscript=[x for x in rows if x["size"]<=9 and x["y"]>160]
  headings=[x for x in rows if x["size"]>=15 and x["y"]<255]
  report["pages"].append({"page":pg,"headings":headings[:10],
    "pageStart":rows[:8],
    "bottomFootnoteCandidates":bottom[-22:],
    "smallFontLines":superscript[-18:]})
 records.append(report)
out=ROOT/"reports/notes-063";out.mkdir(exist_ok=True,parents=True)
(out/"page-typography-supplement.json").write_text(
 json.dumps(records,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BIBLAW_063_TYPOGRAPHY "+json.dumps({"cases":len(records),
  "pages":sum(len(x["pages"]) for x in records)},ensure_ascii=False))
for r in records:
 print("BIBLAW_063_TYPOROW "+json.dumps({"id":r["id"],
  "source":r["sourcePage"],
  "pages":[{"p":p["page"],
    "heading":[x["text"] for x in p["headings"][:4]],
    "printedNotes":[x["text"][:240] for x in p["bottomFootnoteCandidates"] if re.match(r"^\d+\s*[-–—]",x["text"])][:6],
    "lastSmallText":[x["text"] for x in p["smallFontLines"][-4:]]} for p in r["pages"]]},ensure_ascii=False))
print("BIBLAW_063_NO_DOCUMENT_MUTATION")
