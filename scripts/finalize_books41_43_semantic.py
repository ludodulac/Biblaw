#!/usr/bin/env python3
"""Strict final semantic gate for books 41-43."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={41:range(270,296),42:range(270,296),43:range(258,284)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXES={
41:"La responsabilité d’un parent présente la transmission comme une responsabilité qui dépasse la seule protection matérielle et engage l’exemple, l’éducation, la conscience et la qualité des forces offertes à l’enfant. Dans le cadre doctrinal interne du corpus, le livre relie cette responsabilité à la maîtrise de soi, à la fidélité à la vie et à la capacité de préparer un environnement intérieur et extérieur favorable à l’éveil et à l’autonomie.",
42:"L’état ultime de la paix présente la paix non comme une simple absence de conflit, mais comme un état d’équilibre et d’accord intérieur qui se construit par la conscience, le discernement, la maîtrise et une relation juste avec la vie. Selon l’enseignement propre au corpus, cette paix demande d’ordonner les pensées, les sentiments et les actes afin de ne plus nourrir les forces de division et de devenir un lieu d’unité vivante.",
43:"La guérison par les vertus développe, dans le langage doctrinal interne du corpus, l’idée que la guérison est liée à la qualité des forces que l’être humain cultive et laisse agir dans sa vie. Le livre relie les vertus à la conscience, à l’équilibre, au cœur, à la pensée et à la responsabilité, en présentant leur pratique comme un moyen de transformer les causes intérieures de désordre et de soutenir une relation plus juste avec la vie."
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
    for book in (41,42,43): finalize(book)
if __name__=='__main__': main()
