#!/usr/bin/env python3
"""Validate documentary psalm-number lookup without touching thematic semantics."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "browser-search-catalog.json"
JS = ROOT / "js" / "biblaw.js"


def norm(value: object) -> str:
    text = "".join(
        c for c in unicodedata.normalize("NFD", str(value or ""))
        if unicodedata.category(c) != "Mn"
    ).lower().replace("œ", "oe").replace("æ", "ae").replace("’", " ").replace("'", " ")
    text = re.sub(r"[^a-z0-9\s-]", " ", text).replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_psalm_number_query(value: object) -> int | None:
    match = re.fullmatch(r"(?:psaume\s+)?([0-9]{1,4})", norm(value))
    if not match:
        return None
    number = int(match.group(1))
    return number if number > 0 else None


def main() -> None:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    psalms = [record for record in bundle["records"] if record.get("recordType") == "psalm"]
    js = JS.read_text(encoding="utf-8")

    assert len(psalms) == 1158, f"unexpected canonical psalm count: {len(psalms)}"
    assert all(isinstance(record.get("number"), int) and record["number"] > 0 for record in psalms)
    assert all(isinstance(record.get("book", {}).get("number"), int) for record in psalms)

    counts = Counter(record["number"] for record in psalms)
    repeated = {number: count for number, count in counts.items() if count > 1}
    assert repeated, "corpus should expose repeated psalm numbers across books"

    sample_number = min(repeated, key=lambda number: (-repeated[number], number))
    sample_records = [record for record in psalms if record["number"] == sample_number]
    assert len(sample_records) == repeated[sample_number]
    assert len({record["id"] for record in sample_records}) == len(sample_records)

    assert parse_psalm_number_query(str(sample_number)) == sample_number
    assert parse_psalm_number_query(f"psaume {sample_number}") == sample_number
    assert parse_psalm_number_query(f"  Psaume   {sample_number}  ") == sample_number
    assert parse_psalm_number_query("22 commandements") is None
    assert parse_psalm_number_query("alliance 22") is None
    assert parse_psalm_number_query("0") is None

    # Browser implementation must resolve documentary numbers before thematic/text search.
    required = (
        "const parsePsalmNumberQuery",
        "function psalmNumberMatches(number)",
        "const psalmNumber=parsePsalmNumberQuery(query)",
        "return render(psalmNumberMatches(psalmNumber),null,{numberLookup:true,psalmNumber})",
        "Number(r.number)===number",
        "r.book?.number",
        "numberLookup?'Numéro':'Texte'",
    )
    for needle in required:
        assert needle in js, f"missing browser number-search contract: {needle}"

    print(
        f"Psalm number search OK: {len(psalms)} canonical psalms, "
        f"{len(repeated)} repeated numbers, sample={sample_number} matches={len(sample_records)}"
    )


if __name__ == "__main__":
    main()
