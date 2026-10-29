# 🌸 BIBLAW — 066-07 — CONFLITS HISTORIQUES ET RATTACHEMENTS DE VERSETS

**Statut : TERMINÉE — 2/2 notes pilotes examinées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 2 NON RÉSOLUES.** Aucun fichier du corpus modifié.

## 1. Mandat strict, archives et méthode

- [066_PLAN.md](066_PLAN.md) attribue **seulement** `book-27-psalm-169-note-004` et `book-37-psalm-250-note-003` à 066-07. Les anciens `book-27-psalm-169-note-002` et `book-37-psalm-250-note-002`, tous deux **non résolus du cycle 063**, ont été **consultés en lecture seule comme comparands**, sans nouveau verdict, réexamen ou affectation à cette mission.
- GitHub : `ludodulac/Biblaw`, branche `feat/052-search-ui`, HEAD initial `ae838dffb36d8b35bae22d62542a1c7832ef5d26` identique au communiqué ; PR #72 **OPEN, DRAFT, non fusionnée** lors de l'unique vérification initiale.
- Application du [protocole 066-02](066-02_PROTOCOL.md) : source imprimée → appel → pied physique → candidats ; un préfixe textuel exact ou une métadonnée `verse` ne démontre pas l'ID canonique ; les suffixes de psaume et prière doivent rester intégraux.
- **Preuves papier archivées, sans nouveau PDF** : [064-13](../064/064-13_VERDICTS.md), p.2534, [Action 40130414394](https://github.com/ludodulac/Biblaw/actions/runs/40130414394), artefact A `12574772504` ; [064-19](../064/064-19_VERDICTS.md), p.3690, [Action 40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034), artefact B `12651183390`. Les deux artefacts **non expirés**.
- Verdicts intermédiaires repris : [065-11](../065/065-11_VERDICTS.md) pour 27/169/004 et [065-12](../065/065-12_VERDICTS.md) pour 37/250/003. Contrôles techniques ciblés uniquement sur les **deux notes pilotes, leurs deux notes historiques comparées, deux psaumes et deux prières autonomes** ; aucun nouvel audit général ou GitHub Actions.

## 2. Pied physique A — 27/169 p.2534 : concurrence 004 ↔ 002 historique

| Étape | Fait établi et provenance | Limite / blocage |
|---|---|---|
| **Source imprimée** | [064-13/A](../064/064-13_VERDICTS.md) atteste **un seul pied n°1 de 48/48 tokens** p.2534, sur le symbole du caducée, fin « soleil ailé. ». | Une seule occurrence ne permet pas d'authentifier deux fichiers distincts. |
| **Appel imprimé** | **Verset 30 du psaume 169**, page 2534 ; la note 004 déclare `appliesTo.verse=30`. | Rattachement correct du *pied* ≠ preuve de provenance de l'ID 004. |
| **Candidat 004** | `text` de **252 caractères**, pied complet ; `source.pdfPage=2534`, `marker=1`, `validation.status=machine-extracted-needs-review`. | L'extraction courte pourrait être correcte, mais rien ne prouve qu'elle doive être l'unique fichier canonique. |
| **Ancien 002 du 063 (comparand, non retraité)** | **4179 caractères**, commence **exactement** par les 252 caractères de 004, puis les versets **34–42** et la prière **Pr.63**. Les deux IDs sont présents dans `psalm-169.noteIds`. | Réduire le composite sans accord risque de perdre la trace de provenance et de créer un doublon logique. |
| **Garde de conservation de la suite** | Les versets numérotés **34–42** reproduisent exactement les versets du psaume (p.2535–2536). La suite Pr.63 correspond **caractère par caractère** à `raphael-book-27-prayer-063.json`, sauf **le chiffre « 1 » immédiatement après « Amin Salama »**, marqueur d'appel figurant dans le composite. **En retirant seulement ce marqueur, tout le composite égale exactement** pied 004 + versets 34–42 + « Pr. 63. » + texte de prière autonome. | Le marqueur « 1 » fait partie de l'extraction historique ; **ne pas le supprimer**. L'ID du pied reste indécidable. |

### Verdict individuel : `book-27-psalm-169-note-004`

- **FAIT ÉTABLI :** pied physique unique n°1 de **48 tokens p.2534**, appelé au **v.30**, texte de 004 **identique intégralement** au début de l'ancienne 002. Le suffixe composite de 002 contient des versets et une prière déjà conservés de manière autonome, avec une différence de marqueur « 1 » décrite, sans texte mystérieux inventé.
- **HYPOTHÈSE :** 004 pourrait être une nouvelle extraction mieux délimitée du même pied que 002 (063). Cette qualité de frontière ne démontre **pas** l'antériorité ou la primauté éditoriale de l'ID.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** limite du pied à **252 caractères**, rapportée à la preuve 064 ; segmentation du composite ancien en pied + versets 34–42 + Pr.63 **techniquement vérifiée**, avec repérage du marqueur ajouté. Cela **ne constitue pas** une permission d'écrire, tronquer ou authentifier 004.
- **DÉCISION NÉCESSITANT LUDO :** attribuer de façon justifiée l'identité canonique du pied à 002 ou 004, ou valider une stratégie d'alias/archivage non destructif ; approuver expressément la migration des `noteIds` et le traitement du composite. Aucune décision déduite de l'ordinal.
- **PREUVE MANQUANTE :** provenance historique indépendant des seuls textes, page, marqueur et champ `verse`, et décision de conservation avec liens réconciliés. **VERDICT : NON RÉSOLUE**.
- **Empreintes :** note pilote `data/notes/books/book-27/book-27-psalm-169-note-004.json` blob `4b033ca7d43888761ee1a478af4d6a8b07769a31`, note historique `data/notes/books/book-27/book-27-psalm-169-note-002.json` blob `ab69a109d2110b13f2262aeb83f8f591b58e6626`, psaume blob `5edf3f37cc4ab832991b0f335d7efe8c6130f43c`, prière autonome Pr.63 blob `48a96cd82a7c539d4bd2a5c7bef51c2c7c8e2065`.

## 3. Pied physique B — 37/250 p.3690 : concurrence 003 ↔ 002 historique et verset erroné

| Étape | Fait établi et provenance | Limite / blocage |
|---|---|---|
| **Source imprimée** | [064-19/B](../064/064-19_VERDICTS.md) atteste **un pied local n°1 unique de 80/80 tokens** p.3690, sur la statue. | La concurrence des deux extractions n'autorise aucune double authentification. |
| **Emplacement exact de l'appel** | Question « qu’adviendra-t-il de la statue… ?¹ » à la **fin du verset 36**, **p.3690**, juste **avant le verset 37**. Le verset 36 du JSON du psaume contient aussi le signe `?1`. | `appliesTo.verse=11` de 003 est **objectivement erroné** pour cette occurrence ; le verset 11 est déclaré en p.3687. |
| **Candidat 003** | Note de **454 caractères**, exactement le pied imprimé unique ; `pdfPage=3690`, `marker=1`, `verse=11`. | La correction de verse **11→36 est démontrable pour l'appel imprimé**, mais ne résout pas la concurrence d'ID avec 002 et ne doit pas être appliquée sans autorisation. |
| **Ancien 002 du 063 (comparand, non retraité)** | Extraction composite de **2883 caractères**, dont les **454 premiers** égalent **exactement** la note 003. Suite : versets numérotés **42–44** p.3691 et **Pr.135**. Les deux IDs figurent dans `psalm-250.noteIds`. | Ne pas supprimer ou tronquer le composite historique tant que son archivage, ses liens et la conservation du texte ne sont pas autorisés. |
| **Garde de conservation de la suite** | `text_002 === text_003 + " " + <versets 42–44 numérotés> + " Pr. 135. " + <texte de la prière autonome>` **à l'identique**. Les versets sont dans `psalm-250` et Pr.135 dans `michael-book-37-prayer-135.json`, rattachée à ce psaume. | Exactitude de segmentation ≠ droit de réduire 002 ni identité canonique de 003. |

### Verdict individuel : `book-37-psalm-250-note-003`

- **FAIT ÉTABLI :** un pied unique de **80 tokens p.3690** et un renvoi au **v.36, non au v.11**. La note 003 reproduit intégralement le pied ; l'ancien 002 en reprend exactement le texte initial, suivi des versets 42–44 et de Pr.135 déjà conservés.
- **HYPOTHÈSE :** 003 pourrait être l'extraction courte issue d'une étape ultérieure, et le rattachement au verset 11 pourrait être une erreur de l'extracteur. La cause technique exacte de l'erreur n'est **pas prouvée**, seul son constat l'est.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** l'emplacement de l'appel est **v.36** ; la différence de métadonnée `11→36` est certaine **pour cet appel**, et le composite ancien peut être segmenté intégralement. **Aucune correction effective des champs `appliesTo` ni du composite** sans arbitrage de Ludo.
- **DÉCISION NÉCESSITANT LUDO :** déterminer/autoriser un ID canonique 002 ou 003, une politique éventuelle d'alias ou d'archivage, le rattachement corrigé au **verset 36** sur l'ID retenu et la réconciliation des `noteIds` sans lien orphelin.
- **PREUVE MANQUANTE :** provenance certifiée de l'identité 002/003 et instruction éditoriale pour traiter la duplication. **VERDICT : NON RÉSOLUE**.
- **Empreintes :** note pilote `data/notes/books/book-37/book-37-psalm-250-note-003.json` blob `d2b8fa7980c4706ac632a78ad10ff14309058ed5`, historique `data/notes/books/book-37/book-37-psalm-250-note-002.json` blob `306349abd72918ded9ecbe598be2487ea35b6461`, psaume blob `3db54793cf7c6393b27125de28ac3aeecba7a291`, prière Pr.135 blob `ff392e9c7f7de31265e266894ac700dfa5b1ac0b`.

## 4. Plan de réconciliation **proposé et non exécuté**

1. **Préserver le snapshot** des six JSON de note/psaume et deux prières lus : SHA listés ci-dessus, quatre chaînes `text` complètes et références `noteIds` avant toute modification.
2. **Tracer chaque pied physique** (27/169 p.2534 v.30, 37/250 p.3690 v.36) et associer ses deux candidats sans élire celui qui dispose du `verse` le plus précis ou du texte le plus court.
3. **Isoler conceptuellement les composites historiques**, sans retirer leurs suffixes : 27/169/002 (versets 34–42 + Pr.63 + marqueur d'appel « 1 »), 37/250/002 (versets 42–44 + Pr.135). Destinations déjà vérifiées par comparaison intégrale, sans créer de nouveau fichier.
4. **Soumettre à Ludo** : identité retenue ou convention d'alias par pied ; conservation des historiques 063 ; liste exacte des fichiers JSON à modifier ; correction du verset 11→36 pour le pied de 37/250 ; migrations réversibles de `noteIds`.
5. **Après autorisation explicite seulement** : tests d'un pied logique par appel, conservation des fragments **caractère par caractère**, du marqueur de prière en provenance, page/verset correct, absence de doublon et d'orphelin dans les liens, SHA hors périmètre inchangés. **Aucun de ces changements n'est exécuté en 066-07.**

## 5. Contrôles spécialisés en lecture seule

- **PASS** — Plan officiel 066-07 : exactement 2 IDs pilotes.
- **PASS** — Inventaire : 2 IDs attribués uniquement à 066-07.
- **PASS** — 066-02 : protocole de provenance et conservation accessible.
- **PASS** — Précondition de suivi et arbre parent.
- **PASS** — Deux notes pilotes identifiées et historiques seulement comparés.
- **PASS** — Notes pilotes, historiques et psaumes : recordId cohérent.
- **PASS** — 27/169 : même page 2534, marqueur local 1 et source.
- **PASS** — 37/250 : même page 3690, marqueur local 1 et source.
- **PASS** — 27/169 : pied 004 exactement en préfixe de 002 historique.
- **PASS** — 37/250 : pied 003 exactement en préfixe de 002 historique.
- **PASS** — 27/169 : préfixe + versets 34–42+ Pr.63 avec unique marqueur '1' reproduit exactement le composite.
- **PASS** — 27/169 : sans marqueur d'appel 1, prière et versets exactement conservés.
- **PASS** — 37/250 : préfixe + versets 42–44 + Pr.135 exactement égal au composite.
- **PASS** — 27/169 : verset 30 présent page 2534 et champ verse=30.
- **PASS** — 37/250 : appel statue en fin du verset 36 p.3690, métadonnée erronée verse=11.
- **PASS** — Psaumes : IDs pilotes et historiques chacun une fois dans noteIds.
- **PASS** — Psaumes : pages du pied et des suffixes dans la portée.
- **PASS** — 27/169 : neuf versets 34–42 intégralement sur pages 2535/2536.
- **PASS** — 37/250 : versets 42–44 intégralement page 3691.
- **PASS** — Prières autonomes Pr.63 et Pr.135 rattachées à leur psaume.
- **PASS** — Quatre notes, pilotes et historiques, non authentifiées techniquement.

**21/21 PASS.** Unicité et disposition typographique des pieds attestées par les rapports 064 existants ; les tests ci-dessus démontrent seulement la correspondance actuelle des JSON et la cohérence documentaire. **Aucun PDF original rouvert ; aucune nouvelle GitHub Action.**

**Clôture : 066-07 TERMINÉE — 2/2 notes pilotes, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 2 NON RÉSOLUES. Cumul 066-03…066-07 : 16/44 notes pilotes examinées, 44 anomalies toujours NON RÉSOLUES, aucune nouvelle correction. PR #72 DRAFT, non fusionnée. STOP — 066-08 NON COMMENCÉE.**
