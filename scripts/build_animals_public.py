#!/usr/bin/env python3
"""Produce a read-only public animal directory from the canonical Psalms.

Editorial summaries and selected verse references are authored in
data/animals-editorial.json. All occurrences are recomputed from
data/corpus/books/ so no guessed verses enter the public site.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = ROOT / "data" / "animals-editorial.json"
CORPUS = ROOT / "data" / "corpus" / "books"


def normalize(value: str) -> str:
    value = value.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(
        character for character in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(character)
    )


def make_pattern(form: str) -> re.Pattern:
    # Lexical matches only: 'ver' is not the preposition 'vers',
    # 'cerf' in a kite (cerf-volant) is not the animal.
    expression = re.escape(normalize(form))
    if normalize(form) in {"cerf", "cerfs"}:
        expression += r"(?![\\s\\-‑–—]*volant)"
    return re.compile(r"(?<![a-z])" + expression + r"(?![a-z])")

def load_psalms() -> list[dict]:
    records = []
    for book in sorted(CORPUS.glob("book-*")):
        for path in sorted(book.glob("psalm-*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("recordType") == "psalm":
                records.append(record)
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical psalm IDs")
    if len(records) != 1158:
        raise ValueError(f"Expected 1158 canonical Psalms, found {len(records)}")
    return records


def generate(destination: Path) -> dict:
    editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
    records = load_psalms()
    by_id = {record["id"]: record for record in records}
    # Normalize the entire corpus only once; do not scan or normalize it
    # repeatedly for each lexical variant.
    normalized_verses = {
        record["id"]: [
            (verse["number"], normalize(verse["text"])) for verse in record["verses"]
        ] for record in records
    }
    entries = []
    seen_ids = set()
    count = {"totem": 0, "other": 0}
    for entry in editorial["entries"]:
        if entry["id"] in seen_ids:
            raise ValueError(f"Duplicate animal entry: {entry['id']}")
        seen_ids.add(entry["id"])
        category = entry["category"]
        if category not in count:
            raise ValueError(f"Unknown animal category: {category}")
        if not entry["label"].strip() or not entry["summary"].strip() or not entry["forms"]:
            raise ValueError(f"Incomplete animal entry: {entry['id']}")
        count[category] += 1
        patterns = [make_pattern(form) for form in entry["forms"]]
        references = []
        for ref in entry["sources"]:
            record = by_id.get(ref["recordId"])
            if record is None:
                raise ValueError(f"Unknown cited Psalm: {ref['recordId']}")
            valid_verses = {verse["number"]: verse for verse in record["verses"]}
            if not ref["verses"] or any(v not in valid_verses for v in ref["verses"]):
                raise ValueError(f"Unknown cited verse: {entry['id']} {ref}")
            references.append({
                "recordId": record["id"],
                "archangel": record["archangel"],
                "number": record["number"],
                "verses": ref["verses"],
            })

        all_mentions = []
        for record in records:
            verse_nums = [
                number for number, text in normalized_verses[record["id"]]
                if any(pattern.search(text) for pattern in patterns)
            ]
            if verse_nums:
                all_mentions.append({
                    "recordId": record["id"],
                    "archangel": record["archangel"],
                    "number": record["number"],
                    "verses": verse_nums,
                })
        if not all_mentions:
            raise ValueError(f"No explicit verse occurrence for: {entry['id']}")
        # Editorial examples must contain an actual mention of the animal,
        # somewhere within the group of linked verses.
        for reference in entry["sources"]:
            record = by_id[reference["recordId"]]
            selected = (text for number, text in normalized_verses[record["id"]]
                        if number in reference["verses"])
            if not any(pattern.search(text)
                       for text in selected for pattern in patterns):
                raise ValueError(f"Editorial reference does not name animal: {entry['id']} {reference}")

        entries.append({
            "id": entry["id"],
            "category": category,
            "label": entry["label"],
            "summary": entry["summary"],
            "sources": references,
            "occurrences": all_mentions,
        })

    entries.sort(key=lambda e: (e["category"] != "totem", normalize(e["label"])))
    public = {
        "schemaVersion": 1,
        "psalmCount": len(records),
        "scope": editorial["scope"],
        "classification": editorial["classification"],
        "editorialStatus": editorial["editorialStatus"],
        "entries": entries,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(public, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    result = {
        "psalmCount": len(records),
        "entries": len(entries),
        "totems": count["totem"],
        "others": count["other"],
        "publicVerseLinks": sum(len(v["verses"]) for e in entries for v in e["occurrences"]),
    }
    print("Animaux Biblaw:", result)
    return result


if __name__ == "__main__":
    generate(ROOT / "data" / "animals-public.json")
