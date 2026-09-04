#!/usr/bin/env python3
"""Inventory real book boundaries, book titles and psalm headings from the source PDF.

The table of contents also contains strings like "Livre 1", so real book boundaries
are detected from the repeated running headers of the form "Livre N | title | ...".
"""
from __future__ import annotations
import json, re, subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
OUT = ROOT / "data/pilot/book-inventory.json"

raw = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], check=True, capture_output=True, text=True).stdout
pages = raw.split("\f")

header_hits: dict[int, list[tuple[int, str]]] = {}
for page_no, page in enumerate(pages, 1):
    for line in page.splitlines():
        m = re.search(r"(?i)\bLivre\s+(\d+)\s*\|\s*([^|\n]+)(?:\|\s*([^\n]+))?", line)
        if not m:
            continue
        number = int(m.group(1))
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        header_hits.setdefault(number, []).append((page_no, title))

ordered = sorted(header_hits)
books = []
for pos, number in enumerate(ordered):
    hits = header_hits[number]
    first_header = min(page for page, _ in hits)
    next_first_header = min(page for page, _ in header_hits[ordered[pos + 1]]) if pos + 1 < len(ordered) else len(pages) + 1
    # The title/opening page generally precedes the first running header by one or two pages.
    first = max(1, first_header - 2)
    last = max(first, next_first_header - 3) if pos + 1 < len(ordered) else len(pages)
    title_counts = Counter(title for _, title in hits if title)
    book_title = title_counts.most_common(1)[0][0] if title_counts else None

    segment_pages = pages[first - 1:last]
    candidates = []
    for local_index, page in enumerate(segment_pages):
        page_no = first + local_index
        for line in page.splitlines():
            stripped = re.sub(r"\s+", " ", line).strip()
            # Psalm headings are number + a short title. Exclude running headers, page numbers and notes.
            m = re.match(r"^(\d{1,3})\s+(.{3,120})$", stripped)
            if not m:
                continue
            psalm_no = int(m.group(1))
            title = m.group(2).strip()
            low = title.lower()
            if "livre " in low or "note des hiérogrammates" in low or title.startswith("-"):
                continue
            if re.fullmatch(r"[\d\W_]+", title):
                continue
            # Reject obvious prose lines; genuine headings are compact and normally contain no terminal punctuation.
            if len(title.split()) > 18 or title.endswith(('.', ';', ':')):
                continue
            candidates.append({"number": psalm_no, "titleCandidate": title, "pdfPage": page_no})

    seen, unique = set(), []
    for item in candidates:
        key = (item["number"], item["titleCandidate"], item["pdfPage"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    books.append({
        "bookNumber": number,
        "title": book_title,
        "pdfPages": [first, last],
        "firstRunningHeaderPage": first_header,
        "runningHeaderCount": len(hits),
        "psalmHeadingCandidates": unique,
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"source": PDF.name, "status": "machine-inventory", "books": books}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Inventoried {len(books)} real books -> {OUT.relative_to(ROOT)}")
