#!/usr/bin/env python3
import json,importlib.util,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('g',R/'scripts/build_linguistic_adjudication.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
cfg=load('data/linguistic/pilots/juste-config.json');raw,adj,inv=g.build(cfg)
assert raw==load('data/linguistic/pilots/juste-occurrences.json')
assert adj==load('data/linguistic/pilots/juste.json')
assert inv==load('data/linguistic/pilots/juste-compounds.json')
assert raw['occurrenceCount']==1890
assert adj['segmentationCounts']=={'AUTONOMOUS':1890,'VERB_CLITIC':0,'COMPOUND_ELEMENT':0}
assert adj['counts']=={'ADJECTIVE':290,'ADVERB':78,'OTHER':0,'UNKNOWN':1522,'AMBIGUOUS':0},adj['counts']
assert all(a['status']!='VALIDATED' for a in adj['analyses'])
assert not any(x['partOfSpeech']=='NOUN' for x in cfg['analyses'])
assert set(cfg['genericRules'])=={'copular-predicate-adjective','adverb-before-determiner','nominalized-adjective-use'}
by={a['occurrenceId']:a for a in adj['analyses']};gold=load('data/linguistic/gold/juste-gold.json')['entries']
revised=[x for x in gold if 'previousAnalysis' in x]
assert len(revised)==5
for x in revised:
 assert x['previousAnalysis']=={'category':'NOUN','partOfSpeech':'NOUN'}
 assert x['category']=='ADJECTIVE' and x['partOfSpeech']=='ADJ' and x['usage']=={'nominalized':True}
 a=by[x['occurrenceId']]
 assert a['category']=='ADJECTIVE' and a.get('usage')=={'nominalized':True},(x,a)
metrics={'correct':0,'unknown':0,'contradictory':0}
for x in gold:
 a=by[x['occurrenceId']]
 if a['category']==x['category']: metrics['correct']+=1
 elif a['category']=='UNKNOWN': metrics['unknown']+=1
 else: metrics['contradictory']+=1
assert metrics['contradictory']==0,metrics
def o(surface,c):
 i=c.casefold().find(surface.casefold());return {'surfaceForm':c[i:i+len(surface)],'context':c,'startOffset':i}
def C(word,analyses,rules):
 return {'normalizedForm':word,'analyses':analyses,'genericPosMap':{x['partOfSpeech']:x['category'] for x in analyses},'genericRules':rules,'clitics':[],'rules':[]}
ADJADV=[{'category':'ADJECTIVE','lemma':'fort','partOfSpeech':'ADJ'},{'category':'ADVERB','lemma':'fort','partOfSpeech':'ADV'}]
assert g.analyse_configured(o('fort','un fort courant'),C('fort',ADJADV,['prenominal-adjective']))['category']=='UNKNOWN'
assert g.analyse_configured(o('fort','ce courant est fort.'),C('fort',ADJADV,['copular-predicate-adjective']))['category']=='ADJECTIVE'
ROSE=[{'category':'ADJECTIVE','lemma':'rose','partOfSpeech':'ADJ'},{'category':'NOUN','lemma':'rose','partOfSpeech':'NOUN'}]
assert g.analyse_configured(o('rose','un rose bonbon'),C('rose',ROSE,['prenominal-adjective']))['category']=='UNKNOWN'
BIEN=[{'category':'ADVERB','lemma':'bien','partOfSpeech':'ADV'},{'category':'NOUN','lemma':'bien','partOfSpeech':'NOUN'}]
assert g.analyse_configured(o('bien','il faut bien comprendre'),C('bien',BIEN,['modal-adverb-before-infinitive']))['category']=='UNKNOWN'
MEME=[{'category':'ADJECTIVE','lemma':'même','partOfSpeech':'ADJ'},{'category':'ADVERB','lemma':'même','partOfSpeech':'ADV'}]
assert g.analyse_configured(o('même',"c'est même une évidence"),C('même',MEME,['adverb-before-determiner']))['category']=='ADVERB'
VRAI=[{'category':'ADJECTIVE','lemma':'vrai','partOfSpeech':'ADJ'},{'category':'NOUN','lemma':'vrai','partOfSpeech':'NOUN'}]
v=g.analyse_configured(o('vrai','le vrai, le beau'),C('vrai',VRAI,['nominalized-adjective-use']))
assert v['category']=='ADJECTIVE' and v['partOfSpeech']=='ADJ' and v['usage']=={'nominalized':True}
# Independent 010 adversarial sample: automatic may agree or abstain, never contradict.
expected={'occ-fdccbcc0695b26ebb50f060b':'ADJECTIVE','occ-406c78a20321f8feb409f6bd':'ADJECTIVE','occ-3bd59781e5f0d64ac81a9290':'ADJECTIVE','occ-07142990dba162c79e306be1':'ADJECTIVE','occ-fba4535682a6bf3d6a52d2a6':'ADVERB','occ-c1ff671d76ec8401a8c61c44':'ADVERB','occ-27398b2dbbc1e3f2837d6759':'ADVERB','occ-72d21d6832a51e9d64f3cdc6':'ADVERB','occ-cc396f3ef1de0feb070e1975':'ADJECTIVE','occ-b8cf42184458525f28388b09':'ADJECTIVE','occ-91095bfbacbabcbbc5cab1c8':'ADVERB','occ-63fc344b12b3369ed2a4a5b2':'ADVERB'}
adv={'correct':0,'unknown':0,'contradictory':0}
for oid,h in expected.items():
 a=by[oid]['category']
 if a==h:adv['correct']+=1
 elif a=='UNKNOWN':adv['unknown']+=1
 else:adv['contradictory']+=1
assert adv['contradictory']==0,adv
# Prior pilots reconstruct exactly.
for stem in ('porte','suis'):
 c=load(f'data/linguistic/pilots/{stem}-config.json');rr,aa,ii=g.build(c)
 assert rr==load(f'data/linguistic/pilots/{stem}-occurrences.json')
 assert aa==load(f'data/linguistic/pilots/{stem}.json')
 assert ii==load(f'data/linguistic/pilots/{stem}-compounds.json')
subprocess.run([sys.executable,str(R/'scripts/audit_linguistic_inversion_008.py')],check=True)
print(json.dumps({'juste':{'raw':1890,'counts':adj['counts']},'gold009':metrics,'adversarial010':adv,'revisedGold':len(revised)},ensure_ascii=False))
