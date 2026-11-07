# BIBLAW — Préparation d'intégration avant publication (mission 5)
**Date :** 7 novembre 2026  
**État :** PR #76 DRAFT, aucune fusion et aucun déploiement.

## Origines des travaux

- **PR #74** : branche de base `fix/faq-source-audit-2026-11-06`, 102 FAQ contrôlées, 406 références de psaumes, correctifs de recherche, tests sur mobile et ordinateur.
- **PR #75** : `docs/FAQ-MISSION-19-20-STAGING.json` et `docs/FAQ-MISSION-19-20-ROUTING.json`. Trois réponses développées, 19 formulations et preuves PDF (110 versets). Cette PR n'a pas été modifiée.
- **PR #76** : branche issue du HEAD de la PR #74, désormais **ciblée directement sur main** pour une seule intégration comprenant les 102 réponses contrôlées, les trois réponses supplémentaires et les preuves éditoriales de la PR #75. Les autres PR n'ont pas été modifiées.

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

Un test supplémentaire vérifie qu'une autre formulation (*Comment vivre autrement ?*) retrouve bien un **article existant**, plutôt qu'une copie. Cette vérification est passée dans le navigateur Chromium.

## Compatibilité des autres travaux

**La PR #72 est actuellement DRAFT et non fusionnable telle quelle** (état GitHub : `mergeable=false`, 371 fichiers modifiés). Ne pas l'intégrer automatiquement.

Chevauchement des fichiers modifiés :
- **PR #72 / PR #74 : 5 fichiers communs**, dont `index.html`, `js/biblaw.js` et des scripts de tests ;
- **PR #72 / PR #76 : 2 fichiers communs**, `index.html` et `scripts/build_pages_site.py` ;
- **PR #74 / PR #75 : aucun fichier commun** dans les changements déclarés par GitHub.

**Conclusion :** un regroupement automatique des PR #72, #74 et #75 pourrait écraser une partie des interfaces ou des correctifs. Conserver les trois PR intactes ; une vérification séparée du périmètre de #72 est nécessaire avant d'éventuellement reprendre ses fonctions utiles. La PR #76 n'exige pas que #72 soit fusionnée pour tester les FAQ 19/20.

## Décision à venir

1. Utiliser la PR #76 (cible main) comme **candidate unique**, contenant les corrections des PR #74 et les nouvelles réponses de la PR #75.
2. Conserver la PR #72 ouverte et séparée ; examiner son catalogue de notes et ses correctifs canoniques dans un autre chantier, sans écraser la version FAQ actuelle.
3. **Fusionner et déployer uniquement après accord explicite du propriétaire.**
4. Après publication, contrôler les 105 questions, les 424 liens, les 19 formulations et les recherches sur le véritable site.

**Ce dossier est une préparation de publication et non une autorisation de publier.**

## Audit de compatibilité approfondi avec la PR #72

**Résultat : la PR #72 ne doit pas être fusionnée globalement avec la version 105 FAQ.**

- **Interface :** l'ancien index.html de #72 utilise searchForm et themeAutocomplete ; il ne possède ni faqToggle, ni faqLibrary, ni faqSearch. Le choisir à la place de l'index de #76 ferait disparaître l'accès aux 105 réponses. La version actuelle possède aussi la rubrique « Notes par sujets ».
- **Publication :** le constructeur Pages de #72 sélectionne l'ancien index des notes note-themes-public-072B.json. Celui de #76 publie note-themes-public-073.json et les deux fichiers de données FAQ 099.
- **Périmètre #72 :** 371 fichiers modifiés, dont 96 fichiers de notes, 59 chemins thématiques, 13 fichiers de prières, quatre JSON de psaumes, et de nombreux tests et workflows. Ces travaux restent conservés dans #72 ; ils ne sont ni détruits ni déclarés obsolètes.
- **Un verset particulier :** le psaume 155 du livre 22, verset 21, est tronqué dans main et dans #76 à « ... de continuer à agir après la ». La PR #72 contient une suite plus complète. Il faut comparer cette réparation au PDF original dans une mission distincte avant de modifier le corpus canonique. Ne pas importer une correction de psaume par une fusion de masse.
- **Chevauchements :** #72 et #74 touchent cinq chemins communs, dont index.html et js/biblaw.js ; #72 et l'ajout propre de #76 touchent deux chemins communs, index.html et scripts/build_pages_site.py. Une fusion automatique de ces branches divergentes serait risquée.
- **Historique Git :** au contrôle, #72 est divergente de main (330 commits d'avance, 154 de retard) et non fusionnable ; #76 est à jour relativement à main (118 commits d'avance, aucun de retard) avec 47 fichiers de différence et mergeable=true après recalcul.

**Choix de sécurité :** PR #76 est maintenant ciblée directement sur main. Après accord de Ludo, elle peut porter les 105 FAQ et leurs tests dans une seule publication. PR #72 demeure un dossier séparé pour notes, lexique et corrections canoniques.

### Conservation des preuves des nouvelles réponses

Les sources originales de la PR #75 ont été recopiées à l'identique dans #76 : inventaire, bilan, trois textes, 19 routes, vérification de 110 versets dans le PDF, scripts d'audit et workflow dédié. La vérification de staging impose une **égalité stricte** entre les trois réponses vérifiées et data/faq-099.json, ainsi qu'entre le routage éditorial et data/faq-099-routing.json. Il est donc impossible de changer silencieusement les textes publics sans déclencher un échec du contrôle.

**Contrôles réussis sur le code du commit 67ce45ed3f93f5fad53004b0efc709cdcbd30454 :** intégrité des FAQ, 187 vérifications PDF précédentes, nouvel audit PDF de 110 versets, Chromium sur téléphone et ordinateur. Aucun déploiement.

**Statut final : DRAFT.** La publication doit être autorisée explicitement.
