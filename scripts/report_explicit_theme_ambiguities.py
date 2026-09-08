#!/usr/bin/env python3
"""Print a compact, corpus-internal digest of explicit thematic search ambiguities.

This is a read-only review aid. It does not merge, rename or redefine themes. Evidence comes only
from the generated quality audit, which itself is derived from canonical book analyses.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/thematic-index/theme-quality-audit.json"
MAX_TEACHINGS_PER_ID = 8


def compact_teaching(text: str, limit: int = 220) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


data = json.loads(REPORT.read_text(encoding="utf-8"))
ambiguities = data.get("explicitSearchAmbiguities", {}).get("sameNormalizedLabelMultipleIds", [])
expected = data.get("stats", {}).get("sameNormalizedLabelMultipleIdsCount")
assert expected == len(ambiguities), "quality audit ambiguity count does not match its payload"

print(f"Explicit thematic ambiguities: {len(ambiguities)}")
for item in ambiguities:
    normalized = item.get("normalizedLabel")
    ids = item.get("themeIds", [])
    contexts_by_id = item.get("contextualEvidence", {})
    assert normalized and len(ids) >= 2, f"invalid ambiguity payload: {normalized!r}"
    print(f"\n## {normalized}")
    print("labels:", " | ".join(item.get("labels", [])))
    for theme in ids:
        theme_id = theme.get("id")
        contexts = contexts_by_id.get(theme_id, [])
        assert contexts, f"ambiguity {normalized}: {theme_id} has no contextual evidence"
        books = sorted({c.get("bookNumber") for c in contexts if c.get("bookNumber") is not None})
        archangels = sorted({c.get("archangel") for c in contexts if c.get("archangel")})
        importance = Counter(c.get("importance") or "unknown" for c in contexts)
        labels = Counter(c.get("label") or "" for c in contexts)
        print(
            f"- id={theme_id} relations={len(contexts)} books={books} "
            f"archangels={archangels} importance={dict(sorted(importance.items()))} "
            f"labels={dict(labels.most_common())}"
        )
        seen = set()
        shown = 0
        for context in contexts:
            teaching = compact_teaching(context.get("teaching"))
            signature = teaching.casefold()
            if not teaching or signature in seen:
                continue
            seen.add(signature)
            print(
                f"  · book-{int(context.get('bookNumber')):02d} psalm-{context.get('psalmNumber')} "
                f"verses={context.get('verseNumbers', [])}: {teaching}"
            )
            shown += 1
            if shown >= MAX_TEACHINGS_PER_ID:
                break
        if len(seen) < len({compact_teaching(c.get('teaching')).casefold() for c in contexts if c.get('teaching')}):
            print(f"  · … additional contextual teachings omitted from compact display")

print("\nReview rule: keep each ambiguity explicit unless corpus-internal evidence proves a technical duplicate.")
