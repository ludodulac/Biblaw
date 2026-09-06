#!/usr/bin/env python3
"""Finalize Michael book 21 after all close semantic passes, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-21.json'
CORPUS=ROOT/'data/corpus/books/book-21'
EXPECTED=set(range(131,165))
LEGACY=('Le psaume développe de façon répétée le thème','Le psaume développe explicitement le thème')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main():
 d=load(PATH); by={a['number']:a for a in d.get('psalmAnalyses',[])}
 missing=sorted(EXPECTED-set(by)); extra=sorted(set(by)-EXPECTED)
 if missing or extra: raise SystemExit(f'Book 21 analysis range mismatch: missing={missing} extra={extra}')
 errors=[]
 for n in sorted(EXPECTED):
  a=by[n]; corpus=load(CORPUS/f'psalm-{n:03d}.json'); valid={v['number'] for v in corpus.get('verses',[])}
  if a.get('semanticDepth')!='deep-content-grounded': errors.append(f'{n}:not-deep')
  for t in a.get('themes',[]):
   teaching=(t.get('teaching') or '').strip()
   if not teaching or teaching.startswith(LEGACY): errors.append(f'{n}:{t.get("themeId")}:generic-teaching')
   refs=t.get('verseNumbers',[])
   if not refs: errors.append(f'{n}:{t.get("themeId")}:no-evidence')
   bad=[x for x in refs if x not in valid]
   if bad: errors.append(f'{n}:{t.get("themeId")}:invalid-verses={bad}')
 if errors: raise SystemExit('Book 21 cannot be finalized:\n'+'\n'.join(errors))
 d['psalmAnalyses']=[by[n] for n in sorted(EXPECTED)]
 m=d.setdefault('method',{}); m['semanticPass']='deep-content-grounded-complete'; m['deepPsalmCount']=34; m['contentGrounding']='complete'
 d['bookSynthesis']={
  'centralAxis':("Dans le livre 21, Michaël relie la dignité à la capacité de devenir un être conscient, stable et créateur au milieu de plusieurs mondes. Le livre revient sur la parole, la pensée, le travail, l’énergie, le corps, les pieds, la concentration et l’intelligence comme instruments qu’il faut éduquer puis conduire jusqu’à l’œuvre. La dignité se vérifie moins dans une affirmation de soi que dans le discernement des influences, la responsabilité envers sa destinée, la fidélité aux actes entrepris, le respect des espaces et des règnes de la Mère, et la capacité à maintenir une Alliance vivante entre ciel et terre. Les psaumes opposent régulièrement l’abstraction, la dispersion, les apparences et les croyances non vérifiées à l’étude, à la présence, à la vérité vécue et à l’achèvement. Les derniers textes élargissent cette logique à la vie collective : communauté, institutions, dirigeants, conseil de sages et œuvres communes doivent eux aussi recevoir clarté, corps et continuité pour servir le Bien commun. Cette synthèse décrit les articulations internes du corpus sans présenter ses affirmations doctrinales ou prophétiques comme des faits extérieurs."),
  'majorThemes':['dignite','intelligence','conscience','concentration','parole-vivante','pensee-creatrice','responsabilite','destinee','travail','oeuvre','realisation','corps','tradition','alliance','verite','discernement','mere','regnes','bien-commun','vie-collective','transmission']}
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Book 21 finalized: 34/34 deep-content-grounded analyses')
if __name__=='__main__': main()
