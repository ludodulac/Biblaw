#!/usr/bin/env python3
import json,importlib.util,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ENGINE_SHA='ca063c03d3eedb7f5dc976c51dc4ad992ea437ce'
assert hashlib.sha1((f"blob {len((R/'scripts/build_linguistic_adjudication.py').read_bytes())}\0").encode()+ (R/'scripts/build_linguistic_adjudication.py').read_bytes()).hexdigest()==ENGINE_SHA
spec=importlib.util.spec_from_file_location('m',R/'scripts/build_linguistic_adjudication.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cfg=json.loads((R/'data/linguistic/pilots/garde-config.json').read_text()); raw,adj,inv=m.build(cfg)
assert raw['occurrenceCount']==99
assert adj['segmentationCounts']=={'AUTONOMOUS':76,'VERB_CLITIC':16,'COMPOUND_ELEMENT':7}
assert adj['counts']=={'NOUN_GARDE':19,'VERB_GARDER':50,'OTHER':7,'UNKNOWN':23,'AMBIGUOUS':0}
assert inv['count']==7
for rel,obj in [('data/linguistic/pilots/garde-occurrences.json',raw),('data/linguistic/pilots/garde.json',adj),('data/linguistic/pilots/garde-compounds.json',inv)]:
 assert json.loads((R/rel).read_text())==obj, rel
by={x['occurrenceId']:x for x in adj['analyses']}
for goldfile in ['data/linguistic/gold/garde-gold.json','data/linguistic/gold/garde-adversarial-gold.json']:
 gold=json.loads((R/goldfile).read_text()); z={'correct':0,'unknown':0,'ambiguous':0,'contradictory':0}
 for g in gold['entries']:
  a=by[g['occurrenceId']]
  if a['category']==g['category']: z['correct']+=1
  elif a['status']=='UNKNOWN': z['unknown']+=1
  elif a['status']=='AMBIGUOUS': z['ambiguous']+=1
  else: z['contradictory']+=1
 assert z['contradictory']==0,(goldfile,z)
 print(goldfile,z)
assert len(cfg['rules'])==5
txt=(R/'scripts/build_linguistic_adjudication.py').read_text().casefold()
assert 'garde' not in txt
assert all('occ-' not in json.dumps(x) for x in cfg['rules'])
print(json.dumps({'raw':99,'segmentation':adj['segmentationCounts'],'counts':adj['counts'],'configRuleCount':5,'engineChanged':False,'wordSpecificCodeBranches':0,'configOnlySufficient':True}))
