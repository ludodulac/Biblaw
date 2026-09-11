#!/usr/bin/env python3
"""Fail deployment if the public UI drifts from the structured-corpus contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')
js = (ROOT / 'js' / 'biblaw.js').read_text(encoding='utf-8')
theme_entry_js = (ROOT / 'js' / 'theme-entry.js').read_text(encoding='utf-8')
relations_js = (ROOT / 'js' / 'theme-relations.js').read_text(encoding='utf-8')
css = (ROOT / 'css' / 'biblaw.css').read_text(encoding='utf-8')
pages_build = (ROOT / 'scripts' / 'build_pages_site.py').read_text(encoding='utf-8')

for legacy in ('reader.html', 'app.js', 'styles.css'):
    assert not (ROOT / legacy).exists(), f'obsolete public prototype file still exists: {legacy}'

assert 'validation.html' not in html, 'editorial validation must not be linked from the public search page'
assert 'reader.html' not in html, 'obsolete PDF reader must not be linked from public search'
assert 'Voir dans le PDF' not in js, 'result cards must open structured text, not the PDF'
assert '.pdf#page=' not in js, 'public result cards must not contain direct PDF page links'
assert 'recordPages' not in js and 'pdfPages' not in js, 'public search UI must not expose PDF page metadata'
assert "thematic?'Voir le psaume source':'Voir'" in js, 'thematic result cards must expose the current source button label'
assert 'data-open=' in js, 'Voir button must open a structured record'
assert "bookMeta||'Corpus structuré'" in js, 'non-thematic result metadata must stay inside the structured corpus'
assert 'id="downloadRecord"' in html and 'Télécharger le texte' in html, 'download must remain inside the opened record dialog'
assert 'r.attachedPrayer?.text' in js, 'downloaded Psalm text must include the attached prayer when displayed'
assert 'data-open=' not in html, 'result buttons are generated from the structured corpus, not hard-coded in HTML'
assert 'grid-template-columns:minmax(0,1.5fr) minmax(14rem,.7fr)' in css, 'desktop filters must use the current two-column layout'
assert 'class="search-action-row"' in html, 'search field and submit action must stay grouped'
assert html.index('id="query"') < html.index('id="searchButton"') < html.index('class="filters"'), 'search action must be available before filters'
assert '@media(max-width:760px)' in css, 'mobile public layout must remain defined'
assert '.search-panel .search-field{border-color:rgba(255,255,255,.5);background:#f2f5f6}' in css, 'mobile search field must remain high contrast'
assert '#ambiguityPanel{order:5;margin-top:1rem}' in css and '.results-section{order:4}' in css, 'mobile transverse navigation must remain after results'
assert '.filters{display:flex;gap:.65rem;overflow-x:auto' in css, 'mobile filters must stay compact instead of forming a long vertical block'

cooccurrence_notice = 'Ces thèmes apparaissent dans les mêmes psaumes ; cette présence commune ne constitue pas en elle-même une relation thématique validée.'
assert cooccurrence_notice in html, 'cross-navigation must explicitly distinguish co-occurrence from validated thematic relations'
assert 'id="cooccurrenceNavigationNotice"' in html, 'cross-navigation notice must have a dedicated presentation hook'
assert html.index('id="cooccurrenceNavigationNotice"') < html.index('id="senseChoices"'), 'co-occurrence notice must render before cross-navigation choices'
assert 'state.runtime?.neighbors?.[theme.id]' in js, 'cross-navigation must remain fed by runtime co-occurrence neighbors'
assert "ambiguous?'Correspondances multiples':'Navigation transversale'" in js, 'cross-navigation and multiple correspondences must remain distinct modes'
assert "detail.kind !== 'canonical-theme'" in theme_entry_js, 'co-occurrence notice must stay hidden outside canonical theme entries'
assert 'cooccurrenceNotice.hidden = true' in theme_entry_js and 'cooccurrenceNotice.hidden = false' in theme_entry_js, 'co-occurrence notice visibility must follow canonical theme presentation state'
assert 'id="validatedRelationsPanel"' in html and 'id="ambiguityPanel"' in html, 'validated relations and co-occurrence navigation must remain separate panels'
assert 'theme-relations-public.json' in relations_js, 'validated relations panel must keep its dedicated public relation source'

for asset in (
    'css/theme-entry.css',
    'js/theme-entry.js',
    'js/theme-rubrics.js',
    'data/thematic-index/theme-rubrics-public.json',
):
    assert f'"{asset}"' in pages_build, f'Pages production allow-list must include {asset}'

print('Public UI contract OK: structured metadata, direct mobile search flow, compact filters, post-result transverse navigation and complete Pages assets')
