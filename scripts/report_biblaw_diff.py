#!/usr/bin/env python3
"""Show significant Biblaw generated/search differences against a git baseline.

Default usage compares the current working tree with HEAD:
  python scripts/report_biblaw_diff.py

After committing, compare the commit with its parent:
  python scripts/report_biblaw_diff.py --base HEAD~1

The report is intentionally compact: counters, theme/relation/alias/ambiguity changes, material
ranking changes, validation errors/warnings and production sentinel changes. It does not mutate data.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path

from audit_production_search_queries import IMPORTANCE_RANK, QUERIES, norm, resolve

ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "validation": "data/thematic-index/validation-report.json",
    "runtime": "data/thematic-index/theme-search-runtime.json",
    "quality": "data/thematic-index/theme-quality-audit.json",
    "directory": "data/thematic-index/theme-directory.json",
    "bundle": "data/browser-search-catalog.json",
}
MAX_ITEMS = 12


def current_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git_json(base: str, path: str) -> dict | None:
    proc = subprocess.run(
        ["git", "show", f"{base}:{path}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return None
    return json.loads(proc.stdout)


def metrics(data: dict[str, dict]) -> dict:
    validation = data["validation"]
    runtime = data["runtime"]
    quality = data["quality"]
    stats = quality.get("stats", {})
    vstats = validation.get("stats", {})
    return {
        "books": vstats.get("books"),
        "psalms": vstats.get("psalmAnalyses"),
        "relations": vstats.get("themeRelations"),
        "validationErrors": len(validation.get("errors", [])),
        "validationWarnings": len(validation.get("warnings", [])),
        "themes": runtime.get("themeCount"),
        "aliases": runtime.get("aliasCount"),
        "ambiguities": runtime.get("ambiguousAliasCount"),
        "directoryCollisions": stats.get("normalizedDirectoryCollisionCount"),
        "relationsWithoutVerses": stats.get("relationsWithoutVerseNumbers"),
        "relationsWithoutTeaching": stats.get("relationsWithoutTeaching"),
    }


def alias_map(runtime: dict) -> dict[str, tuple[tuple[str, ...], bool]]:
    return {
        key: (tuple(item.get("themeIds", [])), bool(item.get("ambiguous")))
        for key, item in (runtime.get("aliases") or {}).items()
    }


def ambiguity_map(runtime: dict) -> dict[str, tuple[str, ...]]:
    return {
        key: targets
        for key, (targets, ambiguous) in alias_map(runtime).items()
        if ambiguous
    }


def theme_map(directory: dict) -> dict[str, dict]:
    return {item["id"]: item for item in directory.get("themes", []) if item.get("id")}


def relation_map(directory: dict) -> dict[tuple[str, str], dict]:
    """Index canonical projected theme-Psalm relations for compact before/after review."""
    relations: dict[tuple[str, str], dict] = {}
    for theme in directory.get("themes", []):
        theme_id = theme.get("id")
        if not theme_id:
            continue
        for occurrence in theme.get("occurrences", []):
            record_id = occurrence.get("recordId")
            if not record_id:
                continue
            key = (theme_id, record_id)
            if key in relations:
                raise AssertionError(f"duplicate projected relation in directory: {key}")
            relations[key] = {
                "importance": occurrence.get("importance"),
                "directness": occurrence.get("directness"),
                "verseNumbers": tuple(occurrence.get("verseNumbers", [])),
                "teaching": occurrence.get("teaching"),
            }
    return relations


def theme_ranking_signature(theme: dict) -> tuple:
    levels = Counter(o.get("importance", "unknown") for o in theme.get("occurrences", []))
    return (
        theme.get("occurrenceCount", 0),
        theme.get("centralPsalmCount", 0),
        theme.get("score", 0),
        levels.get("central", 0),
        levels.get("important", 0),
        levels.get("related", 0),
    )


def sentinel_state(runtime: dict, directory: dict, bundle: dict) -> dict[str, dict]:
    themes = directory.get("themes", [])
    by_id = {theme["id"]: theme for theme in themes if theme.get("id")}
    psalms = [r for r in bundle.get("records", []) if r.get("recordType") == "psalm"]
    number_by_id = {r.get("id"): r.get("number", 9999) for r in psalms}

    # Normalize each searchable fragment once. This mirrors the browser's pre-indexing strategy and
    # keeps the diff report cheap without changing literal matching semantics.
    normalized_fragments = {
        r.get("id"): [
            norm(r.get("title", "")),
            *[norm(v.get("text", "")) for v in r.get("verses", [])],
        ]
        for r in psalms
    }
    result: dict[str, dict] = {}

    for query in QUERIES:
        source, resolved = resolve(query, runtime, themes, by_id)
        per_record: dict[str, tuple[dict, dict]] = {}
        for theme in resolved:
            for occurrence in theme.get("occurrences", []):
                record_id = occurrence.get("recordId")
                if not record_id:
                    continue
                candidate = (
                    IMPORTANCE_RANK.get(occurrence.get("importance"), 3),
                    -(occurrence.get("score") or 0),
                    theme["id"],
                )
                current = per_record.get(record_id)
                if current is None:
                    per_record[record_id] = (theme, occurrence)
                    continue
                old_theme, old_occurrence = current
                old = (
                    IMPORTANCE_RANK.get(old_occurrence.get("importance"), 3),
                    -(old_occurrence.get("score") or 0),
                    old_theme["id"],
                )
                if candidate < old:
                    per_record[record_id] = (theme, occurrence)

        ordered = sorted(
            per_record.items(),
            key=lambda item: (
                IMPORTANCE_RANK.get(item[1][1].get("importance"), 3),
                number_by_id.get(item[0], 9999),
                item[0],
            ),
        )
        levels = Counter(occ.get("importance", "unknown") for _, occ in per_record.values())
        needle = norm(query)
        literal = sum(
            bool(needle)
            and any(f" {needle} " in f" {fragment} " for fragment in normalized_fragments.get(r.get("id"), []))
            for r in psalms
        )
        result[query] = {
            "resolution": source,
            "themes": tuple(theme["id"] for theme in resolved),
            "indexed": len(ordered),
            "importance": tuple(sorted(levels.items())),
            "literal": literal,
        }
    return result


def fmt_delta(before, after) -> str:
    if isinstance(before, int) and isinstance(after, int):
        delta = after - before
        return f"{before} -> {after} ({delta:+d})"
    return f"{before!r} -> {after!r}"


def limited(values) -> list:
    return list(values)[:MAX_ITEMS]


def relation_name(key: tuple[str, str]) -> str:
    return f"{key[0]} @ {key[1]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD", help="git ref used as baseline; default: HEAD")
    args = parser.parse_args()

    current = {name: current_json(path) for name, path in PATHS.items()}
    baseline = {name: git_json(args.base, path) for name, path in PATHS.items()}
    missing = [name for name, value in baseline.items() if value is None]
    if missing:
        raise SystemExit(f"Baseline {args.base!r} is missing required generated files: {missing}")

    before_metrics = metrics(baseline)  # type: ignore[arg-type]
    after_metrics = metrics(current)
    changed_metrics = {
        key: (before_metrics[key], after_metrics[key])
        for key in before_metrics
        if before_metrics[key] != after_metrics[key]
    }

    before_themes = theme_map(baseline["directory"])  # type: ignore[index]
    after_themes = theme_map(current["directory"])
    added_themes = sorted(set(after_themes) - set(before_themes))
    removed_themes = sorted(set(before_themes) - set(after_themes))
    ranking_changes = []
    for theme_id in sorted(set(before_themes) & set(after_themes)):
        before_sig = theme_ranking_signature(before_themes[theme_id])
        after_sig = theme_ranking_signature(after_themes[theme_id])
        if before_sig != after_sig:
            ranking_changes.append((theme_id, before_sig, after_sig))

    before_relations = relation_map(baseline["directory"])  # type: ignore[index]
    after_relations = relation_map(current["directory"])
    added_relations = sorted(set(after_relations) - set(before_relations))
    removed_relations = sorted(set(before_relations) - set(after_relations))
    changed_importance = []
    changed_evidence = []
    for key in sorted(set(before_relations) & set(after_relations)):
        before = before_relations[key]
        after = after_relations[key]
        if before["importance"] != after["importance"]:
            changed_importance.append((key, before["importance"], after["importance"]))
        evidence_fields = ("directness", "verseNumbers", "teaching")
        if any(before[field] != after[field] for field in evidence_fields):
            changed_evidence.append(key)

    before_aliases = alias_map(baseline["runtime"])  # type: ignore[index]
    after_aliases = alias_map(current["runtime"])
    added_aliases = sorted(set(after_aliases) - set(before_aliases))
    removed_aliases = sorted(set(before_aliases) - set(after_aliases))
    changed_aliases = sorted(
        key for key in set(before_aliases) & set(after_aliases)
        if before_aliases[key] != after_aliases[key]
    )

    before_amb = ambiguity_map(baseline["runtime"])  # type: ignore[index]
    after_amb = ambiguity_map(current["runtime"])
    added_amb = sorted(set(after_amb) - set(before_amb))
    removed_amb = sorted(set(before_amb) - set(after_amb))
    changed_amb = sorted(
        key for key in set(before_amb) & set(after_amb) if before_amb[key] != after_amb[key]
    )

    before_sentinels = sentinel_state(
        baseline["runtime"], baseline["directory"], baseline["bundle"]  # type: ignore[arg-type]
    )
    after_sentinels = sentinel_state(current["runtime"], current["directory"], current["bundle"])
    sentinel_changes = [
        (query, before_sentinels[query], after_sentinels[query])
        for query in QUERIES
        if before_sentinels[query] != after_sentinels[query]
    ]

    print(f"BIBLAW DIFF baseline={args.base}")
    if changed_metrics:
        print("\nCOUNTERS")
        for key, (before, after) in changed_metrics.items():
            print(f"  {key}: {fmt_delta(before, after)}")
    else:
        print("\nCOUNTERS: no change")

    if added_themes or removed_themes:
        print("\nTHEME IDS")
        if added_themes:
            print(f"  added({len(added_themes)}): {limited(added_themes)}")
        if removed_themes:
            print(f"  removed({len(removed_themes)}): {limited(removed_themes)}")

    if added_relations or removed_relations or changed_importance or changed_evidence:
        print("\nTHEME-PSALM RELATIONS")
        if added_relations:
            print(f"  added({len(added_relations)}): {[relation_name(x) for x in limited(added_relations)]}")
        if removed_relations:
            print(f"  removed({len(removed_relations)}): {[relation_name(x) for x in limited(removed_relations)]}")
        if changed_importance:
            print(f"  reclassified({len(changed_importance)}):")
            for key, before, after in changed_importance[:MAX_ITEMS]:
                print(f"    {relation_name(key)}: {before} -> {after}")
        if changed_evidence:
            print(
                f"  evidenceChanged({len(changed_evidence)}): "
                f"{[relation_name(x) for x in limited(changed_evidence)]}"
            )

    if added_aliases or removed_aliases or changed_aliases:
        print("\nALIASES")
        if added_aliases:
            print(f"  added({len(added_aliases)}): {limited(added_aliases)}")
        if removed_aliases:
            print(f"  removed({len(removed_aliases)}): {limited(removed_aliases)}")
        if changed_aliases:
            print(f"  changed({len(changed_aliases)}):")
            for key in changed_aliases[:MAX_ITEMS]:
                print(f"    {key!r}: {before_aliases[key]} -> {after_aliases[key]}")

    if added_amb or removed_amb or changed_amb:
        print("\nAMBIGUITIES")
        if added_amb:
            print(f"  added: {limited(added_amb)}")
        if removed_amb:
            print(f"  removed: {limited(removed_amb)}")
        for key in limited(changed_amb):
            print(f"  changed {key!r}: {before_amb[key]} -> {after_amb[key]}")

    if ranking_changes:
        print(f"\nTHEME RANKING METRICS changedThemes={len(ranking_changes)}")
        for theme_id, before, after in ranking_changes[:MAX_ITEMS]:
            print(
                f"  {theme_id}: occurrence/central/score/C/I/L "
                f"{before} -> {after}"
            )

    if sentinel_changes:
        print(f"\nSENTINELS changed={len(sentinel_changes)}")
        for query, before, after in sentinel_changes:
            print(f"  {query!r}: {before} -> {after}")
    else:
        print("\nSENTINELS: no change")

    significant = bool(
        changed_metrics
        or added_themes
        or removed_themes
        or added_relations
        or removed_relations
        or changed_importance
        or changed_evidence
        or added_aliases
        or removed_aliases
        or changed_aliases
        or added_amb
        or removed_amb
        or changed_amb
        or ranking_changes
        or sentinel_changes
    )
    print(f"\nSUMMARY significantChanges={'yes' if significant else 'no'}")


if __name__ == "__main__":
    main()
