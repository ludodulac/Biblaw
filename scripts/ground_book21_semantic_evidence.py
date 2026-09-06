#!/usr/bin/env python3
"""Ground residual prototype relations in Michael book 21 against canonical PDF-derived psalm verses."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-21.json'
CORPUS=ROOT/'data/corpus/books/book-21'
LEGACY=('Le psaume développe de façon répétée le thème', 'Le psaume développe explicitement le thème')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def short(s,n=235):
 s=clean(s)
 if len(s)<=n:return s
 c=s[:n]
 p=max(c.rfind('. '),c.rfind('; '),c.rfind(', '))
 return (c[:p+1] if p>130 else c.rsplit(' ',1)[0]+'…').strip()
def main():
 d=load(PATH); changed=0
 for a in d.get('psalmAnalyses',[]):
  n=a['number']; ps=load(CORPUS/f'psalm-{n:03d}.json'); by={v['number']:v for v in ps.get('verses',[])}; valid=set(by)
  for t in a.get('themes',[]):
   refs=[x for x in t.get('verseNumbers',[]) if x in valid]
   if refs!=t.get('verseNumbers',[]): t['verseNumbers']=refs
   old=clean(t.get('teaching',''))
   if old.startswith(LEGACY):
    if not refs: raise SystemExit(f'Book 21 Psalm {n} theme {t.get("themeId")}: no valid evidence')
    label=t.get('label',t.get('themeId','thème')); ev=short(by[refs[0]].get('text',''))
    t['teaching']=f'Le passage d’appui retenu pour « {label} » indique : {ev} Cette relation secondaire est conservée comme ancrage textuel du psaume.'
    changed+=1
 d.setdefault('method',{})['residualGrounding']='canonical-verse-evidence'
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Book 21 residual prototype teachings grounded={changed}')
if __name__=='__main__': main()
