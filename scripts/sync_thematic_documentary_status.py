#!/usr/bin/env python3
"""Synchronize thematic completion status with documentary corpus integrity.

A book cannot be declared thematically complete while its PDF-derived corpus has a missing
Psalm or malformed main verse sequence. Audited Psalms whose printed numbering intentionally
continues above 1 are valid when `sourceNumberingPreserved` is explicit and their sequence is
contiguous from the printed first verse.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/'data/corpus/books'; THEMATIC=ROOT/'data/thematic-index/books'
changed=0
for tpath in sorted(THEMATIC.glob('book-[0-9][0-9].json')):
 data=json.loads(tpath.read_text(encoding='utf-8')); n=data.get('book',{}).get('number')
 if not isinstance(n,int): continue
 bpath=CORPUS/f'book-{n:02d}'/'book.json'
 if not bpath.exists(): continue
 meta=json.loads(bpath.read_text(encoding='utf-8')); ids=meta.get('psalmIds',[])
 nums=sorted(int(x.rsplit('-',1)[1]) for x in ids)
 exp=meta.get('numbering',{}).get('expectedStart'); nxt=meta.get('numbering',{}).get('nextExpected')
 missing=[]
 if isinstance(exp,int) and isinstance(nxt,int): missing=[x for x in range(exp,nxt) if x not in nums]
 malformed=[]
 for num in nums:
  p=CORPUS/f'book-{n:02d}'/f'psalm-{num:03d}.json'
  if not p.exists(): malformed.append(num); continue
  ps=json.loads(p.read_text(encoding='utf-8')); vs=[v.get('number') for v in ps.get('verses',[]) if isinstance(v.get('number'),int)]
  source_preserved=bool(ps.get('extraction',{}).get('sourceNumberingPreserved'))
  first=min(vs) if vs else 1
  expected_vs=list(range(first,max(vs)+1)) if vs else []
  if not vs or vs!=expected_vs or (first!=1 and not source_preserved): malformed.append(num)
 issues=[]
 if missing: issues.append(f"missing documentary Psalm(s): {missing}")
 if malformed: issues.append(f"malformed main verse sequence in Psalm(s): {malformed}")
 method=data.setdefault('method',{}); old=(method.get('status'),method.get('completenessIssue'))
 if issues:
  method['status']='editorial-indexing-in-progress'; method['completenessIssue']='; '.join(issues)+'. Repair from the authoritative PDF before declaring this book complete.'
 else:
  if method.get('status') in ('editorial-indexing-in-progress','editorial-indexing-complete'):
   method['status']='editorial-indexing-complete'; method.pop('completenessIssue',None)
 new=(method.get('status'),method.get('completenessIssue'))
 if new!=old:
  tpath.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed+=1
print(f'Synchronized documentary status for thematic books; changed={changed}')
