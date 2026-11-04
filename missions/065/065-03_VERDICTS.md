# 🌸 BIBLAW — 065-03 — VERDICTS DU DEUXIÈME LOT

**Statut : TERMINÉE, REEXAMEN SANS RÉSOLUTION.** Branche `feat/052-search-ui`, PR #72 OPEN/DRAFT au contrôle d'entrée, HEAD initial `95d45b2bd3d483c317fe3d3d35b26399b5d4bb20`. Périmètre exclusif : les quatre notes affectées à 065-03 par `065_PLAN.md`. Aucun traitement des lots précédents ou suivants.

## Méthode et preuves

Les examens originaux des deux pages (PDF p.416 et p.432) sont **déjà documentés avec contrôle visuel** dans les verdicts 064-03 et 064-04 et dans les artefacts d'Actions existants (vérifiés **non expirés**). Les quatre fichiers note JSON et les deux fichiers psaume ont été consultés en lecture seule au HEAD d'entrée : texte, marqueur 1, identifiant, page, champ `appliesTo.verse`, statut technique `machine-extracted-needs-review`, portée des pages et liens réciproques `noteIds`. Les deux paires possèdent chacune **deux enregistrements pour une seule occurrence imprimée**. Les textes de chaque paire sont identiques et les pages concernées appartiennent aux psaumes, non à des prières.

**PDF original non rouvert**, car l'unicité du pied et ses limites sont déjà prouvées ; une nouvelle lecture ne désignerait pas l'identifiant canonique parmi deux captures concurrentes. Une valeur `verse` plus précise sur le fichier `-003` ne constitue pas une preuve d'attribution d'identité. Aucun choix, fusion, suppression ou promotion par conjecture.

## Décisions individuelles (ordre du plan officiel)

### 1. `book-07-psalm-047-note-002`

- **Verdict 064 : NON RÉSOLUE.**
- **Verdict 065-03 : NON RÉSOLUE.**
- **Justification :** Le pied n°1 de la p.416 (35 mots, police 9 pt) et son marqueur sont documentés en 064-03 comme uniques. Le texte et la page correspondent aux fichiers 002 et 003 ; `-002` a `appliesTo.verse=null`. Le renvoi appartient au psaume 47 ; la relation réciproque `noteIds` confirme les deux enregistrements techniques, pas deux notes imprimées.
- **Preuves :** [064-03_VERDICTS.md](../064/064-03_VERDICTS.md), [Actions #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426907184` (preuves de p.416, image/layout/`note-proof.json`), `data/notes/books/book-07/book-07-psalm-047-note-002.json` (blob `aa1063f9c3e4856fa8356a59b9f39fdc2cfa066d`), `data/corpus/books/book-07/psalm-047.json` (références `noteIds` et pages sources).
- **Preuve manquante pour conclure :** La provenance d'extraction permettant d'établir quel ID représente la seule note imprimée, et une règle de réconciliation des `noteIds` sans choisir arbitrairement l'ordinal 002.
- **Correction :** aucune ; `text`, `appliesTo`, `validation` et fichiers canoniques inchangés.

### 2. `book-07-psalm-047-note-003`

- **Verdict 064 : NON RÉSOLUE.**
- **Verdict 065-03 : NON RÉSOLUE.**
- **Justification :** `-003` reprend intégralement le même pied imprimé n°1 de 35 mots p.416 que `-002`, même psaume et même marqueur. `appliesTo.verse=30` apporte un rattachement plus précis que `-002`, sans prouver que 003 plutôt que 002 est l'identifiant canonique.
- **Preuves :** [064-03_VERDICTS.md](../064/064-03_VERDICTS.md), [Actions #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefact `12426907184` (preuves de p.416, image/layout/`note-proof.json`), `data/notes/books/book-07/book-07-psalm-047-note-003.json` (blob `f4b76d580d95938d3a1ecaaad2ae438256d0215c`), `data/corpus/books/book-07/psalm-047.json` (références `noteIds` et pages sources).
- **Preuve manquante pour conclure :** Une preuve d'identité canonique indépendante de la simple présence du numéro de verset 30, avec traçabilité des IDs et gestion sûre des références concurrentes.
- **Correction :** aucune ; `text`, `appliesTo`, `validation` et fichiers canoniques inchangés.

### 3. `book-08-psalm-025-note-002`

- **Verdict 064 : NON RÉSOLUE.**
- **Verdict 065-03 : NON RÉSOLUE.**
- **Justification :** Le seul pied n°1 de la p.432 (67 mots, police 9 pt) et l'appel dans le psaume 25 ont été confirmés en 064-04. `-002` et `-003` ont le même texte, la même page et le même marqueur ; `-002` ne porte pas de numéro de verset (`null`).
- **Preuves :** [064-04_VERDICTS.md](../064/064-04_VERDICTS.md), [Actions #39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802), artefact `12430728297` (preuves de p.432, image/layout/`note-proof.json`), `data/notes/books/book-08/book-08-psalm-025-note-002.json` (blob `345e902e882aaa1e978e716649df436952cb4f12`), `data/corpus/books/book-08/psalm-025.json` (références `noteIds` et pages sources).
- **Preuve manquante pour conclure :** La preuve de provenance attribuant l'unique note imprimée à un ID précis, puis les conditions de résolution de l'autre ID et des références `noteIds` sans perte de contenu.
- **Correction :** aucune ; `text`, `appliesTo`, `validation` et fichiers canoniques inchangés.

### 4. `book-08-psalm-025-note-003`

- **Verdict 064 : NON RÉSOLUE.**
- **Verdict 065-03 : NON RÉSOLUE.**
- **Justification :** Le fichier `-003` présente exactement le même pied n°1 de 67 mots p.432 que `-002`. `appliesTo.verse=18` est cohérent avec le thème « terre des vivants » du verset 18 du psaume 25, mais ne prouve pas l'unicité de cet ID contre `-002`.
- **Preuves :** [064-04_VERDICTS.md](../064/064-04_VERDICTS.md), [Actions #39791400802](https://github.com/ludodulac/Biblaw/actions/runs/39791400802), artefact `12430728297` (preuves de p.432, image/layout/`note-proof.json`), `data/notes/books/book-08/book-08-psalm-025-note-003.json` (blob `fa3ca63e09acf03fa2063ab07450586fa897b893`), `data/corpus/books/book-08/psalm-025.json` (références `noteIds` et pages sources).
- **Preuve manquante pour conclure :** Un document de provenance ou une règle canonique certifiée confirmant que 003 est l'identifiant à conserver plutôt que 002 ; traitement vérifiable des deux références actuelles, sans déduire l'identité du seul verset renseigné.
- **Correction :** aucune ; `text`, `appliesTo`, `validation` et fichiers canoniques inchangés.

## Contrôles spécialisés documentaires

Contrôles ciblés **en lecture seule** sur les informations relevées dans les sources GitHub ci-dessus ; il ne s'agit **pas** d'une nouvelle exécution GitHub Actions. Résultat : **12/12 PASS**.

- PASS — Périmètre : exactement 4 identifiants distincts de 065-03.
- PASS — Les quatre étaient NON RÉSOLUES dans les verdicts 064-03/04.
- PASS — Paire 07/047 : même page, psaume et marqueur 1.
- PASS — Paire 08/025 : même page, psaume et marqueur 1.
- PASS — Paire 07/047 : texte identique 35 mots imprimés dans les deux fichiers.
- PASS — Paire 08/025 : texte identique 67 mots imprimés dans les deux fichiers.
- PASS — 07/047 : champs verse null contre 30.
- PASS — 08/025 : champs verse null contre 18.
- PASS — Psaumes : deux références noteIds concurrentes par paire.
- PASS — Pages imprimées incluses dans les pages canoniques des deux psaumes.
- PASS — Sources de preuve 064 disponibles dans les artefacts existants non expirés.
- PASS — La seule occurrence imprimée par paire ne démontre aucun second ID autonome.

**Garde de modification :** la seule écriture de 065-03 concerne ce rapport, `065_PROGRESS.md` et `missions/STATE.md`. Aucun JSON canonique, psaume, prière, catalogue, interface ou workflow modifié. Aucun nouveau doublon introduit. Les trois échecs CI généraux préexistants ne sont ni réparés ni rejoués.

## Bilan

- **4/4 notes examinées : 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.**
- **065 cumulé : 8/46 réexaminées, 0 résolue, 46 NON RÉSOLUES** (8 revues, 38 à examiner).
- Conflits d'identité inchangés. Aucune nouvelle authentification technique ni éditoriale ; PDF non rouvert, aucune modification canonique.
- **STOP après 065-03 ; 065-04 NON COMMENCÉE.**
