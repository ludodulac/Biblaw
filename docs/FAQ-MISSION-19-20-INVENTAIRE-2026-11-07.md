# BIBLAW — Mission questions 19 et 20 : inventaire et arbitrage éditorial

> **MISE À JOUR DÉFINITIVE (7 novembre 2026)** — Le tableau ci-dessous conserve les 19 formulations et leur **premier classement de repérage** (9/8/2). Les décisions finales, prises après lecture du corpus et vérification directe du PDF original, figurent dans `docs/FAQ-MISSION-19-20-ROUTING.json` et `docs/FAQ-MISSION-19-20-BILAN-FINAL-2026-11-07.md` : **3 réponses nouvelles**, **12 formulations vers des réponses existantes**, **2 formulations renvoyées à l'une des réponses nouvelles**, **2 questions sans source suffisante**. Les **110 versets effectivement cités** ont été localisés dans le PDF original ; les cinq versets débordant sur deux pages ont été rapprochés sur les deux pages. Aucune modification du site public.
**Date :** 7 novembre 2026  
**Statut :** travail préparatoire — non publié, non intégré aux FAQ  
**Dépôt :** `ludodulac/Biblaw`  
**Référence de lecture des 102 FAQ :** branche `fix/faq-source-audit-2026-11-06`, HEAD `5eb79ea617bab48115ebb3d7ad6039b9870e167a` (PR #74, DRAFT). PR #72 inchangée.  
**Branche du présent dossier :** `docs/faq-19-20-editorial-2026-11-07`, créée depuis `main`. Cette branche ne reprend ni ne modifie les changements de la PR #74.

## 1. Méthode et portée effective
Les **102 intitulés** ont été inventoriés sur la branche de la PR #74 : 25 (`faq-public-085`), 5 (lots `faq-090`), 9 (`faq-091`), 10 (`faq-092`), 5 (`faq-093`), 6 (`faq-094`), 7 (`faq-095`), 14 (`faq-096`), 8 (`faq-097`), 13 (`faq-098`). Total : 102.

Le **texte des réponses directement pertinentes** a été rapproché des 19 sujets. Les psaumes retenus pour les trois nouveaux projets de réponse ont été lus dans le corpus canonique structuré `data/corpus/books/`, avec leurs versets numérotés. Cela **n'équivaut pas à un nouvel audit intégral des 102 textes**.

Au stade du premier inventaire, le PDF n'avait pas encore été ouvert directement. **Cette limitation a été levée** : une copie binaire strictement identique au PDF du dépôt a ensuite été comparée et inspectée page par page (SHA-256 et résultats dans le bilan final). La PR #74 contient déjà `docs/FAQ-PDF-SOURCE-EVIDENCE-2026-11-07.json` : **187 versets ciblés de 33 psaumes** comparés à la couche textuelle du PDF, 187 trouvés, dont des divergences de pagination. Cette preuve partielle ne confirme pas automatiquement tous les versets cités ci-dessous. **Cette limite de première passe a été levée pour les trois nouveaux articles**, grâce à la vérification PDF ciblée de l'ensemble des 110 versets cités. Cela ne constitue pas un audit général des 102 réponses antérieures.

### Codes
- **EXISTANTE** : une réponse actuelle répond déjà directement à la question ; conserver le texte de référence, proposer un renvoi.
- **PARTIELLE** : thème voisin traité, mais angle ou formulation supplémentaire ; éviter les réponses quasi identiques.
- **NOUVELLE / SOURCE NON TROUVÉE** : absence de réponse directe et impossibilité de rédiger avec certitude sans texte explicite des psaumes.

## 2. Correspondance des 19 demandes avec les 102 FAQ

| N° | Question demandée (abrégée) | État | Réponses FAQ déjà présentes | Décision |
|---:|---|---|---|---|
| 1 | Que devient notre conscience après la mort ? | PARTIELLE | `faq-mort-1`, `faq-mort-2`, `faq-harmonie-conscience-13` | Projet A, qui traite explicitement la **continuité conditionnelle** de conscience. |
| 2 | La conscience disparaît-elle lorsque le cerveau cesse de fonctionner ? | PARTIELLE | `faq-harmonie-conscience-13`, `faq-mort-2` | Renvoi au projet A et à `faq-harmonie-conscience-13` ; **ne pas attribuer une thèse neurologique aux psaumes**. |
| 3 | Existe-t-il une vie après la mort ? | EXISTANTE | `faq-mort-1`, `faq-mort-4` | Réutilisation de `faq-mort-1`. |
| 4 | Existe-t-il une réincarnation ? | EXISTANTE | `faq-mort-5` (« La réincarnation est-elle possible ? ») | Réutilisation exacte de `faq-mort-5`. |
| 5 | Existe-t-il une autre forme d'existence ? | PARTIELLE | `faq-mort-1`, `faq-realite-spirituelle-1`, `faq-realite-spirituelle-5` | Renvoi coordonné : existence au-delà du corps + dimensions spirituelles. |
| 6 | Que nous apprennent réellement les expériences de mort imminente ? | NOUVELLE / SOURCE NON TROUVÉE | Aucune FAQ directe. | **Suspendre** : aucune évocation précise des expériences de mort imminente repérée par les recherches textuelles ciblées dans le dépôt ; ne pas inventer leur signification. |
| 7 | La conscience peut-elle survivre à la mort du corps ? | PARTIELLE | `faq-mort-2`, `faq-harmonie-conscience-13` | Même réponse principale que n°1 (projet A), sans nouveau doublon. |
| 8 | Que peut nous apprendre la science sur la mort et l'au-delà ? | NOUVELLE / SOURCE NON TROUVÉE | `faq-religions-science-6` à `10` abordent science et réalité, non cette question. | **Suspendre** : aucune réponse doctrinale directe vérifiée ; ne pas insérer de commentaires scientifiques extérieurs. |
| 9 | Comment apprendre à mieux vivre sur Terre ? | PARTIELLE | `faq-pratique-spirituelle-1`, `faq-harmonie-conscience-1`, `faq-bonheur-6` | Question de synthèse ; privilégier un parcours de renvois plutôt qu'une répétition. |
| 10 | Comment vivre autrement ? | PARTIELLE | `faq-pratique-spirituelle-1`, `faq-pratique-spirituelle-11`, `faq-maitrise-interieure-5` | Renvois ; angle trop général pour justifier une FAQ indépendante sans cadrage. |
| 11 | Comment devenir plus heureux ? | EXISTANTE | `faq-bonheur-6`, `faq-bonheur-1` | Réutilisation de `faq-bonheur-6`. |
| 12 | Comment vivre harmonieusement avec les autres ? | EXISTANTE | `faq-harmonie-conscience-1`, `faq-harmonie-conscience-6` | Réutilisation de `faq-harmonie-conscience-1`. |
| 13 | Comment développer sa connaissance de soi ? | EXISTANTE | `faq-priere-paix-7`, `faq-maitrise-interieure-1` | Réutilisation de `faq-priere-paix-7`. |
| 14 | Comment transformer ses pensées et ses émotions ? | EXISTANTE | `faq-maitrise-interieure-1`, `faq-pratique-spirituelle-6`, `faq-pratique-spirituelle-7` | Renvoi aux réponses distinctes, sans texte fusionné répétitif. |
| 15 | Comment développer sa conscience ? | PARTIELLE | `faq-harmonie-conscience-8`, `faq-pratique-spirituelle-3`, `faq-pratique-spirituelle-4` | Projet B : focus sur l'éveil de la conscience, à distinguer de sa définition. |
| 16 | Comment donner un sens à ses activités quotidiennes ? | EXISTANTE | `faq-pratique-spirituelle-11`, `faq-pratique-spirituelle-12` | Réutilisation de `faq-pratique-spirituelle-11`. |
| 17 | Comment concilier vie matérielle et vie spirituelle ? | EXISTANTE | `faq-pratique-spirituelle-1`, `faq-realite-spirituelle-1` | Réutilisation de `faq-pratique-spirituelle-1`. |
| 18 | Comment progresser intérieurement grâce aux expériences de la vie ? | PARTIELLE | `faq-sens-personnel-3`, `faq-sens-personnel-5`, `faq-pratique-spirituelle-11` | Projet C sur les événements, le discernement et l'œuvre. |
| 19 | Comment faire de chaque journée une occasion de développement personnel et spirituel ? | EXISTANTE | `faq-pratique-spirituelle-11`, `faq-pratique-spirituelle-12`, `faq-pratique-spirituelle-13` | Réutilisation de `faq-pratique-spirituelle-11`. |

**Bilan de classement : 9 EXISTANTES, 8 PARTIELLES et 2 NOUVELLES / SOURCE NON TROUVÉE.** Les catégories décrivent l'existence d'une **réponse FAQ**, pas la validité définitive de chaque citation.

## 3. Premières recherches vérifiées dans le corpus canonique

| Sujet | Psaumes lus | Éléments effectivement lus |
|---|---|---|
| Conscience et au-delà | Michaël **254**, v. **1–15** et **20–28** (`book-37/psalm-254.json`) | Unité de la vie avant/après la mort ; conscience comme lien entre les mondes ; seuls les acquis rendus conscients fondent la continuité. |
| Acquis après la mort | Raphaël **106**, v. **14–18** (`book-19/psalm-106.json`) | Perte possible de la mémoire après désincarnation ; possibilité de la sauvegarder par le travail de conscience. |
| Âme et mémoire | Ouriel **277**, v. **5–15** (`book-44/psalm-277.json`) | Distinction entre corps mortel et âme immortelle ; continuité consciente à élaborer ; mémoire de l'âme. |
| Éveil de la conscience | Raphaël **26**, v. **4–11** (`book-07/psalm-026.json`) | Conscience comparée au soleil, active dans la parole, les repas, le travail et les actes. |
| Éveil, étude et formation | Ouriel **106**, v. **5–21** (`book-20/psalm-106.json`) | Éducation de la conscience, étude, unité de pensée, sentiment et volonté. |
| Concentration | Michaël **160**, v. **1–17** (`book-21/psalm-160.json`) | Attention, concentration et conscience au sein des activités, sans protocole inventé. |
| Événements de la vie | Raphaël **177**, v. **3–6**, **14–18** (`book-27/psalm-177.json`) | Événements et rencontres ; méditer sur ce qui a marqué l'existence sans jugement précipité ; mettre l'œuvre en mouvement. |
| Choix et conséquences | Michaël **267**, v. **1–25** et **32–39** (`book-37/psalm-267.json`) | Toute situation propose un chemin ; chaque acte a inspiration et conséquence ; pratique quotidienne et destinée. |
| Inspiration incarnée | Ouriel **14**, v. **2–16** (`book-04/psalm-014.json`) | Unir inspiration de l'esprit et réalisations quotidiennes ; ne pas séparer les deux. |

**Note documentaire actualisée :** les psaumes, les archanges et la numérotation des versets ont été vérifiés dans le corpus canonique ; **les 110 versets cités dans le staging ont aussi été contrôlés dans le PDF original** par une nouvelle exécution ciblée dans la PR #75 (distincte des contrôles antérieurs de la PR #74).

## 4. Livrable rédactionnel et prochaine décision
Trois **projets de réponses développées**, sans insertion publique, sont conservés dans `docs/FAQ-MISSION-19-20-PROJETS-2026-11-07.md` :
- **A** : « Que devient notre conscience après la mort ? » (pour les demandes n°1, n°2 [uniquement l'enseignement doctrinal] et n°7).
- **B** : « Comment développer sa conscience ? » (n°15).
- **C** : « Comment progresser intérieurement grâce aux expériences de la vie ? » (n°18).

Avant toute intégration, terminer l'arbitrage des questions partielles n°5, 9, 10 ; contrôler les citations non couvertes contre le PDF original ; effectuer une validation éditoriale humaine et ensuite seulement produire les données FAQ nécessaires. **Aucun changement des 102 réponses existantes, aucun déploiement, aucune fusion.**
