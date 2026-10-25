# 🌸 BIBLAW — MISSION 064-18 — VERDICTS

**Reprise** : dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT ; HEAD d'entrée `0117eeab5ecc70f7ca518de7cc7b8fe6931b2a1e`, vérifié avant toute mutation. Les 170 notes déjà examinées ne sont pas retraitées ; aucun psaume, aucune prière, aucune interface ni publication modifiés.

## Vigilance CI — avant le lot 064-18

Sur le HEAD initial, **41 SUCCESS / 44 runs**, **trois échecs antérieurs** : **Browser smoke - lexical occurrence expansion** [#40192214053](https://github.com/ludodulac/Biblaw/actions/runs/40192214053), assertions héritées `THÈME`/`MOTS` ; **BIBLAW 058 corpus browse mobile** [#40192213932](https://github.com/ludodulac/Biblaw/actions/runs/40192213932), Playwright/Chromium et Ubuntu 26.04 non compatibles ; **Audit theme entry identity** [#40192214244](https://github.com/ludodulac/Biblaw/actions/runs/40192214244), garde antérieure des changements `js/biblaw.js`. Ne pas les réparer hors périmètre. Différencier ces échecs des tests spécialisés 064-18.

## Sous-lot A — CHECKPOINT : 5 notes

**Preuves** : PDF original (4 744 p.), **10 pages** pertinentes seulement : p.3257–3259, 3266–3269, 3313–3315. Capture à 2× et coordonnées de chaque pied : `scripts/prove_notes_064_18_A.py`, `note-proof.json`, `pdf-page-*-layout.json` et images. [GitHub Actions A #40199143472](https://github.com/ludodulac/Biblaw/actions/runs/40199143472) SUCCESS, artefact **12601790662**. Les appels, pieds, textes et frontières ont été lus visuellement, pas seulement par concordance machine.

| ID | PDF | Verdict | Preuve exacte, début/fin, numéro, rattachement, unicité |
|---|---:|---|---|
| `book-33-psalm-228-note-001` | 3258 | **AUTHENTIFIÉE** | Appel¹ au verset **4** (« feu d'apparaître »), unique pied imprimé n°1 sous filet **48/48 tokens**, de « L'Archange fait allusion à un feu » à « manque d'organisation globale. ». P.3258 est canonique du psaume 228, `noteIds` réciproque. Aucun doublon. |
| `book-33-psalm-230-note-001` | 3267 | **AUTHENTIFIÉE** | Appel¹ au verset **6** (« 22 marches »), pied n°1 **51/51 tokens**, du « Il s'agit du site consacré » jusqu'à « haut de sa pyramide. ». P.3267 dans le psaume 230, `noteIds` réciproque, autre note de p.3268 distincte. |
| `book-33-psalm-230-note-002` | 3268–3269 | **NON RÉSOLUE** | Le fichier a **106 tokens**. Le pied unique imprimé sous filet p.3268 est n°1 et **6 tokens** : « Voir les psaumes 225 et 226. ». Les **100 tokens supplémentaires** proviennent du corps du psaume, versets 23–25 p.3269, non de la note. Surtout ce même pied p.3268 est revendiqué par l'identifiant 230/003 ; aucun doublet imprimé. Ne pas modifier l'ancien dossier composite ni inférer une identité. |
| `book-33-psalm-230-note-003` | 3268 | **NON RÉSOLUE** | Texte du fichier **6/6 tokens exacts**, numéro imprimé n°1 au verset **14** (« bons amis¹ ») et page canonique. Cependant **une seule occurrence imprimée** p.3268, aussi revendiquée par 230/002 (même préfixe et même page) ; impossible d'attribuer deux identités uniques. Aucun dédoublonnage ni promotion. |
| `book-33-psalm-243-note-001` | 3314 | **AUTHENTIFIÉE** | Appel¹ au verset **11** (« guerre¹ »), unique pied n°1 **10/10 tokens** « Voir le psaume 216, « Que la guerre ne soit plus ». ». P.3314 canonique du psaume 243 et `noteIds` réciproque. Pas de doublon. |

**Bilan A : 3 AUTHENTIFIÉES, 0 CORRIGÉE, 2 NON RÉSOLUES** (`33/230/002`, `33/230/003`). Les cinq verdicts sont documentés après inspection des images, gardes et tests. Aucune note canonique modifiée.

## Sous-lot B — À FAIRE
Cinq ID du plan seulement : `34/218/001`, `34/218/002`, `34/228/001`, `34/242/001`, `35/209/001`.
