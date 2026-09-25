#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
CANDIDATES=['marche','compte','livre','veille','aide','garde','reste','passe','juste','sens','tour']
TOKEN=re.compile(r"[^\W_]+(?:[’'][^\W_]+)*",re.UNICODE)
cat=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'))
out={w:[] for w in CANDIDATES}
for rel in cat['records']:
 p=R/rel
 if not p.exists() or not rel.startswith(('data/corpus/books/','data/prayers/','data/notes/')):continue
 o=json.loads(p.read_text(encoding='utf-8'))
 if o.get('recordType') in {'theme','book'} or (o.get('recordType')=='psalm' and not rel.startswith('data/corpus/books/')):continue
 fields=[]
 for k in ('title','text','summary'):
  if isinstance(o.get(k),str):fields.append((k,None,o[k]))
 for v in o.get('verses',[]) or []:
  if isinstance(v.get('text'),str):fields.append(('verses.text',v.get('number'),v['text']))
 for field,verse,text in fields:
  for m in TOKEN.finditer(text):
   w=m.group().casefold()
   if w in out:
    out[w].append({'recordId':o['id'],'field':field,'verse':verse,'surface':m.group(),'before':text[max(0,m.start()-70):m.start()],'after':text[m.end():min(len(text),m.end()+70)]})
for w,rows in out.items():
 print(json.dumps({'candidate':w,'count':len(rows),'samples':rows[:60]},ensure_ascii=False))
