# Finalisation sémantique des livres 23 à 25 — 2026-09-06

## Résultat

Trois livres consécutifs sont maintenant fermés par un garde-barrière sémantique strict :

- Livre 23 — Raphaël, « La pensée créatrice » : 26/26 analyses `deep-content-grounded`.
- Livre 24 — Ouriel, « L’androgynie » : 26/26 analyses `deep-content-grounded`.
- Livre 25 — Michaël, « Les clés de la maîtrise » : 26/26 analyses `deep-content-grounded`.

Chaque relation thématique résiduelle issue de la couche prototype a été remplacée par une relation fondée sur les versets exacts du corpus PDF-derived. Les relations déjà éditorialement approfondies dans le livre 23 ont été conservées. Les références sont contrôlées contre le corpus avant finalisation.

## Psaume 128 du livre 23

Le contrôle documentaire a montré que la numérotation commençant au verset 49 n’est pas à combler artificiellement : le fichier canonique porte explicitement `sourceNumberingPreserved=true` et une base de titre auditée avec continuation de la numérotation source. La méthode du livre enregistre désormais cette particularité et aucun verset 1–48 n’a été inventé.

## Pipeline

Nouveaux éléments reproductibles :

- `scripts/deepen_books23_25_semantic_evidence.py`
- `scripts/finalize_books23_25_semantic.py`
- `.github/workflows/validate-deep-books23-25.yml`

Un premier run a correctement révélé des enseignements prototypes résiduels dans les analyses déjà approfondies 129–131 du livre 23. Le script a été corrigé pour préserver les relations éditoriales tout en grounded les relations résiduelles du même psaume. Le run suivant, `34028506863`, est entièrement vert : finaliseurs 23–25, intégrité documentaire, normalisation, contextes PDF-only, validation globale, répertoire thématique et commit généré.

## État global après fermeture

- 44 livres
- 1 156 analyses de psaumes
- 10 388 relations thématiques
- 0 erreur
- 0 avertissement

Prochaine reprise recommandée : livre 26 puis bloc suivant, sans rouvrir 23–25 sauf nouvelle anomalie documentaire ou sémantique vérifiable.
