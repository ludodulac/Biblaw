# 🌸 BIBLAW — 064-12 — verdicts documentaires

**Périmètre** : dix identifiants définis par `missions/064/064_PLAN.md` ; reprise du HEAD 064-11 `90d013a732a273135ebeca37ee272e82731f796b`. PR #72 OPEN/DRAFT, `feat/052-search-ui`. Pas de publication, fusion, déploiement, ni modification du corpus. Les correspondances automatiques ne sont jamais des verdicts.

## Sous-lot A — cinq notes — CHECKPOINT

**Source et preuve** : PDF original de 4 744 pages ; lecture des images de p.2020–2021, 2023, 2134–2135, 2361–2362, 2373. Contrôle de contexte limité aux pages pertinentes **2019–2024, 2133–2135, 2360–2362, 2372–2374**. Extrait avec `scripts/prove_notes_064_12_A.py` sans mutation, [Actions #40104261969](https://github.com/ludodulac/Biblaw/actions/runs/40104261969) SUCCESS, artefact `biblaw-064-12-proof-A` **12564375980** : `note-proof.json`, images PNG originales et positions typographiques. Les limites et numéros ont été contrôlés visuellement, en distinguant les notes du texte italique des prières et les appels du corps des psaumes.

| ID | Page PDF | Verdict | Preuve des limites imprimées, n° et rattachement | Décision |
|---|---|---|---|---|
| `book-23-psalm-145-note-001` | 2020–2021 | **NON RÉSOLUE** | P.2020 : appel 1 au verset 37 du psaume 145 et **unique note en pied n°1 de 30 tokens**, fin « emprisonnants, etc. ». JSON **263 tokens** : 30 de note puis **233 d'une continuation de la prière Pr.41** distincte, en italique, p.2021 (« Dans l’enracinement et la floraison… Amin. »). `noteIds` réciproque. | Aucune correction ; note composite conservée pour découpage sûr hors 064-12. |
| `book-23-psalm-146-note-001` | 2023 | **AUTHENTIFIÉE** | Appel n°1 au verset 19 ; note unique n°1 sous le filet, **15/15 tokens exacts**, de « Il s’agit de l’étude » à « et de l’œuvre. ». Rattachement au psaume 146 et `noteIds` réciproque ; aucune collision. | Aucune correction. |
| `book-24-psalm-141-note-001` | 2134–2135 | **NON RÉSOLUE** | Appel n°1 au verset 22 du psaume 141 ; pied p.2134 n°1 **50 tokens**, fin « intelligence supérieure. ». JSON **440 tokens** : note 50 + **390 tokens de la prière Pr.36**, typographiquement indépendante p.2135, commençant « Ô Père de la terre de Lumière ». `noteIds` réciproque. | Aucune correction ; distinguer note/prière dans une mission ultérieure. |
| `book-26-psalm-169-note-001` | 2361–2362 | **NON RÉSOLUE** | Appel n°1 au verset 35 du psaume 169 ; pied p.2361 n°1 **24 tokens**, fin « toutes les religions. ». JSON **386 tokens** : note 24 + **362 tokens de la prière Pr.54** (italiques p.2361, suite p.2362 commençant « Tu prendras la statue consacrée… »). `noteIds` réciproque. | Aucune correction ; pas de perte du texte de prière autorisée. |
| `book-26-psalm-172-note-001` | 2373 | **AUTHENTIFIÉE** | Appel n°1 au verset 4 du psaume 172 ; pied n°1 **11/11 tokens exacts**, « Il s’agit de la corde de la Ronde des Archanges. ». Psaume 172 et `noteIds` réciproques ; identités distinctes des notes 002/003 du même psaume. | Aucune correction. |

**A : 5 examinées = 2 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 3 NON RÉSOLUES.** Les trois anomalies sont des textes composites, non des erreurs autorisant un tronquage isolé. Les fichiers sources demeurent inchangés.

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Preuve** : pages PDF principales **2392, 2397, 2412, 2452, 2453**, pages de contrôle 2391–2393, 2396–2398, 2411–2413, 2451–2454, obtenues directement du PDF original par `scripts/prove_notes_064_12_B.py`, images et coordonnées/texte archivés dans `biblaw-064-12-proof-B`, artefact **12564281933** ; [Actions #40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724) **SUCCESS**. Le marqueur imprimé n°1 se réinitialise localement ; l'ordinal d'ID ne constitue pas sa preuve.

| ID | Page PDF | Verdict | Justification documentaire des limites, appels, rattachements et doublons | Décision |
|---|---|---|---|---|
| `book-26-psalm-176-note-001` | 2392 | **AUTHENTIFIÉE** | Appel n°1 au verset 22 et pied distinct n°1 **43/43 tokens**, début « Pour faire suite à ce psaume », fin « maintenir le lien. ». Psaume 176, `noteIds` réciproque et pas d'autre note du psaume. | Aucune correction. |
| `book-26-psalm-178-note-001` | 2397 | **AUTHENTIFIÉE** | Appel n°1 au verset 1 du psaume 178 ; note de pied n°1 **22/22 tokens**, « Lors d’un partage » → « répondu spontanément. ». `noteIds` réciproque ; aucun doublon. | Aucune correction. |
| `book-26-psalm-181-note-001` | 2412 | **AUTHENTIFIÉE** | Appel n°1 au verset 13 ; unique pied n°1 **23/23 tokens**, « Le sceau de L’Archange Gabriel » → « règnes de la création. ». Psaume 181 et `noteIds` réciproques ; les autres IDs 181/002–003 ont une source distincte p.2415, sans confusion avec cette note p.2412. | Aucune correction. |
| `book-26-psalm-189-note-001` | 2452 | **AUTHENTIFIÉE** | Appel n°1 au verset 5 du psaume 189 et pied complet n°1 **102/102 tokens**, « La nuit qui précéda » → « (voir le psaume 176). ». `noteIds` réciproque ; texte distinct du pied p.2453 et des dossiers 002/003. | Aucune correction. |
| `book-26-psalm-189-note-003` | 2453 | **NON RÉSOLUE** | Un seul appel imprimé n°1 au verset 8 et **un seul pied de page n°1, 29/29 tokens**, « L’Archange fait ici référence à la pierre sacrée » → « Ronde des Archanges. ». Le contenu extrait de 003 égale bien le pied, mais le dossier `book-26-psalm-189-note-002` **NON RÉSOLU en 063** revendique également le **même début de 29 tokens et le même appel p.2453**, suivi de versets parasite ; il n'existe pas une seconde occurrence imprimée permettant de justifier deux identités. `noteIds` réciproque ne résout pas cette concurrence. | Aucune correction, dédoublonnage, fusion ou validation implicite du 002 ; résolution d'identité dans une mission distincte. |

**B : 5 examinées = 4 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 1 NON RÉSOLUE.** Une correspondance parfaite au PDF n'efface pas une collision d'identifiants.

## Bilan final — 064-12 uniquement

- **10/10 examinées** : **6 AUTHENTIFIÉES**, **0 CORRIGÉE ET AUTHENTIFIÉE**, **4 NON RÉSOLUES** (`23/145/001`, `24/141/001`, `26/169/001`, `26/189/003`). Deux sous-lots indépendants de cinq : A 2+3, B 4+1.
- **Pages PDF originales strictement ciblées** : p.**2019–2024, 2133–2135, 2360–2362, 2372–2374, 2391–2393, 2396–2398, 2411–2413, 2451–2454** (28 pages). Les impressions des dix notes ont été vérifiées visuellement ; les voisinages n'ont servi qu'aux limites et rattachements.
- **Preuves Actions** : A [#40104261969](https://github.com/ludodulac/Biblaw/actions/runs/40104261969) SUCCESS, garde A [#40104571746](https://github.com/ludodulac/Biblaw/actions/runs/40104571746) SUCCESS, B [#40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724) SUCCESS ; artefacts **12564375980** (A) et **12564281933** (B). La garde B figure dans le script final et vérifie aussi le conflit d'ID 189/002–003.
- **Cumul 064/192** : **120 examinées, 96 AUTHENTIFIÉES dont une corrigée historiquement en 064-06, 24 NON RÉSOLUES, 72 restantes**. Aucun des 110 dossiers déjà traités avant 064-12 n'a été rouvert.
- **Protection** : aucune note, prière, aucun psaume, statut de publication, catalogue, moteur ou interface modifié. PR #72 OPEN/DRAFT, pas de fusion ou déploiement. **STOP après 064-12.**
