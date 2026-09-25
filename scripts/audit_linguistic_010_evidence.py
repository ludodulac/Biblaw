#!/usr/bin/env python3
import json,importlib.util,hashlib,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding='utf-8'))
cfg=load('data/linguistic/pilots/juste-config.json')
spec=importlib.util.spec_from_file_location('g',R/'scripts/build_linguistic_adjudication.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw,adj,inv=g.build(cfg)
rm={x['occurrenceId']:x for x in raw['occurrences']}; am={x['occurrenceId']:x for x in adj['analyses']}
print(json.dumps({'reconstruction':{'raw':raw['occurrenceCount'],'segmentation':adj['segmentationCounts'],'counts':adj['counts']}}))
# Counts + deterministic diverse samples by each generic frame.
byev=collections.defaultdict(list)
for a in adj['analyses']: byev[a['evidence']].append(a)
for ev,rows in sorted(byev.items()):
 if not ev.startswith('generic:'): continue
 rows=sorted(rows,key=lambda x:hashlib.sha256(x['occurrenceId'].encode()).hexdigest())
 print(json.dumps({'frame':ev,'count':len(rows),'sample':[{'id':a['occurrenceId'],'context':rm[a['occurrenceId']]['context'],'category':a['category']} for a in rows[:20]]},ensure_ascii=False))
# UNKNOWN families: deterministic probes selected by observable context.
unknown=[a for a in adj['analyses'] if a['category']=='UNKNOWN']
families={
 'start':lambda c:c.lstrip().casefold().startswith('juste'),
 'end':lambda c:re.search(r'juste\s*[.!?…»”]*\s*$',c,re.I)!=None,
 'copula':lambda c:re.search(r'\b(?:est|était|sera|soit|semble|paraît|devient|reste)\s+juste\b',c,re.I)!=None,
 'preposition':lambda c:re.search(r'\bjuste\s+(?:de|à|dans|sur|pour|avec|avant|après)\b',c,re.I)!=None,
 'coordination':lambda c:re.search(r'\bjuste\s+(?:et|ou|mais)\b',c,re.I)!=None,
 'negation':lambda c:re.search(r'\b(?:ne|n.|pas|jamais|plus)\b.{0,35}\bjuste\b',c,re.I)!=None,
 'determiner_after':lambda c:re.search(r'\bjuste\s+(?:un|une|le|la|les|des|du|ce|cette|ces)\b',c,re.I)!=None,
 'infinitive_like':lambda c:re.search(r'\bjuste\s+(?:être|avoir|faire|vivre|agir|comprendre|voir|dire|mettre|prendre|recevoir|survivre)\b',c,re.I)!=None,
}
for name,pred in families.items():
 rows=[a for a in unknown if pred(rm[a['occurrenceId']]['context'])]
 rows=sorted(rows,key=lambda x:hashlib.sha256(x['occurrenceId'].encode()).hexdigest())
 print(json.dumps({'unknownFamily':name,'count':len(rows),'sample':[{'id':a['occurrenceId'],'context':rm[a['occurrenceId']]['context']} for a in rows[:8]]},ensure_ascii=False))
