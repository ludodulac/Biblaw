# Finalisation sémantique profonde — livres 18 à 20

Date : 2026-09-06

## Règles conservées

- Source éditoriale et sémantique : exclusivement le corpus et les source packs dérivés du PDF de référence.
- Aucun contenu externe utilisé pour rédiger les relations thématiques.
- Les passes profondes sont additives/conservatrices : elles remplacent ou complètent les axes centraux audités et préservent les relations secondaires utiles.
- Toute finalisation vérifie le statut `deep-content-grounded`, l’existence des enseignements, les références de versets contre le corpus courant et l’absence de formulation prototype résiduelle.

## Livre 18 — Gabriel

Le livre 18 est finalisé à 27/27 analyses `deep-content-grounded`.

Les passes profondes couvrent l’ensemble des psaumes 111–137. Les analyses déjà éditorialement précises ont été conservées après contrôle strict plutôt que réécrites artificiellement. La synthèse de livre est produite uniquement après le garde-barrière 27/27.

## Livre 19 — Raphaël

Le livre 19 est finalisé à 26/26 analyses `deep-content-grounded`, psaumes 102–127.

Les passes successives ont approfondi notamment : pensée vivante, respiration et air, communication, affinités et influences, mémoire, Tradition, âme, Alliance, fidélité, préparation, achèvement, responsabilité et continuité de conscience.

Un défaut de pipeline a été découvert lors de la première finalisation : des relations secondaires anciennes conservaient une phrase prototype. Le problème venait de l'interaction entre le nettoyeur résiduel et le finaliseur, non des analyses profondes centrales. La règle générale a été corrigée afin que les enseignements extractifs ancrés dans les versets soient explicitement distingués des prototypes. Aucun thème n'a été supprimé pour faire passer la validation.

## Livre 20 — Ouriel

Le livre 20 est finalisé à 26/26 analyses `deep-content-grounded`, psaumes 104–129.

Six passes profondes couvrent maintenant tout le livre :

- 104–107 : unification pensée/sentiment/volonté, deux terres, lois, conscience, vérité et réalisation ;
- 108–111 : terre intérieure, œuvre quotidienne, terre promise, mémoire collective, éducation et deux natures ;
- 112–115 : communauté d’âmes, Bien commun, dettes et associations, structure de la réussite, connaissance de soi par les actes ;
- 116–119 : argent et échange, porte de Lumière, souplesse, écologie et dignité des règnes ;
- 120–123 : Mère comme médiation, corps comme livre, discernement du faux luxe, offrande et examen de passage ;
- 124–129 : pierre et stabilité, écologie intérieure, impersonnalité et changement de point de vue, parole vraie et silence, mémoires ancestrales, réécriture du monde par l’acte et l’organisation collective.

Le finaliseur `scripts/finalize_book20_semantic.py` exige 26/26 analyses profondes, contrôle chaque référence de verset et produit la synthèse de livre seulement si tous les contrôles passent.

## Pipeline reproductible

Le workflow `.github/workflows/validate-thematic-index.yml` exécute maintenant toutes les passes profondes des livres 18, 19 et 20, puis :

1. ancrage des relations secondaires résiduelles ;
2. finalisation stricte de Gabriel 18 ;
3. finalisation stricte de Raphaël 19 ;
4. finalisation stricte d’Ouriel 20 ;
5. génération des autres livres ;
6. gate documentaire ;
7. normalisation ;
8. construction des contextes ;
9. validation thématique globale ;
10. reconstruction du répertoire thématique ;
11. commit des sorties générées.

Le run de validation complet `34022508913` est passé intégralement, y compris les trois finaliseurs et le validateur global.

## État validé

Rapport `data/thematic-index/validation-report.json` après le run complet :

- statut : `passed` ;
- 44 livres ;
- 1 156 analyses de psaumes ;
- 10 014 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

Les livres 18, 19 et 20 peuvent donc être considérés comme terminés pour cette passe sémantique profonde et reproductible.

## Suite logique

La prochaine étape ne doit pas rouvrir 18–20 sans anomalie nouvelle. Il faut reprendre la feuille de route de passation au prochain bloc non encore audité en profondeur, en conservant les mêmes règles PDF-only et les mêmes garde-barrières de validation.
