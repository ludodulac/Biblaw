#!/usr/bin/env python3
"""Sixth close semantic pass for Michael book 21, Psalms 152-154, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-21.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
152:{'signals':['temps','pensée créatrice','entités','maîtrise','mission'], 'themes':[
 T('temps-et-separativite','Temps et séparativité','central','direct',[1,2,3],"Le psaume relie le temps à la distance entre pensée, parole, action, réalisation et être. Plus ces dimensions sont séparées et confuses, plus le processus s’allonge; leur unification est présentée comme une forme d’immédiateté."),
 T('pensee-creatrice','Pensée créatrice','central','direct',[4,5,6,7,8,9,10,11,12,14,16,17,18,20,22,23,24],"La pensée est décrite comme une création vivante qui cherche des associés et un accomplissement. Penser sans conscience revient donc à peupler son ciel de formes et d’engagements que l’homme devra ensuite porter ou conduire vers une réalisation."),
 T('maitrise-pensee-parole','Maîtrise de la pensée et de la parole','central','direct',[13,14,15,16,17,18,28],"Pensée et parole sont les premiers instruments à maîtriser parce qu’elles engagent l’homme envers des mondes. Juger, promettre ou commenter sans intention d’assumer les conséquences peut créer des charges qui détournent de la mission propre."),
 T('affinites-et-associations','Affinités et associations','important','direct',[5,7,8,11,12,16,20,24,25,34],"Les pensées et projets cherchent des associés par affinité. L’homme doit reconnaître la provenance de ce qui l’inspire et éviter les associations qui l’alourdissent, tout en sachant que l’unification de moyens complémentaires peut rendre une création collective possible."),
 T('mission-et-concentration','Mission et concentration','important','direct',[17,18,19,20,21,22,26,27,29,30,31,32,33],"Le texte demande de se concentrer sur l’œuvre de sa vie plutôt que de porter tout ce qui se présente. Une mission accomplie et aboutie crée une terre et un ciel qui permettent ensuite d’aider les autres sans perdre sa propre force."),
 T('donner-une-ame-a-l-oeuvre','Donner une âme à l’œuvre','important','direct',[19,20,21,22,26,27,29,30],"Vivre avec son âme est défini comme donner une âme à ce que l’on fait. Les idées doivent recevoir un corps, une réalisation et une orientation qui les conduisent vers la perfection et la libération plutôt que rester comme charges inachevées."),
]},
153:{'signals':['pieds','vérité','Mère','stabilité','langage originel'], 'themes':[
 T('pieds-comme-verite','Pieds comme vérité','central','symbolic',[1,2,4,5,10,11,12,13,14,25,26,27,28,29,30,32],"Les pieds sont présentés comme une image de la vérité parce qu’ils donnent un retour immédiat sur le sol, le chemin et les influences rencontrées. Ils opposent une information concrète et fidèle aux constructions abstraites qui peuvent éloigner de la réalité vécue."),
 T('stabilite-et-fondement','Stabilité et fondement','central','direct',[2,10,11,12,19,20,22,28,29],"Les pieds portent, équilibrent et relient au fondement. Leur discrétion symbolise une force qui ne cherche pas à paraître mais qui donne continuité, assurance et capacité de marcher réellement sur un chemin."),
 T('langage-de-la-mere','Langage de la Mère','central','symbolic',[14,16,17,22,23,25,27,28,29,30,31,32,33],"Le contact des pieds avec la terre est décrit comme un langage avec la Mère. Ce lien doit réveiller des perceptions, rappeler les racines et renseigner l’homme sur sa mission, sa destinée et la manière dont son pas s’inscrit dans le monde."),
 T('discernement-par-le-corps','Discernement par le corps','important','direct',[5,11,12,13,16,23,25,26],"Le corps fournit des critères qui complètent ou corrigent les idées de la tête. L’attention aux pieds permet de ressentir les influences et de discerner une direction à partir d’un retour concret plutôt que d’une théorie seule."),
 T('humilite-et-simplicite','Humilité et simplicité','important','direct',[19,20,21,22,23],"Les pieds sont associés à l’humilité, au calme et à la disponibilité. Le psaume valorise cette simplicité contre le besoin de bruit, d’apparence et de reconnaissance qui détourne de ce qui porte réellement la vie."),
 T('pied-mediateur','Pied médiateur','important','direct',[27,28,29,30,31,33],"Le pied est explicitement décrit comme un médiateur entre deux mondes. Il relie l’écriture de la terre au mouvement de l’homme et devient ainsi un organe de communication entre la Mère, le corps et l’orientation de la vie."),
]},
154:{'signals':['vérité','remise en question','impersonnalité','humilité','préparation'], 'themes':[
 T('premier-pas-vers-la-verite','Premier pas vers la vérité','central','direct',[7,10,12,13,14,18,19,21,22],"Le premier pas vers la vérité est d’admettre son ignorance et d’accepter de se remettre en question. Le texte oppose cette disposition à la défense d’une image de soi qui préfère l’illusion à une observation susceptible de déplacer ses certitudes."),
 T('regard-impersonnel','Regard impersonnel','central','direct',[1,2,3,4,5,6,7,8,9,11],"L’homme doit apprendre à observer les fruits de sa propre attitude depuis un point de vue neutre et détaché. Cette impersonnalité permet de reconnaître les influences et incohérences que l’autojustification empêche habituellement de voir."),
 T('humilite','Humilité','central','direct',[13,18,19,21,22,23,24,25,26,27,28],"L’humilité est présentée comme une protection qui accepte l’existence d’une vérité supérieure au désir humain. Elle permet de lire les oppositions et difficultés comme des occasions de correction plutôt que de déclarer automatiquement mauvais ce qui contrarie la volonté personnelle."),
 T('preparation-aux-epreuves','Préparation aux épreuves','important','direct',[15,16,17,18,19,21,22,23],"L’homme ne sait pas sous quelle forme viendra l’épreuve. Il doit donc préparer une façon de vivre fondée sur la Tradition, l’humilité et la capacité de se réexaminer, afin de ne pas dépendre d’une lucidité improvisée au moment de la crise."),
 T('actes-comme-realite','Actes comme réalité','important','direct',[2,7,9,10,11,14,23,27,28],"Le texte réduit les chimères et justifications à ce qui n’est pas confirmé par la vie. Ce que l’homme fait, les atmosphères qu’il produit et les fruits qui apparaissent deviennent les critères concrets de ce qu’il est réellement en train de nourrir."),
 T('opposition-comme-miroir','Opposition comme miroir','important','direct',[23,24,25,26,27,28],"Toute opposition n’est pas interprétée comme attaque d’une force sombre. Elle peut être un écho de la vie et une bénédiction qui révèle ce qui demande à être corrigé, à condition que l’homme accepte de regarder autrement sa propre situation."),
]}}
def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); m=d.setdefault('method',{}); m['semanticPass']='deepening-in-progress'; m['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 21 deep total={m['deepPsalmCount']}")
if __name__=='__main__': main()
