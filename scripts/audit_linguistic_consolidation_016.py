#!/usr/bin/env python3
import json,hashlib,importlib.util,collections,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
BASE_ENGINE_SHA='ca063c03d3eedb7f5dc976c51dc4ad992ea437ce'
def load(p): return json.loads((R/p).read_text(encoding='utf-8'))
def gitblob(p):
 b=(R/p).read_bytes(); return hashlib.sha1((f"blob {len(b)}\0").encode()+b).hexdigest()
assert gitblob('scripts/build_linguistic_adjudication.py')==BASE_ENGINE_SHA
cfg=load('data/linguistic/pilots/garde-config.json')
spec=importlib.util.spec_from_file_location('m',R/'scripts/build_linguistic_adjudication.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,adj,inv=m.build(cfg)
assert raw['occurrenceCount']==99
assert adj['segmentationCounts']=={'AUTONOMOUS':76,'VERB_CLITIC':16,'COMPOUND_ELEMENT':7}
assert adj['counts']=={'NOUN_GARDE':19,'VERB_GARDER':50,'OTHER':7,'UNKNOWN':23,'AMBIGUOUS':0}
assert inv['count']==7
for rel,obj in [('data/linguistic/pilots/garde-occurrences.json',raw),('data/linguistic/pilots/garde.json',adj),('data/linguistic/pilots/garde-compounds.json',inv)]: assert load(rel)==obj,rel
g1=load('data/linguistic/gold/garde-gold.json');g2=load('data/linguistic/gold/garde-adversarial-gold.json');g3=load('data/linguistic/gold/garde-adversarial-gold-015.json')
S1={x['occurrenceId'] for x in g1['entries']};S2={x['occurrenceId'] for x in g2['entries']};S3={x['occurrenceId'] for x in g3['entries']}
dups=S1&S2; u2=S2-S1
expected={'occ-41014a816a23e39e72453b8b','occ-9983886fe77edaef59d32093','occ-547160107b7cda09d673efc8','occ-c00102a35e0b51748775d601'}
assert len(S1)==18 and len(S2)==12 and dups==expected and len(u2)==8 and len(S3)==10
assert not (S1&S3) and not (u2&S3)
by={x['occurrenceId']:x for x in adj['analyses']}
human={x['occurrenceId']:x for g in (g1,g2,g3) for x in g['entries']}
distinct=S1|u2|S3
z=collections.Counter()
for oid in distinct:
 h=human[oid];a=by[oid]
 if a['category']==h['category']: z['correct']+=1
 elif a['status']=='UNKNOWN': z['unknown']+=1
 elif a['status']=='AMBIGUOUS': z['ambiguous']+=1
 else:z['contradictory']+=1
assert len(distinct)==36 and z['contradictory']==0
# Rule evidence matrix.
matrix=[]
for rule in cfg['rules']:
 ev='config-rule:'+rule['id'];ids={a['occurrenceId'] for a in adj['analyses'] if a['evidence']==ev}
 matrix.append({'ruleId':rule['id'],'totalTriggers':len(ids),'inMainGold':len(ids&S1),'in014AdversarialUnique':len(ids&u2),'in015Gold':len(ids&S3),'outsideAllGolds':len(ids-distinct),'linguisticStatus':'PROVISIONAL','independentEvidenceStatus':rule.get('independentEvidenceStatus','OBSERVED_OUTSIDE_MAIN_GOLD' if ids-S1 else 'LIMITED')})
poss=next(x for x in matrix if x['ruleId']=='garde-noun-possessive')
assert poss['totalTriggers']==1 and poss['inMainGold']==1 and poss['in014AdversarialUnique']==0 and poss['in015Gold']==0 and poss['outsideAllGolds']==0
assert next(r for r in cfg['rules'] if r['id']=='garde-noun-possessive')['evidenceScope']=='SINGLE_CORPUS_TRIGGER'
ct=json.dumps(cfg,ensure_ascii=False).casefold(); assert 'occ-' not in json.dumps(cfg['rules']).casefold()
engine=(R/'scripts/build_linguistic_adjudication.py').read_text(encoding='utf-8').casefold(); assert 'garde' not in engine
cl=[a for a in adj['analyses'] if a['segmentation']=='VERB_CLITIC'];assert len(cl)==16 and all(a['category']=='VERB_GARDER' for a in cl)
comp=collections.Counter(x['surfaceForm'].casefold() for x in inv['occurrences']);assert comp==collections.Counter({'garde-manger':5,'garde-mangers':1,'garde-fou':1})
print(json.dumps({'gold014Duplicates':sorted(dups),'distinctHumanEvidence':len(distinct),'humanEvidence':dict(z),'ruleEvidenceMatrix':matrix,'engineChanged':False,'newGenericFrames':0,'wordSpecificCodeBranches':0},ensure_ascii=False))
