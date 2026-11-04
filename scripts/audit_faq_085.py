#!/usr/bin/env python3
"""085: audit the four public FAQ answers, linked Psalm and verse boundaries.
The FAQ does not grant publication rights to any additional historical notes.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

data = read("data/faq-public-085.json")
assert data["version"] == 1, "Invalid FAQ version"
questions = data["questions"]
assert len(questions) == 4
assert [q["id"] for q in questions] == [f"faq-dieu-{n}" for n in range(1, 5)]
assert len({q["title"] for q in questions}) == 4

public = read("data/browser-search-catalog.json")
public_records = {r["id"]: r for r in public["records"]}
assert len([r for r in public_records.values() if r["recordType"] == "note"]) == 11, "No historic note may be exposed"
assert not any(r.get("recordType") == "faq" for r in public_records.values()), "FAQ is editorial content, not a new corpus record"

count = 0
ids = set()
for question in questions:
    answer = question["answer"]
    refs = question["references"]
    assert len(answer) > 500 and len(refs) >= 4
    assert len(re.findall(r"\\(psaume \\d+ [^)]+\\)", answer)) == len(refs), "Missing linked citation"
    previous_end = 0
    for ref in refs:
        at = answer.find(ref["label"], previous_end)
        assert at >= previous_end, "Citation text and order must remain exact"
        previous_end = at + len(ref["label"])
        ident = ref["recordId"]
        ids.add(ident)
        psalm = public_records.get(ident)
        assert psalm is not None and psalm["recordType"] == "psalm", ident
        assert psalm["archangel"] == ref["archangel"] and psalm["number"] == ref["number"], ident
        requested = ref["verses"]
        assert requested == sorted(set(requested)) and requested, ident
        available = {int(verse["number"]) for verse in psalm["verses"]}
        assert set(requested) <= available, (ident,requested)
        match = re.fullmatch(r"book-(\\d+)-psalm-(\\d+)", ident)
        assert match is not None
        canonical = read(f"data/corpus/books/book-{match.group(1)}/psalm-{match.group(2)}.json")
        assert canonical["id"] == ident and canonical["archangel"] == ref["archangel"]
        assert {int(verse["number"]) for verse in canonical["verses"]} >= set(requested)
        count += 1

assert count == 18 and len(ids) == 14, (count,len(ids))
print(f"FAQ 085 PASS: {len(questions)} exact answers, {count} links, {len(ids)} public psalms, every requested verse exists, 11-note privacy unchanged")
