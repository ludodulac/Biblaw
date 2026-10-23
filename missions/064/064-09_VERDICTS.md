# 🌸 BIBLAW — 064-09 — dix notes à authentifier

**Portée :** dix IDs du lot 064-09 de [064_PLAN.md](064_PLAN.md), branche `feat/052-search-ui`, PR #72 OPEN/DRAFT. Script et workflow de preuve repris de 064-08. [Actions #39957324167](https://github.com/ludodulac/Biblaw/actions/runs/39957324167) **SUCCESS**, deux artefacts indépendants `biblaw-064-09-proof-A` (**12503002405**) et `biblaw-064-09-proof-B` (**12503326714**). Sources : images PDF originales, `*-layout.json` et `note-proof.json`.

**Pages PDF ciblées uniquement :** 1383, 1407, 1413, 1445, 1487, 1488, 1518, 1554, 1577, 1579, 1618, 1619 et 1620. Les pages ont été lues visuellement ; les mesures automatiques ne suffisent pas à authentifier. Pour chaque note, contrôle de l’appel imprimé, des limites, de l’unicité et du psaume.

## Sous-lot A — 5 notes — checkpoint GitHub

Artefact **A 12503002405** ; pages inspectées **1383, 1407, 1413, 1445, 1487, 1488**. Les quatre premiers pieds de page sont authentiques et complets. Le cinquième fichier fusionne une véritable note de huit tokens avec la prière indépendante **Pr. 7** de la page suivante : il ne peut être authentifié dans cet état.

| Identifiant | PDF | Verdict | Preuve précise | Correction | Incertitude |
|---|---|---|---|---|---|
| `book-19-psalm-113-note-001` | 1383 | **AUTHENTIFIÉE** | Note 1 sous filet p.1383, 27 tokens exactement, début/fin propres, renvoi à la Table d’émeraude ; unique appel du psaume 113. `noteIds` réciproque, page source du psaume ; 27/27 tokens égaux du début à la fin. | Aucune | Aucune. |
| `book-19-psalm-118-note-001` | 1407 | **AUTHENTIFIÉE** | Note 1 sous filet p.1407, 34 tokens exactement sur les livres « magiques », sans reprise ni doublon du psaume 118. `noteIds` réciproque, page source du psaume ; 34/34 tokens égaux du début à la fin. | Aucune | Aucune. |
| `book-19-psalm-119-note-001` | 1413 | **AUTHENTIFIÉE** | Note imprimée 1 sous filet p.1413, 41 tokens exactement sur les quatre éléments et les quatre Sceaux ; rattachement au psaume 119 prouvé. `noteIds` réciproque, page source du psaume ; 41/41 tokens égaux du début à la fin. | Aucune | Aucune. |
| `book-19-psalm-126-note-001` | 1445 | **AUTHENTIFIÉE** | Note 1 imprimée p.1445, 23 tokens exactement sur les célébrations de Raphaël et d’Ouriel ; pied de page autonome. `noteIds` réciproque, page source du psaume ; 23/23 tokens égaux du début à la fin. | Aucune | Aucune. |
| `book-20-psalm-110-note-001` | 1487–1488 | **NON RÉSOLUE** | Note imprimée 1 p.1487 = **8 tokens** (« Il s’agit du Nom de la Mère. »), mais le JSON comporte **349 tokens** en y copiant la **prière 7 « Pr. 7. Ouriel… Amin. » imprimée comme prière autonome p.1488**. Limite de note non respectée, contamination prouvée. Aucun découpage entrepris. `noteIds` réciproque, page source du psaume ; préfixe exact mais suffixe de prière étrangère. | Aucune | Séparer et rattacher la prière 7 dans une mission spécifique avant correction ; préserver le JSON actuel. |

**A : 4 AUTHENTIFIÉES, 0 CORRIGÉE ET AUTHENTIFIÉE, 1 NON RÉSOLUE.** Ne pas supprimer la prière concaténée ni modifier la note composite dans cette mission ; une correction exige un rattachement et la conservation complète de provenance.

## Sous-lot B — 5 notes — PAS ENCORE CONSIGNÉ

Les identifiants réservés sont `book-20-psalm-117-note-001` (p.1518), `book-20-psalm-124-note-001` (p.1554), `book-20-psalm-129-note-001` (p.1577), `book-20-psalm-129-note-002` (p.1579), et `book-21-psalm-137-note-001` (p.1619). Preuves B déjà disponibles dans **12503326714**, pages 1518,1554,1577,1579,1618–1620. Aucun verdict B n’est inclus au checkpoint A.
