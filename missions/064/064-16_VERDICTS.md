# 🌸 BIBLAW — MISSION 064-16 — verdicts éditoriaux et preuves

**Reprise vérifiée** : HEAD initial `4f0019b909f577a1b94e0953837d47fc0ee9c44d`, branche `feat/052-search-ui`, PR #72 **OPEN/DRAFT**. Le périmètre est celui des dix notes listées par `missions/064/064_PLAN.md`, sans retraiter les 150 déjà examinées ni leurs anomalies. Aucune édition des psaumes, prières, notes antérieures, interface ou publication.

## État CI au début de 064-16

Au HEAD initial, **40 runs PR : 37 SUCCESS, 3 FAILURE**, tous trois déjà présents en 064-15 :

- **Audit theme entry identity**, [#40137858346](https://github.com/ludodulac/Biblaw/actions/runs/40137858346) : protection `Unreviewed js/biblaw.js changes; thematic search remains protected` (PR DRAFT/interface antérieure).
- **Browser smoke - lexical occurrence expansion**, [#40137858364](https://github.com/ludodulac/Biblaw/actions/runs/40137858364) : assertion ancienne des balises `>THÈME</button>` et `>MOTS</button>` (`audit_lexical_expansion_041c.py`).
- **BIBLAW 058 corpus browse mobile**, [#40137858409](https://github.com/ludodulac/Biblaw/actions/runs/40137858409) : Playwright 1.55 ne prend pas en charge Chromium sur `ubuntu26.04-x64` dans ce runner.

Ces échecs généraux sont antérieurs à 064-16 et ne sont pas réparés ; on distingue leurs runs des deux tests PDF spécialisés.

## Sous-lot A — CHECKPOINT (cinq notes)

Preuve PDF originale ciblée : **15 pages** 2986–2988, 2993–2995, 3004–3006, 3027–3029, 3033–3035, obtenues en images ×2 avec positions du texte, numéros et pieds depuis `scripts/prove_notes_064_16_A.py`. Action [#40187665402](https://github.com/ludodulac/Biblaw/actions/runs/40187665402) **SUCCESS**, artefact `biblaw-064-16-proof-A` (**12597171008**) et `note-proof.json`. Les appels ont été examinés sur les images, non inférés du seul rapprochement lexical.

| Identifiant | PDF | Verdict | Vérification du pied, de l'appel, du psaume et de l'unicité |
|---|---:|---|---|
| `book-31-psalm-181-note-001` | 2987 | **AUTHENTIFIÉE** | Note n°1 sous filet **34/34 tokens**, depuis « Ailé » jusqu'à « grandeur d'âme… ». Appel¹ au **verset 2** (« Ange ailé ») du psaume 181 ; PDF p.2987 inclus dans les pages canoniques ; `noteIds` réciproque, aucun doublon. |
| `book-31-psalm-182-note-001` | 2994 | **AUTHENTIFIÉE** | Note imprimée n°1 **42/42 tokens**, du « L'Archange Raphaël fait référence » jusqu'à « Ronde des Archanges. ». Appel¹ au **verset 22** sur « enlever un défaut », page canonique du psaume 182, `noteIds` réciproque, pas d'autre note concurrente. |
| `book-31-psalm-184-note-001` | 3005 | **NON RÉSOLUE** | Pied imprimé n°1 de **71/71 tokens**, du « Il ne s'agit pas de nouveaux Dieux » à « avec Mani. ». **L'appel¹ est dans la prière Pr.76**, p.3005 (« la nouvelle génération des dieux¹ ») après la fin du psaume 184 ; p.3005 est hors pages canoniques **[3002–3004]**. `noteIds` réciproque ne démontre pas un rattachement à un verset du psaume. Aucun changement de prière ou de note. |
| `book-31-psalm-189-note-001` | 3028 | **AUTHENTIFIÉE** | Pied n°1 de **60/60 tokens** de « En entrant dans la Ronde des Archanges » à « etc. » ; appel¹ au **verset 20** (« prêtrise supérieure »), p.3028 canonique et `noteIds` réciproque ; pas de rival imprimé. |
| `book-31-psalm-190-note-001` | 3034 | **AUTHENTIFIÉE** | Pied n°1 **4/4 tokens** « Genèse 6:1-4. » ; appel¹ au **verset 33** sur « enfants au monde », p.3034 canonique, `noteIds` réciproque et une seule occurrence. |

**Bilan A : 4 AUTHENTIFIÉES, 0 CORRIGÉE, 1 NON RÉSOLUE** ; aucune modification de données canoniques. Les cinq verdicts et les preuves sont consignés à ce checkpoint avant B.

## Sous-lot B — À FAIRE
Cinq notes exclusivement : `31/201/001`, `32/182/001`, `32/182/002`, `32/183/001`, `32/185/001`.
