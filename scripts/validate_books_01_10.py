#!/usr/bin/env python3
"""Validate documentary extraction of books 1-10 and diagnose missing psalm headings."""
from __future__ import annotations
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
OUT = ROOT / "data/pilot/books-01-10-validation-report.json"


def extract_text(first: int, last: int) -> str:
    return subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout

books_report = []
for book_no in range(1, 11):
    book_dir = ROOT / "data/corpus/books" / f"book-{book_no:02d}"
    book = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    psalms = []
    for path in sorted(book_dir.glob("psalm-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        nums = [v["number"] for v in data.get("verses", [])]
        expected = list(range(1, max(nums, default=0) + 1))
        psalms.append({
            "number": data["number"],
            "title": data["title"],
            "pages": data.get("source", {}).get("pdfPages", []),
            "verseCount": len(nums),
            "verseSequenceComplete": nums == expected,
            "missingVerses": [n for n in expected if n not in nums],
        })
    numbers = [p["number"] for p in psalms]
    expected_psalms = list(range(1, max(numbers, default=0) + 1))
    missing_psalms = [n for n in expected_psalms if n not in numbers]
    diagnostics = []
    for missing in missing_psalms:
        prev = max((p for p in psalms if p["number"] < missing), key=lambda p:p["number"], default=None)
        nxt = min((p for p in psalms if p["number"] > missing), key=lambda p:p["number"], default=None)
        first = max(prev["pages"][-1] if prev and prev["pages"] else book["source"]["pdfPages"][0], book["source"]["pdfPages"][0])
        last = min(nxt["pages"][0] if nxt and nxt["pages"] else first + 2, book["source"]["pdfPages"][1])
        raw = extract_text(first, last)
        lines = []
        for line in raw.splitlines():
            if re.search(rf"(^|\s){missing}(?:\s|[.)-])", line):
                lines.append(re.sub(r"\s+", " ", line).strip())
        diagnostics.append({"missingPsalm": missing, "pdfPages": [first,last], "candidateLines": lines[:30]})
    books_report.append({
        "bookNumber": book_no,
        "title": book.get("title"),
        "archangel": book.get("archangel"),
        "psalmCount": len(psalms),
        "psalmNumbers": numbers,
        "missingPsalms": missing_psalms,
        "psalmsWithVerseGaps": [p for p in psalms if not p["verseSequenceComplete"]],
        "gapDiagnostics": diagnostics,
    })

status = "passed" if all(not b["missingPsalms"] and not b["psalmsWithVerseGaps"] for b in books_report) else "needs-correction"
OUT.write_text(json.dumps({"scope":"books-01-10","status":status,"books":books_report}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Validation status: {status}")
