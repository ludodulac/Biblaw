# 2026-09-09 — Relations thématiques transversales

## Objet de cette reprise

Reprendre Biblaw depuis l’état réel de GitHub sans relancer les analyses canoniques des 1158 psaumes, diagnostiquer le cas « licorne », puis introduire le plus petit enrichissement générique permettant de préparer une cartographie thème ↔ thème sans affaiblir la rigueur sémantique.

## État réel de départ

- branche principale réelle : `main` ;
- HEAD observé au début de la reprise : `a9597a37dcdd6bb0893ca722652a872132a6856c` (`Publish only staged Pages production assets`) ;
- le workflow Pages correspondant était terminé avec succès ;
- le rapport de validation thématique courant indique 44 livres, 1158 analyses, 10409 relations thématiques, 0 erreur et 0 avertissement ;
- les analyses par psaume restent canoniques ; les index, annuaires, graphes et catalogues aval restent générés ;
- les cooccurrences existantes ne constituent pas des affirmations sémantiques.

## Discipline d’exécution retenue

La reprise suit systématiquement :

`FAST → TARGETED → FULL`

Le FULL n’est pas utilisé lorsqu’un contrôle plus petit apporte la preuve recherchée.

Les gros artefacts générés ne sont pas ouverts ou reconstruits si un index ou une fiche plus petite suffit. Toute validation ajoutée dans ce lot est bornée et ne reconstruit ni corpus ni index.

## Garde-fous contre les opérations anormalement longues

Les workflows existants possèdent déjà plusieurs protections : préflight FAST avant les validations profondes, timeouts globaux et timeouts des sous-processus, signalement des étapes lentes et refus de rejouer aveuglément un résultat devenu obsolète.

Aucune modification de ces garde-fous n’a été faite faute de preuve d’un défaut actuel.

Pour le nouveau diagnostic de relations thématiques, un workflow dédié de branche a été ajouté avec un timeout de 2 minutes. Aucun générateur et aucun FULL n’y sont appelés.

## Diagnostic réel du cas « licorne »

Le cas a été retrouvé dans les données GitHub :

- enregistrement : `book-05-psalm-024` ;
- thème : `union-pere-nature` ;
- formulation : « Union au Père et à la nature » ;
- occurrence actuelle de ce thème dans l’index : 1 ;
- le thème est réellement attesté dans le psaume et n’est donc pas un faux positif lexical.

La preuve par psaume montre que ce thème exprime l’union de l’aspiration vers le Père avec l’incarnation du corps dans la nature.

Dans l’index transversal actuel :

- `union` : 48 occurrences ;
- `pere` : 75 occurrences ;
- `nature` : 40 occurrences.

Conclusion : le problème n’est pas l’existence de `union-pere-nature`. Le manque réel est l’absence d’une couche générale de relations sémantiques typées entre thèmes. L’index de recherche actuel connaît les formulations comme entrées distinctes mais ne peut pas exprimer que certaines sont potentiellement composées, plus générales, plus spécifiques, variantes ou liées.

## Ce qui existait déjà et doit être réutilisé

### Audit de qualité thématique

`data/thematic-index/theme-quality-audit.json` détectait déjà :

- 1247 thèmes ;
- 924 thèmes singleton ;
- 1050 thèmes ayant au plus 2 occurrences ;
- 186 libellés composites candidats ;
- aucune fusion ou renommage sémantique automatique.

`union-pere-nature` faisait déjà partie de ces 186 composites. Le nouveau travail ne crée donc pas une seconde notion concurrente de « fragmentation » : il réutilise ce périmètre.

### Pilote conceptuel `chouette`

`data/concepts/chouette.json` montre déjà une philosophie utile : sens distincts, références exactes, relations explicites et statut de validation humaine.

Il ne fournit cependant pas encore un contrat thème ↔ thème : ses relations `advice`, `principle`, `practice` décrivent le contenu interne du concept.

### Consolidation livres 01–10

Une première consolidation transversale existe également dans `data/thematic-index/consolidations/books-01-10.json`. Elle reste utile comme travail éditorial antérieur, mais ses thèmes liés ne constituent pas encore un graphe exhaustif de relations typées et validées.

## Enrichissement minimal implémenté

Branche de travail : `work/theme-relation-candidates`.

### Rapporteur FAST

`scripts/report_theme_relation_candidates.py`

Rôle : proposer des composantes structurelles à examiner à partir du sous-ensemble de composites déjà produit par l’audit qualité.

Garanties :

- lecture seule ;
- aucune modification des données ;
- aucune fusion ;
- `relationStatus: relation_candidate` ;
- `semanticClaim: false` ;
- validation humaine obligatoire ;
- la structure lexicale produit une candidature, jamais une vérité sémantique.

Pour `union-pere-nature`, le rapport réel propose `pere`, `union` et `nature`. Cela signifie uniquement « composante à examiner » et jamais `pere = union-pere-nature`.

### Audit de non-régression des candidats

`scripts/audit_theme_relation_candidates.py`

Sentinelles actuelles :

- `union-pere-nature` → `union`, `pere`, `nature` ;
- `alliance-de-lumiere` → `alliance`, `lumiere` ;
- `nature-vivante` → `nature` ;
- `union-et-soutien-mutuel` → `union`, `soutien-mutuel`.

L’audit vérifie également que toutes les relations du lot restent des candidats non sémantiques soumis à validation humaine.

## Mesure du phénomène sur les 186 composites existants

Résultat TARGETED :

- composites audités : 186 ;
- composites avec au moins une composante candidate : 145 ;
- composites sans composante candidate par cette règle : 41 ;
- relations `component` candidates produites : 270 ;
- composites singleton avec au moins une composante candidate : 136.

Distribution du nombre de candidats par thème :

- 1 candidat : 53 thèmes ;
- 2 candidats : 71 ;
- 3 candidats : 12 ;
- 4 candidats : 6 ;
- 5 candidats : 3.

Ces chiffres montrent qu’une fragmentation potentielle existe à une échelle suffisante pour justifier une couche de revue générique, mais ils ne valident aucune relation sémantique.

## Contrat sémantique

`data/thematic-index/THEME-RELATIONS-CONTRACT.md`

Le contrat sépare :

- nature de relation : `equivalent_to`, `variant_of`, `broader_than`, `component_of`, `related_to` ;
- statut : `relation_candidate` ou `relation_validated`.

Les inverses sont dérivés plutôt que stockés en double :

- `broader_than` → vue inverse `narrower_than` ;
- `component_of` → vue inverse `has_component`.

Le contrat a été précisé après le pilote :

- le premier graphe exploitable par la recherche relie uniquement des `themeId` réellement présents dans `theme-search-index.json` ;
- les preuves sont indexées par `themeId` avec `evidenceByThemeId` afin de rester non ambiguës lorsqu’une candidature est retypée ou change de direction ;
- une relation validée devra conserver des occurrences réelles des deux thèmes, les versets pertinents, l’enseignement thématique correspondant et une note de validation humaine ;
- une validation de relation ne déclenche jamais automatiquement une fusion d’identifiants.

## Frontière entre couches thématiques

Un test volontaire sur `fidelite-et-infidelite` a révélé une distinction architecturale à préserver : cette fiche existe dans `data/thematic-index/themes/fidelite-et-infidelite.json`, mais cet identifiant n’existe pas dans `theme-search-index.json`.

L’analyse par psaume correspondante (`book-17-psalm-105`) emploie en revanche le thème `fidelite`, avec un enseignement directement ancré dans les versets. La fiche `fidelite-et-infidelite` est donc une consolidation éditoriale de recherche et ne doit pas être traitée automatiquement comme une entité de recherche canonique.

`scripts/report_theme_layer_coverage.py` mesure ce recouvrement sans modifier les données. Résultat :

- thèmes de l’index de recherche : 1247 ;
- fiches éditoriales dans `data/thematic-index/themes/` : 38 ;
- identifiants présents dans les deux couches : 24 ;
- fiches éditoriales sans identifiant homonyme dans l’index de recherche : 14 ;
- fichier éditorial malformé : 0.

Les 14 identifiants éditoriaux seuls sont actuellement : `fidelite-et-infidelite`, `hierarchies`, `intelligence-superieure`, `libre-arbitre`, `maitres-et-sages`, `mensonge-et-illusion`, `nature-et-mere`, `non-savoir`, `perception-et-sens`, `pierres`, `plantes`, `purete-et-verite`, `solidarite-et-soutien-mutuel`, `sommeil-et-reve`.

Conséquence : les fiches éditoriales peuvent fournir du contexte et des hypothèses, mais ne doivent pas être injectées silencieusement comme thèmes de recherche.

## Lot pilote de revue sémantique

`scripts/report_theme_relation_review_context.py` parcourt uniquement les 44 analyses thématiques par livre et restitue un nombre borné d’occurrences attestées pour quelques `themeId` : psaume, importance, directness, versets et enseignement. Il ne génère rien et ne valide aucune relation.

Le lot est stocké dans `data/thematic-index/reviews/theme-relations-pilot.json`. Il reste volontairement non canonique :

- `status: proposed-review-decisions` ;
- `semanticClaim: false` ;
- `requiresHumanApproval: true` ;
- `publicSearchEffect: false`.

Le lot contient maintenant huit décisions proposées :

- `union` → `union-pere-nature` : `component_candidate` retypé en `broader_than` ;
- `pere` ↔ `union-pere-nature` : candidature `component_of` rejetée, `related_to` proposé ;
- `nature` ↔ `union-pere-nature` : même rejet prudent, `related_to` proposé ;
- `alliance` → `alliance-de-lumiere` : retypé en `broader_than` ;
- `lumiere` ↔ `alliance-de-lumiere` : composante rejetée, `related_to` proposé ;
- `nature-vivante` → `nature` : retypé en `variant_of` ;
- `union` → `union-et-soutien-mutuel` : candidature conservée comme `component_of` ;
- `soutien-mutuel` → `union-et-soutien-mutuel` : candidature conservée comme `component_of`.

Les deux cas positifs `component_of` sont ancrés dans `book-22-psalm-142`, notamment le verset 26 qui nomme explicitement « l’union et le soutien mutuel » comme conditions conjointes de la force collective. Le thème cible est donc ici une conjonction attestée de deux dimensions autonomes ; chaque dimension est une composante sans épuiser le thème complet.

Cette comparaison précise une distinction importante : une structure lexicale composite peut correspondre à une vraie composition (`union` + `soutien-mutuel`), mais aussi à un rapport général/spécifique (`alliance` / `alliance-de-lumiere`), à une variante (`nature-vivante` / `nature`) ou seulement à des thèmes liés (`lumiere` / `alliance-de-lumiere`).

`scripts/audit_theme_relation_review_pilot.py` exige désormais la présence des trois issues `accepted`, `retyped`, `rejected`, vérifie les preuves contre les analyses thématiques et impose que le pilote couvre `component_of`, `broader_than`, `related_to` et `variant_of` sans inventer artificiellement une relation `equivalent_to`.

## Test spécifique de l’équivalence et des alias ambigus

`scripts/report_theme_alias_collisions.py` dérive les alias normalisés partagés par plusieurs `themeId` de recherche.

Le rapport retrouve exactement les 5 ambiguïtés déjà déclarées par `theme-search-index.json` et vérifie que le compte dérivé reste égal à `ambiguousAliasCount`.

Collisions actuelles :

- `alliance de lumiere` → `alliance`, `alliance-de-lumiere` ;
- `nutrition subtile` → `nutrition`, `nutrition-subtile` ;
- `service du monde divin` → `service`, `service-du-monde-divin` ;
- `temple interieur` → `temple`, `temple-interieur` ;
- `transmission aux generations` → `transmission`, `transmission-aux-generations`.

Résultat sémantique : une collision d’alias exacte ne constitue pas une preuve d’équivalence. Le cas `alliance de lumiere` est déjà un contre-exemple direct : l’examen du corpus conduit à proposer `alliance` comme thème plus général que `alliance-de-lumiere`, pas comme équivalent.

Aucune relation `equivalent_to` n’est donc proposée à ce stade. Cette absence est volontaire : le modèle ne doit pas remplir artificiellement tous les types du contrat lorsqu’aucune preuve suffisamment forte n’a été trouvée.

## Stockage canonique des relations validées

Le fichier `data/thematic-index/theme-relations-validated.json` a été ajouté comme source éditoriale canonique dédiée aux relations effectivement approuvées.

État actuel :

- `generated: false` ;
- `endpointLayer: theme-search-index` ;
- `publicSearchEffect: false` ;
- `relations: []`.

Le fichier est donc volontairement vide. Aucune des huit propositions du pilote n’a été promue automatiquement.

`scripts/audit_validated_theme_relations.py` protège cette couche. Pour toute future relation validée, il vérifiera notamment :

- extrémités présentes dans la couche de recherche ;
- `relationStatus: relation_validated` ;
- `semanticClaim: true` ;
- `validation.status: human-approved` et note non vide ;
- preuves exactement indexées par les deux `themeId` ;
- occurrence réelle du thème dans le `recordId` cité ;
- versets réellement attestés ;
- enseignement identique à celui de l’analyse canonique ;
- absence de doublons symétriques inversés ;
- absence de relations directionnelles contradictoires en sens inverse.

Comme le stockage est encore vide, l’audit exécute aussi 5 cas négatifs en mémoire avec le même validateur afin d’éviter un succès vacu : candidat dans le stockage validé, extrémité hors couche, verset non attesté, doublon symétrique inversé, plus un cas positif de contrôle.

## Validation TARGETED réelle

Workflow : `.github/workflows/audit-theme-relation-candidates.yml`.

- timeout : 2 minutes ;
- aucun générateur ;
- aucun FULL ;
- audits et diagnostics bornés uniquement.

Jalons récents :

- run n°8 : preuves du pilote vérifiées contre les analyses thématiques — succès ;
- run n°9 : stockage canonique validé vide + 5 self-tests du validateur — succès ;
- run n°12 : ajout des deux cas positifs `component_of` — succès ;
- run n°13 : contrôle croisé des 5 collisions d’alias + ensemble des audits — succès.

Les étapes Python restent de l’ordre de quelques dixièmes de seconde ; le temps principal du workflow reste le checkout/setup GitHub.

## Ce qui n’a volontairement pas été fait

- aucune réanalyse des 1158 psaumes ;
- aucun rebuild massif ;
- aucune fusion de thèmes ;
- aucune modification des analyses canoniques ;
- aucune modification de la recherche publique ;
- aucune modification de l’interface ;
- aucune introduction transversale générée par IA ;
- aucune promotion automatique de candidat en relation validée ;
- aucune décision du lot pilote n’est encore déclarée `relation_validated` ;
- aucune relation `equivalent_to` n’a été inventée faute de preuve suffisante.

## Prochaine frontière

La structure technique du stockage validé existe maintenant et son audit est opérationnel. Le verrou restant n’est plus technique mais éditorial : une relation ne peut entrer dans `theme-relations-validated.json` qu’après une approbation humaine explicite de la décision et de ses preuves.

Avant toute traversée dans la recherche, il reste utile d’élargir légèrement le lot de revue à quelques formulations très différentes pour vérifier que les distinctions observées restent stables, en particulier les cas où la négation, un qualificatif ou une relation grammaticale produisent une fausse proximité lexicale.

Après approbation d’un petit sous-ensemble seulement, la première intégration produit devra rester additive et séparée : correspondance directe actuelle d’un côté, relations validées traversées de l’autre, sans exposer les candidats ni modifier la canonicalisation.