# Passation — relations thématiques transversales

Date de référence : 2026-09-09

Ce document complète `progression/2026-09-09-relations-thematiques-transversales.md`. Il sert de point de reprise compact après la campagne de stress-tests sémantiques. En cas de nouvelle conversation, reconstruire l'état depuis GitHub et utiliser ce document comme orientation, pas comme substitut aux fichiers de revue et aux analyses canoniques.

## État à préserver

- dépôt : `ludodulac/Biblaw` ;
- branche de travail : `work/theme-relation-candidates` ;
- `main` reste volontairement intacte ;
- analyses canoniques : 44 livres, 1158 psaumes ;
- ne pas réanalyser le corpus pour poursuivre ce chantier ;
- `data/thematic-index/theme-relations-validated.json` reste le futur store canonique de relations approuvées et doit rester vide tant qu'aucune approbation humaine explicite n'a été donnée ;
- aucune relation candidate ou proposée ne doit affecter la recherche publique ;
- aucune fusion de thèmes ;
- aucun objectif de densification du graphe ou de réduction du nombre de thèmes.

## Générateur : considéré terminé

`scripts/build_theme_semantic_graph.py` et son audit sont volontairement simples. Ne pas les enrichir sauf défaut réel démontré.

Le générateur doit continuer à :

- lire uniquement les relations explicitement inscrites dans les revues sémantiques prises en charge ;
- ne rien inférer ;
- ne rien fusionner ;
- ne rien normaliser sémantiquement ;
- ne pas utiliser d'heuristique lexicale ;
- ne pas typer automatiquement ;
- ne rien promouvoir dans le store validé ;
- produire un artefact déterministe et reproductible.

Un échec de CI après ajout ou retypage d'une étude de cas peut simplement signifier que `data/thematic-index/reviews/theme-semantic-graph-prototype.json` est périmé. Vérifier d'abord que l'audit des études de cas passe et que l'unique échec est le contrôle de fraîcheur du graphe ; dans ce cas régénérer mécaniquement l'artefact sans modifier le générateur.

## Principe intellectuel central

Pour chaque relation difficile, appliquer le test de reformulation :

> Si les deux concepts étaient reformulés sans leur vocabulaire commun, la relation resterait-elle vraie ?

Relation lexicale ≠ relation conceptuelle. Un mot présent dans un thème composite n'est jamais automatiquement une composante conceptuelle.

Pour une décision difficile, conserver lorsque cela apporte une information réelle : relation proposée, niveau de confiance/statut, relation concurrente plausible, raison de sa plausibilité, test qui départage les types et raison pour laquelle le concurrent échoue ou reste ouvert.

Une frontière explicitement non résolue est préférable à une relation artificiellement certaine.

## Maturité actuelle des cinq distinctions

### `broader_than` / inverse dérivé `narrower_than`

C'est actuellement la distinction la plus stable. Elle résiste bien lorsque le thème cible reste, après reformulation, une application ou détermination réelle d'un concept plus général.

Cas utiles :

- `union` → `union-pere-nature` ;
- `nutrition` → `nutrition-subtile` ;
- `service` → `service-du-monde-divin` ;
- `pierre` → `pierre-verte` ;
- `pensee` → `pensee-verticale` ;
- `maitrise` → `maitrise-pensee-parole`.

Frontière encore intéressante : `oeuvres` → `oeuvres-et-au-dela`. `broader_than` reste proposé mais `related_to` est un concurrent sérieux parce que la cible exprime aussi une relation de conséquence entre accomplissements terrestres et continuité post-mortem.

### `related_to`

Assez mature et surtout désormais utilisé positivement, pas comme simple catégorie résiduelle. Il convient notamment lorsque le second concept utilise le premier comme pôle, objet, opposant, destination ou partenaire sans inclusion conceptuelle démontrée.

Cas structurants :

- `pere` / `nature` ↔ `union-pere-nature` : pôles d'une relation, pas composants automatiques ;
- `imitation` ↔ `discernement-contre-imitation` : objet/opposant du discernement ;
- `abstraction` ↔ `concret-contre-abstraction` : opposition ;
- `pensee` et `parole` ↔ `maitrise-pensee-parole` : instruments/objets à maîtriser, pas pièces de la maîtrise ;
- `eau-et-air` ↔ `terre-eau-air-feu` : proximité cosmologique sans inclusion de la relation binaire ;
- `lumiere` ↔ `apparences-et-fausse-lumiere` : opposition à la vraie lumière malgré le lexème partagé.

### `component_of`

Solide lorsque le psaume atteste des constituants autonomes comme parties du concept complet. Plus fragile pour les relations entre constituants ou pour les termes qui sont seulement objets/pôles d'une action.

Cas solides :

- `corps`, `ame`, `esprit` → `corps-ame-esprit` ;
- `union`, `soutien-mutuel` → `union-et-soutien-mutuel` lorsque le psaume présente explicitement les deux dimensions conjointes.

Frontières :

- `esprit-et-corps` → `corps-ame-esprit` a été retypé en `related_to`; `component_of` reste plausible mais non démontré. Une relation binaire entre deux constituants n'est pas automatiquement une composante de l'architecture qui contient ces constituants.
- `pratique`, `conscience` → `pratique-et-conscience` reste une frontière ouverte : le texte parle de deux aspects simultanés, mais aussi d'une conscience qui naît de la pratique. `component_of` et `related_to` restent en tension.

### `variant_of`

Fonctionnel mais moins stable que `broader_than`. Ne jamais déduire le type de la grammaire ou de l'ajout d'un adjectif.

Contrastes utiles :

- `nature-vivante` → `nature` : variante assez robuste, car le caractère vivant paraît constitutif du référent de base ;
- `soleil-conscience` → `conscience` : variante symbolique assez robuste ;
- `pensee-vivante` → `pensee` : frontière encore fragile, `broader_than` reste un concurrent plausible ;
- `pensee` → `pensee-verticale` : général/spécifique, pas variante ;
- `pierre` → `pierre-verte` : général/spécifique, pas variante.

### `equivalent_to`

Aucun cas positif solide à ce stade. C'est volontaire et acceptable. Alias identique, vocabulaire partagé, proximité locale ou formulation très voisine ne suffisent pas à établir une équivalence corpus-wide.

Ne pas chercher artificiellement à obtenir des `equivalent_to`. `0` peut être le bon résultat.

## Cas adversariaux durables

Les fichiers `data/thematic-index/reviews/case-*.json` et `deferred-composite-boundaries.json` constituent la mémoire détaillée des décisions. Cas particulièrement importants pour une reprise :

- `case-union-pere-nature.json` : général/spécifique, pôles relationnels, variante contextuelle ;
- `case-corps-ame-esprit.json` : composants atomiques réels ;
- `case-nutrition-subtile.json` : alias exact ne prouve pas équivalence ;
- `case-pensee-vivante.json` : frontière `variant_of` / `broader_than` ;
- `case-nature-vivante.json` : propriété constitutive vs sous-classe ;
- `case-discernement-imitation.json` : général/spécifique vs objet d'opposition ;
- `case-concret-abstraction.json` : opposition ≠ composante ;
- `case-present-temporalite.json` : frontières temporelles complexes ;
- `case-maitrise-pensee-parole.json` : correction d'un faux `component_of` lexical ;
- `case-pratique-conscience.json` : vraie frontière ouverte `component_of` / `related_to` ;
- `case-oeuvres-au-dela.json` : frontière `broader_than` / conséquence relationnelle ;
- `case-fausse-lumiere.json` : un qualificatif peut inverser la polarité sémantique ;
- `deferred-composite-boundaries.json` : `maitrise`, `esprit-et-corps`, `eau-et-air`, avec concurrents explicites.

## État du graphe proposé

Après ajout de `case-fausse-lumiere.json`, la reconstruction déterministe attendue contient :

- 48 thèmes/nœuds ;
- 35 relations proposées ;
- 19 fichiers sources de revue ;
- 0 contradiction structurelle ;
- types présents : `broader_than`, `component_of`, `related_to`, `variant_of` ;
- 0 `equivalent_to` positif ;
- `semanticClaim: false` ;
- `requiresHumanApproval: true` ;
- `publicSearchEffect: false`.

Le graphe reste un artefact généré non canonique. Les décisions sémantiques vivent dans les fichiers de revue.

## CI et dernier incident connu

Le run #72, commit `6536f66fd332aace3bcdbebbd45c5328fd46e73e`, était entièrement vert.

L'ajout de `case-fausse-lumiere.json`, commit `a3c98c5dcef23bc45007779c923ab04731a09647`, a produit un run #73 où :

- l'audit des cas sémantiques passe ;
- la construction déterministe passe ;
- l'unique échec est `Audit deterministic semantic graph`, car le graphe commité était périmé après l'ajout du nouveau cas.

L'artefact exact du run #73 a été utilisé pour remettre le graphe commité à jour. Il faut vérifier le run CI du commit de régénération avant de déclarer le HEAD totalement vert.

Ce comportement n'est pas un défaut du générateur et ne justifie aucune modification de celui-ci.

## Ce qui reste à faire avant un passage à plus grande échelle

Le chantier conceptuel est avancé mais pas entièrement clos. Priorité à quelques familles adversariales supplémentaires seulement, pas à l'accumulation de relations.

À éprouver encore en priorité :

1. `component_of` ↔ `related_to` sur composites relationnels, moyens, conditions et interactions ;
2. `variant_of` ↔ `broader_than` sur qualificatifs dont la fonction sémantique est ambiguë ;
3. `broader_than` ↔ `related_to` lorsque le thème cible décrit une conséquence, une destination ou une interaction plutôt qu'une vraie sous-classe ;
4. quelques collisions d'alias exacts pour continuer à tenter de falsifier `equivalent_to` ;
5. une ou deux familles où aucune décision nette n'est possible, afin de vérifier que le format de revue sait conserver honnêtement la frontière.

Familles candidates déjà repérées :

- `union`, `union-des-forces`, `union-et-force-collective` ;
- `communication`, `communication-avec-le-divin` ;
- `dialogue`, `dialogue-avec-la-nature` ;
- `reciprocite`, `reciprocite-avec-la-mere` ;
- `lumiere`, `lumiere-et-obscurite` ;
- collisions exactes autour de `maitrise`, `parole`, `temple`, `volonte` si les preuves canoniques permettent une comparaison réelle.

## Critère de passage à l'échelle

Ne pas passer automatiquement à la cartographie complète parce que le graphe atteint un certain nombre de relations.

Le passage est justifié lorsque les cinq distinctions ont suffisamment résisté aux cas qui les mettent en concurrence et que la revue sait régulièrement produire l'une de ces deux conclusions :

- « X est préférable à Y pour cette raison précise » ;
- « X et Y restent plausibles ; les preuves actuelles ne permettent pas de trancher ».

À ce moment seulement, appliquer la méthode plus largement aux 1247 thèmes, en utilisant les candidats comme aide à la revue et jamais comme affirmation automatique.

## Étapes produit ultérieures — ne pas anticiper

Après un premier sous-ensemble explicitement approuvé humainement :

1. promouvoir seulement ces relations dans `theme-relations-validated.json` avec leurs preuves et notes d'approbation ;
2. auditer le store validé ;
3. concevoir une traversée additive pour la recherche : résultats directs actuels d'un côté, relations validées de l'autre ;
4. ne jamais exposer les candidats non validés ;
5. seulement ensuite travailler les synthèses transversales par thème : nombre de psaumes, première/dernière occurrence dans l'ordre du corpus, distribution, concentrations, longues absences, récurrence, variantes, particularités et différences observables, sans transformer l'ordre du corpus en chronologie historique.

## Règle de reprise rapide

Pour une nouvelle conversation :

1. vérifier le HEAD réel de `work/theme-relation-candidates` et le dernier run CI ;
2. vérifier que `main` n'a pas été modifiée par ce chantier ;
3. lire ce document puis les seuls fichiers de cas concernés par la prochaine famille ;
4. travailler par petites boucles `comprendre → isoler → prouver → modifier → vérifier` ;
5. ne pas toucher au générateur sauf bug réel ;
6. ne pas promouvoir de relation sans approbation humaine explicite ;
7. ne pas connecter la recherche publique avant ce premier lot validé.
