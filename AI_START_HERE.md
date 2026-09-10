# Biblaw — point d’entrée rapide pour une nouvelle conversation

Ce fichier est un routeur, pas une nouvelle source de vérité.

## Contexte transversal

Biblaw appartient à l'écosystème **`ludodulac/Grand-pere`**. Grand Père est documenté dans le dépôt `ludodulac/Grand-pere`.

En nouvelle conversation : lire d'abord `ludodulac/Grand-pere/AI_START_HERE.md`, suivre `projects/_INDEX.md` vers Biblaw et utiliser `LOOP_ENGINEERING.md` pour la méthode de progression ; revenir ensuite ici. **Le dépôt Biblaw reste l'autorité sur corpus, données, générateurs, tests, CI et état déployé.**

## Avant toute écriture

1. vérifier HEAD réel de `main`, PR et CI ;
2. lire la passation courante seulement si nécessaire ;
3. utiliser `docs/_INDEX.md` puis seulement le contrat de la zone ;
4. lire les rapports générés pertinents si corpus/thèmes/recherche ;
5. ne jamais traiter un compteur recopié comme vérité actuelle.

## Routage essentiel

### Corpus
Source canonique : `data/corpus/books/` et pièces cataloguées. Modifier l'amont exige la validation correspondante du pipeline réel.

### Thèmes / sémantique
Source canonique : données thématiques canoniques et générateurs réellement autorisés. Les dérivés générés ne se corrigent pas à la main.

Une proximité lexicale n'est pas une relation conceptuelle. Un mot présent dans le nom d'un thème n'est pas automatiquement une composante du concept. Pour une relation difficile : `relation proposée → relation concurrente → reformulation sans vocabulaire commun → argument/provenance → valider, reclasser ou conserver comme frontière`.

### Recherche
Lire le contrat de recherche et le runtime/générateurs réellement actifs. Admissibilité avant classement. Ne pas masquer un défaut sémantique par un fallback de proximité.

### Interface
Ne jamais masquer en CSS/JS un défaut provenant du corpus, de la normalisation, de l'index ou du runtime.

## Validation

Utiliser les niveaux FAST / TARGETED / FULL définis par les scripts actuels du dépôt. Une validation coûteuse doit être bornée et observable ; ne pas relancer silencieusement un pipeline complet lorsqu'un contrôle ciblé suffit.

Un bug déterministe corrigé doit devenir sentinelle lorsque raisonnable. Un test technique ne remplace pas une validation éditoriale/humaine lorsque la question est sémantique.

## Boucle

`question sémantique ou produit → état réel → plus petit cas discriminant → première frontière responsable → correction/proposition minimale → preuve → CONTINUE / PIVOT / STOP`.

Le but n'est ni de maximiser le nombre de relations ni de réduire artificiellement le nombre de thèmes. Un graphe sparse mais honnête vaut mieux qu'une richesse fabriquée.

## Avant de déclarer terminé

- rapport différentiel sans variation inexpliquée ;
- sentinelles pertinentes vertes ;
- ambiguïtés attendues explicites ;
- aucun dérivé généré corrigé manuellement ;
- validation proportionnée au niveau modifié ;
- prochaine conversation capable de reconstruire **objectif / dernière boucle / preuve / prochaine décision**.
