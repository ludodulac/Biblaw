#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('occ',ROOT/'scripts/build_linguistic_occurrence_index.py'); occ=importlib.util.module_from_spec(spec); spec.loader.exec_module(occ)
def hits(text,form='porte'):
 return [(m.group(),m.start(),m.end()) for m in occ.TOKEN_RE.finditer(text) if occ.norm(m.group())==occ.norm(form)]
assert hits('porte')==[('porte',0,5)]
assert len(hits('porte puis porte'))==2 and hits('porte puis porte')[0][1:]!=hits('porte puis porte')[1][1:]
assert occ.norm('ÉTÉ')=='été' and occ.norm('porté')!='porte'
assert hits('l’homme porte')[-1][0]=='porte'
assert hits("l'homme porte")[-1][0]=='porte'
assert hits('(Porte), porte!')==[('Porte',1,6),('porte',9,14)]
phrase='frapper à la porte'; assert phrase[phrase.index('porte'):phrase.index('porte')+5]=='porte' and len(hits(phrase))==1
assert occ.oid('r','verses.text',7,10,15)==occ.oid('r','verses.text',7,10,15)
assert occ.oid('r','verses.text',7,10,15)!=occ.oid('r','verses.text',7,30,35)
print('Linguistic occurrence unit tests PASS: simple, duplicate, accents, apostrophes, punctuation, case, phrase, deterministic identity')
