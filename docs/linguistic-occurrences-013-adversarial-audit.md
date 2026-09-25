# BIBLAW-LINGUISTIC-OCCURRENCES-013 — audit adversarial COMPTE

Baseline auditée : PR #30 HEAD `1453b6cfce8109f3c7c1b79089f015a4d0fcda45`.
Audit pur : aucune correction du pilote, de la configuration ou du moteur.

## Reconstruction
Reconstruction indépendante : 222 brut, 222 AUTONOMOUS ; NOUN_COMPTE 124, VERB_COMPTER 26, UNKNOWN 72, AMBIGUOUS 0.

## Configuration
Trois règles seulement :
1. famille lexicalisée prendre/rendre (en) compte — 121 déclenchements ;
2. au bout du compte — 3 ;
3. cadres sujets verbaux clairs — 26.

Aucun occurrenceId, aucun contexte exact, aucune liste d'exceptions gold. Aucun `compte` dans le moteur Python. La configuration est déclarative mais la troisième règle encode une petite liste lexicale de sujets/formules (`qui`, `rien ne`, `ce qui`, `l’intention`, `l’œuvre`, `la sagesse`). Cette liste est connaissance lexicale/configurée, pas un cadre français générique. Elle n'est pas un mini-programme occurrence-par-occurrence, mais sa réutilisabilité est volontairement limitée à COMPTE.

## Gold 16 relu
Les 16 contextes ont été relus. Les catégories humaines sont défendables :
- prendre/rendre/se rendre compte et au bout du compte : NOUN ;
- intention/rien/sagesse + compte : VERB.
Automatique : 11 corrects, 5 UNKNOWN, 0 AMBIGUOUS, 0 contradiction.
Aucune erreur humaine certaine trouvée dans le gold.

## Audit 124 NOUN
Les 3 `au bout du compte` sont nominaux.
Échantillonnage déterministe large de la règle 121 : prendre en compte, pris en compte, rendre compte, se rendre compte. Aucun déclenchement inspecté ne montre un VERB `compter`.
La regex exige que la forme prendre/rendre soit immédiatement en fin de contexte gauche, avec seulement `en` optionnel : elle n'effectue pas de rattachement distant à un verbe voisin.
Limite de couverture assumée : négation, pronoms ou adverbes intercalés (`ne prennent pas en compte`, `se rendent même compte`, `rends-toi compte`) restent souvent UNKNOWN.

## Audit 26 VERB
Les 26 déclenchements ont été inspectés via l'inventaire de preuve. Ils correspondent à des emplois finis de `compter` : `ce qui compte`, `rien ne compte`, `l'intention qui compte`, `l'œuvre compte`, `le résultat qui compte`, `la seule chose qui compte`, etc.
Aucun NOUN certain trouvé parmi ces 26.
La règle reste lexicalement étroite et n'est pas présentée comme générique.

## UNKNOWN
Échantillon par familles :
- possessif / compte nominal : 6, ex. `son propre compte`, `trouver son compte` ;
- `laissé pour compte` : 2 ;
- variantes rendre/se rendre compte non couvertes : au moins 18 ;
- variantes prendre en compte non couvertes : au moins 30 ;
- sujets verbaux hors petite liste : ex. `cela ne compte pas vraiment`, `votre pure intention compte`, `la sagesse des Esséniens compte`, `seule la matière compte`.
Ce sont majoritairement des cas humainement évidents mais volontairement non couverts. Aucun défaut de segmentation découvert.

## Recherche AMBIGUOUS
Les UNKNOWN à frontières, poésie et syntaxe faible ont été recherchés. Aucun contexte solide où NOUN et VERB restent tous deux raisonnablement compatibles n'a été démontré. AMBIGUOUS=0 reste acceptable pour ce pilote.

## Échantillon adversarial indépendant
Sélection humaine hors gold, avant comparaison automatique :
- occ-fcbdc68e0c1c99d9ef4d2d04 — `Sans s’en rendre compte` — humain NOUN — auto NOUN — CORRECT
- occ-3d89593b2ab8671816588e9b — `devra en rendre compte` — humain NOUN — auto NOUN — CORRECT
- occ-43171dc25a5938a4bc964f09 est gold et donc exclu de l'échantillon indépendant.
- occ-1b5dff48c4bd9d9f97564aa3 — `au bout du compte` — humain NOUN — auto NOUN — CORRECT
- occ-e502593b7b53d3787866bb0d — `ce qui compte` — humain VERB — auto VERB — CORRECT
- occ-9409ba838823ee68e92d6fee — `le résultat qui compte` — humain VERB — auto VERB — CORRECT
- occ-3a1c3c05d3bca673ae123ed9 — `L’œuvre compte` — humain VERB — auto VERB — CORRECT
- occ-649aa8ef967b998243dcee62 — `cela ne compte pas vraiment` — humain VERB — auto UNKNOWN — UNKNOWN
- occ-e0b9dfd6cd71a2f2bf6278d6 — `votre pure intention compte` — humain VERB — auto UNKNOWN — UNKNOWN
- occ-0e1ee56f1175af4537c25797 — `son propre compte` — humain NOUN — auto UNKNOWN — UNKNOWN
- occ-027c3bd43a357ab279424a8f — `laissé pour compte` — humain NOUN — auto UNKNOWN — UNKNOWN
- occ-3ef3be2e634c01264cabb9e0 — `ne vous rendez pas réellement compte` — humain NOUN — auto UNKNOWN — UNKNOWN

Contradictions certaines : 0.

## Industrialisation
CONFIG_ONLY_WAS_REALLY_SUFFICIENT=YES
CONFIG_IS_DECLARATIVE=YES
CONFIG_CONTAINS_HIDDEN_PROGRAMMING=NO
CONFIG_CONTAINS_GOLD_OVERFITTING=NO
ENGINE_CHANGED=NO
WORD_SPECIFIC_CODE_BRANCHES=0

Nuance : la règle verbale contient une liste lexicale étroite de sujets/formules propres à l'usage de COMPTE. C'est de la connaissance lexicale déclarative et conservatrice ; ce n'est pas une preuve de grammaire générique ni une architecture pour tous les verbes. Le succès industrialisation signifie ici : le moteur accepte un nouveau lexème par données/configuration sans branche Python spécifique, avec abstention massive quand la configuration ne sait pas conclure.

## Régressions
Le workflow 013 exécute PORTE 004, SUIS 006, inversion 008, consolidation JUSTE 011 et pilote COMPTE 012 sans modification du moteur.
