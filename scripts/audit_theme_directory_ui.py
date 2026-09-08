#!/usr/bin/env python3
"""Guard the large public theme directory against eager rendering and payload regressions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
css = (ROOT / "css" / "biblaw.css").read_text(encoding="utf-8")
index_css_path = ROOT / "css" / "theme-index.css"
assert index_css_path.exists(), "theme directory must keep its dedicated presentation stylesheet"
index_css = index_css_path.read_text(encoding="utf-8")

assert 'id="themeFilter"' in html, "theme index must expose a dedicated filter"
assert 'placeholder="Ex. corps d’eau, alliance, lumière"' in html
assert 'href="css/theme-index.css"' in html
assert "fetch('data/thematic-index/theme-directory-public.json')" in js, "public UI must load the compact theme projection"
assert "fetch('data/thematic-index/theme-directory.json')" not in js, "public UI must not download the editorial theme directory"
assert 'function renderThemeDirectory()' in js
assert 'function openIndex()' in js
assert "$('themeFilter').oninput=renderThemeDirectory" in js
assert "$('indexPanel').hidden?openIndex():closeIndex()" in js
assert "renderThemeDirectory();\n    $('indexPanel').hidden=false" in js, "directory must render on opening"
assert "themes(); search();" not in js, "theme directory must not eagerly render at corpus load"
assert "$('themeDirectory').innerHTML=visible.length?" in js
assert "norm(t.label).includes(needle)||norm(t.id).includes(needle)" in js
assert '.index-filter{' in css and '.index-filter .search-field{' in css
assert '.theme-row{' in index_css and '.theme-row:hover' in index_css
assert '.theme-row strong{' in index_css and '.theme-row small{' in index_css

print('Theme directory UI OK: compact payload, lazy rendering, local filtering and readable rows are protected')
