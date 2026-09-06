#!/usr/bin/env python3
"""Fifth close semantic pass for Raphael book 19: Psalm 121."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-19.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
NEW=[
 T('capital-d-eternite','Capital d’éternité','central','direct',[5,6,7,8,12,15,18,19,20,21,23,24,28,29],"Le « capital d’éternité » désigne les expériences, œuvres et états de conscience qui ne sont pas perdus mais deviennent une base pour une évolution continue. Le texte l’oppose à un capital de mort et de recyclage constitué par ce qui enferme ou reste inachevé."),
 T('continuite-de-conscience','Continuité de conscience','central','direct',[2,5,6,7,14,15,19,20],"L’immortalité commence par la conscience et se caractérise par une continuité où les expériences acquises servent d’appui à l’étape suivante, au lieu d’un recommencement cyclique."),
 T('deux-capitaux','Deux capitaux','central','direct',[15,16,17,18,19,20,21],"Chaque être est présenté comme accumulant simultanément un capital d’immortalité et un capital de mort. Les expériences qui éclairent, libèrent et rendent sage augmentent le premier; celles qui enferment et restent non résolues renforcent le second."),
 T('corps-de-sagesse','Corps de sagesse','important','direct',[14,18,19,20],"Le corps de sagesse est la structure construite par l’Enseignement, la pratique et la résolution des points de souffrance; il doit offrir stabilité et continuité à ce qui a été réellement compris et vécu."),
 T('oeuvre-d-immortalite','Œuvre d’immortalité','important','direct',[7,13,22,23,24,25,27,28,29],"Une œuvre d’immortalité est décrite comme une œuvre conduite jusqu’à son achèvement, suffisamment constituée pour devenir une réalité vivante qui ne s’éteint pas avec l’effort initial."),
 T('reincarnation-et-recyclage','Réincarnation et recyclage','important','direct',[1,2,3,9,16,17,18,19,26],"Le texte associe la réincarnation au monde du recyclage et au recommencement d’expériences non conduites à la sagesse, tandis que l’autre orientation est décrite comme évolution continue."),
]
def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); a=next(x for x in d['psalmAnalyses'] if x['number']==121); a['titleSignals']=['capital d’éternité','continuité','immortalité','œuvre','corps de sagesse']; a['themes']=merge(a.get('themes',[]),NEW); a['semanticDepth']='deep-content-grounded'; d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(x.get('semanticDepth')=='deep-content-grounded' for x in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 19 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
