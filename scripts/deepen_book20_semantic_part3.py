#!/usr/bin/env python3
"""Third close semantic pass for Ouriel book 20, Psalms 112-115, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-20.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
112:{'signals':['communauté d’âmes','terre et ciel communs','Bien commun','corps collectif','Alliance'], 'themes':[
 T('communaute-d-ames','Communauté d’âmes','central','direct',[2,18,19,20,21,24,27,30,33,35,46,50,51,52,53,56],"Le psaume décrit la communauté comme le corps nécessaire à la manifestation de la Lumière : des individualités différentes doivent partager une terre, un ciel, une compréhension et un but communs sans perdre leurs capacités propres."),
 T('terre-et-ciel-communs','Terre et ciel communs','central','symbolic',[1,19,20,21,22,27,33,35,45,50,52,56,59],"La terre commune représente l’Enseignement et le ciel commun sa compréhension partagée. L’union du haut et du bas devient possible lorsque les membres d’un peuple disposent de ces repères communs tout en conservant leur diversité."),
 T('bien-commun','Bien commun','central','direct',[2,26,30,32,46,56],"Les capacités individuelles sont légitimes lorsqu’elles servent l’ensemble. Le texte oppose la supériorité qui écrase à une diversité de talents mise au service d’un Bien commun et d’une œuvre que personne ne peut réaliser seul."),
 T('corps-collectif','Corps collectif','important','direct',[18,24,30,35,53],"La Lumière est dite incapable de s’incarner dans un individu isolé : le corps collectif fournit la coupe et le milieu où une intelligence supérieure peut recevoir une forme terrestre et toucher plus largement le monde."),
 T('harmonie-dans-la-diversite','Harmonie dans la diversité','important','direct',[21,32,33,35,46,47,50,51,52,56],"L’unité ne signifie pas uniformité. Chacun doit développer son rayon et sa tâche, tandis que l’Enseignement et la compréhension commune maintiennent les voies multiples dans un plan global sans conflit de domination."),
 T('alliance-de-lumiere','Alliance de Lumière','important','direct',[1,9,17,22,53,57,58],"L’Alliance relie la fidélité de la Tradition, les règnes, les Sceaux et la communauté humaine. Sa continuité dépend d’un peuple suffisamment uni et organisé pour garder une place terrestre à la Lumière."),
]},
113:{'signals':['trois clés','dettes','non-association','préserver le Bien','immortalité'], 'themes':[
 T('trois-cles','Trois clés','central','direct',[7,18,22,31],"Le psaume résume l’approche de la terre promise en trois règles : régler les dettes anciennes, ne pas en engendrer de nouvelles par des associations imprudentes, puis préserver et entretenir le Bien déjà reçu."),
 T('dettes-et-liberation','Dettes et libération','central','direct',[6,7,8,9,15,16,17,20,31],"Les dettes représentent les liens et conséquences qui retiennent la vie en arrière. Elles doivent être réglées par un travail conscient, soutenu par étude, dévotion, rites et œuvres, plutôt qu’être supposées disparaître avec un nouveau départ."),
 T('discernement-des-associations','Discernement des associations','central','direct',[18,19,20,25,27,33,34],"Une association engage la vie dans la durée. Le texte demande de réfléchir avant de se lier à un monde, car une fois le fil tissé il faut souvent parcourir jusqu’au bout les conséquences de l’engagement."),
 T('preserver-le-bien','Préserver le Bien','important','direct',[22,23,24,25,26,28,29,30,31,33],"La troisième clé consiste à reconnaître le précieux déjà présent — famille, belles pensées, tradition, harmonie — et à ne pas l’abandonner sous prétexte de chercher une autre vie. Le Bien doit être protégé, cultivé et rendu durable."),
 T('corps-d-immortalite','Corps d’immortalité','important','direct',[3,9,10,11,15,30,31],"L’immortalité est reliée à un corps rendu léger et libre par l’acquittement des dettes, la maîtrise des associations et l’incarnation de l’Enseignement dans la pensée, le cœur, la volonté et l’œuvre."),
 T('engagement','Engagement','important','direct',[19,25,30,33,34],"L’engagement doit être précédé d’étude et de comparaison. La fidélité au chemin suppose d’accepter qu’un choix crée une relation réelle et demande ensuite d’aller jusqu’au bout plutôt que de changer impulsivement de direction."),
]},
114:{'signals':['réussite','lois','structure','langage universel','alliances'], 'themes':[
 T('secret-de-la-reussite','Secret de la réussite','central','direct',[1,2,3,5,6,7,9,10,11,19,20],"La réussite est attribuée moins à l’intensité de la volonté individuelle qu’à la conformité aux lois, à la préparation des conditions et à la capacité de réunir les intelligences et formes de vie nécessaires à une œuvre."),
 T('structure-et-corps','Structure et corps','central','direct',[6,7,19,20],"Une œuvre doit recevoir un corps, une organisation et un monde capables d’accueillir l’esprit qui veut s’y manifester. Une idée sans structure ou dont des éléments manquent perd sa force avant d’aboutir."),
 T('langage-universel','Langage universel','central','direct',[10,15,16,17,18,19,23],"Le langage universel consiste à prendre en compte les règnes, éléments, hiérarchies et intérêts qui participent à la vie du projet. La volonté du Père n’est pas réduite au point de vue humain mais cherchée dans l’accord d’un ensemble plus vaste."),
 T('alliances','Alliances','important','direct',[7,9,10,11,18,19],"La réussite suppose des alliances parce qu’aucune œuvre ne vit durablement si elle ne trouve de place que dans la volonté d’un seul. Plusieurs mondes doivent pouvoir reconnaître un intérêt, une harmonie ou une fonction dans le projet."),
 T('education','Éducation','important','direct',[13,14,15],"L’éducation prépare le terrain de la réussite : elle apprend à sortir du seul monde humain et à examiner une œuvre depuis plusieurs points de vue avant que les erreurs ne deviennent coûteuses à réparer."),
 T('intelligence-comme-accord','Intelligence comme accord','important','direct',[17,19,20,23],"L’intelligence n’est pas définie seulement comme compréhension mais aussi comme communication, association et circulation. Elle devient l’énergie qui permet à une œuvre de durer sans rupture entre ses différentes étapes."),
]},
115:{'signals':['se connaître','actes','œuvres','observation','réel'], 'themes':[
 T('connaissance-de-soi','Connaissance de soi','central','direct',[1,2,3,4,6,7,8,10,11,12,20,21],"Le psaume demande de chercher son identité dans ce qui est réellement manifesté plutôt que dans les images idéalisées. Corps, actes, relations et œuvres deviennent le livre concret où l’homme peut observer ce qu’il porte."),
 T('actes-comme-revelateur','Actes comme révélateur','central','direct',[2,3,4,6,7,10,11,12,13,18,19,20],"Les actes sont présentés comme le critère qui révèle pensée, sentiment, volonté et degré d’intelligence. Ce que l’homme met au monde dans le concret montre davantage qui il est que ses souhaits ou discours intérieurs."),
 T('observation-de-la-vie','Observation de la vie','important','direct',[8,9,10,13,18,20,21],"L’observation quotidienne permet de lire la qualité des sentiments, de la pensée et de la volonté dans leurs effets : paix ou conflit dans les relations, cohérence des œuvres, libération ou domination des autres."),
 T('volonte-qui-libere','Volonté qui libère','important','direct',[18,19,20],"Une volonté équilibrée ne cherche pas à occuper toute la place : elle donne aux autres des conditions pour grandir et devenir meilleurs. L’exploitation, l’écrasement et le besoin de contrôle sont au contraire lus comme signes de faiblesse."),
 T('reel-contre-faux-semblant','Réel contre faux-semblant','important','direct',[2,7,21,24,25],"Le chemin vers la vérité passe par le réel et non par le besoin de paraître ou de séduire. Les mondes spirituels peuvent eux-mêmes devenir des illusions s’ils servent à fabriquer une image flatteuse qui n’est pas confirmée par la vie."),
 T('oeuvre-et-continuite','Œuvre et continuité','important','direct',[13,22,26,27,28],"Une œuvre reliée à un monde supérieur est présentée comme pouvant conserver son capital et être reprise jusqu’à la perfection, tandis qu’une œuvre dédiée à la reconnaissance du monde humain reste dépendante de ses intérêts et de ses retournements."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 20 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
