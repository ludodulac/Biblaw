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

Pour le nouveau diagnostic de relations thématiques, un workflow dédié de branche a été ajouté avec un timeout de 2 minutes et deux commandes Python ciblées seulement. Aucun générateur et aucun FULL n’y sont appelés.

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

Pour `union-pere-nature`, le rapport réel propose :

- `pere` ;
- `union` ;
- `nature`.

Cela signifie uniquement « composante à examiner » et jamais `pere = union-pere-nature`.

### Audit de non-régression

`scripts/audit_theme_relation_candidates.py`

Sentinelles actuelles :

- `union-pere-nature` → `union`, `pere`, `nature` ;
- `alliance-de-lumiere` → `alliance`, `lumiere` ;
- `nature-vivante` → `nature` ;
- `union-et-soutien-mutuel` → `union`, `soutien-mutuel`.

L’audit vérifie également que toutes les relations du lot restent des candidats non sémantiques soumis à validation humaine.

### Validation TARGETED réelle

Workflow : `.github/workflows/audit-theme-relation-candidates.yml`.

- timeout : 2 minutes ;
- aucun générateur ;
- aucun FULL ;
- audit et diagnostic du cas licorne uniquement.

Run 1 : succès.

Run 2, après ajout des statistiques de lot : succès.

Le calcul Python du lot est de l’ordre de quelques dixièmes de seconde ; le temps principal du workflow est le checkout/setup GitHub.

## Mesure du phénomène sur les 186 composites existants

Résultat du run TARGETED :

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

## Contrat sémantique ajouté

`data/thematic-index/THEME-RELATIONS-CONTRACT.md`

Le contrat sépare désormais :

- nature de relation : `equivalent_to`, `variant_of`, `broader_than`, `component_of`, `related_to` ;
- statut : `relation_candidate` ou `relation_validated`.

Les inverses sont dérivés plutôt que stockés en double :

- `broader_than` → vue inverse `narrower_than` ;
- `component_of` → vue inverse `has_component`.

Une relation validée devra retenir les preuves des deux côtés, les versets/enseignements pertinents et une justification du type de relation retenu. Une validation de relation ne déclenche jamais automatiquement une fusion d’identifiants.

## Frontière découverte entre couches thématiques

Un test volontaire sur `fidelite-et-infidelite` a révélé une distinction architecturale à préserver : cette fiche existe dans `data/thematic-index/themes/fidelite-et-infidelite.json`, mais cet identifiant n’existe pas dans `theme-search-index.json`.

L’analyse par psaume correspondante (`book-17-psalm-105`) emploie en revanche le thème `fidelite`, avec un enseignement directement ancré dans les versets. La fiche `fidelite-et-infidelite` est donc une consolidation éditoriale de recherche et ne doit pas être traitée automatiquement comme une entité de recherche canonique.

Un nouveau rapport FAST, `scripts/report_theme_layer_coverage.py`, mesure ce recouvrement sans modifier les données. Résultat du run TARGETED n°4 :

- thèmes de l’index de recherche : 1247 ;
- fiches éditoriales dans `data/thematic-index/themes/` : 38 ;
- identifiants présents dans les deux couches : 24 ;
- fiches éditoriales sans identifiant homonyme dans l’index de recherche : 14 ;
- fichier éditorial malformé : 0.

Les 14 identifiants éditoriaux seuls sont actuellement : `fidelite-et-infidelite`, `hierarchies`, `intelligence-superieure`, `libre-arbitre`, `maitres-et-sages`, `mensonge-et-illusion`, `nature-et-mere`, `non-savoir`, `perception-et-sens`, `pierres`, `plantes`, `purete-et-verite`, `solidarite-et-soutien-mutuel`, `sommeil-et-reve`.

Conséquence : toute future relation persistée devra déclarer explicitement à quelle couche appartient chaque extrémité. Pour le premier graphe exploitable par la recherche, les extrémités doivent rester des `themeId` réellement présents dans l’index issu des analyses par psaume. Les fiches éditoriales peuvent fournir du contexte et des hypothèses, mais ne doivent pas être injectées silencieusement comme thèmes de recherche.

Le probe qui a exposé cette frontière a produit un échec ciblé attendu (`Unknown theme id: fidelite-et-infidelite`) sans affecter l’audit principal. Le workflow a ensuite été corrigé pour mesurer la couverture des couches explicitement ; le run n°4 est terminé avec succès.

## Ce qui n’a volontairement pas été fait

- aucune réanalyse des 1158 psaumes ;
- aucun rebuild massif ;
- aucune fusion de thèmes ;
- aucune modification des analyses canoniques ;
- aucune modification de la recherche publique ;
- aucune modification de l’interface ;
- aucune introduction transversale générée par IA ;
- aucune promotion automatique de candidat en relation validée.

## Prochaine frontière

Avant toute utilisation dans la recherche, il faut constituer un petit lot de relations examinées manuellement à partir de thèmes très différents et vérifier la capacité du modèle à distinguer :

- équivalence réelle ;
- variante ;
- relation plus général / plus spécifique ;
- composante ;
- thème lié mais distinct ;
- candidat rejeté.

Ce lot devra utiliser les contextes de psaumes, versets justificatifs et enseignements déjà présents. Les extrémités du premier lot devront être des `themeId` présents dans l’index de recherche ; les fiches éditoriales non recouvrantes serviront de contexte de recherche seulement.

Ce n’est qu’après cette preuve que la représentation persistée des relations validées et son exploitation par la recherche devront être implémentées.
