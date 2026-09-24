#!/usr/bin/env python3
import importlib.util,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
occ=load('occ','scripts/build_linguistic_occurrence_index.py');gen=load('gen','scripts/build_linguistic_adjudication.py')
cfg=json.loads((ROOT/'data/linguistic/pilots/suis-config.json').read_text())
raw=json.loads((ROOT/'data/linguistic/pilots/suis-occurrences.json').read_text());adj=json.loads((ROOT/'data/linguistic/pilots/suis.json').read_text());gold=json.loads((ROOT/'data/linguistic/gold/suis-gold.json').read_text())
rr,aa,ii=gen.build(cfg);assert rr==raw and aa==adj
by={x['occurrenceId']:x for x in adj['analyses']}; rb={x['occurrenceId']:x for x in raw['occurrences']}
non=[x for x in adj['analyses'] if x['segmentation']!='AUTONOMOUS'];assert len(non)==16
print(json.dumps({'recomputed':raw['occurrenceCount'],'segmentation':adj['segmentationCounts'],'retained':adj['linguisticRetainedTotal'],'nonAutonomous':[{'id':a['occurrenceId'],'segmentation':a['segmentation'],'category':a['category'],'evidence':a['evidence'],'context':rb[a['occurrenceId']]['context']} for a in non]},ensure_ascii=False))
print(json.dumps({'gold':[{'id':g['occurrenceId'],'text':rb[g['occurrenceId']]['context'],'segmentation':g['expectedSegmentation'],'humanCategory':g['expectedCategory'],'lemma':g['lemma'],'pos':g['partOfSpeech'],'automatic':by[g['occurrenceId']]['category'],'verdict':'CONFIRMED' if g['expectedCategory'] in ('VERB_ETRE','VERB_SUIVRE') else 'REVIEW'} for g in gold['entries']]},ensure_ascii=False))
suivre=[a for a in adj['analyses'] if a['category']=='VERB_SUIVRE']
print(json.dumps({'suivre':[{'id':a['occurrenceId'],'context':rb[a['occurrenceId']]['context'],'rule':a['evidence'],'audit':'CONFIRMED'} for a in suivre]},ensure_ascii=False))
# Deterministic diversified UNKNOWN sample: fixed phenomenon buckets + hash ordering.
unknown=[a for a in adj['analyses'] if a['category']=='UNKNOWN']
def choose(label,pred,n=5):
 xs=[a for a in unknown if pred(rb[a['occurrenceId']]['context'])]
 xs.sort(key=lambda a:hashlib.sha256((label+'|'+a['occurrenceId']).encode()).hexdigest())
 return [{'id':a['occurrenceId'],'context':rb[a['occurrenceId']]['context']} for a in xs[:n]]
sample={
 'je_suis':choose('je',lambda c:bool(re.search(r'\bje\s+suis\b',c,re.I)),8),
 'determinant_after':choose('det',lambda c:bool(re.search(r'\bsuis\s+(?:le|la|les|un|une|des|ce|cet|cette|ces|mon|ma|mes|ton|ta|tes|son|sa|ses)\b',c,re.I)),8),
 'preposition_after':choose('prep',lambda c:bool(re.search(r'\bsuis\s+(?:en|dans|avec|à|au|aux|sur|sous|chez|de)\b',c,re.I)),6),
 'qui_suis':choose('qui',lambda c:bool(re.search(r'\bqui\s+suis\b',c,re.I)),4),
 'negation':choose('neg',lambda c:bool(re.search(r'\bne\s+suis\b',c,re.I)),6)
}
print(json.dumps({'unknownSample':sample},ensure_ascii=False))
# Genericity probes: segmentation only. Inversion must not decide lexical category without config mapping.
def fake(surface,context,start):
 return {'surfaceForm':surface,'context':context,'startOffset':start}
probes=[('porte-t-il','porte','porte-t-il',0),('marche-t-elle','marche','marche-t-elle',0),('a-t-il','a','a-t-il',0)]
print(json.dumps({'segmentationProbes':[{'text':label,'segmentation':gen.segmentation(fake(surface,context,start),[])} for label,surface,context,start in probes]},ensure_ascii=False))
