# BIBLAW-LINGUISTIC-OCCURRENCES-012 — quatrième pilote COMPTE

## Baseline
Départ exact: `055543c6fa9736811dc0752146610f7ea1723525`, main après fusion #29.
Les audits PORTE, SUIS, inversion 008 et consolidation 011 ont été exécutés sur la branche 012 avant le pilote et passent.

## Sélection corpus
Comptes documentaires réévalués avec le contrat existant: MARCHE 224, COMPTE 222, LIVRE 77, VEILLE 25, AIDE 61, GARDE 99, RESTE 266, PASSE 281, SENS 1415, TOUR 97.
- MARCHE: NOUN/VERB, 224, contextes riches mais très proche de PORTE; inversion déjà testée en 008.
- COMPTE: NOUN `compte` / VERB `compter`, 222; nombreuses locutions (`prendre en compte`, `rendre/se rendre compte`, `au bout du compte`) et verbes finis (`ce qui compte`, `rien ne compte`). Très bon test de connaissance lexicale configurable sans nouveau cadre.
- LIVRE: surtout NOUN dans l'échantillon, faible valeur d'homographie.
- GARDE/AIDE/RESTE/PASSE: NOUN/VERB mais valeur d'industrialisation moins nette que COMPTE.
- SENS: NOUN/VERB, très volumineux; utile ultérieurement mais plus coûteux pour un premier test config-only.
COMPTE est retenu parce que son intérêt principal est précisément de tester l'ajout par données/configuration.

## Gold indépendant
16 occurrences human-audited ont été sélectionnées depuis l'inventaire brut AVANT ajout des règles COMPTE. Elles couvrent les deux analyses, négation, impératif, coordination, locutions et fin de phrase.
Le gold n'est pas dérivé du classificateur.

## CONFIG_ONLY_BASELINE
Aucune modification de `scripts/build_linguistic_adjudication.py`.
Configuration:
- NOUN_COMPTE / lemma `compte` / NOUN
- VERB_COMPTER / lemma `compter` / VERB
- trois règles conservatrices dans `compte-config.json`: famille prendre/rendre compte, `au bout du compte`, et quelques cadres sujets lexicaux clairs pour le verbe.

Résultat:
- brut 222
- AUTONOMOUS 222
- NOUN_COMPTE PROVISIONAL 124
- VERB_COMPTER PROVISIONAL 26
- UNKNOWN 72
- AMBIGUOUS 0
- gold correct automatique 11
- gold UNKNOWN 5
- gold AMBIGUOUS 0
- gold contradictoire 0

Les 5 UNKNOWN gold sont acceptés: la configuration reste volontairement étroite.

## Audit adversarial
Les 150 PROVISIONAL ont été regroupés par règle et échantillonnés sur toute leur distribution.
Les cadres noun observés restent des locutions nominales; les cadres verbaux échantillonnés sont des formes de `compter`.
Des cas humains évidents restent UNKNOWN, notamment variantes de `prendre en compte`, `se rendre compte`, `son propre compte`, `laissé pour compte`. Ils documentent la couverture, pas une contradiction.

Recherche AMBIGUOUS: les contextes inspectés distinguent raisonnablement le nom du verbe; aucun cas réellement compatible avec les deux analyses n'a été démontré. AMBIGUOUS reste 0 sans être forcé.

Aucun nouveau cadre grammatical générique n'est nécessaire. Aucun code spécifique au mot n'est introduit dans Python.

## Industrialisation
Pour COMPTE:
- données/configuration: oui — lexique, config, artefacts, gold;
- audits/tests: oui;
- modification moteur Python: non;
- exception lexicale dans le code: 0.

`ENGINE_CHANGED=NO`
`NEW_GENERIC_FRAMES=0`
`WORD_SPECIFIC_CODE_BRANCHES=0`
`CONFIG_ONLY_WAS_SUFFICIENT=YES`

Ce résultat prouve la réutilisabilité pour ce quatrième mot, pas encore pour vingt mots arbitraires. L'industrialisation 20 mots reste PARTIAL: le moteur structurel est stable ici, mais la bibliothèque de cadres génériques n'est pas une grammaire française complète et chaque lexème nécessite normalement sa connaissance lexicale configurée.

## Régressions
PORTE, SUIS, inversion 008 et consolidation JUSTE 011 restent inchangés et audités par CI. JUSTE conserve ADJ/ADV et l'usage nominalisé séparé, sans NOUN lexical créé par substantivation.

Aucune interface publique n'est modifiée.
