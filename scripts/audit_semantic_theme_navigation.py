#!/usr/bin/env python3
"""Audit explicit search vocabulary without touching validated theme/Psalm relations."""
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
runtime=json.loads((ROOT/"data/thematic-index/theme-search-runtime.json").read_text(encoding="utf-8"))
data=json.loads((ROOT/"data/thematic-index/theme-semantic-navigation-public.json").read_text(encoding="utf-8"))

def norm(text):
    s=unicodedata.normalize("NFD",str(text))
    s="".join(c for c in s if unicodedata.category(c)!="Mn").lower()
    s=s.replace("œ","oe").replace("æ","ae").replace("’"," ").replace("'"," ")
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9\s-]"," ",s).replace("-"," ")).strip()

canonical={theme_id for alias in runtime["aliases"].values() for theme_id in alias["themeIds"]}
assert len(canonical)==runtime["themeCount"]==1267
assert data["schemaVersion"]==1
assert data["purpose"]=="explicit-related-theme-discovery-not-canonical-synonymy"
assert data["source"]=="canonical-indexed-theme-names"
assert data["canonicalThemeCount"]==1267
assert data["semanticMerging"] is False and data["createsPsalmRelations"] is False
assert data["reviewedThemeIds"]==sorted(canonical), "Not all 1267 names audited"
assert len(data["groups"])>=125
assert len(data["queries"])>=450

rebuilt={}
for group in data["groups"]:
    ids=group["themeIds"]
    assert ids and len(ids)==len(set(ids)) and set(ids)<=canonical
    assert len(group["terms"])==len(set(group["terms"]))
    for query in group["terms"]:
        assert query==norm(query) and query not in runtime["aliases"]
        assert query not in rebuilt,"A semantic query must have one explicitly curated target group"
        rebuilt[query]={"themeIds":ids,"category":"related-navigation-only"}
assert rebuilt==data["queries"],"Browser lookup must exactly project approved groups"
for query,item in data["queries"].items():
    assert set(item["themeIds"])<=canonical
    assert not any(key in item for key in ("recordIds","verseNumbers","psalmIds","importance","score"))
    assert len(item["themeIds"])<=8, "Related-term proposals must stay navigable"
expected={"blanche-neige","fees","haricot-magique","baguette-magique","licorne"}
for query in ("conte","contes","contes de fees","legende","merveilleux"):
    assert set(data["queries"][query]["themeIds"])==expected
for query in ("assemblee","argent","dieu","blanche neige"):
    assert query not in data["queries"], "Canonical/existing search contract must win"
print("SEMANTIC_NAVIGATION_PASS canonical=1267 reviewed=1267 curated_groups="+
      str(len(data["groups"]))+" search_phrases="+str(len(data["queries"]))+
      " no new theme/Psalm relations; canonical aliases unchanged")
