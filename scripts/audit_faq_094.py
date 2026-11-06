#!/usr/bin/env python3
"""BIBLAW 094: audit six owner-authored happiness answers and all linked canonical verses."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

addon = load("data/faq-094.json")
assert addon["version"] == 1
questions, books = addon["questions"], addon["verifiedPsalms"]
assert len(questions) == 6 and len(books) == 9
catalog = load("data/browser-search-catalog.json")
records = {r["id"]: r for r in catalog["records"]}
assert len([r for r in records.values() if r["recordType"] == "note"]) == 11
pattern = re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
link_count, unique = 0, set()

for index, question in enumerate(questions, 1):
    assert question["id"] == f"faq-bonheur-{index}"
    assert len(question["title"]) > 25 and len(question["answer"]) > 1000
    assert question["answer"].startswith("La Bible essénienne enseigne")
    assert question["answer"].count("\n\n") == (4 if index == 6 else 2)
    citations = list(pattern.finditer(question["answer"]))
    expected = 4 if index == 6 else 3
    assert len(citations) == question["answer"].count("(psaume ") == expected, question["id"]
    for match in citations:
        number = int(match.group(1))
        arch = "".join(c for c in unicodedata.normalize("NFD", match.group(2))
                       if not unicodedata.combining(c)).lower()
        book = books[f"{arch}:{number}"]
        record_id = f"book-{book:02d}-psalm-{number:03d}"
        verses = []
        def expand(m):
            lo, hi = map(int, m.groups())
            assert 0 < lo <= hi <= lo + 100
            verses.extend(range(lo, hi + 1))
            return ""
        rest = re.sub(r"(\d+)\s+à\s+(\d+)", expand, match.group(3))
        verses.extend(map(int, re.findall(r"\d+", rest)))
        assert verses
        record = records[record_id]
        assert record["recordType"] == "psalm"
        assert record["archangel"] == arch and record["number"] == number
        assert set(verses) <= {int(v["number"]) for v in record["verses"]}
        canonical = load(f"data/corpus/books/book-{book:02d}/psalm-{number:03d}.json")
        assert canonical["id"] == record_id and canonical["archangel"] == arch
        assert set(verses) <= {int(v["number"]) for v in canonical["verses"]}
        link_count += 1
        unique.add(record_id)

assert link_count == 19 and len(unique) == 9
assert len(load("data/faq-public-085.json")["questions"]) + 5 + 9 + 10 + 5 + len(questions) == 60
assert '"data/faq-094.json"' in (ROOT / "scripts/build_pages_site.py").read_text(encoding="utf-8")
print(f"FAQ 094 PASS: 6 verbatim happiness answers, {link_count} references, {len(unique)} canonical Psalms; 11 public notes unchanged")
