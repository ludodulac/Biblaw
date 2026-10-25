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

## Sous-lot B — cinq notes — CHECKPOINT FINAL

**Source et preuves** : 15 pages PDF originales, **3173–3176, 3180–3183, 3199–3202, 3211–3213**, rendus ×2, `note-proof.json` et `pdf-page-*-layout.json` ; [Actions B #40191675252](https://github.com/ludodulac/Biblaw/actions/runs/40191675252) **SUCCESS**, artefact **12598825517** (`biblaw-064-17-proof-B`). Appels, pieds, numéros, extrémités et liens de psaumes contrôlés visuellement sur ces seules pages.

| Identifiant | PDF | Verdict | Preuve éditoriale |
|---|---:|---|---|
| `book-32-psalm-197-note-001` | 3174 | **AUTHENTIFIÉE** | Appel¹ au **verset 4** (« Nom »), pied unique n°1 **8/8 tokens** « Il s'agit du Nom de la Mère. ». P.3174 dans les pages canoniques 3174–3176, `noteIds` réciproque. Aucun doublon. |
| `book-32-psalm-197-note-002` | 3175 | **AUTHENTIFIÉE** | Appel local¹ au **verset 14** (« lampe d'Aladin »), pied n°1 **14/14 tokens** « La lampe d'Aladin renferme un génie ayant le pouvoir d'exaucer les vœux. ». P.3175 canonique, `noteIds` réciproque. ID ordinal 002 ≠ numéro de pied, lequel est bien 1 sur sa page. Distinct de 197/001. |
| `book-32-psalm-199-note-001` | 3181–3182 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel¹ au **verset 8** (« université essénienne »), pied n°1 p.3181 de **21 tokens** s'interrompant matériellement après « d'accéder », sans ponctuation finale ; **continuation du même pied**, sous le filet sans nouveau numéro p.3182 : « à l'Enseignement. » (**3 tokens**). Corps du psaume à 12,5 pt distinct du pied à 9 pt ; note complète **24 tokens**. **Correction du champ `text` uniquement 21→24**, page source initiale et `noteIds` inchangés. |
| `book-32-psalm-203-note-002` | 3201–3202 | **CORRIGÉE ET AUTHENTIFIÉE** | Appel local¹ au **verset 11** (« nom qu'il porte »), pied n°1 p.3201 **29 tokens**, de « Le porteur d'une vertu » à « Thomas Sagesse. » ; l'extraction initiale **259 tokens** ajoutait **230 tokens de la prière Pr.93**, qui débute en page 3202 et s'achève par « Amin. » : typographie 13 pt en italique, indépendante du pied 9 pt p.3201. **Correction du champ `text` uniquement 259→29**, retrait de la prière, préservation des pages de psaume et de prière. Autre note 203/001 sur p.3199 différente ; aucun conflit d'identité. |
| `book-32-psalm-205-note-001` | 3212 | **AUTHENTIFIÉE** | Appel¹ au **verset 40** (« œuvre¹ ») du psaume 205, immédiatement avant la prière Pr.95 ; sous le filet p.3212, pied n°1 complet **272/272 tokens** du « Depuis que les Archanges ont ouvert les portes du monde divin » jusqu'à « prêtres sacrificateurs. ». Début et fin dans le même pied, pas de passage de la prière en italique ; p.3212 canonique et `noteIds` réciproque. |

**Bilan B : 5 AUTHENTIFIÉES dont 2 CORRIGÉES ET AUTHENTIFIÉES ; 0 NON RÉSOLUE.**

## Clôture de 064-17

- **10/10 notes examinées en deux sous-lots de cinq** : A **5 authentifiées dont 1 corrigée** ; B **5 authentifiées dont 2 corrigées**. Total **10 AUTHENTIFIÉES, dont 3 CORRIGÉES ET AUTHENTIFIÉES, 0 NON RÉSOLUE**.
- **Trois corrections démontrées par le PDF original** : `32/195/001` **35→5 tokens**, retrait de texte du psaume p.3168 ; `32/199/001` **21→24 tokens**, continuation du pied p.3182 ; `32/203/002` **259→29 tokens**, retrait de la prière Pr.93 p.3202. Une seule propriété `text` de chacun des trois fichiers a été modifiée. Psaumes, prières et publication intacts.
- **Pages PDF originales : 27 pages distinctes** : A 12 (3128–3130,3153–3155,3164–3169), B 15 (3173–3176,3180–3183,3199–3202,3211–3213). Aucun autre lot audité.
- **Preuves / tests spécialisés** : [A #40191609121](https://github.com/ludodulac/Biblaw/actions/runs/40191609121) **SUCCESS** sur le checkpoint A, [B #40191675252](https://github.com/ludodulac/Biblaw/actions/runs/40191675252) **SUCCESS** sur les captures B avant corrections ; gardes explicites des 5 notes A/B, de la suite p.3182 et de l'exclusion de Pr.93. Les runs du HEAD final sont vérifiés séparément ci-dessous.
- **CI générale** : **39/42 SUCCESS au HEAD initial**, 3 échecs historiques non réparés (noms et références ci-dessus). Aucun changement de script CI général ni d'interface par 064-17. Ne jamais assimiler « deux tests spécialisés verts » à « toute la CI verte ».
- **Cumul 064** : **170/192 notes examinées ; 132 authentifiées (dont 8 corrigées), 38 NON RÉSOLUES, 22 restantes**. Les 160 notes examinées précédemment et l'anomalie 31/184/001 ne sont pas retraitées.
- **Protection** : PR #72 OPEN/DRAFT, sans fusion, publication, déploiement ou modification des contenus psaumes/prières. **STOP après 064-17.**
