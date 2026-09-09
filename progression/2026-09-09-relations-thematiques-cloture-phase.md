# Clôture de phase — relations thématiques transversales

Date : 2026-09-09

Ce document complète, sans l'écraser, `progression/2026-09-09-relations-thematiques-passation.md`. L'ancienne passation conserve l'historique intermédiaire ; le présent fichier décrit l'état de clôture vérifié de la phase d'exploration sémantique sur `work/theme-relation-candidates`.

## État vérifié de la branche

- branche : `work/theme-relation-candidates` ;
- dernier commit technique vert avant ce document : `f43c7bc19c99dbec7ef8aef4de31365e99a24047` ;
- run `Audit theme relation candidates` #89 : `success` ;
- graphe déterministe committé : blob Git `b39eed439e2410ac15c4352841c568ef6e436e4e`, identique byte-for-byte à l'artefact CI du run #88 ;
- couverture du graphe proposé : 42 relations, 57 thèmes/nœuds, 23 fichiers sources de revue, 0 contradiction structurelle ;
- types proposés présents : `broader_than`, `component_of`, `related_to`, `variant_of` ;
- `equivalentToPositiveCases: 0` ; ce zéro est volontairement acceptable ;
- chaque relation du graphe conserve `semanticClaim: false` ;
- `requiresHumanApproval: true` ;
- `publicSearchEffect: false`.

Le store canonique `data/thematic-index/theme-relations-validated.json` reste vide. Aucune relation n'a été promue et aucune relation proposée n'est connectée à la recherche publique.

## Corrections conceptuelles finales de cette phase

### Pensée vivante

L'ancienne passation décrivait encore `pensee-vivante → pensee` comme une frontière `variant_of` / `broader_than`. La revue transversale a tranché cette frontière.

Décision proposée actuelle :

`pensee broader_than pensee-vivante`

Raison : le thème général `pensee` couvre plusieurs états et usages, dont des formes limitées, abstraites ou pouvant accueillir un savoir vivant ou mort. `pensee-vivante` sélectionne donc un état qualifié du domaine général plutôt qu'une simple formulation alternative du même concept.

Garde-fou confirmé pendant la correction : une occurrence textuelle de « pensée vivante » n'est pas une attestation du `themeId` `pensee-vivante`. Les preuves par themeId restent limitées aux attestations canoniques des analyses thématiques.

La sentinelle de `scripts/audit_theme_semantic_case_studies.py` a été mise à jour uniquement parce qu'elle encodait encore l'ancienne décision. Le générateur n'a pas été modifié.

### Pratique et conscience

L'ancienne passation conservait encore `pratique` et `conscience` comme candidats `component_of pratique-et-conscience` avec frontière ouverte.

Décisions proposées actuelles :

- `pratique related_to pratique-et-conscience` ;
- `conscience related_to pratique-et-conscience`.

Raison : le psaume concerné présente deux aspects simultanés, mais affirme aussi que la conscience naît de la pratique et de la discipline. La structure moyen/condition → résultat ne justifie pas de traiter automatiquement les deux termes comme composants autonomes.

Règle consolidée : objet, partenaire, destination, condition, moyen, cause ou résultat ne devient pas `component_of` simplement parce qu'il apparaît dans un libellé composite.

### Union et force collective

Le cas `case-union-force-collective.json` a ajouté une frontière utile :

- `union broader_than union-des-forces` ;
- `union related_to union-et-force-collective` ;
- `union-des-forces related_to union-et-force-collective`.

La distinction clé est procédé / résultat : mutualiser des capacités pour constituer une force commune n'est pas identique à la capacité collective qui émerge de la cohésion.

### Temple intérieur et alias exacts

`temple` et `temple-interieur` partagent un alias exact, mais le corpus distingue une extension générale de temples et la construction intérieure spécifique.

Décision proposée :

`temple broader_than temple-interieur`

Cette boucle a renforcé une règle générale : même un alias exactement identique ne démontre pas `equivalent_to` si l'extension conceptuelle diffère. La famille `transmission` reproduisant la même leçon sans frontière supplémentaire, l'exploration des collisions d'alias a été arrêtée plutôt que densifiée artificiellement.

## Maturité à la clôture

### `broader_than`

Distinction la plus stable. Elle est retenue lorsqu'une reformulation sans vocabulaire commun conserve une vraie inclusion général → spécialisation.

### `related_to`

Distinction désormais positive et structurée, non résiduelle. Elle couvre notamment opposition, partenaire, objet, destination, moyen/résultat et causalité fonctionnelle lorsque l'inclusion ou la composition serait trompeuse.

### `component_of`

À réserver aux constituants autonomes réellement présentés comme parties du concept complet. Les cas atomiques comme `corps`, `ame`, `esprit → corps-ame-esprit` restent les exemples les plus solides.

### `variant_of`

À retenir seulement lorsque la reformulation conserve le même noyau conceptuel sans sous-domaine autonome : par exemple propriété constitutive ou modalité symbolique. Il ne doit jamais servir de refuge entre équivalence et spécialisation.

### `equivalent_to`

Aucun cas positif suffisamment solide n'a été trouvé. Ne pas chercher à en fabriquer. Alias, proximité lexicale, cooccurrence ou formulation voisine restent insuffisants.

## Décision Grand Père : STOP sur l'exploration ouverte

La phase d'exploration sémantique ouverte est considérée terminée.

Le critère de sortie est atteint : les dernières boucles ont principalement falsifié ou corrigé des frontières déjà connues, les quatre types positivement utilisés disposent de cas contrastifs, le format de revue sait conserver une frontière honnête, et les garde-fous détectent les dérives d'attestation ou de sentinelle.

Il reste de nombreux candidats non revus, mais leur existence n'est pas en soi une raison de continuer. Poursuivre sans nouvelle question produit risquerait surtout d'augmenter le volume plutôt que l'information.

## Ce qui ne doit pas être fait automatiquement ensuite

- ne pas promouvoir les 42 propositions dans `theme-relations-validated.json` ;
- ne pas fusionner la branche vers `main` sans décision explicite ;
- ne pas connecter ce graphe à la recherche publique ;
- ne pas densifier le graphe pour atteindre un objectif numérique ;
- ne pas modifier le générateur sauf bug réel démontré ;
- ne pas traiter l'ordre du corpus comme une chronologie historique.

## État de `main`

La branche de travail a divergé de `main`. Le merge-base vérifié reste `a9597a37dcdd6bb0893ca722652a872132a6856c`. `main` a depuis avancé, notamment avec le lien de démarrage vers Grand Père. Aucun commit sémantique de cette branche n'a été fusionné par accident.

Ne pas rebaser ou fusionner mécaniquement simplement pour supprimer cette divergence : reconstruire d'abord l'intention du prochain lot et traiter les éventuels conflits au niveau responsable.

## Prochaine décision produit légitime

La prochaine étape n'est plus « trouver encore des relations ». Elle nécessite une décision humaine explicite sur l'un des axes suivants :

1. sélectionner un petit sous-ensemble des propositions et les approuver/rejeter éditorialement ;
2. préparer un mécanisme de promotion du sous-ensemble explicitement approuvé vers le store canonique, sans effet recherche dans un premier temps ;
3. ouvrir une nouvelle phase produit distincte avec un objectif concret justifiant l'utilisation de relations validées ;
4. laisser cette branche comme prototype/revue et revenir à une autre priorité Biblaw.

Un simple « continue » ne vaut pas approbation sémantique de relations individuelles.

## Reprise rapide

Pour une nouvelle conversation :

1. vérifier HEAD réel de `main` et de `work/theme-relation-candidates` ;
2. vérifier le dernier run CI de la branche ;
3. lire `AI_START_HERE.md` / Grand Père, puis ce fichier ;
4. considérer les fichiers `case-*.json` comme mémoire détaillée des propositions, pas comme vérité validée ;
5. vérifier que `theme-relations-validated.json` est toujours vide avant toute promotion ;
6. reprendre seulement à partir d'un objectif utilisateur ou produit explicite ;
7. appliquer `objectif → état réel → plus petit écart important → frontière responsable → modification minimale → preuve → CONTINUE / PIVOT / STOP`.
