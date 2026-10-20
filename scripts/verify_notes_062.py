#!/usr/bin/env python3
"""BIBLAW-062 release guard: source PDF, 72 decisions, 42 exact trims, 30 retained."""
import difflib,json,re,sys,unicodedata
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(Path(p).read_text(encoding="utf8"))
def normalize(s):
 t=unicodedata.normalize("NFD",str(s or "").casefold())
 t="".join(c for c in t if unicodedata.category(c)!="Mn")
 t=t.replace("œ","oe").replace("æ","ae")
 return " ".join(re.findall(r"[a-z0-9]+",t))
folder=Path(sys.argv[1]);footdir=Path(sys.argv[2]);prior=Path(sys.argv[3])
changes=read(folder/"proposed-corrections.json")
foot={r["id"]:r for r in read(footdir/"footnote-boundaries.json")}
report=read(ROOT/"reports/notes-062/decisions.json")
previous={r["id"]:r for r in read(prior/"per-note-proof.json")}
assert len(changes)==42 and len(foot)==72 and len(report["notes"])==72
assert report["summary"]=={"validated":0,"corrected_validated":42,"uncertain":30}
all_by_id={r["id"]:r for r in report["notes"]}
assert len(all_by_id)==72
assert sum(r["status"]=="INCERTAINE" for r in report["notes"])==30
ids={r["id"] for r in changes}
assert sum(r["status"]=="CORRIGÉE ET VALIDÉE" for r in report["notes"])==42
pdf=fitz.open(ROOT/"Bible essénienne (classée par livres).pdf")
assert len(pdf)==4744
for c in changes:
 nid=c["id"];r=foot[nid];d=all_by_id[nid];src=ROOT/c["path"]
 note=read(src);before=previous[nid]["source_note_text"]
 assert note["id"]==nid and note["recordType"]=="note"
 assert note["text"]==c["text"] and before.startswith(note["text"])
 assert len(before)==c["old_chars"] and len(note["text"])==c["new_chars"]
 assert c["new_chars"]<c["old_chars"] and len(before)-len(note["text"])>=9
 assert d["status"]=="CORRIGÉE ET VALIDÉE"
 assert c["source_words_coverage"]>=.985 and c["confidence"]>=.975
 assert r["canonical_note_id_present"] and c["source_reciprocal"]
 bp=r["best"]
 assert bp and bp["marker"]==int(nid.rsplit("-note-",1)[1])
 assert bp["pdfPage"]==c["pdf_page"] and bp["pdfPage"] in r["canonical_psalm_pdf_pages"]
 assert bp["fontSize"]<=9.5 and bp["leftMargin"]<66
 assert normalize(note["text"])==normalize(bp["pdfNote"]),nid
 # Reread actual PDF on the recorded page: lexical proof must still be there.
 actual=normalize(pdf[bp["pdfPage"]-1].get_text(sort=True))
 phrases=normalize(note["text"]).split()
 assert phrases and " ".join(phrases[:min(8,len(phrases))]) in actual,(nid,"prefix missing")
 # Long notes sometimes contain line-end hyphenation; the independent
 # layout proof above requires their precise footnote text.
 assert note.get("validation",{}).get("status")=="machine-extracted-needs-review"
for id,r in all_by_id.items():
 if r["status"]!="INCERTAINE":continue
 p=ROOT/previous[id]["source_file"]
 assert read(p)["text"]==previous[id]["source_note_text"],id
assert len([x for x in all_by_id if x not in ids])==30
catalog=read(ROOT/"data/catalog.json")
assert len([p for p in catalog["records"] if p.startswith("data/notes/")])==11
assert not any(p.startswith("data/notes/books/") for p in catalog["records"])
bundle=read(ROOT/"data/browser-search-catalog.json")
rows=bundle["records"]
counts={k:sum(r["recordType"]==k for r in rows) for k in ("psalm","master-prayer","note")}
assert counts=={"psalm":1158,"master-prayer":676,"note":11},counts
assert "data/notes/books/" not in str(bundle)[:10000]
print("BIBLAW-062 VERIFIED 72/72 corrected=42 uncertain=30 published=0")
print("BIBLAW-062 PDF FOOTNOTE EXACT 42/42; SOURCE META/PSALM LINKS 42/42")
print("BIBLAW-062 GUARDED psalms=1158 prayers=676 public_notes=11")
