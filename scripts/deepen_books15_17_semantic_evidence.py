#!/usr/bin/env python3
"""Deep evidence/indexing pass for books 15-17 using only the canonical PDF-derived corpus.

This pass is intentionally descriptive: it grounds theme connections in exact verse references
without claiming an exhaustive or exclusive interpretation of the Psalms.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
GENERIC=('Le psaume développe de façon répétée','Le thème «')

def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def clause(text,label):
    text=clean(text); words=text.split()
    if len(words)<=34:return text
    needle=label.lower().replace('œ','oe'); low=text.lower().replace('œ','oe'); pos=low.find(needle)
    if pos<0:return ' '.join(words[:34])+'…'
    before=text[:pos].split(); after=text[pos:].split(); return ' '.join(before[max(0,len(before)-10):]+after[:24])+'…'
def grounded(theme,verses):
    refs=[n for n in theme.get('verseNumbers',[]) if n in verses]
    if not refs: raise ValueError(f"theme {theme.get('themeId')} has no valid evidence")
    chosen=[]
    for n in refs[:3]:
        q=clause(verses[n],theme.get('label','thème'))
        if q and q not in [x[1] for x in chosen]: chosen.append((n,q))
    evidence=' / '.join(f"v.{n} : {q}" for n,q in chosen)
    kind='contextuelle' if theme.get('directness') in ('contextual','symbolic') else 'textuelle'
    return f"Relation {kind} d’indexation « {theme.get('label','')} » : {evidence}. Ce repérage sert à la recherche et ne prétend pas épuiser les niveaux de lecture du psaume."
def ensure_book15_psalm75(data):
    if any(a.get('number')==75 for a in data.get('psalmAnalyses',[])): return
    corpus=json.loads((CORPUS/'book-15'/'psalm-075.json').read_text(encoding='utf-8'))
    valid={v['number'] for v in corpus.get('verses',[])}
    expected=set(range(15,28))
    if valid!=expected: raise ValueError(f'book 15 psalm 75: expected audited source verses 15-27, got {sorted(valid)}')
    themes=[
      ('oeuvre','Œuvre','central','direct',[17]),
      ('lumiere','Lumière','central','direct',[16,20,21,23,26]),
      ('monde-divin','Monde divin','important','direct',[19,20,27]),
      ('humilite','Humilité','important','direct',[24]),
      ('maitre','Maître','important','direct',[25]),
      ('imitation','Imitation','important','direct',[26]),
    ]
    data.setdefault('psalmAnalyses',[]).append({
      'recordId':'book-15-psalm-075','number':75,'title':corpus.get('title','On reconnaît un homme à ses œuvres'),
      'titleSignals':['œuvre','actes','modèles'],
      'themes':[{'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':refs,'teaching':''} for i,l,imp,d,refs in themes]
    })
    data['psalmAnalyses'].sort(key=lambda a:a['number'])
def process(book):
    path=BOOKS/f'book-{book:02d}.json'; data=json.loads(path.read_text(encoding='utf-8'))
    if book==15: ensure_book15_psalm75(data)
    grounded_count=curated_count=0
    for a in data.get('psalmAnalyses',[]):
        num=a['number']; cpath=CORPUS/f'book-{book:02d}'/f'psalm-{num:03d}.json'
        if not cpath.exists(): raise ValueError(f'book {book} psalm {num}: corpus file missing')
        corpus=json.loads(cpath.read_text(encoding='utf-8')); verses={v['number']:v.get('text','') for v in corpus.get('verses',[])}
        if not verses: raise ValueError(f'book {book} psalm {num}: empty corpus')
        for t in a.get('themes',[]):
            refs=t.get('verseNumbers',[]); bad=[n for n in refs if n not in verses]
            if bad: raise ValueError(f'book {book} psalm {num} theme {t.get("themeId")}: invalid refs {bad}')
            teaching=(t.get('teaching') or '').strip()
            if not teaching or teaching.startswith(GENERIC): t['teaching']=grounded(t,verses); grounded_count+=1
            else: curated_count+=1
        a['semanticDepth']='deep-content-grounded'
    m=data.setdefault('method',{}); m['semanticPass']='deepening-in-progress'; m['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in data.get('psalmAnalyses',[])); m['contentGrounding']='complete-evidence-pass'; m['interpretiveScope']='descriptive-indexing-non-exclusive'; m['interpretivePolicy']='Theme connections are research aids grounded in corpus verses; they do not claim to exhaust or uniquely determine the Psalm’s possible levels of reading.'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'book {book}: grounded relations={grounded_count}, curated relations preserved={curated_count}, deep={m["deepPsalmCount"]}')
def main():
    for b in (15,16,17): process(b)
if __name__=='__main__': main()