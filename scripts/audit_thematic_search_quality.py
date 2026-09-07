#!/usr/bin/env python3
"""Audit the thematic index for search/navigation quality without changing editorial semantics.

This audit is intentionally conservative. It detects deterministic structural/lexical situations
that may reduce search quality (label collisions, inconsistent labels for one id, singletons,
composite labels, weakly grounded relations). It never merges or renames themes automatically.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
OUT = ROOT / "data/thematic-index/theme-quality-audit.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    text = re.sub(r"[’'`´]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def compact_theme(theme):
    return {
        "id": theme.get("id"),
        "label": theme.get("label"),
        "occurrenceCount": theme.get("occurrenceCount", 0),
        "centralPsalmCount": theme.get("centralPsalmCount", 0),
        "archangelCount": len(theme.get("archangels", [])),
    }


directory = load(DIRECTORY)
themes = directory.get("themes", [])

# Read the editorial sources directly because the generated directory keeps one display label per id.
id_labels = defaultdict(Counter)
label_ids = defaultdict(Counter)
relation_count = 0
relations_without_verses = []
relations_without_teaching = []
for path in sorted(BOOKS.glob("book-*.json")):
    data = load(path)
    book = data.get("book", {})
    for psalm in data.get("psalmAnalyses", []):
        for rel in psalm.get("themes", []):
            relation_count += 1
            tid = rel.get("themeId")
            label = rel.get("label")
            if tid and label:
                id_labels[tid][label] += 1
                label_ids[norm(label)][tid] += 1
            ref = {
                "bookNumber": book.get("number"),
                "psalmNumber": psalm.get("number"),
                "recordId": psalm.get("recordId"),
                "themeId": tid,
                "label": label,
            }
            if not rel.get("verseNumbers"):
                relations_without_verses.append(ref)
            if not (rel.get("teaching") or "").strip():
                relations_without_teaching.append(ref)

same_id_multiple_labels = []
for tid, labels in sorted(id_labels.items()):
    if len(labels) > 1:
        same_id_multiple_labels.append({
            "themeId": tid,
            "labels": [{"label": label, "count": count} for label, count in labels.most_common()],
        })

same_label_multiple_ids = []
for normalized, ids in sorted(label_ids.items()):
    if normalized and len(ids) > 1:
        display = sorted({label for tid in ids for label in id_labels[tid]})
        same_label_multiple_ids.append({
            "normalizedLabel": normalized,
            "labels": display,
            "themeIds": [{"id": tid, "count": count} for tid, count in ids.most_common()],
        })

by_norm = defaultdict(list)
for theme in themes:
    by_norm[norm(theme.get("label", ""))].append(theme)
normalized_collisions = [
    {"normalizedLabel": key, "themes": [compact_theme(t) for t in vals]}
    for key, vals in sorted(by_norm.items()) if key and len(vals) > 1
]

singletons = [compact_theme(t) for t in themes if t.get("occurrenceCount") == 1]
rare = [compact_theme(t) for t in themes if t.get("occurrenceCount", 0) <= 2]

# Composite labels are only review candidates: conjunctions can represent a legitimate indivisible theme.
composite_re = re.compile(r"\b(?:et|ou|avec|contre|sans|versus)\b|[/,+]", re.I)
composites = [compact_theme(t) for t in themes if composite_re.search(t.get("label", ""))]

archangel_spread = Counter()
for theme in themes:
    archangel_spread[len(theme.get("archangels", []))] += 1

report = {
    "schemaVersion": 1,
    "status": "review-candidates-generated",
    "purpose": "search-quality-audit-only; no automatic semantic merging or renaming",
    "stats": {
        "themeCount": len(themes),
        "themeRelationCount": relation_count,
        "singletonThemeCount": len(singletons),
        "rareThemeCountOccurrenceLTE2": len(rare),
        "sameIdMultipleLabelsCount": len(same_id_multiple_labels),
        "sameNormalizedLabelMultipleIdsCount": len(same_label_multiple_ids),
        "normalizedDirectoryCollisionCount": len(normalized_collisions),
        "compositeLabelCandidateCount": len(composites),
        "relationsWithoutVerseNumbers": len(relations_without_verses),
        "relationsWithoutTeaching": len(relations_without_teaching),
        "themeCountByArchangelCoverage": {str(k): v for k, v in sorted(archangel_spread.items())},
    },
    "hardStructuralIssues": {
        "sameIdMultipleLabels": same_id_multiple_labels,
        "sameNormalizedLabelMultipleIds": same_label_multiple_ids,
        "normalizedDirectoryCollisions": normalized_collisions,
        "relationsWithoutVerseNumbers": relations_without_verses,
        "relationsWithoutTeaching": relations_without_teaching,
    },
    "reviewCandidates": {
        "compositeLabels": composites,
        "singletons": singletons,
        "rareThemesOccurrenceLTE2": rare,
    },
    "policy": {
        "automaticMergeAllowed": False,
        "automaticRenameAllowed": False,
        "note": "Rare or composite themes are not errors. They require corpus-grounded review before any editorial consolidation.",
    },
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report["stats"], ensure_ascii=False, indent=2))
