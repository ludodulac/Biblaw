# BIBLAW-LINGUISTIC-OCCURRENCES-011 — consolidation du modèle de preuve

## Principe
Une observation syntaxique n'est convertie en POS lexical que lorsqu'elle constitue une preuve suffisante dans le cadre activé. Une fonction d'usage est stockée séparément du POS.

## Cadres versionnés après 011

| Cadre 009 | Nom 011 | Observation | Conclusion | Statut |
|---|---|---|---|---|
| prenominal-adjective | prenominal-adjective-position | déterminant + cible + mot lexical | aucune classification seule | SUPPORTING_EVIDENCE |
| copular-predicate-adjective | copular-predicate-adjective | copule + cible devant frontière/coordination sûre | ADJ PROVISIONAL si ADJ est analyse lexicale candidate | PROOF |
| adverb-before-determiner | adverb-before-determiner | cadre copulaire/existentiel + cible + déterminant | ADV PROVISIONAL si ADV est analyse candidate | PROOF |
| modal-adverb-before-infinitive | finite-modal-target-lexical-complement | modal fini + cible + token lexical ; aucune morphologie infinitive démontrée | aucune classification seule | RETIRED comme preuve |
| substantivized-adjective | nominalized-adjective-use | déterminant + cible devant frontière/coordination et analyse ADJ candidate | ADJ PROVISIONAL + usage.nominalized=true | PROOF de l'usage nominalisé, sans conversion NOUN |

## JUSTE lexical
011 conserve deux analyses lexicales attestées par le pilote : ADJ et ADV. Les 28 sorties NOUN de 009 provenaient du cadre de substantivation et ne démontraient pas un NOUN lexical indépendant. Elles ne sont donc plus une troisième analyse lexicale automatique.

## Gold
Cinq entrées VALIDATED ont été révisées explicitement : occ-e829fcdf16e8e910cf3dec01, occ-4c429f9c9439e6cb978ea720, occ-687430a18143c749e91f542d, occ-59e4544e1b37e6bee0ea02c5, occ-35c807aa0ad3ccf6a4e35de4.
Ancien : category NOUN, POS NOUN.
Nouveau : category ADJECTIVE, POS ADJ, usage.nominalized=true.
Raison : 010 a établi que le contexte valide la substantivation mais ne suffit pas à transformer silencieusement la fonction syntaxique en POS lexical NOUN.

## Effet conservateur
009 : ADJECTIVE 564 ; ADVERB 150 ; NOUN 28 ; UNKNOWN 1148 ; AMBIGUOUS 0.
011 : ADJECTIVE 290 ; ADVERB 78 ; NOUN supprimé des analyses lexicales JUSTE ; UNKNOWN 1522 ; AMBIGUOUS 0.
Total brut et segmentation restent 1890 AUTONOMOUS.

Différence :
- les 302 sorties prenominal-adjective cessent d'être des preuves ; celles non reprises par un autre cadre deviennent UNKNOWN ;
- les 72 sorties modal-adverb-before-infinitive deviennent UNKNOWN ;
- les 28 substantivations passent de NOUN à ADJ + usage nominalized ;
- les 262 preuves copulaires ADJ et 78 preuves ADV avant déterminant restent ;
- certains comptes se recouvrent fonctionnellement via l'ordre des cadres, d'où le total final déterministe 290/78/1522.

## Sondes hors JUSTE
Non-régressions :
- un rose bonbon -> UNKNOWN, jamais ADJ par position seule ;
- un fort courant -> UNKNOWN par le cadre pré-nominal seul ;
- ce courant est fort -> ADJ ;
- il faut bien comprendre -> UNKNOWN par l'ancien cadre modal seul ;
- c'est même une évidence -> ADV ;
- le vrai, le beau -> ADJ + usage.nominalized=true.

## Industrialisation
A. moteur structurel : séparation POS/usage désormais explicite et sans branche JUSTE.
B. bibliothèque grammaticale : encore incomplète ; de nouveaux cadres génériques peuvent être nécessaires et doivent être falsifiables.
C. connaissance lexicale : les analyses candidates et l'activation de cadres restent nécessairement spécifiques au lexème.

Un nouveau mot peut donc demander de nouvelles données lexicales normalement. Une nouvelle branche de code spécifique au mot reste interdite. Un nouveau cadre grammatical générique est acceptable pendant la construction de la bibliothèque s'il est documenté, adversarialement testé et conservateur.
