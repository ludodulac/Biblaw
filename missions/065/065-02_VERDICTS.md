# 🌸 BIBLAW — MISSION 065-02 — VERDICTS DU PREMIER LOT

**Statut : TERMINÉE — 4 notes examinées ; 0 authentifiée, 0 corrigée, 4 NON RÉSOLUES.** Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT à l'entrée. HEAD de reprise : `fea0f790a844d774da23f30737de2e4a4ff1ae50`. Périmètre strict issu de `065_PLAN.md` : les quatre identifiants ci-dessous et aucun autre.

## Méthode et portée des preuves

Les rapports 064-02 et 064-03 documentent déjà la lecture visuelle des deux pages PDF pertinentes, **p.325 et p.381**, et l'existence d'un **seul pied imprimé par paire**, avec exactement les mêmes textes et marqueurs dans deux notes distinctes. Les artefacts d'Actions ont été vérifiés existants et non expirés en 065-02. Les quatre JSON canoniques et les deux enregistrements de psaume ont été relus **sans mutation**, pour contrôler les IDs, pages, renvois, textes, statuts techniques et pointeurs de verset. **PDF original non rouvert** : un second examen de la même occurrence imprimée ne fournit pas, à lui seul, la preuve manquante d'unicité de l'ID extrait. Les tests/actions 064 historiques sont réutilisés ; aucune CI spécialisée 065-02 exécutée à distance.

Le fait que les `-003` comportent un verset explicite (`11` / `27`) tandis que les `-002` ont `verse=null` est **une différence de métadonnées extraites, non une preuve de préférence canonique**. Aucun des quatre IDs ne peut être promu par seule préférence pour un champ plus renseigné. Les deux psaumes référencent chacun les deux IDs concurrents dans `noteIds` ; toute décision aurait une conséquence de cohérence sur le corpus protégé.

## Décisions individuelles — dans l'ordre du plan

### 1. `book-06-psalm-040-note-002`

- **Verdict précédent (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-02) :** **NON RÉSOLUE**.
- **Justification :** Le seul appel local n°1 et le seul pied de 155 mots sur la page 325 sont aussi revendiqués intégralement par `-003`. Les deux JSON portent le marqueur 1, le même psaume et la même page ; `-002` possède `appliesTo.verse = null`, sans attribut probant d'identité distincte.
- **Preuves utilisées :** [064-02_VERDICTS.md](../064/064-02_VERDICTS.md), [run #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216), artefact A `12426161529` (`biblaw-064-02-proof-A`: image p.325, layout, `note-proof.json`) ; `data/notes/books/book-06/book-06-psalm-040-note-002.json` (blob `9ad3912424df20935f57dc1af7d2dd708f5d85c7`) et le `noteIds` du psaume associé.
- **Ce qui manque pour conclure :** Une traçabilité d'extraction ou une règle canonique documentée désignant explicitement lequel des deux IDs représente l'unique pied, avec résolution sûre des références `noteIds`. Le seul fait que `-002` ait un ordinal inférieur ne constitue pas une preuve.
- **Correction :** aucune ; texte, rattachement et statut technique préservés.

### 2. `book-06-psalm-040-note-003`

- **Verdict précédent (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-02) :** **NON RÉSOLUE**.
- **Justification :** Le texte, l'appel imprimé n°1, la page 325 et le psaume sont strictement identiques à `-002`. `-003` indique `appliesTo.verse = 11`, mais ce renseignement de source machine ne prouve pas à lui seul le choix du fichier canonique ; un seul pied est imprimé.
- **Preuves utilisées :** [064-02_VERDICTS.md](../064/064-02_VERDICTS.md), [run #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216), artefact A `12426161529` (`biblaw-064-02-proof-A`: image p.325, layout, `note-proof.json`) ; `data/notes/books/book-06/book-06-psalm-040-note-003.json` (blob `19619cfca526ea6d776b82e765c9b85708a12160`) et le `noteIds` du psaume associé.
- **Ce qui manque pour conclure :** Preuve documentaire reliant sans ambiguïté cet identifiant précis à la seule occurrence imprimée, plutôt que l'identifiant `-002`, et méthode de réconciliation des deux références canoniques sans perte.
- **Correction :** aucune ; texte, rattachement et statut technique préservés.

### 3. `book-07-psalm-032-note-002`

- **Verdict précédent (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-02) :** **NON RÉSOLUE**.
- **Justification :** La page 381 comporte un seul appel/pied imprimé n°1 « Évangile selon Matthieu 18:20. » (5 tokens). Le JSON `-002` et le JSON `-003` contiennent le même texte, même page, marqueur 1 et psaume ; `-002` indique `appliesTo.verse = null`.
- **Preuves utilisées :** [064-03_VERDICTS.md](../064/064-03_VERDICTS.md), [run #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact A `12426552703` (`biblaw-064-03-proof-A`: image p.381, layout, `note-proof.json`) ; `data/notes/books/book-07/book-07-psalm-032-note-002.json` (blob `c926718098c74047624c37218149baf71ac4e72f`) et le `noteIds` du psaume associé.
- **Ce qui manque pour conclure :** Une provenance ou règle d'attribution certifiée permettant d'élire un des deux identifiants, plus la sécurisation des `noteIds`; ni le numéro ordinal ni le manque de numéro de verset ne sont une preuve suffisante.
- **Correction :** aucune ; texte, rattachement et statut technique préservés.

### 4. `book-07-psalm-032-note-003`

- **Verdict précédent (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-02) :** **NON RÉSOLUE**.
- **Justification :** Le texte de cinq tokens, l'unique pied p.381 et le marqueur 1 sont les mêmes que pour `-002`. `-003` porte `appliesTo.verse = 27`, cohérent avec le rapprochement documentaire de 064-03, mais la précision de ce champ ne certifie pas que `-003` est l'identifiant canonique plutôt que `-002`.
- **Preuves utilisées :** [064-03_VERDICTS.md](../064/064-03_VERDICTS.md), [run #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact A `12426552703` (`biblaw-064-03-proof-A`: image p.381, layout, `note-proof.json`) ; `data/notes/books/book-07/book-07-psalm-032-note-003.json` (blob `fbd669171cd2ba415d6cdb2ebb6d5e039a2aa7b5`) et le `noteIds` du psaume associé.
- **Ce qui manque pour conclure :** Preuve externe au doublon extrait établissant l'ID unique à conserver et sa relation au renvoi du verset 27, puis processus sûr de réconciliation des références. La page PDF déjà inspectée en 064-03 ne comporte pas de second appel.
- **Correction :** aucune ; texte, rattachement et statut technique préservés.

## Tests spécialisés et contrôles (065-02)

Tests documentaires ciblés exécutés sur les données GitHub du HEAD d'entrée (contrôles structuraux en lecture seule, **pas une exécution de GitHub Actions**). Tous passés :

- ✅ 4 identifiants distincts strictement dans le lot 065-02.
- ✅ 06/040 : textes exactement identiques.
- ✅ 07/032 : textes exactement identiques.
- ✅ 06/040 : même psaume, page 325, marqueur 1.
- ✅ 07/032 : même psaume, page 381, marqueur 1.
- ✅ 06/040 : verse null versus 11.
- ✅ 07/032 : verse null versus 27.
- ✅ psaumes : deux notes référencées par paire.
- ✅ pages figurent dans la portée déclarée.
- ✅ aucune des quatre notes n'est techniquement authentifiée.
- ✅ fichiers originaux JSON indépendants.
- ✅ progress indique 065-02 non commencée (pas de travail préexistant).

**Résultat : 12/12 contrôles réussis.** Les deux doublons déjà présents ont été **constatés**, aucun nouveau doublon ni aucun troisième appel n'a été créé. Les quatre fichiers de note et les deux fichiers de psaume n'ont fait l'objet d'aucune modification. Le commit 065-02 ne porte que de la documentation de mission ; les trois workflows généraux préexistants en échec ne sont pas réparés ni relancés.

**Empreintes des quatre fichiers de note contrôlés :**

- `data/notes/books/book-06/book-06-psalm-040-note-002.json` — blob `9ad3912424df20935f57dc1af7d2dd708f5d85c7`
- `data/notes/books/book-06/book-06-psalm-040-note-003.json` — blob `19619cfca526ea6d776b82e765c9b85708a12160`
- `data/notes/books/book-07/book-07-psalm-032-note-002.json` — blob `c926718098c74047624c37218149baf71ac4e72f`
- `data/notes/books/book-07/book-07-psalm-032-note-003.json` — blob `fbd669171cd2ba415d6cdb2ebb6d5e039a2aa7b5`

## Clôture 065-02

- **4/4 notes du lot traitées** ; **0 AUTHENTIFIÉE**, **0 CORRIGÉE ET AUTHENTIFIÉE**, **4 NON RÉSOLUES**, dont deux conflits binaires de provenance.
- Aucun PDF réouvert : l'indécision ne porte pas sur la présence ou le texte du pied imprimé mais sur **l'identifiant unique** à lui attribuer. Toute correction/suppression fondée sur le seul ordre des numéros serait une hypothèse.
- **Bilan cumulé 065 :** 4 des 46 notes de l'inventaire traitées en phase de résolution ; **0 résolue**, **46 NON RÉSOLUES** au total (4 revues en 065-02, 42 autres lots à traiter). Les 146 authentifications 064 restent inchangées.
- Aucun texte canonique, note, psaume, prière, interface, catalogue, publication ni déploiement modifié ; pas de fusion PR #72. **STOP après 065-02.**
