#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
H='-‑–—'
P=r'(?:je|tu|il|elle|on|nous|vous|ils|elles)'
direct=re.compile(rf"(?iu)\b([^\W_]+)([{H}])({P})\b")
euph=re.compile(rf"(?iu)\b([^\W_]+)([{H}])t\2({P})\b")
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
hits=[]
for rel in catalog['records']:
 p=ROOT/rel
 if not p.exists() or not rel.startswith(('data/corpus/books/','data/prayers/','data/notes/')):continue
 o=json.loads(p.read_text(encoding='utf-8'))
 if o.get('type') in {'theme','book'}:continue
 fields=[]
 for k in ('title','text','summary'):
  if isinstance(o.get(k),str):fields.append((k,None,o[k]))
 for v in o.get('verses',[]) or []:
  if isinstance(v.get('text'),str):fields.append(('verses.text',v.get('number'),v['text']))
 for field,verse,text in fields:
  spans=set()
  for kind,rx in [('DIRECT',direct),('EPHONIC_T',euph)]:
   for m in rx.finditer(text):
    key=(m.start(),m.end())
    if key in spans:continue
    spans.add(key);hits.append({'kind':kind,'surface':m.group(0),'stem':m.group(1),'pronoun':m.group(3),'recordId':o['id'],'field':field,'verseNumber':verse,'context':text[max(0,m.start()-60):min(len(text),m.end()+60)]})
families=collections.Counter((x['kind'],x['surface'].casefold()) for x in hits)
summary={
 'totalCandidates':len(hits),
 'byKind':dict(collections.Counter(x['kind'] for x in hits)),
 'byPronoun':dict(collections.Counter((x['kind']+':'+x['pronoun'].casefold()) for x in hits)),
 'byHyphen':dict(collections.Counter(next((c for c in x['surface'] if c in H),'?') for x in hits)),
 'uniqueFamilies':len(families),
 'directConservativeSupported':sum(x['kind']=='DIRECT' and x['pronoun'].casefold() in {'je','tu','il','elle','on','ils','elles'} for x in hits),
 'directNousVousAmbiguous':sum(x['kind']=='DIRECT' and x['pronoun'].casefold() in {'nous','vous'} for x in hits),
 'euphonicFamilies':sorted([{'surfaceFolded':k[1],'count':n} for k,n in families.items() if k[0]=='EPHONIC_T'],key=lambda x:x['surfaceFolded']),
 'examples':hits[:40]
}
print(json.dumps(summary,ensure_ascii=False))
