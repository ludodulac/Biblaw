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

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Preuves PDF original** : pages **2756–2758, 2813–2815, 2829–2834** (12 pages). Le script `scripts/prove_notes_064_14_B.py` capture le pied de page original, l'appel, les cadres typographiques et la page voisine en `note-proof.json`, `*-layout.json` et PNG. [GitHub Actions #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792) SUCCESS, artefact `biblaw-064-14-proof-B` **12576942014**. Les limites ont été examinées visuellement avant verdict.

| Identifiant | PDF | Verdict | Preuve et rattachement documentaire | Correction / incertitude |
|---|---:|---|---|---|
| `book-29-psalm-200-note-001` | 2757 | **AUTHENTIFIÉE** | Sous le filet, marqueur imprimé n°1, **45/45 tokens** depuis « Lorsqu'il est dit dans les textes sacrés » jusqu'à « après lui. ». Appel dans le corps du psaume 200 relatif aux « 7 pierres », page incluse dans les pages canoniques 2752–2757 ; `noteIds` réciproque. Aucune concurrence imprimée. | Aucune. |
| `book-29-psalm-212-note-001` | 2814 | **NON RÉSOLUE** | **Un seul pied de page imprimé n°1 de 4 tokens** : « Mot latin signifiant « assemblée ». », renvoyant au mot **ecclesia¹ de la prière Pr.102**, qui suit le psaume. Le fichier JSON comprend **193 tokens**, mêlant ces quatre tokens à **189 tokens de la prière**, typographiquement distincte. La page 2814 est **hors pages canoniques [2810–2813]** du psaume 212. `noteIds` réciproque insuffisant. | Aucune correction : attribution à la prière et extraction composite à réparer sans perte dans une mission distincte. |
| `book-29-psalm-216-note-001` | 2830 | **AUTHENTIFIÉE** | Note imprimée unique n°1 sous filet sur la page d'ouverture, **28/28 tokens** de « Ce psaume fut transmis » à « terre d’Espagne. ». Renvoi local¹ dans l'introduction (« Olivier Manitara dit à l'Archange Michaël¹ »), page canonique du psaume 216 ; `noteIds` réciproque. La note imprimée p.2831 est distincte. | Aucune. |
| `book-29-psalm-216-note-003` | 2831 | **NON RÉSOLUE** | Appel imprimé 1 au verset 11 (« monde divin¹ ») ; un seul pied de page n°1 sur la portée symbolique de l'épée. Le pied contient **78 tokens** tandis que la note 003 en comporte **77** (forme extraite « audelà » au lieu de la graphie imprimée « au-delà », d'où la divergence après 66 tokens comparés). Le dossier historique **`book-29-psalm-216-note-002`**, extrait composite comportant aussi la suite du corps du psaume, revendique **le même pied et le même appel** p.2831. Une seule occurrence imprimée ne justifie pas deux identités 002/003. | Ni correction isolée de graphie ni promotion : conflit d'identifiants 002↔003 non résolu, dossier 063 non rouvert. |
| `book-29-psalm-217-note-001` | 2833 | **AUTHENTIFIÉE** | Appel n°1 au verset 1 du psaume 217, pied imprimé n°1 **151/151 tokens** de « L'Archange fait allusion aux 2 célébrations » jusqu'à « psaume 215. ». Un seul pied complet, page canonique [2833–2834], `noteIds` réciproque, aucun suffixe de corps ou prière. | Aucune. |

**Checkpoint B : 3 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 2 NON RÉSOLUES.** Les deux anomalies restent intactes.

## Bilan de mission 064-14

- **10/10 dossiers examinés** en deux sous-lots : **6 AUTHENTIFIÉES** dont **1 CORRIGÉE ET AUTHENTIFIÉE**, **4 NON RÉSOLUES** (29/199/002, 29/199/003, 29/212/001, 29/216/003).
- **Correction unique de texte** : `book-29-psalm-195-note-001` 67 → **159 tokens**, ajout du pied de page original p.2728, prouvé visuellement et protégé par `scripts/prove_notes_064_14_A.py`. Champ `text` seulement, aucun autre champ modifié ; note toujours non publiée.
- **Pages du PDF original : 26 distinctes**, uniquement p.2722–2724, 2726–2730, 2747–2752 (14 pages A) et p.2756–2758, 2813–2815, 2829–2834 (12 pages B).
- **GitHub Actions** : [#40135038621](https://github.com/ludodulac/Biblaw/actions/runs/40135038621) SUCCESS pour la garde A et la correction ; [#40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792) SUCCESS pour les preuves B. Artefacts A **12576696887**, B **12576942014**. Les scripts ne rendent jamais de verdict éditorial automatiquement.
- **Cumul 064 : 140/192 examinées ; 107 AUTHENTIFIÉES (dont 2 corrigées historiquement), 33 NON RÉSOLUES, 52 restent à examiner.** Les 130 notes antérieures ne sont pas retraitées.
- **Protection** : aucune autre note, aucun psaume ni prière, aucune publication, interface, catalogue ou déploiement modifiés intentionnellement par 064-14. PR #72 reste OPEN/DRAFT, ne pas fusionner. **STOP après 064-14.**
