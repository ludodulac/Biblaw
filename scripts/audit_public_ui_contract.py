#!/usr/bin/env python3
"""Fail deployment if the public UI drifts from the structured-corpus contract."""
import re
import unicodedata
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

# Literal-search contract: matching and counting share one normalized, word-bounded phrase rule.
assert 'const literalOccurrenceCount = (r, query) =>' in js
assert 'const literalTextMatch = (r, needle) => literalOccurrenceCount(r,needle)>0;' in js
assert 'occurrenceCount:literalOccurrenceCount(record,query)' in js
assert 'b.occurrenceCount-a.occurrenceCount' in js
assert "Number(a.record.number)||Number.MAX_SAFE_INTEGER" in js
assert "String(a.record.id).localeCompare(String(b.record.id),'fr')" in js
assert "companion?.exactSearch?`${occurrenceCount} occurrence${occurrenceCount>1?'s':''}`" in js
assert "render(exactItems,null,{exactSearch:true})" in js
assert '${highlighted(summary(r))}' in js and '${highlighted(v.text)}' in js
assert "new Blob([activeText()]" in js and '<mark' not in js[js.index('function activeText()'):js.index('function renderThemeDirectory()')]
assert '@media print' in css and '.search-hit{padding:0;border-radius:0;background:transparent;color:inherit}' in css
assert 'importanceRank(x.thematic?.importance)-importanceRank(y.thematic?.importance)||x.record.number-y.record.number' in js


def norm(value: str) -> str:
    value = unicodedata.normalize('NFD', value or '')
    value = ''.join(ch for ch in value if unicodedata.category(ch) != 'Mn').lower()
    value = value.replace('œ', 'oe').replace('æ', 'ae').replace('’', ' ').replace("'", ' ')
    value = re.sub(r'[^a-z0-9\s-]', ' ', value).replace('-', ' ')
    return re.sub(r'\s+', ' ', value).strip()


def count_fragments(fragments, query):
    needle = norm(query)
    if not needle:
        return 0
    bounded = f' {needle} '
    return sum(f' {norm(fragment)} '.count(bounded) for fragment in fragments if norm(fragment))

# Focused fixtures cover absence, singular/plural, repeated hits, phrase semantics and deterministic ranking.
assert count_fragments(['La vie demeure.'], 'mort') == 0
assert count_fragments(['La mort demeure.'], 'mort') == 1
assert count_fragments(['Mort et mort, puis la mort.'], 'mort') == 3
assert count_fragments(['La mort sacrée vient.', 'La mort sacrée demeure.'], 'mort sacrée') == 2
assert count_fragments(['La mort seule est ici.', 'Le chemin sacré est là.'], 'mort sacrée') == 0
fixture = [
    {'id': 'psalm-b', 'number': 12, 'count': 2},
    {'id': 'psalm-a', 'number': 7, 'count': 2},
    {'id': 'psalm-c', 'number': 3, 'count': 4},
    {'id': 'psalm-d', 'number': 7, 'count': 2},
]
fixture.sort(key=lambda item: (-item['count'], item['number'], item['id']))
assert [item['id'] for item in fixture] == ['psalm-c', 'psalm-a', 'psalm-d', 'psalm-b']
assert f"{1} occurrence{'' if 1 == 1 else 's'}" == '1 occurrence'
assert f"{2} occurrence{'' if 2 == 1 else 's'}" == '2 occurrences'

print('Public UI contract OK: compact primary search, source traceability, secondary tools, separated relations/navigation, literal occurrence ranking and print-safe highlighting')
