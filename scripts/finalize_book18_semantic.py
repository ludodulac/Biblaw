#!/usr/bin/env python3
"""Finalize Gabriel book 18 after the complete deep semantic pass.

Psalms 111-122 already contain prior editorial, content-specific analyses. This script does not
rewrite them: it promotes them only after checking that every cited verse exists and that no
prototype/generic teaching remains. Psalms 123-137 must already have been deepened by the two
close-reading scripts. The book synthesis is then replaced by a descriptive PDF-only synthesis.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data' / 'thematic-index' / 'books' / 'book-18.json'
CORPUS = ROOT / 'data' / 'corpus' / 'books' / 'book-18'

GENERIC = (
    'Le psaume développe explicitement le thème',
    'Le thème «',
)
EARLY = range(111, 123)
EXPECTED = set(range(111, 138))


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_analysis(analysis):
    num = analysis['number']
    psalm = load(CORPUS / f'psalm-{num:03d}.json')
    valid = {v['number'] for v in psalm.get('verses', [])}
    errors = []
    for theme in analysis.get('themes', []):
        teaching = (theme.get('teaching') or '').strip()
        if not teaching or teaching.startswith(GENERIC):
            errors.append(f'{num}:{theme.get("themeId")}:generic-teaching')
        bad = [v for v in theme.get('verseNumbers', []) if v not in valid]
        if bad:
            errors.append(f'{num}:{theme.get("themeId")}:invalid-verses={bad}')
        if not theme.get('verseNumbers'):
            errors.append(f'{num}:{theme.get("themeId")}:no-evidence')
    return errors


def main():
    data = load(PATH)
    analyses = {a['number']: a for a in data.get('psalmAnalyses', [])}
    missing = sorted(EXPECTED - set(analyses))
    if missing:
        raise SystemExit(f'Book 18 missing Psalm analyses: {missing}')

    errors = []
    for num in sorted(EXPECTED):
        errors.extend(validate_analysis(analyses[num]))
    if errors:
        raise SystemExit('Book 18 cannot be finalized:\n' + '\n'.join(errors))

    for num in EARLY:
        analyses[num]['semanticDepth'] = 'deep-content-grounded'

    not_deep = [n for n in sorted(EXPECTED) if analyses[n].get('semanticDepth') != 'deep-content-grounded']
    if not_deep:
        raise SystemExit(f'Book 18 still has non-deep analyses: {not_deep}')

    data['psalmAnalyses'] = [analyses[n] for n in sorted(EXPECTED)]
    data['method']['semanticPass'] = 'deep-content-grounded-complete'
    data['method']['deepPsalmCount'] = 27
    data['method']['contentGrounding'] = 'complete'
    data['bookSynthesis'] = {
        'centralAxis': (
            'Dans le livre 18, Gabriel relie la recherche de Lumière à la constitution concrète '
            'd’une vie capable de la porter. Les psaumes reviennent sur la qualité de l’eau et des '
            'relations, la pureté, le discernement des influences, la juste place du corps, la '
            'maîtrise de la vie quotidienne, la Tradition et l’Alliance comme structures, ainsi que '
            'sur la responsabilité individuelle et collective de transformer une compréhension en '
            'œuvre. Le livre oppose régulièrement l’abstraction, l’accumulation et l’appropriation à '
            'une pratique incarnée : préparer des conditions, éduquer le regard et l’intellect, '
            'ordonner les activités, purifier les relations, construire un corps et transmettre aux '
            'générations futures. Cette synthèse décrit les articulations internes du texte sans '
            'présenter ses affirmations doctrinales comme des faits extérieurs.'
        ),
        'majorThemes': [
            'eau','purete','lumiere','corps','maitrise','discernement','influences',
            'tradition','alliance','nation-essenienne','oeuvre','relations','responsabilite',
            'terre','sagesse','intelligence','destinee','generations-futures'
        ],
    }
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Book 18 finalized: 27/27 deep-content-grounded analyses')


if __name__ == '__main__':
    main()
