# 🌸 BIBLAW — MISSION 066-11 — NOTES SOUS PR.93 ET PR.76

**STATUT : TERMINÉE — 2/2 notes examinées ; 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE ; 2 NON RÉSOLUES.** Aucune modification canonique.

## 1. Mission, branche, méthode et archives

- Plan officiel [066_PLAN](066_PLAN.md), lot **066-11 C** : **uniquement** `book-30-psalm-211-note-001` et `book-31-psalm-184-note-001` ; [inventaire](066_INVENTAIRE.md), [protocole 066-02](066-02_PROTOCOL.md). Aucun autre dossier revu ; les missions 066-02 à 066-10 restent intactes.
- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 **OPEN/DRAFT, non fusionnée** au seul contrôle initial. HEAD de base `c293c0babf329b24b5a22a25a901f582b268528d`, conforme au HEAD communiqué.
- [Verdicts 065-08](../065/065-08_VERDICTS.md) et inspections visuelles [064-15/A](../064/064-15_VERDICTS.md) p.2952–2953 (Action [40137180838](https://github.com/ludodulac/Biblaw/actions/runs/40137180838), artefact **12576971728**) et [064-16/A](../064/064-16_VERDICTS.md) p.3004–3005 (Action [40187665402](https://github.com/ludodulac/Biblaw/actions/runs/40187665402), artefact **12597171008**) réutilisés. Les **deux artefacts existent et ne sont pas expirés**. Aucun PDF original rouvert, aucune nouvelle Action/CI.
- Application de **source → appel → pied local → note JSON → psaume et prière autonomes**. Les constatations sur l'impression proviennent des preuves **visuelles archivées 064**, celles sur l'état actuel des fichiers des comparaisons en lecture seule au HEAD de base.

## 2. Tableau du rattachement imprimé et de conservation

| Note | Support du renvoi imprimé | Pied local unique | Pages source du psaume | Prière autonome et pages déclarées | Références |
|---|---|---|---|---|---|
| `book-30-psalm-211-note-001` | **Pr.93** « Amin¹ » à la fin de Pr.93 | n°1, **28/28 tokens**, p.**2953**, texte JSON 156 caractères | `[2948, 2949, 2950, 2951, 2952]` — **p.2953 absente** | `gabriel-book-30-prayer-093` ; `printedPages=[2952]` — **p.2953 absente** | `psalm.noteIds` inclut la note 1 fois ; **aucun lien explicite note→prière** |
| `book-31-psalm-184-note-001` | **Pr.76** « la nouvelle génération des dieux¹ » dans Pr.76 | n°1, **71/71 tokens**, p.**3005**, texte JSON 377 caractères | `[3002, 3003, 3004]` — **p.3005 absente** | `raphael-book-31-prayer-076` ; `printedPages=[3004]` — **p.3005 absente** | `psalm.noteIds` inclut la note 1 fois ; **aucun lien explicite note→prière** |

**Conservation absolue :** les **deux champs `note.text`** et les **deux champs `prayer.text`** restent intégralement présents dans les JSON au HEAD de base, avec empreintes Git ci-dessous ; aucune coupe, extraction, normalisation ou édition n'est opérée. Le `1` de chaque appel est conservé dans le texte de sa prière autonome. **Limite de preuve :** la présence de ces chaînes ne certifie pas à elle seule que *la prière entière* reproduit parfaitement le document imprimé ; aucune réinspection/recollation du texte intégral de la prière originale n'a été lancée. **Ne jamais conclure qu'un fragment est supprimable** sans preuve indépendante et autorisation.

## 3. Verdict individuel — `book-30-psalm-211-note-001`

**FAITS ÉTABLIS.** Les sources 064 et 065 attestent **une seule note imprimée locale n°1 de 28 tokens**, au pied de la **p.2953** ; texte intégral du pied correspondant à `note.text` (**156 caractères**), sans duplication/composite supplémentaire documenté dans ce lot. Son appel imprimé « Amin¹ » à la fin de Pr.93 appartient à la **prière Pr.93**, et **non** à un verset du psaume `book-30-psalm-211`. Le psaume n'inclut **pas** la p.2953 dans `source.pdfPages`, bien que `noteIds` réfère l'ID une fois. La prière `gabriel-book-30-prayer-093` existe, est reliée éditorialement à ce psaume, et son `text` de **1728 caractères** contient exactement la séquence d'appel **`Amin1.`**, avec un seul marqueur numérique local de renvoi « 1 ». La prière n'a **pas** de liste de `noteIds` propre.

**MÉTADONNÉES DE PAGES.** `prayer.source.printedPages=[2952]`, **sans p.2953** où est le pied imprimé ; la preuve archivistique situe le renvoi dans la prière, mais la **sémantique des `printedPages`** (pages de texte de prière, pages d'appel, ou pages de pied de note) reste à préciser. Ne pas ajouter une page par supposition.

**HYPOTHÈSES.** Extraction ou importation a probablement associé à tort la note de la prière au psaume voisin sur la seule proximité éditoriale ; aucune preuve ne démontre le mécanisme exact. L'absence de second ID noté dans les archives du cas ne prouve pas une unicité absolue à l'échelle de tout le corpus.

**CORRECTIONS TECHNIQUES DÉMONTRÉES (mais non appliquées).** Support de l'appel **Pr.93** et page de pied **2953** sont déterminés ; pas de verset de psaume à attribuer, texte du pied déjà séparé dans `note.text`, **aucune troncature ni correction de chaîne justifiée**. Les métadonnées actuelles ne permettent pas un lien direct explicite de la note à la prière ; une adaptation du modèle est **nécessaire pour exprimer fidèlement le support imprimé**, mais son schéma n'est pas choisi ni mis en place.

**DÉCISIONS RÉSERVÉES À LUDO.** Approuver le modèle direct de lien note→prière (ID de la prière, marqueur local, emplacement, page), sa coexistence ou migration par rapport à `psalm.noteIds`, la définition de `printedPages`, et la liste des JSON et tests concernés **avant toute mutation**. Sans cette autorisation et la vérification ultérieure de l'intégrité complète des prières, verdict **NON RÉSOLUE**.

**Snapshot SHA (Git blob, HEAD de base) :** note `data/notes/books/book-30/book-30-psalm-211-note-001.json` → `ab7c7ad3d16df369f3d72137e4b1442b7b8e7410` ; psaume `data/corpus/books/book-30/psalm-211.json` → `b34d4ed1a2da760d84a9f27a6f828b0eee5c5b82` ; prière `data/prayers/gabriel-book-30-prayer-093.json` → `35fba5eaa242a37aa91c9677cd2a100197658cf9`.

## 4. Verdict individuel — `book-31-psalm-184-note-001`

**FAITS ÉTABLIS.** Les sources 064 et 065 attestent **une seule note imprimée locale n°1 de 71 tokens**, au pied de la **p.3005** ; texte intégral du pied correspondant à `note.text` (**377 caractères**), sans duplication/composite supplémentaire documenté dans ce lot. Son appel imprimé « la nouvelle génération des dieux¹ » dans Pr.76 appartient à la **prière Pr.76**, et **non** à un verset du psaume `book-31-psalm-184`. Le psaume n'inclut **pas** la p.3005 dans `source.pdfPages`, bien que `noteIds` réfère l'ID une fois. La prière `raphael-book-31-prayer-076` existe, est reliée éditorialement à ce psaume, et son `text` de **1742 caractères** contient exactement la séquence d'appel **`nouvelle génération des dieux1`**, avec un seul marqueur numérique local de renvoi « 1 ». La prière n'a **pas** de liste de `noteIds` propre.

**MÉTADONNÉES DE PAGES.** `prayer.source.printedPages=[3004]`, **sans p.3005** où est le pied imprimé ; la preuve archivistique situe le renvoi dans la prière, mais la **sémantique des `printedPages`** (pages de texte de prière, pages d'appel, ou pages de pied de note) reste à préciser. Ne pas ajouter une page par supposition.

**HYPOTHÈSES.** Extraction ou importation a probablement associé à tort la note de la prière au psaume voisin sur la seule proximité éditoriale ; aucune preuve ne démontre le mécanisme exact. L'absence de second ID noté dans les archives du cas ne prouve pas une unicité absolue à l'échelle de tout le corpus.

**CORRECTIONS TECHNIQUES DÉMONTRÉES (mais non appliquées).** Support de l'appel **Pr.76** et page de pied **3005** sont déterminés ; pas de verset de psaume à attribuer, texte du pied déjà séparé dans `note.text`, **aucune troncature ni correction de chaîne justifiée**. Les métadonnées actuelles ne permettent pas un lien direct explicite de la note à la prière ; une adaptation du modèle est **nécessaire pour exprimer fidèlement le support imprimé**, mais son schéma n'est pas choisi ni mis en place.

**DÉCISIONS RÉSERVÉES À LUDO.** Approuver le modèle direct de lien note→prière (ID de la prière, marqueur local, emplacement, page), sa coexistence ou migration par rapport à `psalm.noteIds`, la définition de `printedPages`, et la liste des JSON et tests concernés **avant toute mutation**. Sans cette autorisation et la vérification ultérieure de l'intégrité complète des prières, verdict **NON RÉSOLUE**.

**Snapshot SHA (Git blob, HEAD de base) :** note `data/notes/books/book-31/book-31-psalm-184-note-001.json` → `310ba084905f01e32ba723b97d7f00fb0a30744b` ; psaume `data/corpus/books/book-31/psalm-184.json` → `5c511fdd13222db3a26e7788cce31aad44a79e07` ; prière `data/prayers/raphael-book-31-prayer-076.json` → `05aa8514f64f428fa78cf68698f70c8694599c0f`.

## 4. Scénario de réconciliation documentaire — NON EXÉCUTÉ

1. Maintenir les identifiants de note actuels et les textes canoniques **tels quels** tant que Ludo n'a pas validé de schéma. Décrire chaque association **sans l'implémenter** : `book-30-psalm-211-note-001` → `gabriel-book-30-prayer-093` (Pr.93, renvoi « Amin¹ », p.2953), `book-31-psalm-184-note-001` → `raphael-book-31-prayer-076` (Pr.76, « génération des dieux¹ », p.3005).
2. Définir explicitement la sémantique `printedPages`. Les deux prières ont leurs appels conservés dans `text`, mais leurs tableaux de pages **excluent les pages des pieds**. C'est une **discordance de couverture**, non une permission de compléter automatiquement les pages.
3. Si une future migration est autorisée : vérifier le texte intégral **de chaque prière imprimée** contre `prayer.text`, l'intégrité de chaque note, les pages et marqueurs, la conservation de tous les caractères, la réciprocité des liens, l'absence d'orphelin, l'absence de double pied logique et le diff limité aux fichiers nommément autorisés.
4. **Alerte préexistante 066-08 conservée, hors périmètre :** **1 679 caractères** du composite historique **26/189** ne sont pas retrouvés dans le psaume actuel, leur conservation ailleurs est **NON DÉMONTRÉE**. Aucun retrait de ces caractères ni nouvel examen de ce dossier.

## 5. Contrôles documentaires spécialisés (lecture seule)

- **PASS** — Périmètre 066-11 exactement deux ID du plan.
- **PASS** — Inventaire : deux notes affectées à 066-11.
- **PASS** — Protocole 066-02 : conservation, support prière, décision de Ludo.
- **PASS** — Mission initialement non commencée ; arbre git disponible.
- **PASS** — 30/211/001 : ID note rattaché au psaume attendu.
- **PASS** — 30/211/001 : source du pied p.2953 hors source du psaume.
- **PASS** — 30/211/001 : pied local marqueur 1, aucun verset désigné.
- **PASS** — 30/211/001 : prière autonome Pr.93 et lien éditorial au psaume.
- **PASS** — 30/211/001 : présence de l'appel imprimé au sein du texte de la prière.
- **PASS** — 30/211/001 : unique marqueur numérique de renvoi '1' dans la prière.
- **PASS** — 30/211/001 : noteIds une seule fois dans psaume.
- **PASS** — 30/211/001 : printedPages de la prière ne couvre que p.2952.
- **PASS** — 30/211/001 : texte du pied présent intégralement, 156 caractères.
- **PASS** — 30/211/001 : relation noteIds non matérialisée en prière.
- **PASS** — 30/211/001 : note en révision, pas authentifiée.
- **PASS** — 30/211/001 : texte autonome de prière complet comme champ stocké (aucune altération).
- **PASS** — 31/184/001 : ID note rattaché au psaume attendu.
- **PASS** — 31/184/001 : source du pied p.3005 hors source du psaume.
- **PASS** — 31/184/001 : pied local marqueur 1, aucun verset désigné.
- **PASS** — 31/184/001 : prière autonome Pr.76 et lien éditorial au psaume.
- **PASS** — 31/184/001 : présence de l'appel imprimé au sein du texte de la prière.
- **PASS** — 31/184/001 : unique marqueur numérique de renvoi '1' dans la prière.
- **PASS** — 31/184/001 : noteIds une seule fois dans psaume.
- **PASS** — 31/184/001 : printedPages de la prière ne couvre que p.3004.
- **PASS** — 31/184/001 : texte du pied présent intégralement, 377 caractères.
- **PASS** — 31/184/001 : relation noteIds non matérialisée en prière.
- **PASS** — 31/184/001 : note en révision, pas authentifiée.
- **PASS** — 31/184/001 : texte autonome de prière complet comme champ stocké (aucune altération).
- **PASS** — Les deux sources de prière sont distinctes et leurs pieds sont uniques dans leurs archives.
- **PASS** — Alerte permanente 1 679 caractères maintenue dans documents en entrée.

**30/30 contrôles PASS** en lecture seule. Aucun test général, aucun PDF rouvert, aucun nouvel audit de mission précédente.

**CLÔTURE : 066-11 TERMINÉE, 2/2 notes examinées, 0 authentifiée, 0 corrigée, 2 NON RÉSOLUES. Cumul 066-03 à 066-11 : 25/44 dossiers examinés ; 44 NON RÉSOLUES, aucun fichier canonique modifié. PR #72 DRAFT, non fusionnée. STOP — 066-12 NON COMMENCÉE.**
