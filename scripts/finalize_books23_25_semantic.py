#!/usr/bin/env python3
"""Strict final semantic gate for books 23-25."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BOOKS=ROOT/'data/thematic-index/books'; CORPUS=ROOT/'data/corpus/books'
EXPECTED={23:range(128,154),24:range(130,156),25:range(165,191)}
GENERIC=('Le psaume développe de façon répétée','Le thème «')
AXES={
23:"La pensée créatrice relie l’éveil de la pensée à la maîtrise, au discernement et à sa traduction en parole, en acte et en œuvre. Le livre insiste sur la nécessité de donner un corps stable à l’intelligence plutôt que de demeurer dans l’abstraction, et traite les mondes subtils selon la cosmologie propre au corpus.",
24:"L’androgynie articule harmonie, équilibre et pouvoir créateur : l’être humain est appelé à unir les polarités et les niveaux de son existence afin que pensée, sentiment, volonté et acte participent à une œuvre stable. La subtilité y désigne une capacité d’accord et de médiation qui doit finalement prendre corps sur la terre.",
25:"Les clés de la maîtrise présentent la maîtrise comme une éducation intégrale de la parole, de la pensée, des sentiments, de la volonté et des actes. Vérité, discernement, responsabilité et fidélité à l’œuvre structurent un chemin où la puissance n’est légitime que lorsqu’elle devient consciente, cohérente et créatrice de vie selon l’enseignement du corpus."
}
def finalize(book):
 p=BOOKS/f'book-{book:02d}.json'; d=json.loads(p.read_text(encoding='utf-8')); aa=d.get('psalmAnalyses',[]); nums=[a['number'] for a in aa]; exp=list(EXPECTED[book])
 if nums!=exp: raise ValueError(f'book {book}: expected {exp[0]}-{exp[-1]}, got {nums}')
 counts=Counter(); labels={}
 for a in aa:
  if a.get('semanticDepth')!='deep-content-grounded': raise ValueError(f'book {book} psalm {a["number"]}: not deep')
  corpus=json.loads((CORPUS/f'book-{book:02d}'/f'psalm-{a["number"]:03d}.json').read_text(encoding='utf-8')); valid={v['number'] for v in corpus.get('verses',[])}
  if not valid: raise ValueError(f'book {book} psalm {a["number"]}: empty corpus')
  for t in a.get('themes',[]):
   teach=(t.get('teaching') or '').strip()
   if not teach or teach.startswith(GENERIC): raise ValueError(f'book {book} psalm {a["number"]}: generic/empty teaching {t.get("themeId")}')
   refs=t.get('verseNumbers',[])
   if not refs or any(n not in valid for n in refs): raise ValueError(f'book {book} psalm {a["number"]}: invalid evidence {t.get("themeId")} {refs}')
   counts[t['themeId']]+=1; labels[t['themeId']]=t.get('label',t['themeId'])
 majors=[k for k,_ in counts.most_common(20)]
 d['bookSynthesis']={'centralAxis':AXES[book],'majorThemes':majors}
 m=d.setdefault('method',{}); m['semanticPass']='deep-content-grounded-complete'; m['deepPsalmCount']=len(aa); m['contentGrounding']='complete'; m['status']='editorial-indexing-complete'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f'book {book}: FINAL deep {len(aa)}/{len(exp)}')
def main():
 for b in (23,24,25): finalize(b)
if __name__=='__main__': main()
