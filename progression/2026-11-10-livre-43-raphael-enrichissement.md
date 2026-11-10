# BIBLAW — Livre 43 « La guérison par les vertus » (Raphaël)

## Enrichissement thématique du 10 novembre 2026

- **26 psaumes** du livre 43, numérotés **258 à 283**.
- **1 023 versets** examinés dans le corpus JSON canonique extrait du PDF.
- **312 associations historiques** protégées et restaurables sans modification.
- **182 nouvelles associations thématiques** (sept par psaume) avec citation littérale intégrale et numéro de verset pour chaque relation.
- **494 associations pour le livre 43** ; **21 419 associations sur les 44 livres** après reconstruction canonique.

### Axes éditoriaux

- Responsabilité du parent, conscience de soi et de sa destinée, engagements et fidélité.
- Communication, écoute, partage, solidarité et organisation collective.
- Respect de soi et des autres, acceptation des différences, souplesse et humilité.
- Transmission, éducation, tradition vivante, exemplarité et cohérence pensée–parole–acte.
- Discernement, neutralité, regard objectif, intériorité et sanctuaire du cœur.
- Pensée, choix et orientation des actes, dépassement des illusions.
- Enseignements doctrinaux sur la guérison, l'équilibre, les vertus et les effets supposés des influences invisibles sur la santé, ainsi que sur l'argent et la richesse.

### Conservation et validation

- Textes sources laissés intacts : `data/corpus/books/book-43/`.
- Archive historique : `data/thematic-index/audits/book43-original-relations.json`.
- Plan éditorial : `data/thematic-index/audits/book43-curation-plan.json`.
- Trois lots de relations : `data/thematic-index/audits/book43-enrichment-relations-part{1,2,3}.json`.
- Application idempotente : `scripts/apply_book43_enrichment.py`.
- Audit permanent, aussi exécuté par GitHub Pages : `scripts/audit_book43_full_theme_coverage.py`.
- Reconstruction canonique avec audits de non-régression des livres 41, 42 et 43 : [GitHub Actions #42811371202](https://github.com/ludodulac/Biblaw/actions/runs/42811371202), résultat **success**.
- Validation de l'index `data/thematic-index/validation-report.json` : `passed`, **44 livres**, **1 158 psaumes**, **21 419 relations**, **0 erreur**, **0 avertissement**.
- PR [#124](https://github.com/ludodulac/Biblaw/pull/124) fusionnée, déclencheur CI temporaire supprimé avant fusion.

### Limites documentaires

Les citations des versets ont été vérifiées dans les fichiers JSON extraits du PDF, **sans nouvelle relecture intégrale indépendante** du PDF original. Ces rapprochements sont des propositions éditoriales de repérage thématique, sans prétendre épuiser toutes les interprétations. Les affirmations relatives aux mondes invisibles, aux causes des maladies, à la guérison, à la santé et aux forces de l'argent représentent les positions doctrinales du texte : **elles ne sont ni des preuves scientifiques, ni des conseils médicaux ou économiques**.
