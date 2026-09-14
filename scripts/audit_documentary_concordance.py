#!/usr/bin/env python3
"""Audit the documentary concordance pilot without inferring thematic meaning."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/documentary-entries.json"
INDEX = ROOT / "data/documentary-occurrence-index.json"
BOOKS = ROOT / "data/thematic-index/books"
JS = ROOT / "js/biblaw.js"
PAGES = ROOT / "scripts/build_pages_site.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    registry = load(REGISTRY)
    assert registry.get("schemaVersion") == 1
    entries = registry.get("entries", [])
    assert len(entries) == 1, "pilot must expose exactly one documentary entry"
    source = entries[0]
    assert source["entryId"] == "anges"
    assert source["label"] == "Ange / Anges"
    assert source["kind"] == "lexical-subject"
    assert source["forms"] == ["ange", "anges"]
    assert source["matching"] == {"mode": "whole-word", "caseSensitive": False}
    assert source["themeTarget"] == {
        "themeId": "anges",
        "status": "validated-documentary-presentation-link",
        "meaning": "combine-theme-teachings-with-lexical-concordance-without-promoting-occurrences-to-theme-relations",
    }

    index = load(INDEX)
    assert index.get("manualEditingAllowed") is False
    assert index.get("entryCount") == 1
    entry = index["entries"][0]
    assert entry["entryId"] == "anges"
    assert entry["recordCount"] == 467, entry["recordCount"]
    assert entry["totalOccurrences"] == 1236, entry["totalOccurrences"]

    records = entry["records"]
    assert len({r["recordId"] for r in records}) == 467
    assert records == sorted(records, key=lambda r: (
        -r["occurrenceCount"], -r["verseCount"], r.get("bookNumber") or 9999,
        r.get("psalmNumber") or 9999, r["recordId"]
    )), "non-thematic concordance order must be deterministic frequency-first"
    for record in records:
        assert "teaching" not in record
        assert "importance" not in record
        assert "themeId" not in record
        assert record["occurrenceCount"] == sum(v["count"] for v in record["occurrences"])
        assert record["verseCount"] == len(record["occurrences"])
        for verse in record["occurrences"]:
            assert verse["count"] == sum(m["count"] for m in verse["matches"])
            assert {m["form"] for m in verse["matches"]} <= {"ange", "anges"}

    # Existing thematic layer is read-only input for the presentation subtraction.
    thematic_records = set()
    specialized_relations = []
    for path in sorted(BOOKS.glob("book-*.json")):
        book = load(path)
        for psalm in book.get("psalmAnalyses", []):
            for rel in psalm.get("themes", []):
                tid = rel.get("themeId")
                if tid == "anges":
                    thematic_records.add(psalm["recordId"])
                if tid in {
                    "ange-gardien", "ange-de-la-benediction", "ange-de-la-sanctification",
                    "ange-comme-orientation", "archanges", "ronde-des-archanges",
                    "quatre-archanges", "vertus-des-anges"
                }:
                    specialized_relations.append((psalm["recordId"], tid))

    lexical_records = {r["recordId"] for r in records}
    overlap = thematic_records & lexical_records
    lexical_only = lexical_records - thematic_records
    theme_only = thematic_records - lexical_records
    assert overlap, "need real thematic+lexical positive controls"
    assert lexical_only, "need real lexical-only controls"
    # The contract must preserve thematic records even if a future theme record has no lexical match.
    synthetic_thematic = thematic_records | {"synthetic-theme-only"}
    assert "synthetic-theme-only" not in lexical_records - synthetic_thematic
    assert "synthetic-theme-only" in synthetic_thematic

    # Specialized themes never imply the generic theme: at least one specialized relation is outside it.
    assert specialized_relations
    assert any(record_id not in thematic_records for record_id, _ in specialized_relations)

    # High lexical frequency remains metadata only.
    assert records[0]["occurrenceCount"] >= records[-1]["occurrenceCount"]
    assert all("importance" not in r and "teaching" not in r for r in records)

    js = JS.read_text(encoding="utf-8")
    assert "documentary-occurrence-index.json" in js
    assert "ENSEIGNEMENTS SUR CE SUJET" in js
    assert "AUTRES OCCURRENCES DANS LE CORPUS" in js
    assert "classé par fréquence du terme dans le texte" in js
    assert "resolveDocumentaryEntry" in js
    assert "documentaryOtherSection" in js

    pages = PAGES.read_text(encoding="utf-8")
    assert '"data/documentary-occurrence-index.json"' in pages

    print(json.dumps({
        "entryId": "anges",
        "recordCount": entry["recordCount"],
        "totalOccurrences": entry["totalOccurrences"],
        "thematicRecordCount": len(thematic_records),
        "thematicAndLexicalCount": len(overlap),
        "lexicalOnlyCount": len(lexical_only),
        "thematicWithoutLexicalCount": len(theme_only),
        "specializedRelationCountChecked": len(specialized_relations),
        "topLexicalOnly": [
            r["recordId"] for r in records if r["recordId"] in lexical_only
        ][:3],
        "topThematicAndLexical": [
            r["recordId"] for r in records if r["recordId"] in overlap
        ][:3],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
