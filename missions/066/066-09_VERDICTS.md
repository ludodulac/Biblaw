# 🌸 BIBLAW — MISSION 066-09 — Concurrents 30/200 et inter-psaumes 35/215

**TERMINÉE — 2/2 notes pilotes du plan, 0 authentifiée, 0 corrigée, 2 NON RÉSOLUES.** Base `5c73b4d1c6f3a226a32e0b211fdb6b94694be30a`, branche `feat/052-search-ui`, PR #72 **OPEN/DRAFT non fusionnée** au seul contrôle initial. Corpus inchangé.

## Périmètre, archives, méthode

- [Plan 066](066_PLAN.md) et [protocole 066-02](066-02_PROTOCOL.md) : source → appel → pied → candidats, conservation sans perte et refus de choisir l'ID sur son ordinal ou son statut.
- **Seulement** `book-30-psalm-200-note-003` et `book-35-psalm-215-note-001`. Comparands historiques consultés **sans nouvelle instruction sur 063** : `book-30-psalm-200-note-002` et `book-35-psalm-214-note-002`.
- Preuves 064-15/A, p.2900–2901 ([Action 40137180838](https://github.com/ludodulac/Biblaw/actions/runs/40137180838), artefact **12576971728**, non expiré) ; 064-19/A, p.3485 ([Action 40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710), artefact **12650754088**, non expiré). [Verdicts 065-13](../065/065-13_VERDICTS.md) réutilisés. **Aucune réouverture du PDF**, aucun workflow nouveau.

## Pilote 1 — `book-30-psalm-200-note-003`

**FAIT ÉTABLI — source et appel :** [064-15/A](../064/064-15_VERDICTS.md) a inspecté **une seule note locale n°1 de 111/111 tokens p.2901** sur les « piliers », liée au dialogue « fonction … donnée ». Le pilote 003 a `source.pdfPage=2901`, `marker=1`, `verse=32` et un texte de **615 caractères**. Le texte du v.32 comporte ce dialogue mais ses `sourcePages=[2900]`. L'écart **p.2900 pour le verset / p.2901 pour la note** est constaté ; son explication n'est pas établie par ces seuls JSON.

**FAIT ÉTABLI — composite :** le texte de l'ancien `30/200/002` (**2935 caractères**) commence par les **615 caractères exacts** du pilote. Égalité stricte de tout le composite :
`text_002 === text_003 + " " + v38…v42 numérotés + " Pr. 83. " + prayer_083.text`.
Les **versets 38–42** sont déjà présents dans `psalm-200.json` p.2902, et la **prière complète Pr.83** dans `gabriel-book-30-prayer-083.json`, reliée au psaume 200. **Aucun fragment de ce composite ne reste sans destination démontrée dans cette comparaison.** Le psaume contient les deux IDs dans `noteIds`.

**HYPOTHÈSE :** 003 serait une extraction plus propre que l'historique 002 ; l'écart de pages pourrait venir du découpage de l'appel et du pied. Ni la chronologie ni la provenance canonique ne sont prouvées.

**CORRECTION TECHNIQUE CERTAINE :** limite du pied à **615 caractères**, suffixe versets et Pr.83 identiques aux destinations existantes, **une seule occurrence imprimée** ; aucune suppression, réécriture ni modification sûre d'identifiant avant arbitrage.

**DÉCISION NÉCESSITANT LUDO :** identité 002/003 ou alias/archivage réversible, `noteIds` réconciliés, éventuelle vérification ciblée du positionnement exact du renvoi. Sans provenance indépendante, **NON RÉSOLUE**.

**Blobs :** pilote `fa829497c11f9d078f854dbda66db4a35f7e0598`, ancien `83b5c7536f173305a47cea79b6989fa49c2424ef`, psaume `4fe5533588c71b4363719a9e06090d91c8c6b905`, Pr.83 `2b416a97d62ac8d56af9dc8d16108676cb0b7452`.

## Pilote 2 — `book-35-psalm-215-note-001`

**FAIT ÉTABLI — source et appel :** [064-19/A](../064/064-19_VERDICTS.md) décrit un **seul pied local n°1 de 24/24 tokens p.3485, appelé au v.36 du psaume 215** (« loi des affinités »). Le JSON de 215 inclut **la page 3485 et le v.36 avec le marqueur d'appel final** ; `215/001` a `verse=null` mais le texte imprimé complet de **137 caractères**.

**FAIT ÉTABLI — double revendication :** l'historique `35/214/002` a le **même texte intégral** (137 caractères), `pdfPage=3485`, `verse=36`, mais `recordId=book-35-psalm-214`. Or le psaume **214 couvre seulement les pages 3481–3483 et les versets 1–25**. `psalm-214.noteIds` référence cet historique ; `psalm-215.noteIds` référence 215/001. **Le rattachement de 214/002 à 214 est techniquement contradictoire avec la source et le verset**, sans démontrer quel fichier ID doit survivre.

**HYPOTHÈSE :** erreur de support dans l'extraction 214/002, puis seconde capture sous 215. Origine des deux noms non établie. Le statut `machine-extracted-source-boundary-audited` de 215/001 ne prouve aucune identité canonique.

**CORRECTION TECHNIQUE CERTAINE :** le **support du pied** est 215/v.36/p.3485 et **non 214** ; les deux chaînes sont strictement égales. La correction concertée des liens est techniquement envisageable, **non autorisée ici**.

**DÉCISION NÉCESSITANT LUDO :** confirmer identité canonique ou politique d'alias, traitement du vieux nom 214/002, rattachement v.36 dans l'enregistrement retenu et migration cohérente des deux listes `noteIds`. Sans décision, **NON RÉSOLUE**.

**Blobs :** pilote `0aa3ed6137d65b8f2e0b495599f1fb173e9c3d25`, ancien `0420773f53ea38c794138741587decfe9a71c6c0`, psaume 215 `2396d0113789b91db3710c80a525932cd4494f31`, psaume 214 `fa2e11eb408fdc41239336919b13568ec7876682`.

## Plan non exécuté et interdiction de perte

1. Conserver les quatre chaînes de notes, leurs empreintes, la prière Pr.83, les psaumes et leurs `noteIds`. 30/200 : après décision, une seule occurrence logique avec ses versets 38–42 et Pr.83 intégralement conservés. 35/215 : après décision, une seule occurrence logique sous 215/v.36, sans lien orphelin.
2. **Alerte 066-08 inchangée et hors examen de ce lot : 1 679 caractères du composite historique 26/189 ne sont pas couverts par le psaume actuel ; leur conservation ailleurs n'est pas démontrée.** Aucune troncature ou modification n'est possible.
3. Toutes écritures des notes, psaumes, prières, interfaces, publications, déploiements, workflows ou fusion PR demanderaient une autorisation explicite de Ludo ; **aucune effectuée**.

## Contrôles spécialisés

- **PASS** — Périmètre officiel : seulement 2 IDs.
- **PASS** — Inventaire 066-09 : deux notes affectées.
- **PASS** — Protocole 066-02 actif.
- **PASS** — État avant mission et arbre Git.
- **PASS** — IDs des deux pilotes et anciens conformes.
- **PASS** — 30/200 : source/page/marqueur communs.
- **PASS** — 30/200 : 615 caractères du pied en préfixe exact.
- **PASS** — 30/200 : composite 2935 caractères reconstruit exactement.
- **PASS** — 30/200 : versets 38–42 sur p.2902.
- **PASS** — 30/200 : Pr83 texte autonome et lien au psaume.
- **PASS** — 30/200 : IDs réciproques présents dans noteIds.
- **PASS** — 30/200 : verse32 source p2900, pied p2901.
- **PASS** — 35/215 : égalité stricte des 137 caractères.
- **PASS** — 35/215 : note locale marqueur 1 page 3485.
- **PASS** — 35/215 : vrai support psaume 215 p3485 et v36.
- **PASS** — 35/214 : ancien lié à 214 hors source 3485 et sans v36.
- **PASS** — 35/215 : deux noteIds distribués dans deux psaumes.
- **PASS** — 35/215 : verse null pilote, verse36 ancien.
- **PASS** — Statuts techniques ne valent pas authentification.
- **PASS** — Alerte 1679 préservée dans documents existants.

**20/20 PASS** en lecture seule ; unicité des pieds issue des preuves visuelles **archivées**, pas d'une nouvelle inspection PDF.

**Clôture : 2/2 pilotes, 0 corrigée, 0 authentifiée, 2 NON RÉSOLUES ; cumul 20/44 examinées et 44 NON RÉSOLUES. PR #72 DRAFT, non fusionnée. STOP — 066-10 non commencée.**
