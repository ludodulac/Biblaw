#!/usr/bin/env python3
"""Finalize Raphael book 19 after all close semantic passes, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-19.json'
CORPUS=ROOT/'data/corpus/books/book-19'
EXPECTED=set(range(102,128))
GENERIC=('Le psaume développe explicitement le thème','Le thème «')

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main():
 d=load(PATH); by={a['number']:a for a in d.get('psalmAnalyses',[])}
 missing=sorted(EXPECTED-set(by))
 if missing: raise SystemExit(f'Book 19 missing analyses: {missing}')
 errors=[]
 for n in sorted(EXPECTED):
  a=by[n]; corpus=load(CORPUS/f'psalm-{n:03d}.json'); valid={v['number'] for v in corpus.get('verses',[])}
  if a.get('semanticDepth')!='deep-content-grounded': errors.append(f'{n}:not-deep')
  for t in a.get('themes',[]):
   teaching=(t.get('teaching') or '').strip()
   if not teaching or teaching.startswith(GENERIC): errors.append(f'{n}:{t.get("themeId")}:generic-teaching')
   refs=t.get('verseNumbers',[])
   if not refs: errors.append(f'{n}:{t.get("themeId")}:no-evidence')
   bad=[x for x in refs if x not in valid]
   if bad: errors.append(f'{n}:{t.get("themeId")}:invalid-verses={bad}')
 if errors: raise SystemExit('Book 19 cannot be finalized:\n'+'\n'.join(errors))
 d['psalmAnalyses']=[by[n] for n in sorted(EXPECTED)]
 d['method']['semanticPass']='deep-content-grounded-complete'; d['method']['deepPsalmCount']=26; d['method']['contentGrounding']='complete'
 d['bookSynthesis']={
  'centralAxis':('Dans le livre 19, Raphaël présente la pensée comme une réalité vivante qui se forme, respire, s’associe à des influences et finit par prendre corps dans les actes, les œuvres et la destinée. Le livre oppose le savoir accumulé au savoir vécu : connaître demande de penser, sentir, être, pratiquer et conduire une compréhension jusqu’à son accomplissement. La respiration, l’air, la communication, la mémoire et la Tradition décrivent différents milieux de liaison entre les mondes. L’âme, l’Alliance et le corps collectif assurent la continuité entre vie terrestre et réalité supérieure dans la logique du texte. Les psaumes insistent également sur la fidélité, l’achèvement des œuvres, la préparation aux étapes, la responsabilité et l’union comme conditions d’une pensée devenue sagesse vivante. Cette synthèse décrit les articulations internes du corpus sans présenter ses affirmations comme des faits extérieurs.'),
  'majorThemes':['pensee','pensee-vivante','sagesse','conscience','respiration','air','communication','tradition','ame','alliance','oeuvre','realisation','union','memoire-vivante','immortalite','fidelite','preparation','responsabilite']}
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Book 19 finalized: 26/26 deep-content-grounded analyses')
if __name__=='__main__': main()
