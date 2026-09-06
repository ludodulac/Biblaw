#!/usr/bin/env python3
"""Strict final semantic gate for books 38-40."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={38:range(244,270),39:range(232,258),40:range(234,260)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXES={
38:"Les 22 étapes de l’Initiation présente l’initiation comme un chemin d’éducation et de transformation qui engage progressivement la pensée, les sentiments, la volonté, la conscience et la manière de vivre. Dans le cadre doctrinal interne du corpus, le livre insiste sur la nécessité de franchir les étapes avec fidélité, discernement et maîtrise afin que l’enseignement devienne une réalité vécue et une œuvre consciente.",
39:"Les vertus du coeur place la qualité intérieure du cœur au centre de la relation à soi, aux autres et au monde vivant. Selon l’enseignement propre au corpus, le livre relie les vertus à l’attention, à la bonté, à la conscience, à la sagesse et à la responsabilité, en invitant l’être humain à cultiver ce qu’il veut réellement faire vivre et rayonner autour de lui.",
40:"L’Ange de la conscience développe la conscience comme une présence intérieure à éveiller, à éduquer et à rendre active dans les pensées, les sentiments et les actes. Dans la cosmologie interne du corpus, le livre associe cet éveil au discernement, à la mémoire, à la responsabilité et à l’alliance avec une intelligence supérieure, afin que l’être humain ne vive plus mécaniquement mais choisisse et agisse avec clarté."
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
    for book in (38,39,40): finalize(book)
if __name__=='__main__': main()
