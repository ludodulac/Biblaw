#!/usr/bin/env python3
"""Protect the first documentary-rubric pilot from search-contract regressions."""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

from build_theme_rubrics_public import build
from validate_theme_rubrics import load_json, validate

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "thematic-index"


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", str(value or ""))
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return " ".join(value.lower().replace("œ", "oe").replace("’", " ").replace("'", " ").replace("-", " ").split())


source = load_json(DATA / "theme-rubrics.json")
public = load_json(DATA / "theme-rubrics-public.json")
validate(source)
assert public == build(source), "public rubric projection must be generated exactly from the editorial source"

assert len(source["rubrics"]) == 1, "pilot must contain exactly one editorial rubric"
rubric = source["rubrics"][0]
assert rubric == {
    "rubricId": "pensee--pensee-et-concret",
    "themeId": "pensee",
    "label": "Pensée et concret",
    "recordIds": ["book-20-psalm-104", "book-20-psalm-105"],
    "validationStatus": "validated",
    "decisionProvenance": {
        "type": "ai-assisted-user-approved",
        "preparedBy": "openai-chatgpt",
        "approvedBy": "user",
        "approvedOn": "2026-09-11",
    },
}, "pilot rubric source drifted from the approved decision"
assert all(item["validationStatus"] == "validated" for item in source["rubrics"] if item["rubricId"] in {r["rubricId"] for r in public["rubrics"]}), (
    "only validated rubrics may reach the public projection"
)

# J: both pilot references must be real canonical occurrences of pensee, with existing importance untouched.
directory = load_json(DATA / "theme-directory-public.json")
pensee = next((theme for theme in directory.get("themes", []) if theme.get("id") == "pensee"), None)
assert pensee, "canonical theme pensee must exist"
occurrences = {item["recordId"]: item for item in pensee.get("occurrences", [])}
assert occurrences["book-20-psalm-104"]["importance"] == "central", "pilot occurrence 104 must remain Central"
assert occurrences["book-20-psalm-105"]["importance"] == "related", "pilot occurrence 105 must remain Lié"

rubric_id = rubric["rubricId"]
rubric_label_norm = norm(rubric["label"])
runtime = load_json(DATA / "theme-search-runtime.json")
search_index = load_json(DATA / "theme-search-index.json")
relations = load_json(DATA / "theme-relations-public.json")

# D/E/F: rubrics are not themes, aliases, runtime entries, or validated conceptual relations.
assert rubric_id not in json.dumps(runtime, ensure_ascii=False), "rubricId leaked into search runtime"
assert rubric_id not in json.dumps(search_index, ensure_ascii=False), "rubricId leaked into search index"
assert rubric_id not in json.dumps(relations, ensure_ascii=False), "rubricId leaked into validated relations"
assert rubric_label_norm not in {norm(alias) for alias in runtime.get("aliases", {}).keys()}, "rubric label became a runtime alias"
assert all(theme.get("id") != rubric_id and norm(theme.get("label")) != rubric_label_norm for theme in directory.get("themes", [])), (
    "rubric must not become a canonical theme"
)

# G: co-occurrence stays an independent generated layer; the pilot identifier must never enter it.
connections_text = (DATA / "theme-connections.json").read_text(encoding="utf-8")
assert rubric_id not in connections_text, "rubricId leaked into co-occurrence connections"

html = (ROOT / "index.html").read_text(encoding="utf-8")
engine_js = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
rubric_js = (ROOT / "js" / "theme-rubrics.js").read_text(encoding="utf-8")

# A/B/C/H: the search engine does not load or know the rubric layer at all.
assert "theme-rubrics" not in engine_js and "Pensée et concret" not in engine_js and rubric_id not in engine_js, (
    "search engine must remain independent from documentary rubrics"
)
assert "resolveIndexedThemes" in engine_js and "thematicItems" in engine_js and "textualFallback:true" in engine_js, (
    "existing thematic and textual-fallback paths must remain present"
)

# I + interface states: only canonical theme presentation can expose a validated public rubric.
assert "theme-rubrics-public.json" in rubric_js, "rubric UI must consume only the public projection"
assert "detail.kind !== 'canonical-theme'" in rubric_js, "rubric UI must hide outside canonical theme entries"
assert "themeRubrics.filter(rubric => rubric.themeId === activeThemeId)" not in rubric_js, "unexpected obsolete rubric filter form"
assert "rubrics.filter(rubric => rubric.themeId === activeThemeId)" in rubric_js, "rubric UI must scope rubrics to the active canonical theme"
assert "if (!rendered.length) return hide();" in rubric_js, "canonical themes without rubrics must hide the panel"
for kind in ("ambiguous-themes", "textual-fallback", "no-result"):
    assert kind in engine_js, f"presentation state {kind} must remain explicit in the search engine"

notice = "Ces rubriques regroupent des textes déjà indexés sous ce thème afin de faciliter leur consultation. Elles ne constituent pas de nouveaux thèmes et ne modifient pas les résultats de recherche."
assert 'id="themeRubricsPanel"' in html and 'id="themeRubricList"' in html, "rubric panel hooks are required"
assert notice in html, "rubric boundary explanation must remain visible"
assert 'src="js/theme-rubrics.js"' in html, "rubric presentation script must be loaded separately from the search engine"

print("Theme rubric pilot audit OK: additive navigation only; search, ranking, relations, co-occurrence and fallback remain independent")
