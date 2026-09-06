#!/usr/bin/env python3
"""Deep evidence pass for books 23-25, using only the canonical PDF-derived corpus.

Already curated relations are preserved, while every residual prototype relation in those same
analyses is grounded from its exact referenced verses. No prayers or outside sources are used.
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
        if q and q not in chosen: chosen.append((n,q))
    evidence=' / '.join(f"v.{n} : {q}" for n,q in chosen)
    if theme.get('directness','direct') in ('contextual','symbolic'):
        return f"Relation contextuelle « {theme.get('label','')} » : {evidence}. Cette relation décrit le sens interne du psaume et n’est pas étendue à une affirmation factuelle extérieure au corpus."
    return f"Relation textuelle « {theme.get('label','')} » : {evidence}. Les autres versets référencés prolongent cette même relation dans le psaume."
def process(book):
    path=BOOKS/f'book-{book:02d}.json'; d=json.loads(path.read_text(encoding='utf-8')); grounded_count=0; curated_count=0
    for a in d.get('psalmAnalyses',[]):
        num=a['number']; c=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{num:03d}.json').read_text(encoding='utf-8')); verses={v['number']:v.get('text','') for v in c.get('verses',[])}
        if not verses: raise ValueError(f'book {book} psalm {num}: empty corpus')
        for t in a.get('themes',[]):
            bad=[n for n in t.get('verseNumbers',[]) if n not in verses]
            if bad: raise ValueError(f'book {book} psalm {num} theme {t.get("themeId")}: invalid refs {bad}')
            teach=(t.get('teaching') or '').strip()
            if not teach or teach.startswith(GENERIC): t['teaching']=grounded(t,verses); grounded_count+=1
            else: curated_count+=1
        a['semanticDepth']='deep-content-grounded'
    m=d.setdefault('method',{}); m['semanticPass']='deepening-in-progress'; m['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d.get('psalmAnalyses',[])); m['contentGrounding']='complete-evidence-pass'
    if book==23: m['numberingNote']='Psalm 128 uses audited corrected numbering 1-34, mapped from printed source numbering 49-82 by a verified offset of 48; the question boundary remains embedded after verse 22 before verse 23.'
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'book {book}: grounded relations={grounded_count}, curated relations preserved={curated_count}, deep={m["deepPsalmCount"]}')
def main():
    for b in (23,24,25): process(b)
if __name__=='__main__': main()
