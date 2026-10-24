# 🌸 BIBLAW — MISSION 064-14 — examen documentaire de dix notes

**Reprise** : HEAD `0a2c9df1a4af22171ad101e2551e1bf36f26fea7`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT. Uniquement les 10 notes prévues par [064_PLAN.md](064_PLAN.md) ; 130 notes précédentes et les anomalies 064-13 laissées intactes. Aucune publication ni fusion.

## Sous-lot A — cinq notes — CHECKPOINT

**Preuves PDF original** : pages **2722–2724, 2726–2730, 2747–2752** (14 pages), captures haute résolution, `note-proof.json`, relevés typographiques `*-layout.json` via `scripts/prove_notes_064_14_A.py`. [GitHub Actions #40134783488](https://github.com/ludodulac/Biblaw/actions/runs/40134783488), artefact **12576696887**, `biblaw-064-14-proof-A`. La délimitation des pieds, l'appel imprimé, les pages canoniques, et les sections de prière sont jugés à partir des images du PDF ; la concordance machine seule ne vaut pas verdict.

| Identifiant | Page PDF | Verdict | Preuve des limites, marqueur, rattachement et unicité | Correction/incertitude |
|---|---:|---|---|---|
| `book-29-psalm-194-note-001` | 2723 | **AUTHENTIFIÉE** | Note en pied sous filet n°1, **5/5 tokens** « Évangile selon Matthieu 7:20. » ; appel 1 au verset 17 du psaume 194, page 2723 dans le psaume et `noteIds` réciproque. Aucun doublon local. | Aucune. |
| `book-29-psalm-195-note-001` | 2727–2728 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel 1 après « je vous bénis » au verset 6 du psaume 195 ; note n°1 sous filet p.2727 **67 tokens**, qui s'achève matériellement au bas de la page par « Or, la loi québécoise exige que ». La même note se poursuit **sans nouveau marqueur, en corps 9 pt sous le filet p.2728** : « tout cimetière soit associé » jusqu'à « la Lumière sur la terre. » (**92 tokens**). La continuation est distincte des versets 7–15 dans le corps de p.2728. Note complète **159 tokens**, comparée aux images et au relevé de position. Page et `noteIds` réciproques, aucun second appel concurrent. | **Correction démontrée** : ajout exact des 92 tokens imprimés sur p.2728 au champ `text` uniquement ; source, identité, rattachement, validation technique et publication inchangés. |
| `book-29-psalm-199-note-001` | 2748 | **AUTHENTIFIÉE** | Appel 1 du psaume 199 et note unique sous filet n°1 de **8/8 tokens**, « L'Archange s'adresse ici à Olivier Manitara. » ; p.2748 appartient au psaume, `noteIds` réciproque, texte distinct du candidat de la prière Pr.90. | Aucune. |
| `book-29-psalm-199-note-002` | 2751 | **NON RÉSOLUE** | Sous filet p.2751, note imprimée n°1 **17/17 tokens** (« L'étude, la dévotion, le rite et l'œuvre... »), mais appel 1 dans la **prière Pr.90**, commencée p.2750. P.2751 **hors pages canoniques 2745–2750** du psaume 199 ; le texte est aussi porté par l'ID candidat 199/003. | Rattachement à prière et collision d'identifiants non résolus ; ne rien modifier. |
| `book-29-psalm-199-note-003` | 2750–2751 | **NON RÉSOLUE** | Le fichier 003 revendique p.2750 et **les mêmes 17 tokens** que 002, mais **aucun pied de page** ne figure sur p.2750 ; le pied unique se situe p.2751 sous Pr.90. Aucun second appel distinct ne prouve une identité autonome 003. | Identité 002/003 concurrente, source PDF de 003 décalée ; aucun dédoublonnage, aucune correction. |

**Checkpoint A : 3 authentifiées dont 1 corrigée, 2 NON RÉSOLUES ; 5/5 examinées.** Les deux anomalies de 199 sont préservées. Aucune modification de psaume, prière, interface, catalogue ou publication.

## Sous-lot B — NON COMMENCÉ
Seulement `29/200/001`, `29/212/001`, `29/216/001`, `29/216/003`, `29/217/001`.
