#!/usr/bin/env python3
"""Build a bounded semantic-neighborhood dossier for the union-pere-nature case.

This is a read-only discovery aid over the canonical per-book thematic analyses.
Lexical cues are used only to select occurrences for human semantic review. They do
not validate, type, merge or persist any relation.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
ANCHOR = "union-pere-nature"
MAX_OCCURRENCES_PER_THEME = 4


def norm(text: str | None) -> str:
    value = unicodedata.normalize("NFKD", text or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def contains_any(text: str, stems: tuple[str, ...]) -> bool:
    return any(stem in text for stem in stems)


UNION_STEMS = (
    "union", "unir", "uni ", " unis", "unifie", "communion", "fusion",
    "relie", "reliant", "liaison", "harmonie", "harmon", "unite",
)
FATHER_STEMS = ("pere",)
DIVINE_STEMS = ("divin", "dieu")
NATURE_STEMS = ("nature", "terre", "corps", "incarn", "matiere", "element")


def cue_buckets(text: str) -> list[str]:
    has_union = contains_any(text, UNION_STEMS)
    has_father = contains_any(text, FATHER_STEMS)
    has_divine = contains_any(text, DIVINE_STEMS)
    has_nature = contains_any(text, NATURE_STEMS)
    buckets = []
    if has_father and has_union:
        buckets.append("father_union")
    if has_divine and has_union:
        buckets.append("divine_union")
    if has_nature and has_union:
        buckets.append("nature_union")
    if has_father and has_nature:
        buckets.append("father_nature")
    return buckets


def main() -> None:
    by_theme: dict[str, list[dict]] = defaultdict(list)
    anchor_occurrences: list[dict] = []

    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        for analysis in data.get("psalmAnalyses") or []:
            record_id = analysis.get("recordId")
            for theme in analysis.get("themes") or []:
                theme_id = theme.get("themeId")
                if not theme_id:
                    continue
                label = theme.get("label") or ""
                teaching = theme.get("teaching") or ""
                combined = norm(f"{label} {teaching}")
                buckets = cue_buckets(combined)
                occurrence = {
                    "recordId": record_id,
                    "bookNumber": book.get("number"),
                    "psalmNumber": analysis.get("number"),
                    "psalmTitle": analysis.get("title"),
                    "themeId": theme_id,
                    "label": label,
                    "importance": theme.get("importance"),
                    "directness": theme.get("directness"),
                    "verseNumbers": theme.get("verseNumbers") or [],
                    "teaching": teaching,
                    "retrievalBuckets": buckets,
                }
                if theme_id == ANCHOR:
                    anchor_occurrences.append(occurrence)
                if not buckets or not theme.get("verseNumbers") or not teaching:
                    continue
                if len(by_theme[theme_id]) < MAX_OCCURRENCES_PER_THEME:
                    by_theme[theme_id].append(occurrence)

    candidates = []
    for theme_id, rows in by_theme.items():
        bucket_set = sorted({bucket for row in rows for bucket in row["retrievalBuckets"]})
        candidates.append({
            "themeId": theme_id,
            "labels": sorted({row["label"] for row in rows if row["label"]}),
            "retrievalBuckets": bucket_set,
            "occurrences": rows,
            "semanticClaim": False,
        })

    bucket_weight = {"father_union": 0, "father_nature": 1, "divine_union": 2, "nature_union": 3}
    candidates.sort(key=lambda item: (
        min(bucket_weight[b] for b in item["retrievalBuckets"]),
        0 if item["themeId"] == ANCHOR else 1,
        item["themeId"],
    ))

    payload = {
        "schemaVersion": 1,
        "recordType": "union-pere-nature-semantic-neighborhood",
        "anchorThemeId": ANCHOR,
        "semanticClaim": False,
        "automaticRelationTyping": False,
        "source": "data/thematic-index/books/book-*.json",
        "selectionMethod": (
            "Lexical cue groups over canonical theme labels and teachings select a bounded set for human review only. "
            "Cue overlap, cooccurrence and lexical similarity are not semantic evidence by themselves."
        ),
        "anchorOccurrences": anchor_occurrences,
        "candidateThemeCount": len(candidates),
        "candidates": candidates,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
