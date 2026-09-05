#!/usr/bin/env python3
"""Deepen selected Psalm analyses in Gabriel book 18 from the authoritative PDF-derived corpus.

This pass replaces generic lexical relations with content-grounded teachings for Psalms already
read in detail. It is deliberately additive in scope: only audited Psalm numbers below are
replaced, all other analyses remain untouched. No prayer text or external source is used.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/thematic-index/books/book-18.json'

def T(theme_id,label,importance,directness,verses,teaching):
 return {'themeId':theme_id,'label':label,'importance':importance,'directness':directness,'verseNumbers':verses,'teaching':teaching}

DEEP={
123:{
 'titleSignals':['corps','juste place','âme','maîtrise','vertus'],
 'themes':[
  T('corps','Corps','central','direct',[1,2,3,4,5,6,7,8,10,12,13,14,15,16,17,18,19,20,21,22,23],"Le psaume décrit le corps comme pouvant devenir le centre qui gouverne toute la vie lorsqu'il est placé au-dessus des autres dimensions de l'être. Il demande non de le rejeter mais de le remettre à sa juste place."),
  T('juste-place-du-corps','Juste place du corps','central','direct',[7,12,13,18,20,21,22,23],"Le corps est présenté comme un outil et un serviteur qui doit être éduqué, apaisé et conduit par une intelligence supérieure plutôt que devenir le maître de la pensée, des sentiments et de la volonté."),
  T('ame','Âme','central','direct',[7,19],"Le texte oppose l'identification exclusive au corps à une vie intérieure tournée vers l'âme, qualifiée d'immortelle, dont le corps doit devenir le serviteur."),
  T('maitrise','Maîtrise','central','direct',[8,12,13,18,20,22,23],"La maîtrise consiste ici à limiter l'emprise du corps et de ses sens, à l'éduquer dans la sagesse et à stabiliser son activité afin qu'une autre intelligence puisse orienter la vie."),
  T('peur','Peur','important','direct',[3,8,22],"La peur est associée à l'identification au corps, à sa crainte de perdre sécurité et contrôle et à sa tendance à vouloir intervenir dans tous les mondes."),
  T('education-du-corps','Éducation du corps','important','direct',[12,13,22,23],"Le psaume présente le corps comme un apprenti qui peut être parlé, éduqué et imprégné de sagesse jusqu'à devenir un support stable plutôt qu'une source de confusion."),
  T('vertus','Vertus','important','direct',[14,15,17,18],"Les vertus sont présentées comme appartenant à un ordre supérieur que les intérêts du corps ne doivent pas détourner; le corps correctement placé peut au contraire leur servir de support."),
  T('service-impersonnel','Service impersonnel','important','direct',[14,17,18],"Le texte oppose l'appropriation corporelle des valeurs supérieures à une attitude de reconnaissance et de service pur et impersonnel."),
  T('monde-visible-et-invisible','Monde visible et monde invisible','important','direct',[4,7,10,21,22],"Le psaume demande de ne pas réduire la réalité au monde visible connu par le corps et d'élargir la vision à d'autres plans sans les ramener aux intérêts corporels."),
  T('meditation','Méditation','related','direct',[6,11,18],"La méditation est donnée comme moyen de recevoir une compréhension qui ne soit pas immédiatement ramenée au point de vue du corps."),
 ]},
124:{
 'titleSignals':['Nation Essénienne','naissance','conditions','incarnation','Alliance'],
 'themes':[
  T('nation-essenienne','Nation Essénienne','central','direct',[3,4,5,7],"La Nation Essénienne est présentée comme une réalité en cours de naissance et d'incarnation, dont l'apparition dans le monde demande un soutien concret et collectif."),
  T('naissance','Naissance','central','direct',[1,2,3],"Le psaume formule une loi de naissance: ce qui doit apparaître dans la vie a besoin de moyens, de préparation, d'éléments concordants, d'un espace et d'une terre capables de le porter."),
  T('conditions-de-manifestation','Conditions de manifestation','central','direct',[1,2,6],"Une idée ou un projet ne devient pas réalité par aspiration seule; les conditions de sa manifestation doivent être pensées, préparées et mises en place."),
  T('incarnation','Incarnation','important','direct',[3,4,5],"Le texte associe l'incarnation à la progression d'une réalité spirituelle jusqu'à une forme terrestre capable de porter son message et son œuvre."),
  T('terre','Terre','important','direct',[2,3,4,5],"La terre est décrite comme le lieu et le support nécessaires pour accueillir ce qui doit naître et pour rendre une œuvre réellement présente."),
  T('alliance','Alliance','important','direct',[5],"L'Alliance est présentée comme le cadre dans lequel les Esséniens reçoivent la tâche de rendre vivante sur terre une réalité qui ne l'était plus."),
  T('lois','Lois','important','direct',[6],"L'étude, la compréhension et l'application des lois sont posées comme conditions de la manifestation plutôt que comme simple savoir théorique."),
  T('lumiere','Lumière','important','direct',[4,6],"La Lumière doit disposer de conditions concrètes pour se manifester; le manque d'intérêt et d'application des lois est présenté comme pouvant affaiblir cette manifestation."),
 ]},
127:{
 'titleSignals':['œil','âme','eau','œuvres','regard'],
 'themes':[
  T('oeil','Œil','central','direct',[8,15,16,18,19,20],"L'œil est présenté comme une porte d'influence qui doit être éduquée et protégée jusqu'à devenir le reflet de l'âme plutôt qu'un regard qui condamne et détruit."),
  T('regard','Regard','central','direct',[15,16,17,18,20],"La manière de regarder est décrite comme une clé: un regard instable peut laisser entrer des influences, tandis qu'un regard éduqué s'appuie sur un corps et une vie structurés."),
  T('ame','Âme','central','direct',[18,20],"L'objectif explicite est que l'œil reflète l'âme; le texte relie cette qualité du regard à l'apparition d'un autre corps, qualifié de parfait."),
  T('oeuvres','Œuvres','central','direct',[1,2,4,5,10,12,13,17,18],"Les œuvres et les actes sont présentés comme les critères concrets qui révèlent ce qui inspire l'homme. Faire des œuvres permet aussi de se voir, de se corriger et de se structurer."),
  T('eau','Eau','central','direct',[3,6,7,8,10,14,15,29,30],"L'eau représente dans le psaume le milieu relationnel et intermédiaire dans lequel circulent influences et inspirations; sa clarté conditionne la capacité à discerner ce qui dirige la vie."),
  T('purete','Pureté','important','direct',[3,6,7,9,10,11,18,19],"La pureté est une condition de protection, d'inspiration et d'aboutissement des œuvres; elle concerne à la fois l'espace intérieur, les relations et les éléments consacrés."),
  T('inspiration','Inspiration','important','direct',[1,3,5,8,11],"Le psaume propose de juger l'inspiration non par une impression subjective mais par la qualité des actes, des œuvres et du milieu intérieur qui les produit."),
  T('protection','Protection','important','direct',[6,8,9,11,16,19],"La protection est liée à la préservation d'une eau claire, d'un endroit sacré, d'un corps structuré et d'un œil qui ne se laisse pas envahir."),
  T('influences','Influences','important','direct',[3,5,8,15],"Les influences peuvent entrer par le regard et affecter l'eau intérieure; le texte demande donc stabilité et discernement plutôt qu'une ouverture indistincte."),
  T('oeuvre-collective','Œuvre collective','important','direct',[10,17],"L'organisation et les œuvres communes sont présentées comme des moyens de renforcement mutuel et de construction d'une nouvelle culture."),
  T('quatre-elements','Quatre éléments','related','direct',[10,11],"Le texte relie eau, feu, air et terre à des cultes et à une consécration des lieux et œuvres, dans une logique de purification et de protection."),
  T('mauvais-oeil','Mauvais œil','related','direct',[20],"Le « mauvais œil » est explicitement opposé à l'œil reflet de l'âme et associé au jugement, à la destruction et à la mort."),
 ]},
128:{
 'titleSignals':['hérédité','responsabilité','lignée','générations','eau'],
 'themes':[
  T('heredite','Hérédité','central','direct',[4,5,8,9],"Le psaume distingue ce qui vient des actes propres de l'homme et ce qui lui est transmis par ses parents et sa lignée, présenté comme une matière reçue qu'il doit apprendre à gérer."),
  T('parents','Parents','central','direct',[4,5],"Les parents sont présentés comme transmettant non seulement une constitution mais aussi des conséquences de choix, pensées, attitudes et cadres collectifs qui participent à la formation de la vie de l'enfant."),
  T('responsabilite','Responsabilité','central','direct',[2,3,7,8,9],"La responsabilité porte à la fois sur la réponse donnée aux conséquences du passé et sur ce que l'homme choisit de transmettre ou de transformer pour les générations suivantes."),
  T('consequences-des-actes','Conséquences des actes','central','direct',[2,4,5],"Le texte présente certaines épreuves présentes comme conséquences d'actes antérieurs et insiste sur la manière actuelle d'y répondre plutôt que sur une idée d'injustice arbitraire."),
  T('lignee','Lignée','important','direct',[5],"La lignée devient un champ d'étude permettant de reconnaître des comportements, identités ou situations qui dépassent l'histoire individuelle immédiate."),
  T('generations','Générations','important','direct',[8,9],"Le psaume insiste sur la responsabilité de ne pas reproduire ni transmettre aux générations futures ce qui est jugé destructeur ou obscur."),
  T('eau','Eau','important','symbolic',[8],"La transmission générationnelle négative est décrite comme une eau sale à transformer en eau claire, sage, pure et vivante."),
  T('famille','Famille','important','direct',[9],"La famille est explicitement présentée comme quelque chose à protéger parce qu'elle est un lieu de passage d'un être à un autre."),
  T('sagesse','Sagesse','important','direct',[2,3],"La sagesse est la qualité recherchée dans la manière de rencontrer les conséquences du passé et d'utiliser les facultés reçues."),
  T('vies-anterieures','Vies antérieures','related','direct',[1,2,4],"Le psaume présente comme explication possible de certains éléments de la vie actuelle des actes ou vies appartenant à un passé plus lointain; l'index conserve cette affirmation comme contenu du texte."),
 ]},
131:{
 'titleSignals':['chercheur de Lumière','corps','opacité','service','catégories de chercheurs'],
 'themes':[
  T('chercheur-de-lumiere','Chercheur de Lumière','central','direct',[1,9,10,11,12,13,14,15,16,17,18,22,24],"Le psaume ne définit pas le chercheur par son discours mais par l'usage qu'il fait de la Lumière, son orientation concrète et la place qu'il donne aux intérêts du corps."),
  T('corps','Corps','central','direct',[2,3,4,7,8,9,10,14,15,16,19,20,21,31],"Le corps est présenté comme une force d'identification et d'interprétation qui peut ramener les enseignements à ses propres intérêts; le travail proposé consiste à reconnaître puis maîtriser cette influence."),
  T('opacite','Opacité','central','direct',[1,2,3,9,13,14,23,27,28],"L'opacité désigne dans ce psaume le monde ou la condition qui détourne la recherche de Lumière vers la conservation et les intérêts du monde humain et corporel."),
  T('service-de-la-lumiere','Service de la Lumière','central','direct',[10,11,15,17,26],"La distinction décisive est formulée entre utiliser la Lumière pour servir le corps et mettre sa vie, ses énergies et ses œuvres au service de la Lumière."),
  T('categories-de-chercheurs','Catégories de chercheurs','central','direct',[12,13,14,15,16,17,18],"Le texte distingue plusieurs catégories de chercheurs selon leur intention et leur rapport au corps: appropriation, recherche sincère mais partagée, bâtisseurs engagés et détachés tournés vers les mondes supérieurs."),
  T('impersonnalite','Impersonnalité','important','direct',[5,6,19],"Une dimension universelle et impersonnelle est opposée à l'isolement produit par l'identification exclusive à l'individualité corporelle."),
  T('maitrise','Maîtrise','important','direct',[15,19,22,31],"Maîtriser le corps signifie ici apaiser son influence, apprendre le détachement et créer les conditions pour comprendre les enseignements sans les ramener immédiatement à ses intérêts."),
  T('alliance','Alliance','important','direct',[14,17,22,24],"L'Alliance et un organisme collectif sont présentés comme des soutiens nécessaires pour qu'une recherche sincère ne soit pas reprise par les intérêts du corps et de l'opacité."),
  T('oeuvre','Œuvre','important','direct',[15,17,21,26],"Le type d'œuvre réellement accomplie sert de critère d'identité: le texte associe les bâtisseurs de Lumière à la construction, la protection et la réalisation concrète."),
  T('purete','Pureté','important','direct',[14,22,25,28,29],"La pureté concerne intention, relations, associations et milieu collectif; elle est présentée comme une condition de cheminement et non comme un simple état intérieur proclamé."),
  T('relations','Relations','important','direct',[25,27,28,29],"Les relations entre personnes se réclamant de la Lumière sont un test concret: tensions, luttes et eau relationnelle trouble contredisent la prétention affichée."),
  T('neutralite','Neutralité','related','direct',[19],"Le texte demande explicitement une attitude neutre et détachée des intérêts du corps afin de percevoir un autre monde sans imposer d'avance ses propres catégories."),
 ]},
}

def main():
 data=json.loads(PATH.read_text(encoding='utf-8')); by={a['number']:a for a in data.get('psalmAnalyses',[])}
 changed=0
 for num,spec in DEEP.items():
  if num not in by: continue
  by[num]['titleSignals']=spec['titleSignals']; by[num]['themes']=spec['themes']; by[num]['semanticDepth']='deep-content-grounded'; changed+=1
 data['psalmAnalyses']=sorted(by.values(),key=lambda a:a['number'])
 data.setdefault('method',{})['semanticPass']='deepening-in-progress'
 PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Deepened {changed} Psalm analyses in book 18')
if __name__=='__main__': main()
