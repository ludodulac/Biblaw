#!/usr/bin/env python3
"""Final close semantic pass for Gabriel book 22, Psalms 162-163, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-22.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
162:{'signals':['pouvoir créateur','écriture','destinée','fidélité','incarnation'], 'themes':[
 T('pouvoir-createur','Pouvoir créateur','central','direct',[2,3,4,5,6,8,9,11,19,20,21,22,23,24,26],"Le pouvoir créateur est présenté comme la capacité de donner une écriture à la destinée en accordant pensée, sentiment, volonté et vie concrète à une intelligence choisie. Il ne s’agit pas seulement de souhaiter mais de devenir apte à porter ce qui doit être réalisé."),
 T('ecrire-sa-destinee','Écrire sa destinée','central','symbolic',[5,8,9,11,12,13,14,15,16,17,19,20,21,22,23,24,25,26],"Écrire la destinée signifie déposer une orientation dans les mondes subtils puis lui donner le temps, la fidélité et le corps nécessaires pour toucher le plan physique. Les changements impulsifs d’orientation sont décrits comme des interférences qui empêchent l’écriture d’aboutir."),
 T('fidelite-et-continuite','Fidélité et continuité','central','direct',[5,6,12,13,14,15,17,20,22,23,25],"Toute réalisation demande continuité de conscience et d’action. Le texte insiste sur la permanence, la patience et l’accord durable entre ce qui est demandé et la manière de vivre, plutôt que sur une volonté passagère qui change dès qu’elle n’obtient pas de résultat immédiat."),
 T('purete-et-authenticite','Pureté et authenticité','important','direct',[3,4,10,21,22,25],"Le pouvoir créateur doit être exercé depuis une vie assez claire pour éviter la contradiction entre demande, identité et acte. Pureté et authenticité concernent ici l’accord avec soi-même et l’équilibre des trois mondes de la pensée, du sentiment et de la volonté."),
 T('incarnation-de-l-ecriture','Incarnation de l’écriture','important','direct',[8,15,20,21,22,23,24,26],"Une écriture ne devient réelle que si l’homme est capable de l’incarner et de l’assumer sur la terre visible. L’organisation de la vie, la discipline et l’unité avec l’intelligence choisie forment le corps par lequel elle peut se manifester."),
 T('temps-comme-allie','Temps comme allié','important','direct',[13,14,17,18,19],"Le temps n’est pas présenté comme obstacle mais comme allié de la réalisation. Ce qui a été écrit demande maturation et préparation; l’impatience devient un facteur de rupture lorsque l’homme abandonne avant d’être capable de porter ce qu’il a demandé."),
]},
163:{'signals':['tout est vivant','transformation','responsabilité','prendre soin','force intérieure'], 'themes':[
 T('tout-est-vivant','Tout est vivant','central','direct',[6,9,15,16,17,18,19,20,21],"Le psaume demande de considérer événements, relations, capacités et êtres comme des réalités vivantes confiées à la responsabilité humaine. Cette perspective déplace l’attention de la plainte vers le soin, la transformation et la part concrète que chacun peut accomplir."),
 T('transformation-de-la-matiere','Transformation de la matière','central','symbolic',[7,8,9,10,11,14],"Toute situation difficile est comparée à une matière première qui doit être transformée en or par la sagesse. Le texte ne demande pas de multiplier le mal mais de travailler ce qui arrive afin qu’une blessure ou une opposition cesse de gouverner la vie."),
 T('responsabilite-de-sa-part','Responsabilité de sa part','central','direct',[3,4,6,7,8,15,16,17,21,22,23,25,27],"Le monde supérieur n’est pas présenté comme chargé d’accomplir le travail humain. L’homme doit organiser sa vie, clarifier ses influences, prendre soin de ce qui lui est confié et accomplir sa part au lieu de placer la cause de toute difficulté uniquement à l’extérieur."),
 T('prendre-soin','Prendre soin','important','direct',[15,16,17,18,19,20,21],"Prendre soin s’étend aux dons, aux proches, aux règnes de la Mère, aux pensées nobles et aux alliances. Le soin est la manière concrète de reconnaître qu’une chose reçue appartient à une relation plus vaste et ne doit pas être abandonnée à la négligence."),
 T('force-interieure','Force intérieure','important','direct',[6,7,8,9,10,24,25,26,27],"La force intérieure apparaît lorsque l’homme cesse d’être dirigé par ses blessures et travaille ce qui l’affaiblit. Le texte associe cette force à la prévoyance, à l’ordre et à la capacité d’empêcher certaines influences de s’installer avant qu’elles ne deviennent écrasantes."),
 T('union-et-organisation','Union et organisation','important','direct',[2,3,4,5,21,23,25],"La continuité de la Tradition et de l’œuvre dépend d’une participation organisée. S’unir et purifier les atmosphères sont présentés comme des moyens concrets de rendre de nouveau possible une coopération avec les mondes décrits par le texte."),
]}}
def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); m=d.setdefault('method',{}); m['semanticPass']='deepening-in-progress'; m['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 22 deep total={m['deepPsalmCount']}")
if __name__=='__main__': main()
