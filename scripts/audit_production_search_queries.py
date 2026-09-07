#!/usr/bin/env python3
"""Audit the production search contract without changing canonical semantics.

This script mirrors the browser's deterministic query resolution for the passation
smoke queries. It reports thematic candidates, indexed psalm counts, importance
levels, support metadata and literal psalm counts. Ambiguous aliases are reported
as such and are never collapsed.
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
QUERIES = (
    "Dieu",
    "alliance",
    "alliance de lumière",
    "lumière",
    "assemblée",
    "l’assemblée",
    "sainte assemblée",
    "la sainte assemblée",
    "argent",
    "chouette",
    "abeille",
    "22 commandements",
)
ARTICLES = {"l", "le", "la", "les", "un", "une", "des"}
IMPORTANCE_RANK = {"central": 0, "important": 1, "related": 2}


def norm(value: object) -> str:
    text = "".join(
        c
        for c in unicodedata.normalize("NFD", str(value or ""))
        if unicodedata.category(c) != "Mn"
    ).lower()
    text = text.replace("œ", "oe").replace("æ", "ae").replace("’", " ").replace("'", " ")
    text = re.sub(r"[^a-z0-9\s-]", " ", text).replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def query_forms(value: str) -> list[str]:
    q = norm(value)
    parts = q.split()
    stripped = " ".join(parts[1:]) if len(parts) > 1 and parts[0] in ARTICLES else q
    return list(dict.fromkeys(x for x in (q, stripped) if x))


def literal_contains(value: object, query: str) -> bool:
    needle = norm(query)
    return bool(needle) and f" {needle} " in f" {norm(value)} "


def resolve(query: str, runtime: dict, themes: list[dict], by_id: dict[str, dict]) -> tuple[str, list[dict]]:
    forms = query_forms(query)
    for q in forms:
        alias = runtime.get("aliases", {}).get(q)
        if alias and alias.get("themeIds"):
            return "alias", [by_id[i] for i in alias["themeIds"] if i in by_id]
    for q in forms:
        exact = [t for t in themes if q == norm(t.get("label")) or q == norm(t.get("id"))]
        if exact:
            return "exact", exact
    q = forms[-1] if forms else ""
    fuzzy = [t for t in themes if q and (q in norm(t.get("label")) or norm(t.get("label")) in q)]
    fuzzy.sort(key=lambda t: (abs(len(norm(t.get("label"))) - len(q)), -(t.get("score") or 0), t.get("id", "")))
    return ("fuzzy", fuzzy[:1]) if fuzzy else ("none", [])


def editorial_theme_matches(term: str) -> list[dict]:
    needle = norm(term)
    matches = []
    for path in sorted(BOOKS.glob("book-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        book = data.get("book", {})
        for psalm in data.get("psalmAnalyses", []):
            for rel in psalm.get("themes", []):
                label = rel.get("label", "")
                theme_id = rel.get("themeId", "")
                if needle in norm(label) or needle in norm(theme_id):
                    matches.append({
                        "file": path.name,
                        "bookNumber": book.get("number"),
                        "psalmNumber": psalm.get("number"),
                        "recordId": psalm.get("recordId"),
                        "themeId": theme_id,
                        "label": label,
                        "importance": rel.get("importance"),
                        "verseNumbers": rel.get("verseNumbers", []),
                    })
    return matches


def main() -> None:
    runtime = json.loads((INDEX / "theme-search-runtime.json").read_text(encoding="utf-8"))
    directory = json.loads((INDEX / "theme-directory.json").read_text(encoding="utf-8"))
    bundle = json.loads((ROOT / "data" / "browser-search-catalog.json").read_text(encoding="utf-8"))
    themes = directory["themes"]
    by_id = {t["id"]: t for t in themes}
    psalms = [r for r in bundle["records"] if r.get("recordType") == "psalm"]

    ambiguous = {k: v for k, v in runtime["aliases"].items() if v.get("ambiguous")}
    print(f"Runtime: {len(themes)} themes; {len(ambiguous)} ambiguous aliases")
    for key, alias in sorted(ambiguous.items()):
        labels = [by_id[i]["label"] for i in alias["themeIds"] if i in by_id]
        print(f"AMBIGUOUS {key}: {' | '.join(labels)}")

    results = {}
    for query in QUERIES:
        source, resolved = resolve(query, runtime, themes, by_id)
        occurrences = []
        for theme in resolved:
            for occurrence in theme.get("occurrences", []):
                occurrences.append((theme, occurrence))
        per_record: dict[str, tuple[dict, dict]] = {}
        for theme, occurrence in occurrences:
            rid = occurrence.get("recordId")
            current = per_record.get(rid)
            candidate_key = (IMPORTANCE_RANK.get(occurrence.get("importance"), 3), -(occurrence.get("score") or 0), theme["id"])
            if current is None:
                per_record[rid] = (theme, occurrence)
            else:
                old_theme, old = current
                old_key = (IMPORTANCE_RANK.get(old.get("importance"), 3), -(old.get("score") or 0), old_theme["id"])
                if candidate_key < old_key:
                    per_record[rid] = (theme, occurrence)
        levels = Counter(o.get("importance", "unknown") for _, o in per_record.values())
        missing_verses = sum(not o.get("verseNumbers") for _, o in per_record.values())
        missing_teaching = sum(not str(o.get("teaching", "")).strip() for _, o in per_record.values())
        literal = sum(
            any(literal_contains(fragment, query) for fragment in [r.get("title", ""), *[v.get("text", "") for v in r.get("verses", [])]])
            for r in psalms
        )
        ids = ",".join(t["id"] for t in resolved) or "-"
        results[query] = [t["id"] for t in resolved]
        print(
            f"QUERY {query!r}: resolution={source}; themes={ids}; indexed={len(per_record)}; "
            f"importance={dict(levels)}; missingVerseNumbers={missing_verses}; "
            f"missingTeaching={missing_teaching}; literal={literal}"
        )

    # Query-normalization invariants required by the product contract.
    assert results["assemblée"] == results["l’assemblée"]
    assert results["sainte assemblée"] == results["la sainte assemblée"]
    if results["assemblée"] and results["sainte assemblée"]:
        assert set(results["assemblée"]) != set(results["sainte assemblée"]), "distinct resolved themes must remain distinct"
    else:
        print("UNRESOLVED_CONTRACT assembly queries: tracing canonical editorial relations")
        editorial = editorial_theme_matches("assembl")
        if editorial:
            for match in editorial:
                print(
                    "EDITORIAL assembly match: "
                    f"{match['file']} psalm={match['psalmNumber']} themeId={match['themeId']} "
                    f"label={match['label']!r} importance={match['importance']} verses={match['verseNumbers']}"
                )
        else:
            print("EDITORIAL assembly match: none in data/thematic-index/books/book-*.json")

    alliance_light = runtime["aliases"].get("alliance de lumiere")
    assert alliance_light and alliance_light.get("ambiguous") is True
    assert set(alliance_light["themeIds"]) == {"alliance", "alliance-de-lumiere"}


if __name__ == "__main__":
    main()
