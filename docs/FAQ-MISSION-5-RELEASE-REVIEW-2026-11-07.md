# BIBLAW — Préparation d'intégration avant publication (mission 5)
**Date :** 7 novembre 2026  
**État :** PR #76 DRAFT, aucune fusion et aucun déploiement.

## Origines des travaux

- **PR #74** : branche de base `fix/faq-source-audit-2026-11-06`, 102 FAQ contrôlées, 406 références de psaumes, correctifs de recherche, tests sur mobile et ordinateur.
- **PR #75** : `docs/FAQ-MISSION-19-20-STAGING.json` et `docs/FAQ-MISSION-19-20-ROUTING.json`. Trois réponses développées, 19 formulations et preuves PDF (110 versets). Cette PR n'a pas été modifiée.
- **PR #76** : branche indépendante créée **à partir du HEAD de la PR #74**. Elle importe uniquement les **textes finalisés** de la PR #75 pour tester leur intégration avec le fonctionnement de la PR #74. La PR #75 reste distincte.

## État de l'aperçu fonctionnel

| Contrat | Résultat |
| --- | --- |
| Réponses précédentes conservées | 102 |
| Nouvelles réponses provenant de la mission 19/20 | 3 |
| **Total de réponses canoniques** | **105** |
| Références antérieures cliquables | 406 |
| Nouvelles références cliquables | 18 |
| **Total des liens de psaumes** | **424** |
| Formulations d'accès/routage | **19** |
| Formulations nouvelles avec leur réponse unique | 3 |
| Formulations renvoyant aux articles existants | 12 |
| Formulations renvoyant à une des nouvelles réponses | 2 |
| Formulations sans source doctrinale explicite | 2 |

Les 19 formulations figurent dans le fichier public `data/faq-099-routing.json`. Elles ne créent **aucun article répété**. Les deux formulations sans source ne sont **pas affichées comme réponses**, mais une recherche exacte de ces questions indique qu'aucune réponse spécifiquement fondée n'est disponible.

Un champ de recherche simple dans la FAQ permet de retrouver les **105 réponses uniques** par leur titre initial ou une formulation alternative ; il fonctionne sans changer le moteur des recherches de psaumes. Le lecteur continue à ouvrir les psaumes avec les bons versets en surbrillance et permet le retour. Les vrais PDF sont exportés depuis les réponses.

## Vérifications réalisées

- `scripts/check_faq_integrity.mjs` : **105 réponses**, **424 liens** et **19 routes** avec contrôle des cibles et absence d'articles inventés pour les deux questions non sourcées.
- `scripts/check_faq_dom.mjs` : ouverture des 105 réponses, simulation des 424 liens, export et impression.
- Les anciens `scripts/smoke_faq_085.mjs` à `scripts/smoke_faq_097_098.mjs` ont été conservés et adaptés à un chargeur comprenant trois réponses supplémentaires, sans modifier les exigences sur les anciennes réponses.
- `scripts/smoke_faq_full_browser.mjs` : navigateur Chromium réel sur les fichiers exacts générés pour Pages, en mobile et ordinateur ; ouverture des 105 réponses, 424 liens visibles et actifs, 18 allers-retours lecteur/FAQ par format, trois vrais PDF par format, index, recherche et synonyme/renvoi. Premier passage **PASS** dans les deux formats : run GitHub Actions `42387064726`.
- La suite de régressions sur les recherches par thème, numéro, occurrences exactes, formes morphologiques et deux mots a également réussi dans ce même run.

Un test supplémentaire a été ajouté pour vérifier explicitement qu'une autre formulation (*Comment vivre autrement ?*) retrouve bien un **article existant**, plutôt qu'une copie. La CI du dernier commit doit encore être vérifiée avant d'affirmer que cette extension est verte.

## Compatibilité des autres travaux

**La PR #72 est actuellement DRAFT et non fusionnable telle quelle** (état GitHub : `mergeable=false`, 371 fichiers modifiés). Ne pas l'intégrer automatiquement.

Chevauchement des fichiers modifiés :
- **PR #72 / PR #74 : 5 fichiers communs**, dont `index.html`, `js/biblaw.js` et des scripts de tests ;
- **PR #72 / PR #76 : 2 fichiers communs**, `index.html` et `scripts/build_pages_site.py` ;
- **PR #74 / PR #75 : aucun fichier commun** dans les changements déclarés par GitHub.

**Conclusion :** un regroupement automatique des PR #72, #74 et #75 pourrait écraser une partie des interfaces ou des correctifs. Conserver les trois PR intactes ; une vérification séparée du périmètre de #72 est nécessaire avant d'éventuellement reprendre ses fonctions utiles. La PR #76 n'exige pas que #72 soit fusionnée pour tester les FAQ 19/20.

## Décision à venir

1. Contrôler la CI du dernier commit de la PR #76.
2. Choisir l'ordre d'intégration : valider d'abord la PR #74, puis la PR #76 qui en dépend ; préserver #75 comme dossier éditorial séparé.
3. Arbitrer les fonctionnalités réellement utiles de la PR #72 et résoudre les conflits manuellement, sans écraser la version actuelle.
4. **Fusionner et déployer uniquement après accord explicite du propriétaire.**
5. Après publication : vérifier les 105 questions, les 424 liens, les 19 formulations et les recherches sur le site public.

**Ce dossier est une préparation de publication et non une autorisation de publier.**
