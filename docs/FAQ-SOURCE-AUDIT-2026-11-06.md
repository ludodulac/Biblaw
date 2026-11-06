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
