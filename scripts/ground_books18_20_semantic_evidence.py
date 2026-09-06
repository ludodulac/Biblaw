#!/usr/bin/env python3
"""Replace remaining prototype/generic teachings in books 18-20 with verse-grounded evidence.

This pass is deliberately conservative:
- it never overwrites analyses already marked deep-content-grounded;
- it uses only the canonical extracted psalm corpus derived from the authoritative PDF;
- it validates every referenced verse number against the current corpus;
- title-only signals are downgraded to contextual rather than presented as direct proof;
- it does not index prayer text.

The result is an intermediate content-grounded layer. It is not a substitute for the later
close semantic reading that earns semanticDepth=deep-content-grounded.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TI = ROOT / 'data' / 'thematic-index' / 'books'
CORPUS = ROOT / 'data' / 'corpus' / 'books'
BOOKS = (18, 19, 20)

GENERIC_PREFIXES = (
    'Le psaume développe explicitement le thème',
    'Le thème «',
)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def clean(text):
    return re.sub(r'\s+', ' ', (text or '')).strip()


def shorten(text, limit=245):
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ('. ', '; ', ': ', ', '):
        pos = cut.rfind(sep)
        if pos >= int(limit * 0.55):
            return cut[: pos + (1 if sep == '. ' else 0)].rstrip()
    return cut.rsplit(' ', 1)[0].rstrip() + '…'


def meaningful_tokens(label):
    words = re.findall(r"[a-zà-ÿœ]+", clean(label).lower())
    stop = {'dans', 'avec', 'pour', 'sans', 'entre', 'monde', 'des', 'les', 'une', 'un', 'de', 'du', 'la', 'le'}
    return [w for w in words if len(w) >= 4 and w not in stop]


def lexical_support(label, texts):
    hay = ' '.join(texts).lower().replace('œ', 'oe')
    tokens = [t.replace('œ', 'oe') for t in meaningful_tokens(label)]
    return any(t in hay for t in tokens) if tokens else False


def grounded_teaching(label, refs, verse_by_number, directness):
    texts = [clean(verse_by_number[n].get('text', '')) for n in refs if n in verse_by_number]
    texts = [t for t in texts if t]
    if not texts:
        return f"Le thème « {label} » est conservé comme signal contextuel, mais aucun verset d’appui exploitable n’est actuellement disponible dans le corpus structuré."

    evidence = []
    for t in texts:
        s = shorten(t)
        if s and s not in evidence:
            evidence.append(s)
        if len(evidence) == 2:
            break

    if directness == 'contextual':
        base = f"Le thème « {label} » est retenu ici comme contexte éditorial plutôt que comme preuve lexicale directe. Le passage d’ancrage indique : {evidence[0]}"
    else:
        base = f"Le psaume relie « {label} » au passage suivant : {evidence[0]}"
    if len(evidence) > 1:
        base += f" Un second appui précise : {evidence[1]}"
    return base


def upgrade_book(number):
    path = TI / f'book-{number:02d}.json'
    data = load(path)
    changed_analyses = 0
    changed_themes = 0

    for analysis in data.get('psalmAnalyses', []):
        if analysis.get('semanticDepth') == 'deep-content-grounded':
            continue

        num = analysis.get('number')
        corpus_path = CORPUS / f'book-{number:02d}' / f'psalm-{num:03d}.json'
        if not corpus_path.exists():
            continue
        psalm = load(corpus_path)
        verses = psalm.get('verses', [])
        verse_by_number = {v.get('number'): v for v in verses if isinstance(v.get('number'), int)}
        valid_numbers = set(verse_by_number)
        analysis_changed = False

        for theme in analysis.get('themes', []):
            refs = [n for n in theme.get('verseNumbers', []) if n in valid_numbers]
            if refs != theme.get('verseNumbers', []):
                theme['verseNumbers'] = refs
                analysis_changed = True

            if not refs and verses:
                refs = [verses[0]['number']]
                theme['verseNumbers'] = refs
                analysis_changed = True

            texts = [verse_by_number[n].get('text', '') for n in refs if n in verse_by_number]
            supported = lexical_support(theme.get('label', ''), texts)
            if not supported and theme.get('directness') == 'direct':
                theme['directness'] = 'contextual'
                analysis_changed = True

            old = clean(theme.get('teaching', ''))
            is_generic = (not old) or old.startswith(GENERIC_PREFIXES)
            if is_generic:
                theme['teaching'] = grounded_teaching(
                    theme.get('label', theme.get('themeId', 'thème')),
                    refs,
                    verse_by_number,
                    theme.get('directness', 'direct'),
                )
                analysis_changed = True
                changed_themes += 1

        if analysis_changed or analysis.get('semanticDepth') != 'content-grounded-extractive':
            analysis['semanticDepth'] = 'content-grounded-extractive'
            changed_analyses += 1

    method = data.setdefault('method', {})
    if number == 18:
        method['semanticPass'] = 'deepening-in-progress'
        method['contentGrounding'] = 'complete-for-non-deep-analyses'
    else:
        method['semanticPass'] = 'content-grounding-complete-deepening-pending'
        method['contentGrounding'] = 'verse-evidence-grounded'

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'book {number}: grounded analyses={changed_analyses}, generic teachings replaced={changed_themes}')


def main():
    for number in BOOKS:
        upgrade_book(number)


if __name__ == '__main__':
    main()
