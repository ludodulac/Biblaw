#!/usr/bin/env python3
"""Fourth close semantic pass for Ouriel book 20, Psalms 116-119, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-20.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
116:{'signals':['argent','échange harmonieux','fructification','terre','réalisation'], 'themes':[
 T('energie-de-l-argent','Énergie de l’argent','central','direct',[7,8,23],"L’argent est décrit comme une énergie dont la fonction originelle serait l’échange harmonieux, le respect et la fructification. Le psaume oppose cette fonction à son accaparement et à son usage comme instrument d’asservissement."),
 T('fructification','Fructification','central','direct',[8,10,12,13,14,22,23],"La terre reçue doit faire fructifier ce qui est bon et juste. Le texte demande d’enrichir d’abord spirituellement ce qui mérite de vivre puis de lui donner une forme physique, afin que la valeur puisse circuler et devenir œuvre."),
 T('accomplissement','Accomplissement','important','direct',[4,5,6,10,19,23,27],"Ouriel est présenté comme la conclusion des mondes et l’accomplissement des œuvres : ce qui lui est confié reçoit une forme et une existence. D’où l’exigence de présenter une semence claire et suffisamment organisée avant sa matérialisation."),
 T('responsabilite-creatrice','Responsabilité créatrice','important','direct',[10,11,12,13,15,16,18,20],"La phase de réalisations plus concrètes augmente la responsabilité : ce qui est mis au monde est considéré comme le prolongement de choix, associations et compréhensions qu’il faut clarifier avant qu’ils ne prennent racine."),
 T('soutien-et-capital-collectif','Soutien et capital collectif','important','direct',[9,19,22,25,27],"Le soutien, l’énergie et les bonnes pensées sont traités comme un capital qui peut fortifier une œuvre collective. Les trésors reçus ne doivent pas être affaiblis mais appréciés, développés et dirigés vers une forme plus juste."),
 T('echange-harmonieux','Échange harmonieux','important','direct',[8,14,23],"L’échange harmonieux relie richesse, gratitude et réciprocité. Il ne s’agit pas seulement d’accumuler mais de faire circuler une énergie qui développe plusieurs êtres et mondes au lieu d’en priver certains."),
]},
117:{'signals':['porte de Lumière','responsabilité','corps','impersonnalité','Bien commun'], 'themes':[
 T('porte-de-la-lumiere','Porte de la Lumière','central','symbolic',[1,2,3,4,8,11,25,26,27],"L’Enseignement ouvre une porte, mais la franchir exige davantage que l’imitation ou la bonne volonté. L’homme doit se former un corps, comprendre ce qu’il veut et convertir l’instruction reçue en vie consciente et responsable."),
 T('responsabilite-et-libre-creation','Responsabilité et libre création','central','direct',[4,5,8,9,10,11],"Le monde divin n’est pas présenté comme un substitut à l’homme. Celui-ci doit prendre sa destinée en mains, rencontrer les obstacles et devenir créateur d’une tâche choisie librement qui contribue au Bien commun."),
 T('corps-de-sagesse','Corps de sagesse','central','direct',[5,6,8,25,26,34],"Recevoir un enseignement signifie se constituer un corps à partir de ce qu’il transmet. Étude, dévotion, rite et œuvre forment les quatre appuis par lesquels la sagesse doit devenir perception, service et action concrète."),
 T('impersonnalite','Impersonnalité','important','direct',[28,29,30,31,33],"L’étude véritable exige de sortir momentanément de son propre point de vue pour comprendre l’autre selon ses besoins. L’impersonnalité est opposée à l’aide projetée, aux concepts préconçus et à la volonté d’imposer son propre bien."),
 T('langage-universel','Langage universel','important','direct',[24,25,33,34],"Le langage universel est la capacité à créer un espace commun où les différences et les règnes peuvent se rencontrer sans domination. La Ronde des Archanges est présentée dans le texte comme une structure destinée à porter cet espace."),
 T('verite-comme-remede','Vérité comme remède','important','direct',[30,31],"Aider ne consiste pas à appliquer sa propre vision du bien : le texte place la vérité au-dessus des préférences personnelles et demande d’apprendre à rencontrer l’autre hors de ses catégories habituelles."),
]},
118:{'signals':['souplesse','discipline','invisible','patience','confiance'], 'themes':[
 T('souplesse','Souplesse','central','direct',[1,2,3,4,5,8,10,12,15,20,27,29,33],"La souplesse est la capacité à rester en mouvement avec les forces présentes sans se figer ni perdre son axe. Elle permet l’échange, l’adaptation et l’accueil d’intelligences plus vastes tout en conservant une stabilité comparable à celle de la pierre."),
 T('discipline-et-souplesse','Discipline et souplesse','central','direct',[12,13,14,15,27],"La discipline prépare la terre mais ne doit pas devenir rigidité. Le texte cherche un équilibre où la structure rend possible la vie et où la souplesse empêche la pratique de se transformer en mécanique coupée de l’invisible."),
 T('participation-de-l-invisible','Participation de l’invisible','important','direct',[6,7,8,9,10,11,14,17,18,19,34,41,42],"Toute œuvre est présentée comme le résultat d’une multitude visible et invisible. Réussir suppose donc de reconnaître les mondes qui participent déjà à la vie et de les associer consciemment plutôt que de croire à une volonté humaine isolée."),
 T('peur-et-doute','Peur et doute','important','direct',[21,22,23,24,25,26],"La peur est décrite comme une association qui coupe la confiance et alimente le doute. La réponse proposée passe par l’étude des lois, la discipline, la souplesse et une alliance jugée plus stable."),
 T('patience','Patience','important','direct',[29,30,31,32,33,38,40],"La patience permet de ne pas forcer une œuvre dans le calendrier de l’homme. Accepter les retournements et saisir le moment propice sont présentés comme plus sages que vouloir imposer à tout prix le scénario prévu."),
 T('oeuvre-durable','Œuvre durable','important','direct',[17,18,19,34,36,37,38,39],"Une œuvre durable est celle qui s’unit à une volonté plus vaste que le désir individuel. Le texte oppose les réalisations séparées et soumises au temps à ce qui s’inscrit dans le Bien et peut continuer au-delà de l’impulsion personnelle."),
]},
119:{'signals':['écologie','dignité des règnes','fausse lumière','renaissance','réalisation'], 'themes':[
 T('ecologie-spirituelle','Écologie spirituelle','central','direct',[17,18,19,20,21,23,24,26,28,29,31,32],"Le psaume critique une écologie motivée uniquement par la survie humaine et demande de rendre dignité, place et langage aux minéraux, végétaux et animaux. La pollution physique est présentée comme le résultat d’une orientation et d’une intelligence plus profondes."),
 T('dignite-des-regnes','Dignité des règnes','central','direct',[18,19,20,21,26,27,32],"Chaque règne doit retrouver une mission et une dignité propres au lieu d’être réduit à une ressource. L’homme est appelé à restaurer un dialogue avec eux et à reconnaître leurs qualités comme des dimensions également présentes en lui."),
 T('fausse-lumiere','Fausse lumière','central','direct',[16,19,20,21,25,27,28,29,34,35,36,39],"Le texte désigne une intelligence « faussement lumineuse » comme source d’une autonomie humaine qui exploite et coupe des autres règnes. S’en libérer demande de reconnaître ses associations plutôt que d’utiliser indistinctement le mot Lumière."),
 T('realisation-concrete','Réalisation concrète','important','direct',[2,4,5,6,8,9,23,24,26,31,32],"Ouriel privilégie l’acte qui touche la terre : la Lumière doit apparaître dans des œuvres, des comportements et une nouvelle façon d’être, non rester dans des concepts écologiques ou spirituels."),
 T('renaissance-par-la-mere','Renaissance par la Mère','important','direct',[34,35,40,41,42,43,44,45],"La renaissance est décrite comme un abandon de l’ancien corps d’identités et d’influences afin d’être reformé dans le monde de la Mère. Les racines, le Nom et la vie dans les règnes sont privilégiés par rapport aux concepts de la tête."),
 T('unisson-et-corps-collectif','Unisson et corps collectif','important','direct',[31,33,38,42,43,45,46],"La reconstruction ne peut pas être purement individuelle : le texte lie le nouveau corps à une Tradition, une Nation et un unisson capables de rendre la Lumière concrète pour le bien de plusieurs mondes."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 20 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
