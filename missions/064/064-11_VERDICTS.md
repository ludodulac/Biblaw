# 🌸 BIBLAW — MISSION 064-11 — dix notes et preuves PDF

**Périmètre strict** : lot 064-11 du [plan 064](064_PLAN.md) ; branche `feat/052-search-ui`, PR #72 OPEN/DRAFT. Réemploi sans refonte de `prove_notes_064_10.py`, adapté en `scripts/prove_notes_064_11.py`. Le workflow [GitHub Actions #39967539345](https://github.com/ludodulac/Biblaw/actions/runs/39967539345) **SUCCESS** a conservé les deux séries de preuves : `biblaw-064-11-proof-A` (**12506424572**) et `biblaw-064-11-proof-B` (**12507282337**). Chaque artefact contient `note-proof.json`, les images du PDF original et les relevés `*-layout.json`.

**Méthode éditoriale** : source 060 et scores lexicaux uniquement indicatifs ; chaque note a été contrôlée par lecture de l’image PDF, avec délimitation des pieds de page, appels imprimés, rattachement au psaume, unicité et absence de parasite. Pages PDF autorisées et utilisées : **1785, 1875–1878, 1896, 1914, 1929, 1934–1937, 1959–1961** (15 pages).

## Sous-lot A — cinq notes, checkpoint GitHub

**Preuves A** (ID 12506424572) : captures p.**1785,1875,1876,1877,1878,1896,1914,1929**. La page 1876 démontre qu’une note imprimée complète a reçu dans son fichier JSON **un morceau du texte versifié imprimé page 1877**. La note est laissée NON RÉSOLUE car le verset 21 dans le fichier protégé du psaume 155 est lui-même tronqué en fin de p.1876 ; il faut garantir qu’aucun texte ne soit perdu avant une correction de la note.

| Identifiant | Page(s) PDF | Verdict | Preuve exacte des limites, numéros, texte et psaume | Correction | Incertitude restante |
|---|---|---|---|---|---|
| `book-22-psalm-139-note-001` | 1785 | **AUTHENTIFIÉE** | P.1785 : un pied de page n°1 de **12/12 tokens**, du début « L’Archange parle » à la fin « cercles d’étude ». Note unique sous filet, appel du psaume 139 et lien `noteIds` confirmés. | Aucune | Aucune. |
| `book-22-psalm-155-note-001` | 1876–1877 | **NON RÉSOLUE** | P.1876 : la note imprimée n°1 compte **231 tokens** et s’achève clairement à « sur toute la terre. ». Le JSON comporte **253 tokens** et ajoute « mort. Ainsi, ils n’entrent pas seulement... C’est la grande bénédiction. » (**22 tokens**), qui sont la **continuation du verset 21** du corps du psaume, en haut de la p.1877, et non une suite du pied de page. Le verset 21 du fichier psaume s'arrête actuellement à « après la » ; tronquer ici la note ferait perdre une copie du fragment tant que le psaume protégé ne peut être réparé. | Aucune | Réparer la continuité du verset 21, puis découper la note avec provenance conservée, dans une mission distincte. Aucune correction ici. |
| `book-22-psalm-159-note-001` | 1896 | **AUTHENTIFIÉE** | P.1896 : un pied de page imprimé n°1 de **15/15 tokens** (« 22 commandements » ; « psaume 114 »), limité au bas de la page du psaume 159. Marqueur et lien réciproque confirmés. | Aucune | Aucune. |
| `book-22-psalm-163-note-001` | 1914 | **AUTHENTIFIÉE** | P.1914 : longue note imprimée n°1 **199/199 tokens**, depuis « Une année d’Archange commence » jusqu’à « il a renouvelé l’Alliance. ». Pied de page imprimé en 9 pt d’un seul tenant, pas de texte parasite ; page d’ouverture du psaume 163 et renvoi propres. | Aucune | Aucune. |
| `book-23-psalm-128-note-001` | 1929 | **AUTHENTIFIÉE** | P.1929 : un seul pied de page imprimé n°1 de **53/53 tokens** sur les « 4 chemins fondamentaux » et les « 4 nobles vérités », limites et numéro propres. Rattachement au psaume 128 confirmé, malgré le statut technique machine `source-boundary-audited`. | Aucune | Aucune. |

**Checkpoint A : 4 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 1 NON RÉSOLUE.** Aucun texte source modifié ; note 155 conservée intacte. Les quatre autres notes sont distinctes, ont des textes complets, leurs marqueurs imprimés et leurs `noteIds` réciproques.

## Sous-lot B — cinq notes, EN ATTENTE DU SECOND CHECKPOINT

Dossiers réservés : `book-23-psalm-129-note-001` et `-002` p.1935 ; `book-23-psalm-129-note-003` et `-004` p.1936 ; `book-23-psalm-133-note-004` p.1960. Preuves B déjà conservées dans l’artefact **12507282337**, pages **1934,1935,1936,1937,1959,1960,1961**. **Aucun verdict B n’est encore consigné dans le checkpoint A.**
