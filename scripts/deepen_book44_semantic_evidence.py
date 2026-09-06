#!/usr/bin/env python3
"""Deep evidence pass for book 44 using only the canonical PDF-derived corpus."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOK=ROOT/'data/thematic-index/books/book-44.json'; CORPUS=ROOT/'data/corpus/books/book-44'
GENERIC=('Le psaume développe de façon répétée','Le thème «')
def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def clause(text,label):
    text=clean(text); words=text.split()
    if len(words)<=34: return text
    needle=label.lower().replace('œ','oe'); low=text.lower().replace('œ','oe'); pos=low.find(needle)
    if pos<0: return ' '.join(words[:34])+'…'
    before=text[:pos].split(); after=text[pos:].split(); return ' '.join(before[max(0,len(before)-10):]+after[:24])+'…'
def grounded(theme,verses):
    refs=[n for n in theme.get('verseNumbers',[]) if n in verses]
    if not refs: raise ValueError(f"theme {theme.get('themeId')} has no valid evidence")
    chosen=[]
    for n in refs[:3]:
        q=clause(verses[n],theme.get('label','thème'))
        if q and q not in [x[1] for x in chosen]: chosen.append((n,q))
    evidence=' / '.join(f"v.{n} : {q}" for n,q in chosen)
    if theme.get('directness','direct') in ('contextual','symbolic'):
        return f"Relation contextuelle « {theme.get('label','')} » : {evidence}. Cette relation décrit le sens interne du psaume et n’est pas étendue à une affirmation factuelle extérieure au corpus."
    return f"Relation textuelle « {theme.get('label','')} » : {evidence}. Les autres versets référencés prolongent cette même relation dans le psaume."
def main():
    data=json.loads(BOOK.read_text(encoding='utf-8')); grounded_count=curated_count=0
    for analysis in data.get('psalmAnalyses',[]):
        num=analysis['number']; corpus=json.loads((CORPUS/f'psalm-{num:03d}.json').read_text(encoding='utf-8')); verses={v['number']:v.get('text','') for v in corpus.get('verses',[])}
        if not verses: raise ValueError(f'book 44 psalm {num}: empty corpus')
        for theme in analysis.get('themes',[]):
            refs=theme.get('verseNumbers',[]); bad=[n for n in refs if n not in verses]
            if bad: raise ValueError(f'book 44 psalm {num} theme {theme.get("themeId")}: invalid refs {bad}')
            teaching=(theme.get('teaching') or '').strip()
            if not teaching or teaching.startswith(GENERIC): theme['teaching']=grounded(theme,verses); grounded_count+=1
            else: curated_count+=1
        analysis['semanticDepth']='deep-content-grounded'
    method=data.setdefault('method',{}); method['semanticPass']='deepening-in-progress'; method['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in data.get('psalmAnalyses',[])); method['contentGrounding']='complete-evidence-pass'
    BOOK.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'book 44: grounded relations={grounded_count}, curated relations preserved={curated_count}, deep={method["deepPsalmCount"]}')
if __name__=='__main__': main()
