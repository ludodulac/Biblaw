#!/usr/bin/env python3
"""Strict final semantic gate for books 29-31."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / 'data/thematic-index/books'
CORPUS = ROOT / 'data/corpus/books'
EXPECTED = {29: range(191,218), 30: range(190,216), 31: range(180,206)}
GENERIC = ('Le psaume développe de façon répétée', 'Le thème «')
AXES = {
    29: "La religion du 21ème siècle présente la religion comme une manière de relier consciemment l’être humain à la vie, à la lumière et au monde divin selon l’enseignement propre au corpus. Le livre insiste sur une foi qui doit devenir connaissance, alliance, responsabilité et œuvre concrète, plutôt que rester une croyance abstraite ou un héritage extérieur.",
    30: "Développer la vision juste place le discernement au centre de la transformation humaine : voir justement suppose d’éduquer la pensée, les sentiments, l’intelligence et la conscience afin de reconnaître ce qui conduit vers la vie et ce qui en détourne. Le livre relie cette vision à l’équilibre, à la responsabilité et à l’incarnation concrète d’une œuvre conforme aux lois décrites dans le corpus.",
    31: "La nouvelle Pâque développe, dans le cadre doctrinal interne du corpus, l’idée d’un passage vers une nouvelle manière de vivre où le corps, l’âme, la pensée et la conscience doivent être réunis dans une alliance vivante. Le livre relie ce passage à la transformation de l’être, à la responsabilité collective et à une œuvre qui cherche à donner corps à la lumière sur la terre."
}


def finalize(book):
    path = BOOKS / f'book-{book:02d}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    analyses = data.get('psalmAnalyses', [])
    nums = [a['number'] for a in analyses]
    expected = list(EXPECTED[book])
    if nums != expected:
        raise ValueError(f'book {book}: expected {expected[0]}-{expected[-1]}, got {nums}')
    counts = Counter()
    for analysis in analyses:
        if analysis.get('semanticDepth') != 'deep-content-grounded':
            raise ValueError(f'book {book} psalm {analysis["number"]}: not deep')
        corpus = json.loads((CORPUS / f'book-{book:02d}' / f'psalm-{analysis["number"]:03d}.json').read_text(encoding='utf-8'))
        valid = {v['number'] for v in corpus.get('verses', [])}
        if not valid:
            raise ValueError(f'book {book} psalm {analysis["number"]}: empty corpus')
        for theme in analysis.get('themes', []):
            teaching = (theme.get('teaching') or '').strip()
            if not teaching or teaching.startswith(GENERIC):
                raise ValueError(f'book {book} psalm {analysis["number"]}: generic/empty teaching {theme.get("themeId")}')
            refs = theme.get('verseNumbers', [])
            if not refs or any(n not in valid for n in refs):
                raise ValueError(f'book {book} psalm {analysis["number"]}: invalid evidence {theme.get("themeId")} {refs}')
            counts[theme['themeId']] += 1
    data['bookSynthesis'] = {'centralAxis': AXES[book], 'majorThemes': [k for k, _ in counts.most_common(20)]}
    method = data.setdefault('method', {})
    method['semanticPass'] = 'deep-content-grounded-complete'
    method['deepPsalmCount'] = len(analyses)
    method['contentGrounding'] = 'complete'
    method['status'] = 'editorial-indexing-complete'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'book {book}: FINAL deep {len(analyses)}/{len(expected)}')


def main():
    for book in (29, 30, 31):
        finalize(book)


if __name__ == '__main__':
    main()
