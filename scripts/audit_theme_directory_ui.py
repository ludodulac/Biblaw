#!/usr/bin/env python3
"""Protect the single public A–Z theme index and its canonical, lazy-loaded data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "js" / "biblaw.js").read_text(encoding="utf-8")
css = (ROOT / "css" / "biblaw-light.css").read_text(encoding="utf-8")
build = (ROOT / "scripts" / "build_pages_site.py").read_text(encoding="utf-8")

# Exactly one visitor entry point: below « Toutes les notes », not in the header.
assert html.count('id="bibleThemesToggle"') == 1
assert html.count('id="bibleThemesLibrary"') == 1
assert html.index('id="notesLibraryToggle"') < html.index('id="bibleThemesToggle"')
assert 'id="bibleThemesToggle" class="popular-questions-toggle"' in html
assert 'aria-controls="bibleThemesLibrary">Index des thèmes</button>' in html
assert '<h2 id="bibleThemesTitle">Index des thèmes</h2>' in html
assert 'id="bibleThemesFilter"' in html
assert 'id="bibleThemesLetters"' in html
assert 'id="bibleThemePsalmList"' in html

# Obsolete, competing directory no longer exists in the public markup/runtime.
for old in ('id="indexToggle"', 'id="indexPanel"', 'id="indexBackdrop"',
            'id="bibleThemesShortcut"', 'id="themeFilter"', 'id="themeDirectory"'):
    assert old not in html, f"old directory still mounted: {old}"
for old in ('function openIndex()', 'function renderThemeDirectory()',
            "css/theme-index.css", '#indexPanel'):
    assert old not in js + html + css + build, f"unused directory code: {old}"

# One index and its Psalm reader; never invent or strip canonical associations.
assert "fetch('data/thematic-index/theme-directory-public.json')" in js
assert "fetch('data/thematic-index/theme-directory.json')" not in js
assert "state.bibleThemesSorted=[...state.themeDirectory]" in js
assert "const shown=query?state.bibleThemesSorted.filter" in js
assert "function renderBibleThemesAlphabetical()" in js
assert "function selectBibleTheme(theme)" in js
assert "thematicItems([theme],true)" in js, "All Psalms must ignore active main-search filters"
assert "importanceRank(a.thematic?.importance)-importanceRank(b.thematic?.importance)" in js
assert "$('bibleThemesToggle').onclick=openBibleThemes" in js
assert "if(state.corpusReady){" in js[js.index("function openBibleThemes()"):js.index("function backFromBibleThemes()")]
assert "void ensureCorpusReady().then(ok=>" in js[js.index("function openBibleThemes()"):js.index("function backFromBibleThemes()")]
assert "body.view-bible-themes #primarySearch" in css
assert "#bibleThemesToggle::before" in css
assert '"css/theme-index.css"' not in build

print("Single A–Z theme index OK: one button after Notes, full canonical Psalms, lazy loading and no duplicate UI")
