#!/usr/bin/env python3
"""Protect the documentary two-theme intersection from semantic drift."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / 'js' / 'biblaw.js').read_text(encoding='utf-8')
html = (ROOT / 'index.html').read_text(encoding='utf-8')

start = js.index('function intersectionItems(')
end = js.index('\n\n  function hideAmbiguity', start)
intersection = js[start:end]

assert 'occurrencesA' in intersection and 'occurrencesB' in intersection
assert 'occurrencesB.get(recordId)' in intersection, 'intersection must be exact on recordId'
assert 'state.runtime' not in intersection and 'neighbors' not in intersection and 'cooccurrence' not in intersection.lower()
assert 'themeMatches:[{theme:themeA,thematic:thematicA},{theme:themeB,thematic:thematicB}]' in intersection
assert 'score+' not in intersection and 'current.score' not in intersection
assert 'resolvedA.length!==1||resolvedB.length!==1' in js
assert 'showDualAmbiguity' in js and 'Résolvez chaque thème avant l’intersection' in js
assert 'dualThemeReasons' in js
assert "thematic.teaching||''" in js
assert 'Teaching combiné' not in js and 'combinedTeaching' not in js
assert 'relatedThemes(r,matchedThemes)' in js
assert 'Autres thèmes dans ce psaume :' in js
assert 'textualPsalmMatches(query)' in js and 'textualFallback:true' in js
assert 'parsePsalmNumberQuery(query)' in js
assert 'selectedTypes()' in js and "$('archangelFilter').value" in js
assert 'theme-relations-public.json' not in intersection
assert 'theme-rubrics.js' in html and 'data-open' not in html

print('Two-theme search audit OK: exact recordId intersection, ambiguity gate, separate importance/teaching/passages, no semantic relation creation')
