# 🌸 BIBLAW — MISSION 066-02 — CONVENTION DES PREUVES

**Statut : TERMINÉE — protocole documentaire seulement.** Lot transversal A ; 44 identifiants NON RÉSOLUS documentés, aucun ID élu, aucune note, psaume ou prière modifiés.

## 1. Objet strict du plan

Le [plan officiel 066](066_PLAN.md) assigne à 066-02 la **convention des preuves et corrections documentaires certaines** : règles de provenance, de conservation et de décision, gabarit source→appel→pied→candidats, neutralisation non destructive et règles d'autorisation. Les 44 ID de [066_INVENTAIRE.md](066_INVENTAIRE.md) sont concernés **en référence transversale**, sans réexamen individuel du PDF ou modification des lots pilotes 066-03 à 066-20.

**Base documentaire :** verdicts [065-02 à 065-13](../065/065_PROGRESS.md), rapports 064 et artefacts déjà cités par chaque dossier de [066_INVENTAIRE.md](066_INVENTAIRE.md). PR #72 OPEN/DRAFT lors de l'unique contrôle initial ; HEAD de base `1ad2fd19f499c78e759aaf605949e3a7e522a6d5`. Les conclusions historiques ne sont ni rouvertes ni réécrites.

## 2. Certitude documentaire ≠ choix éditorial

| Catégorie de preuve | Ce qu'elle établit | Ce qu'elle ne permet jamais seule |
|---|---|---|
| **Preuve visuelle 064 archivée** | Pied réellement imprimé : page, numéro local, texte, limites, position du renvoi et support (psaume ou prière). | Le bon **ID JSON canonique** entre deux extractions concurrentes. |
| **Contrôle technique 065** | Identité de chaîne, préfixe/suffixe, contenu de `noteIds`, champs `pdfPage`, `printedPages`, `appliesTo`, présence d'un fichier de prière. | Une identité historique ni une autorisation de corriger. |
| **Hypothèse** | Schéma probable de contamination, choix d'identifiant ou rattachement envisageable. | Une authentification, même si la concordance des tokens est parfaite. |
| **Décision de Ludo** | Autorise explicitement identité, migration, archivage, création de prière, restitution de verset et mutations **nommées**. | Une suppression si l'invariant de conservation n'est pas démontré. |

Le **marqueur imprimé n°1** se réinitialise localement et **n'est pas** le suffixe `-note-001` du fichier. Une valeur `appliesTo.verse` plus précise, un ordre lexical ou `validation.status=machine-extracted-source-boundary-audited` ne valent pas AUTHENTIFIÉE.

## 3. Gabarit opérationnel : source → appel → pied → candidats

Pour un pied physique, remplir les éléments suivants **sans modifier le corpus** :

| Champ | Contenu exigé |
|---|---|
| `original_document` | Référence PDF et **rapport 064** certifié, Action, identifiant d'artefact et page réellement inspectée. |
| `printed_footnote` | Page, marqueur **local**, début et fin du texte, nombre de tokens selon le verdict, limites typographiques. |
| `call_site` | Support exact **PSAUME** (ID+verset), **PRIÈRE** (ID+Pr.), ou **NON ÉTABLI** ; citation du renvoi imprimé. |
| `candidate_note_ids` | **Tous** les candidats 065/063/064 concernés, même ceux hors des 44, sans en élire aucun. |
| `metadata_snapshot` | Source, page, `appliesTo`, `noteIds` et SHA des fichiers au HEAD de la mission **future autorisée**. |
| `segments_and_destinations` | Chaque élément du composite (pied 1, pied 2, verset, prière) avec sa destination canonique déjà vérifiée ou **DESTINATION NON PROUVÉE**. |
| `evidence_grade` | FAIT ARCHIVÉ / CONCORDANCE TECHNIQUE / HYPOTHÈSE / DÉCISION ÉDITORIALE requise. |
| `missing_evidence` | Question précise bloquante ; si non résolue, verdict **NON RÉSOLUE** conservé. |
| `proposed_migration` | Alternatives de traitement **non exécutées** et plan des renvois `noteIds` avant/après, sans suppression arbitraire. |
| `authorization` | Approbation explicite de Ludo : identité retenue, liste de JSON, schéma note→prière, toute modification. |
| `integrity_tests` | Égalité exacte des fragments, aucun texte perdu, aucun pied dédoublé, aucune référence orpheline, diff limité. |

**Clé de rapprochement à valeur documentaire seulement :** document imprimé + page + marqueur local + emplacement de l'appel + support + limites textuelles. Il ne s'agit **pas** d'une clé canonique automatique. Deux notes ayant le même texte peuvent être des occurrences distinctes ; une occurrence revendiquée par deux IDs ne peut être authentifiée deux fois.

## 4. Règles de conservation sans perte

1. Photographier les valeurs et références des **deux côtés** d'un lien (`note.appliesTo`, `psalm.noteIds`, prière autonome) et enregistrer les SHA au HEAD futur ; aucune écriture dans ce lot.
2. Segmenter les composites en fonction des limites prouvées en 064/065 ; ne pas assimiler automatiquement le suffixe à un texte superflu.
3. Prouver la **conservation intégrale** de chaque fragment dans un enregistrement canonique adapté **avant** toute troncature. Sinon, préserver le composite et consigner le blocage.
4. Pour un pied imprimé sous Pr.11, Pr.38, Pr.53, Pr.63, Pr.90, Pr.102, etc., demander un modèle explicite **note→prière** ; l'adjacence éditoriale et `psalm.noteIds` n'en tiennent pas lieu.
5. Préférer une **proposition documentaire d'alias/neutralisation réversible** à une suppression ; ni l'une ni l'autre n'est autorisée ici. Les dossiers historiques 063 restent inchangés.
6. Les essais futurs devront mesurer l'intégrité du texte **avant/après**, les appels et pieds uniques, les pages et marqueurs locaux, l'absence d'ID orphelin et les seuls fichiers autorisés.
7. **Séparer choix éditorial et correction technique** : on peut démontrer une mauvaise page ou une graphie divergente sans pouvoir décider quel ID est à conserver.
8. Faute de preuve ou d'autorisation claire : laisser NON RÉSOLUE, ne pas déclencher de GitHub Actions ni de réparation générale.

## 5. Rectifications documentaires déjà certaines — uniquement dans ce protocole

| Dossier | Fait enregistré dans 064/065 | Différence documentaire ou obstacle | Rectification permise **ici**, sans édition du corpus |
|---|---|---|---|
| `23/129/003` | [064-11](../064/064-11_VERDICTS.md) décrit le composite avec les **v.38–45** ; [065-12](../065/065-12_VERDICTS.md) indique que les **JSON actuels ne contiennent que v.38–40**. Pr.26 autonome est déjà présente, et `23/129/004` a été authentifiée en 064. | **Divergence de portée entre le rapport historique et les données actuelles.** Ni existence ni absence des v.41–45 dans le PDF ne peut être déduite du seul JSON. | Noter « 38–45 selon 064, 38–40 vérifiés dans JSON » ; ne pas réécrire les rapports ni recréer des versets. |
| `35/215/001` vs historique `35/214/002` | [064-19](../064/064-19_VERDICTS.md) : pied p.3485, appel **v.36 du psaume 215** ; [065-13](../065/065-13_VERDICTS.md) : 35/214/002 revendique la même page et le même pied bien que le psaume 214 ne couvre ni la page 3485 ni un v.36. | **Incohérence de rattachement historique établie**, mais provenance de l'ID à conserver non prouvée. | Noter support imprimé 215 et incohérence de 214/002 ; aucun arbitrage 214/002↔215/001. |
| `35/215/001` et statut machine | [065-13](../065/065-13_VERDICTS.md) relève `machine-extracted-source-boundary-audited`. | Une borne d'extraction contrôlée n'est pas une validation humaine ni une preuve d'unicité de l'ID. | Maintenir explicitement « **statut machine ≠ verdict AUTHENTIFIÉE** ». |
| `29/216/003` | [064-14](../064/064-14_VERDICTS.md) : forme extraite « audelà », imprimé « au-delà » ; 002 historique revendique le même pied. | Graphie prouvée, **identité canonique 002/003 non prouvée**. | Consigner la graphie sans corriger un JSON ni authentifier un ID. |
| `29/199/003` | [065-09](../065/065-09_VERDICTS.md) : 003 indique p.2750 ; pied unique imprimé **p.2751 sous Pr.90**. | La page correcte ne permet pas de choisir entre 002 et 003. | Enregistrer l'écart de page, ne pas déplacer le pied. |
| `37/250/003` | [065-12](../065/065-12_VERDICTS.md) : `appliesTo.verse=11`, renvoi imprimé à **la fin du v.36** ; historique 002 composite concurrent. | Correction du champ verse et choix d'ID restent distincts. | Consigner le bon emplacement d'appel sans mutation. |

Les exemples ci-dessus sont des **corrections de formulation documentaire**, pas des corrections de notes, psaumes, prières ou décisions sur l'ID canonique.

## 6. Matrice de traçabilité — chaque anomalie des 44

Chaque fiche ci-dessous reprend le **fait établi** de [066_INVENTAIRE.md](066_INVENTAIRE.md), sa **preuve manquante**, une **option technique possible** et la **décision de Ludo**. Il s'agit d'une reproduction organisée du constat 065, pas d'un nouvel audit.

### Identifiants concurrents — 28 cas

#### `book-06-psalm-040-note-002` — mission pilote 066-03

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Un seul appel et pied imprimés n°1 de 155 mots ; textes JSON 002 et 003 identiques ; identité canonique non départagée.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-02](../065/065-02_VERDICTS.md) ; [verdict 065-02](../065/065-02_VERDICTS.md) ; [064-02_VERDICTS.md](../064/064-02_VERDICTS.md) ; page(s) PDF **325** citées dans le rapport (PDF original non ouvert) ; [Action #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-06-psalm-040-note-003` — mission pilote 066-03

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Même note imprimée n°1 de 155 mots que 002 ; aucune seconde occurrence imprimée ; choix d'identifiant non établi.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-02](../065/065-02_VERDICTS.md) ; [verdict 065-02](../065/065-02_VERDICTS.md) ; [064-02_VERDICTS.md](../064/064-02_VERDICTS.md) ; page(s) PDF **325** citées dans le rapport (PDF original non ouvert) ; [Action #39779161216](https://github.com/ludodulac/Biblaw/actions/runs/39779161216). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-07-psalm-032-note-002` — mission pilote 066-03

- **Fait établi (verdict 065) :** Identifiants en double. — Un seul appel n°1 au verset 27 ; cinq mots concordants dans deux JSON identiques 002 et 003.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-02](../065/065-02_VERDICTS.md) ; [verdict 065-02](../065/065-02_VERDICTS.md) ; [064-03_VERDICTS.md](../064/064-03_VERDICTS.md) ; page(s) PDF **381** citées dans le rapport (PDF original non ouvert) ; [Action #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-07-psalm-032-note-003` — mission pilote 066-03

- **Fait établi (verdict 065) :** Identifiants en double. — Même appel n°1 et même texte de cinq mots que 002 ; autonomie de l'identifiant non démontrée.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-02](../065/065-02_VERDICTS.md) ; [verdict 065-02](../065/065-02_VERDICTS.md) ; [064-03_VERDICTS.md](../064/064-03_VERDICTS.md) ; page(s) PDF **381** citées dans le rapport (PDF original non ouvert) ; [Action #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-07-psalm-047-note-002` — mission pilote 066-04

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Une seule note imprimée n°1 de 35 mots ; fichiers 002 et 003 identiques et marqueur commun.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-03](../065/065-03_VERDICTS.md) ; [verdict 065-03](../065/065-03_VERDICTS.md) ; [064-03_VERDICTS.md](../064/064-03_VERDICTS.md) ; page(s) PDF **416** citées dans le rapport (PDF original non ouvert) ; [Action #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-07-psalm-047-note-003` — mission pilote 066-04

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Même unique pied n°1 de 35 mots que 002 ; second appel inexistant.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-03](../065/065-03_VERDICTS.md) ; [verdict 065-03](../065/065-03_VERDICTS.md) ; [064-03_VERDICTS.md](../064/064-03_VERDICTS.md) ; page(s) PDF **416** citées dans le rapport (PDF original non ouvert) ; [Action #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-08-psalm-025-note-002` — mission pilote 066-04

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Unique note imprimée n°1 de 67 mots, revendiquée aussi par 003 ; ordinal JSON discordant du marqueur.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-03](../065/065-03_VERDICTS.md) ; [verdict 065-03](../065/065-03_VERDICTS.md) ; [064-04_VERDICTS.md](../064/064-04_VERDICTS.md) ; page(s) PDF **432** citées dans le rapport (PDF original non ouvert) ; [Action #39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-08-psalm-025-note-003` — mission pilote 066-04

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Même note imprimée n°1 de 67 mots que 002 ; deux fichiers pour un seul appel.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-03](../065/065-03_VERDICTS.md) ; [verdict 065-03](../065/065-03_VERDICTS.md) ; [064-04_VERDICTS.md](../064/064-04_VERDICTS.md) ; page(s) PDF **432** citées dans le rapport (PDF original non ouvert) ; [Action #39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-30-psalm-215-note-004` — mission pilote 066-05

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Pied imprimé n°1 de 17 tokens au verset 20 ; 005 revendique exactement la même occurrence.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-04](../065/065-04_VERDICTS.md) ; [verdict 065-04](../065/065-04_VERDICTS.md) ; [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; page(s) PDF **2971** citées dans le rapport (PDF original non ouvert) ; [Action #40137448084](https://github.com/ludodulac/Biblaw/actions/runs/40137448084) et [Action #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-30-psalm-215-note-005` — mission pilote 066-05

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Même pied n°1 de 17 tokens que 004 ; ordinal 005 est un numéro d'extraction, pas un appel imprimé.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-04](../065/065-04_VERDICTS.md) ; [verdict 065-04](../065/065-04_VERDICTS.md) ; [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; page(s) PDF **2971** citées dans le rapport (PDF original non ouvert) ; [Action #40137448084](https://github.com/ludodulac/Biblaw/actions/runs/40137448084) et [Action #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-35-psalm-218-note-002` — mission pilote 066-05

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Unique pied n°1 de 45 tokens au verset 20, intégralement présent dans 002 et 003.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-04](../065/065-04_VERDICTS.md) ; [verdict 065-04](../065/065-04_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3495** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-35-psalm-218-note-003` — mission pilote 066-05

- **Fait établi (verdict 065) :** Double revendication d'un pied imprimé. — Même unique pied n°1 de 45 tokens que 002 ; deux identifiants sans deuxième occurrence.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-04](../065/065-04_VERDICTS.md) ; [verdict 065-04](../065/065-04_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3495** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-21-psalm-143-note-003` — mission pilote 066-12

- **Fait établi (verdict 065) :** Prière et identité concurrente. — Note imprimée n°2 de 83 tokens sous Pr.38, hors pages du psaume ; extraction composite 004 concurrente.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-09](../065/065-09_VERDICTS.md) ; [verdict 065-09](../065/065-09_VERDICTS.md) ; [064-10_VERDICTS.md](../064/064-10_VERDICTS.md) ; page(s) PDF **1654** citées dans le rapport (PDF original non ouvert) ; [Action #39965484218](https://github.com/ludodulac/Biblaw/actions/runs/39965484218). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-21-psalm-143-note-004` — mission pilote 066-12

- **Fait établi (verdict 065) :** Extraction composite et attribution à prière. — JSON 169 tokens réunissant les notes n°1 et n°2 de p.1654 sous Pr.38 ; aucune note 004 autonome.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-09](../065/065-09_VERDICTS.md) ; [verdict 065-09](../065/065-09_VERDICTS.md) ; [064-10_VERDICTS.md](../064/064-10_VERDICTS.md) ; page(s) PDF **1653–1654** citées dans le rapport (PDF original non ouvert) ; [Action #39965484218](https://github.com/ludodulac/Biblaw/actions/runs/39965484218). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-29-psalm-199-note-002` — mission pilote 066-12

- **Fait établi (verdict 065) :** Prière et double identité. — Unique note n°1 de 17 tokens sous Pr.90, hors pages du psaume ; 003 revendique le même pied.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-09](../065/065-09_VERDICTS.md) ; [verdict 065-09](../065/065-09_VERDICTS.md) ; [064-14_VERDICTS.md](../064/064-14_VERDICTS.md) ; page(s) PDF **2751** citées dans le rapport (PDF original non ouvert) ; [Action #40135038621](https://github.com/ludodulac/Biblaw/actions/runs/40135038621) et [Action #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-29-psalm-199-note-003` — mission pilote 066-12

- **Fait établi (verdict 065) :** Prière, page décalée et double identité. — Même texte que 002 ; pas de pied en p.2750 ; note unique en p.2751 sous Pr.90.
- **Preuve manquante :** Pied imprimé p.2751 sous Pr.90, tandis que 003 déclare p.2750 : corriger la page ne désigne pas l'ID canonique.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-09](../065/065-09_VERDICTS.md) ; [verdict 065-09](../065/065-09_VERDICTS.md) ; [064-14_VERDICTS.md](../064/064-14_VERDICTS.md) ; page(s) PDF **2750–2751** citées dans le rapport (PDF original non ouvert) ; [Action #40135038621](https://github.com/ludodulac/Biblaw/actions/runs/40135038621) et [Action #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-33-psalm-230-note-002` — mission pilote 066-06

- **Fait établi (verdict 065) :** Extraction composite et double identité. — JSON de 106 tokens : pied n°1 de six tokens puis 100 tokens de versets ; 003 revendique le même pied.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-10](../065/065-10_VERDICTS.md) ; [verdict 065-10](../065/065-10_VERDICTS.md) ; [064-18_VERDICTS.md](../064/064-18_VERDICTS.md) ; page(s) PDF **3268–3269** citées dans le rapport (PDF original non ouvert) ; [Action #40199370107](https://github.com/ludodulac/Biblaw/actions/runs/40199370107) et [Action #40199469318](https://github.com/ludodulac/Biblaw/actions/runs/40199469318). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-33-psalm-230-note-003` — mission pilote 066-06

- **Fait établi (verdict 065) :** Double identité sur pied composite. — Six tokens conformes au pied unique n°1 ; 002 revendique ce pied avec des versets supplémentaires.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-10](../065/065-10_VERDICTS.md) ; [verdict 065-10](../065/065-10_VERDICTS.md) ; [064-18_VERDICTS.md](../064/064-18_VERDICTS.md) ; page(s) PDF **3268** citées dans le rapport (PDF original non ouvert) ; [Action #40199370107](https://github.com/ludodulac/Biblaw/actions/runs/40199370107) et [Action #40199469318](https://github.com/ludodulac/Biblaw/actions/runs/40199469318). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-35-psalm-213-note-002` — mission pilote 066-17

- **Fait établi (verdict 065) :** Extraction composite et double identité. — Pied n°1 de 55 tokens au verset 19, JSON de 455 tokens prolongeant Pr.102 ; 003 revendique même pied et texte.
- **Preuve manquante :** Deux composites 002 et 003 identiques, contenant une suite de Pr.102 livre 35 absente de son autonome.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-10](../065/065-10_VERDICTS.md) ; [verdict 065-10](../065/065-10_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3479** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-35-psalm-213-note-003` — mission pilote 066-17

- **Fait établi (verdict 065) :** Extraction composite et double identité. — Même pied unique de 55 tokens et même JSON composite de 455 tokens que 002 ; aucune seconde note.
- **Preuve manquante :** Deux composites 002 et 003 identiques, contenant une suite de Pr.102 livre 35 absente de son autonome.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-10](../065/065-10_VERDICTS.md) ; [verdict 065-10](../065/065-10_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3479** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-27-psalm-169-note-003` — mission pilote 066-13

- **Fait établi (verdict 065) :** Prière et double identité. — Unique pied de 48 tokens sous Pr.63 également revendiqué par 005.
- **Preuve manquante :** Le renvoi « Amin Salama¹ » est sous Pr.63, pas v.42 ; même pied que 005, statut de l'ID indécidable.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-11](../065/065-11_VERDICTS.md) ; [verdict 065-11](../065/065-11_VERDICTS.md) ; [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; page(s) PDF **2536** citées dans le rapport (PDF original non ouvert) ; [Action #40130627832](https://github.com/ludodulac/Biblaw/actions/runs/40130627832) et [Action #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-27-psalm-169-note-005` — mission pilote 066-13

- **Fait établi (verdict 065) :** Prière et double identité. — Même appel sous Pr.63 et même pied de 48 tokens que 003 ; aucune seconde occurrence.
- **Preuve manquante :** Le renvoi « Amin Salama¹ » est sous Pr.63, pas v.42 ; même pied que 003, statut de l'ID indécidable.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-11](../065/065-11_VERDICTS.md) ; [verdict 065-11](../065/065-11_VERDICTS.md) ; [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; page(s) PDF **2536** citées dans le rapport (PDF original non ouvert) ; [Action #40130627832](https://github.com/ludodulac/Biblaw/actions/runs/40130627832) et [Action #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-27-psalm-169-note-004` — mission pilote 066-07

- **Fait établi (verdict 065) :** Conflit d'identité avec dossier 063. — Pied n°1 de 48 tokens au verset 30 ; dossier 002 NON RÉSOLU de 063 revendique même pied et appel.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-11](../065/065-11_VERDICTS.md) ; [verdict 065-11](../065/065-11_VERDICTS.md) ; [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; page(s) PDF **2534** citées dans le rapport (PDF original non ouvert) ; [Action #40130627832](https://github.com/ludodulac/Biblaw/actions/runs/40130627832) et [Action #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-37-psalm-250-note-003` — mission pilote 066-07

- **Fait établi (verdict 065) :** Conflit historique et incohérence de verset. — Unique pied n°1 de 80 tokens aussi revendiqué par 002 NON RÉSOLU ; verse=11 discordant de l'appel près du verset 37.
- **Preuve manquante :** Le renvoi imprimé est à la fin du v.36 ; verse=11 dans la note 003, et l'ancien composite 002 revendique le même pied.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-12](../065/065-12_VERDICTS.md) ; [verdict 065-12](../065/065-12_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3690** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-23-psalm-133-note-004` — mission pilote 066-08

- **Fait établi (verdict 065) :** Conflit d'identité avec dossier 063. — Unique pied n°1 de huit tokens ; le dossier 003 NON RÉSOLU de 063A revendique le même appel.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-13](../065/065-13_VERDICTS.md) ; [verdict 065-13](../065/065-13_VERDICTS.md) ; [064-11_VERDICTS.md](../064/064-11_VERDICTS.md) ; page(s) PDF **1960** citées dans le rapport (PDF original non ouvert) ; [Action #39968386949](https://github.com/ludodulac/Biblaw/actions/runs/39968386949). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-26-psalm-189-note-003` — mission pilote 066-08

- **Fait établi (verdict 065) :** Conflit d'identité avec dossier 063. — Unique note imprimée n°1 de 29 tokens ; dossier 002 NON RÉSOLU de 063 revendique le même pied.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-13](../065/065-13_VERDICTS.md) ; [verdict 065-13](../065/065-13_VERDICTS.md) ; [064-12_VERDICTS.md](../064/064-12_VERDICTS.md) ; page(s) PDF **2453** citées dans le rapport (PDF original non ouvert) ; [Action #40104571746](https://github.com/ludodulac/Biblaw/actions/runs/40104571746) et [Action #40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-30-psalm-200-note-003` — mission pilote 066-09

- **Fait établi (verdict 065) :** Conflit avec dossier 063. — Unique pied n°1 de 111 tokens ; dossier 002 NON RÉSOLU de 063 contient le même pied suivi de versets et Pr.83.
- **Preuve manquante :** Provenance indépendante de l'ordinal et du champ verse pour attribuer l'unique pied ; règle de traitement des IDs concurrents et de noteIds.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-13](../065/065-13_VERDICTS.md) ; [verdict 065-13](../065/065-13_VERDICTS.md) ; [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; page(s) PDF **2900–2901** citées dans le rapport (PDF original non ouvert) ; [Action #40137448084](https://github.com/ludodulac/Biblaw/actions/runs/40137448084) et [Action #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

#### `book-35-psalm-215-note-001` — mission pilote 066-09

- **Fait établi (verdict 065) :** Conflit avec dossier historique. — Pied n°1 de 24 tokens au verset 36 ; dossier historique 35/214/002 revendique la même note imprimée.
- **Preuve manquante :** La page 3485 et le verset 36 ne sont pas dans le psaume 214, mais cette incohérence ne suffit pas à choisir l'ID canonique ; réconcilier 214/002 et 215/001.
- **Possibilité technique non exécutée :** Tracer le pied unique et ses candidats ; ne proposer un ID canonique que sur une preuve de provenance ou décision explicite, puis planifier noteIds.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-13](../065/065-13_VERDICTS.md) ; [verdict 065-13](../065/065-13_VERDICTS.md) ; [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; page(s) PDF **3485** citées dans le rapport (PDF original non ouvert) ; [Action #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) et [Action #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034). ; risque : Perte de provenance, double note, suppression d'un suffixe ou lien noteIds orphelin.

### Notes imprimées sous des prières — 5 cas

#### `book-17-psalm-115-note-001` — mission pilote 066-10

- **Fait établi (verdict 065) :** Rattachement à une prière. — Pied imprimé n°1 de cinq tokens sous la prière Pr.11, hors pages canoniques du psaume 115.
- **Preuve manquante :** Relation canonique explicite note→prière, support d'appel, pages et éventuelle modification cohérente de noteIds.
- **Possibilité technique non exécutée :** Modéliser note→prière avec appel et page ; ne pas rebaptiser en note de verset du psaume.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-07](../065/065-07_VERDICTS.md) ; [verdict 065-07](../065/065-07_VERDICTS.md) ; [064-08_VERDICTS.md](../064/064-08_VERDICTS.md) ; page(s) PDF **1122** citées dans le rapport (PDF original non ouvert) ; [Action #39916095956](https://github.com/ludodulac/Biblaw/actions/runs/39916095956). ; risque : Faux renvoi au psaume, mauvais numéro de page ou note invisible.

#### `book-27-psalm-158-note-001` — mission pilote 066-10

- **Fait établi (verdict 065) :** Rattachement à une prière. — Pied n°1 de 22 tokens dont l'appel appartient à Pr.53 ; page 2485 hors psaume 158.
- **Preuve manquante :** Relation canonique explicite note→prière, support d'appel, pages et éventuelle modification cohérente de noteIds.
- **Possibilité technique non exécutée :** Modéliser note→prière avec appel et page ; ne pas rebaptiser en note de verset du psaume.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-07](../065/065-07_VERDICTS.md) ; [verdict 065-07](../065/065-07_VERDICTS.md) ; [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; page(s) PDF **2484–2485** citées dans le rapport (PDF original non ouvert) ; [Action #40130627832](https://github.com/ludodulac/Biblaw/actions/runs/40130627832) et [Action #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623). ; risque : Faux renvoi au psaume, mauvais numéro de page ou note invisible.

#### `book-27-psalm-177-note-001` — mission pilote 066-10

- **Fait établi (verdict 065) :** Rattachement à une prière. — Pied de 103 tokens sous Pr.71 ; page 2570 hors pages canoniques du psaume 177.
- **Preuve manquante :** Relation canonique explicite note→prière, support d'appel, pages et éventuelle modification cohérente de noteIds.
- **Possibilité technique non exécutée :** Modéliser note→prière avec appel et page ; ne pas rebaptiser en note de verset du psaume.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-07](../065/065-07_VERDICTS.md) ; [verdict 065-07](../065/065-07_VERDICTS.md) ; [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; page(s) PDF **2569–2570** citées dans le rapport (PDF original non ouvert) ; [Action #40130627832](https://github.com/ludodulac/Biblaw/actions/runs/40130627832) et [Action #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623). ; risque : Faux renvoi au psaume, mauvais numéro de page ou note invisible.

#### `book-30-psalm-211-note-001` — mission pilote 066-11

- **Fait établi (verdict 065) :** Rattachement à une prière. — Pied de 28 tokens dont l'appel « Amin » appartient à la prière suivant le psaume 211 ; p.2953 hors psaume.
- **Preuve manquante :** Relation canonique explicite note→prière, support d'appel, pages et éventuelle modification cohérente de noteIds.
- **Possibilité technique non exécutée :** Modéliser note→prière avec appel et page ; ne pas rebaptiser en note de verset du psaume.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-08](../065/065-08_VERDICTS.md) ; [verdict 065-08](../065/065-08_VERDICTS.md) ; [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; page(s) PDF **2952–2953** citées dans le rapport (PDF original non ouvert) ; [Action #40137448084](https://github.com/ludodulac/Biblaw/actions/runs/40137448084) et [Action #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177). ; risque : Faux renvoi au psaume, mauvais numéro de page ou note invisible.

#### `book-31-psalm-184-note-001` — mission pilote 066-11

- **Fait établi (verdict 065) :** Rattachement à une prière. — Pied de 71 tokens sous Pr.76 après le psaume 184 ; p.3005 hors pages canoniques du psaume.
- **Preuve manquante :** Relation canonique explicite note→prière, support d'appel, pages et éventuelle modification cohérente de noteIds.
- **Possibilité technique non exécutée :** Modéliser note→prière avec appel et page ; ne pas rebaptiser en note de verset du psaume.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-08](../065/065-08_VERDICTS.md) ; [verdict 065-08](../065/065-08_VERDICTS.md) ; [064-16_VERDICTS.md](../064/064-16_VERDICTS.md) ; page(s) PDF **3005** citées dans le rapport (PDF original non ouvert) ; [Action #40187890100](https://github.com/ludodulac/Biblaw/actions/runs/40187890100) et [Action #40187890311](https://github.com/ludodulac/Biblaw/actions/runs/40187890311). ; risque : Faux renvoi au psaume, mauvais numéro de page ou note invisible.

### Prières absentes ou incomplètes — 6 cas

#### `book-21-psalm-137-note-001` — mission pilote 066-14

- **Fait établi (verdict 065) :** Mélange note et prière. — Pied imprimé de huit tokens ; JSON de 82 tokens absorbant la continuation de la prière Pr.32.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-06](../065/065-06_VERDICTS.md) ; [verdict 065-06](../065/065-06_VERDICTS.md) ; [064-09_VERDICTS.md](../064/064-09_VERDICTS.md) ; page(s) PDF **1619–1620** citées dans le rapport (PDF original non ouvert) ; [Action #39958415133](https://github.com/ludodulac/Biblaw/actions/runs/39958415133). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

#### `book-21-psalm-160-note-001` — mission pilote 066-14

- **Fait établi (verdict 065) :** Mélange note et prière. — Pied imprimé n°1 de 19 tokens ; JSON de 384 tokens avec la prière autonome Pr.54.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-06](../065/065-06_VERDICTS.md) ; [verdict 065-06](../065/065-06_VERDICTS.md) ; [064-10_VERDICTS.md](../064/064-10_VERDICTS.md) ; page(s) PDF **1747–1748** citées dans le rapport (PDF original non ouvert) ; [Action #39965484218](https://github.com/ludodulac/Biblaw/actions/runs/39965484218). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

#### `book-23-psalm-145-note-001` — mission pilote 066-15

- **Fait établi (verdict 065) :** Mélange note et prière. — Pied de 30 tokens, JSON de 263 tokens contenant 233 tokens de continuation de Pr.41.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-06](../065/065-06_VERDICTS.md) ; [verdict 065-06](../065/065-06_VERDICTS.md) ; [064-12_VERDICTS.md](../064/064-12_VERDICTS.md) ; page(s) PDF **2020–2021** citées dans le rapport (PDF original non ouvert) ; [Action #40104571746](https://github.com/ludodulac/Biblaw/actions/runs/40104571746) et [Action #40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

#### `book-24-psalm-141-note-001` — mission pilote 066-15

- **Fait établi (verdict 065) :** Mélange note et prière. — Pied de 50 tokens, JSON de 440 tokens comprenant 390 tokens de Pr.36.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-06](../065/065-06_VERDICTS.md) ; [verdict 065-06](../065/065-06_VERDICTS.md) ; [064-12_VERDICTS.md](../064/064-12_VERDICTS.md) ; page(s) PDF **2134–2135** citées dans le rapport (PDF original non ouvert) ; [Action #40104571746](https://github.com/ludodulac/Biblaw/actions/runs/40104571746) et [Action #40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

#### `book-26-psalm-169-note-001` — mission pilote 066-16

- **Fait établi (verdict 065) :** Mélange note et prière. — Pied de 24 tokens, JSON de 386 tokens comprenant 362 tokens de Pr.54.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-07](../065/065-07_VERDICTS.md) ; [verdict 065-07](../065/065-07_VERDICTS.md) ; [064-12_VERDICTS.md](../064/064-12_VERDICTS.md) ; page(s) PDF **2361–2362** citées dans le rapport (PDF original non ouvert) ; [Action #40104571746](https://github.com/ludodulac/Biblaw/actions/runs/40104571746) et [Action #40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

#### `book-29-psalm-212-note-001` — mission pilote 066-16

- **Fait établi (verdict 065) :** Note de prière composite hors psaume. — Pied n°1 de quatre tokens sous Pr.102 ; JSON de 193 tokens dont 189 tokens de prière ; page hors psaume.
- **Preuve manquante :** Prière autonome complète et continuation textuelle vérifiée avant toute troncature de note.
- **Possibilité technique non exécutée :** Reconstituer la prière avant de réduire le composite ; comparer chaque continuation à la source.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-12](../065/065-12_VERDICTS.md) ; [verdict 065-12](../065/065-12_VERDICTS.md) ; [064-14_VERDICTS.md](../064/064-14_VERDICTS.md) ; page(s) PDF **2814** citées dans le rapport (PDF original non ouvert) ; [Action #40135038621](https://github.com/ludodulac/Biblaw/actions/runs/40135038621) et [Action #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792). ; risque : Effacement d'une continuation qui n'existe nulle part ailleurs.

### Extractions composites — 3 cas

#### `book-07-psalm-035-note-005` — mission pilote 066-18

- **Fait établi (verdict 065) :** Extraction fusionnant deux notes. — Le JSON de 57 mots juxtapose les pieds imprimés distincts n°1 (25 mots) et n°2 (31 mots) ; aucune troisième note imprimée.
- **Preuve manquante :** Limites des pieds individuels, conservation canonique de chaque partie et traitement non destructif des références.
- **Possibilité technique non exécutée :** Séparer pied, corps et prière sans omission de partie ; vérifier les données canoniques déjà conservées.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-05](../065/065-05_VERDICTS.md) ; [verdict 065-05](../065/065-05_VERDICTS.md) ; [064-03_VERDICTS.md](../064/064-03_VERDICTS.md) ; page(s) PDF **387** citées dans le rapport (PDF original non ouvert) ; [Action #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188). ; risque : Perte d'un pied numéroté, de verset ou création de doublon.

#### `book-12-psalm-077-note-001` — mission pilote 066-18

- **Fait établi (verdict 065) :** Extraction de trois notes concaténées. — JSON 89 mots : pied n°1 de 23 mots puis notes imprimées 2 et 3 ; fichiers réciproques séparés absents.
- **Preuve manquante :** Limites des pieds individuels, conservation canonique de chaque partie et traitement non destructif des références.
- **Possibilité technique non exécutée :** Séparer pied, corps et prière sans omission de partie ; vérifier les données canoniques déjà conservées.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-05](../065/065-05_VERDICTS.md) ; [verdict 065-05](../065/065-05_VERDICTS.md) ; [064-05_VERDICTS.md](../064/064-05_VERDICTS.md) ; page(s) PDF **764** citées dans le rapport (PDF original non ouvert) ; [Action #39793260093](https://github.com/ludodulac/Biblaw/actions/runs/39793260093). ; risque : Perte d'un pied numéroté, de verset ou création de doublon.

#### `book-23-psalm-129-note-003` — mission pilote 066-19

- **Fait établi (verdict 065) :** Mélange note, versets et prière. — Pied n°1 de 20 tokens ; JSON de 510 tokens mêlant versets 38–45 et prière Pr.26.
- **Preuve manquante :** Le rapport historique parle de v.38–45 ; les JSON actuels contiennent seulement 38–40, et Pr.26 est déjà conservée dans la prière autonome. L'ID 004 est authentifié en 064.
- **Possibilité technique non exécutée :** Séparer pied, corps et prière sans omission de partie ; vérifier les données canoniques déjà conservées.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-12](../065/065-12_VERDICTS.md) ; [verdict 065-12](../065/065-12_VERDICTS.md) ; [064-11_VERDICTS.md](../064/064-11_VERDICTS.md) ; page(s) PDF **1936–1937** citées dans le rapport (PDF original non ouvert) ; [Action #39968386949](https://github.com/ludodulac/Biblaw/actions/runs/39968386949). ; risque : Perte d'un pied numéroté, de verset ou création de doublon.

### Divergences textuelles — 1 cas

#### `book-29-psalm-216-note-003` — mission pilote 066-20

- **Fait établi (verdict 065) :** Conflit historique et graphie divergente. — Pied de 78 tokens contre 77 extraits (« au-delà »/« audelà ») ; 002 NON RÉSOLU de 063 revendique le même appel.
- **Preuve manquante :** Graphie « audelà » extraite contre « au-delà » imprimé et conflit d'ID avec 002 composite.
- **Possibilité technique non exécutée :** Comparer la forme imprimée et l'extraction, différer la correction isolée tant que l'identité concurrente est ouverte.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-11](../065/065-11_VERDICTS.md) ; [verdict 065-11](../065/065-11_VERDICTS.md) ; [064-14_VERDICTS.md](../064/064-14_VERDICTS.md) ; page(s) PDF **2831** citées dans le rapport (PDF original non ouvert) ; [Action #40135038621](https://github.com/ludodulac/Biblaw/actions/runs/40135038621) et [Action #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792). ; risque : Correction lexicale sans résolution de l'identité.

### Autres anomalies : verset tronqué — 1 cas

#### `book-22-psalm-155-note-001` — mission pilote 066-19

- **Fait établi (verdict 065) :** Note composite et verset tronqué. — Pied de 231 tokens, JSON de 253 ajoutant 22 tokens du verset 21 ; verset du psaume tronqué en amont.
- **Preuve manquante :** Les 22 tokens après « après la » sont dans le composite de note mais absents du verset 21 canonique.
- **Possibilité technique non exécutée :** Restituer le verset 21 intégralement avant de supprimer la copie conservée dans la note.
- **Décision réservée à Ludo :** **Ludo** doit autoriser toute décision d'ID, neutralisation, création de fichier canonique, correction de note/psaume/prière et migration de lien ; la rédaction d'un protocole est purement documentaire.
- **Sources et risque :** [verdict 065-12](../065/065-12_VERDICTS.md) ; [verdict 065-12](../065/065-12_VERDICTS.md) ; [064-11_VERDICTS.md](../064/064-11_VERDICTS.md) ; page(s) PDF **1876–1877** citées dans le rapport (PDF original non ouvert) ; [Action #39968386949](https://github.com/ludodulac/Biblaw/actions/runs/39968386949). ; risque : Disparition des 22 tokens qui complètent le verset 21.

## 7. Contrôles et décision de clôture

- Le document nomme **44/44 IDs distincts** et ne réintroduit pas les deux corrigées de 065-05.
- Chaque fiche comporte **fait, preuve manquante, possibilité technique, décision éditoriale et source**.
- Le protocole distingue certitude de l'imprimé et arbitrage d'ID, préserve chaque pied/verset/prière et proscrit la mutation sans autorisation.
- Les divergences 23/129, 35/214↔215 et statut machine sont conservées comme **rectifications documentaires** ; les rapports historiques restent intacts.
- **Aucun examen PDF, audit général du corpus, modification de note/psaume/prière, publication, déploiement ou fusion.**

**STOP APRÈS 066-02. Missions 066-03 à 066-20 NON COMMENCÉES ; attendre instructions de Grand-père BIBLAW et accord de Ludo pour toute décision éditoriale.**
