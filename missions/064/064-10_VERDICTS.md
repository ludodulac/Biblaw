# 🌸 BIBLAW — 064-10 — Dix verdicts documentaires

**Périmètre strict** : dix notes du [plan 064](064_PLAN.md), lot 064-10, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT. Réemploi du script `scripts/prove_notes_064_10.py` et du workflow précédent sans refonte. [GitHub Actions #39964677882](https://github.com/ludodulac/Biblaw/actions/runs/39964677882) **SUCCESS**, artefacts séparés `biblaw-064-10-proof-A` (**12506082816**) et `biblaw-064-10-proof-B` (**12505982988**) : images du PDF original, `note-proof.json`, `*-layout.json`.

**Méthode** : examiner les appels imprimés, débuts/fins, unicité, pages du psaume et présence de texte parasite ; **identité machine ≠ verdict**. Pages ciblées : **1652–1655, 1684, 1691–1692, 1726, 1746–1748, 1753, 1759, 1766 et 1769** (15 pages). Les notes déjà validées ou laissées non résolues au cours des lots antérieurs n'ont pas été retraitées.

## Sous-lot A — cinq premières notes — checkpoint GitHub

**Preuves** : artefact A **12506082816**, pages **1652, 1653, 1654, 1655, 1684, 1691, 1692 et 1726**, toutes consultées visuellement. Deux notes imprimées en p.1654 relèvent de la **prière Pr.38**, qui suit le psaume 143 sur la page 1653. Le fichier 143/004 amalgame les deux notes imprimées, dont la seconde est également présente dans 143/003. Sur p.1692, un renvoi biblique de deux tokens est suivi par erreur de la suite d'un verset dans le JSON. Aucun de ces cas n'autorise une authentification au seul score automatique.

| Identifiant | Page PDF | Verdict | Preuve précise | Correction | Incertitude restante |
|---|---:|---|---|---|---|
| `book-21-psalm-143-note-003` | 1654 (voir aussi p.1654) | **NON RÉSOLUE** | P.1654, la note imprimée locale **2** a bien 83/83 tokens identiques. Mais elle annote la **prière Pr.38**, commencée p.1653, après la fin du psaume 143. La p.1654 est absente de `psalm-143.source.pdfPages=[1652,1653]` ; rattachement actuel au psaume **non prouvé**. | Aucune | Déterminer rattachement à la prière 38 et résoudre identité avec l'extraction composite 004 ; ne pas déplacer ni supprimer sans mission dédiée. |
| `book-21-psalm-143-note-004` | 1653 (voir aussi p.1654) | **NON RÉSOLUE** | L'extraction PDF déclarée p.1653 contient **169 tokens** : elle reproduit la note imprimée **1 (85 tokens) de p.1654** puis le séparateur « 2 - » et le texte complet de la note imprimée **2 (83 tokens)**, déjà représentée par l'ID 003. P.1653 contient une **autre fin de note sous filet**, pas cette note 1. Texte composite de deux pieds de page sous la **prière Pr.38** ; aucune preuve d'une note 004 autonome. | Aucune | Séparer les appels 1 et 2 de p.1654 et attribuer leur support de prière ; conserver toute la provenance. |
| `book-21-psalm-149-note-001` | 1684 | **AUTHENTIFIÉE** | P.1684, unique note **1** sous filet du psaume 149 : baptême essénien lors de la célébration de Gabriel, **66/66 tokens** exacts du premier au dernier mot, sans parasite ; page dans le psaume, noteIds réciproque. | Aucune | Aucune. |
| `book-21-psalm-150-note-002` | 1692 | **NON RÉSOLUE** | P.1692, la note imprimée **2** contient seulement « **Exode 32.** » (**2 tokens**). Le JSON de **30 tokens** poursuit avec « commandements. Mais en l’absence... », fragment du texte principal du psaume (v.32, poursuivi sur la page suivante). Note composite contaminée par du texte versifié, non authentifiable telle quelle. | Aucune | Distinguer les deux tokens de pied de page du corps du psaume et garantir l'intégrité des versets avant toute correction. |
| `book-21-psalm-157-note-001` | 1726 | **AUTHENTIFIÉE** | P.1726, unique note locale **1** de **13/13 tokens** (« premier message donné ... en Haïti »), intégrale sous le filet du psaume 157 ; appel et rattachement confirmés. | Aucune | Aucune. |

**Checkpoint A : 2 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 3 NON RÉSOLUES.** Aucune note, aucun psaume, aucune prière ni aucun catalogue modifié ; résolution des rattachements et des découpages différée. Les anomalies des lots antérieurs demeurent inchangées.

## Sous-lot B — cinq notes suivantes — NON ENCORE CONSIGNÉ

Restent : `book-21-psalm-160-note-001` (p.1747), `book-21-psalm-161-note-001` (p.1753), `book-21-psalm-162-note-001` (p.1759), `book-21-psalm-163-note-001` (p.1766), `book-21-psalm-164-note-001` (p.1769). Artefact B **12505982988**, PDF p.**1746–1748, 1753, 1759, 1766, 1769**. Aucun verdict B n'est enregistré dans ce checkpoint.
