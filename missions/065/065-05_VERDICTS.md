# 🌸 BIBLAW — MISSION 065-05 — VERDICTS CIBLÉS

**Statut : TERMINÉE — quatre notes examinées, deux CORRIGÉES ET AUTHENTIFIÉES, deux NON RÉSOLUES.** Branche `feat/052-search-ui`, PR #72 DRAFT au contrôle initial, HEAD antérieur `caeaeda78a64efd45bd1137814312a8677662032`. Ce lot correspond exclusivement à la ligne 065-05 de `065_PLAN.md`.

## Procédure et sources

Les seuls rapports antérieurs utilisés sont 064-03, 064-05, 064-10 et 064-09. Leurs archives de preuves contiennent les lectures visuelles, renvois et limites des pages 387, 764, 1692, 1487–1488 ; **aucun PDF original réouvert**, aucune GitHub Action spécialisée rejouée. Les quatre notes et les quatre psaumes correspondants ont été confrontés en lecture seule ; les deux notes corrigées ont été comparées à la preuve documentaire du pied. Pour la prière 7, la correspondance du **suffixe complet** du JSON composite avec le champ `text` de `ouriel-book-20-prayer-007` a été vérifiée caractère par caractère.

Les deux corrections de note sont limitées aux éléments probants ; aucun psaume ou prière n'est modifié. Les statuts techniques restent `machine-extracted-needs-review` : le **verdict éditorial** est enregistré ici et ne constitue ni publication ni promotion technique automatique.

## Verdicts individuels

### 1. `book-07-psalm-035-note-005`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-05) :** **NON RÉSOLUE**.
- **Preuves archivées utilisées :** [064-03](../064/064-03_VERDICTS.md), p.387, [Actions #39781270188](https://github.com/ludodulac/Biblaw/actions/runs/39781270188), artefacts A `12426552703` et B `12426907184` ; JSON 005, notes 003 et 004 (déjà AUTHENTIFIÉES en 064-03) et `psalm-035.noteIds`.
- **Motif documentaire :** L'extraction 005 de 57 mots est la concaténation du pied imprimé n°1 de 25 mots et du pied n°2 de 31 mots, déjà préservés séparément sous les notes 003 et 004. Aucune troisième note imprimée. Valider 005 créerait un doublon ; le supprimer nécessite de réconcilier `noteIds` dans le psaume, modification interdite pour 065-05.
- **Correction :** Aucune ; le JSON 005 et le psaume demeurent inchangés.
- **Preuve manquante / limite :** Décision d'archivage/neutralisation de l'identifiant composite 005 et mise en cohérence démontrée du `psalm-035.noteIds` sans perdre les deux notes existantes.

### 2. `book-12-psalm-077-note-001`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-05) :** **NON RÉSOLUE**.
- **Preuves archivées utilisées :** [064-05](../064/064-05_VERDICTS.md), p.764, [Actions #39793260093](https://github.com/ludodulac/Biblaw/actions/runs/39793260093), artefact B `12432815616` ; JSON 001 et `psalm-077.noteIds`.
- **Motif documentaire :** Le fichier de 89 mots concatène les trois pieds imprimés 1, 2 et 3. Seul le préfixe de 23 mots correspond au pied 1. Les appels 2 et 3 existent dans le verset 1, mais le psaume ne référence qu'un fichier 001. Tronquer ce fichier sans créer et rattacher les deux autres ne préserverait pas l'intégralité du corpus.
- **Correction :** Aucune ; texte composite conservé pour ne pas perdre les notes 2 et 3.
- **Preuve manquante / limite :** Trois fiches documentées avec rattachement distinct et correction réciproque de `psalm-077.noteIds`. Toute modification du psaume est interdite dans 065-05.

### 3. `book-21-psalm-150-note-002`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-05) :** **CORRIGÉE ET AUTHENTIFIÉE**.
- **Preuves archivées utilisées :** [064-10](../064/064-10_VERDICTS.md), p.1692, [Actions #39964677882](https://github.com/ludodulac/Biblaw/actions/runs/39964677882), artefact A `12506082816` ; JSON 002 et verset 32 de `psalm-150` contenant le renvoi imprimé « débauche2 », `noteIds` réciproque.
- **Motif documentaire :** Le seul pied imprimé n°2 est « Exode 32. » (deux tokens). Le suffixe commençant « commandements. Mais en l'absence... » appartient à la suite du corps versifié, et non à la note. La source, la limite, l'appel au verset 32 et le texte sont documentés.
- **Correction :** Dans le seul JSON 21/150/002, `text` devient « Exode 32. » et `appliesTo.verse` devient 32 à la place de null. Autres champs et psaume inchangés.
- **Preuve manquante / limite :** Aucune sur ce pied ; validation technique conservée en revue indépendamment du verdict éditorial.

### 4. `book-20-psalm-110-note-001`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-05) :** **CORRIGÉE ET AUTHENTIFIÉE**.
- **Preuves archivées utilisées :** [064-09](../064/064-09_VERDICTS.md), p.1487–1488, [Actions #39957324167](https://github.com/ludodulac/Biblaw/actions/runs/39957324167), artefact A `12503002405` ; JSON 001, `psalm-110.noteIds`, et prière canonique `data/prayers/ouriel-book-20-prayer-007.json` (blob `2f42b0cd773733530798c8c0321032abf63de038`).
- **Motif documentaire :** Le seul pied imprimé n°1 est « Il s’agit du Nom de la Mère. » (8 tokens). Le suffixe est « Pr. 7. » suivi du texte exact de la prière autonome déjà présente dans le corpus et rattachée à `book-20-psalm-110` ; correspondance **exacte de toute la chaîne**, sans perte de contenu.
- **Correction :** Dans le seul JSON 20/110/001, `text` devient « Il s’agit du Nom de la Mère. ». Le texte autonome de la prière 7, son fichier et le psaume ne sont pas modifiés.
- **Preuve manquante / limite :** Aucune sur l'identité, les limites ou le rattachement de cette note ; validation machine laissée en revue.

## Tests spécialisés exécutés sur les données sources et les corrections

- PASS — Périmètre des modifications strictement 065-05.
- PASS — Lot 065-05 absent des résultats et NON COMMENCÉ.
- PASS — Conservation exacte : pied 20/110 + Pr.7 == texte composite original.
- PASS — Prière autonome existante correctement rattachée au psaume 110.
- PASS — Note 20/110 : page 1487, appel 1, verset 22 préservé.
- PASS — 21/150 : note extraite = « Exode 32. » + suffixe de psaume.
- PASS — 21/150 : marqueur 2 sur p.1692, psaume 150.
- PASS — Statuts machine restent en revue (non promotion).
- PASS — Arbre Git parent disponible.
- PASS — Dédoublement de la prière : aucun caractère perdu.
- PASS — Texte corrigé 20/110 exact.
- PASS — Texte corrigé 21/150 exact.

**Résultat : 12/12 PASS.** Contrôles structurels réellement exécutés sur les objets obtenus de GitHub au HEAD initial et leurs modifications en mémoire ; l'inspection PDF demeure celle des rapports 064, pas une nouvelle inspection. La prière 7 autonome est déjà conservée dans un JSON distinct et n'est pas éditée. Aucun nouveau doublon : les deux composites 07/035 et 12/077 demeurent inchangés, en attente d'un processus autorisé portant également sur les références des psaumes.

## Cumul

**065-05 : 4/4 notes traitées, 0 AUTHENTIFIÉE sans correction, 2 CORRIGÉES ET AUTHENTIFIÉES, 2 NON RÉSOLUES.**

**065 : 16/46 réexaminées, 2 anomalies résolues, 44 NON RÉSOLUES, dont 30 jamais réexaminées.** Les 146 décisions d'authentification 064 sont préservées ; aucun psaume/prière, interface, catalogue, workflow général, publication, déploiement ni fusion. **STOP APRÈS 065-05 ; 065-06 NON COMMENCÉE.**
