#!/usr/bin/env python3
"""Fifth close semantic pass for Ouriel book 20, Psalms 120-123, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-20.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
120:{'signals':['Mère','terre comme messagère','vertus','corps de sagesse','écriture sur terre'], 'themes':[
 T('mere-porte-des-etoiles','Mère, porte des étoiles','central','direct',[7,9,10,12,15,16,17,18,19,20],"La Mère est présentée comme la médiation concrète entre l’homme et les mondes supérieurs : elle porte ce que l’homme inscrit sur la terre et lui permet de constituer un corps capable d’être présenté au-delà de ses concepts."),
 T('terre-comme-ecriture','Terre comme écriture','central','direct',[2,3,4,5,8,9,11,13,20,28,29,44],"La terre est décrite comme le livre où les actes humains deviennent lisibles pour les mondes supérieurs. Prière et méditation ne remplacent donc pas l’écriture concrète laissée par les œuvres, les relations et la manière d’habiter le monde."),
 T('vertus-vivantes','Vertus vivantes','central','direct',[22,23,24,25,26,30,31,32,43,44],"Les vertus sont traitées comme des messagères vivantes qu’il faut accueillir consciemment, cultiver et multiplier. Une vertu reçue mais non comprise peut être détournée; vécue avec conscience, elle devient un corps de manifestation et une alliance avec l’Ange correspondant."),
 T('corps-de-la-mere','Corps de la Mère','important','direct',[7,16,18,19,20,32,43],"Le chemin vers les mondes supérieurs exige un corps formé dans la Tradition et la Mère. Ce corps n’est pas une abstraction spirituelle mais une structure de sagesse constituée par la pratique, la compréhension et l’acte."),
 T('reciprocite-avec-la-mere','Réciprocité avec la Mère','important','direct',[10,12,15,17,18,23,27],"Le texte critique l’usage de la Mère comme simple soutien ou lieu de décharge. La relation juste implique reconnaissance, fidélité et œuvres qui rendent à la terre ce qui a été reçu plutôt que de lui confier uniquement les déchets de la vie."),
 T('pratique-et-savoir','Pratique et savoir','important','direct',[28,31,32,43,44],"La lumière du savoir doit passer par une pratique assidue qui engendre un corps, puis par des actes conscients qui inscrivent les valeurs de la Tradition dans le livre de la destinée et de la terre."),
]},
121:{'signals':['corps comme livre','microcosme','organes','langage universel','enracinement'], 'themes':[
 T('corps-comme-livre','Corps comme livre','central','direct',[1,3,5,7,8,9,11,12,16,17,20,21,22,32,44],"Le corps est présenté comme un livre et un alphabet où des intelligences supérieures seraient inscrites dans les organes. L’étude du corps vise ici à retrouver un langage et une connaissance de soi qui dépassent les schémas mentaux abstraits."),
 T('microcosme-macrocosme','Microcosme et macrocosme','central','direct',[1,5,6,7,11,12,21,32],"L’homme est décrit comme un microcosme du macrocosme : chaque organe correspond à une intelligence ou à une partie de l’univers. La connaissance de soi devient ainsi, dans le texte, un chemin de lecture des relations entre l’homme et les mondes."),
 T('enracinement','Enracinement','central','direct',[8,13,19,23,24,25],"L’accès aux mondes subtils ne doit pas se faire en abandonnant la terre. Comme la plante qui s’enracine davantage à mesure qu’elle s’élève, l’homme doit approfondir ses fondements corporels et terrestres pour éviter une spiritualité déracinée."),
 T('organes-comme-intelligences','Organes comme intelligences','important','direct',[5,7,8,11,12,14,16,17,19,20],"Les organes sont présentés comme porteurs de capacités, de vertus et de fonctions créatrices. Le texte demande de les étudier consciemment au lieu de les utiliser machinalement ou de les réduire à des schémas intellectuels."),
 T('langage-universel-du-corps','Langage universel du corps','important','direct',[22,27,29,31,32,33,44],"Le mouvement, les gestes et les organes sont décrits comme un langage capable de relier l’homme à plusieurs mondes. Réapprendre ce langage par le corps doit permettre une communication plus vaste que la seule parole conceptuelle."),
 T('corps-instrument-de-service','Corps instrument de service','important','direct',[27,28,33,44,45,46],"Le corps est envisagé comme un instrument qui peut servir une œuvre de guérison, d’échange et d’alliance. La maîtrise physique n’est pas suffisante : l’instrument doit aussi être éveillé dans les autres plans décrits par le texte."),
]},
122:{'signals':['faux luxe','fausse lumière','discernement','vraies valeurs','sens'], 'themes':[
 T('faux-luxe','Faux luxe','central','direct',[1,3,4,6,7,8,12,13,15,16,18],"Le faux luxe désigne l’attrait pour une perfection extérieure qui valorise l’apparence tout en vidant la vie intérieure. Le texte ne condamne pas la beauté matérielle en elle-même, mais l’identification qui en fait la mesure principale de la valeur."),
 T('fausse-lumiere','Fausse lumière','central','direct',[4,6,8,15,16,18],"La fausse lumière est ce qui capte les sens et la pensée en donnant au superficiel l’apparence du précieux. Elle détourne du développement intérieur et associe l’homme à des valeurs qui ne nourrissent pas, selon le texte, les dimensions plus subtiles de l’être."),
 T('discernement-du-regard','Discernement du regard','central','direct',[4,8,12,13,14,15,16],"La réponse n’est pas de détourner les yeux du monde mais d’apprendre à discerner ce qui est réellement vivant, vrai et relié à une intelligence plus haute de ce qui ne présente qu’une forme séduisante."),
 T('vraies-valeurs','Vraies valeurs','important','direct',[2,5,9,10,11,17,18],"Les vraies valeurs sont associées à la noblesse intérieure, à la sagesse, à la bonté, au parfum symbolique de la fleur et à ce qui nourrit les sens intérieurs plutôt qu’à une forme parfaite mais sans âme."),
 T('education-des-sens','Éducation des sens','important','direct',[6,8,14,15,17],"Les sens doivent être travaillés pour ne pas être capturés par les apparences. Contempler, écouter, respirer et goûter deviennent des facultés de discernement capables de reconnaître ce qui nourrit réellement la vie intérieure."),
 T('corruptible-et-incorruptible','Corruptible et incorruptible','important','direct',[3,6,16,17,18],"Le psaume oppose la poursuite du corruptible à la recherche de valeurs pouvant dépasser le passage de la mort. Le critère proposé n’est pas le prestige visible mais ce qui constitue un capital intérieur durable."),
]},
123:{'signals':['examen de passage','offrande','achèvement','acquis','nouveau cycle'], 'themes':[
 T('examen-de-passage','Examen de passage','central','direct',[1,4,12,14,15,16,17,25,26,27,29,30,31,33],"Le jubilé est présenté comme un examen où les acquis d’un cycle sont rendus visibles et deviennent la base du suivant. Réussir signifie avoir conduit le travail jusqu’à une forme suffisamment claire et constituée pour être reconnue et poursuivie."),
 T('offrande-parfaite','Offrande parfaite','central','direct',[2,3,5,7,8,9,10,11,25,26],"L’offrande au monde divin ne doit pas être une œuvre inachevée. Elle représente ce que l’homme a réellement constitué; ce qui est offert est ensuite décrit comme revenant à l’homme sous forme d’acquis, de terre ou de condition de vie."),
 T('achevement-et-maitrise','Achèvement et maîtrise','central','direct',[3,7,8,9,13,15,18,19,25,30,33],"Le passage exige de conduire les œuvres jusqu’à leur aboutissement. La maîtrise est moins présentée comme perfection absolue que comme clarté, organisation et décision de poursuivre le travail sans laisser les mélanges interrompre la réalisation."),
 T('acquis','Acquis','important','direct',[6,12,13,17,25,26],"Les acquis du cycle sont décrits comme une terre sous les pieds. Ce qui a été transformé, clarifié ou au contraire maintenu comme problème devient une réalité reconnue qui influencera la suite du chemin."),
 T('purification-et-rattrapage','Purification et rattrapage','important','direct',[16,18,19,21,22,23,24,29,30,32,33],"Après l’examen, le texte prévoit un temps de clarification et de rattrapage. Désillusion, étude, nettoyage et séparation des mondes doivent permettre de corriger ce qui reste lié à la confusion avant le nouveau cycle."),
 T('nouveau-cycle','Nouveau cycle','important','direct',[14,15,17,27,28,31],"Le nouveau cycle commence sur la base du précédent et demande un espace plus clairement séparé du monde des hommes. L’étude, la dévotion, les rites et l’œuvre sont présentés comme les pratiques qui permettront d’y entrer."),
]}}

def merge(e,n):
 by={t.get('themeId'):t for t in e}; [by.__setitem__(t['themeId'],t) for t in n]; o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items(): by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 20 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
