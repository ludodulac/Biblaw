#!/usr/bin/env python3
"""Fail deployment if obsolete PDF-reader navigation returns to the public UI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'index.html').read_text(encoding='utf-8')
js = (ROOT / 'js' / 'biblaw.js').read_text(encoding='utf-8')

for legacy in ('reader.html', 'app.js', 'styles.css'):
    assert not (ROOT / legacy).exists(), f'obsolete public prototype file still exists: {legacy}'

assert 'validation.html' not in html, 'editorial validation must not be linked from the public search page'
assert 'reader.html' not in html, 'obsolete PDF reader must not be linked from public search'
assert 'Voir dans le PDF' not in js, 'result cards must open structured text, not the PDF'
assert '.pdf#page=' not in js, 'public result cards must not contain direct PDF page links'
assert '>Voir</button>' in js, 'result cards must expose a Voir button'
assert 'data-open=' in js, 'Voir button must open a structured record'
assert 'id="downloadRecord"' in html and 'Télécharger le texte' in html, 'download must remain inside the opened record dialog'
assert 'data-open=' not in html, 'result buttons are generated from the structured corpus, not hard-coded in HTML'

print('Public UI contract OK: search-only navigation, structured Voir action, download inside opened record')
