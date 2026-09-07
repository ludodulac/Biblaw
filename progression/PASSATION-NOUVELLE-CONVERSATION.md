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

Un terme n’a pas besoin d’une définition externe ou globale. Son sens peut être développé par plusieurs psaumes et plusieurs formulations contextuelles. Une comparaison externe, même pertinente, ne doit pas servir à normaliser, fusionner, renommer ou définir un thème canonique.

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

Tous les livres 1–44 sont à la profondeur canonique `deep-content-grounded`. Le validateur principal exige désormais aussi exactement 44 fichiers `book-01.json` à `book-44.json`, `method.status: editorial-indexing-complete`, `semanticPass: deep-content-grounded-complete`, `contentGrounding: complete`, `deepPsalmCount` cohérent et des versets d’appui non vides pour chaque relation.

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

## 6. Architecture canonique et frontières historiques

Fichiers importants :

- `data/thematic-index/books/book-XX.json` : analyses thématiques canoniques ;
- `data/thematic-index/theme-directory.json` : annuaire transversal généré ;
- `data/thematic-index/theme-search-index.json` : alias de recherche générés ;
- `data/thematic-index/theme-connections.json` : graphe neutre de cooccurrence ;
- `data/thematic-index/theme-search-runtime.json` : runtime compact navigateur ;
- `data/thematic-index/SEARCH-CONTRACT.md` : contrat de recherche ;
- `data/browser-search-catalog.json` : bundle navigateur ;
- `data/incoherences.json` : registre des ambiguïtés éditoriales.

Les anciens psaumes sous `data/corpus/<archange>/...`, les notes d’extraction legacy non cataloguées et les prototypes sous `data/thematic-index/prototypes/` sont conservés comme historique mais **ne sont pas des entrées de production**. `data/thematic-index/books/` doit contenir exactement les 44 fichiers canoniques.

Le pilote d’extraction du livre 17 conserve volontairement certains anciens identifiants dans ses artefacts historiques. `scripts/normalize_book17_production_attachments.py` constitue la frontière qui normalise les données partagées réellement cataloguées avant génération publique. Ne pas supprimer le pilote simplement pour « nettoyer » le dépôt.

Scripts structurants :

- `scripts/run_canonical_thematic_pipeline.py`
- `scripts/validate_thematic_index.py`
- `scripts/build_thematic_directory.py`
- `scripts/audit_thematic_search_quality.py`
- `scripts/build_thematic_search_index.py`
- `scripts/validate_thematic_search_index.py`
- `scripts/build_thematic_connections.py`
- `scripts/validate_thematic_connections.py`
- `scripts/build_thematic_search_runtime.py`
- `scripts/validate_thematic_search_runtime.py`
- `scripts/build_browser_search_catalog.py`
- `scripts/audit_corpus_attachments.py`
- `scripts/audit_legacy_psalm_references.py`
- `scripts/audit_production_search_queries.py`
- `scripts/audit_assembly_theme_context.py`
- `scripts/audit_psalm_number_search.py`

Toujours modifier un générateur ou une source canonique plutôt qu’une sortie générée lorsque cela s’applique.

## 7. Qualité actuelle de la recherche thématique

Runtime courant :

- **1247 thèmes** ;
- **1339 alias normalisés** ;
- **5 alias ambigus** ;
- **0 collision technique de répertoire normalisé** ;
- `semanticMerging: false` ;
- `connectionMeaning: psalm-cooccurrence-only`.

Les 4 anciennes collisions techniques d’identifiants ont été consolidées après revue du contexte interne, sans perte de relation thématique : `corps-d-eau`, `corps-d-immortalite`, `microcosme-et-macrocosme`, `royaute-interieure`. Les générateurs fautifs ont été corrigés et `normalize_known_theme_identifiers.py --check` empêche leur réintroduction.

Règles :

- alias ≠ fusion sémantique ;
- cooccurrence ≠ synonymie ;
- ne pas fusionner automatiquement les quasi-doublons lexicaux ;
- ne pas supprimer automatiquement les thèmes singleton ;
- un thème composite n’est pas une erreur par principe ;
- une variante de libellé d’un même thème peut exprimer une précision contextuelle et n’est pas une erreur par elle-même ;
- un classement n’est pas une hiérarchie de vérité.

`theme-quality-audit.json` sépare les erreurs structurelles, les ambiguïtés explicites et les candidats de revue contextuelle. Il ne doit jamais auto-fusionner ou auto-renommer un thème.

## 8. Admissibilité avant ranking

Une relation thème–psaume suit deux étapes strictement distinctes :

1. **admissibilité canonique** : la relation existe dans les analyses canoniques et passe `validate_thematic_index.py` (identité, libellé, `directness`, versets, `teaching`, profondeur canonique) ;
2. **ranking** : seulement après admission, `importance` classe `Central → Important → Lié`, puis les critères déterministes d’affichage s’appliquent.

Le ranking ne crée jamais une relation. Un score, une fréquence, une proximité lexicale, une sous-chaîne ou une cooccurrence ne peut jamais faire entrer un psaume dans les résultats thématiques.

## 9. Trois intentions de recherche distinctes

Le moteur distingue explicitement :

1. **numéro de psaume** : accès documentaire ;
2. **Thèmes** : relations éditoriales canoniques ;
3. **Mots et phrases** : occurrences littérales.

Une couche ne doit jamais fabriquer les résultats d’une autre.

### Recherche par numéro

Un entier positif seul (`105`) ou précédé de `psaume` (`psaume 105`) cherche exactement le champ `number` des psaumes.

- la résolution intervient avant les modes thème/texte ;
- le filtre Archange reste actif ;
- si plusieurs livres portent le même numéro, **toutes** les correspondances sont montrées ;
- elles sont distinguées par Archange, livre et titre ;
- `22 commandements` ou `alliance 22` ne sont pas interprétés comme des recherches de numéro.

Audit : `scripts/audit_psalm_number_search.py`.

État courant : 1158 psaumes canoniques et **295 numéros répétés dans plusieurs livres** ; le moteur ne choisit jamais arbitrairement une occurrence.

## 10. Résolution thématique stricte

La résolution thématique du navigateur suit uniquement :

1. normalisation de requête ;
2. alias explicite du runtime ;
3. sinon libellé canonique ou `themeId` exact après normalisation ;
4. sinon aucun thème.

**Aucun fallback par sous-chaîne ou proximité lexicale.**

Une requête thématique non résolue peut proposer séparément la recherche textuelle lorsqu’une occurrence littérale existe. Les alias ambigus conservent tous leurs `themeId` avec `ambiguous: true`.

## 11. Normalisation française

Articles initiaux neutralisés uniquement comme commodité de requête : `l`, `le`, `la`, `les`, `un`, `une`, `des`.

Exemples :

- `l’assemblée` et `assemblée` ont la même forme de recherche ;
- `la sainte assemblée` et `sainte assemblée` ont la même forme de recherche ;
- **`assemblée` et `sainte assemblée` restent deux notions distinctes**.

Cette neutralisation n’est jamais une fusion sémantique.

## 12. Décision éditoriale « Assemblée / Sainte Assemblée »

La revue du corpus est terminée et tracée dans `data/incoherences.json` avec statut `resolved`.

Décision :

- thème canonique `sainte-assemblee` / « Sainte Assemblée » ;
- aucun thème générique `assemblee` ;
- seulement trois relations directement sourcées :
  - `book-29-psalm-197` — Important — versets 16, 28 ;
  - `book-29-psalm-211` — Important — versets 24, 32 ;
  - `book-29-psalm-212` — Central — versets 4, 9, 16, 20, 25, 26, 27, 28, 31.

Contrat de production :

- `assemblée` → aucun thème, route textuelle disponible ;
- `l’assemblée` → idem ;
- `sainte assemblée` → `sainte-assemblee`, 3 psaumes indexés ;
- `la sainte assemblée` → idem.

Ne jamais élargir le thème aux occurrences littérales par simple présence des mots.

## 13. Distinction thème / texte — cas « Dieu »

Ne pas élargir automatiquement le thème `Dieu` à tous les psaumes contenant le mot.

En mode Thèmes : afficher uniquement les psaumes réellement indexés sous ce thème. En parallèle, si des occurrences textuelles existent, proposer séparément les occurrences textuelles.

Même règle pour toutes les requêtes : thème et occurrence lexicale sont des objets différents.

## 14. Bundle navigateur, pièces jointes et runtime

`data/catalog.json` conserve 31 anciens fichiers de psaumes pour des raisons historiques. Le builder navigateur les ignore explicitement et ne publie que les psaumes canoniques sous `data/corpus/books/...`.

État du bundle :

- **1845 enregistrements** au total ;
- **1158 psaumes canoniques** ;
- **31 psaumes legacy ignorés** ;
- couverture parfaite : 1158 psaumes navigateur = 1158 analyses = 1158 psaumes indexés ;
- aucun couple `(psaume, thème)` dupliqué.

Contrat d’attachement actuel : **676 prières**, **11 notes externes**, **265 identifiants de notes internes**. Les prières et notes externes cataloguées doivent pointer vers des IDs canoniques, être réciproques avec le psaume et être cohérentes avec le document/pages source. Le bundle navigateur doit contenir les objets sources courants exactement ; un bundle périmé échoue.

Le runtime thématique suit désormais : **construire candidat → valider contre `theme-search-index.json` et `theme-connections.json` → remplacement atomique → revalidation indépendante**. Il est une projection de navigation seulement et ne crée aucune identité ou relation sémantique.

## 15. État UI voulu

Site : `https://ludodulac.github.io/Biblaw/`

Fichiers : `index.html`, `css/biblaw.css`, `css/theme-index.css`, `js/biblaw.js`.

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
- un clic sur un thème cible directement son ID canonique et force le mode Thèmes ;
- cartes publiques : bouton **Voir** uniquement, sans navigation PDF ;
- téléchargement et impression dans le texte ouvert ;
- aucun lien public vers l’atelier `validation.html` ;
- annuaire des thèmes rendu seulement à son ouverture et filtrable localement, afin de ne pas créer 1247 lignes au chargement.

## 16. Requêtes de production auditées

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

Le test vérifie les identités thématiques attendues, la séparation avec le littéral, l’ordre par importance, la couverture 1158/1158/1158, l’absence de couples thème–psaume dupliqués, l’absence de relations sans versets/`teaching`, les ambiguïtés explicites et l’absence de collision technique.

Ne pas figer inutilement dans la passation des compteurs de résultats susceptibles d’évoluer avec une indexation éditoriale légitime ; les assertions exécutables et les rapports courants priment.

## 17. Publication et CI

La publication Pages ne doit pas être considérée comme un simple upload. Avant déploiement, elle vérifie :

- contrat UI public ;
- annuaire thématique public ;
- runtime thématique ;
- intégrité prières/notes et fraîcheur du bundle ;
- indépendance des identifiants historiques ;
- requêtes de production de référence ;
- recherche documentaire par numéro.

Le pipeline canonique exécute les réparations documentaires, normalisations explicitement revues, passes d’indexation, validation canonique, génération des dérivés, validation du runtime, reconstruction du bundle et audits de frontière de production. Il commit les mêmes catégories de données qu’il vient d’auditer.

## 18. Discipline de modification

Avant toute modification :

- vérifier `main`, les commits/PR récents et les workflows pertinents ;
- lire `SEARCH-CONTRACT.md`, cette passation, les dernières notes de `progression/`, `validation-report.json` et `data/incoherences.json` ;
- distinguer production, prototypes et artefacts historiques ;
- re-fetch le fichier et utiliser son SHA courant ;
- corriger les erreurs techniques déterministes dans les générateurs ;
- ne pas modifier manuellement un artefact généré ;
- ne pas fabriquer de relation sémantique à partir d’une fréquence, cooccurrence, substring ou proximité lexicale ;
- préserver explicitement les alias ambigus ;
- vérifier les audits de recherche et Pages après les changements de production.

Ne pas supprimer, renommer ou réorganiser un artefact uniquement pour rendre le dépôt « plus propre ». Toute suppression doit répondre à un risque ou une obsolescence démontrée et préserver les capacités/données utiles.

## 19. Idées transversales évaluées

Ne pas réintroduire ces abstractions sans nouveau besoin mesuré :

- pas de `confidence`/`unknown` généralisé sur les relations déjà canoniques ; `directness`, versets, `teaching`, validation et `importance` portent des statuts plus précis ;
- pas de champ persistant de « niveau de garantie » : literal-evidence, editorially-indexed, canonical-identity, ambiguous-alias et connection-only restent des natures distinctes documentées par le contrat ;
- pas de manifeste manuel `implemented/tested/verified` : les audits exécutables et la barrière Pages sont la source de vérité ;
- pas de nouvelle architecture de lazy loading tant qu’un problème mesuré ne le justifie pas ; l’annuaire est déjà lazy ;
- pas de couche de personnalisation/visibilité tant qu’aucun parcours personnalisé n’existe. Si cela apparaît, garder un corpus canonique unique et séparer la visibilité.

## 20. Limite de vérification de l’environnement actuel

Les contrôles automatisés, les logs CI et les déploiements GitHub Pages sont vérifiables depuis cet environnement.

L’interaction visuelle réelle dans un navigateur avec clics et rendu n’a pas été exécutée ici faute d’outil de navigateur interactif exposé. **Ne pas prétendre qu’un audit visuel manuel a été effectué.**

Lorsqu’un navigateur interactif est disponible, refaire un passage de bout en bout sur les requêtes de la section 16 et sur quelques numéros répétés.

## 21. Travail éditorial volontairement différé

Ne pas lancer de grande synthèse automatique globale des thèmes.

Pour chaque thème revu :

- examiner toutes les occurrences ;
- tenir compte des versets, contextes, niveaux d’importance et formulations ;
- distinguer les manières différentes dont le thème apparaît ;
- employer des formulations contextuelles plutôt qu’une définition définitive ;
- ne consolider des identifiants que si le corpus interne établit qu’il s’agit d’un doublon technique, jamais sur le seul libellé.

## 22. Règle d’autonomie

Quand le propriétaire dit « continue », « vas-y », « fais-le » : avancer réellement.

- ne pas demander validation étape par étape ;
- résoudre les problèmes techniques déterministes automatiquement ;
- prendre les décisions éditoriales lorsque le corpus permet de les fonder avec une traçabilité suffisante ;
- demander l’avis humain seulement pour une ambiguïté réellement indécidable ou une décision produit structurante ;
- documenter les ambiguïtés non bloquantes dans `data/incoherences.json`.

## 23. Procédure de reprise

1. vérifier HEAD `main`, branches et PR récents ;
2. lire cette passation ;
3. lire `data/thematic-index/SEARCH-CONTRACT.md` ;
4. lire les dernières notes de `progression/`, notamment `2026-09-07-audit-contrats-et-frontieres-production.md` ;
5. lire `data/incoherences.json` ;
6. lire `data/thematic-index/validation-report.json` ;
7. vérifier les workflows récents et le déploiement Pages ;
8. re-fetch avant toute écriture ;
9. reprendre par des audits de recherche/navigation et des améliorations techniques déterministes ;
10. ne pas utiliser de source externe pour une décision thématique ;
11. écrire les décisions méthodologiques importantes dans `progression/`.

## 24. Principe final

Si cette passation et le dépôt semblent se contredire, **le dépôt courant, les rapports et les générateurs priment**.

Le but de cette passation est de permettre une reprise immédiate avec les mêmes règles de neutralité, de traçabilité, de séparation des couches et de prudence sémantique, sans casser l’index canonique ni réintroduire d’anciens comportements approximatifs.
