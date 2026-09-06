#!/usr/bin/env python3
"""Strict final semantic gate for books 32-34."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={32:range(183,208),33:range(218,244),34:range(216,244)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXES={
32:"La Nouvelle Alliance présente l’alliance comme une relation vivante qui doit unir l’être humain, la conscience et l’œuvre à une intelligence supérieure selon l’enseignement propre au corpus. Le livre insiste sur la fidélité, la responsabilité et l’incarnation concrète de cette relation dans la vie, afin que l’engagement ne demeure pas une idée abstraite mais devienne une manière d’être et d’agir.",
33:"Les secrets du Feu décrivent, dans le langage symbolique et doctrinal interne du corpus, le feu comme une puissance de transformation qui révèle, anime et éprouve la vie intérieure. Le livre relie cette force à la conscience, à la volonté, à la maîtrise et à l’œuvre, en soulignant que toute puissance doit être éduquée et orientée pour devenir créatrice plutôt que destructrice.",
34:"L’envoûtement et le désenvoûtement étudie, dans la cosmologie propre au corpus, les influences qui peuvent capter la pensée, les sentiments, la volonté et la conscience. Le livre place le discernement, l’éveil, la maîtrise et l’éducation intérieure au cœur du désenvoûtement, afin que l’être humain retrouve une relation consciente à la vie et puisse agir avec davantage de liberté et de responsabilité."
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
    for book in (32,33,34): finalize(book)
if __name__=='__main__': main()
