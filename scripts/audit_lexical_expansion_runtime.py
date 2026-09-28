#!/usr/bin/env python3
"""Validate the production single-word lexical-expansion sidecar and UI contract."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "data" / "lexical-expansion-runtime.json"
EXPECTED_MORPHALOU_SHA256 = "4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333"
EXPECTED_028_AGGREGATION_SHA256 = "a25019ae5f1b0d6c8a26ff390505d554a05264d69939411affa1b0beb2594be1"
EXPECTED_019_SHA256 = "097e7c4b79ce1c913774e57da59330fd1fb5a617b32b249296f90ac63e8fab8e"
EXPECTED_MACHINE_SAFE = 193248
EXPECTED_PARTICIPIAL_PAIRS = 402

runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
assert runtime["v"] == 1
assert runtime["m"] == EXPECTED_MORPHALOU_SHA256
assert runtime["s"] == EXPECTED_028_AGGREGATION_SHA256
assert runtime["i"] == EXPECTED_019_SHA256
assert runtime["n"] == EXPECTED_MACHINE_SAFE
assert runtime["pf"] == EXPECTED_PARTICIPIAL_PAIRS
assert RUNTIME.stat().st_size < 200_000

groups = runtime["g"]
assert groups and all(isinstance(group, list) and len(group) >= 2 for group in groups)
forms = [form for group in groups for form in group]
assert all(form and " " not in form for form in forms)
assert len(forms) == len(set(forms)), "one browser form must map to one expansion group"

# Regression sentinels from the post-scale human audit and the known no-op MWE case.
for blocked in ("empli", "dote", "travers"):
    assert blocked not in forms, blocked

# Positive sentinel: an ordinary safe inflection family remains useful.
prendre_group = next((group for group in groups if "prendre" in group), None)
assert prendre_group is not None and "prendront" in prendre_group

html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
assert 'id="exactExpansionOption"' in html
assert 'id="includeWordForms"' in html
assert 'Occurrences exactes' in html
assert 'Inclure les formes du même mot' in html
for technical in ("Morphalou", "MACHINE_SAFE", "predictedLemma", "predictedBiblawLexicalPOS"):
    assert technical not in html
assert "data/lexical-expansion-runtime.json" in js
assert "function singleWordQueryKey" in js
assert "function expansionFormsFor" in js
assert "function mergeExpansionMatches" in js
assert "const exactItems=matches(query);" in js
assert "mergeExpansionMatches(exactItems,query);" in js
assert "checkbox.disabled=!key||!expansions.length;" in js
assert "checkbox.checked=false" in js
assert "state.mode!=='exact'" in js

print(
    f"Lexical expansion product contract OK: {len(groups)} groups, {len(forms)} safe single-word anchors, "
    f"participle filter active, exact phrases remain non-expandable, {RUNTIME.stat().st_size} bytes"
)