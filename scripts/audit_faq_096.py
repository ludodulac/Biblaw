#!/usr/bin/env python3
"""BIBLAW 096: check fourteen owner-authored harmony and consciousness answers in canonical corpus."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

payload = load("data/faq-096.json")
assert payload["version"] == 1
questions, books = payload["questions"], payload["verifiedPsalms"]
assert len(questions) == 14 and len(books) == 28
record_list = load("data/browser-search-catalog.json")["records"]
records = {r["id"]: r for r in record_list}
assert len([r for r in record_list if r["recordType"] == "note"]) == 11
assert len([r for r in record_list if r["recordType"] == "psalm"]) == 1158
pattern = re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
expected = [4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 5]
link_count, unique = 0, set()

for i, q in enumerate(questions):
    assert q["id"] == f"faq-harmonie-conscience-{i+1}"
    assert len(q["title"]) > 15 and len(q["answer"]) > 1500
    assert q["answer"].startswith("La Bible essénienne")
    assert q["answer"].count("\n\n") == (5 if i == 13 else 4), q["id"]
    if i == 6:
        assert q["answer"].endswith("à la vie et aux autres.")
        assert "16. Qu'est-ce que" not in q["answer"], "Second topic must be a separate FAQ"
    citations = list(pattern.finditer(q["answer"]))
    assert len(citations) == q["answer"].count("(psaume ") == expected[i], q["id"]
    for citation in citations:
        number = int(citation.group(1))
        arch = "".join(c for c in unicodedata.normalize("NFD", citation.group(2))
                       if not unicodedata.combining(c)).lower()
        book = books[f"{arch}:{number}"]
        record_id = f"book-{book:02d}-psalm-{number:03d}"
        verses = []
        def expand_range(m):
            start, end = map(int, m.groups())
            assert 0 < start <= end <= start + 100
            verses.extend(range(start, end + 1))
            return ""
        remaining = re.sub(r"(\d+)\s+à\s+(\d+)", expand_range, citation.group(3))
        verses.extend(int(n) for n in re.findall(r"\d+", remaining))
        assert verses
        record = records[record_id]
        assert record["recordType"] == "psalm"
        assert record["archangel"] == arch and record["number"] == number
        assert set(verses) <= {int(v["number"]) for v in record["verses"]}, citation.group(0)
        source = load(f"data/corpus/books/book-{book:02d}/psalm-{number:03d}.json")
        assert source["id"] == record_id and source["archangel"] == arch
        assert set(verses) <= {int(v["number"]) for v in source["verses"]}
        unique.add(record_id)
        link_count += 1

assert link_count == 55 and len(unique) == 28
assert len(load("data/faq-public-085.json")["questions"]) + 5 + 9 + 10 + 5 + 6 + 7 + len(questions) == 81
assert '"data/faq-096.json"' in (ROOT / "scripts/build_pages_site.py").read_text(encoding="utf-8")
print(f"FAQ 096 PASS: 14 complete original answers, {link_count} canonical references across {len(unique)} Psalms; 11 public notes unchanged")
