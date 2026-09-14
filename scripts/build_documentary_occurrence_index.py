#!/usr/bin/env python3
"""Build a deterministic lexical concordance from canonical Psalm texts.

Documentary entries are not theme ids. Lexical frequency never creates theme relations,
teachings, or importance levels. Matching is defined explicitly per documentary entry.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/documentary-entries.json"
CORPUS = ROOT / "data/corpus/books"
OUT = ROOT / "data/documentary-occurrence-index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_pattern(forms: list[str], matching: dict) -> re.Pattern[str]:
    if matching != {"mode": "whole-word", "caseSensitive": False}:
        raise SystemExit(f"Unsupported documentary matching contract: {matching}")
    ordered = sorted(set(forms), key=lambda x: (-len(x), x.casefold(), x))
    if not ordered:
        raise SystemExit("Documentary entry without forms")
    escaped = "|".join(re.escape(form) for form in ordered)
    # Unicode-aware word boundaries without treating hyphen/apostrophe as part of the token.
    return re.compile(rf"(?<!\w)(?P<form>{escaped})(?!\w)", re.IGNORECASE | re.UNICODE)


def canonical_psalms():
    for path in sorted(CORPUS.glob("book-*/psalm-*.json")):
        obj = load(path)
        if obj.get("recordType") == "psalm":
            yield obj


def main() -> None:
    registry = load(REGISTRY)
    entries = registry.get("entries", [])
    if not entries:
        raise SystemExit("No documentary entries configured")

    psalms = list(canonical_psalms())
    if len(psalms) != 1158:
        raise SystemExit(f"Expected 1158 canonical psalms, got {len(psalms)}")

    output_entries = []
    for entry in entries:
        pattern = build_pattern(entry.get("forms", []), entry.get("matching", {}))
        records = []
        total_occurrences = 0

        for psalm in psalms:
            verse_occurrences = []
            record_total = 0
            for verse in psalm.get("verses", []):
                form_counts: dict[str, int] = {}
                for match in pattern.finditer(verse.get("text", "")):
                    found = match.group("form").casefold()
                    form_counts[found] = form_counts.get(found, 0) + 1
                if not form_counts:
                    continue
                count = sum(form_counts.values())
                record_total += count
                verse_occurrences.append({
                    "verseNumber": verse.get("number"),
                    "matches": [
                        {"form": form, "count": form_counts[form]}
                        for form in sorted(form_counts)
                    ],
                    "count": count,
                })

            if record_total:
                total_occurrences += record_total
                book = psalm.get("book", {})
                records.append({
                    "recordId": psalm.get("id"),
                    "bookNumber": book.get("number"),
                    "psalmNumber": psalm.get("number"),
                    "archangel": psalm.get("archangel"),
                    "occurrenceCount": record_total,
                    "verseCount": len(verse_occurrences),
                    "occurrences": verse_occurrences,
                })

        records.sort(key=lambda r: (
            -r["occurrenceCount"],
            -r["verseCount"],
            r.get("bookNumber") or 9999,
            r.get("psalmNumber") or 9999,
            r["recordId"],
        ))
        output_entries.append({
            "entryId": entry["entryId"],
            "label": entry["label"],
            "kind": entry["kind"],
            "matching": entry["matching"],
            "forms": entry["forms"],
            "themeTarget": entry.get("themeTarget"),
            "totalOccurrences": total_occurrences,
            "recordCount": len(records),
            "records": records,
        })

    payload = {
        "schemaVersion": 1,
        "generatedFrom": [
            "data/documentary-entries.json",
            "data/corpus/books/book-*/psalm-*.json"
        ],
        "manualEditingAllowed": False,
        "entryCount": len(output_entries),
        "entries": output_entries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Built documentary concordance:")
    for entry in output_entries:
        print(f"  {entry['entryId']}: {entry['recordCount']} psalms, {entry['totalOccurrences']} occurrences")


if __name__ == "__main__":
    main()
