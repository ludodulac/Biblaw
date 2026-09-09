# Contrat des relations thématiques transversales

## But

Cette couche complète l’index thématique existant sans modifier les analyses canoniques par psaume et sans fusion automatique des thèmes.

Elle doit permettre de représenter progressivement des relations entre formulations thématiques tout en conservant l’incertitude et la preuve.

## Principes non négociables

- occurrence textuelle ≠ thème ;
- cooccurrence ≠ synonymie ;
- proximité ≠ causalité ;
- similarité lexicale ≠ équivalence sémantique ;
- alias ambigu ≠ alias à résoudre arbitrairement ;
- thème lié ≠ même thème ;
- composante ≠ thème complet ;
- une relation candidate n’est jamais une relation validée ;
- les analyses canoniques par psaume restent la source primaire de preuve ;
- les artefacts générés restent reproductibles depuis leurs sources.

## Couches d’entités

Le premier graphe exploitable par la recherche relie uniquement des `themeId` présents dans `data/thematic-index/theme-search-index.json`, lui-même dérivé des analyses par psaume.

Les fiches de `data/thematic-index/themes/` qui n’ont pas d’identifiant homonyme dans cet index sont des consolidations éditoriales utiles comme contexte de recherche, mais elles ne doivent pas être injectées silencieusement comme extrémités du graphe de recherche.

Une relation persistée doit donc déclarer sa couche d’extrémités. La première version canonique utilise `endpointLayer: "theme-search-index"`.

## Enregistrement minimal d’une relation

Une relation thématique persistée doit séparer sa nature de son statut et indexer les preuves par `themeId`, afin que la preuve ne devienne pas ambiguë lorsqu’une candidature est retypée ou change de direction :

```json
{
  "schemaVersion": 1,
  "id": "union--union-pere-nature--broader-than",
  "sourceThemeId": "union",
  "targetThemeId": "union-pere-nature",
  "relationType": "broader_than",
  "relationStatus": "relation_validated",
  "semanticClaim": true,
  "evidenceByThemeId": {
    "union": [
      {
        "recordId": "book-03-psalm-010",
        "verseNumbers": [1, 7, 8],
        "teaching": "..."
      }
    ],
    "union-pere-nature": [
      {
        "recordId": "book-05-psalm-024",
        "verseNumbers": [3, 7, 9],
        "teaching": "..."
      }
    ]
  },
  "validation": {
    "status": "human-approved",
    "note": "..."
  }
}
```

Le couple `relationType` / `relationStatus` est obligatoire. Un type de relation ne doit jamais encoder implicitement son niveau de validation.

Les preuves sont référencées par identifiant de thème et doivent correspondre à des occurrences réelles dans `data/thematic-index/books/book-*.json`. Le `recordId`, les numéros de versets et l’enseignement recopié doivent rester cohérents avec l’analyse canonique correspondante ; un audit doit signaler toute dérive.

## Types de relation canoniques

### `equivalent_to`

Les deux formulations représentent le même thème dans le corpus, après examen des contextes et preuves. Relation symétrique. Ne signifie pas nécessairement que les identifiants doivent être fusionnés.

### `variant_of`

La source est une formulation contextuelle très proche de la cible, mais il existe une raison de conserver les deux formulations distinctes. Relation directionnelle.

### `broader_than`

La source est sémantiquement plus générale que la cible. L’inverse `narrower_than` est dérivé à l’affichage et ne doit pas être dupliqué dans les données.

### `component_of`

La source constitue une composante conceptuelle attestée de la cible sans constituer à elle seule le thème complet. L’inverse `has_component` est dérivé à l’affichage.

### `related_to`

Les thèmes sont distincts mais une relation thématique explicable et attestée existe entre eux. Relation symétrique. La simple cooccurrence ne suffit pas.

## Statuts

### `relation_candidate`

Une procédure a identifié une relation à examiner. Elle doit conserver :

- la méthode qui a produit la candidature ;
- les thèmes source et cible ;
- les éléments disponibles pour l’examen ;
- `semanticClaim: false` ;
- `validation.status: needs-human-review`.

Une relation candidate ne doit modifier ni la recherche publique ni la canonicalisation.

### `relation_validated`

La relation a été examinée contre le corpus. Elle doit conserver au minimum :

- une ou plusieurs occurrences justificatives pour chacun des deux thèmes ;
- les numéros de versets pertinents ;
- l’enseignement thématique correspondant tel qu’il existe dans l’analyse canonique ;
- une note expliquant pourquoi ce type précis de relation est retenu ;
- `validation.status: human-approved` ;
- `semanticClaim: true`.

La validation d’une relation ne justifie jamais automatiquement une fusion d’identifiants.

## Stockage canonique des relations validées

Le fichier `data/thematic-index/theme-relations-validated.json` est la source canonique dédiée aux relations effectivement approuvées.

Il est éditorial et non généré. Les rapports de candidats, les lots de revue et les sorties de diagnostic ne doivent jamais le réécrire automatiquement.

Sa présence ne modifie pas à elle seule la recherche. L’exploitation par la recherche devra faire l’objet d’un lot séparé et de tests de non-régression spécifiques.

Le fichier peut rester vide tant qu’aucune relation n’a reçu l’approbation éditoriale requise. Un stockage vide et audité est préférable à une promotion implicite des propositions du pilote.

## Inverses et duplication

Pour éviter les contradictions :

- `equivalent_to` et `related_to` sont symétriques et ne sont stockés qu’une fois ;
- `broader_than` produit `narrower_than` comme vue inverse ;
- `component_of` produit `has_component` comme vue inverse ;
- `variant_of` reste directionnel ;
- les deux directions ne doivent pas être maintenues manuellement comme deux vérités indépendantes.

Pour les relations symétriques, l’ordre de stockage des deux extrémités n’a pas de sens sémantique. Un audit doit donc détecter un doublon même si source et cible sont inversées.

## Candidatures automatiques

Une candidature peut utiliser des signaux tels que :

- structure d’une formulation ;
- normalisation ;
- mots ou composantes communs ;
- contexte des psaumes ;
- versets justificatifs ;
- enseignements ;
- importance du thème ;
- cooccurrences comme indice seulement ;
- analyse sémantique contrôlée.

Aucun de ces signaux pris isolément ne valide une relation sémantique.

Le rapport `scripts/report_theme_relation_candidates.py` est un diagnostic généré : ses sorties ne constituent pas des relations canoniques. Il sert à produire une file de revue.

## Cas sentinelle : `union-pere-nature`

Le thème `union-pere-nature` (« Union au Père et à la nature ») est réellement attesté dans `book-05-psalm-024`.

La structure de sa formulation permet de proposer `union`, `pere` et `nature` comme composantes à examiner. Cette proposition ne signifie notamment jamais :

- `pere = union-pere-nature` ;
- `union = union-pere-nature` ;
- `nature = union-pere-nature` ;
- que les quatre thèmes doivent être fusionnés.

Le lot pilote de revue a déjà montré qu’une candidature `component_candidate` peut devoir être retypée ou rejetée. Aucune sortie de ce pilote n’est automatiquement promue dans le stockage validé.

## Intégration produit

Ordre de progression :

1. modèle sémantique ;
2. données candidates et validées ;
3. validation et audits ;
4. exploitation prudente par la recherche ;
5. présentation.

La recherche littérale, la recherche thématique actuelle, la recherche par numéro de psaume et les ambiguïtés correctement représentées doivent rester inchangées tant que la couche de relations validées n’a pas ses propres tests de non-régression.

Une future recherche transversale devra distinguer explicitement :

- correspondance directe actuelle ;
- relation validée traversée ;
- suggestion candidate destinée à la revue et non à l’utilisateur final.

## Introduction transversale d’un thème

La synthèse textuelle d’un thème ne doit pas être produite avant le calcul de données mesurables, notamment : nombre de psaumes, première et dernière occurrence dans l’ordre du corpus, distribution, concentrations, longues absences, récurrences, variantes, importance et particularités attestées.

L’ordre du corpus Biblaw est une dimension distincte d’une éventuelle chronologie historique.