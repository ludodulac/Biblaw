#!/usr/bin/env python3
"""Validate the editorial workshop's canonical, low-request data contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "js" / "validation.js"
HTML = ROOT / "validation.html"
BUNDLE = ROOT / "data" / "browser-search-catalog.json"
PILOTS = {
    "book-18-psalm-112",
    "book-19-psalm-104",
    "book-20-psalm-105",
    "book-26-psalm-182",
}
DEFAULT = "book-17-psalm-105"


def main() -> None:
    js = JS.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    records = bundle.get("records", [])
    psalms = [record for record in records if record.get("recordType") == "psalm"]
    by_id = {record.get("id"): record for record in psalms if record.get("id")}

    assert "js/validation.js" in html
    assert "fetch('data/browser-search-catalog.json')" in js
    assert "fetch('data/catalog.json')" not in js
    assert "catalog.records.map" not in js
    assert "Promise.all(catalog.records" not in js
    assert "const sourcePages" in js
    assert "book-17-psalm-105" in js

    legacy_fragments = (
        "michael-psalm-105",
        "gabriel-psalm-112",
        "raphael-psalm-104",
        "ouriel-psalm-105",
        "gabriel-psalm-182",
    )
    for fragment in legacy_fragments:
        assert fragment not in js, f"legacy pilot ID still used: {fragment}"

    assert DEFAULT in by_id
    assert PILOTS <= set(by_id), f"missing canonical pilots: {sorted(PILOTS - set(by_id))}"

    book17 = [
        record for record in psalms
        if record.get("archangel") == "michael" and record.get("book", {}).get("number") == 17
    ]
    assert len(book17) == 26, f"expected 26 canonical book-17 Psalms, got {len(book17)}"
    assert {record["number"] for record in book17} == set(range(105, 131))

    selected_ids = {record["id"] for record in book17} | PILOTS
    assert len(selected_ids) == 30
    assert all(record_id.startswith("book-") for record_id in selected_ids)
    assert all((by_id[record_id].get("source", {}).get("pdfPages") or by_id[record_id].get("source", {}).get("printedPages")) for record_id in selected_ids)

    print(
        "Validation workshop OK: one canonical browser bundle, "
        f"{len(book17)} book-17 Psalms + {len(PILOTS)} canonical pilots = {len(selected_ids)} records"
    )


if __name__ == "__main__":
    main()
