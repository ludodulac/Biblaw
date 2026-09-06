#!/usr/bin/env python3
"""Third close semantic pass for Raphael book 19, Psalms 114-117, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-19.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
114:{'signals':['air','souffle','pensées','influences','œuvre'], 'themes':[
 T('souffle-pur','Souffle pur','central','direct',[7,8,15,16,17],"Le souffle pur envoyé par Raphaël est présenté comme une qualité d’air et d’atmosphère capable de guider la vie, dégager les influences empoisonnées et ouvrir un espace plus serein autour de la pensée et de la destinée."),
 T('mauvaises-pensees','Mauvaises pensées','central','direct',[9,10,11,12,13,14,15,16,18],"Les mauvaises pensées ne sont pas traitées comme des idées sans conséquence : le texte les décrit comme des mondes auxquels l’homme donne force et autorité par son attention, ses validations et sa puissance créatrice."),
 T('vigilance-de-la-pensee','Vigilance de la pensée','important','direct',[9,11,13,16],"La réponse proposée n’est pas la crispation mais une vigilance douce : étudier, observer ce qui influence négativement, cesser de nourrir ces pensées et les replacer dans un cadre de discipline et d’alliance."),
 T('oeuvre-collective','Œuvre collective','important','direct',[2,3,4,5,7,8,19,20,21,22],"Le travail collectif en faveur d’une cause supérieure est présenté comme ce qui rend possible l’approche d’un autre monde. Les contributions concrètes sont décrites comme des semences dont les effets accompagnent l’être au-delà du seul présent."),
 T('air','Air','important','direct',[3,7,8,15,16,17],"L’air est à la fois atmosphère collective et milieu subtil de pensée. Le texte relie sa qualité à la possibilité de respirer, penser et recevoir des influences différentes de celles qui dominent le monde ordinaire."),
 T('immortalite','Immortalité','related','direct',[20,22],"Les efforts et contributions faits pour la Lumière sont présentés comme des semences d’immortalité qui demeurent avec l’être et peuvent ouvrir ultérieurement d’autres portes."),
]},
115:{'signals':['quatre respirations','terre','eau','air','feu'], 'themes':[
 T('quatre-respirations','Quatre respirations','central','direct',[1,2,3,7,10,20,21,22,24,29,30,31,32],"Le psaume décrit plusieurs sphères de respiration correspondant progressivement à la terre, l’eau, l’air-éther et le feu. Changer de respiration signifie élargir le monde dans lequel la conscience, la pensée et l’action peuvent vivre."),
 T('respiration-creatrice','Respiration créatrice','central','direct',[3,4,7,10,21],"La respiration est présentée comme un organe créateur reliant passé et futur, attirant des influences et rayonnant ce qui correspond à l’homme. Elle dépasse donc la seule fonction physiologique dans la logique interne du texte."),
 T('sphere-respiratoire','Sphère respiratoire','central','direct',[2,5,6,7,8,9,10],"La sphère respiratoire fixe la frontière à laquelle la pensée et la vie peuvent s’étendre. Une sphère fermée limite même les pensées élevées, tandis que son ouverture est associée à l’universel et au renouvellement."),
 T('terre-eau-air-feu','Terre, eau, air et feu','important','direct',[20,21,26,27,29,30,31],"Les quatre éléments structurent un parcours : rythmes physiques de la terre, perception magique de l’eau, compréhension universelle de l’air puis état créateur et impersonnel du feu."),
 T('pratique-et-conscience','Pratique et conscience','important','direct',[23,24,25,26,29,30,31],"Raphaël relie exercice et conscience : la discipline du corps et du souffle prépare progressivement une perception plus subtile, mais la pratique n’est complète que lorsqu’elle transforme la conscience et la manière d’agir."),
 T('pensee-et-respiration','Pensée et respiration','important','direct',[8,9,10,29],"La pensée est dite dépendante de la qualité de la respiration : sans renouvellement, elle s’asphyxie; ouverte à une autre sphère, elle peut recevoir une intelligence qui la transforme."),
]},
116:{'signals':['souffrance','éducation','centre','tâche','concentration'], 'themes':[
 T('souffrance','Souffrance','central','direct',[2,3,7,12,13],"La souffrance est présentée comme un signal indiquant une orientation ou une éducation qui éloigne de l’équilibre. Le texte demande de l’écouter comme message de redressement plutôt que de lutter contre elle sans en examiner la cause."),
 T('recentrage','Recentrage','central','direct',[4,5,6,8,9,10,11,14,15],"Le chemin proposé consiste à revenir à ce qui est vital, essentiel et réellement confié à l’homme. Se disperser dans ce qui ne le concerne pas est décrit comme une perte d’énergie, de centre et de destinée."),
 T('tache-propre','Tâche propre','central','direct',[15,16,17,18],"Chaque personne est présentée comme ayant une tâche à accomplir. La confusion naît lorsque chacun abandonne son propre travail pour s’occuper de celui des autres et donne ainsi de la force à des pensées et œuvres dont il devient responsable."),
 T('education','Éducation','important','direct',[2,3,7,11],"Une mauvaise éducation est donnée comme l’une des sources de l’enfermement et de la souffrance; la Tradition doit au contraire renvoyer l’homme vers son centre intérieur et lui apprendre à penser et agir à partir de celui-ci."),
 T('concentration','Concentration','important','direct',[4,8,9,15,18],"La concentration sur l’essentiel protège la puissance créatrice de la pensée, de la parole et de la volonté contre la dispersion provoquée par les sollicitations du monde extérieur."),
 T('equilibre-des-mondes','Équilibre des mondes','important','direct',[10,11,12,13],"Une fois établi intérieurement, l’homme est appelé à élargir son influence afin de guérir et harmoniser ce qui l’entoure; l’équilibre intérieur est ainsi posé comme condition d’une action juste sur les autres mondes."),
]},
117:{'signals':['faux savoir','vrai savoir','incarnation','pratique','corps d’immortalité'], 'themes':[
 T('faux-savoir','Faux savoir','central','direct',[1,2,3,10,11,12,13,16],"Le faux savoir est décrit comme une accumulation d’informations et d’explications qui ne transforment pas l’être. Il rassure l’intellect mais maintient des cloisons entre les mondes et peut devenir une prison plutôt qu’une libération."),
 T('vrai-savoir','Vrai savoir','central','direct',[4,5,6,7,14,17,18,19,21,22,24,26,27,28,29,30,32,33,34],"Le vrai savoir doit être vécu : l’étude intellectuelle n’est qu’une première approche qui doit descendre dans le sentiment, l’être, la pratique et l’œuvre. Sa valeur se mesure à sa capacité d’éclairer, libérer et ennoblir la vie."),
 T('incarnation-du-savoir','Incarnation du savoir','central','direct',[7,11,14,17,18,19,21,22,23,27,29,30],"Une connaissance devient réelle lorsqu’elle reçoit une âme, un corps et une action sur la terre. Le psaume demande de transformer chaque lumière reçue en force vécue plutôt que de collectionner des formulations sacrées."),
 T('corps-d-immortalite','Corps d’immortalité','important','direct',[14,18],"Le savoir vivant est présenté comme capable de toucher jusqu’au corps et de participer à la construction d’un autre corps qui respire avec l’universel et traverse l’épreuve de la mort."),
 T('pratique','Pratique','important','direct',[17,19,21,22,23,26,27,30],"La pratique est le passage obligé entre connaissance et intelligence réelle. Elle doit faire d’un principe reçu une manière de penser, sentir, agir et construire."),
 T('tradition-comme-corps-du-savoir','Tradition comme corps du savoir','important','direct',[26,28,29,30,32,33,34],"La Tradition est décrite comme le corps terrestre du savoir issu d’une intelligence supérieure. Elle doit le préserver vivant, le transmettre et permettre à de nouvelles relations et manières de vivre d’en naître."),
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
