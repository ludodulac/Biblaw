# BIBLAW-LINGUISTIC-OCCURRENCES-004 — fondation PORTE corrigée

## Stratégie Git

HEAD de départ : `4e80bf2ab153354a7936358f97021ea2619c10ec` (HEAD #22, contenant #21 + audit 003).
Branche : `fix/linguistic-occurrences-004`.

004 dérive de #22 afin de conserver tout l'historique technique et les preuves de 003, mais sa PR cible directement `main`. Elle est donc destinée, après validation, à constituer une fondation unique remplaçant fonctionnellement les PR dépendantes #21/#22. Aucun merge n'est effectué.

## Convention de segmentation

Chaque surface brute `porte` reçoit exactement une segmentation :
- `AUTONOMOUS` : aucune liaison par tiret à une unité voisine ;
- `VERB_CLITIC` : tiret immédiatement après PORTE suivi d'un clitique explicite configuré (`le, la, les, lui, leur, en, y`) ;
- `COMPOUND_ELEMENT` : tiret adjacent qui n'est pas le cas VERB_CLITIC.

Le tiret n'est donc jamais assimilé automatiquement à « composé ». Les clitiques sont testés en premier. Un cas futur non couvert doit rester UNKNOWN plutôt que d'être deviné.

Les composés sont conservés avec occurrenceId, surface complète, contexte et segmentation dans `porte-compounds.json`, mais exclus du total linguistique retenu.

## Provenance reproductible

Chaîne complète versionnée :

`corpus canonique -> build_linguistic_occurrence_index.py -> porte-occurrences.json -> build_linguistic_adjudication.py -> segmentation + porte.json + porte-compounds.json`.

La configuration lexicale du pilote est dans `porte-config.json`. Le moteur ne contient aucun `if word == "porte"` : le formulaire, les lemmes/catégories du pilote et les clitiques sont des données explicites.

## Adjudication conservatrice

Les règles dangereuses 002 `porte + de/des => NOUN` et `porte + préposition => VERB_PORTER` ne sont plus utilisées.

Les règles automatiques 004 ne produisent que PROVISIONAL ou UNKNOWN. Aucun résultat automatique n'est VALIDATED.

Résultat recomputé :
- surface brute : 1184
- autonome : 1154
- verbe + clitique : 3
- dans composé : 27
- total linguistique retenu : 1157
- NOUN PROVISIONAL : 268
- VERB_PORTER PROVISIONAL : 369
- UNKNOWN : 520
- AMBIGUOUS : 0
- OTHER/composés hors total retenu : 27

Les nombres 535/504 de 002 ne sont pas préservés.

## Cinq sentinelles 003

- `occ-4210e70fcbe4e1d65b894181` « ouvrir une telle porte dans... » -> NOUN PROVISIONAL.
- `occ-f5043c17057a47db9e0b5eed` « qui ... porte des mondes » -> UNKNOWN.
- `occ-a18d1242395f001f1889f138` « l’homme porte de vrai » -> UNKNOWN.
- `occ-75cd0c3a829334cbf3d2165c` « l’homme porte des vertus » -> UNKNOWN.
- `occ-8a55dd99471758e92a13b630` « l’homme porte de vrai, de beau » -> UNKNOWN.

Le gold set humain connaît leur analyse correcte, mais le moteur automatique préfère UNKNOWN lorsqu'il n'a pas de preuve suffisante. Aucune des cinq n'est encore faussement classifiée.

## Gold set

`data/linguistic/gold/porte-gold.json` contient 19 cas humainement/auditivement validés, choisis indépendamment des règles automatiques :
- cinq sentinelles 003 ;
- trois verbes avec clitique ;
- cinq exemples de familles de composés ;
- trois noms évidents ;
- trois verbes évidents.

Le gold set porte une provenance `human-audited / BIBLAW-LINGUISTIC-OCCURRENCES-004`. Sa validation est locale aux occurrences incluses ; elle ne promeut aucune autre occurrence.

## Inventaire des composés

27 occurrences :
- `porte-parole` : 12
- `porte-paroles` : 7
- `porte-Parole` : 3
- `porte‑parole` (tiret insécable) : 1
- `porte-à-faux` : 1
- `porte-drapeau` : 1
- `porte-monnaie` : 1
- `porte-bonheur` : 1

Les variantes graphiques sont conservées telles qu'elles apparaissent dans le corpus ; elles ne sont pas silencieusement normalisées en une seule surface complète.

## Audit 004

`scripts/audit_linguistic_foundation_004.py` vérifie :
- régénération déterministe depuis le corpus canonique ;
- offsets dans le texte original ;
- unicité des occurrenceId ;
- provenance explicite du générateur ;
- couverture intégrale de l'adjudication ;
- partition autonome / clitique / composé ;
- exclusion des 27 composés du total 1157 ;
- conservation exacte des composés dans l'inventaire ;
- cinq sentinelles 003 : correctes ou UNKNOWN, jamais l'ancienne erreur ;
- cohérence et indépendance structurelle du gold set ;
- absence totale de VALIDATED automatique ;
- compatibilité additive avec une expression multi-mots telle que `frapper à la porte`.

## Limites et risques

La précision globale n'est toujours pas mesurée : le gold set de 19 cas est volontairement petit et orienté couverture de phénomènes/sentinelles, pas estimation statistique.

520 UNKNOWN est un résultat acceptable de la politique de précision avant couverture. Il montre aussi que le moteur morphosyntaxique doit encore progresser avant industrialisation.

La règle générique de segmentation par clitiques couvre les clitiques configurés mais n'est pas prétendue être une analyse morphologique complète du français.

Le corpus canonique, l'index thématique et l'UI publique restent inchangés.

## Décision proposée

- Fondation 004 : GO pour revue technique, puis fusion seulement après validation explicite.
- Deuxième mot pilote : NO-GO avant validation/fusion propre de cette fondation et audit de son comportement sur le gold set.
- Interface linguistique : NO-GO ; la couverture automatique reste trop incomplète pour présenter des catégories comme suffisamment fiables au public.
