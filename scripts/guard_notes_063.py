#!/usr/bin/env python3
"""BIBLAW 063 release guard — uses immutable PDF evidence from targeted 063 run.
No 060/061/062 re-audits. Verifies all 33 outcomes + 11 exact edits, protects
previous corrections, canonical corpus and publicly indexed notes.
"""
import json,re,sys,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(sys.argv[1])/"unicode-footnote-decisions.json"
baseline=json.loads(SOURCE.read_text(encoding="utf8"))
ledger=json.loads((ROOT/"reports/notes-063/decisions.json").read_text(encoding="utf8"))
byid={x["id"]:x for x in baseline}
rows=ledger["rows"];ids={r["id"] for r in rows}
assert len(baseline)==len(rows)==len(ids)==33
assert ledger["counts"]=={"reviewed":33,"previously_uncertain":30,
 "book44_separate":3,"validated":1,"corrected_and_validated":10,
 "uncertain":22,"source_notes_edited":11,"published":0}
def norm(s):
 s=unicodedata.normalize("NFD",str(s or "").casefold())
 s="".join(c for c in s if unicodedata.category(c)!="Mn")
 s=s.replace("œ","oe").replace("æ","ae")
 return re.findall(r"[a-z0-9]+",s)
def load(p):return json.loads(Path(p).read_text(encoding="utf8"))
validated=corrected=uncertain=changed=0
for row in rows:
 id=row["id"];old=byid[id]
 file=ROOT/old["sourceFile"];src=load(file)
 assert src["id"]==id and src["recordType"]=="note"
 state=row["status"]
 assert src.get("validation",{}).get("status")=="machine-extracted-needs-review"
 b=old["best"]
 if state=="CORRIGÉE ET VALIDÉE":
  corrected+=1;changed+=1
  assert b and old["proofComplete"] and old["reciprocal"]
  assert old["sourcePdfPage"] in old["canonicalPsalmPdfPages"]
  assert b["marker"]==old["printedMarkerRecorded"]
  assert src["text"]==old["correctedTextProof"] and old["originalText"].startswith(src["text"])
  assert norm(src["text"])==norm(b["text"])
  assert len(src["text"])<len(old["originalText"])
 elif state=="VALIDÉE":
  validated+=1
  assert b and old["proofComplete"] and old["reciprocal"]
  assert src["text"]==old["originalText"]
  assert norm(src["text"])==norm(b["text"])
 elif state=="INCERTAINE":
  uncertain+=1
  if id=="book-44-psalm-285-note-001":
   changed+=1
   assert b and not old["reciprocal"]
   assert src["text"]==b["prefixFromSource"]
   assert norm(src["text"])==norm(b["text"])
   assert len(src["text"])<len(old["originalText"])
  else:
   assert src["text"]==old["originalText"],"Unproven note modified: "+id
 else:raise AssertionError((id,state))
 if state!="INCERTAINE":
  assert row["correction"]!="Aucune" or state=="VALIDÉE"
  psid=old["sourcePsalm"]
  m=re.fullmatch(r"book-(\d+)-psalm-(\d+)",psid)
  assert m
  ps=load(ROOT/"data/corpus/books"/f"book-{m[1]}"/f"psalm-{m[2]}.json")
  assert id in ps.get("noteIds",[])
  assert b["page"] in ps["source"]["pdfPages"]
  for otherid in ps["noteIds"]:
   if otherid==id:continue
   path=ROOT/"data/notes/books"/f"book-{m[1]}"/(otherid+".json")
   if not path.exists():continue
   sibling=load(path)
   if sibling["source"].get("pdfPage")!=b["page"] or sibling["appliesTo"].get("marker")!=b["marker"]:continue
   assert norm(sibling.get("text",""))[:8]!=norm(old["originalText"])[:8],(id,otherid,"same footnote elsewhere in Psalm")
assert (validated,corrected,uncertain,changed)==(1,10,22,11)
for special in (2,3,4):
 id=f"book-44-psalm-285-note-{special:03d}"
 assert next(x for x in rows if x["id"]==id)["status"]=="INCERTAINE"
 assert not byid[id]["reciprocal"]
 # Preserve all PDF-confirmed mission 061 corrections exactly.
 assert load(ROOT/byid[id]["sourceFile"])["text"]==byid[id]["originalText"]
catalog=load(ROOT/"data/catalog.json")
assert len([p for p in catalog["records"] if p.startswith("data/notes/")])==11
assert not any("data/notes/books/" in p for p in catalog["records"])
browser=load(ROOT/"data/browser-search-catalog.json")
cnt={type_:sum(rec["recordType"]==type_ for rec in browser["records"])
     for type_ in ("psalm","master-prayer","note")}
assert cnt=={"psalm":1158,"master-prayer":676,"note":11},cnt
assert len(list((ROOT/"data/notes/books").glob("*/*-note-*.json")))==280
old062=load(ROOT/"reports/notes-062/decisions.json")
assert sum(x["status"]=="CORRIGÉE ET VALIDÉE" for x in old062["notes"])==42
print("BIBLAW-063 VALIDATED 33/33 | VALIDÉE=1 | CORRIGÉE ET VALIDÉE=10 | INCERTAINE=22")
print("BIBLAW-063 PDF-BACKED NOTES CHANGED 11 | DUPLICATE CLAIMS HELD | BOOK44 UNATTACHED")
print("BIBLAW-063 GUARDED psalms=1158 prayers=676 public_notes=11 extracted=280")
print("BIBLAW-063 PUBLISH=0 MERGE=0 DEPLOY=0")
