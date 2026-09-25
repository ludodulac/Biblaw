# BIBLAW-LINGUISTIC-OCCURRENCES-014 — réplication config-only GARDE

Baseline : main 3fbd05fc85be72f322af7ad608484e9975e933c3.

## Sélection
Inventaire corpus : MARCHE 224, SENS 1415, GARDE 99, AIDE 61, RESTE 266, PASSE 281, LIVRE 77, VEILLE 25, TOUR 97. GARDE est retenu : il n'est ni le plus fréquent ni le plus facile. LIVRE est presque uniquement nominal ; VEILLE est petit et très séparé ; SENS ouvre une difficulté sémantique multi-sens non nécessaire au test config-only ; MARCHE est plus proche du pilote PORTE. GARDE teste NOUN/VERB avec impératifs, clitiques, relatives, négation, coordination, locutions « mise/mettre en garde », « prendre garde », possessif « sous sa garde », et composés garde-manger/garde-fou.

WHY_NOT_COMPTE_LIKE_EASY_CASE : contrairement à COMPTE, GARDE ne repose pas principalement sur prendre/rendre compte. Une part importante du verbe est reconnue par segmentation clitique existante et par cadres déclaratifs de sujet/impératif ; les noms proviennent de plusieurs constructions distinctes.
NOVELTY_VS_PREVIOUS_PILOTS : 16 VERB_CLITIC et 7 composés coexistent avec des impératifs autonomes et des locutions nominales, ce qui teste simultanément la segmentation déjà industrialisée et une configuration lexicale nouvelle.

## Gold avant règles
Gold principal : 18 occurrences, figé avant l'ajout des règles GARDE. Il couvre NOUN et VERB, négation, coordination, relative, impératif, ponctuation et clitiques.
Gold adversarial : 12 occurrences, figé après le baseline config-only mais avant tout ajustement de règle. Aucun ajustement de règle n'a ensuite été effectué.

## Configuration
Analyses : NOUN_GARDE (garde/NOUN), VERB_GARDER (garder/VERB).
5 règles déclaratives : mise/mettre en garde ; prendre garde ; possessif + garde ; sujets verbaux conservateurs ; impératif + objet. VERB_CLITIC réutilise segmentationAnalyses.
Aucun occurrenceId, aucun texte complet de gold, aucun pseudo-code procédural. Les regex sont des paramètres déclaratifs analogues au pilote COMPTE. Complexité : modérée, 5 règles + 1 mapping structurel.

## Config-only baseline final
TOTAL 99.
Segmentation : AUTONOMOUS 76 ; VERB_CLITIC 16 ; COMPOUND_ELEMENT 7.
NOUN_GARDE 19 ; VERB_GARDER 50 ; OTHER 7 ; UNKNOWN 23 ; AMBIGUOUS 0.
Gold principal : 11 correct, 7 UNKNOWN, 0 AMBIGUOUS, 0 contradiction.
Gold adversarial : les classifications automatiques concordantes ou UNKNOWN sont exigées par audit ; contradiction certaine = 0.

Les 7 compounds sont garde-manger/garde-mangers/garde-fou et restent OTHER. Aucun besoin de changer le contrat documentaire.

## Audit adversarial
Toutes les sorties PROVISIONAL ont été regroupées par preuve et inspectées. Les constructions nominales classées sont des usages nominaux défendables ; les sorties verbales sont des formes de garder. Les cas humains évidents mais non couverts (p.ex. « le mal se garde pour soi », certaines coordinations/impératifs) restent UNKNOWN : couverture manquante, pas contradiction.
Recherche AMBIGUOUS : aucun contexte solide n'impose NOUN et VERB simultanément ; zéro est conservé sans être forcé.

## Industrialisation
FIRST_CONFIG_ONLY_PILOT = COMPTE
SECOND_CONFIG_ONLY_ATTEMPT = GARDE
SECOND_CONFIG_ONLY_SUCCESS = YES
ENGINE_CHANGED = NO
NEW_GENERIC_FRAMES = 0
WORD_SPECIFIC_CODE_BRANCHES = 0
CONFIG_IS_DECLARATIVE = YES
CONFIG_CONTAINS_HIDDEN_PROGRAMMING = NO
CONFIG_CONTAINS_GOLD_OVERFITTING = NO
CONTRADICTIONS_CERTAINES = 0

Interprétation limitée : deux lexèmes distincts ont démontré une intégration config-only. Cela ne prouve pas que tous les lexèmes futurs seront config-only.
