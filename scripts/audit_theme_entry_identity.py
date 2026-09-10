#!/usr/bin/env python3
"""Protect the presentation-only identity of a uniquely resolved canonical theme."""
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
ENTRY_JS = ROOT / "js" / "theme-entry.js"
INDEX_HTML = ROOT / "index.html"
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
        exact = [theme["id"] for theme in themes if form in {norm(theme.get("label")), norm(theme.get("id"))}]
        if exact:
            return exact
    return []


def literal_psalm_ids(query: str, records: list[dict]) -> list[str]:
    needle = norm(query)
    if not needle:
        return []
    wrapped = f" {needle} "
    found = []
    for record in records:
        if record.get("recordType") != "psalm":
            continue
        fragments = [record.get("title", ""), *[v.get("text", "") for v in record.get("verses", [])]]
        if any(wrapped in f" {norm(fragment)} " for fragment in fragments):
            found.append(record["id"])
    return found


def identity_allowed(theme_ids: list[str]) -> bool:
    return len(theme_ids) == 1


def main() -> None:
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    themes = json.loads(DIRECTORY.read_text(encoding="utf-8"))["themes"]
    records = json.loads(BUNDLE.read_text(encoding="utf-8"))["records"]
    entry_js = ENTRY_JS.read_text(encoding="utf-8")
    index_html = INDEX_HTML.read_text(encoding="utf-8")

    canonical = resolve_theme_ids("alliance", runtime, themes)
    assert len(canonical) == 1 and identity_allowed(canonical), canonical

    assembly = resolve_theme_ids("Assemblée", runtime, themes)
    assert assembly == [] and literal_psalm_ids("Assemblée", records), assembly
    assert not identity_allowed(assembly), "textual fallback must never receive a theme-entry identity"

    absent_query = "qzjxv terme volontairement absent"
    absent = resolve_theme_ids(absent_query, runtime, themes)
    assert absent == [] and literal_psalm_ids(absent_query, records) == []
    assert not identity_allowed(absent), "no-result state must never receive a theme-entry identity"

    ambiguous = next(
        ((alias, data.get("themeIds", [])) for alias, data in runtime.get("aliases", {}).items() if len(data.get("themeIds", [])) > 1),
        None,
    )
    assert ambiguous is not None, "runtime must expose at least one ambiguous alias sentinel"
    assert not identity_allowed(ambiguous[1]), ambiguous

    assert 'id="themeEntryIdentity"' in index_html
    assert 'id="themeEntryName"' in index_html
    assert 'id="themeEntryCount"' in index_html
    assert 'id="documentResultsTitle"' in index_html
    assert 'js/theme-entry.js' in index_html and 'css/theme-entry.css' in index_html
    assert "THÈME INDEXÉ DU CORPUS" in index_html
    assert "Textes indexés pour ce thème" in entry_js
    assert "labels.size === 1" in entry_js
    assert "themeCards.length === cards.length" in entry_js
    assert "isCurrentAmbiguousQuery" in entry_js
    assert "Voir le psaume source" in entry_js
    assert "fetch(" not in entry_js, "presentation layer must not re-resolve or enrich semantic data"
    for forbidden in ("themeId", "aliases", "relationType", "equivalent_to", "broader_than", "component_of", "related_to"):
        assert forbidden not in entry_js, f"presentation layer must not introduce semantic machinery: {forbidden}"

    print(
        "Theme entry identity OK: "
        f"canonical={canonical[0]}; fallback=no-identity; absent=no-identity; "
        f"ambiguous={ambiguous[0]}({len(ambiguous[1])} themes)=no-identity; presentation-only"
    )


if __name__ == "__main__":
    main()
