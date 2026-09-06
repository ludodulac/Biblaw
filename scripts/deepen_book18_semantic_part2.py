#!/usr/bin/env python3
"""Second close semantic pass for Gabriel book 18, grounded only in PDF-derived source packs.

This pass deepens Psalms 129, 130 and 132-137. Psalm 131 and the earlier audited set remain
owned by deepen_book18_semantic.py. Only the listed Psalm analyses are replaced.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data' / 'thematic-index' / 'books' / 'book-18.json'


def T(theme_id, label, importance, directness, verses, teaching):
    return {
        'themeId': theme_id,
        'label': label,
        'importance': importance,
        'directness': directness,
        'verseNumbers': verses,
        'teaching': teaching,
    }


DEEP = {
129: {
    'titleSignals': ['nutrition', 'digestion', 'corps subtil', 'sommeil', 'destinée'],
    'themes': [
        T('nutrition-subtile', 'Nutrition subtile', 'central', 'direct', [5,8,10,11,12,17,21,26,28], "Le psaume élargit la nutrition au-delà de la nourriture physique : pensées, états d’âme, paroles, actes, relations et associations sont présentés comme des aliments qui entrent dans la constitution du corps et de la destinée."),
        T('digestion-subtile', 'Digestion subtile', 'central', 'direct', [10,11,16,17,21,22,23,24], "La digestion désigne le processus par lequel les éléments absorbés pendant la journée sont assimilés, répartis ou accumulés ; le sommeil est présenté comme un temps où cette activité change de monde et prépare le corps et la destinée du lendemain."),
        T('construction-du-corps', 'Construction du corps', 'central', 'direct', [1,2,3,5,6,8,10,14,16,17,32,36,37,38,46], "Le corps est présenté comme une structure à construire en correspondance avec ce que l’homme veut recevoir et vivre ; la qualité des éléments incorporés détermine la capacité à porter une vertu, une intelligence ou la Lumière."),
        T('activite-creatrice', 'Activité créatrice', 'central', 'direct', [13,14,15,27,28], "Le texte décrit l’homme comme créateur en permanence : respirer, penser, parler, regarder, vouloir et agir engendrent des influences et organisent des mondes qui, en retour, participent à sa propre formation."),
        T('sommeil', 'Sommeil', 'important', 'direct', [11,16,22,26,44,45], "Le sommeil n’est pas décrit comme un arrêt, mais comme le déplacement de l’activité dans un autre plan où les productions de la journée sont assimilées et où se prépare la capacité d’accéder ou non à des mondes plus légers."),
        T('dechets-subtils', 'Déchets subtils', 'important', 'direct', [22,23,24,29,30,44], "Le psaume appelle « déchets » les productions de pensée, parole ou action qui ne peuvent être assimilées ; leur accumulation est associée à un alourdissement de la vie et à des obstacles qui ferment l’accès aux mondes supérieurs."),
        T('destinee', 'Destinée', 'important', 'direct', [6,12,14,16,17,44], "La destinée est présentée comme se construisant avec les mêmes matériaux que le corps subtil : les influences et aliments reçus au cours de la journée deviennent le milieu dans lequel l’homme devra ensuite vivre."),
        T('nation-essenienne', 'Nation Essénienne', 'important', 'direct', [18,19,20], "La Nation Essénienne est décrite comme un milieu collectif comparable à une mère ou un placenta, destiné à offrir des éléments, une terre et un ciel permettant de construire un corps orienté vers les mondes supérieurs."),
        T('concentration', 'Concentration', 'important', 'direct', [33,34,35,41,43,46], "La concentration consiste à choisir une orientation, avancer concrètement et fidèlement, limiter les besoins et ne pas accumuler ce qui détourne de l’essentiel ; elle est reliée à la maîtrise de la vie."),
        T('tradition', 'Tradition', 'important', 'direct', [25,34,37,39,42,46], "Une tradition pure et vivante est présentée comme un milieu d’orientation et de protection dont les éléments doivent être incorporés et vécus, non simplement connus, afin de former un corps capable de porter la Lumière."),
    ],
},
130: {
    'titleSignals': ['mort', 'vie', 'corps', 'générosité', 'immortalité'],
    'themes': [
        T('mort', 'Mort', 'central', 'direct', [5,6,7,8,23,25,26,29,30,35,36,45,47], "Le psaume refuse de traiter la mort comme un simple événement final : il la relie à l’identification au corps mortel et aux conséquences de la manière dont l’homme emploie sa vie, ses facultés, ses actes et ses attachements."),
        T('vie', 'Vie', 'central', 'direct', [1,2,11,12,16,17,18,22,23,24,29,31,36,41,45], "La vie est présentée comme un don reçu de la Mère et des règnes, destiné à être développé et transmis ; le texte oppose une vie réduite à la conservation du corps à une vie qui devient génératrice, universelle et porteuse d’une continuité au-delà du corps."),
        T('corps-mortel', 'Corps mortel', 'central', 'direct', [4,5,7,8,13,16,17,18,19,23,27,36,37], "Le corps est décrit comme une partie mortelle de l’être et comme un moyen reçu pour construire autre chose ; le problème n’est pas d’en prendre soin, mais de concentrer toute l’existence sur sa conservation et ses intérêts."),
        T('corps-d-immortalite', 'Corps d’immortalité', 'central', 'direct', [13,17,18,27,31,32,34,37], "Le corps d’immortalité est présenté comme une construction concrète issue de l’usage du corps et de la vie reçus : pensées, sentiments, volonté, œuvres et relations doivent devenir des supports d’une vie plus vaste plutôt qu’une croyance abstraite."),
        T('generosite', 'Générosité', 'central', 'direct', [1,3,14,15,19,21,22,24,31,34], "La générosité est l’axe proposé pour passer d’une logique d’appropriation à une logique de vie : recevoir implique de faire fructifier et redistribuer, jusqu’à élargir l’existence au-delà des seuls intérêts individuels."),
        T('mere', 'Mère', 'important', 'direct', [1,2,3,14,16], "La Mère et les règnes sont présentés comme les donateurs des conditions mêmes de la vie terrestre ; le texte demande reconnaissance et réciprocité plutôt qu’une appropriation considérée comme allant de soi."),
        T('peur', 'Peur', 'important', 'direct', [5,7,9,10], "La peur est associée à l’identification exclusive au corps et au besoin de conserver ce qui est mortel ; le psaume oppose à cette peur un éveil dans le réel et une confrontation lucide avec la vérité."),
        T('responsabilite', 'Responsabilité', 'important', 'direct', [10,12,20,25,30,31,33,34], "La responsabilité consiste à regarder ce que l’on fait réellement de la vie reçue et à poser des actes qui construisent une continuité ; les croyances ou intentions ne remplacent pas cette réalisation concrète."),
        T('generations-futures', 'Générations futures', 'important', 'direct', [1,20,40,42,43,44], "Le texte déplace progressivement l’attention de la conservation personnelle vers la transmission : les générations précédentes sont appelées à ouvrir un chemin et soutenir la « jeune pousse » plutôt qu’à retenir leur place."),
        T('nation-essenienne', 'Nation Essénienne', 'related', 'direct', [32,33,34,44,46], "La Nation Essénienne est présentée comme une œuvre collective qui doit donner un corps concret à la Lumière et comme une nouvelle pousse appelée, dans le texte, à recevoir la place nécessaire pour se développer."),
    ],
},
132: {
    'titleSignals': ['réussite', 'échec', 'récompense', 'éternité', 'œuvre'],
    'themes': [
        T('reussite-et-echec', 'Réussite et échec', 'central', 'direct', [1,2,4,5,6,8,9], "Le psaume relativise les critères immédiats de réussite et d’échec : un résultat favorable dans le présent peut se renverser avec le temps, tandis qu’un échec apparent peut produire guérison, libération ou bénédiction dans une temporalité plus vaste."),
        T('recompense', 'Récompense', 'central', 'direct', [1,2,6,8,9,10,13,14,16], "La récompense n’est pas réduite à un avantage physique immédiat ; le texte distingue les résultats relevant des lois matérielles d’une réserve ou d’un fruit placé dans d’autres mondes et rencontré plus tard."),
        T('eternite', 'Éternité', 'central', 'direct', [4,6,9,14,19,20,22,23,27,28,29,30], "L’éternité fournit le changement de perspective central du psaume : une œuvre est évaluée selon ce qu’elle peut faire vivre au-delà du temps individuel, des apparences et de la seule mémoire personnelle."),
        T('oeuvre', 'Œuvre', 'central', 'direct', [7,18,19,22,23,24,25,27,28,29,30], "L’œuvre est présentée comme le lieu où l’homme constitue un capital de sens qui peut dépasser sa vie physique ; sa valeur tient à sa capacité à ouvrir un chemin, servir d’autres générations et entrer en résonance avec un monde supérieur."),
        T('mort', 'Mort', 'important', 'direct', [10,11,12,14,15,16], "La mort est décrite comme une frontière du corps et une étape où l’homme rencontre les conséquences et affinités qu’il a construites ; elle ne clôt donc pas, dans la logique interne du texte, l’évaluation de la réussite."),
        T('affinites', 'Affinités', 'important', 'direct', [16,17], "Après la mort, le texte dit que l’homme demeure dans les régions correspondant aux affinités cultivées pendant la vie ; ciel, terre, liens et œuvres deviennent ainsi la matière de sa future demeure."),
        T('generations-futures', 'Générations futures', 'important', 'direct', [18,23,25,26,27,29,30], "Une œuvre réussie est notamment celle qui traverse les générations en leur donnant des concepts, une culture, une orientation ou un accès à une conscience plus haute."),
        T('resonance', 'Résonance', 'important', 'symbolic', [28,29,30], "L’œuvre est comparée à un mot dont l’écho traverse les mondes : la résonance sert d’image pour décrire la continuité d’une action qui demeure active longtemps après son accomplissement initial."),
        T('simplicite', 'Simplicité', 'related', 'direct', [13,14,20], "Pour le plan physique, le psaume recommande d’appliquer simplement les lois correspondantes et de ne pas confondre confort matériel immédiat avec accomplissement dans l’éternité."),
    ],
},
133: {
    'titleSignals': ['vertus', 'Anges', 'fleurs', 'eau', 'transformation'],
    'themes': [
        T('vertus', 'Vertus', 'central', 'direct', [1,3,7,8,9,10,11,12,13,16,17,18], "Les vertus constituent le remède et le milieu de transformation central du psaume : elles doivent être cultivées comme des réalités supérieures capables de purifier l’eau des relations et de transformer progressivement la conscience et le comportement."),
        T('fleur', 'Fleur', 'central', 'symbolic', [1,2,3,5,16], "La fleur représente les vertus et sert de modèle d’offrande : beauté, parfum et floraison illustrent une vie qui reçoit une bénédiction puis offre son être pour embellir un monde plus vaste."),
        T('anges', 'Anges', 'central', 'direct', [7,12,18], "Vivre avec les Anges signifie ici s’orienter vers des vertus plus hautes que les habitudes ordinaires et leur donner un milieu concret où elles puissent agir et purifier la vie."),
        T('eau', 'Eau', 'central', 'direct', [6,9,13,14,15,18,22], "L’eau désigne le milieu relationnel et vital qui peut être pollué par l’inconscience ou régénéré par les vertus ; le psaume demande d’en préserver un espace pur capable de recevoir la bénédiction de Gabriel."),
        T('relations', 'Relations', 'important', 'direct', [7,13,14,24,31], "Les relations sont traitées comme une eau commune : jalousie, jugement et tensions la polluent, tandis que fraternité, soutien mutuel, respect et clarté permettent sa régénération."),
        T('transformation', 'Transformation', 'important', 'direct', [10,17,18,20,21,48], "La transformation proposée ne consiste pas à combattre obsessionnellement le sombre ni à transformer l’autre, mais à renforcer ce qui est bon, tirer une sagesse des expériences et réorienter concrètement la vie."),
        T('discernement', 'Discernement', 'important', 'direct', [19,20,21,47,48,49], "Le discernement demande de voir clairement le mauvais sans lui donner une énergie émotionnelle supplémentaire : constater, mettre des filtres, éviter l’obstacle et revenir à une orientation constructive."),
        T('bien-commun', 'Bien commun', 'important', 'direct', [7,24,31,51,52], "Le texte élargit la culture des vertus à une responsabilité collective : étudier, partager les fruits du travail et rendre vivante l’idée d’un monde meilleur doivent servir le Bien commun."),
        T('purete', 'Pureté', 'important', 'direct', [13,14,15,18,24,50], "La pureté concerne l’eau intérieure et relationnelle ainsi que les espaces d’étude ; elle est présentée comme une condition pour que les vertus et une influence supérieure puissent être accueillies sans être déformées."),
    ],
},
134: {
    'titleSignals': ['22 commandements', '22 portes', 'corps de Lumière', 'pratique', 'gardiens'],
    'themes': [
        T('22-commandements', '22 commandements', 'central', 'direct', [1,2,3,5,6,7,8,12,13,14,16,21,26,28,29,30,33], "Les 22 commandements sont présentés comme un chemin pratique et progressif : chacun correspond à une étape, une porte, une relation et un apprentissage que l’homme doit incorporer plutôt que simplement réciter."),
        T('pratique', 'Pratique', 'central', 'direct', [5,6,7,8,12,15,16,18,20,25,29,30], "La pratique transforme le commandement en structure vécue : c’est l’application consciente dans les actes et dans le corps qui constitue la réponse permettant de franchir l’étape suivante."),
        T('corps-de-lumiere', 'Corps de Lumière', 'central', 'direct', [5,6,14,15,27,28,29,33], "Le corps de Lumière est décrit comme le résultat progressif de 22 organes ou relations constitués par la pratique ; l’homme acquiert ainsi, selon le texte, une consistance adaptée aux mondes qu’il veut traverser."),
        T('portes-et-gardiens', 'Portes et gardiens', 'central', 'direct', [3,4,13,14,15,16,28,30,33], "Chaque étape est figurée par une porte et un gardien : le passage dépend de la compréhension, de la conscience, de l’attitude et du corps que l’homme a réellement formés à cette étape."),
        T('conscience', 'Conscience', 'important', 'direct', [16,17,30,31,32,33], "La perfection n’est pas exigée à chaque marche, mais la conscience, la juste compréhension et l’intention ne doivent pas manquer ; l’humilité est donnée comme réponse lorsque la force fait défaut."),
        T('anti-fanatisme', 'Refus du fanatisme', 'important', 'direct', [7], "Le psaume interdit explicitement l’obéissance aveugle et le fanatisme : les commandements doivent conduire à l’intelligence et à l’équilibre, non à une application mécanique."),
        T('transmission', 'Transmission', 'important', 'direct', [2,18,19,20,23,25], "La pratique est présentée comme une empreinte laissée aux générations suivantes ; transmettre ne signifie donc pas seulement conserver le texte mais stabiliser un chemin praticable et vivant."),
        T('soutien-mutuel', 'Soutien mutuel', 'important', 'direct', [8,17,25], "Le soutien mutuel accompagne la pratique parce que le chemin est décrit comme collectif autant qu’individuel : pureté, vérité et entraide renforcent la possibilité de maintenir le lien avec la Tradition."),
        T('alliance', 'Alliance', 'important', 'direct', [14,21,23,25], "Les 22 portes sont aussi décrites comme 22 alliances ou relations entre mondes ; l’Alliance devient vivante lorsque l’enseignement est mis en pratique et reçoit une forme dans la vie."),
    ],
},
135: {
    'titleSignals': ['océan', 'stabilité', 'Tradition', 'influences', 'immortalité'],
    'themes': [
        T('stabilite', 'Stabilité', 'central', 'direct', [2,4,8,9,10,11,12,13,14,16,18,19], "Face à un monde comparé à un océan de courants et de tempêtes, le psaume présente la stabilité comme une capacité à se recentrer sur un fondement durable, retrouver le calme et choisir ensuite une réponse adaptée."),
        T('tradition', 'Tradition', 'central', 'direct', [4,5,6,7,8,11,12,13,14,16,17,22,23,24,25,27,29,34,35], "La Tradition est le fondement proposé pour ne plus dériver au gré des influences : elle doit devenir un corps, une pratique et une identité incarnés plutôt qu’un simple ensemble d’idées extérieures."),
        T('influences', 'Influences', 'central', 'direct', [1,3,8,9,11,14,18,19,20], "Les influences sont comparées à des courants qui peuvent désorienter pensées, sentiments et décisions ; la vigilance consiste à reconnaître leur nature avant d’agir plutôt qu’à nier leur impact."),
        T('ocean', 'Océan', 'important', 'symbolic', [1,3,8,14], "L’océan symbolise le milieu mouvant du monde humain : courants, tempêtes et vagues donnent une image des conditions changeantes dans lesquelles l’homme doit apprendre à naviguer avec conscience."),
        T('vigilance', 'Vigilance', 'important', 'direct', [14,18,19,20], "La vigilance du sage consiste à détecter les perturbations, revenir au calme, observer leur amplitude et préparer une réponse proportionnée qui préserve la liberté de mouvement."),
        T('incorporation', 'Incorporation', 'important', 'direct', [8,13,14,24,27], "L’incorporation signifie faire entrer gestes, souffle, pensée et activité dans la Tradition jusqu’à ce que la pratique ne soit plus intermittente mais devienne la forme même de la vie."),
        T('immortalite', 'Immortalité', 'important', 'direct', [6,7,8,12,15,16,24,26,29], "L’immortalité est reliée à ce qui peut demeurer au-delà du temps : une vie concentrée sur des valeurs stables, une lignée et une pratique capables de traverser les changements plutôt que des productions soumises aux courants du moment."),
        T('serenite', 'Sérénité', 'important', 'direct', [10,11,14], "La sérénité est une pratique active : calmer le système intérieur permet de retrouver lucidité et compréhension avant de se repositionner dans une situation agitée."),
        T('identite-essenienne', 'Identité essénienne', 'related', 'direct', [27,28,29], "L’identité essénienne est décrite comme un état incorporé et durable : si elle dépend des circonstances du jour, le texte considère qu’elle n’a pas encore été réellement constituée."),
    ],
},
136: {
    'titleSignals': ['eau subtile', 'poches d’eau', 'relations', 'libération', 'pensées'],
    'themes': [
        T('eau-subtile', 'Eau subtile', 'central', 'direct', [1,2,3,4,5,8,13,21,22], "Le psaume décrit autour de l’homme une eau subtile, vivante et relationnelle qui sert de milieu aux échanges, pensées et influences ; sa qualité se lit notamment dans la fluidité ou la crispation des relations."),
        T('poches-d-eau-polluee', 'Poches d’eau polluée', 'central', 'direct', [5,6,7,8,10,11,14,15,16,22,34,35,40], "Les « poches » désignent des zones d’eau séparées du courant universel, stagnantes et autoentretenues ; elles sont associées à des blocages personnels ou collectifs qui finissent par alourdir la vie et interrompre la communication."),
        T('relations', 'Relations', 'central', 'direct', [4,10,16], "Les relations servent de diagnostic concret de l’état de l’eau : clarté, dialogue et échange indiquent une circulation vivante, tandis que tensions et oppositions signalent une stagnation ou une pollution."),
        T('liberation', 'Libération', 'central', 'direct', [6,8,10,15,26,34,35,40], "Se libérer consiste à percer les poches, laisser leur contenu se diluer et accepter une phase parfois difficile de désagrégation de l’ancien blocage plutôt qu’à maintenir ce qui s’est amalgamé à l’identité."),
        T('pensee', 'Pensée', 'important', 'direct', [19,20,21,22,23,24,25,26,27], "Les pensées colorent l’eau qui baigne la vie ; le texte distingue celles qui viennent d’une orientation supérieure, celles issues de l’Enseignement et celles qui restent non résolues, chacune demandant un travail différent."),
        T('neutralite', 'Neutralité', 'important', 'direct', [20], "L’observation des pensées doit se faire sans jugement ni réaction émotionnelle automatique, afin de ne pas ajouter une nouvelle coloration à l’eau que l’on cherche justement à comprendre et purifier."),
        T('sante', 'Santé', 'important', 'direct', [21,22], "La santé est définie comme une circulation libre : une pensée issue d’une intelligence supérieure traverse l’âme, la conscience et l’eau jusqu’aux activités concrètes sans être capturée par une poche stagnante."),
        T('bien-commun', 'Bien commun', 'important', 'direct', [11,12,13,14,17], "Le savoir de l’eau est étendu aux familles, peuples et à l’humanité ; le culte de l’eau et la pédagogie sont présentés comme un service collectif visant à prévenir l’accumulation de blocages à grande échelle."),
        T('objectifs', 'Objectifs', 'related', 'direct', [40,41,42], "La sortie des anciennes poches suppose un choix : nettoyer la vie, décider ce qui mérite d’être conservé et donner à un objectif clair les conditions nécessaires pour prendre une forme concrète."),
    ],
},
137: {
    'titleSignals': ['travail', 'responsabilité', 'organisation', 'œuvre collective', 'Alliance'],
    'themes': [
        T('part-du-travail', 'Part du travail', 'central', 'direct', [1,2,3,4,5,6,7,11,21], "Le psaume insiste sur une réciprocité de l’Alliance : les autres règnes sont décrits comme ayant leur tâche, mais la manifestation attendue ne peut se poursuivre si les hommes ne réalisent pas concrètement la leur."),
        T('responsabilite', 'Responsabilité', 'central', 'direct', [3,4,7,10,11,17,19,21], "La responsabilité est présentée comme le passage de l’attente à l’action : reconnaître les conséquences du désordre, prendre l’avenir en mains et tenir sa fonction sans laisser l’inconscience ou le laisser-aller polluer l’ensemble."),
        T('organisation', 'Organisation', 'central', 'direct', [7,8,10,11,14,15,16,17,20,24], "L’organisation n’est pas un thème administratif secondaire : mettre de l’ordre dans les activités terrestres est explicitement relié à la possibilité de dégager le « ciel », stabiliser l’œuvre et créer les conditions d’une approche du monde supérieur."),
        T('oeuvre-collective', 'Œuvre collective', 'central', 'direct', [7,9,11,15,16,20,21,22,23,24], "L’œuvre collective demande que chacun trouve sa place, s’y tienne et apporte une compétence réelle ; le texte oppose cette construction commune à l’isolement et au repli dans les intérêts personnels."),
        T('alliance', 'Alliance', 'important', 'direct', [1,2,6,7,8], "L’Alliance est décrite comme une coopération entre plusieurs règnes dans laquelle l’unité n’efface pas les rôles : chaque partie doit accomplir sa fonction pour que l’ensemble puisse se stabiliser."),
        T('lumiere', 'Lumière', 'important', 'direct', [3,4,5,6], "La Lumière doit, selon le psaume, recevoir un corps stable par des œuvres et des conditions suffisamment claires ; sa manifestation n’est donc pas présentée comme automatique ou indépendante du travail humain."),
        T('solidarite', 'Solidarité', 'important', 'direct', [7,9,16,18,19], "La solidarité vise à empêcher l’isolement et à faire de chacun une source d’eau claire pour l’ensemble ; elle est reliée à la prospérité commune plutôt qu’à une addition d’intérêts individuels."),
        T('ordre', 'Ordre', 'important', 'direct', [10,14,15,20,24], "Le psaume relie explicitement l’ordre terrestre et la clarté du ciel : régler les dysfonctionnements, simplifier les activités et trouver rapidement des solutions deviennent des conditions de solidité de l’œuvre."),
        T('prosperite', 'Prospérité', 'related', 'direct', [18,19], "La prospérité est figurée comme une eau reçue qui doit circuler vers l’ensemble ; elle peut être polluée par irresponsabilité et manque de solidarité ou devenir une bénédiction transmissible lorsque la structure est claire."),
    ],
},
}


def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    by_number = {a['number']: a for a in data.get('psalmAnalyses', [])}
    changed = 0
    for num, spec in DEEP.items():
        if num not in by_number:
            continue
        analysis = by_number[num]
        analysis['titleSignals'] = spec['titleSignals']
        analysis['themes'] = spec['themes']
        analysis['semanticDepth'] = 'deep-content-grounded'
        changed += 1
    data['psalmAnalyses'] = sorted(by_number.values(), key=lambda a: a['number'])
    method = data.setdefault('method', {})
    method['semanticPass'] = 'deepening-in-progress'
    method['deepPsalmCount'] = sum(1 for a in data['psalmAnalyses'] if a.get('semanticDepth') == 'deep-content-grounded')
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Deepened {changed} additional Psalm analyses in book 18; deep total={method["deepPsalmCount"]}')


if __name__ == '__main__':
    main()
