#!/usr/bin/env python3
"""Guard the large public theme directory against eager rendering regressions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
css = (ROOT / "css" / "biblaw.css").read_text(encoding="utf-8")

assert 'id="themeFilter"' in html, "theme index must expose a dedicated filter"
assert 'placeholder="Ex. corps d’eau, alliance, lumière"' in html
assert 'function renderThemeDirectory()' in js
assert 'function openIndex()' in js
assert "$('themeFilter').oninput=renderThemeDirectory" in js
assert "$('indexPanel').hidden?openIndex():closeIndex()" in js
assert "renderThemeDirectory();\n    $('indexPanel').hidden=false" in js, "directory must render on opening"
assert "themes(); search();" not in js, "theme directory must not eagerly render at corpus load"
assert "$('themeDirectory').innerHTML=visible.length?" in js
assert "norm(t.label).includes(needle)||norm(t.id).includes(needle)" in js
assert '.index-filter{' in css and '.index-filter .search-field{' in css

print('Theme directory UI OK: lazy rendering and local theme filter are protected')
