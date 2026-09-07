#!/usr/bin/env python3
"""Describe canonical contexts for Assemblée queries without creating semantics.

The output is evidence for editorial review only: literal co-presence and existing
canonical themes are not treated as synonymy or as proof that a new theme is needed.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
BUNDLE = ROOT / "data/browser-search-catalog.json"
QUERIES = ("assemblée", "sainte assemblée")


def norm(value: object) -> str:
    text = "".join(
        c for c in unicodedata.normalize("NFD", str(value or ""))
        if unicodedata.category(c) != "Mn"
    ).lower().replace("œ", "oe").replace("æ", "ae").replace("’", " ").replace("'", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s-]", " ", text).replace("-", " ")).strip()


def literal_contains(value: object, query: str) -> bool:
    needle = norm(query)
    return bool(needle) and f" {needle} " in f" {norm(value)} "


def load_analyses() -> dict[str, dict]:
    result = {}
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for psalm in data.get("psalmAnalyses", []):
            if psalm.get("recordId"):
                result[psalm["recordId"]] = psalm
    return result


def main() -> None:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    psalms = [r for r in bundle["records"] if r.get("recordType") == "psalm"]
    analyses = load_analyses()

    for query in QUERIES:
        matching = []
        theme_psalm_counts = Counter()
        importance_counts: dict[str, Counter] = defaultdict(Counter)
        direct_support_counts = Counter()
        samples = []

        for record in psalms:
            hits = [v for v in record.get("verses", []) if literal_contains(v.get("text", ""), query)]
            title_hit = literal_contains(record.get("title", ""), query)
            if not hits and not title_hit:
                continue
            rid = record.get("id")
            matching.append(rid)
            analysis = analyses.get(rid, {})
            relations = analysis.get("themes", [])
            for rel in relations:
                tid = rel.get("themeId")
                if not tid:
                    continue
                theme_psalm_counts[tid] += 1
                importance_counts[tid][rel.get("importance", "unknown")] += 1
                support = {int(v) for v in rel.get("verseNumbers", []) if str(v).isdigit()}
                if any(int(v.get("number")) in support for v in hits if str(v.get("number", "")).isdigit()):
                    direct_support_counts[tid] += 1
            for verse in hits:
                if len(samples) < 12:
                    samples.append((rid, record.get("title"), verse.get("number"), verse.get("text")))

        print(f"ASSEMBLY_CONTEXT query={query!r} matchingPsalms={len(matching)}")
        print("TOP_EXISTING_THEMES note='co-presence only; not synonymy' ")
        for tid, count in theme_psalm_counts.most_common(20):
            print(
                f"THEME themeId={tid} matchingPsalms={count} "
                f"importance={dict(importance_counts[tid])} phraseInSupportVerses={direct_support_counts[tid]}"
            )
        print("SAMPLES")
        for rid, title, number, text in samples:
            print(f"VERSE recordId={rid} title={title!r} verse={number} text={text!r}")
        print()


if __name__ == "__main__":
    main()
