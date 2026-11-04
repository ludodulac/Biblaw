# 🌸 BIBLAW — MISSION 066-05 — DEUX PAIRES CONCURRENTES À L’APPEL DU VERSET 20

**Statut : TERMINÉE — 4/4 notes du plan ; 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES. Aucune modification canonique.**

## Reprise et portée probatoire

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`. PR #72 **OPEN / DRAFT, non fusionnée** lors de la vérification initiale unique ; HEAD de départ `af6d74c947544d86b54e628474462bc6f613488f` conforme à la valeur communiquée.
- Périmètre issu exclusivement du [plan 066-05](066_PLAN.md) : `book-30-psalm-215-note-004`, `book-30-psalm-215-note-005`, `book-35-psalm-218-note-002`, `book-35-psalm-218-note-003` ; aucune autre note du corpus traitée.
- [Protocole de preuve 066-02](066-02_PROTOCOL.md) appliqué : **source→appel→pied imprimé→candidats**, distinction entre certitude sur l'occurrence physique, hypothèse d'extraction et choix d'identité canonique par Ludo. L’ordinal du fichier n'est pas le marqueur local.
- **Preuves archivées réutilisées, PDF non rouvert :** [064-15/B](../064/064-15_VERDICTS.md), p.2971 (artefact `12577911782`, [Action 40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177)), [064-19/A](../064/064-19_VERDICTS.md), p.3495 (artefact `12650754088`, [Action 40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710)) ; 064-19/B pour la fiche 003 p.3495 (artefact `12651183390`, [Action 40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034)) et [065-04](../065/065-04_VERDICTS.md). **Trois artefacts non expirés** ; aucun nouveau PDF, workflow ou audit de corpus.
- Quatre notes JSON et deux psaumes lus **en lecture seule**, au HEAD de départ : égalité intégrale du `text`, `source.pdfPage`, marqueur local, `appliesTo.recordId`, `verse`, `noteIds`, pages des versets 20, statut de validation et SHA des blobs.

## Pied physique A — psaume 30/215, p.2971

- **FAIT ÉTABLI :** [064-15/B](../064/064-15_VERDICTS.md) décrit **un seul** pied imprimé local n°1 de **17/17 tokens** sur la page 2971 ; son appel est au **verset 20**, « Père Michaël ». Il renvoie à l'Évangile de l'Archange Michaël, psaume 216. Les JSON 004 et 005 reprennent la **même chaîne complète de 90 caractères**, même source, page, marqueur 1, et sont tous deux dans `book-30-psalm-215.noteIds`.
- **HYPOTHÈSE :** doublon technique produit par l'extraction. Le `verse=null` de 004 et `verse=20` de 005 constituent des **métadonnées différentes**, pas la provenance de l'ID canonique.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** **double revendication d'un unique pied imprimé** démontrée, et emplacement du renvoi au v.20 documenté. **Aucune correction canonique ciblant l'un des IDs n'est certaine sans choix éditorial** ; les deux textes sont déjà conformes à l'imprimé selon 064.
- **DÉCISION ÉDITORIALE — LUDO :** décider quel ID conserve l'identité du pied, ou approuver un dispositif d'alias/archivage qui garde la provenance, puis autoriser la réconciliation de `noteIds` ; pas de suppression ni de règle arbitraire fondée sur 004/005.

## Pied physique B — psaume 35/218, p.3495

- **FAIT ÉTABLI :** [064-19/A et B](../064/064-19_VERDICTS.md) démontrent **un seul** pied imprimé n°1 de **45/45 tokens** p.3495, appelé au **verset 20** après « enfant ». Les JSON 002 et 003 contiennent **265 caractères exactement identiques**, même page, marqueur et psaume ; les deux IDs sont dans `book-35-psalm-218.noteIds`.
- **HYPOTHÈSE :** une double extraction a produit deux IDs pour la même occurrence. `verse=null` (002) face à `verse=20` (003) n'identifie pas le bon fichier.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** **double représentation** et unicité de l'imprimé confirmées. L'alignement au v.20 peut guider une éventuelle réparation de liens, mais **ne rend pas autonome le fichier 003**. Aucune correction de texte ou d'ID indépendante n'est démontrée.
- **DÉCISION ÉDITORIALE — LUDO :** arbitrage documenté 002↔003, possibilité d'alias/archivage réversible, puis approbation du traitement des références `noteIds` et des fiches, sans perte de texte.

## Verdicts individuels selon l'ordre du plan

### 1. `book-30-psalm-215-note-004`

- **FAIT ÉTABLI :** pied imprimé **unique** n°1 p.2971 de **17/17 tokens** ; champ `appliesTo.verse=null`, texte entier **identique** à `book-30-psalm-215-note-005` (**90 caractères**). Le pied de 17/17 tokens renvoie à l'Évangile de l'Archange Michaël, psaume 216 ; appel imprimé au verset 20 (« Père Michaël »). Le numéro 004 désigne une extraction, non un marqueur imprimé 4.
- **HYPOTHÈSE :** duplication de l'extraction, sans preuve documentaire de l'identité canonique de ce fichier comparé à l'autre.
- **CORRECTION TECHNIQUE CERTAINE :** égalité intégrale et double revendication démontrées ; **aucune mutation sûre de cet ID/verse/noteIds** sans arbitrage éditorial et mandat spécifique.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** documenter la provenance ou valider une règle explicite pour départager `book-30-psalm-215-note-004` et `book-30-psalm-215-note-005`, décider l'archivage/alias et autoriser la réconciliation des références du psaume.
- **PREUVES :** [064-15_VERDICTS.md](../064/064-15_VERDICTS.md), [065-04](../065/065-04_VERDICTS.md), [Action 40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177), artefact `12577911782` ; note `data/notes/books/book-30/book-30-psalm-215-note-004.json` (blob `b4d01b16fe5e9e2629f5d4032d6dca95d0075b3d`) ; psaume `data/corpus/books/book-30/psalm-215.json` (blob `9a90fa5904597241398347a0c265d4b109c5b3f2`).
- **PREUVE MANQUANTE :** traçabilité de l'ID canonique indépendante de la seule valeur `verse=20`, ainsi qu'un plan autorisé et non destructif de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 2. `book-30-psalm-215-note-005`

- **FAIT ÉTABLI :** pied imprimé **unique** n°1 p.2971 de **17/17 tokens** ; champ `appliesTo.verse=20`, texte entier **identique** à `book-30-psalm-215-note-004` (**90 caractères**). Même unique pied n°1, rattaché au v.20 dans la preuve historique. La valeur `verse=20` de 005 peut localiser l'appel, pas attribuer l'ID canonique.
- **HYPOTHÈSE :** duplication de l'extraction, sans preuve documentaire de l'identité canonique de ce fichier comparé à l'autre.
- **CORRECTION TECHNIQUE CERTAINE :** égalité intégrale et double revendication démontrées ; **aucune mutation sûre de cet ID/verse/noteIds** sans arbitrage éditorial et mandat spécifique.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** documenter la provenance ou valider une règle explicite pour départager `book-30-psalm-215-note-005` et `book-30-psalm-215-note-004`, décider l'archivage/alias et autoriser la réconciliation des références du psaume.
- **PREUVES :** [064-15_VERDICTS.md](../064/064-15_VERDICTS.md), [065-04](../065/065-04_VERDICTS.md), [Action 40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177), artefact `12577911782` ; note `data/notes/books/book-30/book-30-psalm-215-note-005.json` (blob `aa1b33222e08ae532a783c372271d61a7b49200f`) ; psaume `data/corpus/books/book-30/psalm-215.json` (blob `9a90fa5904597241398347a0c265d4b109c5b3f2`).
- **PREUVE MANQUANTE :** traçabilité de l'ID canonique indépendante de la seule valeur `verse=20`, ainsi qu'un plan autorisé et non destructif de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 3. `book-35-psalm-218-note-002`

- **FAIT ÉTABLI :** pied imprimé **unique** n°1 p.3495 de **45/45 tokens** ; champ `appliesTo.verse=null`, texte entier **identique** à `book-35-psalm-218-note-003` (**265 caractères**). Un pied imprimé unique n°1 sur « l'enfant », appelé au verset 20 de 35/218. La preuve 064-19/A couvre cet ID et la p.3495.
- **HYPOTHÈSE :** duplication de l'extraction, sans preuve documentaire de l'identité canonique de ce fichier comparé à l'autre.
- **CORRECTION TECHNIQUE CERTAINE :** égalité intégrale et double revendication démontrées ; **aucune mutation sûre de cet ID/verse/noteIds** sans arbitrage éditorial et mandat spécifique.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** documenter la provenance ou valider une règle explicite pour départager `book-35-psalm-218-note-002` et `book-35-psalm-218-note-003`, décider l'archivage/alias et autoriser la réconciliation des références du psaume.
- **PREUVES :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md), [065-04](../065/065-04_VERDICTS.md), [Action 40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710), artefact `12650754088` ; note `data/notes/books/book-35/book-35-psalm-218-note-002.json` (blob `2afd3c4729ac89a1e21fa77b69af203b3d1b3ef2`) ; psaume `data/corpus/books/book-35/psalm-218.json` (blob `c3f06ad37e5396cf7e5cea48ce35f9f355abcb4b`).
- **PREUVE MANQUANTE :** traçabilité de l'ID canonique indépendante de la seule valeur `verse=20`, ainsi qu'un plan autorisé et non destructif de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

### 4. `book-35-psalm-218-note-003`

- **FAIT ÉTABLI :** pied imprimé **unique** n°1 p.3495 de **45/45 tokens** ; champ `appliesTo.verse=20`, texte entier **identique** à `book-35-psalm-218-note-002` (**265 caractères**). Même pied unique n°1 sur « l'enfant » ; la preuve 064-19/B atteste aussi que 003 revendique le même contenu. Verse=20 ne tranche pas le choix de l'ID.
- **HYPOTHÈSE :** duplication de l'extraction, sans preuve documentaire de l'identité canonique de ce fichier comparé à l'autre.
- **CORRECTION TECHNIQUE CERTAINE :** égalité intégrale et double revendication démontrées ; **aucune mutation sûre de cet ID/verse/noteIds** sans arbitrage éditorial et mandat spécifique.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** documenter la provenance ou valider une règle explicite pour départager `book-35-psalm-218-note-003` et `book-35-psalm-218-note-002`, décider l'archivage/alias et autoriser la réconciliation des références du psaume.
- **PREUVES :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md), [065-04](../065/065-04_VERDICTS.md), [Action 40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034), artefact `12651183390` ; note `data/notes/books/book-35/book-35-psalm-218-note-003.json` (blob `37bdc0453dacb9a59f18feff9ec6652ead96c5c4`) ; psaume `data/corpus/books/book-35/psalm-218.json` (blob `c3f06ad37e5396cf7e5cea48ce35f9f355abcb4b`).
- **PREUVE MANQUANTE :** traçabilité de l'ID canonique indépendante de la seule valeur `verse=20`, ainsi qu'un plan autorisé et non destructif de réconciliation des `noteIds`. **VERDICT : NON RÉSOLUE.**

## Contrôles spécialisés

- **PASS** — Plan officiel : exactement les quatre IDs 066-05.
- **PASS** — Inventaire : quatre IDs assignés à 066-05.
- **PASS** — Protocole 066-02 : marqueur local, préservation et décisions Ludo.
- **PASS** — 066-05 NON COMMENCÉE et commit parent valide.
- **PASS** — Quatre IDs et recordIds des notes conformes.
- **PASS** — 30/215 : texte strictement égal sur deux notes, 90 caractères.
- **PASS** — 35/218 : texte strictement égal sur deux notes, 265 caractères.
- **PASS** — 30/215 : source identique, page 2971, marqueur imprimé 1.
- **PASS** — 35/218 : source identique, page 3495, marqueur imprimé 1.
- **PASS** — 30/215 : différence verse null/20.
- **PASS** — 35/218 : différence verse null/20.
- **PASS** — 30/215 : notes réciproquement référencées dans noteIds.
- **PASS** — 35/218 : notes réciproquement référencées dans noteIds.
- **PASS** — Pages 2971 et 3495 comprises dans les psaumes.
- **PASS** — Verset 20 présent sur la page de chaque pied.
- **PASS** — Quatre statuts machine nécessitent une revue, aucun promu.
- **PASS** — Textes des notes non composites et longueur calculée sans champ textLength.

**17/17 contrôles PASS** sur les quatre notes JSON et deux psaumes du seul lot, le plan et le protocole. Les constats d'unicité de pieds proviennent des inspections déjà archivées en 064 et ne sont **pas** de nouvelles vérifications visuelles.

## Conditions futures de correction — non exécutées

Ludo doit fournir soit une provenance qui justifie une identité précise, soit une décision éditoriale explicite pour la conserver ; toute proposition de neutralisation/alias doit préserver SHA, historique et texte, puis prévoir la correction de `noteIds` avec contrôle d'absence de références orphelines et d'un seul pied logique par appel. Les mutations ne sont ni décidées ni autorisées par le seul rapport 066-05.

**Bilan 066-05 : 4/4 traitées, 0 AUTHENTIFIÉE, 0 CORRIGÉE, 4 NON RÉSOLUES. Bilan cumulé : 44 NON RÉSOLUES (2 corrigées et authentifiées en 065, aucune correction dans 066). PDF non rouvert, corpus inchangé, PR #72 DRAFT sans fusion. STOP — 066-06 NON COMMENCÉE.**
