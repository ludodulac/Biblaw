#!/usr/bin/env python3
"""First close semantic pass for Ouriel book 20 from PDF-derived source packs only.

The pass is conservative: it replaces/adds audited central relations for Psalms 104-107 while
retaining other already grounded secondary relations. Prayer text is not used as thematic evidence.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data' / 'thematic-index' / 'books' / 'book-20.json'


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
104: {
    'signals': ['pensée', 'sentiment', 'volonté', 'réalisation', 'corps concret'],
    'themes': [
        T('unification-pensee-sentiment-volonte', 'Unification pensée-sentiment-volonté', 'central', 'direct', [2,3,4,5,6,8,10,11,18,21], "Le psaume attribue la faiblesse de l’homme à la séparation de la pensée, du sentiment et de la volonté. Une pensée juste doit être équilibrée dans les sentiments puis conduite dans la volonté jusqu’à une réalisation concrète pour que ces trois intelligences retrouvent leur unité."),
        T('realisation', 'Réalisation', 'central', 'direct', [7,8,9,10,11,12,18], "La réalisation est le critère qui empêche la pensée de rester enfermée dans l’abstraction : ce qui est reconnu comme juste et vrai doit recevoir un acte et un corps concret afin de devenir réellement vivant."),
        T('monde-mental-separe', 'Monde mental séparé', 'central', 'direct', [2,3,4,6,9], "Le texte décrit un monde mental devenu autonome, construit à partir des concepts et perceptions humaines puis coupé du sentiment et de l’énergie d’action. Cette séparation est associée à l’illusion, au doute et à l’insatisfaction."),
        T('corps-concret', 'Corps concret', 'important', 'direct', [8,11,14,15,16,18,19], "Le corps concret est présenté comme la condition pour rencontrer l’esprit sans s’égarer dans une spiritualité abstraite. L’homme doit donner une forme terrestre à ce qu’il veut vivre afin de disposer d’un support adapté à cette rencontre."),
        T('terre-comme-chemin-vers-esprit', 'Terre comme chemin vers l’esprit', 'important', 'direct', [13,14,15,16,17,18], "Le psaume affirme que l’accès à l’esprit passe par la réalité terrestre : harmoniser le monde concret et y constituer un corps est présenté comme le chemin permettant d’approcher l’immortalité et l’éternité."),
        T('verite', 'Vérité', 'important', 'direct', [10,12,19,20], "La vérité est reliée à ce qui peut être conduit jusqu’à l’unité et à la réalisation. Elle ne reste pas une conviction intérieure : elle doit éclairer les différents mondes de l’homme et les accorder dans une même vie."),
    ],
},
105: {
    'signals': ['épreuve', 'deux terres', 'lois', 'cause à effet', 'invisible'],
    'themes': [
        T('epreuve', 'Épreuve', 'central', 'direct', [1,2,3,4,8,11], "L’épreuve est présentée comme une occasion de comprendre et de rectifier plutôt que comme une simple punition. Elle révèle un désaccord avec des lois que l’homme n’a pas étudiées ou appliquées, notamment dans la partie invisible de sa vie."),
        T('deux-terres', 'Deux terres', 'central', 'direct', [5,6,7,9,16,17,24,27,31], "Le psaume distingue une terre visible et une terre invisible qui appartiennent toutes deux à l’existence humaine. Négliger la seconde crée, selon le texte, une dysharmonie qui finit par affecter aussi la vie matérielle."),
        T('lois-du-pere', 'Lois du Père', 'central', 'direct', [3,4,7,8,19,20,21,24,25,26,27,31], "Les lois sont présentées comme communes aux mondes visibles et invisibles. La sagesse consiste à les étudier, comprendre leur logique puis organiser les deux dimensions de la vie en conformité avec elles."),
        T('cause-a-effet', 'Cause à effet', 'important', 'direct', [3,4,8,28,29,30], "La loi de cause à effet sert de cadre pour interpréter les événements : ce qui est accueilli, engendré ou mis en mouvement appelle des conséquences dont l’homme devra ensuite prendre soin jusqu’à leur aboutissement."),
        T('invisible-gouverne-visible', 'Invisible gouverne le visible', 'important', 'direct', [5,9,10,16,17,21,22,23,33], "Le psaume affirme que l’invisible gouverne le visible et critique l’abandon de cette dimension. Pensées, sentiments et influences sont décrits comme des réalités agissantes qui finissent par modeler le monde concret."),
        T('responsabilite', 'Responsabilité', 'important', 'direct', [3,6,7,8,17,24,27,31,32,33], "La responsabilité consiste à ne pas remettre sa vie à une intervention extérieure mais à étudier les lois, observer les effets de ses propres émanations et donner une forme concrète à sa nature supérieure dans les actes."),
    ],
},
106: {
    'signals': ['conscience', 'portes', 'clés', 'étude', 'préparation'],
    'themes': [
        T('conscience', 'Conscience', 'central', 'direct', [5,6,9,10,11,14,15,16,17,18,19,20,21,22,23,24,25], "La conscience est la clé universelle du psaume : elle rend un monde vivant pour l’homme, mobilise pensée, sentiments et volonté, et permet de découvrir les clés particulières qui ouvrent les différentes portes de l’existence."),
        T('portes-et-cles', 'Portes et clés', 'central', 'direct', [2,3,4,5,6,9,10,22,23,24,25], "La vie est décrite comme une succession de portes ouvrant sur des mondes distincts. Chaque porte possède une clé, et la compréhension ne suffit que si l’homme est préparé à entrer réellement dans le monde qu’elle révèle."),
        T('etude', 'Étude', 'important', 'direct', [5,6,14,20,25], "L’étude doit ouvrir vers ce qui n’est pas encore connu et préparer un corps capable de le recevoir. Lorsqu’elle reste enfermée dans l’intellect et dans le déjà-connu, elle ne permet pas de franchir la porte vers un savoir plus large."),
        T('preparation', 'Préparation', 'important', 'direct', [4,7,8,21,24,25], "Le passage d’une porte demande une préparation, une éducation et un corps adaptés. Les vertus, l’attitude et la compréhension sont présentées comme des conditions de capacité, pas comme de simples décorations morales."),
        T('concentration', 'Concentration', 'important', 'direct', [6], "La concentration est comparée à un fil capable d’atteindre la clé aperçue par la conscience ; elle sert donc à maintenir le lien entre une perception intérieure et l’acte qui permet d’ouvrir réellement la porte."),
        T('simple-et-vrai', 'Simple et vrai', 'important', 'direct', [22,23], "Le texte oppose la recherche du merveilleux et du fantastique à une conscience trouvée dans ce qui est simple et vrai. Le réel est présenté comme le lieu où les mondes peuvent finalement être unifiés."),
    ],
},
107: {
    'signals': ['vérité', 'authenticité', 'terre d’Ouriel', 'unification', 'mensonge'],
    'themes': [
        T('verite', 'Vérité', 'central', 'direct', [2,3,4,5,8,9,11,13,15,17,20,25,28,29,30], "La vérité est le critère central d’entrée dans la terre d’Ouriel : elle doit apparaître dans l’ensemble de la vie, jusque dans les pensées, les paroles, les réactions, les relations, les actes et les œuvres, et non seulement dans un moment sacré ou une intention déclarée."),
        T('authenticite', 'Authenticité', 'central', 'direct', [3,4,6,9,10,11,13,15,17,29,30], "L’authenticité consiste à ne pas présenter devant les mondes supérieurs une image différente de celle que l’on manifeste dans la vie quotidienne. Le texte demande une continuité entre l’être déclaré et l’être réellement vécu."),
        T('unification-des-mondes', 'Unification des mondes', 'central', 'direct', [1,2,3,7,14,18,20,30], "Le psaume rejette la séparation qui réserverait la pureté à un monde sacré et abandonnerait le monde ordinaire au désordre. L’unification exige de remettre chaque chose à sa place et de construire un langage commun entre les dimensions de la vie."),
        T('realisation-concrete', 'Réalisation concrète', 'important', 'direct', [11,12,13,14,17,20], "Ouriel est explicitement associé au concret : la valeur d’une parole ou d’une intention est vérifiée dans ce qu’elle devient dans la vie quotidienne et dans les œuvres réalisées."),
        T('mensonge', 'Mensonge', 'important', 'direct', [8,9,10,13,15,16,21,23,24,25,26,27,28,29], "Le mensonge est présenté comme une terre sans stabilité. Son fruit ultime est décrit comme le néant, précédé par la peur, le doute et l’isolement, parce qu’aucune base vraie ne peut soutenir celui qui vit dans une apparence fabriquée."),
        T('relations-comme-revelateur', 'Relations comme révélateur', 'important', 'direct', [3,4,14,18,30], "La vraie nature de l’homme est observée dans ses rapports avec l’environnement et les autres, pas seulement lorsqu’il est seul. Les relations révèlent donc concrètement la cohérence ou la séparation entre ses différents mondes."),
    ],
},
}


def merge_themes(existing, replacements):
    by = {t.get('themeId'): t for t in existing}
    for theme in replacements:
        by[theme['themeId']] = theme
    order = {t['themeId']: i for i, t in enumerate(replacements)}
    return sorted(
        by.values(),
        key=lambda t: (
            0 if t.get('themeId') in order else 1,
            order.get(t.get('themeId'), 999),
            t.get('themeId', ''),
        ),
    )


def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    by_number = {a['number']: a for a in data.get('psalmAnalyses', [])}
    changed = 0
    for num, spec in DEEP.items():
        if num not in by_number:
            continue
        analysis = by_number[num]
        analysis['titleSignals'] = spec['signals']
        analysis['themes'] = merge_themes(analysis.get('themes', []), spec['themes'])
        analysis['semanticDepth'] = 'deep-content-grounded'
        changed += 1
    data['psalmAnalyses'] = sorted(by_number.values(), key=lambda a: a['number'])
    method = data.setdefault('method', {})
    method['semanticPass'] = 'deepening-in-progress'
    method['deepPsalmCount'] = sum(
        1 for a in data['psalmAnalyses'] if a.get('semanticDepth') == 'deep-content-grounded'
    )
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Deepened {changed} Psalm analyses in book 20; deep total={method["deepPsalmCount"]}')


if __name__ == '__main__':
    main()
