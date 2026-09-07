#!/usr/bin/env python3
"""Fail deployment if the public UI drifts from the structured-corpus contract."""
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
assert 'recordPages' not in js and 'pdfPages' not in js, 'public search UI must not expose PDF page metadata'
assert '>Voir</button>' in js, 'result cards must expose a Voir button'
assert 'data-open=' in js, 'Voir button must open a structured record'
assert "bookMeta||'Corpus structuré'" in js, 'non-thematic result metadata must stay inside the structured corpus'
assert 'id="downloadRecord"' in html and 'Télécharger le texte' in html, 'download must remain inside the opened record dialog'
assert 'r.attachedPrayer?.text' in js, 'downloaded Psalm text must include the attached prayer when displayed'
assert 'data-open=' not in html, 'result buttons are generated from the structured corpus, not hard-coded in HTML'

print('Public UI contract OK: structured metadata, Voir action, complete download inside opened record')
