# BIBLAW — 064-19 — Authentification éditoriale des dix notes

**Reprise autorisée** : dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT. HEAD d'entrée vérifié `db7cbddeedc3acf7ae55d057a2a04ee489c4abe0`. Lot strictement défini dans [064_PLAN.md](064_PLAN.md). Aucune des 180 notes historiques, notamment `33/230/002` et `33/230/003`, n'est retraitée. Ni publication, ni modification d'interface, ni merge, ni déploiement.

## État CI avant 064-19

**46 runs**, **43 SUCCESS, 3 FAILURE**, établis au HEAD d'entrée, avant toute modification :
- [BIBLAW 058 corpus browse mobile #40199832118](https://github.com/ludodulac/Biblaw/actions/runs/40199832118) : Playwright 1.55 et Chromium non compatibles avec Ubuntu 26.04.
- [Browser smoke - lexical occurrence expansion #40199832067](https://github.com/ludodulac/Biblaw/actions/runs/40199832067) : test d'ancien contrat de balisage `THÈME`/`MOTS`.
- [Audit theme entry identity #40199832031](https://github.com/ludodulac/Biblaw/actions/runs/40199832031) : garde de modifications historiques `js/biblaw.js`.
Ces échecs sont **préexistants**, hors périmètre ; ils ne seront pas réparés. Les tests de preuve PDF sont séparés de la CI générale.

## Sous-lot A — checkpoint, 5 notes

**PDF source** : 12 pages distinctes p.3477–3479,3480–3482,3484–3486,3494–3496. Captures originales ×2, positions, tailles de police et relevés `note-proof.json` fournis par `scripts/prove_notes_064_19_A.py`. Action [#40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) **SUCCESS**, artefact **12650754088**. Jugement rendu après examen des images, non par le seul test de concordance.

| Identifiant | PDF | Verdict | Lecture éditoriale de l'original |
|---|---:|---|---|
| `book-35-psalm-213-note-002` | 3479 | **NON RÉSOLUE** | Appel imprimé ¹ au **verset 19** (réconciliation), pied **n°1 de 55 tokens**, de « Les nombreux rituels donnés » à « rituel du désenvoûtement. ». Fichier **455 tokens**, contenant après ces 55 tokens une longue continuation de la **prière Pr.102** débutant sur p.3479. `213/003` revendique le **même unique pied** sur la même page et le même texte composite ; identité concurrente. Page canonique, `noteIds` réciproque mais insuffisant. Aucun changement. |
| `book-35-psalm-213-note-003` | 3479 | **NON RÉSOLUE** | Le même texte de 455 tokens et le même pied n°1 de **55 tokens** que `213/002`. Le champ `appliesTo.verse=19` désigne bien le seul appel, mais ne démontre pas une seconde note imprimée. Ni fusion, ni correction arbitraire des deux IDs. |
| `book-35-psalm-214-note-001` | 3481–3482 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel¹ au **verset 1** (« hommes étaient ivres ») du psaume 214. Pied n°1 sous filet **96 tokens**, depuis « Jésus a dit » jusqu'à « (Évangile selon Thomas, logion 28) ». L'extraction initiale avait **113 tokens** : **17 tokens excédentaires** sont la suite du **corps du psaume** (verset de p.3482 : « en la dilapidant… »), pas le pied. Correction démontrée du seul champ `text` : **113→96 tokens**. Page canonique et `noteIds` réciproque ; pas d'identité concurrente pour ce pied. |
| `book-35-psalm-215-note-001` | 3485 | **NON RÉSOLUE** | Appel¹ au **verset 36** (loi des affinités) et pied n°1 de **24/24 tokens**, correspondant exactement au texte enregistré, mais `book-35-psalm-214-note-002`, dossier historique hors périmètre, revendique également **la même page, le même pied et le même texte**. Une seule occurrence physique : rattachement/identité concurrents, non arbitrés ici. |
| `book-35-psalm-218-note-002` | 3495 | **NON RÉSOLUE** | Appel¹ au **verset 20** (« enfant »), pied n°1 **45/45 tokens** exactement, mais `book-35-psalm-218-note-003` revendique exactement le même pied imprimé, même page et même contenu. Impossible de valider deux identifiants pour un seul pied ; aucune modification. |

**Bilan A : 1 AUTHENTIFIÉE (dont 1 CORRIGÉE), 4 NON RÉSOLUES.** Une seule propriété canonique `text` modifiée, pour `35/214/001`. Les psaumes, prières et autres notes restent inchangés.

## Sous-lot B — À FAIRE

Uniquement `35/218/003`, `35/223/001`, `35/227/001`, `36/233/002`, `37/250/003`.
