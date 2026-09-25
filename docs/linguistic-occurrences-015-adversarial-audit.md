# BIBLAW-LINGUISTIC-OCCURRENCES-015 — audit adversarial indépendant de GARDE

Baseline auditée : PR #32 HEAD `6e10f79fae01f5bac226e981afb010a1f8d23767`.
Audit pur : aucune correction du pilote ou du moteur.

## Reconstruction 014
Reconstruction exacte : 99 surfaces ; AUTONOMOUS 76 ; VERB_CLITIC 16 ; COMPOUND_ELEMENT 7 ; retenu 92. NOUN_GARDE 19 ; VERB_GARDER 50 ; UNKNOWN 23 ; AMBIGUOUS 0 ; OTHER 7.

Le moteur générique n'est pas modifié dans #32. Aucun littéral `garde` dans `scripts/build_linguistic_adjudication.py`. NEW_GENERIC_FRAMES=0 ; WORD_SPECIFIC_CODE_BRANCHES=0.

## Gold principal 18
Relecture contextuelle des 18 : 11 classifications automatiques concordantes, 7 UNKNOWN, 0 AMBIGUOUS, 0 contradiction certaine. Aucune erreur humaine certaine trouvée.

## Gold adversarial 014 — chronologie et défaut d'indépendance
La chronologie Git confirme :
- gold principal figé au commit f62f3dd... avant les règles ;
- règles GARDE ajoutées au commit 9bc704e... ;
- baseline mesuré au commit 67cbb7b... ;
- gold adversarial ajouté au commit d1d53b6... ;
- aucune modification ultérieure des règles GARDE.

Cependant le gold adversarial 12 n'est pas entièrement hors gold principal, contrairement à l'exigence de 014. Quatre occurrences sont communes :
- occ-41014a816a23e39e72453b8b
- occ-9983886fe77edaef59d32093
- occ-547160107b7cda09d673efc8
- occ-c00102a35e0b51748775d601

Il contient donc 8 nouvelles occurrences indépendantes, pas 12. Sur ses 12 entrées : aucune contradiction certaine ; les quatre chevauchements sont UNKNOWN dans l'automatique.

## 19 NOUN
Inspection exhaustive des 19 sorties :
- mise/mettre en garde : 15
- prendre garde : 3
- possessif + garde : 1

Toutes les 19 lectures nominales sont défendables dans leur contexte. Aucun faux rattachement verbal certain trouvé.

## 50 VERB
Répartition :
- VERB_CLITIC générique : 16
- règles configurées : 34
  - clear-subject : 25
  - imperative-object : 9

Inspection exhaustive des contextes : aucune sortie nominale certaine trouvée parmi les 50.

## 16 VERB_CLITIC
Les 16 sont des formes verbales réelles : `garde-le`, `garde-les`, et `garde-moi` (tirets ASCII et U+2011 observés). Aucun composé nominal parmi eux. Le mécanisme est celui déjà établi par PORTE/SUIS.

## 7 COMPOUND_ELEMENT
Inventaire exact :
- garde-manger : 5
- garde-mangers : 1
- garde-fou : 1

Les sept sont de vrais composés et doivent être exclus du total lexical GARDE autonome. Aucun faux composé trouvé.

## Configuration et surapprentissage
5 règles configurées + 1 mapping VERB_CLITIC. Aucun occurrenceId, aucun texte complet de gold, aucun pseudo-code, aucune branche Python spécifique.

Distribution :
- garde-noun-mise-en-garde : 15 déclenchements ; gold principal 2 ; gold adv014 2 ; hors deux golds 11.
- garde-noun-prendre-garde : 3 ; gold principal 1 ; gold adv014 1 ; hors golds 1.
- garde-noun-possessive : 1 ; gold principal 1 ; gold adv014 0 ; hors golds 0.
- garde-verb-clear-subject : 25 ; gold principal 4 ; gold adv014 4 ; hors golds 17.
- garde-verb-imperative-object : 9 ; gold principal 1 ; gold adv014 1 ; hors golds 7.

Le point critique est `garde-noun-possessive` : la règle a été ajoutée après le gel du gold principal et son unique déclenchement corpus est précisément l'occurrence gold `sous sa garde`. La règle est linguistiquement plausible et déclarative, mais elle n'a aucune validation corpus hors examen. L'audit ne peut donc pas démontrer l'absence de gold-overfitting pour cette règle. Ce risque doit être distingué d'une contradiction linguistique : aucune contradiction n'est observée.

La règle `clear-subject` contient aussi une liste de sujets lexicaux (l'homme, dieu, père, la lumière, la tradition, le cœur) en plus des pronoms. Elle reste déclarative et déclenche largement hors gold, mais sa complexité est supérieure à une simple connaissance lexicale de GARDE.

## UNKNOWN 23
La majorité sont humainement évidents mais volontairement non couverts : `garde précieusement`, `se garde pour soi`, `garde un lien`, `garde la distance`, `garde en lui`, coordinations `protège, garde et conduit`, séries vocatives `Ô mon Ange, garde...`, ainsi que deux occurrences de `prendre garde` avec mots intercalés/conjugaison non couverte.
Aucune anomalie de segmentation trouvée. Aucun cas solide NOUN/VERB simultanément compatible n'a été identifié ; AMBIGUOUS=0 reste défendable.

## Gold adversarial indépendant 015
Un troisième jeu de 10 occurrences hors des deux golds 014 a été figé avant l'ajout du script de comparaison 015. Il couvre deux NOUN risqués, deux VERB configurés, deux VERB_CLITIC, deux composés et deux VERB humainement clairs laissés UNKNOWN.
Résultat attendu de l'audit : classifications concordantes ou UNKNOWN ; aucune contradiction certaine.

## Conclusion méthodologique
La linguistique GARDE contrôlée ne fournit aucun faux positif certain. La réplication config-only est techniquement réelle : moteur inchangé, zéro nouveau cadre, zéro branche Python spécifique.

En revanche, la preuve expérimentale 014 n'est pas encore suffisamment indépendante pour affirmer sans réserve `CONFIG_CONTAINS_GOLD_OVERFITTING=NO` :
1. une règle n'a qu'un déclenchement, qui est dans le gold utilisé avant sa création ;
2. le gold adversarial annoncé hors gold principal recouvre en réalité quatre occurrences du principal.

Ces défauts justifient un NO-GO de fusion de #32 en l'état, non pour erreur linguistique certaine, mais pour insuffisance de la preuve indépendante de non-surapprentissage.
