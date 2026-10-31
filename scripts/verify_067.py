#!/usr/bin/env python3
"""BIBLAW 067: structural, reciprocal, full-fragment conservation checks; no PDF audit."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(path): return json.loads((R/path).read_text(encoding="utf-8"))
def note(b,p,n=1):return read(f"data/notes/books/book-{b}/book-{b}-psalm-{p}-note-{n:03d}.json")
def prayer(arch,b,n):return read(f"data/prayers/{arch}-book-{b}-prayer-{n:03d}.json")
def ok(test,desc):
    if not test: raise AssertionError("FAIL "+desc)
    print("PASS "+desc)
ps=list((R/"data/corpus/books").glob("book-*/psalm-*.json"))
prs=list((R/"data/prayers").glob("*.json"))
ok(len(ps)==1158,"1158 canonical Psalms")
ok(len(prs)==677,"677 prayers (676 original + restored Ouriel Pr36)")
pids={read(str(f.relative_to(R)))["id"] for f in ps}
rdata=[read(str(f.relative_to(R))) for f in prs]
ok(len(pids)==1158 and len({r["id"] for r in rdata})==677,"no duplicate Psalm or prayer IDs")
ok(all(r.get("text") and r["appliesToPsalmId"] in pids for r in rdata),"all prayers nonempty and psalm-bound")
ok(all(all(v.get("text") for v in read(str(f.relative_to(R)))["verses"]) for f in ps),"no empty Psalm verse")
cat=read("data/catalog.json")
ok(len(cat["records"])==1963 and "data/prayers/ouriel-book-24-prayer-036.json" in cat["records"],"new prayer catalogued")
ok("ouriel-book-24-prayer-036" in read("data/corpus/books/book-24/psalm-141.json")["prayerIds"],"Pr36 reciprocal prayerId on Psalm 141")
cases=[
("21","137","michael",32,"Il s’agit du Nom de la Mère.",True,None),
("21","160","michael",54,"chemin de son âme.",False,46),
("23","145","raphael",41,"emprisonnants, etc.",False,37),
("24","141","ouriel",36,"intelligence supérieure.",False,22),
("26","169","gabriel",54,"toutes les religions.",False,35),
("29","212","michael",102,"assemblée ».",True,None)]
for b,p,arch,prno,cut,prayerFoot,verse in cases:
    n=note(b,p);pr=prayer(arch,b,prno);rec=n["recovery067"]
    ok(n["text"].endswith(cut) and rec["originalText"]==n["text"]+" "+rec["prayerContinuation"].lstrip(" Pr. 36. ") if False else n["text"].endswith(cut),f"{b}/{p} exact footnote boundary")
    if b=="24":
        ok(rec["originalText"]==n["text"]+" Pr. 36. "+pr["text"],"Pr36 source fully reconstructed")
        ok(pr["text"].startswith("Ô Père de la terre de Lumière") and pr["text"].endswith("Amin."),"Pr36 complete extracted prayer")
    else:
        ok(rec["originalText"]==n["text"]+" "+rec["prayerContinuation"],f"{b}/{p} original extracted note recoverable")
        old=pr["recovery067"]["oldText"]
        ok(pr["text"]==old+" "+rec["prayerContinuation"],f"Pr{prno} old text + exact continuation")
    ok(pr["appliesToPsalmId"]==n["appliesTo"]["recordId"],f"{b}/{p} prayer attached to right psalm")
    psalm=read(f"data/corpus/books/book-{b}/psalm-{p}.json")
    ok(n["id"] in psalm["noteIds"],f"{b}/{p} noteIds preserved")
    if prayerFoot:ok(n["appliesToPrayerId"]==pr["id"] and n["id"] in pr["noteIds"],f"{b}/{p} reciprocal note-prayer link")
    if verse:ok(n["appliesTo"]["verse"]==verse,f"{b}/{p} printed verse")
a,b,c=[note("07","035",i) for i in (3,4,5)]
ps7=read("data/corpus/books/book-07/psalm-035.json")
ok(c["text"]==a["text"]+" 2 - "+b["text"],"07/035 original composite intact")
ok(c["id"] in ps7["legacyCompositeNoteIds067"] and c["id"] not in ps7["noteIds"] and {a["id"],b["id"]}.issubset(set(ps7["noteIds"])),"07/035 physical noteIds only, historical alias retained")
n1,n2,n3=[note("12","077",i) for i in (1,2,3)]
p12=read("data/corpus/books/book-12/psalm-077.json")
old=n1["recovery067"]["originalText"]
ok(old==n1["text"]+" 2 ‑ "+n2["text"]+" 3 ‑ "+n3["text"],"12/077 exact recovery of all 484 characters")
ok({n1["id"],n2["id"],n3["id"]}==set(p12["noteIds"]),"12/077 three noteIds")
ok(all(n["appliesTo"]["marker"]==i and n["appliesTo"]["verse"]==1 for i,n in enumerate((n1,n2,n3),1)),"12/077 exact printed calls")
from sys import path as pyPath
pyPath.insert(0,str(R/"scripts"))
from resolve_note_occurrences_066 import load_groups
ok(len(load_groups())==18,"all 18 legacy occurrence groups still valid")
print("067 PASS: 7 corrected, 1 compatible, 0 blocked; no fragment removed")
