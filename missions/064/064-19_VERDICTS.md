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

## Sous-lot B — clôture, 5 notes

**Preuves visuelles PDF original** : 15 pages d'inspection p.3494–3496,3511–3513,3529–3531,3651–3653,3689–3691 ; 3 pages p.3494–3496 déjà examinées dans A, donc **24 pages distinctes dans la mission**. Captures à 2×, métriques typographiques, `note-proof.json` et layouts. [GitHub Actions preuve B #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034) SUCCESS, artefact **12651183390**. La relecture visuelle a précédé chaque verdict.

| Identifiant | PDF | Verdict | Rattachement, début/fin, marqueur, concurrence |
|---|---:|---|---|
| `book-35-psalm-218-note-003` | 3495 | **NON RÉSOLUE** | Fichier de **45/45 tokens**, correspondant exactement au seul pied n°1 imprimé de la page, sur « l'enfant » au verset 20 ; pourtant `218/002` du sous-lot A revendique **exactement la même page, le même pied et le même texte**. Deux ID pour une occurrence ; ne pas supprimer, fusionner ni choisir par supposition. |
| `book-35-psalm-223-note-001` | 3512 | **AUTHENTIFIÉE** | Renvoi¹ au **verset 5** (« constitution d'une église »), pied n°1 de **39/39 tokens**, de « Le nom officiel de cette église » à « nouvelle manifestation de Dieu ». La page est canonique, `noteIds` réciproque, aucune identité concurrente. |
| `book-35-psalm-227-note-001` | 3530 | **AUTHENTIFIÉE** | Renvoi¹ au **verset 27** (« enfanter dans la douleur »), pied imprimé n°1 de **17/17 tokens**, « Voir le psaume 102 de l'Archange Gabriel » à « à la splendeur ». Page canonique, `noteIds` réciproque, aucun doublon. |
| `book-36-psalm-233-note-002` | 3651–3652 | **CORRIGÉE ET AUTHENTIFIÉE** | Pied n°1 page 3652 **122/122 tokens**, « L'Archange Ouriel parle ici du premier travail magique » jusqu'à « paroles sacrés. ». Sur **p.3652**, le renvoi¹ est imprimé après « votre vie », à la **fin du verset 16** commencé sur p.3651. Le fichier associait à tort le pied au **verset 13**, dont le renvoi¹ p.3651 a son **propre pied distinct** expliquant l'initiation des Fils du Soleil. La correction documentaire est **uniquement `appliesTo.verse: 13→16`** : texte de 122 tokens intact, page/numéro/identifiant inchangés, `noteIds` réciproque. Aucun psaume ni prière modifié. |
| `book-37-psalm-250-note-003` | 3690 | **NON RÉSOLUE** | Renvoi¹ sur la question qui précède le verset 37 (« statue ») ; pied physique unique n°1 **80/80 tokens**, du « Il s'agit d'une statue représentant » jusqu'à « ait la sienne. ». Mais le dossier antérieur non résolu `37/250/002` revendique **la même page et le préfixe exact de 80 tokens** suivi de versets et de texte de prière (extraction composite). De plus `appliesTo.verse=11` du candidat ne correspond pas à la position du renvoi imprimé p.3690 ; double incertitude. Ne pas retoucher le dossier historique ni promouvoir `003`. |

**Bilan B : 3 AUTHENTIFIÉES, dont 1 CORRIGÉE ; 2 NON RÉSOLUES.** Seuls les cinq identifiants autorisés ont été examinés.

## Clôture de la mission 064-19

- **10/10 examinées** : A **1 AUTHENTIFIÉE dont 1 corrigée, 4 NON RÉSOLUES** ; B **3 AUTHENTIFIÉES dont 1 corrigée, 2 NON RÉSOLUES**. **Total 4 AUTHENTIFIÉES, 2 CORRIGÉES ET AUTHENTIFIÉES, 6 NON RÉSOLUES**.
- Les deux **corrections prouvées** : `35/214/001` texte composite **113→96 tokens** (suite du psaume exclue) ; `36/233/002` **`appliesTo.verse=13→16`**, sans modification du texte imprimé de 122 tokens.
- Les six cas **NON RÉSOLUS** : `35/213/002`, `35/213/003`, `35/215/001`, `35/218/002`, `35/218/003`, `37/250/003`. Duplications physiques, textes composites ou rattachements concurrents. Aucun dossier des 180 notes précédentes n'est rouvert.
- **24 pages PDF originales distinctes** contrôlées visuellement : A 12 pages ; B 15 dont 3 communes. Preuves techniques et captures archivées A artefact **12650754088**, B **12651183390**.
- **Actions spécialisées initiales** : A [#40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) SUCCESS ; B [#40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034) SUCCESS. Gardes renforcés des candidats et de la correction de rattachement au verset 16, pour exécution au HEAD de clôture.
- **CI générale d'entrée** : 43 SUCCESS / 46, trois échecs préexistants nommés en tête de rapport. Aucun correctif hors périmètre ni changement d'interface. La CI de clôture est vérifiée après push final, sans jamais prétendre que tout est vert.
- **Synchronisation automatique** : commit `8effc49f52fcbf9abcfde4045dbba3e413e1fa58` « Build thematic source packs for books 1-10 » après A : unique mise à jour du texte corrigé `35/214/001` dans `data/thematic-index/source-packs/book-35/part-003.json`, distinct des commits de construction, sans publication. Toute synchronisation complémentaire de l'index reste automatique, non modifiée manuellement.
- **Cumul** : **190/192 examinées — 144 AUTHENTIFIÉES (dont 10 corrigées), 46 NON RÉSOLUES, 2 restantes** ; ces deux notes appartiennent **uniquement à 064-20**, hors mission.
- PR #72 **OPEN/DRAFT**, sans fusion, déploiement, publication, modification de psaume ou de prière. **STOP après 064-19.**
