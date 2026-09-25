#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gen',ROOT/'scripts/build_linguistic_adjudication.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
def o(surface,full):
 i=full.casefold().find(surface.casefold());assert i>=0
 return {'surfaceForm':full[i:i+len(surface)],'context':full,'startOffset':i}
positive=[
 ('suis-je','suis'),('Suis-je','Suis'),
 ('porte-t-il','porte'),('Porte-t-il','Porte'),
 ('marche-t-elle','marche'),('Marche-t-elle','Marche'),
 ('a-t-il','a'),('A-t-il','A'),
 ('porte‑t‑il','porte'),('marche–t–elle','marche'),('a—t—on','a')
]
for full,surface in positive:
 got=gen.segmentation(o(surface,full),[])
 assert got=='VERB_INVERSION',(full,got)
negative=[
 ('porte-parole','porte','COMPOUND_ELEMENT'),
 ('porte-monnaie','porte','COMPOUND_ELEMENT'),
 ('porte-à-faux','porte','COMPOUND_ELEMENT'),
 ('Je-Suis','Suis','COMPOUND_ELEMENT'),
 ('porte-t-shirt','porte','COMPOUND_ELEMENT'),
 ('Suis le maître','Suis','AUTONOMOUS')
]
for full,surface,want in negative:
 got=gen.segmentation(o(surface,full),[])
 assert got==want,(full,got,want)
# Object clitic remains distinct.
assert gen.segmentation(o('suis','suis-le'),['le','la','les','lui','leur','en','y'])=='VERB_CLITIC'
# A non-verbal candidate must not become VERB_INVERSION from graphy alone.\nassert gen.segmentation(o('rayon','rayon-je'),[],False)=='COMPOUND_ELEMENT'\n# Segmentation does not decide a lemma/POS without candidate-specific mapping.
cfg={'analyses':[{'category':'A','lemma':'alpha','partOfSpeech':'VERB'},{'category':'B','lemma':'beta','partOfSpeech':'NOUN'}],'clitics':[],'rules':[]}
a=gen.analyse_configured(o('porte','porte-t-il'),cfg)
assert a['segmentation']=='VERB_INVERSION' and a['category']=='UNKNOWN' and a['lemma'] is None
# Conservative non-claim: direct nous/vous are graphically ambiguous with object/reflexive clitics.
for full,surface in [('aide-nous','aide'),('rappelez-vous','rappelez')]:
 assert gen.segmentation(o(surface,full),[])=='COMPOUND_ELEMENT'
print(json.dumps({'positive':len(positive),'negative':len(negative),'separation':'PASS','emptyBoundary':'PASS'},ensure_ascii=False))
