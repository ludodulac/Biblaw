# 🌸 BIBLAW — MISSION 069 — SÉCURISATION DES 11 NOTES PUBLIQUES

**Branche** `feat/052-search-ui` · **PR #72** DRAFT · **référence** `be57ccf828b1b601f686d912722f45c70d4a8fc4` · **correctif testé** `9718ed9e06d5e9e4c83ba6972b2175cf132c9d5b`.

## 1. Les onze notes publiques, et uniquement elles

Les métadonnées ci-dessous proviennent des onze fichiers déjà listés dans `data/catalog.json` et inclus dans `data/browser-search-catalog.json`. **Aucun PDF n'a été rouvert**. L'origine indiquée dans les onze JSON est `Bible essénienne (classée par livres).pdf`, avec les pages imprimées indiquées.

| Note publique (ID complet) | Validation dans les données | Page(s) imprimée(s) déclarée(s) | Rattachement existant | Affichage après 069 |
|---|---|---|---|---|
| `book-17-psalm-105-note-001` | `validated` — validation humaine (04/09/2026) | 1071 | `book-17-psalm-105`, v. 9 | Authentifiée ; liste, résultat et lecture autonome ; **également dans le psaume** |
| `book-17-psalm-109-note-001` | `machine-validated` | 1087 | `book-17-psalm-109`, v. 20 | **Non authentifiée**, contrôle automatique ; liste/recherche/lecture historique, **pas dans le panneau du psaume** |
| `book-17-psalm-112-note-001` | `machine-validated` | 1104 | `book-17-psalm-112`, v. 19 | Non authentifiée, contrôle automatique ; visibilité historique signalée |
| `book-17-psalm-121-note-001` | `machine-validated` | 1146 | `book-17-psalm-121`, v. 2 | Non authentifiée, contrôle automatique ; visibilité historique signalée |
| `book-17-psalm-122-note-001` | `machine-validated` | 1153 | `book-17-psalm-122`, v. 24 | Non authentifiée, contrôle automatique ; visibilité historique signalée |
| `book-17-psalm-127-note-001` | `machine-validated` | 1177 | `book-17-psalm-127`, v. 1 | Non authentifiée, contrôle automatique ; visibilité historique signalée |
| `book-17-psalm-130-note-001` | `machine-validated` | 1192 | `book-17-psalm-130`, v. 30 | Non authentifiée, contrôle automatique ; visibilité historique signalée |
| `book-18-psalm-112-note-001` | `machine-extracted-needs-human-review` | 1202–1204 | `book-18-psalm-112`, v. 14 | Non authentifiée, extraction à relire ; visibilité historique signalée |
| `book-19-psalm-104-note-001` | `machine-extracted-needs-human-review` | 1341–1344 | `book-19-psalm-104`, v. 22 | Non authentifiée, extraction à relire ; visibilité historique signalée |
| `book-21-psalm-143-note-002` | `manually-located-needs-transcription-review` | 1654 | `book-21-psalm-143`, note n°2 (pas de verset dans l'enregistrement public) | Non authentifiée, **transcription à relire** ; notice et résumé historiques, pas de promotion |
| `book-26-psalm-182-note-001` | `machine-extracted-needs-human-review` | 2417–2420 | `book-26-psalm-182`, v. 13 | Non authentifiée, extraction à relire ; visibilité historique signalée |

**Totaux : 11 notes historiquement publiques ; 1 à `validated`, 6 à `machine-validated`, 3 extraites automatiquement à relire, 1 localisée manuellement dont la transcription reste à réviser.** Soit **10 sans validation humaine du contenu**.

Toutes les onze notes déclarent le même PDF d'origine ; leurs identifiants sont uniques et les identifiants des psaumes cibles existent et comprennent leur ID dans `noteIds`. Dans le navigateur, aucune des onze n'a de `appliesToPrayerId` réciproque. La prière `michael-book-21-prayer-038` conserve une référence historique `noteIds` à `book-21-psalm-143-note-002`, **mais cela ne suffit pas pour authentifier ni afficher cette note comme une note de prière**.

## 2. Correction fonctionnelle livrée

Modifications **exclusivement dans `js/biblaw.js`**, plus un test et son workflow dédiés :

- **Classification stricte et centralisée :** seule `validation.status === 'validated'` signifie « Authentifiée ». `machine-validated`, `machine-extracted-needs-human-review`, `manually-located-needs-transcription-review` et les statuts inconnus portent **« Non authentifiée »**, avec la raison.
- **Affichage cohérent des surfaces déjà existantes :** les onze anciennes entrées restent dans le navigateur, mais leur statut apparaît dans la **liste de consultation**, le **titre des résultats**, le **détail d'un résultat**, la **fenêtre de lecture** et l'**export texte**. Dans la lecture et le résultat détaillé, une notice indique l'ID, le psaume cible, le verset s'il existe, le document et la page imprimée.
- **Aucune extension de publication :** seuls les objets déjà chargés depuis le catalogue public sont utilisés. Le panneau nouveau « Notes authentifiées » des psaumes reste réservé aux notes déjà publiques, avec statut humain, texte et lien réciproque. Pour la prière, présence du champ `noteIds` ne suffit plus : le lien inverse `appliesToPrayerId`, l'identité du psaume et le `noteIds` du psaume sont également exigés.
- La note `book-17-psalm-105-note-001` reste visible dans le psaume 105 ; la note automatique `book-17-psalm-109-note-001` n'y apparaît pas et reste lisible comme enregistrement historique explicitement **non authentifié**.
- Aucun statut source, texte de note, prière, psaume, alias, registre du résolveur ou catalogue n'a été modifié.

### Pourquoi ne pas retirer silencieusement les dix notes ?

Les retirer du bundle public ferait passer le total de **1 846 à 1 836** et modifierait la consultation par ID, les recherches de notes, les anciens liens éventuels et les attentes des tests. Ce serait un **changement éditorial de publication**, pas un simple correctif d'étiquette. La solution conservatoire retenue est **maintenir les onze objets déjà diffusés, expliciter leur statut et interdire toute nouvelle exposition contextuelle des dix non authentifiés**. Un futur retrait éventuel doit faire l'objet d'une décision de l'éditeur et d'un plan de compatibilité des identifiants. Attention : cette mission **ne rend pas privées** les dix notes historiques ; leur contenu reste accessible dans le catalogue déjà public.

## 3. Tests réellement effectués — PASS

Workflow : [BIBLAW 069 — GitHub Actions 41323835641](https://github.com/ludodulac/Biblaw/actions/runs/41323835641) — **SUCCESS** sur le correctif `9718ed9...`.

- Chromium **1280 px / 390 px tactile / 320 px tactile : PASS**. Les **11** fiches sont ouvertes chacune une seule fois ; statuts, PDF, ID, rattachement, avertissements, unicité du navigateur vérifiés.
- Recherche **par mots**, résultat de note automatique explicitement non authentifiée, ouverture de la fiche, **recherche par thème**, navigation psaumes et lecture d'une prière : **PASS**. Pas d'erreur JavaScript ni de requête vers les notes historiques privées.
- Psaume **17/105** : **1 note authentifiée contextuelle** ; psaume **17/109** : **0 note authentifiée** ; prière **21/38** : **0 note promue à tort** : **PASS**.
- Test de garde d'une note de prière **avec jeu de données synthétique exclusivement injecté dans Chromium**, jamais commité : note humaine liée réciproquement affichée, note automatique et note liée au mauvais psaume refusées : **PASS**. Cela valide le mécanisme, pas l'authenticité d'une nouvelle note historique.
- Contrôles spécialisés existants `verify_067.py`, résolveur 066 (`18 groupes / 36 IDs`) et audit des pièces jointes du bundle : **PASS**. Pas de réaudit documentaire 064–067, pas d'essai sur téléphone physique.

## 4. Non-régression et limites

Diff avec le HEAD de référence : **`js/biblaw.js`, `scripts/smoke_notes_069.mjs`, `.github/workflows/verify-notes-ui-069.yml` seulement** (hors présent rapport). Aucun changement aux **1 158 psaumes**, **677 prières**, **29 cas compatibles sans authentification**, **18 groupes de résolution** et **36 identifiants historiques**. Les **1 679 caractères historiques de 26/189** ainsi que les continuations non démontrées ne sont ni modifiés ni déclarés restaurés.

**Restent hors périmètre :** validation humaine des dix fiches, éventuel retrait éditorial des anciennes fiches publiques, intégration d'un résolveur de compatibilité dans le navigateur et validation sur appareils physiques.

**Livraison :** PR #72 **DRAFT**, non fusionnée ; **aucun déploiement**. STOP.
