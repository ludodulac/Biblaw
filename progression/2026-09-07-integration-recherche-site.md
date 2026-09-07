# 2026-09-07 — Intégration de la recherche thématique dans le site

## Objectif

Brancher le site Biblaw sur les couches thématiques validées sans transformer les données d’indexation en interprétation exclusive des Psaumes.

## Données utilisées par le navigateur

Le front charge désormais :

- `data/thematic-index/theme-directory.json` pour les thèmes, occurrences, importance et preuves locales ;
- `data/thematic-index/theme-search-runtime.json` pour la résolution compacte des alias et la navigation vers les thèmes cooccurrents.

Le fichier complet `theme-connections.json` reste disponible pour l’audit mais n’est pas chargé directement dans le navigateur, afin d’éviter un payload inutilement lourd.

## Runtime compact

`scripts/build_thematic_search_runtime.py` dérive un payload destiné au navigateur à partir des couches validées.

État courant :

- 1 250 thèmes ;
- 1 342 alias ;
- 9 alias ambigus ;
- 8 thèmes voisins maximum exposés par thème ;
- `semanticMerging: false` ;
- `connectionMeaning: psalm-cooccurrence-only`.

Les alias ambigus conservent tous les `themeId` possibles. Les connexions servent exclusivement à la navigation par cooccurrence dans les Psaumes.

## Recherche thématique du site

`js/biblaw.js` :

- résout d’abord une requête par l’index d’alias ;
- peut retourner plusieurs thèmes lorsque la formulation est ambiguë ;
- agrège les Psaumes correspondants sans fusionner les thèmes ;
- conserve le niveau d’importance éditorial de chaque occurrence ;
- affiche les versets justificatifs et le champ d’indexation associé ;
- propose des thèmes voisins sous la formulation « thèmes également présents dans ces psaumes » ;
- permet de cliquer sur un thème voisin pour relancer une recherche ;
- conserve la recherche textuelle séparée du mode thématique.

## Filtres

Le site permet maintenant de filtrer les résultats :

- par Archange ;
- par Livre ;
- par type de texte dans la recherche textuelle.

La liste des 44 livres est construite automatiquement à partir du corpus chargé ; elle n’est pas codée en dur dans l’interface.

## Ambiguïtés

Une formulation pouvant correspondre à plusieurs `themeId` n’est plus résolue arbitrairement vers un seul thème. Le panneau de navigation indique plusieurs correspondances possibles et le résultat initial conserve l’union des occurrences correspondantes.

Cette règle est importante pour respecter la pluralité des niveaux de lecture et éviter qu’un détail de normalisation lexicale ne devienne une décision éditoriale implicite.

## Validation automatique

Workflow : `.github/workflows/validate-search-ui.yml`.

Contrôles :

- syntaxe JavaScript via `node --check` ;
- présence des éléments DOM attendus par le moteur de recherche ;
- branchement des filtres Archange et Livre ;
- présence et cohérence du runtime thématique ;
- absence d’identifiants de thèmes inconnus ;
- conservation explicite des alias ambigus ;
- absence de fusion sémantique dans le runtime.

Run de référence après intégration du filtre Livre : `34073851393`, succès complet.

## Publication

Le workflow canonique de l’index thématique produit et conserve désormais `theme-search-runtime.json`. Le workflow Pages publie les modifications du front séparément.

La chaîne est ainsi séparée en trois responsabilités :

1. contenu éditorial et indexation profonde ;
2. données dérivées de recherche et de navigation ;
3. interface de consultation.

Cette séparation permet d’améliorer le moteur du site sans réécrire les analyses éditoriales des Psaumes.

## Suite logique

La prochaine amélioration produit peut porter sur la recherche textuelle elle-même : meilleur classement des expressions exactes, affichage du verset réellement correspondant au lieu d’un simple début de Psaume, puis éventuellement facettes supplémentaires. Ces changements doivent rester séparés de la couche d’interprétation thématique.
