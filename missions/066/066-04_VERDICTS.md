# 🌸 BIBLAW — MISSION 066-04 — DEUX PAIRES DE PIEDS IMPRIMÉS UNIQUES

**Statut : TERMINÉE — 4/4 identifiants strictement du plan, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES. Aucune mutation canonique.**

## Reprise et protocole

- Référence : [066_PLAN.md](066_PLAN.md), 066-04 (« Paires simples 07/047 et 08/025 ») ; IDs dans l'ordre officiel : `book-07-psalm-047-note-002`, `book-07-psalm-047-note-003`, `book-08-psalm-025-note-002`, `book-08-psalm-025-note-003`.
- Base GitHub `7aca233382ad13412348756e1ee6c352abba672f`, branche `feat/052-search-ui`, PR #72 **OPEN / DRAFT / non fusionnée** lors de l'unique vérification initiale.
- [Protocole 066-02](066-02_PROTOCOL.md) : chaîne **source→appel→pied physique→candidats** ; séparer preuve imprimée, concordance technique, hypothèse d'extraction et décision d'identité de Ludo. Le marqueur local « 1 » **ne vaut pas** suffixe `-note-001`.
- Preuves existantes **réutilisées sans nouvel audit** : [064-03](../064/064-03_VERDICTS.md) avec **p.416** (artefact **12426907184**, [Action 39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), preuve B), [064-04](../064/064-04_VERDICTS.md) avec **p.432** (artefact **12430728297**, [Action 39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802), preuve A), et [065-03](../065/065-03_VERDICTS.md). Les deux artefacts concernés sont **non expirés**.
- Deux psaumes et quatre notes JSON consultés en lecture seule : comparaison intégrale du `text`, marqueur, page, `verse`, `recordId`, `noteIds` et statut machine. **Aucune page du PDF original rouverte ; aucune nouvelle GitHub Action.**

## Dossier du pied imprimé A — psaume 07/047, p.416

- **FAIT ÉTABLI :** selon 064-03/B, **un seul pied imprimé local n°1 de 35/35 mots**, sous le psaume 47 p.416. Les JSON 002 et 003 ont exactement **187 caractères identiques**, même document, même p.416, même marqueur 1 et même `recordId=book-07-psalm-047`. Les deux IDs figurent dans `psalm-047.noteIds` ; p.416 est déclarée dans les pages du psaume.
- **HYPOTHÈSE :** un doublon a pu être créé pendant l'extraction ; aucune preuve de provenance ne permet d'établir **quel** ID a été généré pour représenter l'unique pied. `verse=null` (002) opposé à `verse=30` (003) ne démontre aucun choix.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** la **double représentation technique d'un seul pied physique** est établie ; le texte de la note est fidèle à l'imprimé selon 064. **Aucune correction d'ID ou de `noteIds` ne peut être exécutée avec certitude avant arbitrage.**
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** choisir, à partir d'une provenance indépendante ou d'une politique canonique explicitement approuvée, l'identité primaire 002/003 et le traitement réversible du candidat écarté (alias/archivage), puis autoriser le plan de réconciliation des références, sans suppression de texte.

## Dossier du pied imprimé B — psaume 08/025, p.432

- **FAIT ÉTABLI :** selon 064-04/A, **un seul pied imprimé local n°1 de 67/67 mots**, sous le psaume 25 p.432. Les JSON 002 et 003 ont exactement **369 caractères identiques** avec le même marqueur, la même page et le même support ; tous deux sont dans `psalm-025.noteIds`.
- **HYPOTHÈSE :** doublon d'extraction ; le `verse=18` de 003 est cohérent avec l'expression « terre des vivants » du verset 18, mais `verse=null` de 002 ne justifie pas qu'il soit rejeté. La page 432 ne prouve pas quel ID est historiquement canonique.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** duplication de la **revendication** démontrée et limites de la note imprimée connues ; il n'y a **aucune correction lexicale prouvée nécessaire** dans ces fichiers et aucune mutation d'un ID ne serait sûre sans arbitrage.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** déterminer l'ID canonique 002/003 ou approuver une politique d'alias, puis décider du traitement du concurrent et des `noteIds` du psaume. Aucun choix automatique sur `verse` ni `ordinal`.

## Verdicts individuels (ordre du plan)

### 1. `book-07-psalm-047-note-002`

- **FAIT ÉTABLI :** pied unique imprimé p.416, marqueur local 1, **35/35 mots**, texte intégral égal à `book-07-psalm-047-note-003` (**187 caractères**). `appliesTo.verse=null`. Le renvoi appartient au psaume 47 sur p.416 ; -003 renseigne le verset 30, sans preuve de préférence canonique.
- **HYPOTHÈSE :** duplication d'extraction possible ; l'identité canonique de ce fichier, par opposition à son concurrent, n'est pas documentée.
- **CORRECTION TECHNIQUE CERTAINE :** identité lexicale et double revendication **démontrées** ; aucune correction canonique d'ID, de verset ou de `noteIds` n'est prouvée sûre de façon indépendante.
- **DÉCISION ÉDITORIALE — LUDO :** établir la provenance ou décider d'une politique traçable d'identité/alias entre `book-07-psalm-047-note-002` et `book-07-psalm-047-note-003`, autoriser l'ajustement cohérent des références du psaume.
- **PREUVES DISPONIBLES :** [064](../064/064-03_VERDICTS.md), [065-03](../065/065-03_VERDICTS.md), [Action 39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426907184` non expiré ; note `data/notes/books/book-07/book-07-psalm-047-note-002.json` (blob `aa1063f9c3e4856fa8356a59b9f39fdc2cfa066d`) ; psaume `data/corpus/books/book-07/psalm-047.json` (blob `c6c55303c7a888ffa124c71962a3ebea37455642`).
- **PREUVE MANQUANTE :** traçabilité des IDs indépendante du marqueur 1, de l'ordinal 002/003 et du verset renseigné, puis mandat de conservation sans perte et de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 2. `book-07-psalm-047-note-003`

- **FAIT ÉTABLI :** pied unique imprimé p.416, marqueur local 1, **35/35 mots**, texte intégral égal à `book-07-psalm-047-note-002` (**187 caractères**). `appliesTo.verse=30`. Le verset 30 du psaume 47 est sur p.416, mais la métadonnée renseignée ne démontre pas que -003 plutôt que -002 est canonique.
- **HYPOTHÈSE :** duplication d'extraction possible ; l'identité canonique de ce fichier, par opposition à son concurrent, n'est pas documentée.
- **CORRECTION TECHNIQUE CERTAINE :** identité lexicale et double revendication **démontrées** ; aucune correction canonique d'ID, de verset ou de `noteIds` n'est prouvée sûre de façon indépendante.
- **DÉCISION ÉDITORIALE — LUDO :** établir la provenance ou décider d'une politique traçable d'identité/alias entre `book-07-psalm-047-note-003` et `book-07-psalm-047-note-002`, autoriser l'ajustement cohérent des références du psaume.
- **PREUVES DISPONIBLES :** [064](../064/064-03_VERDICTS.md), [065-03](../065/065-03_VERDICTS.md), [Action 39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426907184` non expiré ; note `data/notes/books/book-07/book-07-psalm-047-note-003.json` (blob `f4b76d580d95938d3a1ecaaad2ae438256d0215c`) ; psaume `data/corpus/books/book-07/psalm-047.json` (blob `c6c55303c7a888ffa124c71962a3ebea37455642`).
- **PREUVE MANQUANTE :** traçabilité des IDs indépendante du marqueur 1, de l'ordinal 002/003 et du verset renseigné, puis mandat de conservation sans perte et de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 3. `book-08-psalm-025-note-002`

- **FAIT ÉTABLI :** pied unique imprimé p.432, marqueur local 1, **67/67 mots**, texte intégral égal à `book-08-psalm-025-note-003` (**369 caractères**). `appliesTo.verse=null`. Le renvoi appartient au psaume 25 p.432 ; -003 indique v.18, tandis que -002 a verse=null sans second pied.
- **HYPOTHÈSE :** duplication d'extraction possible ; l'identité canonique de ce fichier, par opposition à son concurrent, n'est pas documentée.
- **CORRECTION TECHNIQUE CERTAINE :** identité lexicale et double revendication **démontrées** ; aucune correction canonique d'ID, de verset ou de `noteIds` n'est prouvée sûre de façon indépendante.
- **DÉCISION ÉDITORIALE — LUDO :** établir la provenance ou décider d'une politique traçable d'identité/alias entre `book-08-psalm-025-note-002` et `book-08-psalm-025-note-003`, autoriser l'ajustement cohérent des références du psaume.
- **PREUVES DISPONIBLES :** [064](../064/064-04_VERDICTS.md), [065-03](../065/065-03_VERDICTS.md), [Action 39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802), artefact `12430728297` non expiré ; note `data/notes/books/book-08/book-08-psalm-025-note-002.json` (blob `345e902e882aaa1e978e716649df436952cb4f12`) ; psaume `data/corpus/books/book-08/psalm-025.json` (blob `5f65243f7f6a2b4398984f2868e8ae983926dd17`).
- **PREUVE MANQUANTE :** traçabilité des IDs indépendante du marqueur 1, de l'ordinal 002/003 et du verset renseigné, puis mandat de conservation sans perte et de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 4. `book-08-psalm-025-note-003`

- **FAIT ÉTABLI :** pied unique imprimé p.432, marqueur local 1, **67/67 mots**, texte intégral égal à `book-08-psalm-025-note-002` (**369 caractères**). `appliesTo.verse=18`. Le verset 18 p.432 contient « terre des vivants », en rapport avec le pied ; le contexte est cohérent, mais ne choisit pas l'ID.
- **HYPOTHÈSE :** duplication d'extraction possible ; l'identité canonique de ce fichier, par opposition à son concurrent, n'est pas documentée.
- **CORRECTION TECHNIQUE CERTAINE :** identité lexicale et double revendication **démontrées** ; aucune correction canonique d'ID, de verset ou de `noteIds` n'est prouvée sûre de façon indépendante.
- **DÉCISION ÉDITORIALE — LUDO :** établir la provenance ou décider d'une politique traçable d'identité/alias entre `book-08-psalm-025-note-003` et `book-08-psalm-025-note-002`, autoriser l'ajustement cohérent des références du psaume.
- **PREUVES DISPONIBLES :** [064](../064/064-04_VERDICTS.md), [065-03](../065/065-03_VERDICTS.md), [Action 39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802), artefact `12430728297` non expiré ; note `data/notes/books/book-08/book-08-psalm-025-note-003.json` (blob `fa3ca63e09acf03fa2063ab07450586fa897b893`) ; psaume `data/corpus/books/book-08/psalm-025.json` (blob `5f65243f7f6a2b4398984f2868e8ae983926dd17`).
- **PREUVE MANQUANTE :** traçabilité des IDs indépendante du marqueur 1, de l'ordinal 002/003 et du verset renseigné, puis mandat de conservation sans perte et de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

## Tests documentaires spécialisés

- **PASS** — Quatre IDs exacts et uniques du plan officiel 066-04.
- **PASS** — Quatre IDs appartenant à l'inventaire 066-04.
- **PASS** — Protocole 066-02 : gabarit, limites probatoires et conservation.
- **PASS** — 066-04 non commencée, commit parent valide.
- **PASS** — Correspondance ID JSON et recordId des quatre notes.
- **PASS** — 07/047 deux textes de note strictement identiques, 187 caractères.
- **PASS** — 08/025 deux textes de note strictement identiques, 369 caractères.
- **PASS** — 07/047 même document, page 416 et marqueur 1.
- **PASS** — 08/025 même document, page 432 et marqueur 1.
- **PASS** — 07/047 versets déclarés null et 30.
- **PASS** — 08/025 versets déclarés null et 18.
- **PASS** — 07/047 références noteIds réciproques pour les deux IDs.
- **PASS** — 08/025 références noteIds réciproques pour les deux IDs.
- **PASS** — Pages du pied couvertes dans les sources des psaumes.
- **PASS** — Versets 30 et 18 présents aux pages correspondantes.
- **PASS** — Quatre statuts machine = extraction à revoir, non authentification.
- **PASS** — Champs textLength absents, longueur calculée et aucun ajout.

**17/17 PASS** — contrôles limités à ces quatre notes et deux psaumes, plus au plan/protocole. L'unicité des pieds imprimés est une **preuve déjà acquise** dans les rapports visuels 064 : elle n'est pas certifiée par une nouvelle lecture PDF ou une nouvelle exécution de CI.

## Solution envisagée mais non autorisée

Pour chaque paire, la résolution éventuelle devra conserver les deux textes et leurs SHA avant intervention, enregistrer une décision explicite de Ludo sur l'ID de référence ou le mécanisme d'alias, prévoir un diff de `noteIds` et vérifier qu'un pied imprimé correspond à une seule occurrence logique sans ID orphelin. Aucune identité, suppression, mutation du corpus ou nouvelle règle de catalogue n'est décidée dans 066-04.

**Clôture 066-04 : 4/4 examinées, 0 authentifiée, 0 corrigée, 4 NON RÉSOLUES. Cumul 066 : 44 NON RÉSOLUES, 2 corrigées et authentifiées au cours de 065 ; 0 correction en phase 066. PR #72 DRAFT non fusionnée. STOP — 066-05 NON COMMENCÉE.**
