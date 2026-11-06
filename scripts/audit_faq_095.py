#!/usr/bin/env python3
"""BIBLAW 095: verify 7 complete owner-authored self-mastery articles and all canonical references."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

addon = load("data/faq-095.json")
assert addon["version"] == 1
questions, books = addon["questions"], addon["verifiedPsalms"]
assert len(questions) == 7 and len(books) == 14
catalog = load("data/browser-search-catalog.json")
records = {r["id"]: r for r in catalog["records"]}
assert len([r for r in records.values() if r["recordType"] == "note"]) == 11

pattern = re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
expected = [3, 3, 3, 3, 4, 4, 5]
link_count, unique = 0, set()
for index, question in enumerate(questions, 1):
    assert question["id"] == f"faq-maitrise-interieure-{index}"
    assert len(question["title"]) > 20 and len(question["answer"]) > 1000
    assert question["answer"].startswith("La Bible essénienne enseigne")
    assert question["answer"].count("\n\n") == (3 if index <= 4 else 4 if index <= 6 else 5)
    citations = list(pattern.finditer(question["answer"]))
    assert len(citations) == question["answer"].count("(psaume ") == expected[index-1], question["id"]
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
            verses.extend(range(lo, hi+1))
            return ""
        remainder = re.sub(r"(\d+)\s+à\s+(\d+)", expand, match.group(3))
        verses.extend(map(int, re.findall(r"\d+", remainder)))
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

assert link_count == 25 and len(unique) == 14
assert len(load("data/faq-public-085.json")["questions"]) + 5 + 9 + 10 + 5 + 6 + len(questions) == 67
assert '"data/faq-095.json"' in (ROOT / "scripts/build_pages_site.py").read_text(encoding="utf-8")
print(f"FAQ 095 PASS: 7 full answers, {link_count} valid references, {len(unique)} canonical Psalms, original paragraphs and 11 public notes preserved")
