#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('occ',ROOT/'scripts/build_linguistic_occurrence_index.py'); occ=importlib.util.module_from_spec(spec); spec.loader.exec_module(occ)
HYPHENS='-‑–—'
SUBJECT_PRONOUNS={'je','tu','il','elle','on','nous','vous','ils','elles'}
def local_parts(o):
 i=min(o['startOffset'],90); return o['context'][:i],o['context'][i+len(o['surfaceForm']):]
def segmentation(o,clitics):
 before,after=local_parts(o)
 if after[:1] in HYPHENS:
  m=re.match(r"[^\W_]+",after[1:],re.UNICODE); follower=m.group().casefold() if m else ''
  if follower in SUBJECT_PRONOUNS: return 'VERB_INVERSION'
  if follower in {x.casefold() for x in clitics}: return 'VERB_CLITIC'
  return 'COMPOUND_ELEMENT'
 if before[-1:] in HYPHENS: return 'COMPOUND_ELEMENT'
 return 'AUTONOMOUS'
def full_compound(o):
 before,after=local_parts(o); left=re.search(rf'[^\s«»“”"(),.;:!?]*$',before); right=re.match(r'^[^\s«»“”"(),.;:!?]*',after)
 return (left.group(0) if left else '')+o['surfaceForm']+(right.group(0) if right else '')
def analyse_configured(o,cfg):
 seg=segmentation(o,cfg.get('clitics',[])); before,after=local_parts(o); by={x['category']:x for x in cfg['analyses']}
 if seg=='COMPOUND_ELEMENT': return {'category':'OTHER','lemma':None,'partOfSpeech':None,'status':'PROVISIONAL','evidence':'segmentation:compound-element','segmentation':seg}
 mapped=cfg.get('segmentationAnalyses',{}).get(seg)
 if mapped:
  x=by[mapped]; return {'category':x['category'],'lemma':x['lemma'],'partOfSpeech':x['partOfSpeech'],'status':'PROVISIONAL','evidence':'morphosyntax:'+seg.lower().replace('_','-'),'segmentation':seg}
 for rule in cfg.get('rules',[]):
  if rule.get('beforeRegex') and not re.search(rule['beforeRegex'],before,re.I): continue
  if rule.get('afterRegex') and not re.search(rule['afterRegex'],after,re.I): continue
  x=by[rule['analysis']]; return {'category':x['category'],'lemma':x['lemma'],'partOfSpeech':x['partOfSpeech'],'status':'PROVISIONAL','evidence':'config-rule:'+rule['id'],'segmentation':seg}
 return {'category':'UNKNOWN','lemma':None,'partOfSpeech':None,'status':'UNKNOWN','evidence':'context-insufficient-conservative','segmentation':seg}
def analyse_legacy(o,cfg):
 seg=segmentation(o,cfg['clitics']); before,after=local_parts(o); b=before.casefold(); a=after.casefold()
 noun=cfg['noun']; verb=cfg['verb']
 if seg=='COMPOUND_ELEMENT': return {'category':'OTHER','lemma':None,'partOfSpeech':None,'status':'PROVISIONAL','evidence':'segmentation:compound-element','segmentation':seg}
 if seg=='VERB_CLITIC': return {'category':verb['category'],'lemma':verb['lemma'],'partOfSpeech':verb['partOfSpeech'],'status':'PROVISIONAL','evidence':'morphosyntax:verb-clitic','segmentation':seg}
 subj=re.search(r"(?:^|[\s«“\"(])(?:je|tu|il|elle|on|nous|vous|ils|elles|qui|qu['’]il|qu['’]elle|chacun|personne)\s+(?:ne\s+|n['’]\s*)?$",b)
 noun_coll=re.search(r"(?:ouvrir|ouvre|ouvres|ouvrent|ouvert|fermer|ferme|fermes|ferment|fermé|franchir|franchit|franchis)\s+(?:la|une|cette|sa|ma|ta|notre|votre|leur|telle)\s+$",b)
 noun_det=re.search(r"(?:^|[\s«“\"(])(?:une|cette|sa|ma|ta|notre|votre|leur|chaque|aucune|quelle|telle|seule|grande|petite|sainte|même|dernière|première|nouvelle)\s+$",b)
 noun_pred=re.match(r"^\s+(?:ouvrant|s['’]ouvre|s['’]ouvrira|est\s+ouverte|est\s+fermée|sera\s+ouverte|sera\s+fermée)\b",a)
 imperative=(o['surfaceForm'][:1].isupper() and (not before.strip() or re.search(r'[.!?…:;]\s*$',before)) and re.match(r"^\s+(?:le|la|les|un|une|des|ce|cet|cette|ces|son|sa|ses|mon|ma|mes|ton|ta|tes|notre|votre|leur|leurs|en|sur|dans|à|au|aux|avec)\b",a))
 if noun_coll or noun_det or noun_pred: return {'category':noun['category'],'lemma':noun['lemma'],'partOfSpeech':noun['partOfSpeech'],'status':'PROVISIONAL','evidence':'morphosyntax:noun-frame-conservative','segmentation':seg}
 if subj or imperative: return {'category':verb['category'],'lemma':verb['lemma'],'partOfSpeech':verb['partOfSpeech'],'status':'PROVISIONAL','evidence':'morphosyntax:verb-frame-conservative','segmentation':seg}
 return {'category':'UNKNOWN','lemma':None,'partOfSpeech':None,'status':'UNKNOWN','evidence':'context-insufficient-conservative-v004','segmentation':seg}
def analyse(o,cfg):\n return analyse_configured(o,cfg) if 'analyses' in cfg else analyse_legacy(o,cfg)\ndef build(cfg):
 raw=occ.payload(cfg['normalizedForm']); analyses=[]; compounds=[]
 for o in raw['occurrences']:
  a={'occurrenceId':o['occurrenceId'],**analyse(o,cfg)}; analyses.append(a)
  if a['segmentation']=='COMPOUND_ELEMENT':
   compounds.append({'occurrenceId':o['occurrenceId'],'surfaceForm':full_compound(o),'context':o['context'],'segmentation':'COMPOUND_ELEMENT'})
 counts={k:sum(x['category']==k for x in analyses) for k in ('NOUN','VERB_PORTER','OTHER','UNKNOWN','AMBIGUOUS')}
 segcounts={k:sum(x['segmentation']==k for x in analyses) for k in ('AUTONOMOUS','VERB_CLITIC','COMPOUND_ELEMENT')}
 adj={'schemaVersion':2,'purpose':cfg.get('purpose','porte-pilot-reproducible-adjudication'),'normalizedForm':cfg['normalizedForm'],'generator':'scripts/build_linguistic_adjudication.py','policy':'Conservative generic morphosyntactic evidence produces PROVISIONAL only; unresolved retained units remain UNKNOWN; compounds are preserved as OTHER and excluded from linguistic retained total.','counts':counts,'segmentationCounts':segcounts,'linguisticRetainedTotal':sum(v for k,v in segcounts.items() if k!='COMPOUND_ELEMENT'),'analyses':analyses}
 inv={'schemaVersion':1,'purpose':'compound-elements-containing-target-surface','normalizedForm':cfg['normalizedForm'],'generator':'scripts/build_linguistic_adjudication.py','count':len(compounds),'occurrences':compounds}
 return raw,adj,inv
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',default='data/linguistic/pilots/porte-config.json');ap.add_argument('--write',action='store_true');a=ap.parse_args()
 cfg=json.loads((ROOT/a.config).read_text(encoding='utf-8')); raw,adj,inv=build(cfg)
 if a.write:
  stem=cfg.get('outputStem','porte'); targets=[(f'data/linguistic/pilots/{stem}-occurrences.json',raw),(f'data/linguistic/pilots/{stem}.json',adj),(f'data/linguistic/pilots/{stem}-compounds.json',inv)]
  for rel,obj in targets:(ROOT/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'raw':raw['occurrenceCount'],'segmentation':adj['segmentationCounts'],'retained':adj['linguisticRetainedTotal'],'counts':adj['counts'],'compounds':inv['count']},ensure_ascii=False))
if __name__=='__main__':main()
