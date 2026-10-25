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

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Preuves PDF** : treize pages ciblées **3325–3328, 3376–3378, 3439–3441, 3459–3461**, rendus 2× et coordonnées typographiques via `scripts/prove_notes_064_18_B.py`. [GitHub Actions B #40199469318](https://github.com/ludodulac/Biblaw/actions/runs/40199469318) **SUCCESS**, artefact **12601686392**, `note-proof.json`, captures PNG. Les notes ont été confrontées visuellement aux appels imprimés, au filet séparateur, aux limites de texte et aux pages de psaume.

| ID | PDF | Verdict | Preuve du texte, numéro, rattachement et unicité |
|---|---:|---|---|
| `book-34-psalm-218-note-001` | 3326 | **AUTHENTIFIÉE** | Appel¹ au **verset 1** (« lieu saint … offert¹ »), note **n°1 de 33/33 tokens** de « L'Archange parle de la grande statue » à « pyramide à 22 marches. ». Première des deux notes imprimées sous filet, page canonique du psaume 218 et `noteIds` réciproque. |
| `book-34-psalm-218-note-002` | 3326 | **AUTHENTIFIÉE** | Appel² au **verset 5** (« eau de cette statue² »), pied **n°2 de 82/82 tokens** depuis « À l'époque où l'Archange transmit ce psaume » jusqu'à « à travers les 22 marches. ». Second pied distinct, après le premier et avec son propre numéro ; page du psaume et `noteIds` réciproque. Aucun doublon. |
| `book-34-psalm-228-note-001` | 3377 | **AUTHENTIFIÉE** | Appel¹ au **verset 23** (« baptême de l'âme¹ »), pied unique n°1 **22/22 tokens** de « Il s'agit de la célébration » à « de ce psaume. ». Page canonique du psaume 228, `noteIds` réciproque. |
| `book-34-psalm-242-note-001` | 3440 | **AUTHENTIFIÉE** | Appel¹ au **verset 2** (« buvez-la¹ »), pied unique n°1 **31/31 tokens** de « Cette célébration fut la première » à « baptême essénien. ». Page canonique du psaume 242 et `noteIds` réciproque. |
| `book-35-psalm-209-note-001` | 3460 | **AUTHENTIFIÉE** | Appel¹ au **verset 5** (« dialogue avec l'Ange¹ »), pied n°1 **61/61 tokens**, de « Dans le chemin des formations esséniennes » à « pour les Esséniens. ». Page canonique du psaume 209, `noteIds` réciproque, pas de doublon. |

**Bilan B : 5 AUTHENTIFIÉES, 0 CORRIGÉE, 0 NON RÉSOLUE.** Seules les cinq notes autorisées du sous-lot B ont été jugées.

## Clôture 064-18

- **10/10 notes examinées** : sous-lot A **3 AUTHENTIFIÉES, 2 NON RÉSOLUES** ; sous-lot B **5 AUTHENTIFIÉES, 0 NON RÉSOLUE**. **Total : 8 AUTHENTIFIÉES, 0 CORRIGÉE, 2 NON RÉSOLUES**.
- **Deux cas NON RÉSOLUS :** `33/230/002` (extraction composite du pied + versets du psaume) et `33/230/003` (même pied unique p.3268 revendiqué par deux ID). Aucun dossier historique, source note, psaume ou prière modifié pour déduire une identité.
- **23 pages PDF originales distinctes vérifiées visuellement** : A 10 pages p.3257–3259,3266–3269,3313–3315 ; B 13 pages p.3325–3328,3376–3378,3439–3441,3459–3461.
- **Tests et preuves** : A [#40199370107](https://github.com/ludodulac/Biblaw/actions/runs/40199370107) **SUCCESS** au checkpoint A, artefact **12601790662** ; B [#40199469318](https://github.com/ludodulac/Biblaw/actions/runs/40199469318) **SUCCESS** pour la capture B initiale, artefact **12601686392**. Des gardes assertent les cinq textes, marqueurs, pages et la collision A, mais ne rendent jamais automatiquement les verdicts humains. Derniers tests du HEAD vérifiés séparément.
- **CI générale vérifiée au checkpoint de clôture `3acaf43`** : **43 SUCCESS / 46 runs, 3 FAILURE** — [Audit theme entry identity #40199694199](https://github.com/ludodulac/Biblaw/actions/runs/40199694199), [Browser smoke - lexical occurrence expansion #40199694285](https://github.com/ludodulac/Biblaw/actions/runs/40199694285), [BIBLAW 058 corpus browse mobile #40199694142](https://github.com/ludodulac/Biblaw/actions/runs/40199694142). Ce sont les trois échecs déjà constatés au départ (41 SUCCESS / 44), sans nouvelle régression. Les tests spécialisés au checkpoint sont **A [#40199694215](https://github.com/ludodulac/Biblaw/actions/runs/40199694215) SUCCESS et B [#40199694076](https://github.com/ludodulac/Biblaw/actions/runs/40199694076) SUCCESS**. Aucune réparation CI hors périmètre.
- **Bilan cumulé** : **180/192 notes examinées, 140 AUTHENTIFIÉES (dont 8 corrigées), 40 NON RÉSOLUES et 12 restantes**. Les 170 notes déjà jugées et les trois corrections 064-17 ont été préservées.
- **Protections** : aucun texte source modifié, aucune note publiée, PR #72 OPEN/DRAFT, aucune fusion ni déploiement. **STOP après 064-18.**
