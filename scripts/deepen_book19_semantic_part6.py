#!/usr/bin/env python3
"""Complete close semantic pass for Raphael book 19, Psalms 122-127, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-19.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
122:{'signals':['fidélité','don reçu','âme de la vie','Tradition','transmission'], 'themes':[
 T('fidelite','Fidélité','central','direct',[5,7,8,9,12,13,15,19,21,24,25,26,28,30,31,32,33,34,35,36,37,38],"La fidélité est présentée comme la capacité à accueillir ce qui a été reçu, le développer et le conduire jusqu’à son accomplissement au lieu de l’abandonner au profit d’une nouveauté. Elle doit traverser pensée, sentiment, actes et engagements."),
 T('don-recu','Don reçu','central','direct',[1,2,3,4,5,7,9,13,15,18],"Le psaume part du don reçu à la naissance — souffle, âme de la vie, qualités, possibilités et mission — et demande de le reconnaître comme une base à faire fructifier plutôt que comme un acquis sans responsabilité."),
 T('ame-de-la-vie','Âme de la vie','important','direct',[3,9,10,14,18,20],"L’âme de la vie est présentée comme la dimension vivante qui relie les êtres, les choses et les événements à un tout plus grand. Sa perte de vue conduit à traiter ce qui existe comme interchangeable et sans valeur."),
 T('stabilite-et-racines','Stabilité et racines','important','direct',[12,15,16,17,25,38],"L’homme a besoin de racines et d’une terre pour approfondir ce qu’il reçoit. La stabilité est opposée au passage constant d’un courant ou d’une pratique à l’autre sans incorporation réelle."),
 T('tradition','Tradition','important','direct',[12,16,17,26,37],"La Tradition est le terrain sur lequel la fidélité peut devenir un corps et une continuité. Le texte demande de ne pas seulement visiter des sagesses successives mais de faire vivre celle à laquelle on s’est réellement engagé."),
 T('transmission','Transmission','important','direct',[13,15,18,26,27,28,38],"Préserver ce qui est beau et vrai implique de le transmettre dans le temps. La fidélité acquiert ainsi une dimension collective : certaines vertus doivent rester vivantes pour les générations et les règnes qui les portent."),
]},
123:{'signals':['enfant intérieur','épreuves','sagesse','éducation','renouveau'], 'themes':[
 T('enfant-interieur','Enfant intérieur','central','symbolic',[9,10,11,12,13,14,15,16,21],"L’enfant intérieur symbolise une capacité de recommencement, d’enthousiasme et de confiance qui empêche les années et les épreuves de se transformer uniquement en poids. Le texte demande de préserver cette fraîcheur tout en grandissant en sagesse."),
 T('epreuves','Épreuves','central','direct',[2,4,5,17,18,19,22,23,24,25,26,27,30],"Les épreuves sont présentées comme des occasions de désillusion, de miroir et de rééquilibrage plutôt que comme des punitions. Elles persistent lorsque l’expérience n’est pas conduite jusqu’à une sagesse qui change réellement la vie."),
 T('sagesse','Sagesse','central','direct',[5,6,7,8,14,17,18,19,20,21,23,24,25,26,27,29,30],"La sagesse est la voie de sortie du fatalisme et du recommencement. Elle transforme l’épreuve en compréhension, permet de se reconstruire et maintient une orientation de vie qui ne s’éteint pas avec les difficultés."),
 T('education-et-transmission','Éducation et transmission','important','direct',[1,2,5,7,8],"Le texte attribue une part de la difficulté humaine à une éducation qui n’apprend ni le discernement ni le sens profond de la vie. Une autre formation doit être transmise sur plusieurs générations pour que la sagesse puisse mûrir."),
 T('fatalisme','Fatalisme','important','direct',[5,6,12,16,18,24],"Le fatalisme apparaît lorsque l’homme accumule les problèmes sans retrouver le chemin du renouveau. Il est opposé à la capacité de se relever, recommencer et traiter chaque épreuve comme un passage temporaire."),
 T('immortalite','Immortalité','related','direct',[14,15,29,30],"La conscience d’une vie qui ne s’arrête pas et l’union à une sagesse qui rajeunit sont présentées comme une orientation vers l’immortalité, maintenue jusque dans la disparition du corps."),
]},
124:{'signals':['passage sur terre','mission','mémoire','œuvres','au-delà'], 'themes':[
 T('mission-terrestre','Mission terrestre','central','direct',[1,2,3,7,8,9,10,11],"La vie terrestre est décrite comme un passage limité dans le temps, reçu pour accomplir une œuvre. Les rencontres, épreuves et circonstances sont interprétées comme pouvant réveiller la mémoire de cette mission et orienter l’action."),
 T('memoire-de-la-mission','Mémoire de la mission','central','direct',[2,3,9,10,11,12,13,14],"Se souvenir de qui l’on est et de ce que l’on est venu faire constitue le pivot du psaume. La Tradition et la formation sont présentées comme des moyens de réveiller cette mémoire sans tomber dans les projections et illusions."),
 T('oeuvres-et-au-dela','Œuvres et au-delà','central','direct',[4,5,6,7,8],"Les œuvres réalisées sur la terre sont décrites comme constituant une base dans l’au-delà. Ce qui a été vécu en relation avec un monde supérieur donne une stabilité et une continuité, tandis que les illusions terrestres se prolongent aussi sous une autre forme."),
 T('famille-d-ame','Famille d’âme','important','direct',[3],"Une fois la mission reconnue, le texte recommande de trouver des associés en affinité avec l’œuvre — une « famille d’âme » — afin de disposer d’une force collective pour la réaliser."),
 T('tradition-et-formation','Tradition et formation','important','direct',[10,11,13,14,17,18],"La Tradition est décrite comme un cadre de formation du corps de sagesse et de vérification de la mémoire. Le texte déconseille les explorations isolées de voies sorties de leur contexte sacré, jugées vulnérables à l’illusion."),
 T('concepts-projetes','Concepts projetés','important','direct',[15,16,17,18],"L’homme est présenté comme créateur de concepts qui peuvent remplacer la réalité qu’il cherche à connaître. Une approche d’un monde supérieur demande donc de devenir une terre ouverte et stable plutôt que d’aller chercher la réponse déjà souhaitée."),
]},
125:{'signals':['roue du temps','éternité','correspondance','terre de Lumière','rites'], 'themes':[
 T('roue-du-temps','Roue du temps','central','symbolic',[1,2,8,9,10,11,15,16,28],"La roue du temps désigne le cycle où l’homme répète les mêmes expériences et recherches sans acquérir de sagesse. L’arrêter signifie se décaler du mouvement automatique du monde humain pour retrouver stabilité, contemplation et intelligence."),
 T('eternite','Éternité','central','direct',[10,11,13,14,16,17,26,30],"Entrer dans l’éternité est associé à la sérénité, à l’éveil et à une vie orientée vers ce qui peut traverser les mondes. Le texte oppose cette continuité à l’agitation et au recommencement du monde de la mort."),
 T('correspondance-des-mondes','Correspondance des mondes','central','direct',[3,4,5,6,7,17,20,21],"Une relation avec un monde supérieur exige une correspondance préalable avec les autres règnes et les différentes dimensions de la vie. L’offrande et l’aspiration doivent être reconnues dans plusieurs mondes avant d’être présentées au monde divin."),
 T('terre-de-lumiere','Terre de Lumière','important','direct',[17,18,20,21,24,30],"La terre de Lumière est la base concrète et relationnelle qui doit être en cohérence avec le ciel. Le texte refuse une spiritualité dont les pieds resteraient dans un monde opposé à ce que la tête prétend honorer."),
 T('rites-meditatifs','Rites méditatifs','important','direct',[23,24,26],"Les rites méditatifs sont intégrés à un parcours comprenant Tradition, étude, dévotion, rite puis œuvres. Ils doivent ancrer la Lumière dans le corps et dans une structure collective plutôt que remplacer la vie quotidienne."),
 T('liberation-des-regnes','Libération des règnes','important','direct',[5,17,18,19,20,21],"La libération personnelle est liée à une réconciliation avec les règnes environnants. Le chemin n’est pas présenté comme une fuite individuelle mais comme une manière de rendre dignité et espace aux êtres autour de soi."),
]},
126:{'signals':['préparation','étapes','influences','semence','Ouriel'], 'themes':[
 T('preparation','Préparation','central','direct',[1,2,3,4,5,6,7,8,12,14,15,17,18,19,20,21,25,26,27,29],"Chaque étape de la vie demande une préparation consciente. Le texte oppose la participation active — étude, nettoyage, sélection des influences et clarification des intentions — à une vie laissée au pilotage d’un monde extérieur."),
 T('influences','Influences','central','direct',[2,8,9,11,12,13,16,23,24,25,26,27,28,29,30],"Les périodes de la vie sont présentées comme traversées par des influences qu’il faut connaître et mettre à leur place. Sans formation, l’homme devient leur pantin; avec conscience, il peut décider lesquelles conserver, transformer ou refuser."),
 T('semence-et-realisation','Semence et réalisation','central','symbolic',[8,10,12,13,14,15,16],"À l’approche d’Ouriel, les pensées et tendances portées en soi sont comparées à des semences qui recevront une terre et une réalisation. D’où l’exigence de présenter une semence choisie, claire et préparée."),
 T('maitrise','Maîtrise','important','direct',[15,16,17,25,26,27,28,29,31],"La maîtrise consiste à connaître les mondes intermédiaires sans s’y perdre, savoir qui l’on est et ce que l’on veut devenir, puis agir consciemment même face à des influences plus grandes que soi."),
 T('participation-active','Participation active','important','direct',[6,8,9,11,18,21,22,30],"Le psaume refuse une philosophie de passivité où tout serait déjà organisé. Chacun doit participer à l’ensemble, tenir sa place et prendre part aux décisions qui construisent son avenir."),
 T('corps-de-divinite','Corps de divinité','related','direct',[31],"La rencontre avec une grandeur ne doit pas dissoudre l’individu : le texte demande de s’y unir consciemment tout en se construisant un corps réel et agissant capable de porter cette relation."),
]},
127:{'signals':['Alliance','Dieu Air','organisation','pensées','propagation'], 'themes':[
 T('alliance','Alliance','central','direct',[1,2,3,4,7,8,23],"Le psaume s’ouvre sur une Alliance dite scellée puis en décrit les conséquences pratiques : entretenir le culte de l’Air, préparer la suite avec Ouriel et construire une organisation capable de soutenir et propager l’enseignement."),
 T('organisation','Organisation','central','direct',[5,8,10,14,15,21,22,23,26],"L’organisation devient une condition de propagation et de réalisation. Les compétences doivent être mises en commun afin d’alléger ceux qui portent certaines fonctions et de constituer un corps international capable de faire entendre une voix collective."),
 T('vigilance-de-la-pensee','Vigilance de la pensée','central','direct',[9,12,13,16,17,18,19,20],"Les pensées sont décrites comme construisant les futurs pas, relations et milieux de vie. Étude, observation et vigilance doivent limiter les associations inutiles ou asservissantes et renforcer un corps de sagesse."),
 T('air-et-atmosphere','Air et atmosphère','important','direct',[2,3,4,5,6,9,12],"Le monde de l’Air est associé à l’atmosphère collective, au souffle et aux pensées. Les œuvres sur les sommets, l’étude et le culte de l’Air sont présentés comme des moyens de dégager une atmosphère devenue difficile à traverser."),
 T('soutien-des-fonctions','Soutien des fonctions','important','direct',[7,15,21,22,23],"Le texte demande de soutenir les responsables et le guide en partageant compétences et charges. L’objectif formulé est qu’ils puissent se concentrer sur leur fonction propre au service de l’œuvre collective."),
 T('preparation-a-ouriel','Préparation à Ouriel','important','direct',[8,25,27],"La fin du livre prépare explicitement la célébration d’Ouriel : il ne s’agit pas de demander quelque chose mais de présenter consciemment ce qui a été cultivé, clarifié et offert pour la suite de l’œuvre."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses'])
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 19 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
