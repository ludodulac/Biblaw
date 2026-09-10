#!/usr/bin/env python3
"""Protect the generic encyclopedic fallback without changing semantic resolution.

The browser contract is:
1. canonical theme when strict resolution succeeds;
2. otherwise literal corpus exploration when text exists;
3. otherwise a genuine no-result state.

Literal presence never creates an alias, a theme, or a conceptual relation.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
DIRECTORY = INDEX / "theme-directory-public.json"
RUNTIME = INDEX / "theme-search-runtime.json"
BUNDLE = ROOT / "data" / "browser-search-catalog.json"
BROWSER_JS = ROOT / "js" / "biblaw.js"
ARTICLES = {"l", "le", "la", "les", "un", "une", "des"}


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


def resolve_theme_ids(query: str, runtime: dict, themes: list[dict]) -> list[str]:
    by_id = {theme["id"]: theme for theme in themes}
    for form in query_forms(query):
        alias = runtime.get("aliases", {}).get(form)
        if alias and alias.get("themeIds"):
            return [theme_id for theme_id in alias["themeIds"] if theme_id in by_id]
    for form in query_forms(query):
        exact = [
            theme["id"]
            for theme in themes
            if form in {norm(theme.get("label")), norm(theme.get("id"))}
        ]
        if exact:
            return exact
    return []


def literal_psalm_ids(query: str, records: list[dict]) -> list[str]:
    needle = norm(query)
    if not needle:
        return []
    wrapped_needle = f" {needle} "
    found = []
    for record in records:
        if record.get("recordType") != "psalm":
            continue
        fragments = [record.get("title", ""), *[v.get("text", "") for v in record.get("verses", [])]]
        if any(wrapped_needle in f" {norm(fragment)} " for fragment in fragments):
            found.append(record["id"])
    return found


def route(query: str, runtime: dict, themes: list[dict], records: list[dict]) -> tuple[str, list[str], list[str]]:
    theme_ids = resolve_theme_ids(query, runtime, themes)
    if theme_ids:
        return "theme", theme_ids, literal_psalm_ids(query, records)
    textual_ids = literal_psalm_ids(query, records)
    if textual_ids:
        return "textual-fallback", [], textual_ids
    return "no-result", [], []


def main() -> None:
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    themes = json.loads(DIRECTORY.read_text(encoding="utf-8"))["themes"]
    records = json.loads(BUNDLE.read_text(encoding="utf-8"))["records"]
    browser_js = BROWSER_JS.read_text(encoding="utf-8")

    resolved = route("alliance", runtime, themes, records)
    assert resolved[0] == "theme" and "alliance" in resolved[1], resolved

    assembly = route("Assemblée", runtime, themes, records)
    assert assembly[0] == "textual-fallback", assembly
    assert assembly[1] == [], assembly
    assert assembly[2], "Assemblée must have literal corpus occurrences for the product sentinel"
    assembly_alias = runtime.get("aliases", {}).get("assemblee")
    assert not assembly_alias or "sainte-assemblee" not in assembly_alias.get("themeIds", []), (
        "generic Assemblée must still not resolve to Sainte Assemblée"
    )

    absent_query = "qzjxv terme volontairement absent"
    absent = route(absent_query, runtime, themes, records)
    assert absent == ("no-result", [], []), absent

    # Protect the browser implementation as well as the data-level routing model.
    assert "return render(textual,[],{textualCount:textual.length,unresolvedTheme:true,textualFallback:true});" in browser_js
    assert "OCCURRENCE DU TERME DANS LE CORPUS" in browser_js
    assert "THÈME INDEXÉ" in browser_js
    assert "Thèmes canoniques indexés dans ce psaume" in browser_js
    assert "Ces occurrences ne constituent pas un thème." in browser_js
    assert "assemblée" not in browser_js.casefold(), "browser fallback must remain generic, never query-specific"
    assert "sainte-assemblee" not in browser_js.casefold(), "browser fallback must remain generic, never theme-specific"

    print(
        "Encyclopedic fallback OK: "
        f"resolved-theme={resolved[1]}; "
        f"assemblée=textual-fallback({len(assembly[2])} psalms); "
        "absent=no-result; no semantic promotion"
    )


if __name__ == "__main__":
    main()
