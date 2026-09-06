#!/usr/bin/env python3
"""Strict final semantic gate for book 44."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOK=ROOT/'data/thematic-index/books/book-44.json'; CORPUS=ROOT/'data/corpus/books/book-44'; EXPECTED=list(range(260,286)); GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXIS="L’énergie de l’argent étudie, dans le cadre doctrinal interne du corpus, l’argent comme une force d’échange, d’orientation et de responsabilité qui révèle la qualité des intentions et des alliances humaines. Le livre relie cette énergie à la conscience, au discernement, à la maîtrise, à la création et à l’œuvre, en insistant sur la nécessité d’éduquer le rapport à la matière afin que les moyens disponibles servent la vie plutôt que des forces de captation ou de dépendance."
def main():
    data=json.loads(BOOK.read_text(encoding='utf-8')); analyses=data.get('psalmAnalyses',[]); nums=[a['number'] for a in analyses]
    if nums!=EXPECTED: raise ValueError(f'book 44: expected 260-285, got {nums}')
    counts=Counter()
    for a in analyses:
        if a.get('semanticDepth')!='deep-content-grounded': raise ValueError(f'book 44 psalm {a["number"]}: not deep')
        corpus=json.loads((CORPUS/f'psalm-{a["number"]:03d}.json').read_text(encoding='utf-8')); valid={v['number'] for v in corpus.get('verses',[])}
        if not valid: raise ValueError(f'book 44 psalm {a["number"]}: empty corpus')
        for theme in a.get('themes',[]):
            teaching=(theme.get('teaching') or '').strip(); refs=theme.get('verseNumbers',[])
            if not teaching or teaching.startswith(GENERIC): raise ValueError(f'book 44 psalm {a["number"]}: generic/empty teaching {theme.get("themeId")}')
            if not refs or any(n not in valid for n in refs): raise ValueError(f'book 44 psalm {a["number"]}: invalid evidence {theme.get("themeId")} {refs}')
            counts[theme['themeId']]+=1
    data['bookSynthesis']={'centralAxis':AXIS,'majorThemes':[k for k,_ in counts.most_common(20)]}; method=data.setdefault('method',{}); method['semanticPass']='deep-content-grounded-complete'; method['deepPsalmCount']=26; method['contentGrounding']='complete'; method['status']='editorial-indexing-complete'; BOOK.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print('book 44: FINAL deep 26/26')
if __name__=='__main__': main()
