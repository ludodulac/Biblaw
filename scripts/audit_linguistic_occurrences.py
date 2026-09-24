#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('occ',ROOT/'scripts/build_linguistic_occurrence_index.py'); occ=importlib.util.module_from_spec(spec); spec.loader.exec_module(occ)
RAW=ROOT/'data/linguistic/pilots/porte-occurrences.json'; ADJ=ROOT/'data/linguistic/pilots/porte.json'; LEX=ROOT/'data/linguistic/lexicon.json'
raw=json.loads(RAW.read_text(encoding='utf-8')); adj=json.loads(ADJ.read_text(encoding='utf-8')); lex=json.loads(LEX.read_text(encoding='utf-8'))
# Synthetic contracts: case, accents, apostrophes, punctuation, duplicate positions, deterministic IDs.
assert occ.norm('PORTE')=='porte' and occ.norm('Porte')=='porte'
assert occ.norm('porté')=='porté' and occ.norm('porte')!='porté'
sample="Porte, l’homme porte; l'homme porte. frapper à la porte"
tokens=[(m.group(),m.start(),m.end()) for m in occ.TOKEN_RE.finditer(sample)]
porte=[x for x in tokens if occ.norm(x[0])=='porte']
assert len(porte)==4 and len({(s,e) for _,s,e in porte})==4
for surface,s,e in porte: assert sample[s:e]==surface
assert "frapper à la porte" in sample
a=occ.oid('r','text',None,1,6); assert a==occ.oid('r','text',None,1,6) and a!=occ.oid('r','text',None,10,15)
# Deterministic regeneration from canonical files.
generated=occ.payload('porte')
assert generated==raw, 'committed raw PORTE slice differs from deterministic canonical regeneration'
ids=[x['occurrenceId'] for x in raw['occurrences']]
assert len(ids)==len(set(ids)), 'duplicate occurrenceId'
# Canonical lookup and original-text offset verification.
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8')); records={}
for rel in catalog['records']:
 p=ROOT/rel
 if not p.exists(): continue
 o=json.loads(p.read_text(encoding='utf-8'))
 if occ.searchable(rel,o): records[o['id']]=o
for x in raw['occurrences']:
 assert x['recordId'] in records, f"missing recordId {x['recordId']}"
 o=records[x['recordId']]; found=None
 for field,verse,text in occ.fields(o):
  if field==x['field'] and verse==x['verseNumber']: found=text; break
 assert found is not None, f"missing field for {x['occurrenceId']}"
 s,e=x['startOffset'],x['endOffset']; assert 0<=s<e<=len(found)
 assert found[s:e]==x['surfaceForm'], f"offset mismatch {x['occurrenceId']}"
 assert occ.norm(x['surfaceForm'])=='porte'
 assert x['occurrenceId']==occ.oid(x['recordId'],x['field'],x['verseNumber'],s,e)
# Adjudication coverage and referential integrity.
allowed={'NOUN','VERB_PORTER','OTHER','AMBIGUOUS','UNKNOWN'}; statuses={'PROVISIONAL','VALIDATED','AMBIGUOUS','UNKNOWN'}
analyses=adj['analyses']; aids=[x['occurrenceId'] for x in analyses]
assert len(aids)==len(set(aids))==len(ids)
assert set(aids)==set(ids), 'PORTE adjudication is incomplete or orphaned'
for x in analyses:
 assert x['category'] in allowed and x['status'] in statuses
 if x['category']=='UNKNOWN': assert x['status']=='UNKNOWN'
 if x['category']=='AMBIGUOUS': assert x['status']=='AMBIGUOUS'
# Lexicon is possibility-only and contains both attested pilot analyses.
entry=next(x for x in lex['entries'] if x['normalizedForm']=='porte')
pairs={(x['lemma'],x['partOfSpeech']) for x in entry['possibleAnalyses']}
assert ('porte','NOUN') in pairs and ('porter','VERB') in pairs and 'never sufficient' in entry['decisionPolicy']
# Real same-record sentinel.
gab=[x for x in raw['occurrences'] if x['recordId']=='gabriel-book-18-prayer-001']
gab_a={x['occurrenceId']:x for x in analyses}
assert any(gab_a[x['occurrenceId']]['category']=='VERB_PORTER' and 'qui porte' in x['context'].lower() for x in gab)
assert any(gab_a[x['occurrenceId']]['category']=='NOUN' and 'porte ouvrant' in x['context'].lower() for x in gab)
counts={k:sum(1 for x in analyses if x['category']==k) for k in sorted(allowed)}
assert counts=={k:adj['counts'].get(k,0) for k in sorted(allowed)}
print(f"Linguistic occurrence audit PASS: {len(ids)} PORTE occurrences; "+", ".join(f"{k}={v}" for k,v in counts.items()))
