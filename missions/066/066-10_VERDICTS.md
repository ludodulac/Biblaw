# 🌸 BIBLAW — MISSION 066-10 — NOTES IMPRIMÉES SOUS PR.11, PR.53 ET PR.71

**Statut : TERMINÉE — 3/3 notes pilotes examinées ; 0 AUTHENTIFIÉE ; 0 CORRIGÉE ET AUTHENTIFIÉE ; 3 NON RÉSOLUES.** Aucune modification des JSON canoniques.

## 1. Mandat, branche et archives

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, HEAD initial `b95c32b0e22d6ee5e3ccbfe70118395ec5c1a5b9` conforme au communiqué ; PR #72 **OPEN / DRAFT, non fusionnée** à l'unique vérification initiale.
- [Plan officiel 066-10](066_PLAN.md) : **exclusivement** `book-17-psalm-115-note-001`, `book-27-psalm-158-note-001`, `book-27-psalm-177-note-001`. Lecture du [protocole 066-02](066-02_PROTOCOL.md) : **source → appel → pied → support**, puis classement des faits, hypothèses, corrections démontrées et autorisations de Ludo.
- Trois fichiers de **notes**, trois **psaumes** et trois **prières autonomes** ont été lus au HEAD de base, sans mutation. Le [verdict 065-07](../065/065-07_VERDICTS.md), [064-08](../064/064-08_VERDICTS.md) et [064-13](../064/064-13_VERDICTS.md) permettent d'éviter toute nouvelle inspection visuelle.
- Preuves originales déjà capturées et **non expirées** : Pr.11, p.1122 [Action 39916095956](https://github.com/ludodulac/Biblaw/actions/runs/39916095956) / 064-08/A artefact **12484399373** ; Pr.53, p.2485 [Action 40130414394](https://github.com/ludodulac/Biblaw/actions/runs/40130414394) / 064-13/A artefact **12574772504** ; Pr.71, p.2570 [Action 40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623) / 064-13/B artefact **12574719450**. **PDF non rouvert, aucun nouveau workflow ni audit général.**

## 2. Rapprochement document source → appel → pied → candidats

| Note pilote | Unique pied imprimé selon archives 064 | Appel et support imprimés | Page hors psaume | Prière autonome existante | Obstacle |
|---|---|---|---|---|---|
| `17/115/001` | **5/5 tokens**, n°1, **p.1122** | **Pr.11**, « manger mon corps et boire mon sang¹ » | **OUI**, `psalm.source.pdfPages=[1117,1118,1119,1120,1121]` | `michael-book-17-prayer-011`, `printedPages=[1121,1122]` | absence de relation note→prière malgré une page de prière enregistrée |
| `27/158/001` | **22/22 tokens**, n°1, **p.2485** | **Pr.53**, « casque sacré¹ » | **OUI**, `psalm.source.pdfPages=[2481,2482,2483,2484]` | `raphael-book-27-prayer-053`, `printedPages=[2484]` | absence de relation note→prière ; `printedPages` omet la page du pied |
| `27/177/001` | **103/103 tokens**, n°1, **p.2570** | **Pr.71**, « 6 directions comme le septième jour de l’Alliance¹ » | **OUI**, `psalm.source.pdfPages=[2567,2568,2569]` | `raphael-book-27-prayer-071`, `printedPages=[2569]` | absence de relation note→prière ; `printedPages` omet la page du pied |

**Précision méthodologique :** `psalm.noteIds` référence chaque note **une fois**, mais son existence ne démontre pas que le pied soit imprimé sous un verset. Le schéma actuel des prières possède `appliesToPsalmId`, non `noteIds` ; le marqueur « 1 » présent dans leur texte ne constitue pas à lui seul une relation canonique explicite. Aucun second ID concurrent ou composite n'est documenté pour ces trois occurrences dans les preuves consultées.

## 3. Verdict individuel — `book-17-psalm-115-note-001`

**FAITS ÉTABLIS.** La preuve visuelle archivée **064-08/A** atteste un **pied local imprimé n°1 de 5 tokens sur la page 1122** correspondant à la chaîne intégrale du JSON (25 caractères) ; appel **dans Pr.11**, « manger mon corps et boire mon sang¹ ». La prière autonome existe, affiche exactement ce marqueur d'appel dans son `text` et possède `appliesToPsalmId=book-17-psalm-115`. Le psaume porte le seul `noteIds` réciproque, mais sa liste de pages **exclut p.1122**. `appliesTo.verse=null` et statut `machine-extracted-needs-review`.

**FAIT TECHNIQUE DE PAGE.** `prayer.source.printedPages=[1121, 1122]` inclut la page physique du pied imprimé ; aucune anomalie de `printedPages` n'est constatée pour Pr.11.

**HYPOTHÈSE.** L'extraction a probablement classé une note de prière sous le psaume adjacent faute de relation note→prière dans le modèle ; ce mécanisme n'est **pas** prouvé. L'absence de second pied dans les inspections ciblées ne constitue pas un audit d'unicité de tout le corpus.

**CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE.** Le **support imprimé est Pr.11**, non un verset du psaume book-17-psalm-115 ; le texte du pied n'exige **aucune coupure ni correction lexicale** d'après la preuve historique. La page du pied est p.1122. Il existe un besoin documenté de relation explicite note→prière et de contrôle cohérent des `noteIds` du psaume sans changement spéculatif de page. **Aucune correction dans le corpus n'est autorisée.**

**DÉCISION NÉCESSITANT LUDO.** Valider le **schéma note→prière** (identifiant stable de prière, emplacement de l'appel, page de pied, marqueur imprimé local, politique de référencement sans lien orphelin), puis autoriser explicitement les éventuels changements de `note.appliesTo`, `psalm.noteIds` et métadonnées de prière. **Pas de réattribution arbitraire à un verset.** Verdict : **NON RÉSOLUE**.

**Traçabilité (blobs Git) :** note `data/notes/books/book-17/book-17-psalm-115-note-001.json` — `15f2c093f28bc8bed1ac1d58ccf9d94ef62cfcbf` ; psaume `data/corpus/books/book-17/psalm-115.json` — `bcb34ebaaa863f6f3934fed6ceb019dcbed56fe9` ; prière `data/prayers/michael-book-17-prayer-011.json` — `c53a44dfd3a953d50a99821aaf3f04ff47225bd7`.

## 4. Verdict individuel — `book-27-psalm-158-note-001`

**FAITS ÉTABLIS.** La preuve visuelle archivée **064-13/A** atteste un **pied local imprimé n°1 de 22 tokens sur la page 2485** correspondant à la chaîne intégrale du JSON (115 caractères) ; appel **dans Pr.53**, « casque sacré¹ ». La prière autonome existe, affiche exactement ce marqueur d'appel dans son `text` et possède `appliesToPsalmId=book-27-psalm-158`. Le psaume porte le seul `noteIds` réciproque, mais sa liste de pages **exclut p.2485**. `appliesTo.verse=null` et statut `machine-extracted-needs-review`.

**FAIT TECHNIQUE DE PAGE.** `prayer.source.printedPages=[2484]` n'inclut **pas** la p.2485 du pied imprimé. La source archivée confirme la continuation de la prière et son appel sous Pr.53, mais la correction du périmètre des pages requiert un mandat documentaire pour ne pas confondre page de texte et page de note.

**HYPOTHÈSE.** L'extraction a probablement classé une note de prière sous le psaume adjacent faute de relation note→prière dans le modèle ; ce mécanisme n'est **pas** prouvé. L'absence de second pied dans les inspections ciblées ne constitue pas un audit d'unicité de tout le corpus.

**CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE.** Le **support imprimé est Pr.53**, non un verset du psaume book-27-psalm-158 ; le texte du pied n'exige **aucune coupure ni correction lexicale** d'après la preuve historique. La page du pied est p.2485. Il existe un besoin documenté de relation explicite note→prière et de clarification de `printedPages` (décrit-elle la seule prière, ou aussi la page de la note ?) et des `noteIds` du psaume. **Aucune correction dans le corpus n'est autorisée.**

**DÉCISION NÉCESSITANT LUDO.** Valider le **schéma note→prière** (identifiant stable de prière, emplacement de l'appel, page de pied, marqueur imprimé local, politique de référencement sans lien orphelin), puis autoriser explicitement les éventuels changements de `note.appliesTo`, `psalm.noteIds` et métadonnées de prière. **Pas de réattribution arbitraire à un verset.** Verdict : **NON RÉSOLUE**.

**Traçabilité (blobs Git) :** note `data/notes/books/book-27/book-27-psalm-158-note-001.json` — `5f16c231b2a451d30a099bd4c63528405c5cf7c0` ; psaume `data/corpus/books/book-27/psalm-158.json` — `bff32ad60d45e0982699f3a97b53f79540851b57` ; prière `data/prayers/raphael-book-27-prayer-053.json` — `0bcbd30b4a14a9a1372838a868031f712027e01a`.

## 5. Verdict individuel — `book-27-psalm-177-note-001`

**FAITS ÉTABLIS.** La preuve visuelle archivée **064-13/B** atteste un **pied local imprimé n°1 de 103 tokens sur la page 2570** correspondant à la chaîne intégrale du JSON (564 caractères) ; appel **dans Pr.71**, « 6 directions comme le septième jour de l’Alliance¹ ». La prière autonome existe, affiche exactement ce marqueur d'appel dans son `text` et possède `appliesToPsalmId=book-27-psalm-177`. Le psaume porte le seul `noteIds` réciproque, mais sa liste de pages **exclut p.2570**. `appliesTo.verse=null` et statut `machine-extracted-needs-review`.

**FAIT TECHNIQUE DE PAGE.** `prayer.source.printedPages=[2569]` n'inclut **pas** la p.2570 du pied imprimé. La source archivée confirme la continuation de la prière et son appel sous Pr.71, mais la correction du périmètre des pages requiert un mandat documentaire pour ne pas confondre page de texte et page de note.

**HYPOTHÈSE.** L'extraction a probablement classé une note de prière sous le psaume adjacent faute de relation note→prière dans le modèle ; ce mécanisme n'est **pas** prouvé. L'absence de second pied dans les inspections ciblées ne constitue pas un audit d'unicité de tout le corpus.

**CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE.** Le **support imprimé est Pr.71**, non un verset du psaume book-27-psalm-177 ; le texte du pied n'exige **aucune coupure ni correction lexicale** d'après la preuve historique. La page du pied est p.2570. Il existe un besoin documenté de relation explicite note→prière et de clarification de `printedPages` (décrit-elle la seule prière, ou aussi la page de la note ?) et des `noteIds` du psaume. **Aucune correction dans le corpus n'est autorisée.**

**DÉCISION NÉCESSITANT LUDO.** Valider le **schéma note→prière** (identifiant stable de prière, emplacement de l'appel, page de pied, marqueur imprimé local, politique de référencement sans lien orphelin), puis autoriser explicitement les éventuels changements de `note.appliesTo`, `psalm.noteIds` et métadonnées de prière. **Pas de réattribution arbitraire à un verset.** Verdict : **NON RÉSOLUE**.

**Traçabilité (blobs Git) :** note `data/notes/books/book-27/book-27-psalm-177-note-001.json` — `a6e692b595f6dafae98839c19a07cb51cc1e565e` ; psaume `data/corpus/books/book-27/psalm-177.json` — `09dbbd82fe2e69a162dce914275fbbdfeafd0ced` ; prière `data/prayers/raphael-book-27-prayer-071.json` — `2890fc2f6852bfeacbcb61cbd3c4359b314532bf`.

## 6. Proposition documentaire de relation note→prière — NON IMPLÉMENTÉE

- Chaque occurrence peut être décrite, **sans inventer de nouvel ID ni modifier les fichiers**, par la relation documentée : note existante → `prayer.id` (Pr.11, Pr.53, Pr.71) → marqueur local n°1 retrouvé dans `prayer.text` → page du pied imprimé. Le nom du champ, le sens d'un éventuel alias et la réconciliation avec `psalm.noteIds` nécessitent **l'approbation de Ludo**.
- Pour **Pr.53 et Pr.71**, les `printedPages` des prières n'enregistrent que les pages de début (2484 / 2569) ; la page du pied est 2485 / 2570. **Ne pas supposer qu'il s'agit nécessairement d'une erreur du champ**, car celui-ci pourrait être défini pour les seules pages du texte prière. Fixer la sémantique de ce champ avant toute modification.
- Garanties futures : aucune disparition de note, aucun lien orphelin, un seul appel logique vers le bon pied, conservation de tous les textes, SHA des fichiers hors périmètre inchangés ; tests à mener **seulement après** autorisation.
- **ALERTE PERMANENTE ANTÉRIEURE, HORS PÉRIMÈTRE ET NON RÉEXAMINÉE :** les **1 679 caractères** du composite historique 26/189 **ne sont pas couverts par le psaume actuel** ; leur conservation ailleurs **n'est pas démontrée**, donc aucun retrait de texte n'est admissible. Cette alerte est maintenue sans nouvelle manipulation.

## 7. Contrôles spécialisés en lecture seule

- **PASS** — Plan 066-10 : exactement trois IDs dans l'ordre officiel.
- **PASS** — Inventaire : trois IDs affectés au seul lot 066-10.
- **PASS** — Protocole 066-02 : rattachement note→prière soumis à Ludo.
- **PASS** — État pré-mission 066-10 NON COMMENCÉE et arbre parent existant.
- **PASS** — 17/115/001 ID note et référence au psaume.
- **PASS** — 17/115/001 preuve p.1122 exclue des pages du psaume.
- **PASS** — 17/115/001 prière Pr.11 reliée éditorialement au psaume.
- **PASS** — 17/115/001 présence d'un renvoi local unique dans la prière.
- **PASS** — 17/115/001 marqueur de note 1, verse null, statut machine en attente.
- **PASS** — 17/115/001 source du pied incluse dans printedPages ou anomalie documentée.
- **PASS** — 17/115/001 conservation de la note textuelle sans suffixe composite observé.
- **PASS** — 17/115/001 absence de noteIds explicite dans la prière actuelle.
- **PASS** — 27/158/001 ID note et référence au psaume.
- **PASS** — 27/158/001 preuve p.2485 exclue des pages du psaume.
- **PASS** — 27/158/001 prière Pr.53 reliée éditorialement au psaume.
- **PASS** — 27/158/001 présence d'un renvoi local unique dans la prière.
- **PASS** — 27/158/001 marqueur de note 1, verse null, statut machine en attente.
- **PASS** — 27/158/001 source du pied incluse dans printedPages ou anomalie documentée.
- **PASS** — 27/158/001 conservation de la note textuelle sans suffixe composite observé.
- **PASS** — 27/158/001 absence de noteIds explicite dans la prière actuelle.
- **PASS** — 27/177/001 ID note et référence au psaume.
- **PASS** — 27/177/001 preuve p.2570 exclue des pages du psaume.
- **PASS** — 27/177/001 prière Pr.71 reliée éditorialement au psaume.
- **PASS** — 27/177/001 présence d'un renvoi local unique dans la prière.
- **PASS** — 27/177/001 marqueur de note 1, verse null, statut machine en attente.
- **PASS** — 27/177/001 source du pied incluse dans printedPages ou anomalie documentée.
- **PASS** — 27/177/001 conservation de la note textuelle sans suffixe composite observé.
- **PASS** — 27/177/001 absence de noteIds explicite dans la prière actuelle.
- **PASS** — Pages de la prière 11 = 1121–1122.
- **PASS** — Pr.53 et Pr.71 ont printedPages limitées à 2484 et 2569.
- **PASS** — Alerte 066-08 1 679 caractères préservée dans les rapports sources.

**31/31 contrôles PASS** : seulement les trois notes pilotes et leurs psaumes/prières ; le constat d'unicité du pied relève des **archives visuelles 064** et n'a pas été refait sur le PDF.

**CLÔTURE : 066-10 TERMINÉE — 3/3 pilotes examinées, 0 authentifiée, 0 corrigée, 3 NON RÉSOLUES. Bilan cumulé 066-03…066-10 : 23/44 notes examinées ; 44 NON RÉSOLUES. Aucune écriture canonique ni fusion de PR #72. STOP — 066-11 NON COMMENCÉE.**
