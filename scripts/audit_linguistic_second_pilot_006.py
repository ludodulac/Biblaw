#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
occ=load('occ','scripts/build_linguistic_occurrence_index.py');gen=load('gen','scripts/build_linguistic_adjudication.py')
cfg=json.loads((ROOT/'data/linguistic/pilots/suis-config.json').read_text(encoding='utf-8'))
raw=json.loads((ROOT/'data/linguistic/pilots/suis-occurrences.json').read_text(encoding='utf-8'))
adj=json.loads((ROOT/'data/linguistic/pilots/suis.json').read_text(encoding='utf-8'))
inv=json.loads((ROOT/'data/linguistic/pilots/suis-compounds.json').read_text(encoding='utf-8'))
gold=json.loads((ROOT/'data/linguistic/gold/suis-gold.json').read_text(encoding='utf-8'))
rr,aa,ii=gen.build(cfg)
assert rr==raw and aa==adj and ii==inv, 'SUIS artifacts are not reproducible from canonical corpus'
assert raw['occurrenceCount']==631
ids=[x['occurrenceId'] for x in raw['occurrences']];assert len(ids)==len(set(ids))==631
assert adj['segmentationCounts']=={'AUTONOMOUS':615,'VERB_CLITIC':1,'COMPOUND_ELEMENT':10,'VERB_INVERSION':5}
assert sum(adj['segmentationCounts'].values())==631 and adj['linguisticRetainedTotal']==621
assert adj['counts']=={'VERB_ETRE':116,'VERB_SUIVRE':4,'OTHER':10,'UNKNOWN':501,'AMBIGUOUS':0}
assert all(x['status']!='VALIDATED' for x in adj['analyses'])
# Canonical offsets and identities.
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'));records={}
for rel in catalog['records']:
 p=ROOT/rel
 if p.exists():
  o=json.loads(p.read_text(encoding='utf-8'))
  if occ.searchable(rel,o):records[o['id']]=o
for x in raw['occurrences']:
 o=records[x['recordId']]; original=None
 for field,verse,text in occ.fields(o):
  if field==x['field'] and verse==x['verseNumber']:original=text;break
 assert original is not None
 s,e=x['startOffset'],x['endOffset'];assert original[s:e]==x['surfaceForm']
 assert x['occurrenceId']==occ.oid(x['recordId'],x['field'],x['verseNumber'],s,e)
# Segmentation sentinels.
by={x['occurrenceId']:x for x in adj['analyses']}
assert by['occ-50f49afe4946617ebb1bda1c']['segmentation']=='VERB_CLITIC'
for oid in ['occ-47c84cbf66fab6b4de6b4437','occ-fb7d101d388c4ce8a34c402b','occ-7974eeb9afb641bbaed6116b','occ-67c4071d0dd4f3265fce5b31','occ-5937680d6e0c20fe9df2f3ed']:
 assert by[oid]['segmentation']=='VERB_INVERSION'
assert {x['surfaceForm'] for x in inv['occurrences']}=={'Je-Suis'} and inv['count']==10
# Independent human gold: automatic result may agree or prudently abstain, never contradict.
assert gold['provenance']['validationType']=='human-audited' and len(gold['entries'])==14
rb={x['occurrenceId']:x for x in raw['occurrences']}
for g in gold['entries']:
 assert g['occurrenceId'] in rb and rb[g['occurrenceId']]['context']==g['context']
 a=by[g['occurrenceId']];assert a['segmentation']==g['expectedSegmentation']
 assert a['category'] in {g['expectedCategory'],'UNKNOWN'},(g['occurrenceId'],a['category'],g['expectedCategory'])
 if a['category']!='UNKNOWN':
  assert a['lemma']==g['lemma'] and a['partOfSpeech']==g['partOfSpeech']
# Lexicon has two same-POS, different-lemma possibilities.
lex=json.loads((ROOT/'data/linguistic/lexicon.json').read_text(encoding='utf-8'))
entry=next(x for x in lex['entries'] if x['normalizedForm']=='suis')
assert {(x['lemma'],x['partOfSpeech']) for x in entry['possibleAnalyses']}=={('être','VERB'),('suivre','VERB')}
# Structural engine must not branch on candidate word.
engine=(ROOT/'scripts/build_linguistic_adjudication.py').read_text(encoding='utf-8')
assert "word == 'suis'" not in engine and 'word == "suis"' not in engine
print('Linguistic second pilot 006 audit PASS:',json.dumps({'raw':631,'segmentation':adj['segmentationCounts'],'retained':621,'counts':adj['counts'],'gold':14},ensure_ascii=False))
