#!/usr/bin/env python3
"""Finalize Ouriel book 20 after all close semantic passes, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-20.json'
CORPUS=ROOT/'data/corpus/books/book-20'
EXPECTED=set(range(104,130))
GENERIC=('Le psaume développe explicitement le thème','Le thème «')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main():
 d=load(PATH); by={a['number']:a for a in d.get('psalmAnalyses',[])}
 missing=sorted(EXPECTED-set(by))
 if missing: raise SystemExit(f'Book 20 missing analyses: {missing}')
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
 if errors: raise SystemExit('Book 20 cannot be finalized:\n'+'\n'.join(errors))
 d['psalmAnalyses']=[by[n] for n in sorted(EXPECTED)]
 d['method']['semanticPass']='deep-content-grounded-complete'; d['method']['deepPsalmCount']=26; d['method']['contentGrounding']='complete'
 d['bookSynthesis']={
  'centralAxis':('Dans le livre 20, Ouriel ramène constamment l’enseignement vers la terre, le corps, la structure et l’accomplissement. Une pensée, une vertu, une alliance ou une aspiration n’est pleinement reconnue que lorsqu’elle reçoit des fondements, une organisation, des actes et une continuité capables de la porter dans le réel. Le livre articule ainsi les deux terres visible et invisible, la conscience des lois et des influences, l’éducation, le discernement, la dignité des règnes, la Mère, la mémoire, la parole et le corps collectif. La réalisation juste exige de préparer les conditions, d’unifier les mondes sans les confondre, de préserver ce qui est précieux et de conduire les œuvres jusqu’à leur achèvement. Les derniers psaumes insistent sur la stabilité, l’écologie intérieure, l’impersonnalité, la parole vraie, la libération des mémoires héritées et l’organisation collective comme moyens de réécrire concrètement le futur. Cette synthèse décrit les articulations internes du corpus sans présenter ses affirmations comme des faits extérieurs.'),
  'majorThemes':['realisation','terre','corps','structure','lois','conscience','verite','discernement','organisation','oeuvre','mere','dignite','responsabilite','alliance','memoire','parole','stabilite','bien-commun']}
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Book 20 finalized: 26/26 deep-content-grounded analyses')
if __name__=='__main__': main()
