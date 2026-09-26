#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, os, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SOURCE_SHA = "5c755358f5cda20db52a2d748cbb2664a1831dcc"
OUTPUT = ROOT / "biblaw-global-vocabulary-inventory-019.json"

spec = importlib.util.spec_from_file_location("occurrence_index", ROOT / "scripts/build_linguistic_occurrence_index.py")
occ = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(occ)

def is_dash_punctuation(ch: str) -> bool:
    return bool(ch) and unicodedata.category(ch) == "Pd"

def occurrence_id(record_id, field, verse, start, end):
    return occ.oid(record_id, field, verse, start, end)

def main():
    catalog = json.loads(occ.CATALOG.read_text(encoding="utf-8"))
    forms = {}
    total_tokens = 0
    apostrophe_tokens = 0
    hyphen_adjacent_tokens = 0
    all_occurrence_ids = set()
    duplicate_occurrence_ids = 0
    dash_characters = Counter()

    for rel in catalog["records"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing catalog record: {rel}")
        obj = json.loads(path.read_text(encoding="utf-8"))
        if not occ.searchable(rel, obj):
            continue
        book_number, psalm_number = occ.meta(obj)
        for field, verse_number, text in occ.fields(obj):
            for match in occ.TOKEN_RE.finditer(text):
                surface = match.group()
                normalized = occ.norm(surface)
                start, end = match.span()
                oid = occurrence_id(obj["id"], field, verse_number, start, end)
                if oid in all_occurrence_ids:
                    duplicate_occurrence_ids += 1
                all_occurrence_ids.add(oid)
                before = text[start - 1] if start > 0 else ""
                after = text[end] if end < len(text) else ""
                adjacent_dashes = [ch for ch in (before, after) if is_dash_punctuation(ch)]
                has_apostrophe = "'" in surface or "’" in surface
                has_hyphen_adjacency = bool(adjacent_dashes)
                total_tokens += 1
                apostrophe_tokens += int(has_apostrophe)
                hyphen_adjacent_tokens += int(has_hyphen_adjacency)
                dash_characters.update(adjacent_dashes)
                if normalized not in forms:
                    forms[normalized] = {
                        "normalizedForm": normalized,
                        "totalFrequency": 0,
                        "_variants": Counter(),
                        "_records": set(),
                        "_books": set(),
                        "_fields": set(),
                        "_recordTypes": set(),
                        "apostrophePresent": False,
                        "hyphenAdjacencyObserved": False,
                        "_dashCharacters": Counter(),
                        "stableOccurrenceReferences": [],
                    }
                entry = forms[normalized]
                entry["totalFrequency"] += 1
                entry["_variants"][surface] += 1
                entry["_records"].add(obj["id"])
                if book_number is not None:
                    entry["_books"].add(book_number)
                entry["_fields"].add(field)
                if obj.get("recordType") is not None:
                    entry["_recordTypes"].add(obj.get("recordType"))
                entry["apostrophePresent"] = entry["apostrophePresent"] or has_apostrophe
                entry["hyphenAdjacencyObserved"] = entry["hyphenAdjacencyObserved"] or has_hyphen_adjacency
                entry["_dashCharacters"].update(adjacent_dashes)
                entry["stableOccurrenceReferences"].append({
                    "occurrenceId": oid,
                    "recordId": obj["id"],
                    "bookNumber": book_number,
                    "psalmNumber": psalm_number,
                    "verseNumber": verse_number,
                    "field": field,
                    "startOffset": start,
                    "endOffset": end,
                })

    output_forms = []
    variant_integrity = True
    for normalized in sorted(forms):
        entry = forms[normalized]
        variants = [{"surfaceForm": s, "count": c} for s, c in sorted(entry.pop("_variants").items())]
        variant_integrity = variant_integrity and sum(v["count"] for v in variants) == entry["totalFrequency"]
        entry["surfaceVariants"] = variants
        entry["occurrenceCount"] = len(entry["stableOccurrenceReferences"])
        entry["recordCount"] = len(entry.pop("_records"))
        entry["bookCount"] = len(entry.pop("_books"))
        entry["fields"] = sorted(entry.pop("_fields"))
        entry["recordTypes"] = sorted(entry.pop("_recordTypes"))
        entry["hyphenAdjacencyCharacters"] = [
            {"character": ch, "count": count} for ch, count in sorted(entry.pop("_dashCharacters").items())
        ]
        output_forms.append(entry)

    distinct_forms = len(output_forms)
    sum_frequencies = sum(x["totalFrequency"] for x in output_forms)
    sum_occurrences = sum(x["occurrenceCount"] for x in output_forms)
    distinct_apostrophe = sum(x["apostrophePresent"] for x in output_forms)
    distinct_hyphen = sum(x["hyphenAdjacencyObserved"] for x in output_forms)
    top20 = sorted(
        ({"normalizedForm": x["normalizedForm"], "totalFrequency": x["totalFrequency"]} for x in output_forms),
        key=lambda x: (-x["totalFrequency"], x["normalizedForm"]),
    )[:20]

    if sum_frequencies != total_tokens:
        raise SystemExit("integrity failure: frequency sum")
    if distinct_forms != len(output_forms):
        raise SystemExit("integrity failure: distinct forms")
    if not variant_integrity:
        raise SystemExit("integrity failure: variant counts")
    if duplicate_occurrence_ids or sum_occurrences != total_tokens or len(all_occurrence_ids) != total_tokens:
        raise SystemExit("integrity failure: occurrences")

    payload = {
        "schemaVersion": 1,
        "purpose": "full-corpus-raw-vocabulary-inventory-019",
        "baselineSourceSha": BASELINE_SOURCE_SHA,
        "executedHeadSha": os.environ.get("GITHUB_SHA", "LOCAL"),
        "tokenizationContract": {
            "sourceModule": "scripts/build_linguistic_occurrence_index.py",
            "catalog": "data/catalog.json",
            "searchableContract": "same searchable() and fields() functions",
            "tokenRegex": occ.TOKEN_RE.pattern,
            "singlePass": True,
        },
        "normalizationContract": "Unicode NFC + casefold(), via existing norm()",
        "totalCorpusTokens": total_tokens,
        "distinctNormalizedForms": distinct_forms,
        "tokensWithApostrophe": apostrophe_tokens,
        "distinctFormsWithApostrophe": distinct_apostrophe,
        "tokensWithHyphenAdjacency": hyphen_adjacent_tokens,
        "distinctFormsWithHyphenAdjacency": distinct_hyphen,
        "hyphenAdjacencyCharacterDistribution": [
            {"character": ch, "count": count} for ch, count in sorted(dash_characters.items())
        ],
        "forms": output_forms,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"TOTAL_CORPUS_TOKENS = {total_tokens}")
    print(f"DISTINCT_NORMALIZED_FORMS = {distinct_forms}")
    print(f"TOKENS_WITH_APOSTROPHE = {apostrophe_tokens}")
    print(f"DISTINCT_FORMS_WITH_APOSTROPHE = {distinct_apostrophe}")
    print(f"TOKENS_WITH_HYPHEN_ADJACENCY = {hyphen_adjacent_tokens}")
    print(f"DISTINCT_FORMS_WITH_HYPHEN_ADJACENCY = {distinct_hyphen}")
    print("TOP_20_NORMALIZED_FORMS_BY_FREQUENCY = " + json.dumps(top20, ensure_ascii=False, separators=(",", ":")))
    print(f"INTEGRITY_SUM_FREQUENCIES = {'PASS' if sum_frequencies == total_tokens else 'FAIL'}")
    print(f"INTEGRITY_VARIANT_COUNTS = {'PASS' if variant_integrity else 'FAIL'}")
    print(f"INTEGRITY_OCCURRENCES = {'PASS' if duplicate_occurrence_ids == 0 and sum_occurrences == total_tokens and len(all_occurrence_ids) == total_tokens else 'FAIL'}")
    print(f"BASELINE_SOURCE_SHA = {BASELINE_SOURCE_SHA}")
    print(f"EXECUTED_HEAD_SHA = {os.environ.get('GITHUB_SHA', 'LOCAL')}")

if __name__ == "__main__":
    main()
