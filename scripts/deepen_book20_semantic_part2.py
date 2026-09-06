#!/usr/bin/env python3
"""Second close semantic pass for Ouriel book 20, Psalms 108-111, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-20.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
108:{'signals':['terre intérieure','jardinier','héritage','racines','offrande'], 'themes':[
 T('terre-interieure','Terre intérieure','central','symbolic',[1,2,5,6,7,8,9,10,11,13,14,15,17,18,19,20,22,27,28],"Le corps et la vie sont comparés à une terre reçue en héritage. L’homme doit la cultiver, protéger sa richesse, enlever les racines qui l’envahissent et organiser tout l’espace pour que ce qu’il choisit de faire vivre puisse réellement fructifier."),
 T('jardinier','Jardinier','central','symbolic',[5,8,9,10,11,17,18,19],"Devenir jardinier de sa terre signifie ne plus se contenter de se plaindre des conditions : il faut discerner ce qui pousse, agir jusque sur les racines invisibles et occuper la terre par des semences choisies plutôt que la laisser à l’abandon."),
 T('heritage','Héritage','central','direct',[1,3,7,14,17,22],"L’héritage comprend le corps, la lignée et un potentiel à faire fructifier. La responsabilité envers cet héritage relie les ancêtres aux générations futures et interdit de le traiter comme une propriété sans devoir."),
 T('racines-et-influences','Racines et influences','important','symbolic',[6,8,9,10,13,15,18,19,21,28],"Les influences indésirables sont figurées par des mauvaises herbes dont les racines peuvent rester invisibles. Le texte demande une action en profondeur et une vigilance continue plutôt qu’un nettoyage seulement apparent."),
 T('ordre-et-maitrise','Ordre et maîtrise','important','direct',[18,19,20,22],"Une terre protégée n’est pas laissée vide : elle est entièrement ordonnée et placée dans une structure de maîtrise. L’organisation du corps et de la vie sert à empêcher que des influences étrangères s’installent dans les espaces non habités."),
 T('offrande-et-reciprocite','Offrande et réciprocité','important','direct',[22,23,24,25,26],"La prospérité de la terre intérieure doit devenir nourriture pour plusieurs mondes. L’offrande exprime une réciprocité : l’homme partage ce qu’il a fait fructifier avec la terre et le ciel au lieu de vivre exclusivement pour lui-même."),
]},
109:{'signals':['œuvre quotidienne','écriture du futur','Alliance','qualité intérieure','réalisation'], 'themes':[
 T('oeuvre-quotidienne','Œuvre quotidienne','central','direct',[1,2,3,4,5,6,7,8,10,11,13,14,15,16,18,19,20,21,22,23],"Le psaume demande qu’un acte ou une œuvre soit posé chaque jour pour écrire concrètement le monde dans lequel l’homme veut vivre. Cette œuvre doit être reliée à une intelligence, une organisation et une alliance plutôt qu’être un geste isolé."),
 T('ecriture-du-futur','Écriture du futur','central','symbolic',[2,3,9,13,18,21,22],"Les actes quotidiens sont décrits comme des écritures déposées dans la terre : ils ensemencent le futur. Le contenu intérieur de l’acte — vertu, peur, irritation, pureté ou confusion — est présenté comme faisant partie de ce qui sera ensuite récolté."),
 T('qualite-de-l-oeuvre','Qualité de l’œuvre','central','direct',[5,6,7,9,10,11,12,19],"L’œuvre ne se définit pas seulement par son objectif : calme, pureté, authenticité, vertu et état d’âme participent à sa constitution. Le texte avertit qu’une œuvre peut incorporer les contre-vertus présentes au moment où elle est accomplie."),
 T('alliance','Alliance','important','direct',[4,8,12,14,15,22],"L’Alliance fournit le milieu qui relie étude, méditation, rites et réalisation à une âme collective de Lumière. Elle est présentée comme une condition pour que l’œuvre individuelle participe à une réalité plus vaste."),
 T('etude-comme-oeuvre','Étude comme œuvre','important','direct',[3,4,14],"L’étude peut devenir une œuvre quotidienne lorsqu’elle relie des personnes dans une même orientation et s’inscrit dans un monde, une vision et une volonté agissants plutôt que dans une accumulation intellectuelle."),
 T('realisation','Réalisation','important','direct',[2,6,14,18,23],"La réalisation est le passage de l’intention à une écriture effective dans la terre. Le psaume relie explicitement la pratique quotidienne à la construction progressive d’une vie et d’un monde."),
]},
110:{'signals':['terre promise','4 Sceaux','mémoire','corps collectif','universalité'], 'themes':[
 T('terre-promise','Terre promise','central','direct',[1,2,5,8,12,13,16,17,18],"Le psaume présente la Nation comme arrivée à la frontière d’une nouvelle étape : la terre promise n’est pas seulement un lieu, mais l’état où un corps collectif, des cultes et des sceaux sont suffisamment constitués pour relier durablement plusieurs mondes."),
 T('quatre-sceaux','Quatre Sceaux','central','direct',[1,5,8,16,17,20,21,23,24],"Les quatre Sceaux sont décrits comme des points d’incarnation et de mémoire reliant la terre aux portes des mondes supérieurs. Leur fonction est de stabiliser une Alliance et de conserver ce qui est accompli dans l’œuvre collective."),
 T('memoire-collective','Mémoire collective','central','direct',[17,20,21,22,23,25],"La mémoire ne doit plus dépendre du seul individu : une pierre et les Sceaux sont présentés comme gardant l’empreinte des noms, actes et énergies afin qu’une continuité puisse traverser les générations."),
 T('corps-collectif','Corps collectif','important','direct',[2,10,13,17,19,28,29,30,31,32],"Le travail des années précédentes est décrit comme ayant préparé un corps collectif. Il doit maintenant être structuré avec stabilité, dirigeants clairs et fonctions efficaces pour devenir le support vivant d’un savoir et d’un invisible supérieur."),
 T('separation-des-mondes','Séparation des mondes','important','direct',[14,15],"La prochaine étape exige un discernement qui protège l’espace de l’étude et de l’œuvre contre les influences profanes ou conflictuelles. Séparer n’est pas ici rompre l’Alliance, mais préserver la qualité du milieu où elle doit vivre."),
 T('universalite','Universalité','important','direct',[7,14,17,19,23],"Le projet doit dépasser une construction réservée à un petit groupe : le texte parle d’un monde intermédiaire et universel permettant à l’œuvre de toucher plus largement l’humanité tout en conservant sa source et sa mémoire."),
]},
111:{'signals':['éducation','deux natures','équilibre','corps de Lumière','maîtrise'], 'themes':[
 T('education-du-genre-humain','Éducation du genre humain','central','direct',[1,5,6,7,13,18,19,20,24,25,26,30],"La confusion humaine est attribuée à une éducation incapable d’expliquer ce qu’est l’homme, ses deux natures et sa fonction entre les mondes. Le texte propose une formation structurée par étude, dévotion, rites et œuvre afin de rendre la vie plus consciente."),
 T('deux-natures','Deux natures','central','direct',[2,4,5,6,8,14,15,16,17],"L’homme est présenté comme portant une nature ouverte à une intelligence supérieure et une nature dense liée à la matière. Le problème n’est pas d’en supprimer une mais d’apprendre à les connaître, les ordonner et les équilibrer sans que la nature mortelle s’empare de la Lumière."),
 T('equilibre-des-mondes','Équilibre des mondes','central','direct',[1,2,3,4,8,13,24],"La fonction de l’homme est explicitement décrite comme celle d’un équilibre entre deux mondes. L’éducation doit lui permettre d’écouter la matière sans perdre l’ouverture à l’universel et de rendre ces dimensions compatibles dans une même vie."),
 T('corps-de-lumiere','Corps de Lumière','important','direct',[13,15,19,20,25,26,27,28,29,30,31,32],"Le corps de Lumière désigne une structure de perception et d’action adaptée à une réalité supérieure. Il ne doit pas être construit avec les seuls yeux et intérêts du corps mortel, mais par une maîtrise progressive issue de pratiques et d’œuvres."),
 T('maitrise','Maîtrise','important','direct',[16,20,22,23,30],"La maîtrise consiste à empêcher le mélange où la nature mortelle voudrait exploiter ce qu’elle perçoit de supérieur. Elle est reliée à une formation complète et à la capacité de tenir chaque nature à sa juste place."),
 T('bien-commun','Bien commun','important','direct',[1,19,24,25,26,32],"Le but de l’éducation n’est pas seulement individuel : le texte associe l’harmonie des deux natures à une participation collective à une œuvre présentée comme bénéfique pour l’humanité et les règnes."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 20 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
