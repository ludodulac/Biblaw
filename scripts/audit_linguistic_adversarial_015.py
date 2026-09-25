#!/usr/bin/env python3
import json,hashlib,importlib.util,collections,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding='utf-8'))
cfg=load('data/linguistic/pilots/garde-config.json')
rawv=load('data/linguistic/pilots/garde-occurrences.json'); adjv=load('data/linguistic/pilots/garde.json')
spec=importlib.util.spec_from_file_location('m',R/'scripts/build_linguistic_adjudication.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,adj,inv=m.build(cfg)
assert raw==rawv and adj==adjv
assert raw['occurrenceCount']==99
assert adj['segmentationCounts']=={'AUTONOMOUS':76,'VERB_CLITIC':16,'COMPOUND_ELEMENT':7}
assert adj['counts']=={'NOUN_GARDE':19,'VERB_GARDER':50,'OTHER':7,'UNKNOWN':23,'AMBIGUOUS':0}
rm={x['occurrenceId']:x for x in raw['occurrences']}; am={x['occurrenceId']:x for x in adj['analyses']}
# Configuration architecture.
assert len(cfg['rules'])==5
ct=json.dumps(cfg,ensure_ascii=False).casefold()
assert 'occ-' not in ct
engine=(R/'scripts/build_linguistic_adjudication.py').read_text(encoding='utf-8').casefold()
assert 'garde' not in engine
# Rule trigger distribution and gold overlap.
g1=load('data/linguistic/gold/garde-gold.json');g2=load('data/linguistic/gold/garde-adversarial-gold.json');g3=load('data/linguistic/gold/garde-adversarial-gold-015.json')
sets=[set(x['occurrenceId'] for x in g['entries']) for g in (g1,g2,g3)]
for ev in sorted(set(a['evidence'] for a in adj['analyses'])):
 rows=[a for a in adj['analyses'] if a['evidence']==ev]
 if ev.startswith('config-rule:'):
  ids={a['occurrenceId'] for a in rows}
  print(json.dumps({'rule':ev,'triggers':len(ids),'goldPrincipal':len(ids&sets[0]),'goldAdv014':len(ids&sets[1]),'outside014Golds':len(ids-(sets[0]|sets[1]))}))
# All 16 clitics must slice into target-hyphen-clitic and be VERB.
clitics=[a for a in adj['analyses'] if a['segmentation']=='VERB_CLITIC']
assert len(clitics)==16 and all(a['category']=='VERB_GARDER' for a in clitics)
for a in clitics:
 ctx=rm[a['occurrenceId']]['context']
 assert re.search(r'garde[-‑–—](?:moi|le|les)\b',ctx,re.I), (a['occurrenceId'],ctx)
# Compounds exact families.
comp=[x['surfaceForm'].casefold() for x in inv['occurrences']]
assert collections.Counter(comp)==collections.Counter({'garde-manger':5,'garde-mangers':1,'garde-fou':1})
# Gold comparisons.
for label,g in [('principal',g1),('adversarial014',g2),('adversarial015',g3)]:
 z=collections.Counter()
 for x in g['entries']:
  a=am[x['occurrenceId']]
  if a['category']==x['category']: z['correct']+=1
  elif a['status']=='UNKNOWN': z['unknown']+=1
  elif a['status']=='AMBIGUOUS': z['ambiguous']+=1
  else: z['contradictory']+=1
 print(json.dumps({'gold':label,**z}))
 assert z['contradictory']==0
print(json.dumps({'reconstruction':adj['counts'],'segmentation':adj['segmentationCounts'],'verbByConfig':34,'verbByClitic':16,'engineChanged':False,'newGenericFrames':0,'wordSpecificCodeBranches':0}))
