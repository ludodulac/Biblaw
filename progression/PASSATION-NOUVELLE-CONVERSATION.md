# PASSATION BIBLAW — nouvelle conversation

> Point d’entrée permanent pour reprendre Biblaw sans casser le travail validé.
> Dernière consolidation : 2026-09-07.

## 1. Mission

Construire Biblaw comme une expertise structurée et interrogeable du corpus de la **Bible essénienne (classée par livres).pdf**, avec une indexation thématique riche, traçable et navigable.

Le projet n’a pas pour but de produire une interprétation définitive des psaumes. Il doit **indexer, répertorier et relier** les thèmes, notions, images, entités, oppositions, répétitions et correspondances présents dans le corpus afin de permettre une recherche utile.

## 2. Position d’analyse à respecter

Le travail doit rester neutre et humble :

- ne pas prétendre épuiser le sens des psaumes ;
- accepter plusieurs niveaux de lecture ;
- décrire les affirmations du corpus comme internes au corpus ;
- distinguer explicite, contextuel, symbolique, indirect et éditorial ;
- ne jamais transformer une cooccurrence en synonymie, causalité ou doctrine ;
- préférer les formulations documentaires : « le texte présente », « le psaume associe », « ce passage relie », « dans ce psaume… ».

## 3. Source autoritative

Pour toute donnée doctrinale, contextuelle, éditoriale ou thématique :

- source autoritative unique : `Bible essénienne (classée par livres).pdf` et les source packs dérivés ;
- aucune source externe pour enrichir ou corriger le contenu sémantique ;
- les prières restent liées aux psaumes mais ne sont pas une source primaire de thèmes ;
- une ambiguïté de fond réellement indécidable doit être documentée dans `data/incoherences.json`.

## 4. État canonique validé

Toujours relire `data/thematic-index/validation-report.json` avant de citer les nombres.

État courant au 2026-09-07 :

- `status`: `passed`
- **44 livres**
- **1158 analyses de psaumes**
- **10409 relations thématiques**
- **0 erreur**
- **0 avertissement**

Tous les livres 1–44 sont à la profondeur canonique `deep-content-grounded`.

## 5. Anomalies documentaires connues

Préserver ces cas établis par le PDF :

1. Livre 15 / Psaume 75 : numérotation source 15–27 ; le Psaume 76 repart ensuite à 1.
2. Livre 23 / Psaume 128 : source imprimée 49–82, canonique 1–34, offset 48 ; question après 22, réponse 23.
3. Livre 26 / Psaume 186 : source 23–50.
4. Livre 32 / Psaume 182 : source 28–50, restauré depuis le PDF.
5. Livre 35 / Psaume 215 : source 26–46.
6. Livre 36 / Psaume 217 : source 16–36.
7. Livre 38 / Psaume 260 : source 23–54.
8. Livre 44 / Psaume 285 : versets 1–16 seulement ; annexe finale détachée.

Ne pas « réparer » ces structures selon une attente conventionnelle si le PDF montre autre chose.

## 6. Architecture canonique

Fichiers importants :

- `data/thematic-index/books/book-XX.json` : analyses thématiques canoniques ;
- `data/thematic-index/theme-directory.json` : annuaire transversal généré ;
- `data/thematic-index/theme-search-index.json` : alias de recherche générés ;
- `data/thematic-index/theme-connections.json` : graphe neutre de cooccurrence ;
- `data/thematic-index/theme-search-runtime.json` : runtime compact navigateur ;
- `data/thematic-index/SEARCH-CONTRACT.md` : contrat de recherche ;
- `data/browser-search-catalog.json` : bundle navigateur ;
- `data/incoherences.json` : registre des ambiguïtés éditoriales.

Scripts structurants :

- `scripts/build_thematic_directory.py`
- `scripts/build_thematic_search_index.py`
- `scripts/validate_thematic_search_index.py`
- `scripts/build_thematic_connections.py`
- `scripts/validate_thematic_connections.py`
- `scripts/build_thematic_search_runtime.py`
- `scripts/build_browser_search_catalog.py`
- `scripts/audit_thematic_search_quality.py`
- `scripts/audit_production_search_queries.py`
- `scripts/audit_assembly_theme_context.py`
- `scripts/audit_psalm_number_search.py`
- `scripts/run_canonical_thematic_pipeline.py`

Toujours modifier un générateur ou une source canonique plutôt qu’une sortie générée lorsque cela s’applique.

## 7. Qualité actuelle de la recherche thématique

Runtime courant :

- **1251 thèmes** ;
- **1343 alias normalisés** ;
- **9 alias ambigus** ;
- `semanticMerging: false` ;
- `connectionMeaning: psalm-cooccurrence-only`.

Règles :

- alias ≠ fusion sémantique ;
- cooccurrence ≠ synonymie ;
- ne pas fusionner automatiquement les quasi-doublons lexicaux ;
- ne pas supprimer automatiquement les thèmes singleton ;
- un thème composite n’est pas une erreur par principe ;
- un classement n’est pas une hiérarchie de vérité.

## 8. Trois intentions de recherche distinctes

Le moteur distingue désormais explicitement :

1. **numéro de psaume** : accès documentaire ;
2. **Thèmes** : relations éditoriales canoniques ;
3. **Mots et phrases** : occurrences littérales.

Une couche ne doit jamais fabriquer les résultats d’une autre.

### Recherche par numéro

Un entier positif seul (`105`) ou précédé de `psaume` (`psaume 105`) cherche exactement le champ `number` des psaumes.

- la résolution intervient avant les modes thème/texte ;
- le filtre Archange reste actif ;
- si plusieurs livres portent le même numéro, **toutes** les correspondances sont montrées ;
- elles sont distinguées par Archange, livre, titre et référence documentaire ;
- `22 commandements` ou `alliance 22` ne sont pas interprétés comme des recherches de numéro.

Audit : `scripts/audit_psalm_number_search.py`.

État courant : 1158 psaumes canoniques et **295 numéros répétés dans plusieurs livres** ; le moteur ne choisit jamais arbitrairement une occurrence.

## 9. Résolution thématique stricte

La résolution thématique du navigateur suit uniquement :

1. normalisation de requête ;
2. alias explicite du runtime ;
3. sinon libellé canonique ou `themeId` exact après normalisation ;
4. sinon aucun thème.

**Aucun fallback par sous-chaîne ou proximité lexicale.**

Une requête thématique non résolue peut proposer séparément la recherche textuelle lorsqu’une occurrence littérale existe.

## 10. Normalisation française

Articles initiaux neutralisés uniquement comme commodité de requête : `l`, `le`, `la`, `les`, `un`, `une`, `des`.

Exemples :

- `l’assemblée` et `assemblée` ont la même forme de recherche ;
- `la sainte assemblée` et `sainte assemblée` ont la même forme de recherche ;
- **`assemblée` et `sainte assemblée` restent deux notions distinctes**.

Cette neutralisation n’est jamais une fusion sémantique.

## 11. Décision éditoriale « Assemblée / Sainte Assemblée »

La revue du corpus est terminée et tracée dans `data/incoherences.json` avec statut `resolved`.

Décision :

- création du thème canonique `sainte-assemblee` / « Sainte Assemblée » ;
- aucune création d’un thème générique `assemblee` ;
- seulement trois relations directement sourcées :
  - `book-29-psalm-197` — Important — versets 16, 28 ;
  - `book-29-psalm-211` — Important — versets 24, 32 ;
  - `book-29-psalm-212` — Central — versets 4, 9, 16, 20, 25, 26, 27, 28, 31.

Le psaume 212 est intitulé « Fondements moraux et magiques de la sainte assemblée » et explicite directement cette notion.

Contrat de production :

- `assemblée` → aucun thème, route textuelle disponible ;
- `l’assemblée` → idem ;
- `sainte assemblée` → `sainte-assemblee`, 3 psaumes indexés ;
- `la sainte assemblée` → idem.

Ne jamais élargir le thème aux 58 occurrences littérales par simple présence des mots.

## 12. Distinction thème / texte — cas « Dieu »

Décision produit importante : ne pas élargir automatiquement le thème `Dieu` à tous les psaumes contenant le mot.

En mode Thèmes : afficher uniquement les psaumes réellement indexés sous ce thème. En parallèle, si des occurrences textuelles existent, afficher « Deux lectures de cette recherche » et proposer « Voir les occurrences textuelles ».

Même règle pour toutes les requêtes : thème et occurrence lexicale sont des objets différents.

## 13. Bundle navigateur canonique

`data/catalog.json` contient encore 31 anciens fichiers de psaumes sous `data/corpus/<archange>/...` pour des raisons historiques. Le builder navigateur les ignore explicitement et ne publie que les psaumes canoniques sous `data/corpus/books/...`.

État du bundle :

- **1845 enregistrements** au total ;
- **1158 psaumes canoniques** ;
- **31 psaumes legacy ignorés** ;
- couverture parfaite : 1158 psaumes navigateur = 1158 analyses = 1158 psaumes indexés ;
- aucun couple `(psaume, thème)` dupliqué.

La CI reconstruit le bundle et échoue s’il n’est pas reproductible depuis les sources. Le workflow `rebuild-browser-search-catalog.yml` garde le bundle synchronisé lors des changements du corpus/catalogue.

Ne jamais réintroduire les fichiers legacy dans la recherche de production.

## 14. État UI voulu

Site : `https://ludodulac.github.io/Biblaw/`

Fichiers : `index.html`, `css/biblaw.css`, `js/biblaw.js`, `.github/workflows/validate-search-ui.yml`.

Contrat UI :

- recherche vide au chargement ;
- Psaumes coché par défaut ; Prières, Notes, Annexes décochés ;
- filtre Livre supprimé ; filtre Archange conservé ;
- modes `Thèmes` et `Mots et phrases` ;
- champ capable de recevoir thème, mot, expression ou numéro de psaume ;
- résultats thématiques : Central → Important → Lié, puis ordre déterministe ;
- versets d’appui dans « Passage concerné » ;
- `teaching` présenté comme repère contextuel ;
- thèmes secondaires cliquables ;
- thèmes présents à la fin du psaume ouvert ;
- surlignage lexical uniquement ;
- ambiguïtés d’alias montrées explicitement ;
- un clic sur un thème cible directement son ID canonique et force le mode Thèmes.

## 15. Requêtes de production auditées

`audit_production_search_queries.py` couvre :

- `Dieu`
- `alliance`
- `alliance de lumière`
- `lumière`
- `assemblée`
- `l’assemblée`
- `sainte assemblée`
- `la sainte assemblée`
- `argent`
- `chouette`
- `abeille`
- `22 commandements`

État validé :

- `Dieu` → `dieu`, 1 psaume thématique, 662 psaumes littéraux ;
- `alliance` → `alliance`, 157 thématiques, 491 littéraux ;
- `alliance de lumière` → ambiguïté explicite `alliance` + `alliance-de-lumiere`, 158 thématiques, 85 littéraux ;
- `lumière` → `lumiere`, 425 thématiques, 1048 littéraux ;
- `assemblée` → aucun thème, 75 littéraux ;
- `l’assemblée` → aucun thème, 16 littéraux ;
- `sainte assemblée` → `sainte-assemblee`, 3 thématiques (1 Central, 2 Important), 58 littéraux ;
- `la sainte assemblée` → même thème, 3 thématiques, 48 littéraux ;
- `argent` → `argent`, 6 thématiques, 61 littéraux ;
- `chouette` → `chouette`, 1 thématique, 2 littéraux ;
- `abeille` → `abeille`, 2 thématiques, 7 littéraux ;
- `22 commandements` → `22-commandements`, 1 thématique, 9 littéraux.

Toutes les occurrences thématiques représentatives de cet audit ont des versets d’appui et un `teaching`.

## 16. CI et discipline de modification

Avant toute modification :

- re-fetch le fichier et utiliser son SHA courant ;
- corriger les erreurs techniques déterministes automatiquement ;
- modifier les générateurs plutôt que les sorties générées ;
- ne pas fabriquer de relation sémantique à partir d’une fréquence ou d’une proximité lexicale ;
- faire passer les audits de recherche après modification ;
- vérifier GitHub Pages après les changements de production.

Le pipeline canonique régénère et valide les couches thématiques dans un ordre déterministe. Ne pas revenir à des publications naïves non-fast-forward.

## 17. Limite de vérification de l’environnement actuel

Les contrôles automatisés, les logs CI et les déploiements GitHub Pages sont vérifiables depuis cet environnement.

L’interaction visuelle réelle dans un navigateur avec clics et rendu n’a pas été exécutée ici faute d’outil de navigateur interactif exposé. **Ne pas prétendre qu’un audit visuel manuel a été effectué.**

Lorsqu’un navigateur interactif est disponible, refaire un passage de bout en bout sur les requêtes de la section 15 et sur quelques numéros répétés.

## 18. Travail éditorial volontairement différé

Ne pas lancer encore de grandes synthèses automatiques globales de thèmes.

Cette phase devra être séparée et, pour chaque thème :

- examiner toutes les occurrences ;
- tenir compte des versets, contextes, niveaux d’importance et connexions ;
- distinguer les manières différentes dont le thème apparaît ;
- employer des formulations contextuelles plutôt qu’une définition définitive.

## 19. Règle d’autonomie

Quand le propriétaire dit « continue », « vas-y », « fais-le » : avancer réellement.

- ne pas demander validation étape par étape ;
- résoudre les problèmes techniques déterministes automatiquement ;
- prendre les décisions éditoriales lorsque le corpus permet de les fonder avec une traçabilité suffisante ;
- demander l’avis humain seulement pour une ambiguïté réellement indécidable ou une décision produit structurante ;
- documenter les ambiguïtés non bloquantes dans `data/incoherences.json`.

## 20. Procédure de reprise

1. lire cette passation ;
2. lire les dernières notes de `progression/`, en particulier `2026-09-07-recherche-numero-et-sainte-assemblee.md` ;
3. lire `data/incoherences.json` ;
4. lire `data/thematic-index/validation-report.json` ;
5. vérifier HEAD `main` et les workflows récents ;
6. re-fetch avant toute écriture ;
7. vérifier le déploiement Pages ;
8. reprendre par des audits de recherche/navigation et des améliorations techniques déterministes ;
9. ne pas utiliser de source externe pour une décision thématique ;
10. écrire les décisions méthodologiques importantes dans `progression/`.

## 21. Principe final

Si cette passation et le dépôt semblent se contredire, **le dépôt courant, les rapports et les générateurs priment**.

Le but de cette passation est de permettre une reprise immédiate avec les mêmes règles de neutralité, de traçabilité, de séparation des couches et de prudence sémantique, sans casser l’index canonique ni réintroduire d’anciens comportements approximatifs.
