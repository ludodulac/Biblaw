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

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Preuve PDF original** : 16 pages ciblées **3089–3092, 3111–3115, 3118–3120, 3126–3129**, sans réexaminer d'autres notes, seulement pour le contexte éditorial. Images originales ×2, `*-layout.json`, `note-proof.json`, [GitHub Actions B #40187890311](https://github.com/ludodulac/Biblaw/actions/runs/40187890311) **SUCCESS**, artefact **12597066515**. Relecture visuelle des débuts/fins et de la typographie : texte sous le filet en corps 9 pt, appels au bon verset, numéros imprimés et références réciproques.

| Identifiant | PDF | Verdict | Preuve et délimitation |
|---|---:|---|---|
| `book-31-psalm-201-note-001` | 3090 | **AUTHENTIFIÉE** | Appel¹ au **verset 1** du psaume 201 (« deux ou trois … réunis ») ; note sous filet n°1 **5/5 tokens** « Évangile selon Matthieu 18:20. ». Page canonique et `noteIds` réciproque. Les identifiants 201/002 et 201/003 revendiquent une **autre** page (3092) et un **autre** texte, non examinés ; aucune concurrence avec la note 001. |
| `book-32-psalm-182-note-001` | 3113 | **AUTHENTIFIÉE** | Appel¹ au **verset 39** (« livre de la magie »), note n°1 **97/97 tokens** sur le « livre des génies », du début « L'Archange Ouriel parle » jusqu'à « travail magique. ». P.3113 canonique, `noteIds` réciproque, note imprimée distincte du pied n°1 local p.3114. |
| `book-32-psalm-182-note-002` | 3114–3115 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel local¹ au **verset 49** (« pieds des Esséniens »), p.3114 : pied imprimé n°1 **113 tokens**, du « De tout temps et dans tous les peuples » à « ils se préservent de l'abstraction », **sans point final**. P.3115 : **continuation du même pied sous le filet en 9 pt, sans nouveau marqueur**, de « philosophique et spirituelle, un piège majeur » à « ciel et la terre. », soit **49 tokens supplémentaires**. Texte complet **162 tokens**, sans versets ou prières ajoutés. Les pages 3114 et 3115 sont dans la source du psaume 182 ; `noteIds` réciproque. **Champ `text` complété seulement : 113 → 162 tokens** ; aucun autre champ touché. |
| `book-32-psalm-183-note-001` | 3119 | **AUTHENTIFIÉE** | Appel¹ au **verset 28** (« corde de la Lumière »), pied n°1 sous filet **11/11 tokens** « Il s'agit de la corde de la Ronde des Archanges. ». P.3119 canonique, `noteIds` réciproque, pas de doublon. |
| `book-32-psalm-185-note-001` | 3127 | **AUTHENTIFIÉE** | Appel¹ au **verset 3** (« maison de Dieu »), pied sous filet n°1 **148/148 tokens** depuis « Maison de Dieu » jusqu'à « dédiés à Dieu. ». P.3127 canonique, `noteIds` réciproque. L'autre note 185/002 est sur **3129**, avec un texte différent, et ne concurrence pas ce pied. |

**Bilan B : 5 AUTHENTIFIÉES, dont 1 CORRIGÉE ET AUTHENTIFIÉE, 0 NON RÉSOLUE.** Tous les appels ont été vérifiés sur les captures du PDF original et les limites de note contrôlées.

## Clôture stricte 064-16

- **10/10 notes examinées : 9 AUTHENTIFIÉES dont 1 CORRIGÉE ET AUTHENTIFIÉE ; 1 NON RÉSOLUE** (`31/184/001`, note sous Pr.76, p.3005 hors pages canoniques du psaume).
- **Une seule correction canonique** `32/182/002`, ajout fidèle de 49 tokens imprimés du pied p.3115, 113 → 162 tokens ; aucun psaume ni prière édité, aucun changement de publication.
- **31 pages PDF distinctes examinées**, A 15 et B 16 : p.2986–2988,2993–2995,3004–3006,3027–3029,3033–3035,3089–3092,3111–3115,3118–3120,3126–3129.
- **Actions spécialisées** : garde A [#40188216027](https://github.com/ludodulac/Biblaw/actions/runs/40188216027) **SUCCESS**, garde B [#40188215852](https://github.com/ludodulac/Biblaw/actions/runs/40188215852) **SUCCESS** sur le checkpoint B `f985af2` ; précédentes preuves visuelles A [#40187665402](https://github.com/ludodulac/Biblaw/actions/runs/40187665402) et B [#40187890311](https://github.com/ludodulac/Biblaw/actions/runs/40187890311), artefacts A **12597171008**, B **12597066515**. Les gardes testent les limites, la page, le marqueur et la continuation de p.3115 ; elles ne valident jamais automatiquement une note.
- **CI générale initiale : 37/40 SUCCESS**, trois échecs préexistants nommés et documentés en ouverture ; au checkpoint `f985af2` (avant synchronisation) : trois mêmes échecs, [Audit theme entry identity #40188215891](https://github.com/ludodulac/Biblaw/actions/runs/40188215891), [BIBLAW 058 corpus browse mobile #40188215990](https://github.com/ludodulac/Biblaw/actions/runs/40188215990), [Browser smoke - lexical occurrence expansion #40188215779](https://github.com/ludodulac/Biblaw/actions/runs/40188215779). Aucun de ces trois échecs n’est imputable aux modifications ciblées 064-16. Dernier état spécifique consulté pour `f985af2` : **38 SUCCESS, 3 FAILURE, 1 IN_PROGRESS**, dont A/B SUCCESS. Les résultats seront revérifiés sur la dernière révision.
- **Synchronisation automatique GitHub** : commit séparé `30f60927de1d58631f614d76c703adfd810eb271` « Build thematic source packs for books 1-10 » ; il répercute uniquement le texte corrigé `32/182/002` dans `data/thematic-index/source-packs/book-32/part-001.json`. Les runs du commit automatique ont eu `action_required` (approbation GitHub), et ne doivent donc pas être présentés comme SUCCESS ; les preuves A/B du checkpoint précédent sont explicitement SUCCESS. Pas de changement manuel du catalogue ou de l’interface.
- **Bilan 064 cumulé** : **160/192 examinées ; 122 authentifiées (dont 5 corrigées), 38 NON RÉSOLUES, 32 restant à examiner**. Les 150 notes antérieures n'ont pas été retraitées.
- PR #72 **OPEN/DRAFT**, aucune fusion, publication ou déploiement. **STOP après 064-16.**
