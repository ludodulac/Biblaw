# Finalisation sémantique des livres 26 à 44 — 2026-09-06

## Résultat

Les livres 26 à 44 sont désormais fermés par des passes `deep-content-grounded` reproductibles, fondées exclusivement sur le corpus dérivé du PDF. Les synthèses de livre ne sont produites qu’après contrôle de toutes les analyses du livre.

### Livres 26 à 28

- Livre 26 — Gabriel, « L’énergie créatrice » : 26/26 deep.
- Livre 27 — Raphaël, « Le Serpent de la Sagesse » : 26/26 deep.
- Livre 28 — Ouriel, « Le vrai corps du Christ » : 26/26 deep.
- Run de fermeture : `34039541390`.

### Livres 29 à 31

- Livre 29 — Michaël, « La religion du 21ème siècle » : 27/27 deep.
- Livre 30 — Gabriel, « Développer la vision juste » : 26/26 deep.
- Livre 31 — Raphaël, « La nouvelle Pâque » : 26/26 deep.
- Run de fermeture : `34039973400`.

### Livres 32 à 34

- Livre 32 — Ouriel, « La Nouvelle Alliance » : 26/26 deep, psaumes 182–207.
- Livre 33 — Michaël, « Les secrets du Feu » : 26/26 deep.
- Livre 34 — Gabriel, « L’envoûtement et le désenvoûtement » : 28/28 deep.

Le psaume 182 du livre 32 a été restauré depuis le PDF par `scripts/repair_book32_psalm182.py`. La reconstruction retrouve les repères source 28–50 sur les pages PDF 3109, 3113, 3114 et 3115, avec deux notes. Le finaliseur attend désormais explicitement 182–207. La réparation est rejouée dans les workflows qui reconstruisent ce segment afin d’éviter toute régression.

### Livres 35 à 37

- Livre 35 — Raphaël, « Le chemin du bonheur » : 26/26 deep.
- Livre 36 — Ouriel, « Être un socle pour le monde divin » : 26/26 deep.
- Livre 37 — Michaël, « La maîtrise du serpent » : 26/26 deep.

Frontières PDF auditées et réparées :

- livre 35, psaume 215 : repères source 26–46 ;
- livre 36, psaume 217 : repères source 16–36.

La mention antérieure d’une anomalie au psaume 196 du livre 35 était incorrecte : le cas réel et audité est le psaume 215.

### Livres 38 à 40

- Livre 38 — Gabriel, « Les 22 étapes de l’Initiation » : 26/26 deep.
- Livre 39 — Raphaël, « Les vertus du coeur » : 26/26 deep.
- Livre 40 — Ouriel, « L’Ange de la conscience » : 26/26 deep.
- Run de fermeture : `34052258817`.

Le psaume 260 du livre 38 conserve sa numérotation source auditée 23–54.

### Livres 41 à 43

- Livre 41 — Michaël, « La responsabilité d’un parent » : 26/26 deep.
- Livre 42 — Gabriel, « L’état ultime de la paix » : 26/26 deep.
- Livre 43 — Raphaël, « La guérison par les vertus » : 26/26 deep.
- Run de fermeture : `34052354924`.

Le rapport documentaire 41–44 valide ces trois livres sans psaume manquant ni trou de versets.

### Livre 44

- Livre 44 — Ouriel, « L’énergie de l’argent » : 26/26 deep.
- Run de fermeture : `34052427861`.

Le psaume final 285 est limité aux versets 1–16 ; l’annexe qui suit est détachée par la réparation auditée et ne doit pas être indexée comme versets du psaume.

## Stabilisation du pipeline canonique

Le workflow global `.github/workflows/validate-thematic-index.yml` a été corrigé afin qu’une reconstruction générique ne puisse plus effacer les passes profondes déjà validées. Il :

1. installe l’outil d’extraction PDF ;
2. rejoue les réparations documentaires auditées ;
3. reconstruit les lots canoniques ;
4. rejoue les passes et finaliseurs profonds de tous les livres 23 à 44 ;
5. synchronise l’intégrité documentaire ;
6. normalise les métadonnées ;
7. reconstruit les contextes PDF-only et le répertoire thématique ;
8. exécute la validation globale avant commit.

Le run canonique complet `34052571366` a passé toutes les étapes. Il a notamment confirmé :

- livre 23 / psaume 128 : source 49–82 → canonique 1–34, question entre 22 et 23 ;
- livre 26 / psaume 186 : source 23–50 ;
- livre 32 / psaume 182 : restauré depuis le PDF ;
- livre 35 / psaume 215 : source 26–46 ;
- livre 36 / psaume 217 : source 16–36 ;
- livre 38 / psaume 260 : source 23–54 ;
- livre 44 / psaume 285 : annexe détachée après le verset 16.

Commit généré final du run canonique : `1861a57` (`Preserve audited corpus and deep thematic index`).

## État global consolidé

Le rapport `data/thematic-index/validation-report.json` indique :

- 44 livres ;
- 1 157 analyses de psaumes ;
- 10 400 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

Le répertoire thématique reconstruit contient 1 250 thèmes.

À ce stade, la chaîne 23–44 est à la fois sémantiquement approfondie et protégée contre les régressions déterministes du pipeline de reconstruction.
