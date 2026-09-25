#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]; targets={'juste','compte','marche','garde'}
TOKEN=re.compile(r"[^\W_]+(?:[’'][^\W_]+)*",re.UNICODE)
cat=json.loads((R/'data/catalog.json').read_text())
rows={x:[] for x in targets}
for rel in cat['records']:
 p=R/rel
 if not p.exists() or not rel.startswith(('data/corpus/books/','data/prayers/','data/notes/')):continue
 o=json.loads(p.read_text())
 if o.get('type') in {'theme','book'}:continue
 fields=[(k,None,o[k]) for k in ('title','text','summary') if isinstance(o.get(k),str)]
 fields += [('verses.text',v.get('number'),v['text']) for v in (o.get('verses') or []) if isinstance(v.get('text'),str)]
 for field,verse,text in fields:
  ms=list(TOKEN.finditer(text))
  for i,m in enumerate(ms):
   w=m.group().casefold()
   if w in targets:
    prev=[x.group().casefold() for x in ms[max(0,i-3):i]]
    nxt=[x.group().casefold() for x in ms[i+1:i+4]]
    rows[w].append({'id':o['id'],'field':field,'verse':verse,'surface':m.group(),'prev':prev,'next':nxt,'context':text[max(0,m.start()-100):min(len(text),m.end()+100)]})
for w,rr in rows.items():
 n=len(rr); idx=sorted(set([round(i*(n-1)/39) for i in range(40)])) if n else []
 print(json.dumps({'candidate':w,'count':n,'distributed':[rr[i] for i in idx]},ensure_ascii=False))
