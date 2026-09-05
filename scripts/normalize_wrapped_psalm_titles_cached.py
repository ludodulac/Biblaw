#!/usr/bin/env python3
"""Repair wrapped Psalm titles with the same documentary rule as the legacy normalizer,
but cache every PDF page so each page is extracted at most once per run.

Optional environment variables BOOK_MIN and BOOK_MAX restrict work to a documentary range.
This script intentionally preserves the exact matching/repair semantics of
normalize_wrapped_psalm_titles.py; only I/O strategy and range scoping differ.
"""
from __future__ import annotations
import json, os, re, subprocess
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
BOOKS=ROOT/'data/corpus/books'
BOOK_MIN=int(os.environ.get('BOOK_MIN','1')); BOOK_MAX=int(os.environ.get('BOOK_MAX','999'))

def clean(value:str)->str:
 value=re.sub(r'\s+',' ',value).strip(); value=re.sub(r'^([A-ZÀ-ÖØ-Ý])\s+([a-zà-öø-ÿ])',r'\1\2',value); value=re.sub(r'\s+([,.;:!?])',r'\1',value); value=re.sub(r"([’'])\s+",r'\1',value); return value
@lru_cache(maxsize=None)
def pdf_page(page:int)->tuple[str,...]:
 raw=subprocess.run(['pdftotext','-layout','-f',str(page),'-l',str(page),str(PDF),'-'],check=True,capture_output=True,text=True).stdout
 return tuple(raw.splitlines())
def repair(record:dict)->bool:
 title=clean(record.get('title','')); pages=record.get('source',{}).get('pdfPages',[]); number=record.get('number')
 if not title or not pages or not isinstance(number,int): return False
 for page in pages[:2]:
  lines=pdf_page(page)
  for i,line in enumerate(lines):
   compact=re.sub(r'\s+',' ',line).strip(); m=re.match(rf'^{number}\s+(?![.])(.+)$',compact)
   if not m: continue
   first=clean(m.group(1)); common=max(8,min(len(title),len(first),24))
   if first[:common].casefold()!=title[:common].casefold(): continue
   continuation=[]
   for nxt in lines[i+1:i+5]:
    c=re.sub(r'\s+',' ',nxt).strip()
    if not c: continue
    if '| Évangile de l’Archange' in c: continue
    if re.match(r'^1[.]\s+',c): break
    if re.match(r'^\d{1,3}[.]\s+',c) or re.match(r'^\d{1,3}\s+(?![.])',c): break
    continuation.append(c)
    if len(continuation)>=2: break
   repaired=clean(' '.join([first,*continuation]))
   if repaired!=title and len(repaired.split())<=30:
    record['title']=repaired; record.setdefault('extraction',{})['wrappedTitleNormalized']=True; return True
 return False
changed=0; examined=0
for book_no in range(BOOK_MIN,BOOK_MAX+1):
 bdir=BOOKS/f'book-{book_no:02d}'
 if not bdir.exists(): continue
 for path in sorted(bdir.glob('psalm-*.json')):
  data=json.loads(path.read_text(encoding='utf-8')); examined+=1
  if repair(data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed+=1
print(f'Normalized {changed} wrapped Psalm titles across {examined} Psalms; cached PDF pages={pdf_page.cache_info().currsize}; range={BOOK_MIN}-{BOOK_MAX}')
