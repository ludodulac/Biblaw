#!/usr/bin/env python3
import json,re,collections,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C=['marche','sens','garde','aide','reste','passe','livre','veille','tour']
TOKEN=re.compile(r"[^\W_]+(?:[’'][^\W_]+)*",re.UNICODE)
cat=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'))
out={w:[] for w in C}
for rel in cat['records']:
 p=R/rel
 if not p.exists() or not rel.startswith(('data/corpus/books/','data/prayers/','data/notes/')): continue
 o=json.loads(p.read_text(encoding='utf-8'))
 if o.get('type') in {'theme','book'}: continue
 fields=[]
 for k in ('title','text','summary'):
  if isinstance(o.get(k),str): fields.append((k,o[k]))
 for v in o.get('verses',[]) or []:
  if isinstance(v.get('text'),str): fields.append(('verses.text',v['text']))
 for field,text in fields:
  for m in TOKEN.finditer(text):
   w=m.group().casefold()
   if w in out:
    ctx=text[max(0,m.start()-90):min(len(text),m.end()+90)]
    out[w].append({'surface':m.group(),'context':ctx})
for w,rows in out.items():
 rows=sorted(rows,key=lambda x:hashlib.sha256(x['context'].encode()).hexdigest())
 print(json.dumps({'candidate':w,'count':len(rows),'samples':rows[:35]},ensure_ascii=False))
