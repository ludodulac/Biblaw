#!/usr/bin/env python3
"""Validate the derived thematic search alias index without making semantic judgments.

Besides identity/ambiguity integrity, this validator protects deterministic ordering so equal-frequency
or case-only label variants cannot produce noisy generated diffs across equivalent rebuilds.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
SEARCH = ROOT / "data/thematic-index/theme-search-index.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    text = text.replace("œ", "oe").replace("æ", "ae")
    text = re.sub(r"[’'`´]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def label_sort_key(label: str) -> tuple[str, str]:
    return (label.casefold(), label)


def observed_label_sort_key(item: dict) -> tuple[int, str, str]:
    label = str(item.get("label") or "")
    return (-int(item.get("count") or 0), *label_sort_key(label))


directory = load(DIRECTORY)
search = load(SEARCH)
errors = []

canonical = {t.get("id"): t for t in directory.get("themes", []) if t.get("id")}
records = {t.get("themeId"): t for t in search.get("themes", []) if t.get("themeId")}
aliases = search.get("aliases", [])
alias_map = {}

alias_keys = [alias.get("queryKey") for alias in aliases]
if alias_keys != sorted(alias_keys):
    errors.append("aliases must be deterministically sorted by queryKey")

for alias in aliases:
    key = alias.get("queryKey")
    ids = alias.get("themeIds", [])
    if not key:
        errors.append("alias without queryKey")
        continue
    if key in alias_map:
        errors.append(f"duplicate alias key: {key}")
    alias_map[key] = ids
    if alias.get("ambiguous") != (len(ids) > 1):
        errors.append(f"bad ambiguity flag for alias: {key}")
    labels = alias.get("labels", [])
    if labels != sorted(labels, key=label_sort_key):
        errors.append(f"non-deterministic label ordering for alias: {key}")
    for tid in ids:
        if tid not in canonical:
            errors.append(f"alias {key} references unknown theme id {tid}")

for tid, theme in canonical.items():
    if tid not in records:
        errors.append(f"canonical theme missing from search records: {tid}")
        continue
    record = records[tid]
    label = theme.get("label")
    key = normalize(label)
    if not key:
        errors.append(f"theme has empty normalized canonical label: {tid}")
    elif tid not in alias_map.get(key, []):
        errors.append(f"canonical label does not resolve to own theme: {tid} / {label}")

    observed = record.get("observedLabels", [])
    if observed != sorted(observed, key=observed_label_sort_key):
        errors.append(f"non-deterministic observed-label ordering for theme: {tid}")
    normalized_aliases = record.get("normalizedAliases", [])
    if len(normalized_aliases) != len(set(normalized_aliases)):
        errors.append(f"duplicate normalized alias in theme record: {tid}")

for tid in records:
    if tid not in canonical:
        errors.append(f"search record references non-canonical theme id: {tid}")

if search.get("semanticMerging") is not False:
    errors.append("search index must explicitly keep semanticMerging=false")
if search.get("themeCount") != len(canonical):
    errors.append(f"themeCount mismatch: search={search.get('themeCount')} directory={len(canonical)}")
if search.get("aliasCount") != len(aliases):
    errors.append("aliasCount mismatch")
if search.get("ambiguousAliasCount") != sum(1 for a in aliases if a.get("ambiguous")):
    errors.append("ambiguousAliasCount mismatch")

print(json.dumps({
    "status": "passed" if not errors else "failed",
    "themeCount": len(canonical),
    "aliasCount": len(aliases),
    "ambiguousAliasCount": sum(1 for a in aliases if a.get("ambiguous")),
    "deterministicOrdering": not any("deterministic" in error for error in errors),
    "errors": errors,
}, ensure_ascii=False, indent=2))
if errors:
    sys.exit(1)
