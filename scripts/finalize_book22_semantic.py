#!/usr/bin/env python3
"""Finalize Gabriel book 22 after all close semantic passes, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-22.json'; CORPUS=ROOT/'data/corpus/books/book-22'
EXPECTED=set(range(138,164)); LEGACY=('Le psaume développe de façon répétée le thème','Le psaume développe explicitement le thème')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main():
 d=load(PATH); by={a['number']:a for a in d.get('psalmAnalyses',[])}; missing=sorted(EXPECTED-set(by)); extra=sorted(set(by)-EXPECTED)
 if missing or extra: raise SystemExit(f'Book 22 analysis range mismatch: missing={missing} extra={extra}')
 errors=[]
 for n in sorted(EXPECTED):
  a=by[n]; valid={v['number'] for v in load(CORPUS/f'psalm-{n:03d}.json').get('verses',[])}
  if a.get('semanticDepth')!='deep-content-grounded': errors.append(f'{n}:not-deep')
  for t in a.get('themes',[]):
   teaching=(t.get('teaching') or '').strip(); refs=t.get('verseNumbers',[])
   if not teaching or teaching.startswith(LEGACY): errors.append(f'{n}:{t.get("themeId")}:generic-teaching')
   if not refs: errors.append(f'{n}:{t.get("themeId")}:no-evidence')
   bad=[x for x in refs if x not in valid]
   if bad: errors.append(f'{n}:{t.get("themeId")}:invalid-verses={bad}')
 if errors: raise SystemExit('Book 22 cannot be finalized:\n'+'\n'.join(errors))
 d['psalmAnalyses']=[by[n] for n in sorted(EXPECTED)]; m=d.setdefault('method',{}); m['semanticPass']='deep-content-grounded-complete'; m['deepPsalmCount']=26; m['contentGrounding']='complete'
 d['bookSynthesis']={
  'centralAxis':("Dans le livre 22, Gabriel développe la mémoire comme une réalité qui doit être digérée, purifiée, incarnée et reliée à une continuité vivante. L’eau sert de grand langage symbolique : elle représente les relations, les influences, les écritures, les résonances et le passage entre plusieurs états de l’existence. Le livre insiste sur l’individualisation par l’étude vécue, la construction de corps stables, la pureté, l’impersonnalité, la légèreté et le discernement nécessaires pour ne pas être gouverné par des impressions ou des mondes non choisis. La Tradition apparaît comme mémoire vivante et courant à transmettre, tandis que les œuvres, les alliances et les habitudes quotidiennes sont décrites comme les écritures qui façonnent la destinée. Les derniers psaumes relient cette logique à la préparation de la mort, à la vie comme clé de l’immortalité, au pouvoir créateur, à la fidélité et à la responsabilité de rendre vivant ce qui a été reçu. Les affirmations concernant l’après-mort et les mondes invisibles sont ici décrites comme doctrines internes du corpus et non comme faits extérieurs vérifiés."),
  'majorThemes':['memoire','eau','purete','tradition','individualisation','etude','corps','corps-d-eau','discernement','impersonnalite','legerete','alliances','destinee','vie','immortalite','continuite','relations','parole','oeuvre','pouvoir-createur','responsabilite','transmission']}
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print('Book 22 finalized: 26/26 deep-content-grounded analyses')
if __name__=='__main__': main()
