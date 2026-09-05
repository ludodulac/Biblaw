#!/usr/bin/env python3
"""Synchronize thematic completion status with documentary corpus integrity.

A book cannot be declared thematically complete while its PDF-derived corpus has a missing
Psalm or a malformed main verse sequence. This guard is deterministic and introduces no
semantic interpretation.
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
  if not vs or vs != list(range(1,max(vs)+1)): malformed.append(num)
 issues=[]
 if missing: issues.append(f"missing documentary Psalm(s): {missing}")
 if malformed: issues.append(f"malformed main verse sequence in Psalm(s): {malformed}")
 method=data.setdefault('method',{})
 old=(method.get('status'),method.get('completenessIssue'))
 if issues:
  method['status']='editorial-indexing-in-progress'; method['completenessIssue']='; '.join(issues)+'. Repair from the authoritative PDF before declaring this book complete.'
 else:
  # Only promote corpus-scale generated books; preserve special non-completion statuses if explicitly semantic/editorial.
  if method.get('status') in ('editorial-indexing-in-progress','editorial-indexing-complete'):
   method['status']='editorial-indexing-complete'; method.pop('completenessIssue',None)
 new=(method.get('status'),method.get('completenessIssue'))
 if new!=old:
  tpath.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed+=1
print(f'Synchronized documentary status for thematic books; changed={changed}')
