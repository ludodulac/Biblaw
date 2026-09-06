#!/usr/bin/env python3
"""Strict final indexing/evidence gate for books 15-17."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={15:range(75,102),16:range(78,104),17:range(105,131)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')

def finalize(book):
    path=BOOKS/f'book-{book:02d}.json'; data=json.loads(path.read_text(encoding='utf-8')); analyses=data.get('psalmAnalyses',[]); nums=[a['number'] for a in analyses]; expected=list(EXPECTED[book])
    if nums!=expected: raise ValueError(f'book {book}: expected {expected[0]}-{expected[-1]}, got {nums}')
    counts=Counter(); labels={}
    for a in analyses:
        if a.get('semanticDepth')!='deep-content-grounded': raise ValueError(f'book {book} psalm {a["number"]}: not deep')
        corpus=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{a["number"]:03d}.json').read_text(encoding='utf-8')); valid={v['number'] for v in corpus.get('verses',[])}
        if not valid: raise ValueError(f'book {book} psalm {a["number"]}: empty corpus')
        for t in a.get('themes',[]):
            teaching=(t.get('teaching') or '').strip(); refs=t.get('verseNumbers',[])
            if not teaching or teaching.startswith(GENERIC): raise ValueError(f'book {book} psalm {a["number"]}: generic/empty teaching {t.get("themeId")}')
            if not refs or any(n not in valid for n in refs): raise ValueError(f'book {book} psalm {a["number"]}: invalid evidence {t.get("themeId")} {refs}')
            counts[t['themeId']]+=1; labels.setdefault(t['themeId'],t.get('label',t['themeId']))
    major=[k for k,_ in counts.most_common(20)]; names=[labels[k] for k in major[:10]]
    data['bookSynthesis']={
      'centralAxis':f"Synthèse d’indexation non exclusive : les relations indexées de ce livre font ressortir notamment {', '.join(names)}. Cette synthèse sert au repérage et à la recherche dans le corpus ; elle ne prétend pas épuiser ni fixer les différents niveaux de lecture possibles.",
      'majorThemes':major,
      'scope':'descriptive-indexing-non-exclusive'
    }
    m=data.setdefault('method',{}); m['semanticPass']='deep-content-grounded-complete'; m['deepPsalmCount']=len(analyses); m['contentGrounding']='complete'; m['status']='editorial-indexing-complete'; m['interpretiveScope']='descriptive-indexing-non-exclusive'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'book {book}: FINAL deep {len(analyses)}/{len(expected)}')
def main():
    for b in (15,16,17): finalize(b)
if __name__=='__main__': main()