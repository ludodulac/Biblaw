# 🌸 BIBLAW — 066-03 — PAIRES SIMPLES 06/040 ET 07/032

**TERMINÉE — 4 notes du plan traitées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.** Aucune correction canonique.

## Périmètre et chaîne de preuves

- [Plan officiel](066_PLAN.md) : précisément `book-06-psalm-040-note-002`, `book-06-psalm-040-note-003`, `book-07-psalm-032-note-002`, `book-07-psalm-032-note-003`. Protocole [066-02](066-02_PROTOCOL.md) : source→appel→pied→candidats, choix éditorial distinct des concordances techniques. PR #72 OPEN/DRAFT lors du seul contrôle initial, base `a9bfa97c86161b5473cf9273d96d154e8143109d`.
- Pied 06/040 : [064-02](../064/064-02_VERDICTS.md), p.325, [run #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216), artefact A `12426161529` ; pied 07/032 : [064-03](../064/064-03_VERDICTS.md), p.381, [run #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact A `12426552703` ; les deux artefacts **non expirés**. [Verdicts 065-02](../065/065-02_VERDICTS.md). PDF original non rouvert, aucune nouvelle Action.
- Métadonnées vérifiées en lecture seule : quatre fichiers notes, deux psaumes, pages et marqueurs locaux, texte entier, réciprocité des `noteIds`, champ `verse` et statut technique. Les champs `textLength` ne sont **pas** présents comme propriété des JSON canoniques ; longueur calculée depuis `text` (934 / 30 caractères par paire), sans écriture.

## Pied imprimé A — psaume 06/040, p.325

**FAIT ÉTABLI :** unique pied imprimé n°1 de **155 mots**, repris *caractère pour caractère* dans 002 et 003 (934 caractères), même page et marqueur. Deux `noteIds` dans le psaume. La 064-02 constate une seule occurrence physique.

**HYPOTHÈSE :** doublon créé par l'extraction ; impossible de déterminer l'ID de provenance à partir de la page ou du texte identique. Le `verse=null` de 002 et le `verse=11` de 003 ne désignent pas l'identifiant canonique.

**CORRECTION TECHNIQUE CERTAINE :** constater une **double revendication d'un seul pied**, non deux pieds distincts. Une présentation canonique ne devrait pas les exposer comme deux occurrences physiques. **Aucune modification de JSON, de `noteIds` ou d'ID ne serait sûre avant la décision éditoriale** ; aucune graphie à corriger.

**DÉCISION ÉDITORIALE — LUDO :** désigner l'ID conservé par provenance certifiée ou approuver une politique d'alias/archivage réversible, puis autoriser la réconciliation de `psalm-040.noteIds` sans supprimer le texte ni la trace historique.

## Pied imprimé B — psaume 07/032, p.381

**FAIT ÉTABLI :** unique pied imprimé n°1 « Évangile selon Matthieu 18:20. » (**5/5 mots**), appelé au v.27 d'après 064-03. Les deux champs `text` sont strictement identiques (30 caractères) ; `002` et `003` réclament la même page et le même marqueur. Deux références `noteIds` existent.

**HYPOTHÈSE :** doublon d'extraction ; le `verse=null` de 002 et le `verse=27` de 003 ne permettent pas de préférer l'un des deux IDs.

**CORRECTION TECHNIQUE CERTAINE :** état de double revendication objectivement établi ; ni le texte imprimé ni le bon verset d'appel ne suffisent à corriger *un ID particulier*. **Zéro correction canonique exécutable indépendamment de la décision de Ludo**.

**DÉCISION ÉDITORIALE — LUDO :** déterminer l'identité unique ou la politique d'alias et autoriser le traitement de l'autre fiche et de `psalm-032.noteIds`.

## Verdicts individuels — source → appel → pied → candidats

### 1. `book-06-psalm-040-note-002`

- **FAIT ÉTABLI :** 155 mots sur **un seul** pied imprimé en p.325, appel local n°1, au terme du psaume 40. JSON : `marker=1`, `verse=null`, texte **identique intégralement** à `book-06-psalm-040-note-003` et même source.
- **HYPOTHÈSE :** doublon d'extraction ; aucune preuve d'une identité de fichier indépendante de l'autre candidat.
- **CORRECTION TECHNIQUE CERTAINE :** correspondance lexicale et double revendication confirmées, mais **aucune modification canonique sûre** sans arbitrage.
- **DÉCISION ÉDITORIALE — LUDO :** déterminer identité canonique ou alias entre `book-06-psalm-040-note-002` et `book-06-psalm-040-note-003`, et approuver le traitement des références `noteIds`.
- **PREUVES :** [064-02](../064/064-02_VERDICTS.md), [065-02](../065/065-02_VERDICTS.md), [Action 39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216), artefact `12426161529`. JSON `data/notes/books/book-06/book-06-psalm-040-note-002.json` (blob `9ad3912424df20935f57dc1af7d2dd708f5d85c7`) ; psaume `data/corpus/books/book-06/psalm-040.json` (blob `3bfd2aec41ac420ba33a0d02325aa7a1862d638a`).
- **PREUVE MANQUANTE :** provenance de l'ID indépendant de l'ordre d'extraction et du champ de verset, plus politique sûre de réconciliation. **VERDICT : NON RÉSOLUE.**

### 2. `book-06-psalm-040-note-003`

- **FAIT ÉTABLI :** 155 mots sur **un seul** pied imprimé en p.325, appel local n°1, au terme du psaume 40 ; verse=11 déclaré dans 003. JSON : `marker=1`, `verse=11`, texte **identique intégralement** à `book-06-psalm-040-note-002` et même source.
- **HYPOTHÈSE :** doublon d'extraction ; aucune preuve d'une identité de fichier indépendante de l'autre candidat.
- **CORRECTION TECHNIQUE CERTAINE :** correspondance lexicale et double revendication confirmées, mais **aucune modification canonique sûre** sans arbitrage.
- **DÉCISION ÉDITORIALE — LUDO :** déterminer identité canonique ou alias entre `book-06-psalm-040-note-003` et `book-06-psalm-040-note-002`, et approuver le traitement des références `noteIds`.
- **PREUVES :** [064-02](../064/064-02_VERDICTS.md), [065-02](../065/065-02_VERDICTS.md), [Action 39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216), artefact `12426161529`. JSON `data/notes/books/book-06/book-06-psalm-040-note-003.json` (blob `19619cfca526ea6d776b82e765c9b85708a12160`) ; psaume `data/corpus/books/book-06/psalm-040.json` (blob `3bfd2aec41ac420ba33a0d02325aa7a1862d638a`).
- **PREUVE MANQUANTE :** provenance de l'ID indépendant de l'ordre d'extraction et du champ de verset, plus politique sûre de réconciliation. **VERDICT : NON RÉSOLUE.**

### 3. `book-07-psalm-032-note-002`

- **FAIT ÉTABLI :** 5 mots sur **un seul** pied imprimé en p.381, appel local n°1 du verset 27 selon la preuve 064-03. JSON : `marker=1`, `verse=null`, texte **identique intégralement** à `book-07-psalm-032-note-003` et même source.
- **HYPOTHÈSE :** doublon d'extraction ; aucune preuve d'une identité de fichier indépendante de l'autre candidat.
- **CORRECTION TECHNIQUE CERTAINE :** correspondance lexicale et double revendication confirmées, mais **aucune modification canonique sûre** sans arbitrage.
- **DÉCISION ÉDITORIALE — LUDO :** déterminer identité canonique ou alias entre `book-07-psalm-032-note-002` et `book-07-psalm-032-note-003`, et approuver le traitement des références `noteIds`.
- **PREUVES :** [064-03](../064/064-03_VERDICTS.md), [065-02](../065/065-02_VERDICTS.md), [Action 39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426552703`. JSON `data/notes/books/book-07/book-07-psalm-032-note-002.json` (blob `c926718098c74047624c37218149baf71ac4e72f`) ; psaume `data/corpus/books/book-07/psalm-032.json` (blob `be8873404f67f5e924149e0a45d38a94e39525ee`).
- **PREUVE MANQUANTE :** provenance de l'ID indépendant de l'ordre d'extraction et du champ de verset, plus politique sûre de réconciliation. **VERDICT : NON RÉSOLUE.**

### 4. `book-07-psalm-032-note-003`

- **FAIT ÉTABLI :** 5 mots sur **un seul** pied imprimé en p.381, appel local n°1 du verset 27 selon la preuve 064-03 ; verse=27 déclaré dans 003. JSON : `marker=1`, `verse=27`, texte **identique intégralement** à `book-07-psalm-032-note-002` et même source.
- **HYPOTHÈSE :** doublon d'extraction ; aucune preuve d'une identité de fichier indépendante de l'autre candidat.
- **CORRECTION TECHNIQUE CERTAINE :** correspondance lexicale et double revendication confirmées, mais **aucune modification canonique sûre** sans arbitrage.
- **DÉCISION ÉDITORIALE — LUDO :** déterminer identité canonique ou alias entre `book-07-psalm-032-note-003` et `book-07-psalm-032-note-002`, et approuver le traitement des références `noteIds`.
- **PREUVES :** [064-03](../064/064-03_VERDICTS.md), [065-02](../065/065-02_VERDICTS.md), [Action 39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426552703`. JSON `data/notes/books/book-07/book-07-psalm-032-note-003.json` (blob `fbd669171cd2ba415d6cdb2ebb6d5e039a2aa7b5`) ; psaume `data/corpus/books/book-07/psalm-032.json` (blob `be8873404f67f5e924149e0a45d38a94e39525ee`).
- **PREUVE MANQUANTE :** provenance de l'ID indépendant de l'ordre d'extraction et du champ de verset, plus politique sûre de réconciliation. **VERDICT : NON RÉSOLUE.**

## Contrôles documentaires spécialisés

- **PASS** — Plan officiel : 4 ID exacts.
- **PASS** — Préconditions : 066-03 NON COMMENCÉE.
- **PASS** — Quatre IDs de note et deux IDs de psaume corrects.
- **PASS** — Texte 06/040 identique sur les deux fichiers.
- **PASS** — Texte 07/032 identique sur les deux fichiers.
- **PASS** — 06/040 page 325, même marker imprimé local 1.
- **PASS** — 07/032 page 381, même marker imprimé local 1.
- **PASS** — 06/040 verset déclaré null contre 11.
- **PASS** — 07/032 verset déclaré null contre 27.
- **PASS** — 06/040 référence réciproque des deux notes.
- **PASS** — 07/032 référence réciproque des deux notes.
- **PASS** — Deux pages incluses dans les périmètres de psaumes.
- **PASS** — Quatre statuts machine encore en revue.
- **PASS** — Métadonnées de longueur : absence de textLength déclarée, texte conservé sans mutation.

**14/14 contrôles ciblés PASS.** Aucun PDF original rouvert, aucune nouvelle GitHub Action, aucun audit du corpus. Les deux preuves visuelles restent celles de 064.

## Résolution éventuelle après décision de Ludo

Une proposition réversible serait d'identifier une fiche primaire et de garder l'autre comme trace/alias avec provenance explicite. Aucun choix entre 002 et 003 n'est démontré : Ludo doit approuver le principe, l'identité, les fichiers modifiables et le traitement de `noteIds`. Dans une mission ultérieure, sauvegarder les SHA des deux notes et du psaume, contrôler pied affiché une fois, intégralité des deux textes et absence de références orphelines. **Aucune de ces opérations n'est effectuée.**

**Clôture : 4/4 toujours NON RÉSOLUES, 0 authentification et 0 correction. Bilan global : 44 NON RÉSOLUES, 2 corrigées et authentifiées durant 065 ; aucun cas résolu pendant 066-03. PR #72 DRAFT sans fusion. STOP après 066-03 ; 066-04 NON COMMENCÉE.**
