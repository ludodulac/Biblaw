# Audit recherche textuelle littérale — 2026-09-07

## Objet

Poursuite de l’audit de recherche demandé dans `PASSATION-NOUVELLE-CONVERSATION.md`, sans modification de l’index thématique canonique.

Le problème déterministe identifié concernait le mode `Mots et phrases` et le compteur d’occurrences textuelles affiché en parallèle d’un thème reconnu.

## Problème constaté

La fonction de recherche textuelle traitait une requête composée de plusieurs mots comme une correspondance partielle : un seul terme de la requête suffisait pour retenir un document.

Conséquence : une requête telle que `alliance de lumière` pouvait être élargie artificiellement par des mots isolés comme `de` ou `lumière`, alors que l’interface parlait de l’occurrence du « mot ou de l’expression ».

Le moteur incluait également `conceptIds` dans le texte recherchable. Une métadonnée sémantique pouvait donc contribuer à un résultat présenté comme textuel, ce qui brouillait la distinction produit déjà validée entre thème indexé et occurrence littérale.

## Correction appliquée

Fichier : `js/biblaw.js`.

Commit fonctionnel : `9be3aa713e00cc4e9f30f7353aa78664f9fd6448` (`Make textual search literal for phrases`).

Décisions techniques :

- une requête textuelle est désormais recherchée comme une séquence normalisée contiguë ;
- la correspondance est bornée par les mots : `Dieu` ne correspond pas à `dieux` ;
- pour un psaume, la recherche textuelle porte sur le titre et les versets, pas sur les `conceptIds`, ni sur une couche sémantique ;
- pour les autres types de documents activés explicitement par l’utilisateur, elle porte sur les champs textuels affichables (`title`, `text`, `summary`) ;
- les versets affichés dans « Passage où la recherche apparaît » doivent contenir l’expression complète recherchée ;
- le surlignage reste volontairement lexical mot par mot. Il demeure un effet de présentation et ne définit pas la correspondance.

Cette correction ne modifie ni les thèmes, ni leurs alias, ni leurs relations, ni leurs niveaux d’importance.

## Garde-fou CI

Fichier : `.github/workflows/validate-search-ui.yml`.

Commit : `a73289c5ab6104638c7bd0dc63a2c9e73eab495a` (`Validate literal phrase search contract`).

La CI vérifie désormais notamment :

- l’absence des `conceptIds` dans la recherche textuelle navigateur ;
- l’absence de l’ancien calcul `terms.filter` ;
- la présence du contrat de recherche littérale ;
- `Alliance de lumière.` correspond à `alliance de lumière` ;
- `Alliance dans la lumière.` ne correspond pas à `alliance de lumière` ;
- `Dieu` correspond à `dieu` ;
- `dieux` ne correspond pas à `dieu` ;
- la distinction thème / occurrence textuelle reste exposée par l’interface.

Le job `Validate thematic search UI` associé au commit `a73289c5...` a passé toutes ses étapes, y compris `node --check js/biblaw.js`, le contrat UI/recherche et le contrat du runtime thématique.

La publication GitHub Pages du même commit a également réussi.

## Comptages littéraux de l’audit

Les tests CI ont mesuré, sur le bundle navigateur courant, les nombres de psaumes contenant littéralement chaque requête selon le nouveau contrat :

| Requête | Psaumes avec occurrence littérale |
| --- | ---: |
| `Dieu` | 668 |
| `alliance` | 508 |
| `alliance de lumière` | 90 |
| `lumière` | 1079 |
| `assemblée` | 76 |
| `l’assemblée` | 17 |
| `sainte assemblée` | 58 |
| `la sainte assemblée` | 48 |
| `argent` | 62 |
| `chouette` | 3 |
| `abeille` | 7 |
| `22 commandements` | 9 |

Ces nombres décrivent uniquement une présence textuelle normalisée dans les psaumes du bundle navigateur. Ils ne constituent pas un décompte thématique et ne doivent pas être utilisés pour élargir automatiquement un thème canonique.

Le bundle testé contient 1876 enregistrements, dont 1189 enregistrements de type psaume. Le rapport canonique d’analyses thématiques reste une couche distincte et n’est pas modifié par cet audit.

## Règle à préserver

Le mode `Thèmes` répond à la question : « quels psaumes ont été indexés sous ce thème ? »

Le mode `Mots et phrases` répond à la question : « dans quels textes cette formulation apparaît-elle littéralement ? »

Une correspondance dans l’un ne doit pas être fabriquée à partir de l’autre.
