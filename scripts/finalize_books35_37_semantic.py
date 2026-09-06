#!/usr/bin/env python3
"""Strict final semantic gate for books 35-37."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={35:range(206,232),36:range(208,234),37:range(244,270)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXES={
35:"Le chemin du bonheur présente le bonheur comme le fruit d’une manière juste de vivre, de penser et d’agir, fondée sur la conscience, la valeur accordée à la vie et la responsabilité envers ce que l’être humain porte et nourrit en lui. Dans le cadre doctrinal interne du corpus, le livre relie cet accomplissement à la maîtrise, à l’équilibre et à la capacité de conduire ses forces vers une œuvre constructive.",
36:"Être un socle pour le monde divin développe, selon le langage doctrinal propre au corpus, l’idée que l’être humain doit devenir un fondement stable capable d’accueillir, de préserver et de manifester une vie supérieure. Le livre associe cette stabilité à la conscience, à la fidélité, à l’engagement, au discernement et à une responsabilité concrète dans les pensées, les sentiments et les actes.",
37:"La maîtrise du serpent présente, dans la symbolique interne du corpus, le serpent comme une puissance qui doit être connue, éduquée et orientée plutôt que subie. Le livre relie cette maîtrise à la vigilance, à la pensée, à la volonté, à la conscience et à la transformation des forces intérieures afin qu’elles servent une œuvre créatrice plutôt qu’un mouvement de captation ou de destruction."
}
def finalize(book):
    path=BOOKS/f'book-{book:02d}.json'; data=json.loads(path.read_text(encoding='utf-8')); analyses=data.get('psalmAnalyses',[]); nums=[a['number'] for a in analyses]; expected=list(EXPECTED[book])
    if nums!=expected: raise ValueError(f'book {book}: expected {expected[0]}-{expected[-1]}, got {nums}')
    counts=Counter()
    for a in analyses:
        if a.get('semanticDepth')!='deep-content-grounded': raise ValueError(f'book {book} psalm {a["number"]}: not deep')
        corpus=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{a["number"]:03d}.json').read_text(encoding='utf-8')); valid={v['number'] for v in corpus.get('verses',[])}
        if not valid: raise ValueError(f'book {book} psalm {a["number"]}: empty corpus')
        for theme in a.get('themes',[]):
            teaching=(theme.get('teaching') or '').strip(); refs=theme.get('verseNumbers',[])
            if not teaching or teaching.startswith(GENERIC): raise ValueError(f'book {book} psalm {a["number"]}: generic/empty teaching {theme.get("themeId")}')
            if not refs or any(n not in valid for n in refs): raise ValueError(f'book {book} psalm {a["number"]}: invalid evidence {theme.get("themeId")} {refs}')
            counts[theme['themeId']]+=1
    data['bookSynthesis']={'centralAxis':AXES[book],'majorThemes':[k for k,_ in counts.most_common(20)]}; method=data.setdefault('method',{}); method['semanticPass']='deep-content-grounded-complete'; method['deepPsalmCount']=len(analyses); method['contentGrounding']='complete'; method['status']='editorial-indexing-complete'; path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'book {book}: FINAL deep {len(analyses)}/{len(expected)}')
def main():
    for book in (35,36,37): finalize(book)
if __name__=='__main__': main()
