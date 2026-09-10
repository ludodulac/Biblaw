#!/usr/bin/env python3
"""Measure structural thematic coverage without claiming semantic exhaustiveness."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus/books"
THEMATIC = ROOT / "data/thematic-index/books"
DIRECTORY = ROOT / "data/thematic-index/theme-directory.json"
SEARCH_INDEX = ROOT / "data/thematic-index/theme-search-index.json"
RELATIONS = ROOT / "data/thematic-index/theme-relations-validated.json"
OUT = ROOT / "data/thematic-index/thematic-coverage-report.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    corpus_ids = set()
    corpus_book_counts = Counter()
    for path in sorted(CORPUS.glob("book-*/psalm-*.json")):
        record = load(path)
        rid = record.get("id")
        if not rid:
            raise AssertionError(f"missing corpus id: {path.relative_to(ROOT)}")
        if rid in corpus_ids:
            raise AssertionError(f"duplicate corpus id: {rid}")
        corpus_ids.add(rid)
        corpus_book_counts[path.parent.name] += 1

    analysis_ids = set()
    theme_occurrences = 0
    theme_ids = set()
    labels_by_theme = defaultdict(set)
    importance_counts = Counter()
    directness_counts = Counter()
    empty_theme_psalms = []
    incomplete_books = []

    thematic_files = sorted(THEMATIC.glob("book-*.json"))
    for path in thematic_files:
        data = load(path)
        method = data.get("method") or {}
        if not (
            method.get("status") == "editorial-indexing-complete"
            and method.get("semanticPass") == "deep-content-grounded-complete"
            and method.get("contentGrounding") == "complete"
        ):
            incomplete_books.append(path.name)
        for psalm in data.get("psalmAnalyses", []):
            rid = psalm.get("recordId")
            if not rid:
                raise AssertionError(f"missing analysis id: {path.relative_to(ROOT)}")
            if rid in analysis_ids:
                raise AssertionError(f"duplicate thematic analysis id: {rid}")
            analysis_ids.add(rid)
            themes = psalm.get("themes", [])
            if not themes:
                empty_theme_psalms.append(rid)
            for theme in themes:
                tid = theme.get("themeId")
                if not tid:
                    continue
                theme_occurrences += 1
                theme_ids.add(tid)
                label = str(theme.get("label") or "").strip()
                if label:
                    labels_by_theme[tid].add(label)
                importance_counts[str(theme.get("importance"))] += 1
                directness_counts[str(theme.get("directness"))] += 1

    directory = load(DIRECTORY)
    directory_ids = {t.get("id") for t in directory.get("themes", []) if t.get("id")}
    search_index = load(SEARCH_INDEX)
    search_ids = {t.get("themeId") for t in search_index.get("themes", []) if t.get("themeId")}
    aliases = search_index.get("aliases", [])
    ambiguous_aliases = [alias for alias in aliases if alias.get("ambiguous") or len(alias.get("themeIds", [])) > 1]
    relations = load(RELATIONS)

    missing_analysis = sorted(corpus_ids - analysis_ids)
    extra_analysis = sorted(analysis_ids - corpus_ids)
    missing_directory = sorted(theme_ids - directory_ids)
    extra_directory = sorted(directory_ids - theme_ids)
    missing_search_index = sorted(theme_ids - search_ids)
    extra_search_index = sorted(search_ids - theme_ids)
    label_variant_theme_ids = sorted(tid for tid, labels in labels_by_theme.items() if len(labels) > 1)

    relation_endpoint_ids = {
        tid
        for rel in relations.get("relations", [])
        for tid in (rel.get("sourceThemeId"), rel.get("targetThemeId"))
        if tid
    }
    relation_endpoints_missing_from_search = sorted(relation_endpoint_ids - search_ids)

    structural_complete = not missing_analysis and not extra_analysis and not incomplete_books
    catalog_integrity_complete = not (
        missing_directory or extra_directory or missing_search_index or extra_search_index
        or relation_endpoints_missing_from_search
    )

    report = {
        "schemaVersion": 1,
        "recordType": "thematic-coverage-report",
        "generated": True,
        "claims": {
            "structuralPsalmCoverageComplete": structural_complete,
            "catalogIntegrityComplete": catalog_integrity_complete,
            "semanticExhaustivenessClaim": False,
            "semanticExhaustivenessReason": (
                "Every corpus Psalm can be checked for a grounded thematic analysis, but no deterministic audit can prove that every meaningful concept or every semantic reformulation has been identified."
            ),
        },
        "corpus": {
            "bookCount": len(corpus_book_counts),
            "psalmCount": len(corpus_ids),
        },
        "thematicAnalyses": {
            "bookFileCount": len(thematic_files),
            "psalmAnalysisCount": len(analysis_ids),
            "themeOccurrenceCount": theme_occurrences,
            "psalmsWithoutThemes": empty_theme_psalms,
            "missingPsalmAnalysisIds": missing_analysis,
            "extraPsalmAnalysisIds": extra_analysis,
            "incompleteBookFiles": incomplete_books,
            "importanceCounts": dict(sorted(importance_counts.items())),
            "directnessCounts": dict(sorted(directness_counts.items())),
        },
        "catalog": {
            "distinctDetectedThemeIdCount": len(theme_ids),
            "directoryThemeCount": len(directory_ids),
            "searchIndexThemeCount": len(search_ids),
            "searchIndexDeclaredThemeCount": search_index.get("themeCount"),
            "aliasCount": len(aliases),
            "searchIndexDeclaredAliasCount": search_index.get("aliasCount"),
            "ambiguousAliasCount": len(ambiguous_aliases),
            "searchIndexDeclaredAmbiguousAliasCount": search_index.get("ambiguousAliasCount"),
            "themeIdsWithMultipleObservedLabelsCount": len(label_variant_theme_ids),
            "themeIdsWithMultipleObservedLabels": label_variant_theme_ids,
            "detectedThemeIdsMissingFromDirectory": missing_directory,
            "directoryThemeIdsNotDetectedInAnalyses": extra_directory,
            "detectedThemeIdsMissingFromSearchIndex": missing_search_index,
            "searchIndexThemeIdsNotDetectedInAnalyses": extra_search_index,
            "semanticMerging": bool(search_index.get("semanticMerging", False)),
        },
        "validatedRelations": {
            "count": len(relations.get("relations", [])),
            "publicSearchEffect": relations.get("publicSearchEffect"),
            "endpointIdsMissingFromSearchIndex": relation_endpoints_missing_from_search,
        },
    }

    assert search_index.get("themeCount") == len(search_ids), "declared search themeCount mismatch"
    assert search_index.get("aliasCount") == len(aliases), "declared aliasCount mismatch"
    assert search_index.get("ambiguousAliasCount") == len(ambiguous_aliases), "declared ambiguousAliasCount mismatch"
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not structural_complete:
        raise SystemExit("Thematic structural coverage is incomplete")
    if not catalog_integrity_complete:
        raise SystemExit("Thematic catalog integrity is incomplete")


if __name__ == "__main__":
    main()
