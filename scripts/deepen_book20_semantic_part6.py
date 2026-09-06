#!/usr/bin/env python3
"""Final close semantic pass for Ouriel book 20, Psalms 124-129, PDF-derived only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PATH=ROOT/'data/thematic-index/books/book-20.json'
def T(i,l,imp,d,v,t): return {'themeId':i,'label':l,'importance':imp,'directness':d,'verseNumbers':v,'teaching':t}
DEEP={
124:{'signals':['Évangiles esséniens','pierre','stabilité','fondements','générations futures'], 'themes':[
 T('evangiles-comme-oeuvre','Évangiles comme œuvre','central','direct',[1,2,3,7,9,11,13,14,15,16],"Les Évangiles sont présentés comme une parole reçue qui devient une œuvre lorsqu’elle est posée concrètement sur la pierre. Leur valeur tient à la continuité de l’Alliance, à l’étude et à la transmission d’un support destiné aussi aux générations futures."),
 T('pierre-et-stabilite','Pierre et stabilité','central','direct',[1,18,20,21,23,27,33],"La pierre est le modèle de stabilité qui permet de fixer les éléments d’une vie et d’en faire un corps durable. L’enseignement doit descendre jusqu’à cette stabilité par l’étude, la dévotion, le rite et l’œuvre."),
 T('fondements','Fondements','central','direct',[14,15,18,20,21,22,23,27,33],"Le texte insiste sur la nécessité de fondements clairs et structurés : sans terre, corps ou structure capables de porter une aspiration, les impressions et compréhensions restent éphémères et se dispersent."),
 T('transmission-future','Transmission aux générations futures','important','direct',[7,14,15],"Poser une œuvre durable signifie travailler au-delà de l’utilité immédiate. Les textes et les fondements constitués sont explicitement orientés vers les générations futures et la possibilité de maintenir une vie de l’âme."),
 T('discernement','Discernement','important','direct',[25,26,29,30,32,34],"La stabilité ne signifie pas rigidité aveugle : le psaume demande de discerner ce qui mérite d’être regardé, entendu et honoré, de sortir des apparences et de ne pas laisser les perceptions être conduites par des influences sans fondement."),
 T('enracinement','Enracinement','important','direct',[18,20,21,22,23,27,33],"L’enracinement transforme une aspiration en existence. Renforcer les racines, se poser sur une terre et structurer la vie sont les conditions données pour qu’une valeur intérieure cesse d’être une sensation passagère."),
]},
125:{'signals':['dignité','écologie intérieure','déchets','maîtrise','respect des règnes'], 'themes':[
 T('dignite','Dignité','central','direct',[1,2,4,5,6,8,9,13],"La dignité consiste à reconnaître la valeur de la pensée, du cœur, de la parole et des émanations qui ont été confiées à l’homme. Cette valeur doit être protégée de ce qui dégrade et étendue à tous les règnes, de la pierre à l’homme."),
 T('ecologie-interieure','Écologie intérieure','central','direct',[13,14,18,19,20,21,22,23],"Le psaume relie directement pollution extérieure et désordre intérieur. Faire le ménage dans toutes les parties de l’être, régler ce qui est laissé en suspens et surveiller ce que l’on génère constituent l’écologie préalable à toute écologie visible."),
 T('respect-des-regnes','Respect des règnes','central','direct',[7,8,9,20,23],"Aucun règne ne doit être traité comme un déchet : chacun porte une valeur qui appelle respect et dignité. La dégradation de la nature est présentée comme le reflet d’une dégradation déjà installée dans la vie intérieure humaine."),
 T('maitrise-des-influences','Maîtrise des influences','important','direct',[12,13,14,15,16,17,26,27,28,30,31],"La maîtrise demande de reconnaître les influences qui cherchent à féconder la vie intérieure sans leur donner automatiquement un corps. Résister consciemment, préserver son espace vital et rester stable dans l’épreuve renforcent progressivement l’autonomie."),
 T('responsabilite-du-futur','Responsabilité du futur','important','direct',[15,16,17,19,21,30],"Ce qui est pensé, laissé en suspens ou caché prépare une situation future. Le texte demande donc d’être attentif à ce que l’on veut voir naître et de ne pas engendrer aujourd’hui des conditions qui deviendront demain incontrôlables."),
]},
126:{'signals':['point de vue','impersonnalité','écoute','langage universel','préparation'], 'themes':[
 T('point-de-vue','Point de vue','central','direct',[1,2,3,4,6,7,8],"Le point de vue personnel filtre ce qui est entendu et peut transformer une loi ou un enseignement en confirmation de ses propres attentes. Le psaume situe donc une cause majeure d’erreur dans l’incapacité à sortir de sa perception habituelle."),
 T('impersonnalite','Impersonnalité','central','direct',[6,8,9,10,12,13,14],"L’impersonnalité est la capacité de recevoir une réponse sans la plier au désir d’être rassuré, valorisé ou confirmé. Elle demande un espace intérieur suffisamment libre pour accueillir une parole telle qu’elle est."),
 T('langage-universel','Langage universel','central','direct',[5,6,8,9],"Le langage universel élargit l’écoute au-delà du seul point de vue humain. Les animaux, végétaux et pierres sont convoqués comme des perspectives qui rappellent mouvement, noblesse, mémoire et stabilité avant l’approche d’un enseignement plus élevé."),
 T('ecoute','Écoute','important','direct',[3,4,5,6,7,8,9],"Écouter ne signifie pas sélectionner ce qui convient. L’écoute juste suppose de suspendre l’interprétation immédiate, d’accepter qu’une parole dérange les repères existants et de chercher ce qu’elle demande réellement de transformer."),
 T('preparation-interieure','Préparation intérieure','important','direct',[9,10,12],"Avant de questionner un sage, le texte demande de préparer une terre intérieure claire, consciente des mondes et points de vue qui l’habitent, afin que la réponse puisse être reçue sans être immédiatement déformée."),
]},
127:{'signals':['parole','vérité','silence','fidélité','cohérence'], 'themes':[
 T('parole-vivante','Parole vivante','central','direct',[1,2,3,6,9,10,16,17,18,22,39,40,41,42],"La parole est présentée comme l’expression de l’être entier et non comme un simple outil de communication. La guérir consiste à rendre de nouveau cohérents parole, identité, âme, engagement et manière de vivre."),
 T('verite-de-la-parole','Vérité de la parole','central','direct',[4,7,8,19,20,24,25,26,27,28,29,32,34,37,38],"La vérité est le critère qui rend la parole juste. Elle demande simplicité, conscience et équilibre, et libère la parole de l’usage stratégique destiné à fabriquer une apparence ou à obtenir quelque chose d’autrui."),
 T('parler-ou-se-taire','Parler ou se taire','central','direct',[27,28,30,31,32,33,34,35],"Savoir parler inclut le droit de se taire. Le choix juste dépend de ce qui est vrai et opportun : s’il n’y a rien à dire, le silence vaut mieux qu’une parole fabriquée; s’il faut parler, la parole doit être simple et assumée."),
 T('fidelite-a-la-parole','Fidélité à la parole','important','direct',[1,2,4,12,13,17,36],"Donner sa parole engage la stabilité et la dignité de l’être. L’inconstance, la promesse oubliée et le double langage sont décrits comme une perte de cohérence qui empêche une relation de confiance durable."),
 T('mensonge-et-separation','Mensonge et séparation','important','direct',[3,5,7,8,11,12,14,35,36,43],"Le mensonge crée une séparation entre ce qui est dit, pensé et vécu. À mesure que cette séparation devient habituelle, l’homme perd ses repères, sa stabilité et sa capacité à reconnaître lui-même ce qui est vrai."),
]},
128:{'signals':['mémoires ancestrales','passé','lignée','mémoire immortelle','sagesse'], 'themes':[
 T('memoires-ancestrales','Mémoires ancestrales','central','direct',[1,2,3,4,5,7,9,10,19,20],"Le passé est décrit comme un ensemble de mémoires, désirs et habitudes transmis qui continuent à chercher une expression dans le présent. Les identifier permet de distinguer l’héritage reçu de ce que l’on choisit consciemment de prolonger."),
 T('memoire-immortelle','Mémoire immortelle','central','direct',[2,9,11,13,14,15,21,22,23],"Le texte oppose la mémoire mortelle, attachée aux expériences et désirs inachevés, à une mémoire immortelle reliée à la sagesse et à la Tradition. Le travail proposé est de donner un corps à cette seconde mémoire plutôt qu’à la répétition du passé."),
 T('relation-au-passe','Relation au passé','central','direct',[6,10,11,12,17,18,19],"Le passé n’est pas nié : lorsqu’il est connu, il devient un acquis et un fondement. Mais le réalimenter sans cesse le ramène dans le présent et lui donne une nouvelle force, au lieu de permettre d’avancer."),
 T('lignee','Lignée','important','direct',[2,3,7,10,19,20,22],"La lignée véritable est rendue visible par ce que la vie quotidienne manifeste et nourrit. Le psaume demande ainsi de discerner si l’on prolonge mécaniquement des ambitions anciennes ou une tradition conduite dans la sagesse."),
 T('sagesse-comme-liberation','Sagesse comme libération','important','direct',[9,12,13,14,15,17,21,23],"La sagesse est la voie de transformation des mémoires : les expériences sont acceptées puis reliées à un sens plus vaste, afin que leur énergie cesse d’imposer une répétition et puisse devenir un fondement libéré."),
]},
129:{'signals':['réécriture du monde','organisation','corps collectif','Alliance','acte concret'], 'themes':[
 T('reecriture-du-monde','Réécriture du monde','central','direct',[4,5,8,20,32,33,34],"Le psaume décrit les réalités visibles comme précédées d’une écriture dans des plans plus subtils et demande de modifier cette écriture en donnant un autre point de vue sur les manifestations de la vie. La transformation n’est donc pas réduite à une opinion : elle doit finir par toucher la réalité terrestre."),
 T('acte-concret','Acte concret','central','direct',[14,15,16,19,20,23,25,29],"L’accent final du livre porte sur l’acte concret : la Lumière doit recevoir une forme, un corps et une organisation reconnaissables. La prière ou la méditation abstraites ne remplacent pas le travail de réalisation dans le monde physique."),
 T('organisation-collective','Organisation collective','central','direct',[14,17,18,19,20,21,22,23,25,26,27,28,29],"L’organisation est présentée comme le moyen de transformer des valeurs communes en un peuple et une œuvre durables. Communication, répartition des fonctions, soutien des responsables et structures matérielles constituent le corps collectif demandé par le texte."),
 T('alliance-vivante','Alliance vivante','important','direct',[3,6,12,13,17,27,29],"L’Alliance doit être entretenue comme un lien vivant plutôt que supposée acquise. La fidélité, la transmission et le soutien des fonctions qui gardent ce lien ouvert sont décrits comme des conditions de continuité pour les générations futures."),
 T('corps-et-structure','Corps et structure','important','direct',[14,16,17,19,25,29],"Une valeur ne devient une réalité commune qu’en recevant un corps solide et une structure intelligente. Le texte relie explicitement cette incarnation à la capacité de durer, de transmettre et de faire vivre l’œuvre au-delà des individus."),
 T('purification-de-la-terre','Purification de la terre','important','direct',[30],"La conclusion demande de préparer une terre saine avant le cycle suivant : enlever les mauvaises racines devient l’image d’une clarification préalable à toute nouvelle semence et à toute nouvelle réalisation."),
]}}
def merge(e,n):
 by={t.get('themeId'):t for t in e}
 for t in n: by[t['themeId']]=t
 o={t['themeId']:i for i,t in enumerate(n)}
 return sorted(by.values(),key=lambda t:(0 if t.get('themeId') in o else 1,o.get(t.get('themeId'),999),t.get('themeId','')))
def main():
 d=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in d['psalmAnalyses']}
 for num,s in DEEP.items():
  if num not in by: continue
  by[num].update({'titleSignals':s['signals'],'themes':merge(by[num].get('themes',[]),s['themes']),'semanticDepth':'deep-content-grounded'})
 d['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number']); d['method']['semanticPass']='deepening-in-progress'; d['method']['deepPsalmCount']=sum(a.get('semanticDepth')=='deep-content-grounded' for a in d['psalmAnalyses']); PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Book 20 deep total={d['method']['deepPsalmCount']}")
if __name__=='__main__': main()
