# BIBLAW — Audit des réponses spirituelles, lot 01 (6 novembre 2026)

## Portée et règle
Contrôle de **10 réponses** dans les fichiers `data/faq-096.json` (questions 9 à 14) et `data/faq-098.json` (questions 1 à 4). Chaque citation mentionnée a été rapprochée du passage correspondant du **corpus canonique structuré** dans `data/corpus/books/`. Il ne s'agit **pas** d'une relecture visuelle indépendante des pages du PDF source ni d'une validation éditoriale humaine.

Règle propriétaire : restituer les enseignements de la Bible essénienne, avec attribution explicite aux archanges et références aux psaumes ; aucun commentaire scientifique extérieur, aucun exercice ajouté par le rédacteur, aucune conclusion attribuée à un archange lorsqu'elle n'est pas justifiée par les versets.

## Résultats, lot de 10
| ID | Thème | Correction |
| --- | --- | --- |
| faq-harmonie-conscience-9 | Corps et cerveau | Synthèse finale recentrée sur les trois psaumes cités ; retrait de la déduction explicite sur le cerveau. |
| faq-harmonie-conscience-10 | Cerveau et mental | Ouverture et conclusion recentrées sur les notions effectivement exposées (intellect, pensée, intelligence). La limite des passages cités concernant le cerveau est explicitée. |
| faq-harmonie-conscience-11 | Mental et conscience | Pas de modification ; références relues dans le corpus. |
| faq-harmonie-conscience-12 | Âme | Pas de modification ; références relues dans le corpus. |
| faq-harmonie-conscience-13 | Conscience et cerveau | Ouverture et conclusion recentrées sur les affirmations explicites des psaumes, sans théorie sur l'origine cérébrale de la conscience. |
| faq-harmonie-conscience-14 | Identité véritable | Pas de modification ; références relues dans le corpus. |
| faq-pratique-spirituelle-1 | Vie spirituelle quotidienne | Conclusion resserrée sur les thèmes réellement cités. |
| faq-pratique-spirituelle-2 | Méditer | Remplacement du protocole pratique inventé par des indications effectivement enseignées par Ouriel 82 et Raphaël 18. |
| faq-pratique-spirituelle-3 | Attention | Remplacement du protocole d'observation inventé par le contenu de Michaël 160, versets 15-16. |
| faq-pratique-spirituelle-4 | Concentration | Remplacement du protocole libre par l'enseignement de Michaël 189, versets 15-17. |

## Traçabilité des sources principales
- Corps et identité : `book-40/psalm-256`, `book-21/psalm-155`, `book-39/psalm-249`, `book-44/psalm-277`, `book-30/psalm-191`, `book-28/psalm-156`.
- Pensée, intellect, conscience : `book-19/psalm-102`, `book-18/psalm-119`, `book-25/psalm-181`, `book-20/psalm-106`, `book-28/psalm-169`, `book-07/psalm-026`, `book-06/psalm-033`, `book-37/psalm-254`.
- Pratiques : `book-32/psalm-182`, `book-04/psalm-014`, `book-21/psalm-160`, `book-03/psalm-018`, `book-16/psalm-082`, `book-07/psalm-045`, `book-24/psalm-152`, `book-40/psalm-253`, `book-25/psalm-189`.

Tous ces chemins sont sous `data/corpus/books/`.

## Contrôles effectués et limites
- JSON reparsé ; nombre de questions inchangé (14 et 13).
- Identifiants, titres, ordre et carte `verifiedPsalms` inchangés.
- Modifications textuelles limitées à neuf paragraphes de sept réponses.
- La présence d'une référence dans un fichier ne constitue **pas** une authentification éditoriale humaine de chaque affirmation.
- À poursuivre : audit des réponses 5 à 13 de `data/faq-098.json` (plusieurs paragraphes prescriptifs commençant par « Concrètement ») puis les autres fichiers FAQ, par lots de 10 ; vérifier également les extraits du PDF originel pour les passages litigieux.
- La branche d'audit n'est **pas** publiée. Préserver `main` et la PR #72 en DRAFT.

## Lot 02 — pratiques quotidiennes (6 novembre 2026)

- **Périmètre :** neuf réponses restantes du fichier `data/faq-098.json` (questions 5 à 13).
- **Examen :** chaque enseignement principal et les propositions pratiques ont été confrontés aux psaumes canoniques de `data/corpus/books/` cités dans ces réponses : Gabriel 156, 165, 28, 197, 67, 209 ; Michaël 208, 170, 171, 189, 267, 145, 165, 140 ; Raphaël 45, 218, 134 ; Ouriel 152, 214, 182.
- **Modifications :** 17 paragraphes corrigés dans 9 réponses. Suppression de protocoles de méditation, d'attention, de gratitude, d'habitudes et de conseils de comportement qui étaient des propositions rédactionnelles non attribuables aux versets ; remplacement par des prescriptions présentes dans les psaumes, avec références précises. Rectification des exemples de repas, marche et parole.
- **Invariants :** 13 réponses conservées dans ce fichier, sans modification des identifiants, titres, ordre et correspondances `verifiedPsalms`. Aucun corpus, index, script de chargement ou code d'interface modifié.
- **Contrôle :** JSON valide et relecture des neuf réponses corrigées dans la structure chargée ; validation de la publication réelle et relecture indépendante du PDF non réalisées. 


## Lot 03 — réalité spirituelle (8 réponses, fichier 097)

Les 8 réponses ont été relues avec leurs passages du corpus : Raphaël 88, 15, 268, 222, 76 ; Gabriel 244, 33, 191, 213, 70 ; Michaël 94, 279, 254 ; Ouriel 182, 277, 156, 186, 106 et 152. Les affirmations principales sont appuyées par les passages cités. **Aucune modification textuelle** nécessaire pour ce lot ; ce n'est pas une certification éditoriale indépendante des PDF.

## Lot 04 — harmonie et conscience, questions 1 à 8 (8 réponses, fichier 096)

Les 8 réponses ont été relues avec les psaumes de référence : Gabriel 244, 165, 156, 144, 291 ; Ouriel 131, 200, 214 ; Raphaël 171, 190, 211, 26 ; Michaël 170, 236, 15 ; Ouriel 106 et 156. Les exemples de Gabriel 244:30-40 dans la question 7 ont été vérifiés en particulier. **Aucune modification textuelle** nécessaire dans ce lot. Contrôle effectué contre les textes structurés du dépôt, non contre le fac-similé PDF.


## Lots 05 à 08 — approfondissement des réponses (28 réponses)

- **Lot 05 — FAQ 095, 7 réponses** : connaissance de soi, habitudes, désirs, réactions, caractère, volonté, vie intérieure. Les passages de Raphaël 102, 134, 190 ; Gabriel 84, 165, 209 ; Ouriel 132, 152, 154, 169, 239, 252 ; Michaël 171, 189 ont été comparés aux affirmations. Aucune modification textuelle nécessaire.
- **Lot 06 — FAQ 094, 6 réponses** : bonheur et circonstances, intérieur et richesse. Comparaison avec Gabriel 29, 174, 197 ; Ouriel 15, 59, 73 ; Michaël 102 ; Raphaël 68, 211. Le passage Ouriel 73:12 confirme expressément l'exemple du repas en famille/avec des amis ; conservé. Aucune modification.
- **Lot 07 — FAQ 093, 5 réponses** : sens de la vie et mission personnelle. Comparaison avec Ouriel 16, 155, 237 ; Raphaël 177 ; Michaël 205, 267. Aucune modification.
- **Lot 08 — FAQ 092, 10 réponses** : religions, science, conscience. Comparaison avec Gabriel 178, 216 ; Michaël 159, 191, 211, 274, 280, 285, 289, 292 ; Raphaël 194, 269, 282, 26, 102 ; Ouriel 146. Les réponses traitent de la « science » *telle que citée et comprise dans les psaumes* ; aucune assertion externe de validation ou réfutation scientifique n'y a été ajoutée. Aucune modification.

**À ce stade : 63 réponses examinées sur 102.** Les contrôles décrits restent documentaires sur le corpus structuré, non des validations éditoriales humaines.

