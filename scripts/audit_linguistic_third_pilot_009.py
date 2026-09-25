#!/usr/bin/env python3
import json,importlib.util,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gen',R/'scripts/build_linguistic_adjudication.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
cfg=load('data/linguistic/pilots/juste-config.json');raw,adj,inv=gen.build(cfg)
assert raw==load('data/linguistic/pilots/juste-occurrences.json')
assert adj==load('data/linguistic/pilots/juste.json')
assert inv==load('data/linguistic/pilots/juste-compounds.json')
assert raw['occurrenceCount']==1890
assert all(x['status']!='VALIDATED' for x in adj['analyses'])
by={x['occurrenceId']:x for x in adj['analyses']}; gold=load('data/linguistic/gold/juste-gold.json')['entries']
assert 20<=len(gold)<=40 and len({x['occurrenceId'] for x in gold})==len(gold)
metrics={'correct':0,'unknown':0,'ambiguous':0,'contradictory':0}
for g in gold:
 assert g['occurrenceId'] in by
 a=by[g['occurrenceId']]
 if a['category']==g['category']:metrics['correct']+=1
 elif a['category']=='UNKNOWN':metrics['unknown']+=1
 elif a['category']=='AMBIGUOUS':metrics['ambiguous']+=1
 else:metrics['contradictory']+=1
assert metrics['contradictory']==0,metrics
def o(surface,context):
 i=context.casefold().find(surface.casefold());return {'surfaceForm':context[i:i+len(surface)],'context':context,'startOffset':i}
# Adversarial generic probes: former false positives must abstain, not become ADV.
for c in ['la façon juste de vivre','la vision juste des imperfections','une attitude intérieure juste pour agir','il est juste là','il est juste enfermé']:
 a=gen.analyse_configured(o('juste',c),cfg);assert a['category']!='ADVERB',(c,a)
# High-confidence reusable frames.
for c,w in [('une juste orientation','UNKNOWN'),('cela est juste, vraiment','ADJECTIVE'),("c'est juste une image",'ADVERB'),('il faut juste comprendre','UNKNOWN'),('le juste, le vrai','ADJECTIVE')]:
 a=gen.analyse_configured(o('juste',c),cfg);assert a['category']==w,(c,a,w)
# Existing pilots must reconstruct byte-structurally.
for stem in ('porte','suis'):
 c=load(f'data/linguistic/pilots/{stem}-config.json');rr,aa,ii=gen.build(c)
 assert rr==load(f'data/linguistic/pilots/{stem}-occurrences.json')
 assert aa==load(f'data/linguistic/pilots/{stem}.json')
 assert ii==load(f'data/linguistic/pilots/{stem}-compounds.json')
subprocess.run([sys.executable,str(R/'scripts/audit_linguistic_inversion_008.py')],check=True)
print(json.dumps({'raw':raw['occurrenceCount'],'counts':adj['counts'],'segmentation':adj['segmentationCounts'],'gold':metrics},ensure_ascii=False))
