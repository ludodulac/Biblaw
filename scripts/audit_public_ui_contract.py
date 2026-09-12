#!/usr/bin/env python3
"""Fail deployment if the public UI drifts from the structured-corpus contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')
js = (ROOT / 'js' / 'biblaw.js').read_text(encoding='utf-8')
theme_entry_js = (ROOT / 'js' / 'theme-entry.js').read_text(encoding='utf-8')
relations_js = (ROOT / 'js' / 'theme-relations.js').read_text(encoding='utf-8')
css = (ROOT / 'css' / 'biblaw.css').read_text(encoding='utf-8')

for legacy in ('reader.html', 'app.js', 'styles.css'):
    assert not (ROOT / legacy).exists(), f'obsolete public prototype file still exists: {legacy}'

assert 'validation.html' not in html
assert 'reader.html' not in html
assert 'Voir dans le PDF' not in js and '.pdf#page=' not in js
assert 'recordPages' not in js and 'pdfPages' not in js
assert "thematic||themeMatches?'Voir le psaume source':'Voir'" in js
assert 'data-open=' in js and 'data-open=' not in html
assert "bookMeta||'Corpus structuré'" in js
assert 'id="downloadRecord"' in html and 'Télécharger le texte' in html
assert 'r.attachedPrayer?.text' in js
assert 'id="query2"' in html and 'Thème 2 facultatif' in html
assert 'id="secondaryTools"' in html and 'Autres recherches et filtres' in html
assert html.index('id="results"') < html.index('id="secondaryTools"')
assert 'id="transversePanel"' in html and html.index('id="results"') < html.index('id="transversePanel"')
assert 'Ces thèmes apparaissent dans les mêmes psaumes ; cette présence commune ne constitue pas en elle-même une relation thématique validée.' in html
assert 'state.runtime?.neighbors?.[theme.id]' in js
assert 'id="validatedRelationsPanel"' in html and 'id="ambiguityPanel"' in html
assert 'theme-relations-public.json' in relations_js
assert "norm($('query2')?.value)" in relations_js
assert "detail.kind === 'dual-theme'" in theme_entry_js
assert '@media(max-width:760px)' in css and '.search-submit{grid-column:1/-1' in css
assert '.compact-related{display:flex' in css and '.inline-themes{display:inline-flex;flex-wrap:wrap' in css
assert 'theme-rubrics.js' in html and 'theme-rubrics-panel' in html

print('Public UI contract OK: compact primary search, source traceability, secondary tools, separated relations and navigation')
