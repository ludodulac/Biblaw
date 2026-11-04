# 🌸 BIBLAW — MISSION 065-12 — VERDICTS DU QUATRIÈME LOT C

**Statut : TERMINÉE — 4/4 réexaminées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.**

## Reprise et périmètre

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT au contrôle initial unique. HEAD de reprise `6c19acd27522fd08b2f128ded0b144ca4b6a7c58`, identique au dernier HEAD communiqué ; rapport 065-12 inexistant au départ et suivi NON COMMENCÉE.
- Périmètre exclusivement défini par les quatre IDs du lot **065-12 / classe C** dans `065_PLAN.md` et `065_INVENTAIRE.md`. Aucun résultat ni verdict des lots précédents rouvert.
- **Preuves réemployées** : uniquement [064-11](../064/064-11_VERDICTS.md) (p.1876–1877 et 1936–1937, artefacts A **12506424572**, B **12507282337**), [064-14](../064/064-14_VERDICTS.md) (p.2813–2814, artefact B **12576942014**) et [064-19](../064/064-19_VERDICTS.md) (p.3690, artefact B **12651183390**). Les artefacts concernés ont été contrôlés disponibles et non expirés.
- Vérifications ciblées en lecture seule : quatre JSON de note, quatre psaumes, deux prières autonomes (Pr.26/livre 23, Pr.102/livre 29), deux notes liées **uniquement pour constater les duplications** (23/129/004 déjà authentifiée ; 37/250/002 dossier historique 063). **Aucun PDF original rouvert ni nouvelle GitHub Action lancée.**
- Les corrections bloquées ne sont pas forcées : ne perdre aucun texte canonique, ne pas réattribuer une note de prière à un psaume et ne pas choisir sans preuve entre IDs concurrents.

## Verdicts individuels

### 1. `book-22-psalm-155-note-001`

- **Verdict 064 :** NON RÉSOLUE.
- **Verdict 065-12 :** **NON RÉSOLUE**.
- **Problème, texte imprimé, identité, doublons et rattachement :** Sur p.1876, la note imprimée n°1 est constituée de **231 tokens**, jusqu'à « sur toute la terre. ». Le JSON en contient 253 : les **22 tokens ajoutés** (« mort. Ainsi, ils n’entrent pas seulement… C’est la grande bénédiction. ») viennent du **verset 21** continué en haut de p.1877, pas du pied. Le psaume canonique `psalm-155.json` a bien p.1876–1877 dans ses pages mais **son verset 21 se termine à « après la »** et n'inclut pas ce passage. Le supprimer de la note laisserait ce fragment perdu des deux représentations canoniques. Le renvoi du verset 19 est présent, `noteIds` est réciproque ; pas de deuxième identifiant concurrent établi ici.
- **Sources vérifiées :** [064-11_VERDICTS.md](../064/064-11_VERDICTS.md), [GitHub Actions #39967539345](https://github.com/ludodulac/Biblaw/actions/runs/39967539345), artefact historique `12506424572` p.1876–1877 ; `data/notes/books/book-22/book-22-psalm-155-note-001.json` (blob `1527b84d43465424f940a843ec398a77444267fe`) ; `data/corpus/books/book-22/psalm-155.json` (blob `b393598044516df3042a0ca7a47690b2f5e32b50`).
- **Preuve/bloquant manquant :** Une restauration sûre et sourcée du texte intégral du verset 21 dans le psaume, avec autorisation ciblée de modifier le psaume, avant de découper le pied et de valider la note. Aucun tronquage isolé.
- **Correction :** Aucune ; la copie de secours du verset 21 reste intacte.

### 2. `book-23-psalm-129-note-003`

- **Verdict 064 :** NON RÉSOLUE.
- **Verdict 065-12 :** **NON RÉSOLUE**.
- **Problème, texte imprimé, identité, doublons et rattachement :** La note imprimée locale **n°1 p.1936** correspond aux 20 tokens du renvoi à l'« Évangile de l’Archange Ouriel », psaume 109. Le JSON 003 concatène ce pied avec le **texte versifié et la prière Pr.26**, objets éditoriaux séparés. Le pied existe déjà dans `book-23-psalm-129-note-004.json`, classé AUTHENTIFIÉE en 064-11, que nous avons consulté uniquement comme référence de collision, **sans réexaminer son verdict**. Le psaume 129 possède actuellement les versets **38, 39, 40** avec leurs textes présents intégralement dans le composite ; la prière autonome Pr.26 est également présente et son texte est contenu intégralement dans celui du composite. **Précision de traçabilité :** le rapport 064-11 mentionne « versets 38–45 », mais les JSON actuels ne montrent que 38–40 ; aucune affirmation d'existence des versets 41–45 ne peut être soutenue par ces fichiers. `noteIds` du psaume contient 003 et 004 : tronquer 003 et l'authentifier créerait un doublon non réconcilié.
- **Sources vérifiées :** [064-11_VERDICTS.md](../064/064-11_VERDICTS.md), [GitHub Actions #39967539345](https://github.com/ludodulac/Biblaw/actions/runs/39967539345), artefact historique `12507282337` p.1936–1937 ; `data/notes/books/book-23/book-23-psalm-129-note-003.json` (blob `9ef32d93651d36310aa8cc85d31d030967936d4e`) ; `data/corpus/books/book-23/psalm-129.json` (blob `3e936c87c56e9a5f914ef020d5f8990b06e4f3c6`); autre candidat `data/notes/books/book-23/book-23-psalm-129-note-004.json` (blob `d3323736b52914224945ea9bc2a0d641fc2fab13`); prière autonome `data/prayers/raphael-book-23-prayer-026.json` (blob `316b5b9050b94049183ddb0bcd5bdae10ee37d72`).
- **Preuve/bloquant manquant :** Réconciliation documentaire de l'identité 003/004 et des références `noteIds`, en distinguant les objets note, versets et prière ; clarification de la mention historique 38–45 sans modifier les psaumes ni les prières hors autorisation.
- **Correction :** Aucune ; conservation du composite 003 et des fichiers canoniques.

### 3. `book-29-psalm-212-note-001`

- **Verdict 064 :** NON RÉSOLUE.
- **Verdict 065-12 :** **NON RÉSOLUE**.
- **Problème, texte imprimé, identité, doublons et rattachement :** Sur la page imprimée **2814**, le seul pied n°1 de **4 tokens** est « Mot latin signifiant « assemblée ». », appelé après **« ecclesia¹ »** dans la prière **Pr.102**. Cette page n'appartient pas aux pages canoniques du psaume 212 `[2810–2813]`. Le JSON de note (193 tokens) comprend **la continuation de Pr.102** après ces quatre tokens (953 caractères). La prière autonome `michael-book-29-prayer-102.json` existe, porte bien l'appel « ecclesia1 » et est liée éditorialement au psaume 212, mais **sa propriété `text` ne contient ni le début ni la fin du suffixe repris dans la note**, ni son intégralité. L'attribution canonique de cette note à la prière ne résulte pas de `psalm-212.noteIds` et une troncature ferait perdre la continuation dans les fichiers canoniques.
- **Sources vérifiées :** [064-14_VERDICTS.md](../064/064-14_VERDICTS.md), [GitHub Actions #40135139792](https://github.com/ludodulac/Biblaw/actions/runs/40135139792), artefact historique `12576942014` p.2813–2814 ; `data/notes/books/book-29/book-29-psalm-212-note-001.json` (blob `8816236e7d2b21cbb5680aabd22e0e64b00642ba`) ; `data/corpus/books/book-29/psalm-212.json` (blob `d2fd9f1a911ae4d3573421dbb4542ffb1c2b5728`); prière autonome `data/prayers/michael-book-29-prayer-102.json` (blob `4072b814cf0d40e8ea355349f89b2d81738ca487`).
- **Preuve/bloquant manquant :** Restitution documentée de la continuation dans Pr.102 et relation explicite entre note et prière ; autorisation de modifier la prière et de réconcilier les liens du psaume avant toute correction de note.
- **Correction :** Aucune ; aucune suppression de la continuation de prière.

### 4. `book-37-psalm-250-note-003`

- **Verdict 064 :** NON RÉSOLUE.
- **Verdict 065-12 :** **NON RÉSOLUE**.
- **Problème, texte imprimé, identité, doublons et rattachement :** La page **3690** présente un **seul pied imprimé n°1 de 80 tokens** sur la statue, correspondant **exactement** au texte du JSON 003. Le fichier historique `book-37-psalm-250-note-002.json` (dossier antérieur 063 NON RÉSOLU) commence par **ce même texte**, sur la même page, puis ajoute des versets et de la prière dans une extraction composite. Le psaume conserve les deux IDs dans `noteIds` : aucune preuve ne départage les identités 002/003. De plus, la note 003 prétend `appliesTo.verse=11` alors que la question annotée (« qu’adviendra-t-il de la statue… ?¹ ») se trouve à la **fin du verset 36**, juste avant le verset 37. Une correction de verse=11 sans résolution de collision ne permettrait pas l'authentification complète.
- **Sources vérifiées :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md), [GitHub Actions #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034), artefact historique `12651183390` p.3690 ; `data/notes/books/book-37/book-37-psalm-250-note-003.json` (blob `d2b8fa7980c4706ac632a78ad10ff14309058ed5`) ; `data/corpus/books/book-37/psalm-250.json` (blob `3db54793cf7c6393b27125de28ac3aeecba7a291`); autre candidat `data/notes/books/book-37/book-37-psalm-250-note-002.json` (blob `306349abd72918ded9ecbe598be2487ea35b6461`).
- **Preuve/bloquant manquant :** Preuve d'identifiant canonique pour le pied unique p.3690 et décision de réconciliation avec 002 historique, suivies d'un rattachement explicitement certifié au renvoi de la fin du v.36, avec références canoniques cohérentes.
- **Correction :** Aucune ; ni modification de verset, ni dédoublonnage arbitraire.

## Contrôles spécialisés en lecture seule

- **PASS** — Quatre IDs exacts de 065-12, sans doublon.
- **PASS** — Quatre notes liées à leur psaume, et noteIds réciproques.
- **PASS** — Quatre notes non authentifiées automatiquement.
- **PASS** — 22/155/001 : suffixe de verset commence par « mort. » et p.1877 est page canonique.
- **PASS** — 22/155/001 : verset 21 tronqué « après la » et ne contient pas le suffixe.
- **PASS** — 23/129/003 : pied imprimé déjà porté intégralement par 004, sans arbitrage.
- **PASS** — 23/129/003 : versets 38, 39, 40 présents dans la copie composite.
- **PASS** — 23/129/003 : la prière autonome Pr.26 existe et son texte est conservé dans le composite.
- **PASS** — 29/212/001 : pied de quatre tokens p.2814 hors pages du psaume.
- **PASS** — 29/212/001 : Pr.102 contient l'appel ecclesia1 et est rattachée au psaume.
- **PASS** — 29/212/001 : continuation extraite absente du texte autonome de Pr.102.
- **PASS** — 37/250/003 : pied exact préfixe du composite 002, page identique.
- **PASS** — 37/250/003 : renvoi sur question de v.36, verse=11 erroné.
- **PASS** — 037/250/002 et 003 concurrents présents dans les noteIds canoniques.
- **PASS** — Suivi 065-12 NON COMMENCÉE, pas de clôture préalable.
- **PASS** — Arbre parent du commit initial disponible pour push non forcé.

**16/16 contrôles structuraux et documentaires ciblés PASS.** Les contrôles inspectent les JSON lus et appliquent les constats de PDF archivés (pas de nouvelles vérifications visuelles ou CI). Les anomalies sont constatées, et **non** certifiées résolues.

## Clôture et protections

- **065-12 : 4/4 examinées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.**
- **Cumul phase 065 : 42/46 notes réexaminées, 2 anomalies résolues, 44 NON RÉSOLUES, 4 encore à réexaminer.** Les 146 authentifications historiques 064 et tous les verdicts 065-02 à 065-11 demeurent inchangés.
- Aucune suppression de données, aucune modification des notes, psaumes, prières, interface, catalogue, workflows généraux ; aucun PDF rouvert, aucune fusion, publication ni déploiement. **STOP après 065-12 ; 065-13 NON COMMENCÉE.**
