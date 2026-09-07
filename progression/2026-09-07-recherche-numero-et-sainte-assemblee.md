# 2026-09-07 — Recherche par numéro et revue « Sainte Assemblée »

## Objet

Cette séquence poursuit la stabilisation de la recherche de production sans mélanger les couches documentaire, textuelle et thématique.

## Recherche documentaire par numéro de psaume

Le moteur accepte désormais un entier positif seul (`105`) ou précédé de `psaume` (`psaume 105`) comme accès documentaire direct.

Décisions :

- la résolution se fait sur le champ canonique `number` des psaumes ;
- elle intervient avant la recherche thématique ou textuelle ;
- elle fonctionne dans les deux modes de l’interface sans changer leur sens ;
- le filtre Archange reste actif ;
- plusieurs livres peuvent porter le même numéro : toutes les correspondances sont affichées, triées par livre puis identifiant ;
- aucun résultat n’est choisi arbitrairement ;
- des requêtes comme `22 commandements` ou `alliance 22` restent des requêtes ordinaires et ne sont pas interprétées comme un numéro.

L’audit `scripts/audit_psalm_number_search.py` contrôle ce contrat. Sur le corpus canonique actuel :

- 1158 psaumes ;
- 295 numéros apparaissent dans plus d’un livre ;
- le numéro 1, utilisé comme échantillon automatique, possède 4 correspondances.

## Séparation stricte des recherches

Le résolveur thématique du navigateur suit désormais uniquement :

1. alias explicite du runtime ;
2. libellé canonique ou `themeId` exact après normalisation ;
3. sinon aucun thème.

Le fallback par sous-chaîne/proximité lexicale a été supprimé. Une requête thématique non résolue peut proposer séparément la recherche littérale, mais ne fabrique pas une relation thématique.

## Revue éditoriale « Assemblée / Sainte Assemblée »

L’audit de contexte a montré deux réalités différentes :

- `assemblée` est employé dans des contextes nombreux et variés ; la fréquence du mot ne suffit pas à justifier un thème générique ;
- `Sainte Assemblée` est explicitement constituée comme notion dans des passages ciblés, notamment le psaume 212 du livre 29, intitulé « Fondements moraux et magiques de la sainte assemblée ».

Décision éditoriale :

- création du thème canonique `sainte-assemblee` / « Sainte Assemblée » ;
- aucune création de thème générique `assemblee` ;
- trois relations seulement, explicitement sourcées :
  - `book-29-psalm-197`, important, versets 16 et 28 ;
  - `book-29-psalm-211`, important, versets 24 et 32 ;
  - `book-29-psalm-212`, central, versets 4, 9, 16, 20, 25, 26, 27, 28 et 31.

La requête `sainte assemblée` et sa variante avec article `la sainte assemblée` résolvent donc `sainte-assemblee`. Les requêtes `assemblée` et `l’assemblée` ne résolvent aucun thème et conservent leur route textuelle.

Aucune relation n’a été créée automatiquement à partir des 58 occurrences textuelles de `sainte assemblée` ou des 75 occurrences de `assemblée`.

## Contrôles après modification

Le pipeline canonique valide :

- 44 livres ;
- 1158 analyses de psaumes ;
- 10409 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

Le runtime contient :

- 1251 thèmes ;
- 1343 alias ;
- 9 alias ambigus conservés ;
- `semanticMerging: false` ;
- connexions interprétées uniquement comme cooccurrences de psaumes.

L’audit des requêtes de production confirme notamment :

- `assemblée` → aucun thème, 75 psaumes littéraux ;
- `l’assemblée` → aucun thème, 16 psaumes littéraux ;
- `sainte assemblée` → `sainte-assemblee`, 3 psaumes indexés (1 Central, 2 Important), 58 psaumes littéraux ;
- `la sainte assemblée` → `sainte-assemblee`, mêmes 3 psaumes indexés, 48 psaumes littéraux ;
- aucun verset d’appui ni `teaching` manquant pour ces résultats.

## Règle durable

Une amélioration de rappel ne doit jamais contourner le contrat éditorial. La recherche doit préférer un « aucun thème reconnu » explicite à une correspondance sémantique supposée.

La recherche par numéro est documentaire et ne doit jamais devenir un alias thématique ou une recherche textuelle déguisée.
