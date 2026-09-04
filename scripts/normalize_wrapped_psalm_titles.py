#!/usr/bin/env python3
"""Repair psalm titles split across PDF lines.

The source PDF page is re-read for every psalm. When a numbered heading is followed by
one or more title-continuation lines before verse 1, those lines are joined to the title.
Because the continuation must occur between the numbered heading and verse 1, the rule
is documentary and reproducible rather than editorial guesswork.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
BOOKS = ROOT / "data/corpus/books"


def clean(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"^([A-ZÀ-ÖØ-Ý])\s+([a-zà-öø-ÿ])", r"\1\2", value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([’'])\s+", r"\1", value)
    return value


def pdf_page(page: int) -> list[str]:
    raw = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return raw.splitlines()


def repair(record: dict) -> bool:
    title = clean(record.get("title", ""))
    pages = record.get("source", {}).get("pdfPages", [])
    number = record.get("number")
    if not title or not pages or not isinstance(number, int):
        return False

    for page in pages[:2]:
        lines = pdf_page(page)
        for i, line in enumerate(lines):
            compact = re.sub(r"\s+", " ", line).strip()
            m = re.match(rf"^{number}\s+(?![.])(.+)$", compact)
            if not m:
                continue
            first = clean(m.group(1))
            common = max(8, min(len(title), len(first), 24))
            if first[:common].casefold() != title[:common].casefold():
                continue

            continuation = []
            for nxt in lines[i + 1 : i + 5]:
                c = re.sub(r"\s+", " ", nxt).strip()
                if not c:
                    continue
                if "| Évangile de l’Archange" in c:
                    continue
                if re.match(r"^1\.\s+", c):
                    break
                if re.match(r"^\d{1,3}[.]\s+", c) or re.match(r"^\d{1,3}\s+(?![.])", c):
                    break
                # Continuation is accepted only in the narrow heading-to-verse-1 zone.
                continuation.append(c)
                if len(continuation) >= 2:
                    break

            repaired = clean(" ".join([first, *continuation]))
            if repaired != title and len(repaired.split()) <= 30:
                record["title"] = repaired
                record.setdefault("extraction", {})["wrappedTitleNormalized"] = True
                return True
    return False


changed = 0
for path in sorted(BOOKS.glob("book-*/psalm-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if repair(data):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed += 1

print(f"Normalized {changed} wrapped psalm titles")
