# 🌸 BIBLAW — MISSION 065-11 — VERDICTS DU TROISIÈME LOT C

**Statut : TERMINÉE — 4/4 notes examinées ; 0 AUTHENTIFIÉE ; 0 CORRIGÉE ET AUTHENTIFIÉE ; 4 NON RÉSOLUES.**

## Reprise, périmètre et preuves

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT au contrôle initial ; HEAD de départ `0f6022b3a70d09f2bc67d7ba432636148ce2f519`, conforme au dernier HEAD communiqué. `065-11_VERDICTS.md` absent à l'entrée ; suivi 065-11 = NON COMMENCÉE.
- Le périmètre **exclusif** 065-11, classe C, regroupe les quatre identifiants ci-dessous ; aucun dossier du lot précédent n'a été relu.
- **Preuves archivées réutilisées** : [064-13](../064/064-13_VERDICTS.md), captures p.2534 et p.2536 en A **12574772504** et B **12574719450** ; [064-14](../064/064-14_VERDICTS.md), p.2831 en B **12576942014**. Les trois artefacts originaux ont été confirmés non expirés. Les numéros, frontières et supports des notes sont établis par leurs contrôles visuels historiques : pas de nouvelle ouverture du PDF original.
- Comparaisons ciblées du HEAD : quatre JSON de la mission, deux JSON historiques 063 concurrents **en lecture seule et uniquement pour constater les collisions**, deux psaumes et la prière autonome Pr.63. Résultats : 003/005 strictement égales en 27/169 ; 004 préfixe exact de l'ancien 002 composite en 27/169 ; 003 préfixe exact de l'ancien 002 composite en 29/216. Aucune ambiguïté de *texte* ne lève l'ambiguïté d'*identifiant*.
- Interdictions respectées : pas de sélection arbitraire, pas de suppression de texte canonique, pas de changement de note, psaume, prière, interface, catalogue ou validation ; aucune GitHub Action nouvelle, aucune réparation générale, aucune publication, aucun déploiement ni fusion.

## Décisions par note

### 1. `book-27-psalm-169-note-003`

- **Ancien verdict :** NON RÉSOLUE (mission source 064).
- **Nouveau verdict :** **NON RÉSOLUE**.
- **Texte, identité, support et doublon :** Un seul pied imprimé n°1 de **48 tokens** en p.2536, sous la prière **Pr.63**, appelé après « Amin Salama¹ ». Le JSON 003 transcrit exactement le texte de ce pied, mais le JSON 005 en reproduit **strictement le même texte, sur la même page et avec le même appel**. Le psaume 169 référence les deux IDs dans `noteIds`, alors que le pied relève de la prière après le psaume, et non des versets 41–42. La prière canonique `raphael-book-27-prayer-063.json` existe, commence « Amin Salama » et est rattachée éditorialement au psaume 169, mais aucun lien explicite note→prière ne départage les IDs. `appliesTo.verse` de 003 est null.
- **Preuves documentaires :** [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; [Actions #40130414394](https://github.com/ludodulac/Biblaw/actions/runs/40130414394) ; artefact(s) `12574772504 (A), 12574719450 (B)` p.2536, preuves visuelles archivées ; `data/notes/books/book-27/book-27-psalm-169-note-003.json` (blob `708b835078de82c80e90ff28777a5e15dd64b7a3`) ; `data/corpus/books/book-27/psalm-169.json` (blob `5edf3f37cc4ab832991b0f335d7efe8c6130f43c`) ; `data/prayers/raphael-book-27-prayer-063.json` (blob `48a96cd82a7c539d4bd2a5c7bef51c2c7c8e2065`) ; autre candidat `book-27-psalm-169-note-005`.
- **Preuve bloquante à obtenir :** Preuve documentaire attribuant sans ambiguïté le pied sous Pr.63 à un ID unique parmi 003 et 005, puis règle de rattachement de notes aux prières et réconciliation de `noteIds` sans modification interdite de psaume ou prière.
- **Correction :** Aucune, ni fusion ni promotion. Aucun texte ni référence canonique modifié.

### 2. `book-27-psalm-169-note-005`

- **Ancien verdict :** NON RÉSOLUE (mission source 064).
- **Nouveau verdict :** **NON RÉSOLUE**.
- **Texte, identité, support et doublon :** Le JSON 005 porte **48/48 tokens**, le même pied n°1 p.2536 sous **Pr.63** (appel après « Amin Salama¹ ») que le candidat 003 ; la comparaison des deux champs `text` confirme leur **égalité exacte**. L'annotation `appliesTo.verse=42` de 005 ne prouve pas que l'appel soit au verset 42 : la preuve imprimée le situe dans la prière autonome, non dans le corps du psaume. Une seule note imprimée et deux IDs concurrents, malgré leur présence dans `psalm-169.noteIds`.
- **Preuves documentaires :** [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; [Actions #40130702623](https://github.com/ludodulac/Biblaw/actions/runs/40130702623) ; artefact(s) `12574719450 (B), 12574772504 (A)` p.2536, preuves visuelles archivées ; `data/notes/books/book-27/book-27-psalm-169-note-005.json` (blob `74b04d555210f61464a8d0c194210edaab2889e2`) ; `data/corpus/books/book-27/psalm-169.json` (blob `5edf3f37cc4ab832991b0f335d7efe8c6130f43c`) ; `data/prayers/raphael-book-27-prayer-063.json` (blob `48a96cd82a7c539d4bd2a5c7bef51c2c7c8e2065`) ; autre candidat `book-27-psalm-169-note-003`.
- **Preuve bloquante à obtenir :** Départager les IDs 003/005 par une preuve d'identité archivistique et autoriser la modélisation note→Pr.63 avec références cohérentes ; aucune preuve d'un deuxième pied.
- **Correction :** Aucune, ni suppression ni choix d'ID. Aucun texte ni référence canonique modifié.

### 3. `book-27-psalm-169-note-004`

- **Ancien verdict :** NON RÉSOLUE (mission source 064).
- **Nouveau verdict :** **NON RÉSOLUE**.
- **Texte, identité, support et doublon :** Le pied n°1 de **48/48 tokens** est imprimé p.2534 et son appel est au **verset 30** du psaume 169 ; le texte de 004 est bien ce pied (« Symbole alchimique et magique du caducée… soleil ailé. »). Toutefois le fichier historique 002 (ancien dossier 063 NON RÉSOLU) revendique **la même page, le même appel et le préfixe textuel exact de 004**, puis ajoute dans son extraction composite des versets du psaume et une prière. `noteIds` du psaume répertorie les deux IDs. L'unicité de l'impression ne permet pas d'authentifier deux fichiers autonomes concurrents ; le dossier 063 est seulement consulté comme pièce de conflit, sans retraitement.
- **Preuves documentaires :** [064-13_VERDICTS.md](../064/064-13_VERDICTS.md) ; [Actions #40130414394](https://github.com/ludodulac/Biblaw/actions/runs/40130414394) ; artefact(s) `12574772504 (A)` p.2534, preuves visuelles archivées ; `data/notes/books/book-27/book-27-psalm-169-note-004.json` (blob `4b033ca7d43888761ee1a478af4d6a8b07769a31`) ; `data/corpus/books/book-27/psalm-169.json` (blob `5edf3f37cc4ab832991b0f335d7efe8c6130f43c`) ; `data/prayers/raphael-book-27-prayer-063.json` (blob `48a96cd82a7c539d4bd2a5c7bef51c2c7c8e2065`) ; autre candidat `book-27-psalm-169-note-002 (dossier historique 063)`.
- **Preuve bloquante à obtenir :** Preuve attribuant le pied unique à l'identifiant canonique 002 ou 004, traitement documenté de l'extraction composite historique et réconciliation des renvois ; ne pas choisir sur la seule exactitude des 48 tokens.
- **Correction :** Aucune : aucune troncature du composite, ni édition de psaume ou prière. Aucun texte ni référence canonique modifié.

### 4. `book-29-psalm-216-note-003`

- **Ancien verdict :** NON RÉSOLUE (mission source 064).
- **Nouveau verdict :** **NON RÉSOLUE**.
- **Texte, identité, support et doublon :** L'appel imprimé n°1 est au **verset 11** du psaume 216 (p.2831), et le pied imprimé contient **78 tokens** sur la portée symbolique de l'épée. Le JSON 003 comporte **77 tokens**, notamment « audelà » là où le PDF imprime « au-delà » : écart lexical documenté en 064-14 après 66 tokens. Le fichier historique 002 (dossier 063 NON RÉSOLU) reproduit comme préfixe **exactement le texte actuel de 003**, suivi d'une extraction composite du corps du psaume. Les deux IDs et le même appel figurent sur une unique page et sont tous deux enregistrés dans `psalm-216.noteIds`. La graphie peut être rectifiée en principe, mais elle ne résout pas le conflit d'identité 002/003 ; pas de correction partielle présentée comme authentification.
- **Preuves documentaires :** [064-14_VERDICTS.md](../064/064-14_VERDICTS.md) ; [Actions #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792) ; artefact(s) `12576942014 (B)` p.2831, preuves visuelles archivées ; `data/notes/books/book-29/book-29-psalm-216-note-003.json` (blob `f1a27327ef8774c3040b83b4abcf6236207097a8`) ; `data/corpus/books/book-29/psalm-216.json` (blob `c33f8594af886b2f4c461b7eb4e51360c41e7e8f`) ; autre candidat `book-29-psalm-216-note-002 (dossier historique 063)`.
- **Preuve bloquante à obtenir :** Désignation documentaire unique de l'ID canonique et résolution traçable du composite 002, puis correction graphique exacte « audelà » → « au-delà » selon le pied imprimé avec références cohérentes.
- **Correction :** Aucune : graphie et données conservées dans l'attente de l'arbitrage. Aucun texte ni référence canonique modifié.

## Contrôles spécialisés ciblés (sans nouvelle CI)

- **PASS** — Périmètre exact de quatre IDs distincts 065-11.
- **PASS** — Quatre sources JSON en attente de révision.
- **PASS** — 27/169/003 et 005 : texte identique, même page et même marqueur.
- **PASS** — 27/169/003, 005 : métadonnées verse distinctes, ne prouvent pas l'appel sous Pr.63.
- **PASS** — 27/169/003, 005 : deux IDs listés dans psaume 169, p.2536 présente au corpus.
- **PASS** — Pr.63 existe, est rattachée au psaume 169 et commence par Amin Salama.
- **PASS** — 27/169/004 : appel v.30 p.2534 et référencement dans psaume.
- **PASS** — 27/169/002 historique contient 004 comme préfixe exact.
- **PASS** — 29/216/003 : appel v.11 p.2831 et référencement dans psaume.
- **PASS** — 29/216/002 historique contient 003 comme préfixe exact.
- **PASS** — 29/216/003 : graphie audelà observée dans JSON, source 064 documente au-delà.
- **PASS** — Les deux psaumes conservent les ID historiques concurrents.
- **PASS** — Aucune permission d'édition des psaumes ou prières, seules écritures de rapports prévues.
- **PASS** — Suivi initial : 065-11 non commencée, aucune clôture antérieure.
- **PASS** — Arbre du commit de base disponible pour commit sans écrasement.

**15/15 contrôles de cohérence documentaire et structurale PASS**. Les comparaisons textuelles et les métadonnées ont été lues au HEAD de départ ; les faits sur l'imprimé sont ceux déjà prouvés en 064. Ces contrôles ne constituent ni une réinspection PDF, ni une authentification automatique des IDs en collision.

## Bilan et arrêt

- **065-11 : 4/4 réexaminées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.** Deux collisions sous 27/169 (003↔005 pour Pr.63 ; 004↔002 historique 063 pour la note du v.30) et une collision 29/216/003↔002 historique 063, assortie de l'écart graphique « audelà »/« au-delà ».
- **Cumul 065 : 38/46 anomalies réexaminées, 2 résolues, 44 NON RÉSOLUES, 8 restant à réexaminer.** Les 146 notes authentifiées en 064 et les verdicts antérieurs restent inchangés.
- Aucun PDF rouvert, aucun psaume/prière modifié, aucun déploiement ni fusion. **STOP après 065-11 ; 065-12 NON COMMENCÉE.**
