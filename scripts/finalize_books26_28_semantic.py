#!/usr/bin/env python3
"""Strict final semantic gate for books 26-28."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / 'data/thematic-index/books'
CORPUS = ROOT / 'data/corpus/books'
EXPECTED = {26: range(164,190), 27: range(154,180), 28: range(156,182)}
GENERIC = ('Le psaume développe de façon répétée', 'Le thème «')
AXES = {
    26: "L’énergie créatrice relie la qualité intérieure de l’être à la manière dont les forces de vie, la pensée, les sentiments et la volonté deviennent créatrices. Le livre insiste sur l’éducation, le discernement et la maîtrise nécessaires pour orienter ces forces vers une œuvre consciente, harmonieuse et fidèle à l’intelligence supérieure selon l’enseignement propre au corpus.",
    27: "Le Serpent de la Sagesse présente la sagesse comme une intelligence vivante qui doit unir vision, conscience, pensée, corps et action. Le livre décrit, dans la cosmologie propre au corpus, un travail de transformation et de maîtrise par lequel l’être humain apprend à discerner les influences, à s’accorder aux lois de la vie et à donner une forme juste à son œuvre sur la terre.",
    28: "Le vrai corps du Christ développe l’idée, interne au corpus, d’un corps spirituel et collectif qui ne se réduit pas au corps physique : il se construit par l’alliance, la conscience, la pensée, la parole et les actes. Le livre relie cette incarnation à une œuvre concrète sur la terre, où la lumière et l’intelligence doivent prendre corps dans une communauté de vie et de responsabilité."
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
    for book in (26, 27, 28):
        finalize(book)


if __name__ == '__main__':
    main()
