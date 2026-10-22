# BIBLAW — 064-01 — verdicts éditoriaux des dix premières notes

**PR #72 DRAFT.** Dossiers couverts par [064_PLAN.md](064_PLAN.md) (les dix premiers IDs). Les preuves sont issues **des seules pages 70, 82, 105, 119, 150 et 211 du PDF original**, examinées par lecture ciblée des images et du texte typographique. Le workflow [Actions 39751751006](https://github.com/ludodulac/Biblaw/actions/runs/39751751006) a terminé **SUCCESS**, sans modifier aucun fichier canonique ; ses deux artefacts d'audit contiennent les extraits, numéros imprimés, limites, captures de pages et référencements réciproques.

**Règle de validation appliquée :** texte complet (tous les tokens égaux, différences typographiques d'espaces insécables seulement), du premier au dernier mot, appel typographique en 9 pt, numéro imprimé local = marqueur enregistré, page PDF incluse dans les pages du psaume, `psaume.noteIds` réciproque, et aucun texte supplémentaire ni appel imprimé revendiqué deux fois. **Les verdicts restent documentaires** : les fichiers `data/notes/` gardent `validation.status=machine-extracted-needs-review`, aucune promotion au catalogue.

## Sous-lot A — cinq premières notes — AUTHENTIFIÉES

Preuves : artefact **`biblaw-064-01-proof-A`** (ID 12414425817) du [run 39751751006](https://github.com/ludodulac/Biblaw/actions/runs/39751751006), `note-proof.json` et images PDF pages **70, 82, 105**. Lecture visuelle des trois pages : les notes apparaissent isolées sous une règle, imprimées en petite typographie, après le texte du psaume, avec marqueurs et fins de paragraphe clairement délimités. Les trois notes de la p. 70 ont des numéros distincts **1, 2, 3**, sans revendication croisée.

| ID | Page PDF | Verdict | Preuve précise | Correction | Incertitude |
|---|---:|---|---|---|---|
| `book-01-psalm-004-note-001` | 70 | **AUTHENTIFIÉE** | Marqueur imprimé **1**, police **9 pt**, 40/40 mots normalisés identiques à la note complète, `psaume.noteIds` réciproque. Début « Les Esséniens étaient assemblés sur une montagne sacrée. 7 » ; fin « dans les mondes subtils des énergies et forces sacrées. ». | Aucune | **Aucune** : limites, rattachement et unicité confirmés sur l'image p.70. |
| `book-01-psalm-004-note-002` | 70 | **AUTHENTIFIÉE** | Marqueur imprimé **2**, police **9 pt**, 8/8 mots normalisés identiques à la note complète, `psaume.noteIds` réciproque. Début « L’Archange Michaël s’adresse à Olivier Manitara. » ; fin « L’Archange Michaël s’adresse à Olivier Manitara. ». | Aucune | **Aucune** : limites, rattachement et unicité confirmés sur l'image p.70. |
| `book-01-psalm-004-note-003` | 70 | **AUTHENTIFIÉE** | Marqueur imprimé **3**, police **9 pt**, 47/47 mots normalisés identiques à la note complète, `psaume.noteIds` réciproque. Début « À la suite de ce psaume, les Esséniens ont » ; fin « et de recevoir sa bénédiction de génération en génération. ». | Aucune | **Aucune** : limites, rattachement et unicité confirmés sur l'image p.70. |
| `book-01-psalm-010-note-001` | 82 | **AUTHENTIFIÉE** | Marqueur imprimé **1**, police **9 pt**, 11/11 mots normalisés identiques à la note complète, `psaume.noteIds` réciproque. Début « Il s’agit du dernier enseignement de la célébration en » ; fin « s’agit du dernier enseignement de la célébration en cours. ». | Aucune | **Aucune** : limites, rattachement et unicité confirmés sur l'image p.82. |
| `book-02-psalm-003-note-001` | 105 | **AUTHENTIFIÉE** | Marqueur imprimé **1**, police **9 pt**, 120/120 mots normalisés identiques à la note complète, `psaume.noteIds` réciproque. Début « Pour célébrer L’Archange Gabriel, les Esséniens placent sa statue » ; fin « puis l’océan, touchant ainsi toutes les eaux du monde. ». | Aucune | **Aucune** : limites, rattachement et unicité confirmés sur l'image p.105. |

**Résultat du sous-lot A : 5 AUTHENTIFIÉES, 0 corrigée, 0 NON RÉSOLUE.** Aucun fichier de note, texte de psaume, prière ni catalogue modifié. Checkpoint GitHub obligatoire après ce sous-lot.

## Sous-lot B — cinq notes suivantes — À TRAITER

Les cinq identifiants suivants restent en attente de documentation dans ce registre au stade du premier checkpoint : `book-02-psalm-012-note-001`, `book-03-psalm-004-note-001`, `book-04-psalm-012-note-001`, `book-04-psalm-012-note-002`, `book-04-psalm-012-note-003`. Ne pas les déclarer validés sans la vérification distincte du sous-lot B. Artefact de preuve B disponible, mais verdicts **non encore enregistrés** au stade de ce checkpoint.
