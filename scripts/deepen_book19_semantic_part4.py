#!/usr/bin/env python3
"""Fourth close semantic pass for Raphael book 19: Psalm 109 and Psalms 118-120."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-19.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
109:{'signals':['vérité','trois centres','responsabilité','engagement','civilisation'], 'themes':[
 T('verite','Vérité','central','direct',[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,26,27,36],"La vérité n’est pas définie comme le simple fait d’exprimer son opinion : elle apparaît lorsque pensée, sentiment et action sont équilibrés et unis à une réalité plus universelle, puis incarnés jusque dans les œuvres."),
 T('trois-centres-d-intelligence','Trois centres d’intelligence','central','direct',[9,10,12,16,17,19,20,21,22,36],"Le psaume distingue pensée, sentiment et action comme trois centres qui doivent être harmonisés. Un engagement ou une fonction n’est vrai que si ces trois dimensions portent la même orientation."),
 T('responsabilite','Responsabilité','central','direct',[18,20,21,22,23,25,33,34,35,36,40,41,42],"La responsabilité commence après l’engagement : les personnes qui acceptent une fonction doivent en incarner le principe et assumer les conséquences de leurs pensées, paroles, états d’âme et actes sur l’œuvre collective."),
 T('fonction-sacree','Fonction sacrée','important','direct',[18,19,20,21,25,28,35],"Les fonctions de prêtre, pilier, vestale ou dirigeant sont décrites comme plus grandes que les personnes qui les portent. Elles exigent une cohérence intérieure et une organisation capables d’ennoblir la fonction au lieu de l’utiliser comme façade."),
 T('mensonge','Mensonge','important','direct',[1,2,3,13,17,19,23,26],"Le mensonge est associé à la séparation, au faux-semblant et à l’action sans connaissance réelle. Il nourrit, selon le texte, des influences qui enferment l’homme et mettent en péril la manifestation concrète de l’œuvre."),
 T('nouvelle-civilisation','Nouvelle civilisation','important','direct',[27,31,32,33,34,35,36,37],"La nouvelle civilisation est présentée comme une œuvre que le monde divin propose mais que les hommes doivent réaliser. Sa stabilité dépend de responsables clairs, d’une organisation solide et de rôles tenus fidèlement."),
]},
118:{'signals':['achèvement','œuvre','unification','séparation','collectivité'], 'themes':[
 T('achevement','Achèvement','central','direct',[13,14,15,18,21,22,23,24,44,45,46,47],"Le secret pratique du psaume est d’aller jusqu’au bout de ce qui a été entrepris. Achever une œuvre permet la rencontre, constitue une force et empêche les mondes engagés dans le travail de rester bloqués dans un état inachevé."),
 T('unification','Unification','central','direct',[1,2,3,4,5,14,18,20,22,27,28,29,31,32,33],"La vie est définie comme unification et la séparation comme mort. L’accomplissement d’œuvres, l’union des personnes et l’étude collective doivent replacer l’individu dans un tout plus vaste au lieu de renforcer son isolement."),
 T('oeuvres-comme-organes','Œuvres comme organes','important','direct',[18,22,24,25,47],"Les œuvres réalisées sont décrites comme formant autour de l’homme des écritures, sceaux ou organes qui deviennent un langage dans d’autres mondes. La réalisation concrète précède ainsi toute prétention à une communication supérieure."),
 T('separation','Séparation','important','direct',[2,3,4,6,11,12,15,16],"La séparation est associée à la peur de la mort, à l’exploitation et à l’illusion d’une existence autosuffisante. Le texte présente cette isolation comme l’obstacle principal à la rencontre avec l’autre et avec la totalité de son propre être."),
 T('oeuvre-collective','Œuvre collective','important','direct',[26,27,28,29,31,32,33],"Face à une œuvre collective de destruction décrite dans le texte, l’alternative proposée passe par une autre œuvre collective : union, étude commune, organisation et mise en commun des victoires."),
]},
119:{'signals':['hiérarchie','Alliance','corps collectif','soutien','juste place'], 'themes':[
 T('hierarchie-de-la-lumiere','Hiérarchie de la Lumière','central','direct',[2,4,7,15,16,23,24,25,26,27,34],"La hiérarchie est présentée comme une organisation fonctionnelle comparable à un corps : certaines personnes portent des tâches spécifiques liées à l’Alliance, tandis que les autres les soutiennent afin que la fonction puisse bénéficier à l’ensemble."),
 T('juste-place','Juste place','central','direct',[1,2,3,4,7,13,17,18,23,26,27,29],"Le psaume demande à chacun de trouver sa place réelle plutôt que de vouloir accomplir indistinctement toutes les fonctions. La vie terrestre, les œuvres concrètes et le soutien mutuel sont présentés comme des contributions légitimes au même corps collectif."),
 T('corps-collectif','Corps collectif','central','direct',[7,13,17,18,21,23,26,27,29,30,32,34],"Le chemin vers un monde supérieur est décrit comme collectif. La Nation et la Tradition doivent former un corps dans lequel les fonctions sont différenciées mais interdépendantes, et où les acquis de certains peuvent devenir une bénédiction pour tous."),
 T('soutien-mutuel','Soutien mutuel','important','direct',[4,7,8,15,16,19,24,25,27,34],"Le soutien mutuel consiste à créer des conditions de force, de pureté et de disponibilité pour ceux qui portent une fonction collective, tout en construisant soi-même une vie juste et des œuvres physiques utiles."),
 T('anti-spiritualite-abstraite','Refus de la spiritualité abstraite','important','direct',[1,5,6,7,8,9,10,11,12,14,17,28],"Le texte critique la conquête individuelle et conceptuelle des mondes supérieurs. Il renvoie au monde physique, à une vie bonne et aux réalisations concrètes comme base avant toute approche d’une fonction plus haute."),
 T('alliance','Alliance','important','direct',[4,13,15,20,21,23,26,27,29,30,31,34],"L’Alliance suit des conditions et des rôles précis : elle est entretenue par un corps organisé et non par la seule aspiration individuelle. Sa manifestation dépend donc d’une structure et d’un soutien conformes à l’Enseignement."),
]},
120:{'signals':['rites méditatifs','stabilité','étude','dévotion','réalisation'], 'themes':[
 T('rites-meditatifs','Rites méditatifs','central','direct',[9,10,11,12],"Les rites méditatifs associent position du corps, méditation, pensée, sentiment et intention afin d’ouvrir la vie intérieure et de donner au travail une dimension collective. Ils sont présentés comme un moyen de centrer l’être plutôt que comme une formalité extérieure."),
 T('stabilite-interieure','Stabilité intérieure','central','direct',[3,4,5,6,11,12],"Étude, méditation et concentration doivent stabiliser le corps et les émotions afin que les remarques, doutes et influences extérieures ne détruisent pas la capacité d’agir et de créer."),
 T('etude-devotion-rite-oeuvre','Étude, dévotion, rite et œuvre','central','direct',[3,6,7,8,9,10,12,13],"Le psaume articule quatre pratiques complémentaires : l’étude structure la pensée, la dévotion nourrit la vie intérieure, le rite ouvre à une dimension collective et l’œuvre impose concrètement ce qui a été reconnu comme juste."),
 T('affirmation-juste','Affirmation juste','important','direct',[1,2,3,4,11,13],"Prendre sa place ne signifie pas dominer arbitrairement mais disposer d’une vie intérieure assez structurée pour agir conformément à ce qui est reconnu comme vrai sans être constamment renversé par les influences extérieures."),
 T('organisation-des-oeuvres','Organisation des œuvres','important','direct',[14],"Le désordre dans les activités est explicitement critiqué : multiplier les projets sans maîtrise ni préparation empêche de construire les étapes nécessaires à un avenir réussi."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; order={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in order else 1,order.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses'])
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 19 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
