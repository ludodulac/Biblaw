# Finalisation sémantique des livres 23 à 25 — 2026-09-06

## Résultat

Trois livres consécutifs sont fermés par un garde-barrière sémantique strict :

- Livre 23 — Raphaël, « La pensée créatrice » : 26/26 analyses `deep-content-grounded`.
- Livre 24 — Ouriel, « L’androgynie » : 26/26 analyses `deep-content-grounded`.
- Livre 25 — Michaël, « Les clés de la maîtrise » : 26/26 analyses `deep-content-grounded`.

Chaque relation thématique résiduelle issue de la couche prototype a été remplacée par une relation fondée sur les versets exacts du corpus PDF-derived. Les relations déjà éditorialement approfondies dans le livre 23 ont été conservées. Les références sont contrôlées contre le corpus avant finalisation.

## Psaume 128 du livre 23

Le contrôle documentaire approfondi a établi que le psaume 128, « Ne sois pas un rêveur », doit être représenté canoniquement en 34 versets numérotés 1 à 34. Le PDF imprime les repères 49 à 82 ; le pipeline applique donc un décalage audité de 48, sans inventer ni supprimer de contenu. La question est intégrée à la fin du verset canonique 22 et la réponse commence au verset 23. Le script `scripts/repair_book23_psalm128_numbering.py` impose et vérifie cette transformation après reconstruction depuis le PDF.

## Pipeline

Éléments reproductibles :

- `scripts/repair_known_pdf_psalm_anomalies.py`
- `scripts/repair_book23_psalm128_numbering.py`
- `scripts/deepen_books23_25_semantic_evidence.py`
- `scripts/finalize_books23_25_semantic.py`
- `.github/workflows/validate-deep-books23-25.yml`

Le run historique `34028506863` avait fermé la passe sémantique initiale. La correction documentaire du psaume 128 a ensuite été validée par le run `34035664802`. Enfin, le workflow canonique global `34052571366` a reconstruit le psaume depuis le PDF, appliqué la renumérotation 49–82 vers 1–34, rejoué la passe profonde 23–25 et validé l’ensemble sans erreur ni avertissement.

## État global consolidé

Après restauration du psaume 182 du livre 32 et consolidation de tous les blocs ultérieurs :

- 44 livres
- 1 157 analyses de psaumes
- 10 400 relations thématiques
- 0 erreur
- 0 avertissement

Le livre 23 ne doit plus être décrit comme conservant la numérotation source 49–82 : cette numérotation est désormais explicitement mappée vers la numérotation canonique 1–34.
