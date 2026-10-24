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

## Sous-lot B — À FAIRE (cinq notes)

Seulement `book-30-psalm-215-note-001`, `002`, `003`, `004`, `005`. Pas de reprise des cas précédents.
