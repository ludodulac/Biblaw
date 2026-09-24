#!/usr/bin/env python3
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
texts=[]
def searchable(rel,o): return rel.startswith(('data/corpus/books/','data/prayers/','data/notes/')) and o.get('type') not in {'theme','book'}
def fields(o):
 for k in ('title','text','summary'):
  if isinstance(o.get(k),str): yield k,None,o[k]
 for v in o.get('verses',[]) or []:
  if isinstance(v.get('text'),str): yield 'verses.text',v.get('number'),v['text']
for rel in catalog['records']:
 p=ROOT/rel
 if not p.exists(): continue
 o=json.loads(p.read_text(encoding='utf-8'))
 if not searchable(rel,o): continue
 for field,verse,text in fields(o): texts.append((o['id'],field,verse,text))
patterns={
 'HYPHEN_INVERSION':r'(?i)\bsuis[-‑–—]je\b',
 'SOLID_INVERSION':r'(?i)\bsuisje\b',
 'HYPHEN_JE_SUIS':r'(?i)\bje[-‑–—]suis\b',
 'SOLID_JE_SUIS':r'(?i)\bjesuis\b',
 'SPACED_JE_SUIS':r'(?i)\bje\s+suis\b',
 'OTHER_HYPHEN_AFTER':r'(?i)\bsuis[-‑–—][^\W_]+',
 'HYPHEN_BEFORE':r'(?i)[^\W_]+[-‑–—]suis\b'
}
for name,pat in patterns.items():
 hits=[]
 for rid,field,verse,text in texts:
  for m in re.finditer(pat,text): hits.append({'recordId':rid,'field':field,'verseNumber':verse,'surface':m.group(),'context':text[max(0,m.start()-70):min(len(text),m.end()+70)]})
 print(json.dumps({'family':name,'count':len(hits),'variants':sorted({h['surface'] for h in hits}),'examples':hits[:20]},ensure_ascii=False))
