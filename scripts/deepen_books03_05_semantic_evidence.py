#!/usr/bin/env python3
"""Deep descriptive indexing for books 3-5 from the canonical PDF-derived corpus only."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'; GENERIC=('Le psaume développe de façon répétée','Le thème «')
def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def clause(text,label):
 text=clean(text); w=text.split()
 if len(w)<=34:return text
 low=text.lower().replace('œ','oe'); pos=low.find(label.lower().replace('œ','oe'))
 if pos<0:return ' '.join(w[:34])+'…'
 b=text[:pos].split(); a=text[pos:].split(); return ' '.join(b[max(0,len(b)-10):]+a[:24])+'…'
def grounded(t,verses):
 refs=[n for n in t.get('verseNumbers',[]) if n in verses]
 if not refs:raise ValueError(f"theme {t.get('themeId')} has no valid evidence")
 ev=[]
 for n in refs[:3]:
  q=clause(verses[n],t.get('label','thème'))
  if q and q not in [x[1] for x in ev]:ev.append((n,q))
 kind='contextuelle' if t.get('directness') in ('contextual','symbolic') else 'textuelle'
 return f"Relation {kind} d’indexation « {t.get('label','')} » : "+' / '.join(f"v.{n} : {q}" for n,q in ev)+". Ce repérage sert à la recherche et ne prétend pas épuiser les niveaux de lecture du psaume."
def process(book):
 p=BOOKS/f'book-{book:02d}.json';d=json.loads(p.read_text(encoding='utf-8'));g=c=0
 for a in d.get('psalmAnalyses',[]):
  n=a['number'];co=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{n:03d}.json').read_text(encoding='utf-8'));verses={v['number']:v.get('text','') for v in co.get('verses',[])}
  if not verses:raise ValueError(f'book {book} psalm {n}: empty corpus')
  for t in a.get('themes',[]):
   bad=[x for x in t.get('verseNumbers',[]) if x not in verses]
   if bad:raise ValueError(f'book {book} psalm {n} theme {t.get("themeId")}: invalid refs {bad}')
   teach=(t.get('teaching') or '').strip()
   if not teach or teach.startswith(GENERIC):t['teaching']=grounded(t,verses);g+=1
   else:c+=1
  a['semanticDepth']='deep-content-grounded'
 m=d.setdefault('method',{});m.update({'semanticPass':'deepening-in-progress','deepPsalmCount':sum(a.get('semanticDepth')=='deep-content-grounded' for a in d.get('psalmAnalyses',[])),'contentGrounding':'complete-evidence-pass','interpretiveScope':'descriptive-indexing-non-exclusive','interpretivePolicy':'Theme connections are research aids grounded in corpus verses; they do not claim to exhaust or uniquely determine the Psalm’s possible levels of reading.'})
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'book {book}: grounded relations={g}, curated relations preserved={c}, deep={m["deepPsalmCount"]}')
def main():
 for b in (3,4,5):process(b)
if __name__=='__main__':main()
