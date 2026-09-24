#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path
# This audit is also the permanent regression sentinel for findings from mission 003.
ROOT=Path(__file__).resolve().parents[1]
def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
occ=loadmod('occ','scripts/build_linguistic_occurrence_index.py'); gen=loadmod('adjgen','scripts/build_linguistic_adjudication.py')
cfg=json.loads((ROOT/'data/linguistic/pilots/porte-config.json').read_text(encoding='utf-8'))
raw=json.loads((ROOT/'data/linguistic/pilots/porte-occurrences.json').read_text(encoding='utf-8'))
adj=json.loads((ROOT/'data/linguistic/pilots/porte.json').read_text(encoding='utf-8'))
inv=json.loads((ROOT/'data/linguistic/pilots/porte-compounds.json').read_text(encoding='utf-8'))
gold=json.loads((ROOT/'data/linguistic/gold/porte-gold.json').read_text(encoding='utf-8'))
# Full provenance: canonical corpus -> raw index -> segmentation/adjudication/inventory.
rr,aa,ii=gen.build(cfg)
assert rr==raw,'raw index not reproducible from canonical corpus'
assert aa==adj,'adjudication not reproducible from versioned generator'
assert ii==inv,'compound inventory not reproducible from versioned generator'
assert adj['generator']=='scripts/build_linguistic_adjudication.py'
# Identity, offsets, uniqueness.
ids=[x['occurrenceId'] for x in raw['occurrences']]; assert len(ids)==len(set(ids))==1184
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8')); records={}
for rel in catalog['records']:
 p=ROOT/rel
 if p.exists():
  o=json.loads(p.read_text(encoding='utf-8'))
  if occ.searchable(rel,o): records[o['id']]=o
for x in raw['occurrences']:
 o=records[x['recordId']]; original=None
 for field,verse,text in occ.fields(o):
  if field==x['field'] and verse==x['verseNumber']: original=text;break
 assert original is not None
 s,e=x['startOffset'],x['endOffset'];assert original[s:e]==x['surfaceForm']
 assert x['occurrenceId']==occ.oid(x['recordId'],x['field'],x['verseNumber'],s,e)
# Segmentation partition and retained totals.
sc=adj['segmentationCounts'];assert sc=={'AUTONOMOUS':1154,'VERB_CLITIC':3,'COMPOUND_ELEMENT':27}
assert sum(sc.values())==1184 and adj['linguisticRetainedTotal']==sc['AUTONOMOUS']+sc['VERB_CLITIC']==1157
assert inv['count']==sc['COMPOUND_ELEMENT']==len(inv['occurrences'])
assert {x['occurrenceId'] for x in inv['occurrences']}=={x['occurrenceId'] for x in adj['analyses'] if x['segmentation']=='COMPOUND_ELEMENT'}
# No automatic validation.
assert all(x['status']!='VALIDATED' for x in adj['analyses'])
# Coverage and declared counts.
assert {x['occurrenceId'] for x in adj['analyses']}==set(ids)
counts={k:sum(x['category']==k for x in adj['analyses']) for k in ('NOUN','VERB_PORTER','OTHER','UNKNOWN','AMBIGUOUS')}
assert counts==adj['counts']
# Gold set is independent, small, unique and explicitly human-audited.
assert gold['provenance']['validationType']=='human-audited' and 10<=len(gold['entries'])<=30
gids=[x['occurrenceId'] for x in gold['entries']];assert len(gids)==len(set(gids)) and set(gids)<=set(ids)
by={x['occurrenceId']:x for x in adj['analyses']}
for g in gold['entries']:
 a=by[g['occurrenceId']];assert a['segmentation']==g['expectedSegmentation']
 if g['expectedSegmentation']=='COMPOUND_ELEMENT': assert a['category']=='OTHER'
 elif g['expectedSegmentation']=='VERB_CLITIC': assert a['category']=='VERB_PORTER'
 else: assert a['category'] in {g['expectedCategory'],'UNKNOWN'},f"gold contradiction {g['occurrenceId']}: {a['category']} vs {g['expectedCategory']}"
# Five 003 sentinels may be correct or UNKNOWN, never the known wrong classification.
sent={'occ-4210e70fcbe4e1d65b894181':'NOUN','occ-f5043c17057a47db9e0b5eed':'VERB_PORTER','occ-a18d1242395f001f1889f138':'VERB_PORTER','occ-75cd0c3a829334cbf3d2165c':'VERB_PORTER','occ-8a55dd99471758e92a13b630':'VERB_PORTER'}
for oid,correct in sent.items(): assert by[oid]['category'] in {correct,'UNKNOWN'}
# Multi-word literal compatibility remains additive: original corpus text is untouched and token index still sees PORTE inside a phrase.
phrase='frapper à la porte'; hits=[m.group() for m in occ.TOKEN_RE.finditer(phrase) if occ.norm(m.group())=='porte'];assert hits==['porte'] and phrase.endswith('la porte')
print('Linguistic foundation 004 audit PASS:',json.dumps({'raw':len(ids),'segmentation':sc,'retained':adj['linguisticRetainedTotal'],'counts':counts,'gold':len(gold['entries'])},ensure_ascii=False))
