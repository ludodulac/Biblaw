#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('g',R/'scripts/build_linguistic_adjudication.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def o(surface,c):
 i=c.casefold().find(surface.casefold());return {'surfaceForm':c[i:i+len(surface)],'context':c,'startOffset':i}
def cfg(word,analyses,rules):
 return {'normalizedForm':word,'analyses':analyses,'genericPosMap':{x['partOfSpeech']:x['category'] for x in analyses},'genericRules':rules,'clitics':[],'rules':[]}
cases=[]
def run(label,word,c,analyses,rules,human):
 a=g.analyse_configured(o(word,c),cfg(word,analyses,rules));cases.append({'label':label,'context':c,'human':human,'auto':a['category'],'evidence':a['evidence']})
ADJADV=[{'category':'ADJECTIVE','lemma':'fort','partOfSpeech':'ADJ'},{'category':'ADVERB','lemma':'fort','partOfSpeech':'ADV'}]
run('prenominal-reusable','fort','un fort courant',ADJADV,['prenominal-adjective'],'ADJECTIVE')
run('copular-reusable','fort','ce courant est fort.',ADJADV,['copular-predicate-adjective'],'ADJECTIVE')
BIEN=[{'category':'ADVERB','lemma':'bien','partOfSpeech':'ADV'},{'category':'NOUN','lemma':'bien','partOfSpeech':'NOUN'}]
run('modal-reusable','bien','il faut bien comprendre',BIEN,['modal-adverb-before-infinitive'],'ADVERB')
MEME=[{'category':'ADJECTIVE','lemma':'même','partOfSpeech':'ADJ'},{'category':'ADVERB','lemma':'même','partOfSpeech':'ADV'}]
run('before-det-reusable','même',"c'est même une évidence",MEME,['adverb-before-determiner'],'ADVERB')
# Falsification probe: superficial prenominal frame is not universally sufficient.
ROSE=[{'category':'ADJECTIVE','lemma':'rose','partOfSpeech':'ADJ'},{'category':'NOUN','lemma':'rose','partOfSpeech':'NOUN'}]
run('prenominal-counterexample','rose','un rose bonbon',ROSE,['prenominal-adjective'],'NOUN')
# Substantivization convention probe: engine encodes nominalized ADJ as NOUN when configured so.
VRAI=[{'category':'ADJECTIVE','lemma':'vrai','partOfSpeech':'ADJ'},{'category':'NOUN','lemma':'vrai','partOfSpeech':'NOUN'}]
run('substantivization-convention','vrai','le vrai, le beau',VRAI,['substantivized-adjective'],'CONVENTION_NOMINALIZED_ADJ')
print(json.dumps(cases,ensure_ascii=False))
