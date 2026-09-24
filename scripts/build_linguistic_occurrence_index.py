#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CATALOG=ROOT/'data/catalog.json'; CANON='data/corpus/books/'
def norm(s):
 return unicodedata.normalize('NFC',s).casefold()
def searchable(rel,o):
 t=o.get('recordType'); return t not in {'theme','book'} and not (t=='psalm' and not rel.startswith(CANON))
def fields(o):
 if o.get('recordType')=='psalm':
  if isinstance(o.get('title'),str): yield 'title',None,o['title']
  for v in o.get('verses',[]):
   if isinstance(v.get('text'),str): yield 'verses.text',v.get('number'),v['text']
 else:
  for k in ('title','text','summary'):
   if isinstance(o.get(k),str): yield k,None,o[k]
def meta(o):
 return o.get('book',{}).get('number',o.get('bookNumber')), o.get('number') if o.get('recordType')=='psalm' else None
def oid(rid,field,verse,start,end):
 loc=f'{field}[{verse}]' if verse is not None else field; raw=f'{rid}|{loc}|{start}|{end}'; return 'occ-'+hashlib.sha256(raw.encode()).hexdigest()[:24]
def occurrences(form):
 target=norm(form); out=[]; token=re.compile(r"[^\W_]+(?:[’'][^\W_]+)*",re.UNICODE); catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
 for rel in catalog['records']:
  p=ROOT/rel
  if not p.exists(): raise SystemExit(f'missing catalog record: {rel}')
  o=json.loads(p.read_text(encoding='utf-8'))
  if not searchable(rel,o): continue
  bn,pn=meta(o)
  for field,verse,text in fields(o):
   for m in token.finditer(text):
    if norm(m.group())!=target: continue
    s,e=m.span(); out.append({'occurrenceId':oid(o['id'],field,verse,s,e),'recordId':o['id'],'recordType':o.get('recordType'),'bookNumber':bn,'psalmNumber':pn,'verseNumber':verse,'field':field,'surfaceForm':m.group(),'normalizedForm':target,'startOffset':s,'endOffset':e,'context':text[max(0,s-90):min(len(text),e+90)]})
 return out
def payload(form):
 x=occurrences(form); return {'schemaVersion':1,'purpose':'linguistic-occurrence-index-pilot-slice','source':'canonical-catalog-records','normalizedForm':norm(form),'occurrenceIdConvention':'occ- + first 24 hex chars of SHA-256(recordId|field[verse]|startOffset|endOffset); [verse] omitted for non-verse fields','offsetUnit':'Python Unicode code-point index into original field text','exactPhraseCompatibility':'This derived token index is additive. Existing literal multi-word search continues to operate on original corpus text and is not replaced by token lookup.','occurrenceCount':len(x),'occurrences':x}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--form',default='porte'); ap.add_argument('--output'); a=ap.parse_args(); p=payload(a.form); data=json.dumps(p,ensure_ascii=False,indent=2)+'\n'
 if a.output:
  q=ROOT/a.output; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(data,encoding='utf-8')
 print(data,end='')
if __name__=='__main__': main()
