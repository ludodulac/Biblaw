#!/usr/bin/env python3
"""Audit Biblaw's production search contract without inventing semantics.

The browser thematic resolver is intentionally strict: normalized runtime alias, then
exact canonical label/id, otherwise no thematic result. Literal text search and psalm
number lookup are separate contracts.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
BOOKS = INDEX / "books"
BUNDLE = ROOT / "data" / "browser-search-catalog.json"
QUERIES = (
    "Dieu", "alliance", "alliance de lumière", "lumière",
    "assemblée", "l’assemblée", "sainte assemblée", "la sainte assemblée",
    "argent", "chouette", "abeille", "22 commandements",
)
ARTICLES = {"l", "le", "la", "les", "un", "une", "des"}
IMPORTANCE_RANK = {"central": 0, "important": 1, "related": 2}
EXPECTED_THEMES = {
    "Dieu": ["dieu"],
    "alliance": ["alliance"],
    "alliance de lumière": ["alliance", "alliance-de-lumiere"],
    "lumière": ["lumiere"],
    "assemblée": [],
    "l’assemblée": [],
    "sainte assemblée": ["sainte-assemblee"],
    "la sainte assemblée": ["sainte-assemblee"],
    "argent": ["argent"],
    "chouette": ["chouette"],
    "abeille": ["abeille"],
    "22 commandements": ["22-commandements"],
}


def norm(value: object) -> str:
    text = "".join(
        c for c in unicodedata.normalize("NFD", str(value or ""))
        if unicodedata.category(c) != "Mn"
    ).lower()
    text = text.replace("œ", "oe").replace("æ", "ae").replace("’", " ").replace("'", " ")
    text = re.sub(r"[^a-z0-9\s-]", " ", text).replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def query_forms(value: str) -> list[str]:
    q = norm(value)
    parts = q.split()
    stripped = " ".join(parts[1:]) if len(parts) > 1 and parts[0] in ARTICLES else q
    return list(dict.fromkeys(form for form in (q, stripped) if form))


def literal_contains(value: object, query: str) -> bool:
    needle = norm(query)
    return bool(needle) and f" {needle} " in f" {norm(value)} "


def resolve(query: str, runtime: dict, themes: list[dict], by_id: dict[str, dict]) -> tuple[str, list[dict]]:
    """Mirror js/biblaw.js exactly: alias -> exact -> none. Never fuzzy/sub-string."""
    forms = query_forms(query)
    for form in forms:
        alias = runtime.get("aliases", {}).get(form)
        if alias and alias.get("themeIds"):
            return "alias", [by_id[theme_id] for theme_id in alias["themeIds"] if theme_id in by_id]
    for form in forms:
        exact = [theme for theme in themes if form in {norm(theme.get("label")), norm(theme.get("id"))}]
        if exact:
            return "exact", exact
    return "none", []


def load_analyses() -> tuple[dict[str, dict], Counter]:
    analyses: dict[str, dict] = {}
    relation_pairs: Counter = Counter()
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for psalm in data.get("psalmAnalyses", []):
            record_id = psalm.get("recordId")
            if not record_id:
                continue
            analyses[record_id] = psalm
            for relation in psalm.get("themes", []):
                if relation.get("themeId"):
                    relation_pairs[(record_id, relation["themeId"])] += 1
    return analyses, relation_pairs


def main() -> None:
    runtime = json.loads((INDEX / "theme-search-runtime.json").read_text(encoding="utf-8"))
    directory = json.loads((INDEX / "theme-directory.json").read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    themes = directory["themes"]
    by_id = {theme["id"]: theme for theme in themes}
    psalms = [record for record in bundle["records"] if record.get("recordType") == "psalm"]
    analyses, relation_pairs = load_analyses()

    duplicate_pairs = [(pair, count) for pair, count in relation_pairs.items() if count > 1]
    assert not duplicate_pairs, f"duplicate canonical theme/Psalm pairs: {duplicate_pairs[:10]}"

    indexed_ids = {
        occurrence["recordId"]
        for theme in themes
        for occurrence in theme.get("occurrences", [])
        if occurrence.get("recordId")
    }
    browser_ids = {record["id"] for record in psalms if record.get("id")}
    analysis_ids = set(analyses)
    assert browser_ids == analysis_ids == indexed_ids, (
        f"coverage mismatch browser={len(browser_ids)} analyses={len(analysis_ids)} indexed={len(indexed_ids)}"
    )
    assert all(analysis.get("themes") for analysis in analyses.values())
    print(
        f"COVERAGE browserPsalms={len(browser_ids)} analyses={len(analysis_ids)} "
        f"indexedPsalms={len(indexed_ids)} duplicateThemePsalmPairs=0"
    )

    ambiguous = {key: alias for key, alias in runtime["aliases"].items() if alias.get("ambiguous")}
    assert len(ambiguous) == runtime["ambiguousAliasCount"] == 9
    assert runtime["semanticMerging"] is False
    assert runtime["connectionMeaning"] == "psalm-cooccurrence-only"
    print(f"Runtime: {len(themes)} themes; {runtime['aliasCount']} aliases; {len(ambiguous)} ambiguous aliases")

    observed: dict[str, dict] = {}
    for query in QUERIES:
        source, resolved = resolve(query, runtime, themes, by_id)
        resolved_ids = [theme["id"] for theme in resolved]
        per_record: dict[str, tuple[dict, dict]] = {}
        for theme in resolved:
            for occurrence in theme.get("occurrences", []):
                record_id = occurrence.get("recordId")
                if not record_id:
                    continue
                current = per_record.get(record_id)
                candidate_key = (
                    IMPORTANCE_RANK.get(occurrence.get("importance"), 3),
                    -(occurrence.get("score") or 0),
                    theme["id"],
                )
                if current is None:
                    per_record[record_id] = (theme, occurrence)
                    continue
                old_theme, old_occurrence = current
                old_key = (
                    IMPORTANCE_RANK.get(old_occurrence.get("importance"), 3),
                    -(old_occurrence.get("score") or 0),
                    old_theme["id"],
                )
                if candidate_key < old_key:
                    per_record[record_id] = (theme, occurrence)

        ordered = sorted(
            per_record.items(),
            key=lambda item: (
                IMPORTANCE_RANK.get(item[1][1].get("importance"), 3),
                next((record.get("number", 9999) for record in psalms if record.get("id") == item[0]), 9999),
                item[0],
            ),
        )
        ranks = [IMPORTANCE_RANK.get(value[1][1].get("importance"), 3) for value in ordered]
        assert ranks == sorted(ranks), f"importance order broken for {query!r}"

        levels = Counter(occurrence.get("importance", "unknown") for _, occurrence in per_record.values())
        missing_verses = sum(not occurrence.get("verseNumbers") for _, occurrence in per_record.values())
        missing_teaching = sum(not str(occurrence.get("teaching", "")).strip() for _, occurrence in per_record.values())
        literal_count = sum(
            any(
                literal_contains(fragment, query)
                for fragment in [record.get("title", ""), *[verse.get("text", "") for verse in record.get("verses", [])]]
            )
            for record in psalms
        )
        observed[query] = {
            "themes": resolved_ids,
            "indexed": len(per_record),
            "importance": levels,
            "missingVerseNumbers": missing_verses,
            "missingTeaching": missing_teaching,
            "literal": literal_count,
        }
        print(
            f"QUERY {query!r}: resolution={source}; themes={','.join(resolved_ids) or '-'}; "
            f"indexed={len(per_record)}; importance={dict(levels)}; "
            f"missingVerseNumbers={missing_verses}; missingTeaching={missing_teaching}; literal={literal_count}"
        )

    for query, expected_ids in EXPECTED_THEMES.items():
        assert observed[query]["themes"] == expected_ids, (
            f"unexpected thematic resolution for {query!r}: {observed[query]['themes']} != {expected_ids}"
        )
        assert observed[query]["missingVerseNumbers"] == 0
        assert observed[query]["missingTeaching"] == 0

    assert observed["assemblée"]["themes"] == observed["l’assemblée"]["themes"] == []
    assert observed["sainte assemblée"]["themes"] == observed["la sainte assemblée"]["themes"] == ["sainte-assemblee"]
    assert observed["sainte assemblée"]["indexed"] == 3
    assert observed["sainte assemblée"]["importance"] == Counter({"important": 2, "central": 1})

    assembly_alias = runtime["aliases"].get("assemblee")
    assert not assembly_alias or "sainte-assemblee" not in assembly_alias.get("themeIds", []), (
        "generic 'assemblée' must not be redirected to Sainte Assemblée"
    )
    sacred_alias = runtime["aliases"].get("sainte assemblee")
    assert sacred_alias and sacred_alias.get("themeIds") == ["sainte-assemblee"] and not sacred_alias.get("ambiguous")

    alliance_light = runtime["aliases"].get("alliance de lumiere")
    assert alliance_light and alliance_light.get("ambiguous") is True
    assert set(alliance_light["themeIds"]) == {"alliance", "alliance-de-lumiere"}

    print("Production search contract OK: explicit thematic resolution, literal text separation, canonical coverage complete")


if __name__ == "__main__":
    main()
