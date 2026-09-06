#!/usr/bin/env python3
"""First close semantic pass for Raphael book 19 from PDF-derived source packs only.

The pass is conservative: it replaces/adds audited central relations for the listed Psalms while
retaining other already grounded secondary relations. Prayer text is not used.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data' / 'thematic-index' / 'books' / 'book-19.json'


def T(theme_id, label, importance, directness, verses, teaching):
    return {'themeId': theme_id, 'label': label, 'importance': importance, 'directness': directness,
            'verseNumbers': verses, 'teaching': teaching}


DEEP = {
102: {
 'signals': ['pensées vivantes','trois degrés','destinée','conscience','corps de sagesse'],
 'themes': [
  T('pensee-vivante','Pensée vivante','central','direct',[1,2,3,8],"Le psaume présente la pensée comme une réalité vivante et agissante dont les paroles, actes et œuvres physiques ne sont que les manifestations visibles; penser engage donc déjà une création et une destinée."),
  T('trois-degres-de-pensee','Trois degrés de pensée','central','direct',[4,5,6,7],"Le texte distingue une pensée mécanique et instinctive, une pensée réfléchie qui construit des cycles de cause à effet, puis une pensée dite divine, consciente et constructrice, associée à la méditation et à l'immortalité."),
  T('destinee','Destinée','central','direct',[6,7,8,10,19],"La destinée est décrite comme se construisant avec les pensées auxquelles l'homme s'associe; elles précèdent sentiments et actes et finissent par organiser le futur dans lequel il devra vivre."),
  T('conscience','Conscience','important','direct',[5,6,7,9,12,13,16,17,19],"La conscience permet de ne plus être simplement animé par des pensées automatiques ou empruntées; elle doit s'étendre à la pensée et à l'acte pour que l'homme puisse discerner ses associations et construire volontairement sa vie."),
  T('mauvaises-pensees','Mauvaises pensées','important','direct',[10,11,12,13,14,15],"La mauvaise pensée est décrite comme une association qui peut se déguiser, gagner de la puissance par l'homme et devenir agissante; la réponse proposée est l'éveil, l'étude, la vigilance et la séparation d'avec ce monde plutôt que la simple bonne intention."),
  T('corps-de-sagesse','Corps de sagesse','important','direct',[12,16,17,19],"L'étude et l'incorporation des paroles de sagesse doivent constituer un corps intérieur capable de stabiliser pensée et agir; ce corps est présenté comme la condition pour traverser les épreuves et s'orienter vers une vie immortelle."),
 ]},
103: {
 'signals': ['communication','langage universel','écoute','adaptation','unification'],
 'themes': [
  T('communication','Communication','central','direct',[1,2,3,5,8,13,14,16,17,18,20,22,23],"La communication est définie comme une capacité à entrer en relation sans imposer son propre monde: comprendre son interlocuteur, adapter le langage, écouter clairement et ouvrir un échange permettant une compréhension plus large."),
  T('langage-universel','Langage universel','central','direct',[3,4,5,6,7,15,17],"Le langage de l'humanité est présenté comme un alphabet de l'univers: apprendre à comprendre les différences humaines devient la première école nécessaire avant de prétendre communiquer avec d'autres règnes ou mondes."),
  T('parole-vraie','Parole vraie','important','direct',[9,10,11,12,23],"La parole juste demande de ne pas se cacher derrière des mots, masques ou opinions variables; elle part d'une identité intérieure stable tout en sachant se rendre compréhensible à l'autre."),
  T('ecoute','Écoute','important','direct',[17,18,22,23],"Écouter consiste à recevoir le message sans y projeter immédiatement ses convictions, son aura ou son besoin de se défendre; la sérénité permet de traverser les apparences pour entendre ce qui est réellement communiqué."),
  T('adaptation-sans-perte-identite','Adaptation sans perte d’identité','important','direct',[3,5,11,13],"Le texte distingue l'adaptation du langage de la versatilité: il faut rencontrer l'autre à son niveau sans abandonner la clarté de ce que l'on est ni changer de fond selon la situation."),
  T('unification-des-mondes','Unification des mondes','important','direct',[14,19,20,22,23],"La communication a pour finalité de créer une terre commune et d'unifier des mondes différents; elle est comparée à un instrument capable de faire apparaître un monde plutôt qu'à un moyen d'imposer une opinion."),
 ]},
104: {
 'signals': ['pensée angélique','respiration','ciel de pensée','affinités','étude sacrée'],
 'themes': [
  T('pensee-angelique','Pensée angélique','central','direct',[1,4,5,6,7,8,9,23,24,25,26],"La pensée angélique désigne des pensées élevées et vivantes qui ne peuvent être réduites à des idées abstraites: elles demandent une atmosphère, une étude et une discipline capables de leur donner un corps dans la vie humaine."),
  T('respiration-et-pensee','Respiration et pensée','central','direct',[2,3,4,7,10,11],"Le psaume relie la pensée au souffle, à l'air et au sang: l'atmosphère de pensées entretenue autour de l'homme imprègne son corps et sa destinée comme l'air respiré nourrit et circule dans l'organisme."),
  T('ciel-de-pensee','Ciel de pensée','central','direct',[2,3,12,13],"Chaque homme est décrit comme portant un ciel formé par les pensées et influences qu'il entretient; ce ciel attire par affinité des êtres et atmosphères semblables et tend ensuite à renforcer les mêmes habitudes."),
  T('affinites','Affinités','important','direct',[3,10,12,13],"Les affinités expliquent la formation de milieux collectifs de pensée: des atmosphères semblables se rejoignent et peuvent enfermer l'homme dans un seul monde ou, au contraire, l'ouvrir à des pensées plus hautes."),
  T('etude-sacree','Étude sacrée','important','direct',[9,10,11,23,24,25,26],"L'étude sacrée est présentée comme un service qui renouvelle la pensée et donne un corps au savoir; elle ne vise pas l'accumulation personnelle mais l'accueil conscient d'une intelligence à rendre vivante sur la terre."),
  T('liberation-par-la-pensee','Libération par la pensée','important','direct',[8,9,10,13,26],"Certaines pensées enferment et d'autres libèrent; le passage proposé vers une pensée libératrice associe éveil de la conscience, étude, discipline, repos et pratiques destinées à desserrer l'emprise des habitudes négatives."),
 ]},
105: {
 'signals': ['signes','projection','actes','réalité','subtilité'],
 'themes': [
  T('signes-de-la-vie','Signes de la vie','central','direct',[1,2,10,11,16,18],"Le psaume critique la tendance à interpréter automatiquement événements, animaux ou épreuves comme des messages personnels du monde supérieur; il demande de distinguer la vie ordinaire, les conséquences des actes et une véritable approche du monde divin."),
  T('projection','Projection','central','direct',[1,2,3,10,15,16,18],"La projection consiste à chercher dans le monde extérieur la confirmation de son identité, de sa valeur ou de ses croyances; le texte la présente comme une source d'illusion qui empêche de regarder sa propre vie avec justesse."),
  T('actes-comme-critere','Actes comme critère','central','direct',[6,9,13,14,15,16,17],"Pour savoir qui l'on est et sur quel chemin on marche, le psaume renvoie aux actes et aux œuvres plutôt qu'aux signes, discours ou consolations recherchées dans l'invisible."),
  T('realite','Réalité','important','direct',[3,12,17,18,19,21,22],"La sagesse est associée au retour au réel: être concret dans son monde, assumer ce que l'on fait et sortir des récits qui servent seulement à rassurer ou préserver une fausse identité."),
  T('maitrise-de-la-vie-interieure','Maîtrise de la vie intérieure','important','direct',[8,9,20],"Étude et discipline doivent permettre d'observer et de maîtriser pensées, sentiments et attitudes afin de ne plus se cacher derrière des apparences ni dépendre du regard supposé d'un monde supérieur."),
  T('subtilite-concrete','Subtilité concrète','important','direct',[19,20,21],"Le psaume distingue une subtilité enracinée dans l'harmonie du corps et de la vie d'une spiritualité abstraite; cette subtilité concrète est présentée comme une porte naturelle vers une sagesse plus vaste."),
 ]},
106: {
 'signals': ['alchimie','éphémère','immortalité','terre','transformation'],
 'themes': [
  T('alchimie-interieure','Alchimie intérieure','central','symbolic',[5,9,14,20,21],"L'alchimie décrit la transformation de l'homme brut et périssable en un être capable de porter une continuité: l'image du plomb devenu métal incorruptible exprime un travail conscient effectué dans la vie terrestre."),
  T('ephemere-et-immortel','Éphémère et immortel','central','direct',[2,5,10,14,15,17,20,21],"Le psaume demande de connaître simultanément les lois de l'éphémère et de l'immortalité: l'expérience du temps et de la perte devient le terrain où l'homme peut choisir ce qui mérite d'être transformé en support durable."),
  T('mission-de-l-homme','Mission de l’homme','central','direct',[2,3,4,6,11,12,13],"L'homme est présenté comme placé à la frontière du visible et de l'invisible afin d'agir en créateur: son travail consiste à libérer plutôt qu'enfermer et à conduire pensées, paroles, actes et matière vers une évolution supérieure."),
  T('terre','Terre','important','direct',[6,7,8,19],"La terre n'est pas un lieu à fuir: l'évolution de l'homme et celle de la terre sont dites indissociables, et l'ascension doit emporter avec elle le monde concret plutôt que l'abandonner."),
  T('corps-d-immortalite','Corps d’immortalité','important','direct',[4,12,15,16,17,19],"Le corps d'immortalité est la stabilité construite à partir des expériences, de l'étude et des œuvres; il doit permettre de conserver conscience et mémoire au-delà de la disparition du corps physique."),
  T('incarnation','Incarnation','important','direct',[4,5,12,13],"L'incarnation est présentée comme la condition même du travail: la mission ne s'accomplit pas en s'évadant dans l'invisible mais en transformant la pensée, la parole, l'acte et le corps au sein du monde terrestre."),
 ]},
107: {
 'signals': ['fleur','animal','concepts','communication avec les règnes','libération'],
 'themes': [
  T('relation-directe-aux-regnes','Relation directe aux règnes','central','direct',[1,2,3,4,5,9,10,11],"Le psaume demande de rencontrer fleurs, animaux et autres êtres sans interposer immédiatement les concepts appris; la communication recherchée part d'une présence partagée et d'une relation réelle plutôt que d'une interprétation symbolique automatique."),
  T('concepts-et-conditionnement','Concepts et conditionnement','central','direct',[1,2,4,5,9,26],"Les concepts transmis par la culture peuvent isoler l'homme de ce qu'il rencontre et de lui-même; le texte demande de discerner ce qui relève d'une sagesse durable de ce qui reproduit seulement les projections et rêves hérités."),
  T('fleur','Fleur','important','symbolic',[2,3,4,7,8],"La fleur enseigne par sa manière d'être: elle partage un espace, fleurit et donne une forme à ce qu'elle est; le psaume en fait un modèle de croissance et d'apparition dans un monde supérieur sans la réduire à un simple présage."),
  T('animaux','Animaux','important','direct',[9,10,11],"L'animal n'est présenté ni comme bon ni comme mauvais en fonction des projections humaines; sa présence rappelle la coexistence des règnes et invite à partager et harmoniser l'espace de vie."),
  T('fraternite-universelle','Fraternité universelle','important','direct',[7,10,11],"La fraternité s'élargit au-delà des seuls humains: reconnaître les autres règnes comme parties d'une même vie permet d'ouvrir les sentiments et les sens à une famille plus vaste."),
  T('transmission','Transmission','important','direct',[26,27,28,29],"Le psaume demande de ne transmettre des héritages que ce qui rend libre et sage; la libération des mondes commence par se dégager soi-même des conditionnements qui reproduisent la bêtise et l'enfermement."),
 ]},
108: {
 'signals': ['mémoire','évolution','règnes','voyageur','Tradition'],
 'themes': [
  T('memoire-vivante','Mémoire vivante','central','direct',[1,2,3,5,8,12,13,14,16,20,22,25,28,30,32],"La mémoire est beaucoup plus qu'un souvenir biographique: elle est présentée comme la continuité vivante du voyage à travers les règnes et comme la condition pour connaître son origine, sa tâche et l'étape suivante de l'évolution."),
  T('evolution-des-regnes','Évolution des règnes','central','direct',[5,6,7,9,10,11,12,18,21,23,31,32],"Le psaume expose une évolution où le voyageur traverse minéral, végétal, animal et humain avant de s'orienter vers l'état angélique; l'étape supérieure doit intégrer et élever les expériences des étapes précédentes."),
  T('etre-eternel-et-voyageur','Être éternel et voyageur','central','direct',[4,9,30],"Deux dimensions sont distinguées: un être éternel, au-delà de la naissance, et un voyageur fragmenté qui traverse les mondes et doit retrouver progressivement l'intelligence du corps total."),
  T('tradition-comme-corps-de-memoire','Tradition comme corps de mémoire','important','direct',[13,14,15,20,21,24,25],"La Tradition est décrite comme le corps collectif capable de porter le souvenir sacré à travers le temps; étude, rites, dévotion et œuvre doivent y reconstruire une mémoire que l'individu isolé a perdue."),
  T('immortalite','Immortalité','important','direct',[1,3,17,20,21,22,26,30,31],"L'immortalité est reliée à la continuité consciente du voyage: conserver l'intelligence acquise, constituer un autre corps et pouvoir poursuivre l'évolution sans être enfermé dans l'identité humaine actuelle."),
  T('unite-des-mondes','Unité des mondes','important','direct',[10,11,18,22,31],"L'ascension doit réunir ce qui a été traversé: l'homme élève avec lui les formes de vie et leur intelligence plutôt que de s'en séparer, jusqu'à retrouver une unité plus vaste."),
 ]},
110: {
 'signals': ['union','Alliance','Enseignement','œuvre collective','liberté'],
 'themes': [
  T('union','Union','central','direct',[1,4,5,6,8,9,16,20,22,30,31,32,33,34],"Le psaume présente l'union comme une condition de réalisation plutôt qu'un idéal abstrait: les forces, qualités et compétences individuelles doivent être mises en commun pour qu'une œuvre assez forte puisse réellement franchir les limites du monde humain."),
  T('alliance','Alliance','central','direct',[5,8,20,21,26,27,30],"L'Alliance est le cadre de rencontre entre des mondes décrits comme incompatibles sans médiation; elle doit recevoir un corps concret par des personnes, lieux, pratiques et structures qui la rendent habitable."),
  T('enseignement-comme-mediateur','Enseignement comme médiateur','central','direct',[8,9,10,17,30,34],"L'Enseignement est présenté comme le point de compatibilité entre le monde humain et le monde divin: l'incorporer collectivement doit créer le corps de liaison permettant l'ouverture d'un passage."),
  T('oeuvre-collective','Œuvre collective','important','direct',[9,11,16,17,24,32,33,34,35,36],"L'œuvre collective transforme l'union en réalisation: chacun offre talents et moyens pour construire une autre manière de vivre et un chemin qui puisse rester accessible aux êtres venant après."),
  T('liberte','Liberté','important','direct',[16,17,18,20,21],"La liberté est reliée à l'existence d'un choix réel entre plusieurs façons de vivre; le texte craint qu'une absence de corps collectif de la sagesse laisse l'homme prisonnier d'un seul système et d'influences qu'il ne maîtrise plus."),
  T('preparation','Préparation','important','direct',[22,25,26,27,28,29,30],"La préparation consiste à ne pas attendre passivement l'épreuve: vivre déjà dans un monde de sagesse, disposer de repères et de lieux concrets doit permettre de trouver une réponse lorsque les conditions deviennent difficiles."),
 ]},
}


def merge_themes(existing, replacements):
    by = {t.get('themeId'): t for t in existing}
    for theme in replacements:
        by[theme['themeId']] = theme
    # audited central relations first, then retained grounded secondary relations
    order = {t['themeId']: i for i, t in enumerate(replacements)}
    return sorted(by.values(), key=lambda t: (0 if t.get('themeId') in order else 1,
                                              order.get(t.get('themeId'), 999),
                                              t.get('themeId','')))


def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    by_number = {a['number']: a for a in data.get('psalmAnalyses', [])}
    changed = 0
    for num, spec in DEEP.items():
        if num not in by_number:
            continue
        a = by_number[num]
        a['titleSignals'] = spec['signals']
        a['themes'] = merge_themes(a.get('themes', []), spec['themes'])
        a['semanticDepth'] = 'deep-content-grounded'
        changed += 1
    data['psalmAnalyses'] = sorted(by_number.values(), key=lambda a: a['number'])
    method = data.setdefault('method', {})
    method['semanticPass'] = 'deepening-in-progress'
    method['deepPsalmCount'] = sum(1 for a in data['psalmAnalyses'] if a.get('semanticDepth') == 'deep-content-grounded')
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Deepened {changed} Psalm analyses in book 19; deep total={method["deepPsalmCount"]}')


if __name__ == '__main__':
    main()
