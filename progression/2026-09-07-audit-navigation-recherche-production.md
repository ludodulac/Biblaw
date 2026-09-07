# Audit recherche et navigation de production — 7 septembre 2026

## Portée

Cette étape stabilise la couche de recherche/navigation de l’interface de production sans modifier le sens des relations thématiques canoniques.

Les sources éditoriales restent `data/thematic-index/books/book-*.json`. Les corrections ci-dessous sont techniques, déterministes ou de présentation. Aucun thème n’a été fusionné, renommé ou créé à partir de simples occurrences lexicales.

## Recherche textuelle

Le mode `Mots et phrases` recherche désormais la formulation complète normalisée, contiguë et bornée par les mots dans le texte affichable du corpus.

Les identifiants sémantiques (`conceptIds`) ne participent plus aux correspondances textuelles. Une expression comme `alliance de lumière` ne correspond donc pas à un passage contenant séparément `alliance` et `lumière`.

Les passages affichés en recherche textuelle sont également sélectionnés à partir de l’expression complète. Le surlignage reste lexical et purement présentatif.

## Séparation Thèmes / Mots et phrases

Le mode `Thèmes` ne retombe plus silencieusement sur une recherche textuelle lorsqu’aucun thème canonique n’est résolu.

Dans ce cas, l’interface indique explicitement qu’aucun thème indexé ne correspond et, si des occurrences littérales existent, propose de basculer vers `Mots et phrases` en conservant la requête.

Pour un thème reconnu comme `Dieu`, l’interface conserve les deux lectures : résultats indexés sous le thème d’un côté, occurrences littérales de l’autre.

## Classement thématique

L’ordre de production est désormais fondé explicitement sur `importance` :

1. `central` ;
2. `important` ;
3. `related`.

Le code ne dépend plus implicitement des poids numériques 3/2/1 du générateur. Les égalités sont départagées de façon déterministe.

## Ambiguïtés et navigation canonique

Le runtime contient actuellement 9 alias ambigus. Ils restent volontairement explicites : aucune fusion automatique n’est effectuée.

Lorsque plusieurs thèmes portent le même libellé visible, les choix affichent désormais un contexte distinctif (volume indexé et identifiant canonique lorsque nécessaire).

Un clic sur un choix ambigu, un thème secondaire dans une carte, un thème dans le psaume ouvert ou un thème dans l’index latéral cible maintenant directement l’identifiant canonique sélectionné. La navigation force le mode `Thèmes` et ne repasse pas par une nouvelle résolution ambiguë du libellé.

## Schéma de l’index latéral

L’interface utilisait encore les anciens champs `psalmCount` et `totalScore`, absents du générateur actuel. Elle utilise désormais les champs canoniques `occurrenceCount` et `score`.

La CI verrouille ce schéma afin d’éviter un affichage `undefined` lors d’une future évolution.

## Bundle navigateur et 31 doublons legacy

L’audit de couverture a initialement signalé 1 189 psaumes dans le bundle navigateur contre 1 158 analyses canoniques.

La cause n’était pas une lacune éditoriale : `data/catalog.json` référence les fichiers canoniques `data/corpus/books/...` et conserve également 31 anciens fichiers de psaumes sous `data/corpus/<archange>/...`.

Le builder `scripts/build_browser_search_catalog.py` concaténait les deux couches. Ces 31 fichiers legacy étaient donc publiés comme doublons de recherche.

Le builder publie maintenant uniquement les psaumes canoniques situés sous `data/corpus/books/`. Les fichiers legacy restent dans le dépôt pour leur valeur documentaire/historique mais ne sont plus des enregistrements de production.

Une CI de fraîcheur reconstruit le bundle et échoue si le fichier commité diverge des sources. Un workflow dédié reconstruit et publie automatiquement `data/browser-search-catalog.json` lorsque le catalogue, le corpus ou son builder change.

État validé après correction :

- 1 845 enregistrements dans le bundle navigateur ;
- 1 158 psaumes canoniques ;
- 31 psaumes legacy ignorés ;
- 1 158 analyses éditoriales ;
- 1 158 psaumes présents dans le répertoire thématique ;
- 0 psaume navigateur sans analyse ;
- 0 analyse sans thème ;
- 0 psaume navigateur sans relation thématique ;
- 0 relation thématique vers un psaume absent ;
- 0 analyse vers un psaume absent ;
- 0 doublon `(psaume, themeId)` dans les relations canoniques.

Cette égalité des trois ensembles d’identifiants est désormais une assertion bloquante de l’audit de production.

## Audit des requêtes de passation après déduplication

Comptages littéraux canoniques observés :

- `Dieu` : 662 psaumes ; thème `dieu` : 1 psaume indexé ;
- `alliance` : 491 ; thème `alliance` : 157 psaumes indexés ;
- `alliance de lumière` : 85 ; résolution ambiguë conservée entre `alliance` et `alliance-de-lumiere`, 158 psaumes indexés au total ;
- `lumière` : 1 048 ; thème `lumiere` : 425 psaumes indexés ;
- `assemblée` : 75 ; aucun thème canonique résolu ;
- `l’assemblée` : 16 ; aucun thème canonique résolu ;
- `sainte assemblée` : 58 ; aucun thème canonique résolu ;
- `la sainte assemblée` : 48 ; aucun thème canonique résolu ;
- `argent` : 61 ; thème `argent` : 6 psaumes indexés ;
- `chouette` : 2 ; thème `chouette` : 1 psaume indexé ;
- `abeille` : 7 ; thème `abeille` : 2 psaumes indexés ;
- `22 commandements` : 9 ; thème `22-commandements` : 1 psaume indexé.

Pour toutes les relations thématiques renvoyées par ces requêtes, les versets d’appui et le champ `teaching` sont présents.

## Cas éditorial restant : Assemblée

Le scan complet des 44 fichiers `book-*.json` ne trouve aucune relation dont le `themeId` ou le libellé normalisé contient `assembl`.

Les occurrences textuelles sont nombreuses, mais leur fréquence ne suffit pas à créer automatiquement un thème ni à décider que `Assemblée` et `Sainte Assemblée` doivent être deux thèmes canoniques.

Ce cas reste donc ouvert dans `data/incoherences.json` et nécessite une décision éditoriale sourcée avant toute modification sémantique.

## Validation

Le commit de durcissement de couverture a passé :

- fraîcheur du bundle navigateur ;
- syntaxe JavaScript ;
- contrat DOM/UI ;
- séparation des modes ;
- tri Central → Important → Lié ;
- navigation directe par identifiant canonique ;
- contrat du runtime thématique ;
- audit des 12 requêtes ;
- égalité des 1 158 identifiants canoniques.

La publication GitHub Pages correspondante s’est terminée avec succès.
