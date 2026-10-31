# 🌸 BIBLAW — 066_PLAN — RÉSOLUTION ENVISAGÉE DES 44 ANOMALIES

**066-01 = planification sans correction.** Les missions suivantes sont des **propositions**, non des instructions de construction exécutables sans validation distincte de Grand-père BIBLAW et de Ludo. L'ordre A→E donne les priorités ; des dépendances sur les règles de provenance, sur le schéma note→prière et sur la conservation des textes peuvent imposer une autre séquence.

## Contrats de sécurité et distinction technique/éditoriale

- **Faits techniques/documentaires certains :** texte et limites des pieds selon preuves archivées, correspondance préfixe/suffixe des JSON, page et appel imprimés, présence/absence de prière autonome. Ils peuvent donner lieu à une **rectification dans la documentation 066** sans mutation du corpus.
- **Décisions éditoriales :** élection d'un identifiant canonique, regroupement/archivage de notes, migration du lien note→prière, création ou reconstruction de prière, restauration de verset, modification de noteIds. Ces opérations exigent **l'autorisation explicite de Ludo**. Une concordance imprimée ne prouve pas une identité de fichier.
- **Aucune perte de texte :** avant tout retrait d'un fragment composite, confirmer sa conservation complète dans un fichier canonique distinct ou autoriser et certifier sa restauration ; conserver la provenance et contrôler les liens.
- **Tests ciblés :** IDs, support, texte entier, pages, marqueur, verset, unicité de pied, sauvegarde des suffixes et intégrité des références. Pas d'audit global du corpus, de nouveau workflow général, de publication ou de fusion.
- **Anti-boucle :** ne pas recommencer les vérifications 064/065 ; deux tentatives maximum pour une opération technique ; en absence de preuve, NON RÉSOLUE, documenter et arrêter. Écritures éventuelles sur HEAD vérifié, expected_sha, sans force push.
- **Périmètre :** le lot A 066-02 est **transversal** ; les lots pilotes 066-03 à 066-20 affectent chacun des 44 IDs **une seule fois**. Une note peut relever de plusieurs problèmes, mais une seule mission principale responsable de sa résolution.

## Tableau de missions courtes et indépendantes

| Mission proposée | Priorité | IDs pilotes | Objectif | État |
|---|---|---:|---|---|
| 066-02 | A | 44 (transversal) | Convention des preuves et corrections documentaires certaines | PROPOSÉE — NON COMMENCÉE |
| 066-03 | B | 4 | Paires simples 06/040 et 07/032 | PROPOSÉE — NON COMMENCÉE |
| 066-04 | B | 4 | Paires simples 07/047 et 08/025 | PROPOSÉE — NON COMMENCÉE |
| 066-05 | B | 4 | Paires simples 30/215 et 35/218 | PROPOSÉE — NON COMMENCÉE |
| 066-06 | B | 2 | Pied composite et ID concurrents 33/230 | PROPOSÉE — NON COMMENCÉE |
| 066-07 | B | 2 | Concurrents historiques et rattachement verset | PROPOSÉE — NON COMMENCÉE |
| 066-08 | B | 2 | Concurrents historiques 23/133 et 26/189 | PROPOSÉE — NON COMMENCÉE |
| 066-09 | B | 2 | Concurrents 30/200 et inter-psaumes 35/215 | PROPOSÉE — NON COMMENCÉE |
| 066-10 | C | 3 | Notes sous Pr.11, 53 et 71 | PROPOSÉE — NON COMMENCÉE |
| 066-11 | C | 2 | Notes sous Pr.93 et Pr.76 | PROPOSÉE — NON COMMENCÉE |
| 066-12 | C | 4 | Collisions sous Pr.38 et Pr.90 | PROPOSÉE — NON COMMENCÉE |
| 066-13 | C | 2 | Collision de notes sous Pr.63 | PROPOSÉE — NON COMMENCÉE |
| 066-14 | D | 2 | Suites manquantes de Pr.32 et Pr.54 (livre 21) | PROPOSÉE — NON COMMENCÉE |
| 066-15 | D | 2 | Suite Pr.41 et Pr.36 absente | PROPOSÉE — NON COMMENCÉE |
| 066-16 | D | 2 | Suites Pr.54 (livre 26) et Pr.102 (livre 29) | PROPOSÉE — NON COMMENCÉE |
| 066-17 | D+B | 2 | Pr.102 livre 35 et double identité 35/213 | PROPOSÉE — NON COMMENCÉE |
| 066-18 | E | 2 | Pieds distincts fusionnés 07/035 et 12/077 | PROPOSÉE — NON COMMENCÉE |
| 066-19 | E | 2 | Composite 23/129 et verset tronqué 22/155 | PROPOSÉE — NON COMMENCÉE |
| 066-20 | E | 1 | Graphie et identifiants 29/216 | PROPOSÉE — NON COMMENCÉE |

## Cahiers de mission détaillés

### 066-02 — A — Convention des preuves et corrections documentaires certaines

- **Objectif :** Établir les règles de provenance, de conservation et de décision, sans revisiter le PDF ; enregistrer les divergences déjà certaines (23/129 versets 38–40, 35/214 page incorrecte, statut machine).
- **Identifiants :** les **44 IDs de [066_INVENTAIRE.md](066_INVENTAIRE.md)** en référence transversale, sans affectation pilote et sans réexamen.
- **Fichiers à examiner :** `missions/065/065_INVENTAIRE.md` ; `missions/065/065_PLAN.md` ; `missions/065/065-02_VERDICTS.md … 065-13_VERDICTS.md` ; `missions/065/065-13_VERDICTS.md` ; sources documentaires [065-02](../065/065-02_VERDICTS.md), [065-03](../065/065-03_VERDICTS.md), [065-04](../065/065-04_VERDICTS.md), [065-05](../065/065-05_VERDICTS.md), [065-06](../065/065-06_VERDICTS.md), [065-07](../065/065-07_VERDICTS.md), [065-08](../065/065-08_VERDICTS.md), [065-09](../065/065-09_VERDICTS.md), [065-10](../065/065-10_VERDICTS.md), [065-11](../065/065-11_VERDICTS.md), [065-12](../065/065-12_VERDICTS.md), [065-13](../065/065-13_VERDICTS.md).
- **Preuves manquantes et démarche :** Gabarit source→appel→pied→candidats ; protocole de neutralisation non destructive et d'autorisation. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Toute règle proposée n'est pas une décision de migration.
- **Conditions de réussite :** 44 IDs référencés, gabarit approuvé comme documentation, zéro préférence d'ID.
- **Tests nécessaires :** Comptage 44 IDs, vérification des citations et des corrections purement documentaires.
- **Risques :** La convention risque d'être prise à tort pour une autorisation de migration.
- **Autorisations éventuelles :** Pas d'accord pour documenter ; Ludo doit approuver toute règle éditoriale appliquée à des données.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-03 — B — Paires simples 06/040 et 07/032

- **Objectif :** Deux pieds uniques revendiqués chacun par deux IDs.
- **Identifiants :** `book-06-psalm-040-note-002`, `book-06-psalm-040-note-003`, `book-07-psalm-032-note-002`, `book-07-psalm-032-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-06/book-06-psalm-040-note-002.json` ; `data/corpus/books/book-06/psalm-040.json` ; `data/notes/books/book-06/book-06-psalm-040-note-003.json` ; `data/notes/books/book-07/book-07-psalm-032-note-002.json` ; `data/corpus/books/book-07/psalm-032.json` ; `data/notes/books/book-07/book-07-psalm-032-note-003.json` ; sources documentaires [065-02](../065/065-02_VERDICTS.md).
- **Preuves manquantes et démarche :** Réutiliser 064-02/03 et comparer texte/page/appel/verse sans prioriser le plus petit ordinal. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Provenance explicite ou maintien NON RÉSOLUE, références prévues sans perte.
- **Tests nécessaires :** Égalité des textes, unicité des renvois, noteIds.
- **Risques :** Sélection arbitraire d'un numéro d'ID.
- **Autorisations éventuelles :** Ludo pour arbitrage, archivage d'ID et noteIds.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-04 — B — Paires simples 07/047 et 08/025

- **Objectif :** Départager deux autres paires de pieds uniques.
- **Identifiants :** `book-07-psalm-047-note-002`, `book-07-psalm-047-note-003`, `book-08-psalm-025-note-002`, `book-08-psalm-025-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-07/book-07-psalm-047-note-002.json` ; `data/corpus/books/book-07/psalm-047.json` ; `data/notes/books/book-07/book-07-psalm-047-note-003.json` ; `data/notes/books/book-08/book-08-psalm-025-note-002.json` ; `data/corpus/books/book-08/psalm-025.json` ; `data/notes/books/book-08/book-08-psalm-025-note-003.json` ; sources documentaires [065-03](../065/065-03_VERDICTS.md).
- **Preuves manquantes et démarche :** Rapprocher 064-03/04 et provenance des extractions. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Une décision sourcée par paire, ou blocage consigné ; aucune mutation non autorisée.
- **Tests nécessaires :** Contrôle texte, appel local, page, référentiel de liens.
- **Risques :** Confusion du champ verse renseigné avec preuve d'ID.
- **Autorisations éventuelles :** Ludo pour choix d'ID et correction du catalogue.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-05 — B — Paires simples 30/215 et 35/218

- **Objectif :** Rapprocher les deux paires partageant un appel au v.20.
- **Identifiants :** `book-30-psalm-215-note-004`, `book-30-psalm-215-note-005`, `book-35-psalm-218-note-002`, `book-35-psalm-218-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-30/book-30-psalm-215-note-004.json` ; `data/corpus/books/book-30/psalm-215.json` ; `data/notes/books/book-30/book-30-psalm-215-note-005.json` ; `data/notes/books/book-35/book-35-psalm-218-note-002.json` ; `data/corpus/books/book-35/psalm-218.json` ; `data/notes/books/book-35/book-35-psalm-218-note-003.json` ; sources documentaires [065-04](../065/065-04_VERDICTS.md).
- **Preuves manquantes et démarche :** Réutiliser les captures 064-15/B et 064-19/B, pas de relecture générale. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Pieds uniques et alternatives identifiés sans double comptage.
- **Tests nécessaires :** Égalité exacte, marqueur, référence noteIds.
- **Risques :** Création d'un deuxième pied inexistant.
- **Autorisations éventuelles :** Ludo pour décisions d'identité et références.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-06 — B — Pied composite et ID concurrents 33/230

- **Objectif :** Isoler conceptuellement le pied de 6 tokens des versets 23–25.
- **Identifiants :** `book-33-psalm-230-note-002`, `book-33-psalm-230-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-33/book-33-psalm-230-note-002.json` ; `data/corpus/books/book-33/psalm-230.json` ; `data/notes/books/book-33/book-33-psalm-230-note-003.json` ; sources documentaires [065-10](../065/065-10_VERDICTS.md).
- **Preuves manquantes et démarche :** Vérifier l'égalité exacte des versets du composite et énoncer les options de provenance. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Six tokens conservés une fois et 100 tokens de corps non perdus après éventuelle décision.
- **Tests nécessaires :** Test exact du préfixe et suffixe canonique, référence au v.14.
- **Risques :** Troncature prématurée ou duplicat non résolu.
- **Autorisations éventuelles :** Ludo pour choix 002/003 et modifications de notes/noteIds.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-07 — B — Concurrents historiques et rattachement verset

- **Objectif :** Distinguer les IDs corrects des composites 063, dont le renvoi p.3690 au v.36.
- **Identifiants :** `book-27-psalm-169-note-004`, `book-37-psalm-250-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-27/book-27-psalm-169-note-004.json` ; `data/corpus/books/book-27/psalm-169.json` ; `data/notes/books/book-27/book-27-psalm-169-note-002.json` ; `data/notes/books/book-37/book-37-psalm-250-note-003.json` ; `data/corpus/books/book-37/psalm-250.json` ; `data/notes/books/book-37/book-37-psalm-250-note-002.json` ; sources documentaires [065-11](../065/065-11_VERDICTS.md), [065-12](../065/065-12_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer les concurrents 27/169/002 et 37/250/002 sans les retraiter ; consigner verset 11 erroné. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Un plan de réconciliation par pied, avec preuves indépendantes.
- **Tests nécessaires :** Préfixes, pages, appel v.30 et fin v.36, noteIds.
- **Risques :** Perte des suffixes des vieux composites.
- **Autorisations éventuelles :** Ludo pour arbitrage et corrections des liens/versets.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-08 — B — Concurrents historiques 23/133 et 26/189

- **Objectif :** Rapprocher les pieds de 8 et 29 tokens de leurs composites 063.
- **Identifiants :** `book-23-psalm-133-note-004`, `book-26-psalm-189-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-23/book-23-psalm-133-note-004.json` ; `data/corpus/books/book-23/psalm-133.json` ; `data/notes/books/book-23/book-23-psalm-133-note-003.json` ; `data/notes/books/book-26/book-26-psalm-189-note-003.json` ; `data/corpus/books/book-26/psalm-189.json` ; `data/notes/books/book-26/book-26-psalm-189-note-002.json` ; sources documentaires [065-13](../065/065-13_VERDICTS.md).
- **Preuves manquantes et démarche :** Proposer une provenance de l'ID canonique, garder les anciens fichiers inchangés. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Chaque occurrence physique a une attribution justifiée ou un blocage précis.
- **Tests nécessaires :** Appel unique, préfixe exact et conservation des références.
- **Risques :** Double promotion d'un même pied.
- **Autorisations éventuelles :** Ludo pour arbitrage et archivage.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-09 — B — Concurrents 30/200 et inter-psaumes 35/215

- **Objectif :** Traiter le composite Pr.83 et le doublon 35/214/002 rattaché au mauvais psaume.
- **Identifiants :** `book-30-psalm-200-note-003`, `book-35-psalm-215-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-30/book-30-psalm-200-note-003.json` ; `data/corpus/books/book-30/psalm-200.json` ; `data/notes/books/book-30/book-30-psalm-200-note-002.json` ; `data/notes/books/book-35/book-35-psalm-215-note-001.json` ; `data/corpus/books/book-35/psalm-215.json` ; `data/notes/books/book-35/book-35-psalm-214-note-002.json` ; `data/corpus/books/book-35/psalm-214.json` ; sources documentaires [065-13](../065/065-13_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer source p.2901, puis p.3485 et pages du psaume 214 sans changer ses données. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Preuve de conservation de Pr.83 et scénario cohérent entre les deux psaumes.
- **Tests nécessaires :** Préfixe 111 tokens, égalité 24 tokens, page 3485/absence v.36 dans 214.
- **Risques :** Déplacer une note à tort ou perdre une continuation de prière.
- **Autorisations éventuelles :** Ludo pour décisions inter-psaumes, noteIds et toute prière à restaurer.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-10 — C — Notes sous Pr.11, 53 et 71

- **Objectif :** Préparer les trois rattachements explicites note→prière.
- **Identifiants :** `book-17-psalm-115-note-001`, `book-27-psalm-158-note-001`, `book-27-psalm-177-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-17/book-17-psalm-115-note-001.json` ; `data/corpus/books/book-17/psalm-115.json` ; `data/prayers/michael-book-17-prayer-011.json` ; `data/notes/books/book-27/book-27-psalm-158-note-001.json` ; `data/corpus/books/book-27/psalm-158.json` ; `data/prayers/raphael-book-27-prayer-053.json` ; `data/notes/books/book-27/book-27-psalm-177-note-001.json` ; `data/corpus/books/book-27/psalm-177.json` ; `data/prayers/raphael-book-27-prayer-071.json` ; sources documentaires [065-07](../065/065-07_VERDICTS.md).
- **Preuves manquantes et démarche :** Confronter renvoi, page et texte des prières autonomes avec les 064. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Trois supports prière prouvés, sans attribuer un verset de psaume.
- **Tests nécessaires :** Page hors psaume, marqueur dans prière, unicité, printedPages.
- **Risques :** Fausse attribution par voisinage et noteId orphelin.
- **Autorisations éventuelles :** Ludo pour schéma note→prière et modifications de liens.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-11 — C — Notes sous Pr.93 et Pr.76

- **Objectif :** Rattacher deux pieds imprimés sous des prières après leurs psaumes.
- **Identifiants :** `book-30-psalm-211-note-001`, `book-31-psalm-184-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-30/book-30-psalm-211-note-001.json` ; `data/corpus/books/book-30/psalm-211.json` ; `data/prayers/gabriel-book-30-prayer-093.json` ; `data/notes/books/book-31/book-31-psalm-184-note-001.json` ; `data/corpus/books/book-31/psalm-184.json` ; `data/prayers/raphael-book-31-prayer-076.json` ; sources documentaires [065-08](../065/065-08_VERDICTS.md).
- **Preuves manquantes et démarche :** Utiliser 064-15/16 ; confronter pages 2953/3005 et appels des prières. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Plan de lien direct avec pages d'origine, sans faux verset.
- **Tests nécessaires :** Textes 28/71 tokens, source hors psaume, pages des prières.
- **Risques :** Rattachement erroné à un psaume.
- **Autorisations éventuelles :** Ludo pour schéma et modification des métadonnées.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-12 — C — Collisions sous Pr.38 et Pr.90

- **Objectif :** Réconcilier deux pieds sous Pr.38 et un pied sous Pr.90 revendiqué deux fois.
- **Identifiants :** `book-21-psalm-143-note-003`, `book-21-psalm-143-note-004`, `book-29-psalm-199-note-002`, `book-29-psalm-199-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-21/book-21-psalm-143-note-003.json` ; `data/corpus/books/book-21/psalm-143.json` ; `data/prayers/michael-book-21-prayer-038.json` ; `data/notes/books/book-21/book-21-psalm-143-note-002.json` ; `data/notes/books/book-21/book-21-psalm-143-note-004.json` ; `data/notes/books/book-29/book-29-psalm-199-note-002.json` ; `data/corpus/books/book-29/psalm-199.json` ; `data/prayers/michael-book-29-prayer-090.json` ; `data/notes/books/book-29/book-29-psalm-199-note-003.json` ; sources documentaires [065-09](../065/065-09_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer le composite 21/143/004 aux pieds 002 et 003, puis le pied p.2751 vs page 2750 déclarée. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Plan d'identité sans suppression ni création de pied imaginaire.
- **Tests nécessaires :** Égalité des deux pieds, pages et marqueurs, noteIds.
- **Risques :** Pr.38 corrompue ou choix forcé du 29/199/003.
- **Autorisations éventuelles :** Ludo pour arbitrage et schéma prière/notes.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-13 — C — Collision de notes sous Pr.63

- **Objectif :** Départager les deux fiches du même renvoi « Amin Salama » sous Pr.63.
- **Identifiants :** `book-27-psalm-169-note-003`, `book-27-psalm-169-note-005`.
- **Fichiers à examiner :** `data/notes/books/book-27/book-27-psalm-169-note-003.json` ; `data/corpus/books/book-27/psalm-169.json` ; `data/prayers/raphael-book-27-prayer-063.json` ; `data/notes/books/book-27/book-27-psalm-169-note-005.json` ; sources documentaires [065-11](../065/065-11_VERDICTS.md).
- **Preuves manquantes et démarche :** Réutiliser 064-13 et la prière autonome ; distinguer v.42 du renvoi imprimé. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Lien note→Pr.63 et identité prouvée ou NON RÉSOLUE.
- **Tests nécessaires :** 48 tokens identiques, unicité, noteIds, appel p.2536.
- **Risques :** Transformer un renvoi de prière en pied de verset 42.
- **Autorisations éventuelles :** Ludo pour modèle de lien et ID retenu.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-14 — D — Suites manquantes de Pr.32 et Pr.54 (livre 21)

- **Objectif :** Proposer la restauration des continuations Pr.32 et Pr.54 contenues dans des notes.
- **Identifiants :** `book-21-psalm-137-note-001`, `book-21-psalm-160-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-21/book-21-psalm-137-note-001.json` ; `data/corpus/books/book-21/psalm-137.json` ; `data/prayers/michael-book-21-prayer-032.json` ; `data/notes/books/book-21/book-21-psalm-160-note-001.json` ; `data/corpus/books/book-21/psalm-160.json` ; `data/prayers/michael-book-21-prayer-054.json` ; sources documentaires [065-06](../065/065-06_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer limites de pieds et suffixes archivés (362, 1889 caractères) avec fichiers de prières. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Continuation intégralement préservée avant découpe de note.
- **Tests nécessaires :** Diff exact des suffixes, pages et emplacement.
- **Risques :** Perdre du texte de prière.
- **Autorisations éventuelles :** Ludo pour éditer prières et notes.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-15 — D — Suite Pr.41 et Pr.36 absente

- **Objectif :** Préparer la restitution de Pr.41 et l'éventuelle création de Pr.36.
- **Identifiants :** `book-23-psalm-145-note-001`, `book-24-psalm-141-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-23/book-23-psalm-145-note-001.json` ; `data/corpus/books/book-23/psalm-145.json` ; `data/prayers/raphael-book-23-prayer-041.json` ; `data/notes/books/book-24/book-24-psalm-141-note-001.json` ; `data/corpus/books/book-24/psalm-141.json` ; `data/prayers/ouriel-book-24-prayer-036.json (fichier absent — prouvé 065-06)` ; sources documentaires [065-06](../065/065-06_VERDICTS.md).
- **Preuves manquantes et démarche :** Exploiter 064-12, vérifier texte complet et numéro de prière plutôt que présumer l'existence. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Pr.41 vérifiée, Pr.36 prouvée avant toute création.
- **Tests nécessaires :** Appels, bornes, pages 2020–2021 et 2134–2135, texte non perdu.
- **Risques :** Créer un faux fichier de prière ou l'amputer.
- **Autorisations éventuelles :** Ludo pour création de Pr.36 et édition de Pr.41/notes.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-16 — D — Suites Pr.54 (livre 26) et Pr.102 (livre 29)

- **Objectif :** Préparer la conservation de deux continuations de prières absentes des autonomes.
- **Identifiants :** `book-26-psalm-169-note-001`, `book-29-psalm-212-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-26/book-26-psalm-169-note-001.json` ; `data/corpus/books/book-26/psalm-169.json` ; `data/prayers/gabriel-book-26-prayer-054.json` ; `data/notes/books/book-29/book-29-psalm-212-note-001.json` ; `data/corpus/books/book-29/psalm-212.json` ; `data/prayers/michael-book-29-prayer-102.json` ; sources documentaires [065-07](../065/065-07_VERDICTS.md), [065-12](../065/065-12_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer les suffixes et appels 064-12/14, distinguer note de psaume et note de prière. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Suites complètes, prière correcte et lien note→Pr.102 sans perte.
- **Tests nécessaires :** Texte suffixe, marqueur ecclesia, pages, noteIds.
- **Risques :** Supprimer le seul exemplaire des fins de prière.
- **Autorisations éventuelles :** Ludo pour compléter prières et modifier relations.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-17 — D+B — Pr.102 livre 35 et double identité 35/213

- **Objectif :** Rétablir la suite manquante de Pr.102 et arbitrer deux composites identiques.
- **Identifiants :** `book-35-psalm-213-note-002`, `book-35-psalm-213-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-35/book-35-psalm-213-note-002.json` ; `data/corpus/books/book-35/psalm-213.json` ; `data/prayers/raphael-book-35-prayer-102.json` ; `data/notes/books/book-35/book-35-psalm-213-note-003.json` ; sources documentaires [065-10](../065/065-10_VERDICTS.md).
- **Preuves manquantes et démarche :** Séparer dans un projet le pied initial de 55 tokens et la continuation de prière (autonome actuellement 137 caractères). Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Suffixe conservé dans une prière complète avant modification des deux IDs.
- **Tests nécessaires :** Égalité stricte 002/003, bornes du pied et présence des ~400 tokens de suite.
- **Risques :** Perdre une longue continuation ou produire deux pieds.
- **Autorisations éventuelles :** Ludo pour restauration, choix d'ID et noteIds.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-18 — E — Pieds distincts fusionnés 07/035 et 12/077

- **Objectif :** Proposer le traitement d'un composite de deux pieds déjà conservés et d'un de trois pieds sans fiches séparées.
- **Identifiants :** `book-07-psalm-035-note-005`, `book-12-psalm-077-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-07/book-07-psalm-035-note-005.json` ; `data/corpus/books/book-07/psalm-035.json` ; `data/notes/books/book-07/book-07-psalm-035-note-003.json` ; `data/notes/books/book-07/book-07-psalm-035-note-004.json` ; `data/notes/books/book-12/book-12-psalm-077-note-001.json` ; `data/corpus/books/book-12/psalm-077.json` ; sources documentaires [065-05](../065/065-05_VERDICTS.md).
- **Preuves manquantes et démarche :** Comparer 064-03/05 ; conserver 07/035/003/004 sans retravailler leurs verdicts, créer un plan pour trois pieds 12/077. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Un pied imprimé par enregistrement, sans suppression de pieds 2/3.
- **Tests nécessaires :** Bornes, nombre de pieds, texte exact, noteIds.
- **Risques :** Effacer les pieds 2 et 3 ou créer doublons.
- **Autorisations éventuelles :** Ludo pour archivage composite et création/édition de notes et psaume.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-19 — E — Composite 23/129 et verset tronqué 22/155

- **Objectif :** Traiter le composite note/versets/Pr.26 et la fin manquante du verset 21.
- **Identifiants :** `book-23-psalm-129-note-003`, `book-22-psalm-155-note-001`.
- **Fichiers à examiner :** `data/notes/books/book-23/book-23-psalm-129-note-003.json` ; `data/corpus/books/book-23/psalm-129.json` ; `data/prayers/raphael-book-23-prayer-026.json` ; `data/notes/books/book-23/book-23-psalm-129-note-004.json` ; `data/notes/books/book-22/book-22-psalm-155-note-001.json` ; `data/corpus/books/book-22/psalm-155.json` ; sources documentaires [065-12](../065/065-12_VERDICTS.md).
- **Preuves manquantes et démarche :** Contrôler la divergence 38–45 du rapport 064 vs 38–40 des JSON ; restituer les 22 tokens de 22/155 avant toute réduction. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Conservation prouvée dans Pr.26 et psaume ; note 23/129/004 authentifiée non dupliquée.
- **Tests nécessaires :** Diff des versets 38–40, Pr.26 intégrale, jonction « après la mort. ».
- **Risques :** Perte de la seule fin de verset ou double note.
- **Autorisations éventuelles :** Ludo pour modification du psaume 22/155 et des notes/noteIds.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

### 066-20 — E — Graphie et identifiants 29/216

- **Objectif :** Préciser l'écart audelà/au-delà sans masquer 29/216/002 historique.
- **Identifiants :** `book-29-psalm-216-note-003`.
- **Fichiers à examiner :** `data/notes/books/book-29/book-29-psalm-216-note-003.json` ; `data/corpus/books/book-29/psalm-216.json` ; `data/notes/books/book-29/book-29-psalm-216-note-002.json` ; sources documentaires [065-11](../065/065-11_VERDICTS.md).
- **Preuves manquantes et démarche :** Contrôler la graphie du pied 78 tokens et arbitrer l'identité avant correction éventuelle. Voir les obstacles propres à chaque ID dans [066_INVENTAIRE.md](066_INVENTAIRE.md). Aucun ID n'est retenu sans provenance sourcée.
- **Conditions de réussite :** Une seule identité prouvée ; correction textuelle fidèle seulement si validée.
- **Tests nécessaires :** 78 tokens et 77 extraits, préfixe composite, appel v.11.
- **Risques :** Rectifier l'orthographe mais laisser une double identité.
- **Autorisations éventuelles :** Ludo pour arbitrage, correction de texte et références.
- **Statut :** PROPOSÉE, NON COMMENCÉE ; aucune mutation autorisée à ce stade.

## Dépendances communes et choix restant à Ludo

1. **A en amont des mutations :** établir et approuver si nécessaire le contrat de provenance des IDs, de conservation de texte et de statut humain ; sans ce contrat, conserver NON RÉSOLUE plutôt que supprimer un doublon.
2. **B par pied physique :** les lots de paires et d'anciens composites sont indépendants les uns des autres ; ne modifier un candidat historique 063 que dans un mandat explicitement étendu à ce fichier.
3. **C avant changement de rattachement :** faire valider un schéma note→prière sans supposer qu'un `psalm.noteIds` valide un appel de psaume ; Pr.38, Pr.90 et Pr.63 cumulent ce problème avec un choix d'ID.
4. **D avant réduction de composites :** conserver le texte de Pr.32, Pr.54, Pr.41, Pr.36, Pr.102 (livres 29 et 35 distincts) dans l'autonome approprié. `24/141/001` nécessite une **création** de Pr.36 si l'absence est confirmée ; `35/213/002–003` doit être traité ensemble.
5. **E après préservation du texte :** note 12/077 = trois pieds, 23/129 = pied+versets+Pr.26, 22/155 = verset 21 amputé, 29/216 = graphie divergente et ID concurrent. La seule correction lexicale ne clôt pas un conflit d'identité.
6. **Portée stricte 066-01 :** aucune correction lancée, aucune nouvelle mission activée, aucune page PDF rouverte. **Attendre la validation de Grand-père BIBLAW et de Ludo.**

**Contrôle du plan : 44 ID distincts, aucune omission ni double affectation principale, 18 lots pilotes adaptés aux dépendances ; 066-02 est un préalable transversal.**
