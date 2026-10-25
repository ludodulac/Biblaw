# 🌸 BIBLAW — MISSION 064-17 — VERDICTS DOCUMENTAIRES

**Reprise officielle** : dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT ; HEAD initial `c9facbafc0558cfd4ba9f5a9f85f783e956c2b9d`. Périmètre strict : les 10 ID du [plan 064](064_PLAN.md), sans retraiter les 160 notes déjà examinées. Aucune publication, modification d'interface, fusion ni déploiement.

## Vigilance CI — état **avant** 064-17

Sur le HEAD initial : **39 SUCCESS / 42 runs**, trois échecs historiques distincts de 064-17 :

- **Browser smoke - lexical occurrence expansion**, [#40188421220](https://github.com/ludodulac/Biblaw/actions/runs/40188421220) : assertion d'ancien contrat lexical (`THÈME` / `MOTS`).
- **Audit theme entry identity**, [#40188383364](https://github.com/ludodulac/Biblaw/actions/runs/40188383364) : garde des changements historiques `js/biblaw.js`.
- **BIBLAW 058 corpus browse mobile**, [#40188383217](https://github.com/ludodulac/Biblaw/actions/runs/40188383217) : incompatibilité de Chromium/Playwright 1.55 avec `ubuntu26.04-x64`.

Causes établies en missions 064-15/16 ; pas de réparation hors périmètre. Les checks spécialisés du lot sont évalués séparément.

## Sous-lot A — cinq notes — CHECKPOINT

**Source** : 12 pages PDF originales distinctes **3128–3130, 3153–3155, 3164–3169** ; rendus visuels 2×, `note-proof.json`, `pdf-page-*-layout.json` enregistrés via `scripts/prove_notes_064_17_A.py`. [GitHub Actions preuve A #40191350349](https://github.com/ludodulac/Biblaw/actions/runs/40191350349) **SUCCESS**, artefact **12598441515**. Rattachement, marqueur, début/fin et pied ont été vérifiés **sur les images du PDF** ; une correspondance automatique seule ne donne jamais un verdict.

| Identifiant | PDF | Verdict | Preuves éditoriales (image, délimitation et unicité) |
|---|---:|---|---|
| `book-32-psalm-185-note-002` | 3129 | **AUTHENTIFIÉE** | Appel local¹ au **verset 19** (après « action »), note imprimée unique n°1 **44/44 tokens**, depuis « Dans une conférence donnée en février 2006 » jusqu'à « constituera son nouveau corps. » ; p.3129 appartient au psaume 185 et `noteIds` réciproque. La note 185/001 du lot 064-16 était sur p.3127, autre pied et autre texte ; pas de doublon. |
| `book-32-psalm-191-note-001` | 3154 | **AUTHENTIFIÉE** | Appel¹ au **verset 18** (« être possédé »), pied unique n°1 **17/17 tokens** du « Il s'agit du sixième » à « psaume 114. », p.3154 dans le psaume 191, `noteIds` réciproque. |
| `book-32-psalm-194-note-001` | 3165 | **AUTHENTIFIÉE** | Appel¹ au **verset 2** (« enseignements et rites reçus »), pied n°1 **38/38 tokens**, « L'Archange Ouriel fait référence » → « Grèce en mai 2013. ». Page canonique, `noteIds` réciproque. |
| `book-32-psalm-194-note-002` | 3166 | **AUTHENTIFIÉE** | Appel local¹ au **verset 17** (« terres esséniennes »), pied n°1 **47/47 tokens** de « En 2013, en plus du Québec » à « Ronde des Archanges. ». Bien que son ordinal ID soit 002, **le numéro imprimé sur cette page est 1** ; c'est une autre note, sur autre page, distincte du pied de p.3165 ; aucun conflit. |
| `book-32-psalm-195-note-001` | 3167–3168 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel¹ au **verset 1** (« poutre dans le tien »), pied n°1 p.3167 **5/5 tokens** : « Évangile selon Luc 6:42. ». L'extraction initiale contenait **35 tokens** ; les **30 tokens excédentaires** (« la même faiblesse, car il sait maintenant… ») sont en réalité la continuation en **corps de texte du verset 9**, en haut de p.3168, pas une note. **Correction du champ `text` uniquement : 35→5 tokens** ; p.3167 canonique, `noteIds` réciproque. |

**Bilan A : 5 notes AUTHENTIFIÉES, dont 1 CORRIGÉE ET AUTHENTIFIÉE ; 0 NON RÉSOLUE.** Aucun psaume ni prière modifié ; aucune note publiée.

## Sous-lot B — À FAIRE

Exclusivement `book-32-psalm-197-note-001`, `197-note-002`, `199-note-001`, `203-note-002`, `205-note-001`. La mission 064-16 et l'anomalie `31/184/001` demeurent intactes.
