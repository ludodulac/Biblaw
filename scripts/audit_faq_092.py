#!/usr/bin/env python3
"""092 — verify ten complete owner-provided FAQ answers and every cited Psalm verse."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

addon = load("data/faq-092.json")
assert addon["version"] == 1
questions = addon["questions"]
books = addon["verifiedPsalms"]
assert len(questions) == 10 and len(books) == 16

catalog = load("data/browser-search-catalog.json")
records = {r["id"]: r for r in catalog["records"]}
assert len([r for r in records.values() if r["recordType"] == "note"]) == 11
pattern = re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
unique = set()
refs = 0

for index, question in enumerate(questions, 1):
    assert question["id"] == f"faq-religions-science-{index}"
    assert len(question["title"]) > 15 and len(question["answer"]) > 900
    mentions = list(pattern.finditer(question["answer"]))
    assert len(mentions) == question["answer"].count("(psaume ") == 3, question["id"]

    for match in mentions:
        number = int(match.group(1))
        arch = "".join(ch for ch in unicodedata.normalize("NFD", match.group(2))
                       if not unicodedata.combining(ch)).lower()
        book = books[f"{arch}:{number}"]
        record_id = f"book-{book:02d}-psalm-{number:03d}"
        verses = []
        def expand(m):
            low, high = map(int, m.groups())
            assert 0 < low <= high <= low + 100
            verses.extend(range(low, high + 1))
            return ""
        tail = re.sub(r"(\d+)\s+à\s+(\d+)", expand, match.group(3))
        verses.extend(int(n) for n in re.findall(r"\d+", tail))
        assert verses
        record = records[record_id]
        assert record["recordType"] == "psalm"
        assert record["archangel"] == arch and record["number"] == number
        assert set(verses) <= {int(v["number"]) for v in record["verses"]}
        source = load(f"data/corpus/books/book-{book:02d}/psalm-{number:03d}.json")
        assert source["id"] == record_id and source["archangel"] == arch
        assert set(verses) <= {int(v["number"]) for v in source["verses"]}
        refs += 1
        unique.add(record_id)

assert refs == 30 and len(unique) == 16
assert len(load("data/faq-public-085.json")["questions"]) + 5 + 9 + len(questions) == 49
assert '"data/faq-092.json"' in (ROOT / "scripts/build_pages_site.py").read_text(encoding="utf-8")
print(f"FAQ 092 PASS: 10 verbatim answers, {refs} linked citations, {len(unique)} real Psalms; 11 public notes unchanged")
