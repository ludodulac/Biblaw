# 2026-09-07 — Couche de recherche thématique et connexions

## Cadre méthodologique

La couche de recherche ne cherche pas à fixer un sens unique des Psaumes. L’indexation reste descriptive, liée aux passages du corpus et compatible avec plusieurs niveaux de lecture. Les rapprochements calculés servent à retrouver et parcourir les textes ; ils ne constituent ni des équivalences doctrinales, ni des affirmations causales, ni une interprétation exhaustive.

Le corpus PDF et les paquets de lecture qui en dérivent restent la seule source de contenu éditorial, doctrinal, symbolique et thématique.

## État canonique de l’index

Validation principale :

- 44 livres ;
- 1 158 analyses de Psaumes ;
- 10 406 relations thème ↔ Psaume ;
- 0 erreur ;
- 0 avertissement.

Le pipeline canonique `scripts/run_canonical_thematic_pipeline.py` reconstruit désormais l’ensemble des livres 1 à 44, réapplique les réparations documentaires auditées, rejoue les passes profondes puis génère et valide les couches destinées à la recherche.

## Audit de qualité de recherche

Le script `scripts/audit_thematic_search_quality.py` produit `data/thematic-index/theme-quality-audit.json` sans modifier les analyses éditoriales.

État observé :

- 1 250 thèmes ;
- 930 thèmes présents dans un seul Psaume ;
- 1 055 thèmes présents dans au plus deux Psaumes ;
- 31 `themeId` associés à plusieurs libellés observés ;
- 9 libellés normalisés pouvant désigner plusieurs `themeId` ;
- 4 collisions de libellés normalisés dans le répertoire courant ;
- 187 libellés composites signalés uniquement comme candidats de revue ;
- aucune relation sans numéro de verset ;
- aucune relation sans formulation d’indexation (`teaching`).

Les thèmes rares ou composites ne sont pas traités comme des erreurs et ne sont pas fusionnés automatiquement.

## Libellés canoniques

`build_thematic_directory.py` choisit désormais le libellé d’affichage d’un `themeId` de façon déterministe : libellé observé le plus fréquent, puis règles stables de départage. Les variantes restent conservées dans `labelVariants`.

Cette normalisation concerne uniquement l’affichage et la stabilité technique ; elle ne réécrit pas les relations éditoriales sources.

## Index d’alias

`scripts/build_thematic_search_index.py` génère `data/thematic-index/theme-search-index.json`.

État validé :

- 1 250 thèmes ;
- 1 342 alias normalisés ;
- 9 alias ambigus ;
- `semanticMerging: false`.

Les accents, apostrophes, ponctuations et variantes observées sont utilisables pour retrouver les thèmes. Quand un alias correspond à plusieurs identifiants, tous sont conservés : aucune fusion sémantique n’est déduite de la proximité lexicale.

Le script `scripts/validate_thematic_search_index.py` vérifie que chaque thème canonique reste retrouvable, qu’aucun identifiant fantôme n’est introduit et que les ambiguïtés restent explicitement représentées.

## Graphe de connexions

`scripts/build_thematic_connections.py` génère `data/thematic-index/theme-connections.json`.

La relation garantie est exclusivement : **cooccurrence dans un même Psaume indexé**.

État validé :

- 1 250 thèmes ;
- 13 121 arêtes non orientées de cooccurrence ;
- jusqu’à 30 connexions les mieux classées exposées par thème ;
- chaque connexion conserve les Psaumes partagés qui la justifient ;
- `semanticClaim: false`.

Le score utilise uniquement les niveaux d’importance déjà présents dans l’index (`central`, `important`, `related`) afin de classer les connexions pour la navigation. Une arête ne signifie pas synonymie, causalité, identité doctrinale ou interprétation privilégiée.

Le script `scripts/validate_thematic_connections.py` contrôle les identifiants, l’absence d’auto-liens et de voisins inconnus, les scores positifs et la stabilité du classement.

## Contrat pour le site

`data/thematic-index/SEARCH-CONTRACT.md` formalise l’usage attendu :

- toujours permettre de revenir aux Psaumes et versets justificatifs ;
- utiliser les alias pour le rappel de recherche sans fusion automatique ;
- proposer les connexions comme navigation par cooccurrence ;
- conserver les différences entre Archanges, livres et thèmes ;
- ne pas présenter le classement comme une hiérarchie de vérité ;
- ne pas transformer les synthèses d’indexation en sens unique des textes ;
- ne pas utiliser de sources externes pour compléter le contenu doctrinal ou symbolique.

## Robustesse du workflow

Le workflow canonique a été rendu résistant aux courses de publication entre exécutions concurrentes. Si `main` avance pendant un calcul, le job se recale sur le dernier `main` et régénère les sorties déterministes avant de publier, au lieu de rebaser un gros commit de fichiers générés.

Run de validation de cette stratégie : `34073397124`, succès complet.

## Suite logique

La base permet maintenant de travailler sur l’exploitation produit de la recherche : résolution de requêtes, classement des Psaumes, filtres par Archange/livre, affichage des preuves et navigation vers les thèmes cooccurrents. Les éventuelles consolidations éditoriales entre thèmes proches doivent rester corpus-grounded et ne seront pas automatisées sur la seule ressemblance des mots.
