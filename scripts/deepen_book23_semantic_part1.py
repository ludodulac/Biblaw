#!/usr/bin/env python3
"""First close semantic pass for Raphael book 23, Psalms 129-131, PDF-derived only.

Psalm 128 is deliberately excluded pending documentary review because the current structured corpus
starts at verse 49 and omits intervening PDF pages. Metaphysical claims are indexed as internal
teaching of the text rather than external verified facts.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-23.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
129:{'signals':['réincarnation','cellules','mémoire','transformation','liberté'], 'themes':[
 T('reincarnation-et-continuite-cellulaire','Réincarnation et continuité cellulaire','central','contextual',[1,2,3,6,7,8,9,10,20,23,25,26],"Le psaume expose une doctrine de la réincarnation où ce qui n’est pas transformé ne réapparaît pas simplement comme un problème extérieur : il est décrit comme intégré au futur corps à travers une continuité cellulaire. Cette relation est indexée comme enseignement interne du corpus, sans être présentée comme un fait biologique ou métaphysique vérifié extérieurement."),
 T('cellules-comme-memoire','Cellules comme mémoire','central','contextual',[3,4,5,6,7,10,11,13,19,20,21,22],"Les cellules sont décrites comme porteuses de mémoire, d’intelligence et de destinée. Les habitudes et œuvres les éduqueraient et constitueraient un capital repris dans une autre vie selon la logique du texte ; cette représentation est conservée comme doctrine propre au psaume."),
 T('transformer-maintenant','Transformer maintenant','central','direct',[8,9,11,16,17,18],"Le texte refuse de reporter à une vie future ce qui peut encore être vu et travaillé maintenant. Tant qu’un défaut est perceptible, il est présenté comme une occasion de transformation ; l’abandonner à plus tard revient à le laisser s’intégrer davantage à l’être."),
 T('liberte-et-choix','Liberté et choix','important','direct',[13,14,15],"La liberté est reliée à une succession de choix qui forment progressivement les conditions intérieures de l’homme. Plus une orientation est consolidée, plus elle facilite ou réduit les possibilités futures de penser et d’agir autrement."),
 T('corps-de-lumiere','Corps de Lumière','important','contextual',[18,19,20,22,25],"Le psaume relie les œuvres conscientes à l’élaboration d’un corps de Lumière et d’immortalité composé de cellules consacrées. Cette formulation est indexée comme cosmologie interne du texte, tandis que l’axe pratique reste l’éducation du corps par les actes et les associations."),
 T('oeuvres-comme-acquis','Œuvres comme acquis','important','direct',[19,20,21,24,25,26],"Les œuvres réalisées sont présentées comme des acquis qui structurent le corps et les capacités futures. Le texte invite donc à construire maintenant des habitudes et réalisations durables plutôt qu’à compter sur une correction ultérieure automatique."),
]},
130:{'signals':['présent','passé-futur','digestion','influences','alliance'], 'themes':[
 T('conscience-du-present','Conscience du présent','central','direct',[3,4,5,6,10,20,21,22,24,30],"La conscience du présent est une attitude de vigilance, d’organisation et de maîtrise permettant de reconnaître ce qui agit maintenant. Elle ne signifie pas oublier passé et futur mais utiliser l’instant comme lieu où les influences peuvent être observées et réorientées."),
 T('present-pont-passe-futur','Présent, pont entre passé et futur','central','symbolic',[5,6,13,15,16,18,20,23],"Le présent est comparé au point neutre de la respiration où le mouvement s’inverse. Il relie ce qui a été construit hier à ce qui deviendra demain et devient ainsi un espace de transformation plutôt qu’un instant isolé de toute continuité."),
 T('digestion-du-passe','Digestion du passé','central','symbolic',[13,15,16],"La sagesse consiste à digérer les expériences passées pour en extraire un socle et des leçons. Sans cette assimilation, les mêmes erreurs sont décrites comme se recyclant au lieu de devenir matière de construction pour un futur différent."),
 T('discernement-des-influences','Discernement des influences','important','direct',[6,7,8,9,10,11],"Vivre le présent exige de reconnaître les pensées, paroles et forces avec lesquelles l’homme est en association. L’analyse de soi et l’observation du milieu subtil sont proposées comme disciplines pour distinguer ce qui fortifie la conscience de ce qui reconduit les anciennes orientations."),
 T('tradition-comme-continuite','Tradition comme continuité','important','direct',[23,25,26,28,29,31,32],"La Tradition est définie comme conscience du passé et vision de l’avenir reliées au présent. Elle situe la vie individuelle dans un ensemble plus vaste et demande de penser l’autre, la terre et les générations plutôt que seulement le moi limité."),
 T('alliance-et-destinee','Alliance et destinée','important','contextual',[7,17,18,19,20,22,26,27],"Le psaume affirme qu’une alliance avec un monde supérieur peut modifier l’écriture essentielle de la destinée. Cette proposition est indexée comme doctrine interne du texte ; son versant pratique est l’exigence d’une vie, d’une offrande et d’une œuvre cohérentes avec l’alliance revendiquée."),
 T('offrande-du-present','Offrande du présent','important','symbolic',[17,18,26],"Le présent est comparé à un autel où les fruits de la vie sont offerts. Cette image relie choix immédiats, orientation du futur et responsabilité de ce que l’homme décide de nourrir aujourd’hui."),
]},
131:{'signals':['méditation','concentration','mouvement','patience','réalisation'], 'themes':[
 T('meditation-comme-art-de-vivre','Méditation comme art de vivre','central','direct',[1,2,3,4,5,17,22,23,24,26],"La méditation est étendue à toute la vie : maintenir conscience, concentration et présence malgré les sollicitations devient l’entraînement qui révèle la manière dont l’homme conduira ses œuvres et sa destinée."),
 T('concentration-et-memoire','Concentration et mémoire','central','direct',[2,3,4,5,10,24,26],"Les influences qui capturent l’attention sont décrites comme faisant perdre la mémoire du but. La concentration maintient vivant ce qui a été choisi et empêche l’énergie d’un projet de disparaître avant qu’il puisse recevoir une forme concrète."),
 T('mouvement-de-la-vie','Mouvement de la vie','central','direct',[5,6,7,10,14,15,16,17,32,33],"Le mouvement juste doit être relié à une cause et à une intelligence plutôt qu’à l’agitation. L’homme est invité à bouger avec le mouvement de la vie et à faire du visible la conséquence d’une conception suffisamment claire et harmonieuse."),
 T('patience-et-serenite','Patience et sérénité','important','direct',[9,10,11,12,13,17,18,22,24,30],"La patience n’est pas définie comme attente passive mais comme concentration continue sur le but sans précipiter la matérialisation. Sérénité, finesse et maîtrise permettent de conserver l’œuvre assez longtemps pour qu’elle mûrisse."),
 T('realisation-subtile-puis-tangible','Réalisation subtile puis tangible','important','contextual',[14,15,16,17,18,25,26,27,28,31,33],"Le psaume affirme que l’œuvre doit d’abord être constituée dans des mondes subtils avant d’apparaître matériellement. Cette causalité est indexée comme enseignement interne du texte ; concrètement, elle exprime l’exigence de concevoir, préparer, nourrir et stabiliser un projet avant sa première manifestation tangible."),
 T('quatre-fondamentaux','Quatre fondamentaux','important','direct',[23],"La méditation est explicitement reliée aux quatre fondamentaux : étude, dévotion, rite et œuvre. Ils doivent affiner l’intelligence, purifier les sentiments et placer la volonté dans un mouvement jugé harmonieux."),
 T('etapes-de-la-creation','Étapes de la création','important','direct',[27,28,29],"Une création réussie avance pas à pas. La première manifestation tangible doit être suffisamment bien formée pour servir de base aux suivantes, tandis que brûler les étapes ou abandonner la préparation produit des formes incomplètes."),
]}}
def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); m=d.setdefault('method',{}); m['semanticPass']='deepening-in-progress'; m['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 23 deep total={m['deepPsalmCount']}")
if __name__=='__main__': main()
