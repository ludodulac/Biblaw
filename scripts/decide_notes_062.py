#!/usr/bin/env python3
"""BIBLAW-062: 72-note editorial evidence decision matrix (NO source edits).

Reuses only archived mission-061 77-note evidence and mission-062 PDF
footnote layout, both from the original PDF in this GitHub repo.
A genuine validation requires note typography, exact marker, reciprocal
canonical psalm, source-page concordance and complete PDF text boundaries.
"""
import json,re,sys,unicodedata,difflib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
old=json.loads(Path(sys.argv[1]).read_text(encoding="utf8"))
layout=json.loads(Path(sys.argv[2]).read_text(encoding="utf8"))
FIXED={"book-05-psalm-036-note-001","book-22-psalm-150-note-001",
"book-44-psalm-285-note-002","book-44-psalm-285-note-003","book-44-psalm-285-note-004"}
targets=[r for r in old if r["id"] not in FIXED]
byid={r["id"]:r for r in layout}
assert len(old)==77 and len(targets)==72 and len(byid)==72
def folded(text):
 t=unicodedata.normalize("NFD",str(text or "").casefold())
 t="".join(c for c in t if unicodedata.category(c)!="Mn")
 return t.replace("œ","oe").replace("æ","ae")
def spans(t):
 return [(folded(m.group()),m.start(),m.end()) for m in re.finditer(r"[^\W_]+",str(t),re.U)]
def key(t):return " ".join(x[0] for x in spans(t))
summary=collections.Counter();rows=[];corrections=[]
for oldrow in targets:
 id=oldrow["id"];source=ROOT/oldrow["source_file"]
 record=json.loads(source.read_text(encoding="utf8"))
 original=record.get("text","")
 proof=byid[id];b=proof.get("best") or {}
 current=spans(original);printed=spans(b.get("pdfNote",""))
 O=[x[0] for x in current];P=[x[0] for x in printed]
 matches=difflib.SequenceMatcher(None,O,P,autojunk=False).get_matching_blocks()
 count=sum(x.size for x in matches)
 coverage=count/len(P) if P else 0
 mapped=[(x.b+j,x.a+j) for x in matches if x.size>0 for j in range(x.size)]
 lastpdf=max((p for p,_ in mapped),default=-100)
 lastorig=max((q for p,q in mapped if p>=len(P)-2),default=-1)
 candidate=(original[:current[lastorig+1][1]].strip() if lastorig+1<len(current) else original.strip()) if lastorig>=0 else ""
 candidate_sim=difflib.SequenceMatcher(None,key(candidate),key(b.get("pdfNote","")),autojunk=False).ratio() if candidate else 0
 contained=key(original)==key(b.get("pdfNote",""))
 marker=int(b.get("marker") or -1)
 ordinal=int(id.rsplit("-note-",1)[1])
 links=bool(proof["canonical_note_id_present"])
 pages=proof["canonical_psalm_pdf_pages"]
 page=int(b["pdfPage"]) if b.get("pdfPage") else None
 page_ok=page in pages
 # Printed note occupies distinct <10pt annotation region at x 56.7,
 # rather than larger 12.5-13pt Psalm lines; match its printed marker.
 layout_confirmed=bool(b and b.get("fontSize",11)<=9.5 and b.get("leftMargin",999)<66
    and b.get("firstTextSimilarity",0)>=.95)
 boundary_confirmed=bool(layout_confirmed and coverage>=.985 and lastpdf>=len(P)-2
    and candidate_sim>=.975 and len(P)>=6 and
    (candidate.endswith((".",":","!","?","»","”",")"))))
 all_verified=layout_confirmed and links and page_ok and marker==ordinal and boundary_confirmed
 if all_verified and contained:
  status="VALIDÉE";reason="PDF: note intégrale en bas de page, typographie distincte, numéro et psaume cohérents"
 elif all_verified and candidate!=original and len(original)-len(candidate)>=9:
  status="CORRIGÉE ET VALIDÉE"
  reason="PDF: fin exacte de la note prouvée avant le texte de psaume parasite"
  corrections.append({"id":id,"path":oldrow["source_file"],"text":candidate,
    "old_chars":len(original),"new_chars":len(candidate),"pdf_page":page,
    "pdf_marker":marker,"source_reciprocal":links,"source_page_match":page_ok,
    "source_words_coverage":round(coverage,3),"confidence":round(candidate_sim,3)})
 else:
  status="INCERTAINE"
  blockers=[]
  if not b:blockers.append("appel de note non identifié dans la mise en page PDF")
  if b and not layout_confirmed:blockers.append("typographie ou début de note non confirmé")
  if b and marker!=ordinal:blockers.append("numéro imprimé différent du numéro JSON")
  if not links:blockers.append("rattachement canonique non réciproque")
  if not page_ok:blockers.append("page PDF non attribuée au psaume")
  if not boundary_confirmed:blockers.append("limites du texte non prouvées")
  reason=" ; ".join(blockers)
 summary[status]+=1
 rows.append({"id":id,"pdf_page":page or oldrow["pdf_page_declared"],
  "flags":oldrow["flags_from_060"],"source_marker":marker if b else None,
  "canonical_psalm":proof["psalm"],"pdf_footnote_size":b.get("fontSize"),
  "pdf_note_excerpt_start":b.get("pdfNote","")[:170],
  "pdf_note_excerpt_end":b.get("pdfNote","")[-180:],
  "source_coverage":round(coverage,3),"boundary_similarity":round(candidate_sim,3),
  "reciprocal_psalm":links,"pdf_page_in_psalm":page_ok,
  "verification":"PDF original : typographie de note, texte imprimé, numéro, fin de note et psaume",
  "possible_edit":"retirer texte étranger après la fin de note" if status=="CORRIGÉE ET VALIDÉE" else "aucune",
  "proof":"PDF p. "+str(page) if page else "PDF p. "+str(oldrow["pdf_page_declared"]),
  "status":status,"reason":reason})
assert len(rows)==72 and len({r["id"] for r in rows})==72
rout=ROOT/"reports/notes-062";rout.mkdir(parents=True,exist_ok=True)
(rout/"decision-proofs.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(rout/"proposed-corrections.json").write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("BIBLAW_062_DECISIONS "+json.dumps({"notes":len(rows),
  "valid":summary["VALIDÉE"],"corrected_proposed":summary["CORRIGÉE ET VALIDÉE"],
  "uncertain":summary["INCERTAINE"],"corrections_not_yet_applied":True}))
for r in rows:
 print("BIBLAW_062_DECISION_ROW "+json.dumps({
  "id":r["id"],"p":r["pdf_page"],"s":r["status"],
  "sim":r["boundary_similarity"],"coverage":r["source_coverage"],
  "reciprocal":r["reciprocal_psalm"],"page":r["pdf_page_in_psalm"],
  "marker":r["source_marker"],"reason":r["reason"][:155]},ensure_ascii=False))
print("BIBLAW_062_CORRECTIONS_JSON "+json.dumps(corrections,ensure_ascii=False))
