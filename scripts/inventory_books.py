#!/usr/bin/env python3
"""Inventory book boundaries, titles and psalm headings directly from the source PDF.

This is the first generic extraction stage for Biblaw. It does not guess thematic
content. It maps the documentary structure so books can then be extracted in order.
The output is intentionally conservative and is used only to drive later extraction.
"""
from __future__ import annotations
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
OUT = ROOT / "data/pilot/book-inventory.json"

raw = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], check=True, capture_output=True, text=True).stdout
pages = raw.split("\f")

book_hits: dict[int, list[int]] = {}
for i, page in enumerate(pages, 1):
    for m in re.finditer(r"(?im)^\s*Livre\s+(\d+)\b", page):
        book_hits.setdefault(int(m.group(1)), []).append(i)

books = []
ordered = sorted(book_hits)
for pos, number in enumerate(ordered):
    first = min(book_hits[number])
    next_first = min(book_hits[ordered[pos+1]]) if pos + 1 < len(ordered) else len(pages) + 1
    last = next_first - 1
    segment = "\n".join(pages[first-1:last])
    headings = []
    for m in re.finditer(r"(?m)^\s*(\d{1,3})\s+([^\n]{3,140})$", segment):
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        if title and not title.isdigit():
            headings.append({"number": int(m.group(1)), "titleCandidate": title})
    seen, unique = set(), []
    for h in headings:
        key = (h["number"], h["titleCandidate"])
        if key not in seen:
            seen.add(key); unique.append(h)
    books.append({"bookNumber": number, "pdfPages": [first, last], "psalmHeadingCandidates": unique})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"source": PDF.name, "status": "machine-inventory", "books": books}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Inventoried {len(books)} books -> {OUT.relative_to(ROOT)}")
