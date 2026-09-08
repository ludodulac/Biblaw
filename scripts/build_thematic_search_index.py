#!/usr/bin/env python3
"""Build a search-facing alias index without merging editorial themes.

The thematic book files remain authoritative. This derived layer improves recall for spelling,
punctuation and historical label variants while preserving every distinct theme id.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
OUT = ROOT / "data/thematic-index/theme-search-index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    text = text.replace("œ", "oe").replace("æ", "ae")
    text = re.sub(r"[’'`´]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def label_sort_key(label: str) -> tuple[str, str]:
    """Stable ordering even when labels differ only by case (set order must never leak to output)."""
    return (label.casefold(), label)


def observed_labels(counter: Counter) -> list[tuple[str, int]]:
    """Counter.most_common() preserves insertion order on ties; make tie order explicit instead."""
    return sorted(counter.items(), key=lambda item: (-item[1], *label_sort_key(item[0])))


directory = load(DIRECTORY)
theme_meta = {t["id"]: t for t in directory.get("themes", [])}
labels_by_id = defaultdict(Counter)

for path in sorted(BOOKS.glob("book-*.json")):
    data = load(path)
    for psalm in data.get("psalmAnalyses", []):
        for rel in psalm.get("themes", []):
            tid, label = rel.get("themeId"), rel.get("label")
            if tid and label:
                labels_by_id[tid][label] += 1

# Every observed label becomes a search alias. The canonical display label remains the one in
# theme-directory.json; we do not rewrite editorial files and do not collapse ids.
alias_to_ids = defaultdict(set)
alias_display = defaultdict(set)
records = []
for tid in sorted(set(theme_meta) | set(labels_by_id)):
    meta = theme_meta.get(tid, {})
    canonical = meta.get("label")
    observed = labels_by_id.get(tid, Counter())
    ordered_observed = observed_labels(observed)
    labels = []
    if canonical:
        labels.append(canonical)
    labels.extend(label for label, _ in ordered_observed if label != canonical)
    # Also index the id as a fallback slug-form alias, but never display it as a label.
    normalized_aliases = []
    for label in labels:
        key = normalize(label)
        if not key:
            continue
        alias_to_ids[key].add(tid)
        alias_display[key].add(label)
        if key not in normalized_aliases:
            normalized_aliases.append(key)
    slug_key = normalize(tid.replace("-", " "))
    if slug_key:
        alias_to_ids[slug_key].add(tid)
        normalized_aliases.append(slug_key) if slug_key not in normalized_aliases else None
    records.append({
        "themeId": tid,
        "canonicalLabel": canonical,
        "observedLabels": [{"label": label, "count": count} for label, count in ordered_observed],
        "normalizedAliases": normalized_aliases,
        "occurrenceCount": meta.get("occurrenceCount", 0),
        "score": meta.get("score", 0),
    })

aliases = []
for key in sorted(alias_to_ids):
    ids = sorted(alias_to_ids[key], key=lambda tid: (-theme_meta.get(tid, {}).get("score", 0), tid))
    aliases.append({
        "queryKey": key,
        "themeIds": ids,
        "labels": sorted(alias_display.get(key, set()), key=label_sort_key),
        "ambiguous": len(ids) > 1,
    })

OUT.write_text(json.dumps({
    "schemaVersion": 1,
    "generatedFrom": ["data/thematic-index/books/book-*.json", "data/thematic-index/theme-directory.json"],
    "semanticMerging": False,
    "themeCount": len(records),
    "aliasCount": len(aliases),
    "ambiguousAliasCount": sum(1 for a in aliases if a["ambiguous"]),
    "themes": records,
    "aliases": aliases,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Built thematic search index: {len(records)} themes, {len(aliases)} aliases, {sum(1 for a in aliases if a['ambiguous'])} ambiguous")
