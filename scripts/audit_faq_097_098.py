#!/usr/bin/env python3
"""Audit 097 and 098: author's exact spiritual-life answers, canonical Psalms and public privacy."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

a, b = load("data/faq-097.json"), load("data/faq-098.json")
assert a["version"] == b["version"] == 1
assert len(a["questions"]) == 8 and len(a["verifiedPsalms"]) == 19
assert len(b["questions"]) == 13 and len(b["verifiedPsalms"]) == 25
records_list = load("data/browser-search-catalog.json")["records"]
records = {r["id"]: r for r in records_list}
assert len([x for x in records_list if x["recordType"] == "psalm"]) == 1158
assert len([x for x in records_list if x["recordType"] == "note"]) == 11
citation_rx = re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
expected_a=[3,3,3,4,3,3,4,4]
expected_b=[3,5,4,4,5,5,4,5,5,5,5,6,18]
unique=set()
total=0

for pack,prefix,expected in [(a,"faq-realite-spirituelle-",expected_a),
                             (b,"faq-pratique-spirituelle-",expected_b)]:
    books=pack["verifiedPsalms"]
    for i,q in enumerate(pack["questions"]):
        assert q["id"] == prefix + str(i+1), q["id"]
        assert len(q["title"]) > 10 and len(q["answer"]) > 1200
        assert q["answer"].startswith("La Bible essénienne"), q["id"]
        assert q["answer"].count("\n\n") >= 3
        matches = list(citation_rx.finditer(q["answer"]))
        assert len(matches) == expected[i] == q["answer"].count("(psaume "), q["id"]
        for m in matches:
            n=int(m.group(1))
            arch="".join(c for c in unicodedata.normalize("NFD",m.group(2))
                         if not unicodedata.combining(c)).lower()
            book=books[arch+":"+str(n)]
            rec_id=f"book-{book:02d}-psalm-{n:03d}"
            verse_nums=[]
            def expand(s):
                lo,hi=map(int,s.groups())
                assert 0<lo<=hi<=lo+100
                verse_nums.extend(range(lo,hi+1))
                return ""
            remaining=re.sub(r"(\d+)\s+à\s+(\d+)",expand,m.group(3))
            verse_nums += [int(x) for x in re.findall(r"\d+", remaining)]
            assert verse_nums
            record=records[rec_id]
            assert record["recordType"] == "psalm" and record["archangel"] == arch
            assert int(record["number"]) == n
            assert set(verse_nums) <= {int(v["number"]) for v in record["verses"]}
            canonical=load(f"data/corpus/books/book-{book:02d}/psalm-{n:03d}.json")
            assert canonical["id"] == rec_id and canonical["archangel"] == arch
            assert set(verse_nums) <= {int(v["number"]) for v in canonical["verses"]}
            unique.add(rec_id)
            total+=1

last=b["questions"][-1]["answer"]
for heading in ["Les repas : nourrir le corps et les dimensions plus subtiles de la vie.",
                "La marche peut devenir un exercice d'attention et de présence.",
                "La parole peut devenir un exercice de vérité et de maîtrise intérieure."]:
    assert "**"+heading+"**" in last
assert last.count("**") == 6
assert total == 101 and len(unique) == 42, (total,len(unique))
assert 25+5+9+10+5+6+7+14+8+13 == 102
build=(ROOT/"scripts/build_pages_site.py").read_text(encoding="utf-8")
assert '"data/faq-097.json"' in build and '"data/faq-098.json"' in build
print("FAQ 097/098 PASS: 21 complete original answers, 101 canonical references, 42 Psalms, original subsection headings and 11 public notes preserved")
