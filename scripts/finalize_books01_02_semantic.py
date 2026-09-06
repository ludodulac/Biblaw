#!/usr/bin/env python3
"""Strict final indexing/evidence gate for books 1-2."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BOOKS=ROOT/'data/thematic-index/books';CORPUS=ROOT/'data/corpus/books';EXPECTED={1:range(1,23),2:range(1,25)};GENERIC=('Le psaume développe de façon répétée','Le thème «')
def finalize(book):
 p=BOOKS/f'book-{book:02d}.json';d=json.loads(p.read_text(encoding='utf-8'));aa=d.get('psalmAnalyses',[]);nums=[a['number'] for a in aa];ex=list(EXPECTED[book])
 if nums!=ex:raise ValueError(f'book {book}: expected {ex[0]}-{ex[-1]}, got {nums}')
 counts=Counter();labels={}
 for a in aa:
  if a.get('semanticDepth')!='deep-content-grounded':raise ValueError(f'book {book} psalm {a["number"]}: not deep')
  co=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{a["number"]:03d}.json').read_text(encoding='utf-8'));valid={v['number'] for v in co.get('verses',[])}
  for t in a.get('themes',[]):
   teach=(t.get('teaching') or '').strip();refs=t.get('verseNumbers',[])
   if not teach or teach.startswith(GENERIC):raise ValueError(f'book {book} psalm {a["number"]}: generic/empty {t.get("themeId")}')
   if not refs or any(n not in valid for n in refs):raise ValueError(f'book {book} psalm {a["number"]}: invalid evidence {t.get("themeId")} {refs}')
   counts[t['themeId']]+=1;labels.setdefault(t['themeId'],t.get('label',t['themeId']))
 major=[k for k,_ in counts.most_common(20)];names=[labels[k] for k in major[:10]]
 d['bookSynthesis']={'centralAxis':f"Synthèse d’indexation non exclusive : les relations indexées de ce livre font ressortir notamment {', '.join(names)}. Cette synthèse sert au repérage et à la recherche dans le corpus ; elle ne prétend pas épuiser ni fixer les différents niveaux de lecture possibles.",'majorThemes':major,'scope':'descriptive-indexing-non-exclusive'}
 m=d.setdefault('method',{});m.update({'semanticPass':'deep-content-grounded-complete','deepPsalmCount':len(aa),'contentGrounding':'complete','status':'editorial-indexing-complete','interpretiveScope':'descriptive-indexing-non-exclusive'})
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'book {book}: FINAL deep {len(aa)}/{len(ex)}')
def main():
 for b in (1,2):finalize(b)
if __name__=='__main__':main()
