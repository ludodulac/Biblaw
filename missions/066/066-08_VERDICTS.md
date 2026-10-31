# 🌸 BIBLAW — MISSION 066-08 — CONCURRENTS HISTORIQUES 23/133 ET 26/189

**Statut : TERMINÉE — 2/2 notes pilotes traitées ; 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 2 NON RÉSOLUES ; aucune écriture canonique.**

## 1. Périmètre et sources de preuve

- [066_PLAN.md](066_PLAN.md) affecte exclusivement **`book-23-psalm-133-note-004`** et **`book-26-psalm-189-note-003`** au lot 066-08. Les anciens `book-23-psalm-133-note-003` et `book-26-psalm-189-note-002` (dossiers **063 non résolus**) sont **comparés en lecture seule**, sans réexaminer leurs anciens verdicts ni les compter parmi les 44 pilotes.
- Reprise GitHub : `ludodulac/Biblaw`, branche `feat/052-search-ui`, base `743ef00501e1c5007a12758a800b04f609016b88` ; PR #72 **OPEN, DRAFT, non fusionnée** au contrôle initial unique.
- Application du [protocole 066-02](066-02_PROTOCOL.md) : **document source → appel local → pied physique → candidats**, puis classification en FAIT ÉTABLI / HYPOTHÈSE / CORRECTION TECHNIQUE CERTAINE / DÉCISION NÉCESSITANT LUDO. Concordance exacte du texte **≠** identification certaine d'un ID canonique.
- Preuves déjà archivées : [064-11/B](../064/064-11_VERDICTS.md) p.1960, [Action 39967539345](https://github.com/ludodulac/Biblaw/actions/runs/39967539345), artefact `12507282337` **non expiré** ; [064-12/B](../064/064-12_VERDICTS.md) p.2453, [Action 40104623724](https://github.com/ludodulac/Biblaw/actions/runs/40104623724), artefact `12564281933` **non expiré**. [065-13](../065/065-13_VERDICTS.md) réutilisé. Aucun PDF rouvert, aucun nouveau workflow.
- Lectures ciblées : notes pilotes et concurrents historiques (quatre JSON), deux psaumes, prière autonome Pr.30 du livre 23 pour **vérifier la conservation du suffixe**. Aucune modification de ces fichiers ni d'autres notes.

## 2. Dossier A — `book-23-psalm-133-note-004` contre `book-23-psalm-133-note-003`

| Étape | FAIT ÉTABLI | Portée / limite |
|---|---|---|
| **Source / pied imprimé** | PDF p.**1960**, **un seul pied imprimé local n°1**, **8/8 tokens**, « Il s’agit du chemin des formations esséniennes. » ; inspection visuelle historique **064-11/B**. | Le même pied est revendiqué par deux IDs, mais cela ne prouve pas deux occurrences distinctes. |
| **Appel** | Psaume **23/133**, appel au **verset 30** (p.1960) confirmé par 064 ; `note-004.appliesTo.verse=30`. | Un `verse` plus précis ne justifie pas l'identité 004 face à 003. |
| **Pilote 004** | Transcription du pied seul, **47 caractères**, `marker=1`, `pdfPage=1960`. | Transcription imprimée conforme, identité canonique non établie. |
| **Comparand historique 003** | Texte composite de **4606 caractères**, `verse=null` ; **préfixe exactement égal** aux 47 caractères de 004, suivi du corps versifié et de la prière Pr.30. `psalm-133.noteIds` référence les deux candidats. | L'ancien fichier 063 n'est pas authentifié ni invalidé dans ce lot. |
| **Frontière et conservation** | **Égalité exacte de tout le composite** : `text_003 === text_004 + " " + <versets 35–45 numérotés> + " Pr. 30. " + <texte de la prière autonome>`. Les versets **35–45** sont présents au psaume et la prière autonome `raphael-book-23-prayer-030.json` correspond **caractère par caractère** au suffixe. | On sait **où le texte se trouve déjà**, mais aucune réduction, fusion ou archivage de 003 n'est autorisé. |

### VERDICT INDIVIDUEL — `book-23-psalm-133-note-004`

- **FAIT ÉTABLI :** un seul pied physique de **8 tokens p.1960 au v.30**, copié exactement dans 004 et en préfixe de l'ancien composite 003. La suite du composite est déjà conservée dans le psaume et dans la prière Pr.30 autonome.
- **HYPOTHÈSE :** 004 est une nouvelle extraction mieux délimitée ; la date ou provenance de sa création et l'identité primaire du pied n'ont pas été démontrées.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** **frontière du pied** déterminée et **conservation intégrale** des fragments du composite 003 vérifiée par égalité stricte. Cela ne constitue pas une correction canonique autorisée ; **aucune mutation**.
- **DÉCISION NÉCESSITANT LUDO :** choix d'identité canonique 003/004 sur provenance, ou règle d'alias/archivage réversible ; approbation de la conservation et de la mise en cohérence de `noteIds`.
- **PREUVE MANQUANTE :** provenance des ID 063A/064 et décision de traitement du lien existant ; sans cela **NON RÉSOLUE**.
- **Empreintes des données au HEAD initial :** 004 `e06f03a0ead33c8ed124bdd4be1e8deb455bf344` ; historique 003 `226296a96ed1967ee7951def12d4e655c9fcbd04` ; psaume `812aac5deb7cbfd02d0da6de0ad0e5a0757d5021` ; Pr.30 `3b1838d9266cbc81eed557f0d551be398fb660a6`.

## 3. Dossier B — `book-26-psalm-189-note-003` contre `book-26-psalm-189-note-002`

| Étape | FAIT ÉTABLI | Portée / limite |
|---|---|---|
| **Source / pied imprimé** | PDF p.**2453**, **un seul appel n°1** et **un seul pied imprimé local n°1**, **29/29 tokens**, début « L’Archange fait ici référence à la pierre sacrée » ; preuve visuelle **064-12/B**. | Aucun deuxième pied imprimé pour deux IDs. |
| **Appel** | Psaume **26/189**, **verset 8** sur p.2453 ; `note-003.appliesTo.verse=8`. | Cette valeur ne démontre pas l'identifiant canonique face au concurrent 002 historique. |
| **Pilote 003** | Transcription du pied seul, **151 caractères**, `marker=1`, `pdfPage=2453`, statut machine non authentifié. | Texte du pied exact selon 064, mais double revendication persistante. |
| **Comparand historique 002** | `text` composite **4265 caractères**, `verse=null`. Les **151 premiers caractères** sont strictement ceux de 003. `psalm-189.noteIds` contient 002 et 003. | Le préfixe ne suffit pas à choisir un des deux ID. |
| **Corps présent dans le psaume** | Après les 151 caractères du pied, la concaténation numérotée **19–29** du psaume correspond **caractère par caractère** au début du suffixe : elle occupe **2434 caractères** hors séparateur. | **Attention : le suffixe total ne se limite pas à ces versets.** |
| **Suite non couverte par le psaume actuel** | Après le préfixe `pied + espace + v.19–29`, il reste **1679 caractères** dans l'ancien composite : continuation non numérotée après la fin actuelle du **v.29**, puis des passages numérotés **30–35**. Le JSON du psaume 26/189 **s'arrête au v.29** ; aucune destination canonique de ces 1679 caractères n'a été démontrée avec les fichiers du lot. | **CONSERVATION NON PROUVÉE pour ces 1679 caractères.** Ne pas les retirer. Leur présence dans le PDF original, leur rattachement définitif et l'existence éventuelle d'une autre destination nécessitent une preuve spécifique avant toute future correction. |

### VERDICT INDIVIDUEL — `book-26-psalm-189-note-003`

- **FAIT ÉTABLI :** un pied physique de **29 tokens p.2453, appel v.8** ; 003 le copie, et 002 historique commence par cette note exacte. Le composite contient aussi un corps versifié, dont la partie **v.19–29** recopie la version canonique actuelle.
- **HYPOTHÈSE :** 003 pourrait être une extraction plus propre du pied ; la suite de 002 pourrait provenir d'une capture de plusieurs pages ou d'un corps versifié plus étendu. Il n'existe **aucune preuve suffisante** dans ce lot permettant d'attribuer l'ID canonique ou la destination des 1679 caractères supplémentaires.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** limite des **151 caractères du pied imprimé** et correspondance exacte du segment numéroté v.19–29 démontrées. **AUCUNE séparation/troncature totale sûre** : il reste **1679 caractères non conservés par le psaume actuel** dans les fichiers examinés. Aucune mutation.
- **DÉCISION NÉCESSITANT LUDO :** identité 002/003 ou alias/archivage, préservation du texte historique intégral, autorisation d'investiguer puis de ranger correctement les fragments v.29-fin / 30–35 **avant toute réduction**, et mise à jour sûre de `noteIds`.
- **PREUVE MANQUANTE :** provenance d'ID et justification documentée de la destination de toute la suite composite. **NON RÉSOLUE**, sans faux verdict d'intégrité complète.
- **Empreintes des données au HEAD initial :** 003 `0469a312adaa734d51ee7337d12086dd58b94ef6` ; historique 002 `49abde7a85b0e5bfd653663544342a4e53378f0b` ; psaume `86c0d174f61cca9268a9b3c43784ef0a9d469b34`.

## 4. Plan de réconciliation — **PROPOSITION NON EXÉCUTÉE**

1. **Conserver intégralement** les deux composites historiques, les chaînes des notes pilotes et leurs SHA, ainsi que les liens `noteIds` préexistants.
2. **Pour 23/133 :** identifier la provenance canonique 003 ou 004, conserver une trace de l'autre ID ; le fait que la suite v.35–45 / Pr.30 soit déjà présente ailleurs ne donne pas permission de la supprimer ici.
3. **Pour 26/189 :** obtenir une preuve de destination **pour les 1679 caractères non couverts** par `psalm-189.json` (fin du v.29 puis passages numérotés 30–35). En l'absence de preuve, **ne pas tronquer** le composite ; ne pas supposer un périmètre source de psaume ou de prière non établi.
4. **Ludo décide explicitement** identité canonique, règle d'alias/archivage réversible, modifications nommées des notes/psaumes et gestion des `noteIds` ; ne pas départager d'après le suffixe 003/004, `verse` ou la seule concordance du pied.
5. Seulement après autorisation : tests de conservation **caractère par caractère**, un pied logique par appel, zéro texte ou lien orphelin, absence d'effets sur les autres JSON, diff limité aux fichiers approuvés. Aucun changement n'est effectué en 066-08.

## 5. Contrôles spécialisés documentaires

- **PASS** — Plan officiel 066-08 contient exactement les deux pilotes.
- **PASS** — Inventaire 066 : deux cas affectés à 066-08.
- **PASS** — Protocole 066-02 : provenance et conservation sans perte.
- **PASS** — Suivi 066-08 NON COMMENCÉE et arbre de base disponible.
- **PASS** — Notes pilotes et historiques portent leurs IDs distincts.
- **PASS** — 23/133 : même document, page 1960 et marqueur 1.
- **PASS** — 26/189 : même document, page 2453 et marqueur 1.
- **PASS** — Notes rattachées aux bons psaumes, ID pilotes et historiques dans noteIds.
- **PASS** — Pages 1960 et 2453 incluses dans le périmètre source des psaumes.
- **PASS** — Appels des notes pilotes : versets 30 et 8 localisés en page d'appel.
- **PASS** — Anciennes notes ont verse=null.
- **PASS** — Préfixe 23/133/004 : 47 caractères égaux au début du composite 003.
- **PASS** — 23/133 composite exactement pied + versets 35–45 + Pr.30.
- **PASS** — 23/133 versets 35–45 source canonique présents au psaume.
- **PASS** — 23/133 prière Pr.30 autonome rattachée à psaume 133.
- **PASS** — Préfixe 26/189/003 : 151 caractères égaux au composite 002.
- **PASS** — 26/189 suite au moins égale exactement aux versets 19–29 enregistrés.
- **PASS** — 26/189 19–29 présents aux sources canoniques page 2454.
- **PASS** — 26/189 suite supplémentaire de 1679 caractères non couverte par les versets du psaume.
- **PASS** — 26/189 suffixe commence par continuation non numérotée après texte canonique du verset 29.
- **PASS** — Quatre statuts machine non authentifiés.

**21/21 PASS** sur les données en lecture seule et archives déjà établies ; aucune réinspection visuelle du PDF ni nouvelle exécution GitHub Actions.

**CLÔTURE 066-08 : 2/2 pilotes examinés, 0 authentifié, 0 corrigé, 2 NON RÉSOLUS. Cumul 066-03 à 066-08 : 18/44 cas examinés, 44 anomalies toujours NON RÉSOLUES. PR #72 DRAFT, non fusionnée. STOP — 066-09 NON COMMENCÉE.**
