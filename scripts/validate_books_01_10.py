#!/usr/bin/env python3
"""Validate documentary extraction of books 1-10 and diagnose internal gaps."""
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


def compact_excerpt(raw: str, missing: int) -> list[str]:
    lines = raw.splitlines()
    interesting = set()
    for i, line in enumerate(lines):
        if re.search(rf"(^|\s){missing}(?:\s|[.)-])", line) or re.match(r"^\s*1\.\s+", line):
            for j in range(max(0, i - 4), min(len(lines), i + 7)):
                interesting.add(j)
    if not interesting:
        # Preserve a bounded page excerpt for headings split across lines.
        interesting.update(range(min(len(lines), 80)))
    return [re.sub(r"\s+", " ", lines[i]).strip() for i in sorted(interesting) if lines[i].strip()][:120]


books_report = []
for book_no in range(1, 11):
    book_dir = ROOT / "data/corpus/books" / f"book-{book_no:02d}"
    book = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    psalms = []
    for path in sorted(book_dir.glob("psalm-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        nums = [v["number"] for v in data.get("verses", [])]
        unique_sorted = sorted(set(nums))
        expected = list(range(min(unique_sorted, default=1), max(unique_sorted, default=0) + 1)) if unique_sorted else []
        psalms.append({
            "number": data["number"], "title": data["title"], "pages": data.get("source", {}).get("pdfPages", []),
            "verseCount": len(nums), "verseSequenceComplete": nums == expected,
            "missingVerses": [n for n in expected if n not in nums], "duplicateOrOutOfOrderVerses": nums != unique_sorted,
        })
    numbers = [p["number"] for p in psalms]
    expected_psalms = list(range(min(numbers), max(numbers) + 1)) if numbers else []
    missing_psalms = [n for n in expected_psalms if n not in numbers]
    diagnostics = []
    for missing in missing_psalms:
        prev = max((p for p in psalms if p["number"] < missing), key=lambda p:p["number"], default=None)
        nxt = min((p for p in psalms if p["number"] > missing), key=lambda p:p["number"], default=None)
        first = max(prev["pages"][-1] if prev and prev["pages"] else book["source"]["pdfPages"][0], book["source"]["pdfPages"][0])
        last = min(nxt["pages"][0] if nxt and nxt["pages"] else first + 2, book["source"]["pdfPages"][1])
        raw = extract_text(first, last)
        candidate_lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines() if re.search(rf"(^|\s){missing}(?:\s|[.)-])", line)]
        diagnostics.append({
            "missingPsalm": missing, "pdfPages": [first,last], "candidateLines": candidate_lines[:30],
            "sourceExcerpt": compact_excerpt(raw, missing),
        })
    books_report.append({
        "bookNumber": book_no, "title": book.get("title"), "archangel": book.get("archangel"), "psalmCount": len(psalms),
        "psalmRange": [min(numbers), max(numbers)] if numbers else None, "psalmNumbers": numbers,
        "missingPsalms": missing_psalms, "psalmsWithVerseGaps": [p for p in psalms if not p["verseSequenceComplete"]],
        "gapDiagnostics": diagnostics,
    })

status = "passed" if all(not b["missingPsalms"] and not b["psalmsWithVerseGaps"] for b in books_report) else "needs-correction"
OUT.write_text(json.dumps({"scope":"books-01-10","status":status,"books":books_report}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Validation status: {status}")
