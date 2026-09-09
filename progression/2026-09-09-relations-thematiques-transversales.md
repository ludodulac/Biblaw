# 2026-09-09 — Relations thématiques transversales

## Objet

Reprendre Biblaw depuis l’état réel de GitHub sans relancer les analyses canoniques des 1158 psaumes, diagnostiquer le cas « licorne », puis introduire une couche de revue thème ↔ thème suffisamment rigoureuse pour préparer une cartographie transversale sans fusion automatique, sans réanalyse du corpus et sans modification de la recherche publique.

## État réel de départ

- branche principale : `main` ;
- HEAD de `main` observé au début de la reprise : `a9597a37dcdd6bb0893ca722652a872132a6856c` (`Publish only staged Pages production assets`) ;
- le workflow Pages correspondant était terminé avec succès ;
- validation thématique : 44 livres, 1158 analyses, 10409 relations thématiques, 0 erreur, 0 avertissement ;
- les analyses par psaume restent canoniques ;
- les index, annuaires, graphes et catalogues aval restent générés ;
- cooccurrence, proximité lexicale et alias ne constituent pas des affirmations sémantiques.

Branche de travail de cette reprise : `work/theme-relation-candidates`. `main` n’a pas été modifiée.

## Discipline d’exécution

La reprise suit `FAST → TARGETED → FULL`. Aucun FULL n’a été nécessaire dans ce chantier. Les gros artefacts générés ne sont pas ouverts ou reconstruits lorsqu’un index ou un rapport plus petit suffit.

Le workflow dédié `.github/workflows/audit-theme-relation-candidates.yml` reste borné à 2 minutes, en lecture seule sur les données, sans générateur de corpus ni rebuild global. Les calculs Python restent courts ; checkout/setup GitHub dominent le temps d’exécution.

## Diagnostic du cas « licorne »

Le cas réel est `book-05-psalm-024`, thème `union-pere-nature`, libellé « Union au Père et à la nature », occurrence actuelle : 1. Le thème est directement attesté par les versets 3, 7 et 9 et exprime l’union de l’aspiration vers le Père avec l’incarnation du corps dans la nature.

Dans l’index transversal : `union` = 48 occurrences, `pere` = 75, `nature` = 40. Le défaut n’est donc pas l’existence du thème composite : le manque est une couche de relations sémantiques typées entre thèmes.

La revue propose actuellement :

- `union` → `union-pere-nature` : `broader_than` ;
- `pere` ↔ `union-pere-nature` : `related_to`, candidature `component_of` rejetée ;
- `nature` ↔ `union-pere-nature` : `related_to`, candidature `component_of` rejetée.

Ces propositions restent non canoniques.

## Périmètre de fragmentation déjà existant

`data/thematic-index/theme-quality-audit.json` reste la source du périmètre à examiner :

- 1247 thèmes ;
- 924 singleton ;
- 1050 thèmes avec au plus 2 occurrences ;
- 186 libellés composites candidats ;
- aucune fusion ou renommage automatique.

Le nouveau rapporteur `scripts/report_theme_relation_candidates.py` réutilise ces 186 composites. Il ne crée pas une notion concurrente de fragmentation.

Mesure actuelle :

- 186 composites audités ;
- 145 avec au moins une composante lexicale candidate ;
- 41 sans candidat par cette règle ;
- 270 paires `component_candidate` ;
- 136 composites singleton avec au moins un candidat.

Distribution : 53 cibles ont 1 candidat, 71 en ont 2, 12 en ont 3, 6 en ont 4, 3 en ont 5.

Chaque sortie garde `relationStatus: relation_candidate`, `semanticClaim: false` et `requiresHumanValidation: true`.

## Contrat sémantique

`data/thematic-index/THEME-RELATIONS-CONTRACT.md` définit :

- `equivalent_to` ;
- `variant_of` ;
- `broader_than` ;
- `component_of` ;
- `related_to`.

Les inverses `narrower_than` et `has_component` sont dérivés et ne doivent pas être stockés en double.

Le statut est distinct du type : `relation_candidate` ou `relation_validated`. Une relation validée devra conserver des preuves réelles des deux thèmes dans `evidenceByThemeId`, des versets attestés, l’enseignement thématique correspondant et une note d’approbation humaine. Même validée, une relation ne fusionne jamais automatiquement des identifiants.

## Frontière entre couches thématiques

`data/thematic-index/themes/` n’est pas une copie un-à-un de la couche de recherche. `scripts/report_theme_layer_coverage.py` mesure :

- 1247 `themeId` de recherche ;
- 38 fiches éditoriales ;
- 24 identifiants présents dans les deux couches ;
- 14 fiches éditoriales seulement ;
- 0 fichier éditorial malformé.

Le test `fidelite-et-infidelite` a montré le risque : cette fiche éditoriale existe, alors que l’analyse canonique du psaume emploie `fidelite`. Le premier graphe exploitable par la recherche doit donc relier uniquement des `themeId` réellement présents dans `theme-search-index.json`. Les fiches éditoriales peuvent fournir contexte et hypothèses, jamais devenir silencieusement des thèmes de recherche.

## Lot pilote de revue

`data/thematic-index/reviews/theme-relations-pilot.json` contient maintenant 14 décisions proposées, toutes avec `semanticClaim: false`, approbation humaine obligatoire et aucun effet sur la recherche publique.

Il démontre les trois issues indispensables : accepter une vraie composition, retyper une candidature lexicale, ou rejeter la lecture `component_of`.

Cas structurants :

- `union` et `soutien-mutuel` → `union-et-soutien-mutuel` : `component_of` ;
- `alliance` → `alliance-de-lumiere` : `broader_than` ;
- `lumiere` ↔ `alliance-de-lumiere` : `related_to` ;
- `nature-vivante` → `nature` : `variant_of` ;
- `discernement` → `discernement-contre-imitation` : `broader_than` ;
- `imitation` ↔ `discernement-contre-imitation` : `related_to`, composante rejetée ;
- `abstraction` ↔ `concret-contre-abstraction` : `related_to`, composante rejetée ;
- `alliance` → `alliance-angelique` : `broader_than` ;
- `anges` ↔ `alliance-angelique` : `related_to` ;
- `nature` ↔ `dialogue-avec-la-nature` : `related_to`.

`scripts/audit_theme_relation_review_pilot.py` vérifie les preuves contre les analyses par livre et verrouille notamment les contre-exemples d’opposition et de relation grammaticale.

## Alias ambigus et équivalence

`scripts/report_theme_alias_collisions.py` retrouve exactement les 5 alias ambigus déclarés par l’index : `alliance de lumiere`, `nutrition subtile`, `service du monde divin`, `temple interieur`, `transmission aux generations`.

Une collision exacte ne prouve pas l’équivalence. `alliance` / `alliance-de-lumiere` est déjà un contre-exemple : la revue conduit à `broader_than`, pas `equivalent_to`.

Aucune relation `equivalent_to` n’est proposée à ce stade. Cette absence est volontaire.

## Risques grammaticaux

`scripts/report_theme_relation_candidate_risks.py` détecte les formulations dont la structure peut être détruite par la simple tokenisation. Il ne décide rien sémantiquement.

Deux niveaux procéduraux existent :

- `review-first` : négation ou opposition ;
- `review-next` : autre mot relationnel potentiellement perdu (`avec`, `entre`, `au`, etc.).

10 thèmes à risque ont été repérés. Le lot `data/thematic-index/reviews/theme-relations-risk-review.json`, complété par le pilote, couvre désormais explicitement leurs 17 paires lexicales.

`scripts/audit_theme_relation_risk_review_coverage.py` exige : 10 cibles, 17 paires examinées, aucune promotion canonique et aucune acceptation `component_of` dans ce sous-ensemble grammaticalement risqué.

Exemples prouvés :

- `concret-contre-abstraction` oppose réellement le concret à l’abstraction ;
- `discernement-contre-imitation` utilise l’imitation comme objet du discernement, non comme composante ;
- `relations-avec-les-regnes` : `relations` est plus général, `regnes` est le partenaire de la relation ;
- `communication-avec-le-divin` : `communication` est plus général ;
- `reciprocite-avec-la-mere` : `mere` est le partenaire de la relation.

La grammaire sert donc à prioriser la revue, jamais à fixer automatiquement le type.

## File de revue fondée sur la disponibilité des preuves

`scripts/report_theme_relation_review_queue.py` classe les paires non encore examinées uniquement selon la disponibilité de preuves dans les analyses existantes : versets, enseignement, directness et importance. Ce classement ne mesure ni similarité sémantique ni probabilité d’être vrai.

Avant le lot général, la file comptait 22 paires déjà examinées et 251 paires encore dans la file, dont 209 `ready-high` et 42 `ready-standard`.

La première version était artificiellement dominée par le thème très fréquent `corps`. La présentation a donc été diversifiée avec `max-one-pair-per-source-theme`. L’audit exige plusieurs sources distinctes et interdit à un thème fréquent de monopoliser le premier lot.

## Lot général diversifié

`data/thematic-index/reviews/theme-relations-general-review.json` ajoute 13 décisions proposées fondées sur des preuves directes fortes. `scripts/report_theme_relation_general_evidence.py` produit un diagnostic compact et reproductible de 19 thèmes ; le run TARGETED n°31 a confirmé 19/19 thèmes présents, sans manque. Un artefact GitHub Actions de quelques kilo-octets remplace désormais la lecture de logs volumineux pour ce diagnostic.

11 relations sont proposées comme vraies composantes :

- `corps`, `ame`, `esprit` → `corps-ame-esprit` ;
- `terre`, `eau`, `air`, `feu` → `terre-eau-air-feu` ;
- `pratique`, `conscience` → `pratique-et-conscience` ;
- `pensee`, `parole` → `maitrise-pensee-parole`.

Deux faux rapprochements lexicaux sont explicitement rejetés :

- `lumiere` ↔ `apparences-et-fausse-lumiere` : `related_to`, pas `component_of` ;
- `dieux` ↔ `idoles-et-faux-dieux` : `related_to`, pas `component_of`.

Les qualificatifs « fausse » et « faux » montrent que le risque ne vient pas seulement des mots-outils : un modificateur lexical peut renverser la relation suggérée par le sous-ensemble de tokens.

Trois candidats sont volontairement laissés hors de ce lot : `maitrise`, `esprit-et-corps`, `eau-et-air`. Leur relation au composite est moins directe et doit être examinée séparément plutôt que forcée.

`scripts/audit_theme_relation_general_review.py` vérifie les 13 décisions et toutes leurs références de preuve contre les analyses canoniques. Le run TARGETED n°33 (`34325349481`) est terminé avec succès sur toutes les étapes, y compris cet audit général et l’audit du stockage validé.

La file de revue inclut désormais ce troisième lot dans les paires déjà examinées ; ces 13 paires ne sont donc plus reproposées comme travail à faire.

## Stockage canonique des relations validées

`data/thematic-index/theme-relations-validated.json` existe comme source éditoriale canonique future. État actuel :

- `generated: false` ;
- `endpointLayer: theme-search-index` ;
- `publicSearchEffect: false` ;
- `relations: []`.

Le stockage reste volontairement vide. Aucune décision des lots de revue n’a été promue automatiquement.

`scripts/audit_validated_theme_relations.py` vérifie notamment : extrémités présentes dans la couche de recherche, `relationStatus: relation_validated`, `semanticClaim: true`, validation `human-approved`, preuves exactes par `themeId`, versets réellement attestés, enseignement cohérent, absence de doublons symétriques inversés et absence de contradictions directionnelles. Il exécute aussi 5 self-tests afin qu’un fichier vide ne produise pas un succès vacu.

## Ce qui n’a volontairement pas été fait

- aucune réanalyse des 1158 psaumes ;
- aucun rebuild massif ;
- aucune fusion de thèmes ;
- aucune modification des analyses canoniques ;
- aucune modification de la recherche publique ;
- aucune modification d’interface ;
- aucune introduction transversale générée par IA ;
- aucune promotion automatique en `relation_validated` ;
- aucune relation `equivalent_to` inventée ;
- aucun classement sémantique automatique à partir de la grammaire ou de la fréquence.

## Prochaine frontière

Le problème technique de génération de candidats et le problème méthodologique des faux positifs lexicaux sont maintenant suffisamment encadrés pour arrêter d’ajouter des heuristiques générales à l’aveugle.

La prochaine étape doit rester éditoriale et bornée : examiner les candidats différés (`maitrise`, `esprit-et-corps`, `eau-et-air`) et un nouveau petit échantillon diversifié de la file, afin de vérifier les limites entre `component_of`, `broader_than`, `variant_of` et `related_to` sur des structures moins évidentes.

Tant qu’aucune décision n’a reçu d’approbation humaine explicite, `theme-relations-validated.json` reste vide et aucune traversée de relations ne doit être activée dans la recherche. Après approbation d’un petit sous-ensemble seulement, l’intégration produit devra rester additive : résultats directs actuels d’un côté, relations validées traversées de l’autre, sans exposer les candidats ni modifier la canonicalisation.