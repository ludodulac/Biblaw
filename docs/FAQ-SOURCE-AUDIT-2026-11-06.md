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


## Lot 09 — questions fondamentales, FAQ 085 (25 réponses)

- **Périmètre** : `data/faq-public-085.json`, ses 25 questions, et les **56 psaumes distincts** cités dans leurs objets `references`, lus dans `data/corpus/books/`.
- **Contrôle** : chacun des versets référencés a été retrouvé dans son fichier canonique structuré et rapproché des affirmations correspondantes.
- **Corrections : 3 réponses**, sans modifier leurs identifiants, titres, ordre ou références :
  1. `faq-dieu-2` (« Existe-t-il des preuves de l'existence de Dieu ? ») : retrait du commentaire sur les « preuves scientifiques » ; retour aux lois et au discernement enseignés dans les psaumes.
  2. `faq-mort-5` (« La réincarnation est-elle possible ? ») : retrait de la réserve scientifique extérieure ; conservation de la distinction entre réincarnation et immortalité.
  3. `faq-nature-dieu-4` (« Dieu est-il une énergie ? ») : retrait de la comparaison avec l'électricité et les forces étudiées par la science ; remplacement par Ouriel 171.
- **Aucune modification** des 22 autres réponses de ce fichier.

## Lot 10 — présence divine et signes, FAQ 090 (5 réponses)

- **Périmètre** : `data/faq-090-1.json` à `data/faq-090-5.json` et `data/faq-090-books.json`.
- Les références à Michaël 5 et 94, Raphaël 72, 104, 50, 177, 105, 163, 272, 252, Gabriel 279 et 205, Ouriel 274, 74 et 192 ont été relues dans le corpus structuré.
- **Aucune modification** après examen : les cinq réponses restituent les passages cités. Les exemples concernant les signes et les animaux sont cohérents avec Raphaël 105 et 163.

## Lot 11 — prière, paix et connaissance de soi, FAQ 091 (9 réponses)

- **Périmètre** : `data/faq-091-1.json` à `data/faq-091-9.json` et `data/faq-091-books.json`.
- Les références de Raphaël 72, 2, 45, 154, 161, 130, Michaël 5, 43, 273, 168, 205, 257 et 1, Gabriel 76, 278, 289 et 198, Ouriel 62, 74, 85, 25, 115, 221 et 137 ont été relues.
- **Corrections : 2 réponses** : `faq-priere-paix-1` et `faq-priere-paix-4`. Les commentaires rédactionnels finaux ont été remplacés par des enseignements de Raphaël 72 et Ouriel 62.
- **Sept autres réponses** conservées telles quelles.

## Bilan des 102 réponses — audit documentaire terminé

| Fichier(s) | Réponses examinées | Réponses modifiées |
| --- | ---: | ---: |
| `data/faq-public-085.json` | 25 | 3 |
| `data/faq-090-{1..5}.json` | 5 | 0 |
| `data/faq-091-{1..9}.json` | 9 | 2 |
| `data/faq-092.json` | 10 | 0 |
| `data/faq-093.json` | 5 | 0 |
| `data/faq-094.json` | 6 | 0 |
| `data/faq-095.json` | 7 | 0 |
| `data/faq-096.json` | 14 | 3 |
| `data/faq-097.json` | 8 | 0 |
| `data/faq-098.json` | 13 | 13 |
| **Total** | **102** | **21** |

**Dernière vérification de contenu** : les 22 fichiers FAQ ont été chargés sur la branche d'audit et reparsés. Les deux lots totalisent respectivement **35** et **67** réponses, avec des identifiants distincts dans chaque lot. Aucune expression figurant dans le filtre de commentaires scientifiques extérieurs (dont « scientifique », « pas une preuve », « démontré » et « doctrine ») n'a été relevée dans les 102 réponses de la branche corrigée ; chaque réponse contient une mention de psaume.

**Limites à conserver explicitement** : la comparaison a été réalisée avec les psaumes canoniques *structurés et extraits* du dépôt, sans relecture indépendante des pages scannées du PDF source et sans authentification humaine. Un contrôle lexical et une vérification de l'existence de versets ne prouvent pas à eux seuls chaque nuance éditoriale. La branche, cette note et les modifications de FAQ restent en **PR DRAFT** : aucune fusion, aucune publication.


## Contrôle d'intégration et correction de régression — 6 novembre 2026

Une vérification des règles du chargeur public \`js/biblaw-faq.js\` a révélé une anomalie **non détectée par les validations linguistiques** : les corrections éditoriales ajoutaient des citations alors que le chargeur impose un nombre exact de références par question. Sans correction, le chargement des FAQ aurait échoué après intégration, malgré la validité des JSON. Certaines citations composaient par ailleurs deux psaumes dans une même parenthèse, que le parseur aurait attribuée à tort à un seul psaume.

**Réparation, dans l'ordre :**
1. Les trois réponses modifiées de \`faq-public-085.json\` ont conservé leurs références d'origine cliquables, sans citation supplémentaire contradictoire.
2. Les références groupées ambiguës ont été supprimées dans \`faq-091-1.json\`, \`faq-096.json\` (question 13) et \`faq-098.json\` (question 1) ; les références originales justifiant ces passages ont été conservées.
3. Les compteurs exacts attendus pour les questions 091, 096 et 098 ont été alignés sur les textes corrigés dans le chargeur. Le contrôle strict reste actif : une référence absente ou supplémentaire provoquera une erreur détectable, plutôt qu'une interprétation silencieuse.
4. Une sentinelle indépendante a été ajoutée dans \`scripts/check_faq_integrity.mjs\`, déclenchée sur les PR pertinentes par \`.github/workflows/faq-integrity.yml\`. Elle vérifie les 102 identifiants, les compteurs de références, la syntaxe des citations, leur ordre (FAQ 085), la correspondance archange/livre/psaume, l'existence des numéros de versets et l'absence de références groupées ambiguës.

**Preuve CI :** exécution GitHub Actions « FAQ reference integrity » **réussie** sur le commit \`d7ad8599ca960febe7fe22481ff79460e4978373\`. Résultat : **102 réponses distinctes, 407 références de psaumes exploitables, 166 psaumes canoniques distincts**. Les quatre autres workflows GitHub de ce commit ont également terminé avec succès. Cette preuve est **technique**, pas une relecture théologique ni un test visuel sur téléphone.

**Reste à vérifier :** le PDF original nommé \`Bible essénienne (classée par livres).pdf\`, indiqué comme provenance par le corpus, n'a pas été retrouvé parmi les fichiers identifiés dans le Drive connecté lors de cette intervention. Les comparaisons directes avec les pages du PDF et le test visuel interactif en navigateur mobile n'ont pas été effectués. Pas de fusion, pas de publication : PR #74 et PR #72 conservées en DRAFT.

## Nettoyage éditorial ciblé — 6 novembre 2026

- Une relecture complémentaire des formulations visibles a identifié un commentaire rédactionnel extérieur au corpus dans `faq-harmonie-conscience-10` (« Quelle est la différence entre le cerveau et le mental ? ») : une explication sur ce que les psaumes ne définissent pas anatomiquement. Cette réserve a été **supprimée**, en conservant uniquement l'enseignement de Gabriel 119:14-16. Le nombre et le contenu des six références cliquables n'ont pas changé.
- Principe pour la suite : supprimer d'abord les phrases non appuyées, ne pas ajouter de nouvelles interprétations, ne conserver que les formulations reliées directement à des psaumes. Les passages douteux doivent être comparés aux versets avant correction.

## Relecture ciblée des formulations déductives — suite du 6 novembre 2026

La vérification a repris les réponses sur la science, les sens subtils, la conscience, la pensée, la mission personnelle et les pratiques spirituelles. Les passages à risque sont comparés aux versets avant suppression, sans modifier les questions ou le corpus.

Deux corrections supplémentaires :

1. `faq-religions-science-8` (« Une expérience mystique est-elle uniquement un phénomène cérébral ? ») : suppression de la conclusion rédactionnelle présentant l'expérience mystique comme n'étant pas exclusivement liée aux fonctions physiques. Ce rapprochement avec le cerveau n'était pas énoncé directement par les passages cités. Remplacement par l'enseignement explicite de Michaël 274:7-9 : les sens physiques servent de fondement à l'éveil des sens subtils. Les trois références existantes sont maintenues.
2. `faq-harmonie-conscience-11` (« Quelle est la différence entre le mental et la conscience ? ») : retrait du dernier paragraphe qui constituait une synthèse interprétative non sourcée définissant « le mental ». Les quatre paragraphes attribués à Ouriel et Raphaël, avec leurs quatre références canoniques, restent inchangés.

**Contrôle après corrections :** les cinq workflows GitHub du commit `ba565c14c4ec2f4f35760e2a2f15cd57ffe830f4` ont abouti avec succès, notamment `FAQ reference integrity` (102 réponses et liens canoniques).

**Attention intégration :** le fichier `index.html` de la branche historique PR #72 ne contient pas encore la section FAQ, et plusieurs fichiers FAQ/leur chargeur y sont absents. Ne jamais supposer que PR #72 et PR #74 sont interchangeables ; conserver ces changements séparés et vérifier la conservation de la FAQ si les deux branches sont réunies ultérieurement. Rien n'a été fusionné ni publié.

**Bilan corrigé :** 23 réponses ont fait l'objet d'au moins une modification textuelle dans cette branche, dont les deux corrections ci-dessus. Les réponses restantes n'ont pas été réécrites. La confirmation éditoriale humaine et la comparaison indépendante au PDF source restent distinctes des tests techniques.

## Préparation finale de publication — 6 novembre 2026

- **État éditorial effectif** : 102 réponses présentes, 23 réponses modifiées par rapport à `main`. Les suppressions ciblent les commentaires scientifiques extérieurs, les consignes inventées et les synthèses non explicitement fondées sur les textes canoniques. Les autres réponses sont conservées.
- **État technique final** : 406 références cliquables dans les 102 réponses ; 166 psaumes distincts du corpus structuré. Les doublons rédactionnels finaux de FAQ 091-1 et 091-4 ont été retirés après audit, sans toucher aux psaumes.
- **Compatibilité déploiement Pages** : tous les anciens audits `audit_faq_*.py` et tests `smoke_faq_*.mjs` sont désormais joués dans la CI de la PR. Les scripts historiques 096 et 097/098 ont été alignés sur le nouveau nombre réel de citations, tout en maintenant leurs contrôles des identifiants, des numéros de versets, des titres et des exports. L'exécution ciblée a réussi.
- **Navigation réelle testée** : le smoke Chromium à fenêtre mobile (390 × 844) a confirmé la liste des 102 questions, l'ouverture d'une réponse, les versets cités mis en évidence, le retour à la réponse, un téléchargement PDF réel et les sous-titres de la dernière question. Le test distinct de la recherche a aussi permis d'identifier et corriger un problème mobile où la liste de suggestions recouvrait le bouton « Rechercher » ; sur petit écran elle reste désormais dans le flux de la page.
- **Cache du navigateur** : la version des assets modifiés a été incrémentée en `v=099` dans `index.html` et le chargeur FAQ, afin d'éviter de servir l'ancien texte et le vieux JavaScript.
- **PDF canonique retrouvé dans le dépôt** : `Bible essénienne (classée par livres).pdf` existe à la racine du dépôt (`main`, 15 890 697 octets), contrairement à l'incertitude indiquée dans les notes intermédiaires. Cette intervention a contrôlé le corpus structuré et ses métadonnées de pages, pas vérifié indépendamment chaque page originale du PDF. La présence du PDF n'est pas une validation humaine automatique des interprétations.
- **Préservation** : PR #72 non modifiée, distincte de la PR #74. Aucun changement au corpus canonique.


## MISSION 2 — Comparaison directe avec le PDF original — 7 novembre 2026

**Résultat : contrôle effectué sur le PDF original lui-même.** Fichier `Bible essénienne (classée par livres).pdf`, 4 744 pages (15 890 697 octets), conservé dans le dépôt. Le lecteur PyMuPDF a extrait la couche textuelle de pages identifiées dans ce fichier ; le contrôle a comparé des segments de texte en début, milieu et fin de chaque verset sensible avec les versets des JSON du corpus.

| Mesure | Résultat |
| --- | ---: |
| Psaumes sélectionnés parmi les sources des 23 FAQ modifiées | **33** |
| Versets ciblés directement confrontés au PDF | **187** |
| Versets retrouvés dans le PDF | **187 / 187** |
| Absences textuelles confirmées | **0** |
| Versets avec correspondance de 3 segments sur 3 | **174** |
| Cas présentant une divergence de page source indiquée dans le JSON | **8** |

Les **8 divergences de pagination** ne sont pas des désaccords sur le texte : sept versets du **psaume 182 d'Ouriel, versets 29 à 35**, figurent page **3112** du PDF, tandis que `sourcePages` les place page **3109** (page de titre du livre 32). Le verset **16 du psaume 189 de Michaël** est retrouvé page **2320**, alors que la page source enregistrée est **2319** (un passage chevauchant une page est possible). Les passages eux-mêmes concordent ; la provenance paginée doit faire l'objet d'une correction distincte, contrôlée, sans retoucher les mots des psaumes.

**Exemples de rapprochements éditoriaux contrôlés :**

- **Michaël 274:7–9 (PDF pages 4168–4169)** : les sens physiques sont un fondement pour l'éveil des sens subtils ; formulation de FAQ correspondante conservée.
- **Gabriel 119:14–16 (page 1237)** : l'intellect est une partie de l'intelligence globale ; la réponse sur le cerveau et le mental conserve uniquement cet enseignement.
- **Ouriel 138:5–9 et Raphaël 184:10–13 (pages 2117 et 3003–3004)** : les versets exposent explicitement la réincarnation telle que la Bible essénienne l'enseigne ; la réponse ne doit pas réintroduire de réserve scientifique extérieure.
- **Raphaël 26:4–10 (pages 362–363)** : passages sur l'éveil et la fonction de la conscience.
- **Gabriel 209:4–10 (pages 2939–2940)** : amour, respect, admiration, confiance et dialogue ; la formulation de FAQ est effectivement appuyée par ces versets.
- **Ouriel 182:29–35 (page 3112)** : unité de la vie spirituelle et de la vie matérielle, malgré les erreurs de `sourcePages` des sept versets.

**Traçabilité :** fichier `docs/FAQ-PDF-SOURCE-EVIDENCE-2026-11-07.json` (187 contrôles individuels), script reproductible `scripts/audit_faq_pdf_source.py`, GitHub Actions « FAQ source PDF comparison » du run **42367205982** (réussi). Les correspondances contrôlent des segments des versets et ne constituent pas, à elles seules, une validation indépendante de toutes les nuances rédactionnelles des 102 réponses.

**Périmètre et sécurité :** aucun texte du corpus original n'a été modifié et aucune PR n'a été fusionnée ou publiée. Mission 2 de vérification de la source des passages sensibles **achevée** ; les anomalies de pagination sont consignées pour une correction spécifique à la provenance, distincte du nettoyage éditorial.

## MISSION 3 — Nettoyage éditorial final des 102 réponses — 7 novembre 2026

**Principe éditorial confirmé :** exposer les enseignements de la Bible essénienne, sans avis scientifique extérieur, réserve personnelle, extrapolation au-delà des versets ni consignes pratiques inventées. Conserver les paragraphes appuyés par des psaumes et ne supprimer que les ajouts étrangers au corpus.

**Relecture finale :** l'ensemble des **102 réponses** a été contrôlé par une nouvelle recherche de commentaires éditoriaux extérieurs, de comparaisons cérébrales, de réserves scientifiques et de faux exercices pratiques. Après correction, aucune des expressions ciblées n'est restée dans les réponses. Les synthèses de l'enseignement provenant de plusieurs versets ne sont pas supprimées mécaniquement lorsqu'elles sont cohérentes avec les sources citées.

Corrections ciblées effectuées pendant cette mission :

1. `faq-mort-3`, **« Peut-on retrouver ses proches décédés ? »** : suppression de la formule ajoutée « les passages examinés ne garantissent pas… », qui commentait les textes de l'extérieur. L'explication sur Raphaël 178:4,5,15 a été précisée pour parler des mondes subtils et des influences réellement rencontrés pendant la vie, sans suggérer indûment la réunion avec les proches humains après la mort. Trois liens conservés.
2. `faq-religions-science-8`, **expérience mystique et cerveau** : suppression de la comparaison initiale inférée avec les phénomènes du corps physique et d'une reprise finale redondante. Conservation de l'enseignement explicite de Michaël 274 sur les sens physiques et subtils, avec les trois références déjà présentes.
3. `faq-realite-spirituelle-3`, **« Dieu existe-t-il ? »** : retrait de la comparaison selon laquelle Dieu ne serait pas une « simple idée élaborée par l'homme ». Conservation de l'exposé positif de la Bible essénienne et des trois psaumes sources.
4. **Sept introductions** reformulées sans changer leur sens ni leurs références : `faq-dieu-3`, `faq-mort-4`, `faq-nature-dieu-1`, `faq-nature-dieu-2`, `faq-nature-dieu-4`, `faq-nature-dieu-5` et `faq-priere-paix-4`. Désormais, chaque réponse commence exactement par **« La Bible essénienne enseigne que »**.

**Bilan comparé à `main` :** **30 réponses modifiées**, **72 autres laissées intactes**. Le nombre de réponses demeure 102. Les **406 références cliquables** sont maintenues, y compris dans les réponses retouchées pendant cette mission. Le script `scripts/check_faq_integrity.mjs` impose dorénavant la formule d'attribution dès le début de chaque réponse et interdit explicitement plusieurs tournures de commentaires scientifiques ou éditoriaux extérieurs.

**Validation technique :** le workflow « FAQ reference integrity » et le workflow « FAQ source PDF comparison » ont terminé avec succès après les dernières modifications de contenu (commit `fa1450278739bae7f6bbfd1575a446ec13cd9453`). Ces contrôles n'affirment pas que les 102 paraphrases ont été certifiées par une autorité doctrinale. Ils garantissent la structure, la fidélité textuelle des 187 versets PDF contrôlés précédemment et l'absence des tournures bannies recherchées.

**Conservation des travaux :** PR #74 toujours **DRAFT**, PR #72 inchangée, pas de fusion, pas de publication et aucune modification des textes canoniques.

**Statut : MISSION 3 TERMINÉE.** Les tests fonctionnels complets et la préparation de publication constituent les missions 4 et 5.

## MISSION 4 — Tests complets de l'interface publique — 7 novembre 2026

**Statut : TERMINÉE, tous les tests du parcours de la mission 4 ont réussi.**

Un nouveau test intégré Chromium/Playwright, `scripts/smoke_faq_full_browser.mjs`, a parcouru automatiquement le **véritable assemblage local de GitHub Pages (`_site`)**, sans publication, dans **deux fenêtres** : téléphone **390 × 844** et ordinateur **1440 × 900**.

| Scénario | Téléphone | Ordinateur |
| --- | ---: | ---: |
| Questions affichées dans l'index | 102/102 | 102/102 |
| Réponses ouvertes, puis retour à l'index | 102/102 | 102/102 |
| Liens de psaumes présents et actifs | 406/406 | 406/406 |
| Aller-retour réel lecteur de psaume → réponse, versets cités surlignés | 16 | 16 |
| Vrais fichiers PDF téléchargés, entête `%PDF-` et contenu non vide | 3 | 3 |
| Écrans débordant horizontalement | 0 pixel | 0 pixel |
| Erreurs JavaScript dans la console/page | 0 | 0 |
| Recherche d'un numéro de psaume puis changement de thème | PASS | PASS |
| Recherche de deux mots `vie + amour` | PASS | PASS |
| Fermeture/réouverture de la FAQ, sous-titres des réponses | PASS | PASS |
| Présence des filtres de sources/archanges, Notes et Index, Questions populaires cachées | PASS | PASS |

Dans les deux formats, la recherche `105` produit **quatre psaumes**, puis le remplacement par `sainte assemblée` donne **trois psaumes**, sans laisser les anciens résultats visibles. Les trois vrais PDF extraits par format sont valides (tailles 2 811, 3 626 et 13 843 octets). Les trois tests précédemment installés ont réussi dans la même exécution : `smoke_faq_browser.mjs`, `smoke_occurrence_expansion_browser.mjs`, `smoke_occurrences_041c.mjs` (8 racines d'expansion lexicales).

**Correction découverte et vérifiée pendant la mission 4 :** sur ordinateur, la liste déroulante de six suggestions de recherche pouvait couvrir le bouton **« Rechercher »**, empêchant son clic. Le test complet l'a reproduit, alors que la version téléphone réussissait. La règle CSS de maintien des suggestions dans le flux, initialement réservée au mobile, est devenue commune aux deux formats, sans changer le fond ni le style des éléments. La version de `css/biblaw-light.css` utilisée par `index.html` a été incrémentée à `v=100`. Le nouveau test et la régression de recherche sont désormais **verts dans les deux formats**.

**Preuve GitHub Actions :** `Browser smoke - lexical occurrence expansion`, run **42370822346**, commit **`15ccc597510d2951cc947eb2a958cb9a2dc5a6fe`**, conclusion **success**. Les rapports `MISSION4_VIEWPORT_PASS` présents dans les logs donnent les mesures détaillées pour chaque format. Le workflow a fait une construction locale de la charge utile GitHub Pages, et n'a pas testé le domaine public après déploiement.

**Périmètre :** les tests portent sur la FAQ, le parcours de recherche, les liens canoniques, les PDF, les options et la navigation. Ce sont des tests fonctionnels automatisés de navigateur, pas une revue esthétique manuelle de toutes les pages ni un essai sur chaque appareil physique. Les tests complémentaires de compatibilité et de mise en ligne sont réservés à la mission 5.

**Sécurité :** PR #74 toujours DRAFT et non fusionnée, PR #72 intacte, aucun changement aux textes canoniques, aucun déploiement.
