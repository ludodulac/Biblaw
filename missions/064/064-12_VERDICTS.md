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

## Sous-lot B — NON COMMENCÉ
Dossiers attendus : `26/176/001`, `26/178/001`, `26/181/001`, `26/189/001`, `26/189/003`. Ce dernier nécessite une vérification de l'unique appel imprimé face au dossier historique 063 `26/189/002`, non résolu : aucune conclusion par correspondance machine.
