# BIBLAW-LINGUISTIC-OCCURRENCES-016 — consolidation méthodologique GARDE

Baseline directe : main `3fbd05fc85be72f322af7ad608484e9975e933c3`. Cette branche consolide le pilote utile de #32 et les constats de l'audit #33 ; #32/#33 ne doivent pas être fusionnées séparément.

## Reconstruction
99 surfaces ; 76 AUTONOMOUS ; 16 VERB_CLITIC ; 7 COMPOUND_ELEMENT ; 92 retenues. NOUN_GARDE 19 ; VERB_GARDER 50 ; UNKNOWN 23 ; AMBIGUOUS 0. Aucun résultat linguistique n'est modifié pour améliorer l'expérience.

## Golds et histoire expérimentale
GOLD_PRINCIPAL_014 = 18.
GOLD_ADVERSARIAL_014_ORIGINAL = 12 entrées annoncées.
015 a découvert quatre doublons avec le principal : occ-41014a816a23e39e72453b8b, occ-9983886fe77edaef59d32093, occ-547160107b7cda09d673efc8, occ-c00102a35e0b51748775d601.
Donc GOLD_ADVERSARIAL_014_UNIQUE = 8 nouveaux cas, et non 12.
GOLD_ADVERSARIAL_015 = 10 nouvelles occurrences ; intersection avec principal = vide ; intersection avec les 8 uniques 014 = vide.

L'audit 016 vérifie ces intersections et interdit de réécrire 014 comme douze nouveaux cas.

## Deux questions désormais séparées
TECHNICAL_CONFIG_ONLY = YES : le moteur générique reste byte-identique à la baseline ; aucun nouveau cadre ; aucune branche Python GARDE.
INDEPENDENT_REPLICATION_STRENGTH = LIMITED : la règle garde-noun-possessive n'a qu'un seul déclenchement corpus, `sous sa garde`, et ce déclenchement appartient au gold principal figé avant la règle.

Cela ne démontre ni une erreur linguistique ni un mécanisme direct de surapprentissage. Cela limite la force expérimentale indépendante de cette règle.

## Possessif
`garde-noun-possessive` reste déclarative et PROVISIONAL. Sa configuration porte `evidenceScope=SINGLE_CORPUS_TRIGGER` et `independentEvidenceStatus=LIMITED`. Aucun nouveau cas n'est recherché et aucune règle n'est élargie.

## Configuration
CONFIG_IS_DECLARATIVE = YES.
CONFIG_CONTAINS_HIDDEN_PROGRAMMING = NO.
NO_DIRECT_OVERFIT_MECHANISM_DETECTED = YES : aucune occurrenceId, aucun texte de gold, aucune branche procédurale occurrence par occurrence dans les règles.
INDEPENDENT_EVIDENCE_LIMITATION = garde-noun-possessive.

## Clitiques et composés
16 VERB_CLITIC : réutilisation de la segmentation générique, sans changement moteur.
7 COMPOUND_ELEMENT : 5 garde-manger, 1 garde-mangers, 1 garde-fou.

## Interprétation
GARDE peut rester techniquement config-only et linguistiquement sans contradiction certaine observée, tout en ayant une réplication indépendante seulement LIMITED. L'industrialisation gagne une seconde expérience utile, mais pas une seconde preuve indépendante aussi forte que COMPTE.
