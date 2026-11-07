# BIBLAW — Mission 1 : regroupement conservatoire des questions redondantes

**Date :** 7 novembre 2026  
**Branche de travail :** `feat/faq-100-dedup-10-2026-11-07`  
**PR :** #77 — DRAFT, aucune publication autorisée à cette étape.

## Objet

Réduire la présentation des questions qui font presque double emploi **sans supprimer la connaissance issue des psaumes**. Une réponse principale regroupe deux formulations proches et devient plus complète ; l'ancien titre est enregistré comme **formulation alternative recherchable**, et non comme seconde réponse.

Le regroupement est **conservatoire et réversible** : au lieu de réécrire librement la théologie, ce premier passage **conserve absolument chaque phrase, chaque paragraphe et chaque référence des deux réponses originales**, sans modification. Un intertitre « Approfondissement » sépare les enseignements complémentaires. Ce choix privilégie la garantie d'intégrité à la concision immédiate ; le texte peut encore contenir des répétitions de formulation entre les deux anciennes réponses, qui ne seront supprimées que lors d'une future relecture éditoriale rigoureuse.

## Les dix regroupements

| N° | Question conservée dans l'index | Autre formulation dirigée vers celle-ci | Particularité conservée |
|---:|---|---|---|
| 1 | Dieu existe-t-il vraiment, et comment peut-on le savoir ? | Dieu existe-t-il ? | Présence divine dans la conscience, l'étude des psaumes et les actes |
| 2 | Avons-nous une mission particulière ? | Ai-je une mission particulière ? | Talents, destinée, fidélité à l'œuvre individuelle |
| 3 | Pourquoi Dieu ne répond-il pas toujours à nos prières ? | Pourquoi certaines demandes restent-elles sans réponse ? | Patience, persévérance, accueil et transformation nécessaires |
| 4 | Toutes les religions conduisent-elles à la même vérité ? | Les religions sont-elles toutes des chemins vers Dieu ? | Les religions historiques et la Religion vivante |
| 5 | La science et la spiritualité sont-elles compatibles ? | Peut-on concilier une démarche scientifique avec la croyance en Dieu ? | Étude, foi, expérimentation et expérience de la connaissance |
| 6 | Comment trouver la paix intérieure et se rapprocher de son être profond ? | Comment cultiver sa paix intérieure ? | Méditation, stabilité intérieure, travail sur soi et actes |
| 7 | Qu'est-ce que le véritable bonheur et comment l'atteindre ? | Comment devenir véritablement heureux ? | Gratitude, santé, simplicité, joie de l'âme et quotidien |
| 8 | Comment aimer véritablement ? | Comment développer l'amour ? | Respect, écoute, bienveillance, coopération et actes |
| 9 | Pourquoi sommes-nous sur Terre ? | Pourquoi existons-nous ? | Mission terrestre et responsabilité envers les règnes de la nature |
| 10 | Comment mieux se connaître ? | Comment mieux me connaître et maîtriser mes pensées et mes émotions ? | Observation, méditation, maîtrise des influences et sentiments |

## Comptabilité de la prévisualisation

- **105 textes d'origine, strictement conservés** dans les fichiers JSON des FAQ 085 à 099.
- **10 réponses enrichies** par rapprochement de 20 textes, avec les deux textes complets et leurs liens.
- **95 questions visibles** dans l'index, soit 10 entrées redondantes de moins.
- **424 liens de citations vers les psaumes** ; aucun lien supprimé, toutes les références ouvrables.
- Les **19 formulations** issues des questions 19 et 20 conservent leurs destinations ; lorsqu'une destination renvoie à une entrée regroupée, elle pointe vers l'article enrichi correspondant.
- Export PDF : le texte complet des deux sources figure dans le même téléchargement ; pas de suppression d'enseignements.

La source des opérations est `data/faq-100-merge.json` : dix paires d'identifiants avec un intertitre de distinction. Le moteur construit la réponse enrichie à partir des textes originaux en mémoire ; le dépôt n'entretient **aucune copie éditoriale parallèle** des psaumes ou de leurs réponses.

Le script `scripts/check_faq_100_merge.mjs` reconstitue et examine l'ensemble des données, les 10 associations, les 95 titres visibles, les 424 citations et la validité des 19 routes. L'interface est testée par `scripts/check_faq_dom.mjs` et par Chromium sur téléphone et ordinateur.

## Ce qui n'est volontairement pas réalisé ici

La mission suivante demandée par le propriétaire — **afficher un menu « Les questions les plus fréquentes sur… » et des boutons de thèmes avant de charger ou d'afficher les questions** — n'a pas été engagée dans cette PR. Elle sera traitée séparément, une fois ce premier regroupement contrôlé, afin de ne pas mélanger les modifications éditoriales et les changements de navigation.

**Ne pas fusionner ni publier la PR #77 avant l'accord du propriétaire.**
