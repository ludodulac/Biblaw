# 🌸 BIBLAW — MISSION 064-15 — contrôle éditorial de 10 notes

**Reprise vérifiée** : branche `feat/052-search-ui`, PR #72 OPEN/DRAFT, HEAD initial `24157b49d9875d2236bea971361c5e2310454c44`. Périmètre = les dix identifiants du lot 064-15 de [064_PLAN.md](064_PLAN.md). Aucune des 140 notes historiques, ni leurs 33 anomalies, n'est réexaminée ; aucune publication, fusion, déploiement ou modification d'interface.

## Vigilance CI — état initial AVANT 064-15

Sur le HEAD d'entrée `24157b49` : **38 runs PR, 35 SUCCESS, 3 FAILURE**. Ces trois échecs étaient déjà présents avant toute opération du lot 064-15 ; on ne les répare pas ici :

1. **Browser smoke - lexical occurrence expansion** — [#40135535584](https://github.com/ludodulac/Biblaw/actions/runs/40135535584), échec `Validate legacy and 041C lexical safety contracts` : `scripts/audit_lexical_expansion_041c.py` exige `>THÈME</button>` et `>MOTS</button>` dans la page, `AssertionError` (contrat ancien de balises HTML).
2. **Audit theme entry identity** — [#40135535722](https://github.com/ludodulac/Biblaw/actions/runs/40135535722), échec `Verify search contract artifacts are untouched` : `Unreviewed js/biblaw.js changes; thematic search remains protected` ; protection des modifications d'interface héritées de la PR DRAFT.
3. **BIBLAW 058 corpus browse mobile** — [#40135535698](https://github.com/ludodulac/Biblaw/actions/runs/40135535698), étape `Install isolated Chromium` : Playwright 1.55.0 ne prend pas en charge Chromium sur `ubuntu26.04-x64` dans ce runner.

Les références, noms et causes viennent des métadonnées et journaux réels GitHub Actions au HEAD d'entrée. Les scripts PDF spécialisés ci-dessous sont distincts : leur succès ne vaut pas « toute la CI verte ».

## Sous-lot A — cinq notes — CHECKPOINT

**Preuves originales** : PDF source de 4 744 pages, **15 pages seulement** [2853–2855, 2872–2874, 2896–2898, 2900–2902, 2952–2954] rendues en images ×2, avec `note-proof.json` et relevés typographiques des pieds, après examen des appels imprimés, débuts et fins, numéros, pages des psaumes et identités concurrentes. [Action initiale #40137180838](https://github.com/ludodulac/Biblaw/actions/runs/40137180838) **SUCCESS**, artefact **12576971728** (`biblaw-064-15-proof-A`). Le verdict repose aussi sur une lecture visuelle, jamais sur un alignement automatique isolé.

| ID de la note | Pages source | Verdict | Preuve documentaire et décision |
|---|---|---|---|
| `book-30-psalm-192-note-001` | 2854–2855 | **CORRIGÉE ET AUTHENTIFIÉE** | P.2854 : renvoi¹ après « donnera » au verset **2** du psaume 192 ; un seul pied imprimé n°1 **5 tokens**, « Évangile selon Matthieu 7:7. » du début à la fin. L'ancienne extraction contenait **93 tokens**, 88 tokens ajoutés à tort depuis le début de la page 2855, continuation du **verset 11** (« qualité de vie qui fuit… »), nettement dans le corps du psaume, et non dans le pied. Psaume, page et `noteIds` réciproques. **Champ `text` corrigé à 5 tokens, rien d'autre.** |
| `book-30-psalm-196-note-001` | 2873–2874 | **CORRIGÉE ET AUTHENTIFIÉE** | P.2873 : renvoi¹ au **verset 3** (« mères pour l'autre ») ; pied imprimé n°1 **142 tokens**, du « Lorsque Olivier Manitara… » à « …qui est divin. » avec guillemet final. L'extraction initiale de **164 tokens** englobait indûment **22 tokens** commençant au haut de p.2874 (« terre ? » me direz-vous… »), continuation du **verset 6** et non du pied. Note ramenée à 142 tokens prouvés ; page, numéro et `noteIds` réciproques, pas de doublon. **Champ `text` uniquement.** |
| `book-30-psalm-200-note-001` | 2897 | **AUTHENTIFIÉE** | Appel¹ du verset **9** (« collier à 12 perles ») p.2897, pied n°1 **89/89 tokens** sans suffixe, de « Dans la Nation Essénienne… » à « …ciel de la Nation Essénienne. ». Psaume et `noteIds` réciproques ; occurrence distincte du pied p.2901. Aucune correction. |
| `book-30-psalm-200-note-003` | 2900–2901 | **NON RÉSOLUE** | Appel¹ sur « fonction … donnée » au dialogue p.2901, unique pied n°1 **111/111 tokens** sur les « piliers », sous filet. Mais `book-30-psalm-200-note-002`, dossier historique 063 NON RÉSOLU, revendique **la même page, le même pied et exactement le préfixe de 111 tokens**, suivi des versets 38–42 et de Pr.83 dans une extraction composite. Une seule note imprimée : identité 002/003 concurrente, dossier 063 non rouvert. Pas de correction. |
| `book-30-psalm-211-note-001` | 2952–2953 | **NON RÉSOLUE** | Pied n°1 **28/28 tokens** p.2953 (« Cette prière est la Prière de la goutte d'eau-Lumière… »), renvoi imprimé¹ attaché à **« Amin » dans la prière qui suit le psaume**, non à l'un de ses versets ; p.2953 **hors pages canoniques du psaume 211 [2948–2952]**, malgré `noteIds` réciproque. Rattachement à la prière indécidable dans l'identité actuelle : aucune mutation de prière ni de note. |

**Checkpoint A : 5 examinées — 3 AUTHENTIFIÉES, dont 2 CORRIGÉES ET AUTHENTIFIÉES ; 2 NON RÉSOLUES**. Les corrections sont des suppressions de texte du corps ajouté par erreur, pas des altérations du psaume ; les cinq verdicts sont consignés avant le sous-lot B.

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Preuves PDF original** : pages **2968–2973** (6 pages uniquement), captures ×2, relevés de disposition et source `note-proof.json` via `scripts/prove_notes_064_15_B.py`. [Actions initiale B #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177) **SUCCESS**, artefact **12577911782** (`biblaw-064-15-proof-B`). Les cinq cas ont été confrontés visuellement aux renvois et aux pieds originaux, pas uniquement aux tokens.

| ID de la note | Source PDF | Verdict | Preuve, limites, marqueur, rattachement et unicité |
|---|---:|---|---|
| `book-30-psalm-215-note-001` | 2969 | **AUTHENTIFIÉE** | Appel¹ au **verset 1** (« nouvelle année… la terre »), pied imprimé n°1 **62/62 tokens** de « Au sein de la tradition essénienne » à « l'année qui commence. » ; aucun débordement, page canonique et `noteIds` réciproque. |
| `book-30-psalm-215-note-002` | 2969 | **AUTHENTIFIÉE** | Appel² au **verset 3** (« 4 grandes fêtes de l'année »), pied imprimé **n°2** de **41/41 tokens** énumérant les quatre célébrations ; limites sous filet, page canonique et `noteIds` réciproque, aucun doublon. |
| `book-30-psalm-215-note-003` | 2969 | **AUTHENTIFIÉE** | Appel³ au **verset 5** (« dernière célébration de l'Archange Michaël »), troisième pied **n°3 de 140/140 tokens**, commencé « L'Archange fait ici allusion » et terminé « Nation Essénienne. ». Trois pieds différents numérotés 1, 2 et 3 sur la page, sans collision. `noteIds` réciproque. |
| `book-30-psalm-215-note-004` | 2971 | **NON RÉSOLUE** | Appel local¹ au **verset 20** (« Père Michaël »), pied imprimé n°1 **17/17 tokens**, renvoi « Dans l'Évangile de l'Archange Michaël, voir le psaume 216 » ; mais **un seul pied sur cette page** et l'identifiant `215/005` revendique exactement le même contenu, la même page et le même appel. Aucune preuve pour distinguer ces deux IDs ; identité concurrente. |
| `book-30-psalm-215-note-005` | 2971 | **NON RÉSOLUE** | Même pied unique n°1 de **17/17 tokens** sous filet et même appel au verset 20 que `215/004`. Le numéro 5 du fichier désigne un ordinal d'extraction et **pas** un n°5 imprimé. Impossible d'authentifier deux notes distinctes à partir d'une seule occurrence ; aucune fusion, suppression ou correction inférée. |

**Checkpoint B : 5 examinées — 3 AUTHENTIFIÉES, 0 CORRIGÉE, 2 NON RÉSOLUES.**

## Bilan final strict 064-15

- **10/10 notes examinées** : sous-lot A **3 authentifiées (dont 2 corrigées) + 2 NON RÉSOLUES** ; sous-lot B **3 authentifiées + 2 NON RÉSOLUES**. Total : **6 AUTHENTIFIÉES, dont 2 CORRIGÉES ET AUTHENTIFIÉES, et 4 NON RÉSOLUES**.
- **Notes corrigées** : `30/192/001` (93→5 tokens, retrait de la suite imprimée du verset 11 sur p.2855) ; `30/196/001` (164→142 tokens, retrait de la suite imprimée du verset 6 sur p.2874). **Deux champs `text` seulement**, textes des psaumes, prières et champs de publication intacts.
- **Cas non résolus** : `30/200/003` (note jumelle d'un ancien dossier 063 `30/200/002` non rouvert) ; `30/211/001` (note sous prière p.2953, hors pages du psaume) ; `30/215/004` et `30/215/005` (deux identifiants concurrents pour un seul pied n°1 p.2971).
- **21 pages PDF distinctes** examinées : A 15 pages (2853–2855,2872–2874,2896–2898,2900–2902,2952–2954) ; B 6 pages (2968–2973), sans page répétée. Pièces PNG et layout dans les artefacts A **12576971728**, B **12577911782**.
- **Tests spécialisés** : [#40137448084](https://github.com/ludodulac/Biblaw/actions/runs/40137448084) (A après corrections) SUCCESS, [#40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177) (preuve B initiale) SUCCESS ; gardes Python de concordance, d'unicité et de rattachement. Les Actions de la clôture finale se vérifient aussi sur le dernier HEAD.
- **État CI général initial** : 35/38 SUCCESS, **3 FAILURE antérieurs à la mission** ; noms, runs et causes détaillés en tête de ce registre. La mission ne touche à aucun des workflows généraux ni à l'interface, ne prétend pas avoir rétabli leur état. À comparer avec l'état GitHub des workflows après le commit final.
- **Historique de synchronisation** : le commit GitHub `ae259b8d55082bc91064d5a66627c7ab426b5c47` (« Build thematic source packs for books 1-10 »), survenu après le checkpoint A, a synchronisé les deux seules notes corrigées dans `data/thematic-index/source-packs/book-30/part-001.json` et `part-002.json`. Pas de publication ; modification automatique distincte des commits de construction.
- **Bilan cumulé 064** : **150/192 examinées, 113 authentifiées (dont 4 corrigées), 37 NON RÉSOLUES, 42 restantes**. Les 140 notes des missions précédentes ne sont pas retraitées. Aucun déploiement, fusion ni changement d'interface ; PR #72 **OPEN/DRAFT**. **STOP après 064-15.**
