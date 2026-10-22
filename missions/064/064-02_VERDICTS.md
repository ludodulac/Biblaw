# BIBLAW — 064-02 — verdicts des notes 11 à 20 du plan

**Dépôt** : `ludodulac/Biblaw` ; branche `feat/052-search-ui` ; PR #72 OPEN/DRAFT.  
**Travail en deux sous-lots de 5, sans retoucher 064-01.** Réutilisation du protocole `prove_notes_064_01.py` dans `prove_notes_064_02.py`, même capture PDF et comparaison typographique ; uniquement les pages source **268, 314, 318, 325, 334, 357, 369 et 378** (8 pages). [Workflow GitHub Actions #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216) **SUCCESS**, deux artefacts de preuves `biblaw-064-02-proof-A` et `biblaw-064-02-proof-B`.

La similitude automatique du rapport 060 n'est pas tenue pour validation : toutes les pages PDF pertinentes ont été inspectées visuellement, y compris les marqueurs et limites de bas de page, puis croisées avec les enregistrements JSON et la réciprocité des `noteIds`.

## Sous-lot A — notes 1 à 5 — checkpoint enregistré

Preuves conservées dans l'artefact **`biblaw-064-02-proof-A`** (GitHub Actions, ID **12426161529**) : `note-proof.json`, rendus PDF p.268, 314, 318, 325 et leurs `*-layout.json`. Les notes 1 à 3 ont chacune un appel distinct sur une page qui appartient au psaume. La page 325 ne présente qu'une **seule note imprimée n°1** (fin du psaume 40), bien qu'elle soit revendiquée par deux JSON entièrement identiques.

| Identifiant | Page PDF | Verdict éditorial | Preuve précise | Correction | Incertitude résiduelle |
|---|---:|---|---|---|---|
| `book-05-psalm-035-note-001` | 268 | **AUTHENTIFIÉE** | PDF p. 268 : note imprimée n° 1, corps 9 pt, 62/62 mots concordants du début (« C’est la première fois que les Archanges mentionnent la ») à la fin (« fait lors de cette célébration et des 3 suivantes. »). Appel dans le psaume et `psaume.noteIds` réciproque, limites visibles. | Aucune | Aucune après contrôle ciblé des images |
| `book-06-psalm-034-note-001` | 314 | **AUTHENTIFIÉE** | PDF p. 314 : note imprimée n° 1, corps 9 pt, 50/50 mots concordants du début (« À un moment donné, l’homme qui veut rencontrer Dieu ») à la fin (« qui établira cette rencontre, mais le divin en lui. »). Appel dans le psaume et `psaume.noteIds` réciproque, limites visibles. | Aucune | Aucune après contrôle ciblé des images |
| `book-06-psalm-036-note-001` | 318 | **AUTHENTIFIÉE** | PDF p. 318 : note imprimée n° 1, corps 8 pt, 8/8 mots concordants du début (« L’Archange s’adresse ici à Olivier Manitara. ») à la fin (« L’Archange s’adresse ici à Olivier Manitara. »). Appel dans le psaume et `psaume.noteIds` réciproque, limites visibles. | Aucune | Aucune après contrôle ciblé des images |
| `book-06-psalm-040-note-002` | 325 | **NON RÉSOLUE** | PDF p. 325 : **un seul appel imprimé n° 1** et **un seul texte de 155 mots**, repris à l’identique dans les deux extractions `book-06-psalm-040-note-002` et `-003` (même `appliesTo.marker=1`, ordinales JSON 2 et 3). Concordance lexicale **155/155** mais **unicité impossible** : un imprimé pour deux identifiants. | Aucune | Deux identifiants pour le même passage imprimé ; association des appels au psaume et dédoublonnage canonique non établis. |
| `book-06-psalm-040-note-003` | 325 | **NON RÉSOLUE** | PDF p. 325 : **un seul appel imprimé n° 1** et **un seul texte de 155 mots**, repris à l’identique dans les deux extractions `book-06-psalm-040-note-002` et `-003` (même `appliesTo.marker=1`, ordinales JSON 2 et 3). Concordance lexicale **155/155** mais **unicité impossible** : un imprimé pour deux identifiants. | Aucune | Deux identifiants pour le même passage imprimé ; association des appels au psaume et dédoublonnage canonique non établis. |

**Checkpoint 064-02/A : 3 AUTHENTIFIÉES ; 0 CORRIGÉE ET AUTHENTIFIÉE ; 2 NON RÉSOLUES.** Les deux doublons potentiels ne sont ni supprimés, ni fusionnés, ni artificiellement authentifiés. Aucun fichier note, psaume, prière ou catalogue modifié ; point de sauvegarde GitHub avant le sous-lot B.

## Sous-lot B — notes 6 à 10 — EN ATTENTE DE FINALISATION

La source PDF des cinq notes suivantes est déjà enregistrée dans l'artefact `biblaw-064-02-proof-B` (ID **12425963016**), pages 334, 357, 369, 378. **Leurs verdicts ne sont pas encore consignés au stade de ce checkpoint A.** Ne pas reprendre A à la suite ; seulement finaliser B.
