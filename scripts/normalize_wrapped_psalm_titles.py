#!/usr/bin/env python3
"""Repair psalm titles split across PDF lines.

Only records whose extracted title ends with a connector likely to require a continuation
(e.g. "de", "des", "du", "et") are candidates. The source PDF page is re-read and the
continuation is accepted only when it appears immediately after the numbered heading and
before verse 1. This keeps the correction documentary and reproducible.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
BOOKS = ROOT / "data/corpus/books"
CONNECTOR_RE = re.compile(r"(?i)(?:\bde|\bdes|\bdu|\bde la|\bde l[’']|\bet|\bà|\bau|\baux)$")


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
    title = record.get("title", "")
    if not CONNECTOR_RE.search(title):
        return False
    pages = record.get("source", {}).get("pdfPages", [])
    number = record.get("number")
    if not pages or not isinstance(number, int):
        return False

    for page in pages[:2]:
        lines = pdf_page(page)
        for i, line in enumerate(lines):
            compact = re.sub(r"\s+", " ", line).strip()
            m = re.match(rf"^{number}\s+(?![.])(.+)$", compact)
            if not m:
                continue
            first = clean(m.group(1))
            # Require source first line to agree with the extracted title enough to avoid prose numbers.
            if not (first.startswith(title[: max(8, min(len(title), 24))]) or title.startswith(first[: max(8, min(len(first), 24))])):
                continue
            continuation = []
            for nxt in lines[i + 1 : i + 4]:
                c = re.sub(r"\s+", " ", nxt).strip()
                if not c:
                    continue
                if re.match(r"^1\.\s+", c):
                    break
                if re.match(r"^\d{1,3}[.]\s+", c) or re.match(r"^\d{1,3}\s+", c):
                    break
                if "| Évangile de l’Archange" in c:
                    continue
                continuation.append(c)
                # One continuation line is the normal case; do not absorb body prose.
                break
            if continuation:
                repaired = clean(first + " " + " ".join(continuation))
                if repaired != title and len(repaired.split()) <= 24:
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
