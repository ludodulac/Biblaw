# Diagnostic des validations et garde-fous — 2026-09-08

## Pourquoi cette reprise a été faite

Une session précédente a été interrompue après plusieurs heures d'activité apparente. Avant toute nouvelle opération lourde, l'état réel de `main`, les commits déjà poussés et les dernières Actions GitHub ont été vérifiés afin de ne pas recommencer un travail déjà terminé.

## Diagnostic réel

- aucune Action récente sur `main` n'était encore bloquée en cours au moment de la reprise ;
- les validations légères récentes terminaient en quelques dizaines de secondes ;
- le pipeline canonique FULL observé dans GitHub Actions a exécuté **93 étapes en 13,373 s** ;
- aucune de ces étapes n'a dépassé environ 3 secondes lors de cette exécution ;
- le pipeline a conclu `No canonical thematic changes` ;
- les heures observées pendant la session précédente ne correspondaient donc pas à un calcul canonique GitHub de plusieurs heures, mais à l'orchestration de session, aux inspections successives et au risque de répétitions inutiles.

Un défaut réel existait néanmoins dans l'ancien workflow : en cas d'avancement concurrent de `main`, sa logique de publication pouvait rejouer le pipeline FULL dans une boucle de plusieurs tentatives, sans timeout explicite au niveau du job.

## Garde-fous désormais en place

### Workflow canonique

`.github/workflows/validate-thematic-index.yml` :

- `cancel-in-progress: true` pour rendre obsolète un ancien FULL lorsqu'un nouveau changement canonique arrive ;
- `timeout-minutes: 60` au niveau du job ;
- préflight `FAST --area thematic` avant FULL ;
- timeout par sous-étape canonique : `BIBLAW_STAGE_TIMEOUT_SECONDS`, défaut **900 s** ;
- seuil d'alerte de lenteur : `BIBLAW_SLOW_STEP_SECONDS`, défaut **120 s** ;
- publication refusée si le résultat est devenu périmé parce que `main` a avancé ;
- aucune boucle automatique de rejeu FULL en cas de conflit de publication.

### Pipeline FULL

`scripts/run_canonical_thematic_pipeline.py` :

- progression visible `START` / `DONE` ;
- durée de chaque sous-processus ;
- timeout explicite par sous-processus ;
- avertissement GitHub pour une étape anormalement lente ;
- résumé final des étapes les plus coûteuses ;
- les réparations documentaires PDF sont elles aussi exécutées dans des sous-processus bornés.

### Rebuild TARGETED

`scripts/rebuild_thematic_derivatives.py` :

- timeout par étape via `BIBLAW_TARGETED_STAGE_TIMEOUT_SECONDS`, défaut **600 s** ;
- progression et durées visibles ;
- avertissement de lenteur ;
- pas de rejeu des extractions PDF ni des passes sémantiques profondes lorsque seules les dérivées déterministes doivent être reconstruites.

### Entrée proportionnée unique

`scripts/check_biblaw.py` conserve trois niveaux distincts :

- `FAST` : contrôles courts, non destructifs ;
- `TARGETED` : reconstruction déterministe limitée à la zone touchée ;
- `FULL` : pipeline canonique complet puis contrats production/UI.

Chaque commande enfant est maintenant bornée par `BIBLAW_CHECK_STEP_TIMEOUT_SECONDS`, défaut **1800 s**, et sa durée est affichée.

### Pages

`.github/workflows/pages.yml` :

- `timeout-minutes: 10` ;
- `cancel-in-progress: true` ;
- audit statique `scripts/audit_validation_orchestration.py` avant les autres contrôles ;
- cet audit vérifie les timeouts, FAST avant FULL, les signaux de progression/lenteur et l'absence de boucle de rejeu FULL sans exécuter lui-même de calcul lourd.

Le premier jet de cet audit a produit un faux positif car il trouvait le nom du script FULL dans la section `paths:` du workflow avant la vraie commande `run:`. L'assertion a été corrigée pour comparer les commandes d'exécution explicites. Le déploiement Pages suivant a réussi en environ 25 secondes.

## Règle de reprise à conserver

Avant toute validation FULL :

1. vérifier le HEAD réel de `main` et les Actions déjà associées ;
2. ne pas relancer un calcul déjà validé pour ce même état ;
3. exécuter FAST, puis TARGETED si cela suffit ;
4. réserver FULL aux changements qui touchent réellement les couches canoniques amont ;
5. si un run devient périmé parce que `main` avance, l'annuler ou le laisser échouer comme stale — ne pas rejouer automatiquement FULL dans le même job ;
6. si une étape dépasse son seuil habituel, inspecter son log et sa durée avant toute nouvelle tentative.

## Intégrité prière/note déjà couverte

La tâche suivante envisagée lors de la session précédente — vérifier les références prière/note vers les Psaumes canoniques — n'a pas été recréée car elle est déjà couverte par `scripts/audit_corpus_attachments.py` et les audits de références legacy. Le contrat existant contrôle notamment les cibles canoniques, la réciprocité des prières, les références de versets des notes, l'absence de cibles legacy et la fraîcheur du bundle navigateur.

## État thématique de référence observé

La dernière exécution canonique observée conserve :

- **1247 thèmes** ;
- **10409 relations thématiques** ;
- **5 ambiguïtés de libellé normalisé vers plusieurs IDs** ;
- **0 collision technique de répertoire normalisé** ;
- **924 thèmes singleton** ;
- **1050 thèmes avec occurrence <= 2** ;
- **31 cas même ID / plusieurs libellés** ;
- **100 candidats de libellés composites** ;
- **0 relation sans versets d'appui** ;
- **0 relation sans enseignement contextuel**.

Ces nombres sont un instantané de diagnostic. Pour toute décision future, `data/thematic-index/validation-report.json`, `theme-quality-audit.json` et le runtime généré restent les sources de vérité à relire avant de citer des compteurs.
