#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/'data/linguistic/pilots/porte-occurrences.json').read_text(encoding='utf-8'))
adj=json.loads((ROOT/'data/linguistic/pilots/porte.json').read_text(encoding='utf-8'))
am={x['occurrenceId']:x for x in adj['analyses']}
rows=[dict(o,**am[o['occurrenceId']]) for o in raw['occurrences']]
def local(o):
 i=min(o['startOffset'],90); return o['context'][:i],o['context'][i+len(o['surfaceForm']):]
hy=[]; clitic=[]; compound=[]
for o in rows:
 b,a=local(o)
 if re.search(r'[-‑–—]$',b) or re.match(r'^[-‑–—]',a):
  hy.append(o)
  if re.match(r'^[-‑–—](?:le|la|les|lui|leur|en|y)\b',a,re.I): clitic.append(o)
  else: compound.append(o)
# High-certainty contradiction sentinels discovered independently from the generating heuristic.
expected={
 'occ-4210e70fcbe4e1d65b894181':('VERB_PORTER','NOUN','ouvrir une telle porte'),
 'occ-f5043c17057a47db9e0b5eed':('NOUN','VERB_PORTER','qui ... porte des mondes'),
 'occ-a18d1242395f001f1889f138':('NOUN','VERB_PORTER',"l’homme porte de vrai"),
 'occ-75cd0c3a829334cbf3d2165c':('NOUN','VERB_PORTER',"l’homme porte des vertus"),
 'occ-8a55dd99471758e92a13b630':('NOUN','VERB_PORTER',"l’homme porte de vrai")
}
byid={x['occurrenceId']:x for x in rows}
for oid,(current,correct,_) in expected.items():
 assert byid[oid]['category']==current
# Reproducible diversified control sample: stable hash ordering, category quotas,
# then greedy preference for unseen record type/book/evidence before filling quota.
def sample(category,n=24):
 pool=[x for x in rows if x['category']==category]
 pool.sort(key=lambda x:x['occurrenceId'])
 out=[]; seen=set()
 for x in pool:
  key=(x['recordType'],x.get('bookNumber'),x.get('field'),x.get('evidence'))
  if key not in seen: out.append(x); seen.add(key)
  if len(out)==n:return out
 for x in pool:
  if x['occurrenceId'] not in {y['occurrenceId'] for y in out}: out.append(x)
  if len(out)==n:return out
 return out
samples={k:sample(k) for k in ('NOUN','VERB_PORTER','UNKNOWN')}
report={
 'schemaVersion':1,
 'purpose':'adversarial-quality-audit-selection-and-sentinels',
 'sourceHead':'64a7a1306abe73885195f95974812d2a0100c27e',
 'sampleMethod':'stable occurrenceId ordering within each category; greedily cover distinct recordType/bookNumber/field/evidence, then fill to 24',
 'sampleSize':sum(map(len,samples.values())),
 'sampleCounts':{k:len(v) for k,v in samples.items()},
 'hyphenAdjacentCount':len(hy),'cliticVerbCount':len(clitic),'compoundSegmentationCount':len(compound),
 'compoundCurrentCategories':{k:sum(1 for x in compound if x['category']==k) for k in ('NOUN','VERB_PORTER','UNKNOWN')},
 'knownHighCertaintyClassificationErrors':[{'occurrenceId':oid,'context':byid[oid]['context'],'current':cur,'proposed':cor,'reason':reason} for oid,(cur,cor,reason) in expected.items()],
 'sample':{k:[{'occurrenceId':x['occurrenceId'],'recordId':x['recordId'],'recordType':x['recordType'],'bookNumber':x.get('bookNumber'),'psalmNumber':x.get('psalmNumber'),'verseNumber':x.get('verseNumber'),'context':x['context'],'currentCategory':x['category'],'evidence':x['evidence']} for x in v] for k,v in samples.items()}
}
out=ROOT/'data/linguistic/audits/porte-003-audit.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Audit 003 selection PASS: sample={report['sampleSize']}; compound-segmentation={len(compound)}; high-certainty-classification-errors={len(expected)}")
