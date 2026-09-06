#!/usr/bin/env python3
"""Second close semantic pass for Raphael book 19, Psalms 111-113, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-19.json'

def T(i,l,importance,directness,verses,teaching):
 return {'themeId':i,'label':l,'importance':importance,'directness':directness,'verseNumbers':verses,'teaching':teaching}

DEEP={
111:{'signals':['porte','demande','service','union','œuvre'], 'themes':[
 T('frapper-a-la-porte','Frapper à la porte','central','symbolic',[1,2,3,6,7,8],"Frapper à une porte signifie rencontrer réellement un autre monde. Le texte distingue la demande tournée vers des problèmes que l’homme peut résoudre lui-même de l’approche du monde divin, qui doit viser rencontre, union, service et œuvre plutôt qu’assistance personnelle."),
 T('service','Service','central','direct',[7,14,15,16,17,19,22],"Le service est le critère donné à l’approche d’un monde supérieur : demander et recevoir doivent conduire à honorer ce monde et à faire naître une œuvre plus grande que la personne, non à renforcer seulement son existence individuelle."),
 T('union','Union','central','direct',[1,7,11,12,13,21,22],"L’union est associée à la réussite d’une œuvre et à l’entrée dans une vie plus vaste. Les êtres sont appelés à réunir leurs forces autour d’un but clair plutôt qu’à s’agiter séparément pour exister."),
 T('respect-de-la-vie','Respect de la vie','important','direct',[8,9,10,11],"Le respect de la vie est étendu au-delà du corps physique : déstabiliser, affaiblir ou détruire les dimensions plus fines d’un être est également présenté comme une atteinte à la vie."),
 T('discernement-du-don','Discernement du don','important','direct',[14,15,16,17,18,23,24,25],"Le psaume différencie ce qui doit être donné à une œuvre de Lumière de l’aide accordée à une demande personnelle. Le discernement porte sur ce que l’autre fait réellement de sa vie et sur le monde que le don va nourrir."),
 T('tradition-comme-lien','Tradition comme lien','important','direct',[25,26,27,28,29,30,31],"La Tradition est décrite comme le corps par lequel une demande rejoint une intelligence supérieure; la qualité de la réponse dépend donc, dans le texte, de la qualité du monde auquel cette tradition relie l’homme."),
 T('transmission','Transmission','related','direct',[20],"Ce qui est cultivé intérieurement rayonne et devient semence pour les générations suivantes; la sagesse acquise est ainsi présentée comme une transmission indirecte autant qu’un bien personnel."),
]},
112:{'signals':['âme','réconciliation','deux mondes','correspondance','Tradition'], 'themes':[
 T('ame','Âme','central','direct',[2,3,4,5,6,8,9,10,11,12,13,15,16,17,18,19,21,22,23,24,27,30],"L’âme est l’intermédiaire central entre la vie terrestre et les mondes supérieurs. Elle traduit ce que l’homme vit, peut s’enrichir de ses expériences conscientes et permet la communication entre des réalités qui resteraient autrement séparées."),
 T('reconciliation-des-mondes','Réconciliation des mondes','central','direct',[8,16,18,23,24,25,26,27,30],"La réconciliation consiste à rendre la vie mortelle correspondante à une réalité immortelle afin que l’âme puisse circuler entre les mondes. Étude, rites, œuvres et relations aux règnes deviennent des moyens d’établir cette continuité."),
 T('loi-des-correspondances','Loi des correspondances','central','direct',[18,23,24],"La loi des correspondances exige que ce qui est accompli en bas soit en accord avec une réalité plus haute; l’union n’est possible que si les deux dimensions de la vie résonnent au lieu de se contredire."),
 T('corps-de-la-tradition','Corps de la Tradition','important','direct',[7,14,18,24,28,30],"La Tradition doit structurer le corps et la vie afin d’offrir à l’âme un lieu stable où respirer dans les deux mondes. Elle est ainsi présentée comme un support concret de continuité plutôt qu’un savoir extérieur."),
 T('memoire-immortelle','Mémoire immortelle','important','direct',[7,8],"Les expériences qui éveillent et ennoblissent la conscience sont décrites comme pouvant être reçues par l’âme et participer à une mémoire qui se prolonge au-delà de la mort physique."),
 T('nourriture-universelle','Nourriture universelle','important','symbolic',[22,25,26,27,28,29,30],"Le texte nomme la réconciliation des mondes « nourriture universelle » : une vie qui nourrit simultanément plusieurs plans est opposée à celle qui alimente seulement le corps mortel."),
]},
113:{'signals':['Tradition','corps vivant','Mère','petit et grand','alliance'], 'themes':[
 T('tradition','Tradition','central','direct',[1,2,3,4,5,13,15,19,20,23,27,29,30,33],"La Tradition est présentée comme le corps et le langage nécessaires pour approcher un autre monde sans quitter la réalité terrestre. Elle transmet une continuité, une éducation et une forme concrète permettant à la sagesse d’être vécue plutôt que projetée dans l’abstraction."),
 T('tradition-corps-vivant','Tradition comme corps vivant','central','direct',[2,3,5,19,20,23,30],"Le psaume insiste sur l’incorporation : la Tradition doit devenir une base réelle faite d’étude, de pensée, de sentiment, de volonté et d’actes quotidiens, jusqu’à constituer un corps capable d’habiter un monde supérieur."),
 T('mere','Mère','important','direct',[3,4,15],"La Tradition est explicitement mise en relation avec la Mère et sa manifestation concrète; vivre avec les animaux, végétaux et minéraux est présenté comme une école de réalité opposée à une spiritualité purement abstraite."),
 T('petit-et-grand','Petit et grand','important','direct',[13,14,27,28],"Le rapport entre petit et grand sert de loi de vérification : le monde supérieur ne doit pas contredire la réalité proche. Ce qui existe en grand doit déjà pouvoir trouver une correspondance et une forme dans le petit."),
 T('anti-abstraction','Refus de l’abstraction','important','direct',[13,14,15,16,17,18,20,21,24,25,31,32],"Le psaume critique les mondes spirituels abstraits qui permettent d’éviter les conséquences de la vie. La vérité doit être observable dans le quotidien, les relations et la manière de vivre avant de pouvoir prétendre ouvrir un autre monde."),
 T('alliance-des-mondes','Alliance des mondes','important','direct',[27,28,29,30],"Se tourner vers un monde supérieur est légitime seulement comme création d’une alliance entre le manifesté et le non-manifesté. La Tradition doit fournir pureté, impersonnalité et universalité pour que cette ouverture ne devienne pas une projection personnelle."),
]}}

def merge(existing,new):
 by={t.get('themeId'):t for t in existing}
 for t in new: by[t['themeId']]=t
 order={t['themeId']:i for i,t in enumerate(new)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in order else 1,order.get(t.get('themeId'),999),t.get('themeId','')))

def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for n,s in DEEP.items():
  a=by[n]; a['titleSignals']=s['signals']; a['themes']=merge(a.get('themes',[]),s['themes']); a['semanticDepth']='deep-content-grounded'
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number'])
 d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses'])
 PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f"Book 19 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
