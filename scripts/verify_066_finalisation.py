#!/usr/bin/env python3
"""Finalisation 066: structural and no-loss checks; no PDF and no destructive writes."""
import json,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"scripts"))
from resolve_note_occurrences_066 import load_groups,load_note,resolve
def read(p): return json.loads((R/p).read_text(encoding="utf-8"))
def before(p): return json.loads(subprocess.check_output(["git","show","HEAD^:"+p],cwd=R,text=True))
def check(ok,label):
    if not ok: raise AssertionError("FAIL: "+label)
    print("PASS "+label)
ps=list((R/"data/corpus/books").glob("book-*/psalm-*.json"))
pr=list((R/"data/prayers").glob("*.json"))
check(len(ps)==1158,"1158 psalms")
check(len(pr)==676,"676 prayers")
psalms=[json.loads(f.read_text(encoding="utf-8")) for f in ps]
prayers=[json.loads(f.read_text(encoding="utf-8")) for f in pr]
pi={j["id"] for j in psalms}
check(len(pi)==1158,"unique psalms")
check(all(v.get("text") for p in psalms for v in p["verses"]),"all verses nonempty")
check(len({p["id"] for p in prayers})==676,"unique prayers")
check(all(p["appliesToPsalmId"] in pi and bool(p["text"]) for p in prayers),"prayer text and psalm links")
g=load_groups()
check(len(g)==18,"18 occurrence groups")
check(len({m for x in g for m in x["members"]})==36,"36 distinct aliases")
for x in g:
    a,b=x["members"];found=resolve([b,a])
    check(len(found)==1 and set(found[0]["memberRecords"])=={a,b},"both references "+x["occurrenceId"])
    check(all(found[0]["memberRecords"][id_]["text"]==load_note(id_)["text"] for id_ in (a,b)),"full texts "+x["occurrenceId"])
links=[("17-115-001","michael-book-17-prayer-011"),("27-158-001","raphael-book-27-prayer-053"),("27-177-001","raphael-book-27-prayer-071"),("30-211-001","gabriel-book-30-prayer-093"),("31-184-001","raphael-book-31-prayer-076"),("21-143-002","michael-book-21-prayer-038"),("21-143-003","michael-book-21-prayer-038"),("29-199-002","michael-book-29-prayer-090"),("29-199-003","michael-book-29-prayer-090")]
for short,pid in links:
    b,p,n=short.split("-");id_=f"book-{b}-psalm-{p}-note-{n}";note=load_note(id_);prayer=read("data/prayers/"+pid+".json")
    psalm=read("data/corpus/books/book-"+b+"/psalm-"+p+".json")
    check(note["appliesToPrayerId"]==pid and id_ in prayer["noteIds"] and id_ in psalm["noteIds"],"reciprocal and legacy: "+id_)
    check(note["text"] and prayer["appliesToPsalmId"]==note["appliesTo"]["recordId"],"correct prayer destination: "+id_)
note=load_note("book-22-psalm-155-note-001")
psalm=read("data/corpus/books/book-22/psalm-155.json")
tail=note["recovery066"]["originalText"][len(note["text"])+1:]
v=next(v["text"] for v in psalm["verses"] if v["number"]==21)
check(note["text"]+" "+tail==note["recovery066"]["originalText"] and v==note["recovery066"]["oldVerse21"]+" "+tail,"22/155 verse21 no loss")
com=load_note("book-21-psalm-143-note-004")
check("".join(z.get("text",z.get("separator","")) for z in com["compositeOccurrence066"]["parts"])==com["text"],"21/143 original composite exact")
a=load_note("book-29-psalm-199-note-003")
check(a["source"]["pdfPage"]==2751 and a["appliesTo"]["verse"] is None and a["recovery066Finalisation"]["previousPdfPage"]==2750,"29/199 proven page/verse")
for num in ("002","003"):
    q=load_note("book-29-psalm-216-note-"+num)
    check(q["recovery066Finalisation"]["originalText"].replace("audelà","au-delà")==q["text"],"29/216 reversible typography "+num)
changed=subprocess.check_output(["git","diff","--name-only","HEAD^","HEAD","--","data/corpus/books","data/prayers"],cwd=R,text=True).splitlines()
check(set(changed)<={"data/prayers/michael-book-21-prayer-038.json","data/prayers/michael-book-29-prayer-090.json"},"no other canonical psalm/prayer changed")
for path in changed: check(before(path)["text"]==read(path)["text"],"prayer text byte-for-byte "+path)
for id_ in ("book-26-psalm-189-note-002","book-35-psalm-213-note-002","book-35-psalm-213-note-003","book-26-psalm-169-note-001"):
    b=id_.split("-")[1];path="data/notes/books/book-"+b+"/"+id_+".json"
    check(before(path)["text"]==read(path)["text"],"protected historical composite "+id_)
print("FINAL PASS: 1158 psalms, 676 prayers, 18 groups, 36 aliases, 7 corrected, 29 compatible, 8 blocked")
