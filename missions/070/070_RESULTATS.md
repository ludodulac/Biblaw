# 🌸 BIBLAW — MISSION 070 — LECTURE ET NAVIGATION

**Branche :** `feat/052-search-ui` · **référence :** `1d6d18ba57786698dd88798cab85fc661a0c94bc` · **correctif testé :** `6ba1cb1eba76274565076863df81eb0f9ffec77e` · **PR #72 : DRAFT**.

## 1. Dysfonctionnements fonctionnels corrigés

1. **Prières associées inaccessibles depuis la lecture normale :** auparavant, un psaume ne montrait ses prières en lecture que si la case « Prières » du **filtre de recherche** était cochée ; en consultation par catalogue, cette option était même ignorée. Désormais, chaque psaume propose **une liste explicite et indépendante des filtres**, avec un bouton par prière réciproquement reliée et une référence au psaume. Le comportement historique d'affichage du texte intégral des prières quand le filtre est coché reste intact. Le texte canonique ne change pas.
2. **Absence de retour dédié aux résultats :** précédemment, « Retour à la liste » n'apparaissait que depuis la consultation du catalogue ; depuis un résultat, il fallait fermer par « × » sans indication. Un bouton **« Retour aux résultats »** est désormais présent en lecture issue d'une recherche, et **« Retour à la liste »** en lecture issue du catalogue. Retour au bouton exact qui a ouvert le texte, et conservation de la requête, des résultats développés et de la position de défilement de la page.
3. **Navigation interne psaume ↔ prière :** les boutons « Lire la prière » ouvrent la prière sans fermer le dialogue, et **« Retour au texte précédent »** revient au psaume avec sa position de lecture. Une prière ouverte directement via le catalogue propose **« Lire le psaume source »**, si les rattachements sont réciproques. La pile de lecture est réinitialisée à la fermeture ; le dialogue n'est jamais rouvert via un deuxième `showModal()`.
4. **Affichage des longs psaumes :** `white-space: pre-wrap` préserve les retours à la ligne déjà présents dans les versets ; colonne et texte longs protégés contre le débordement horizontal ; typographie, interligne, numérotation et en-tête adaptés ; commandes de lecture accessibles au toucher (hauteur minimale **44 px**), au clavier et à **320 px**. Aucun verset, numéro ou paragraphe source n'est réécrit.

## 2. Tests d'interaction réels — PASS

Workflow [BIBLAW 070 — GitHub Actions #41327400535](https://github.com/ludodulac/Biblaw/actions/runs/41327400535) — **SUCCESS**, Chromium avec chargement du véritable payload Pages **en staging local, sans déploiement**.

| Parcours | 1280 px | 390 px tactile émulé | 320 px tactile émulé |
|---|---|---|---|
| Recherche du psaume 105 → résultat → lecture → prière → retour au psaume et aux mêmes résultats/position | PASS | PASS | PASS |
| Texte du psaume 17/105 : seule la note humaine authentifiée attachée | PASS | PASS | PASS |
| Notes historiques 17/109 « Non authentifiée », 17/105 « Authentifiée » ; avertissements lisibles, pas de débordement horizontal | PASS | PASS | PASS |
| Navigation réelle par catégorie de textes, sans recharger la recherche | PASS | PASS | PASS |
| Prière `ouriel-book-24-prayer-036` : **1 968 caractères** dans le bundle ; lecture et aller-retour vers `book-24-psalm-141` | PASS | PASS | PASS |
| Psaume long de **90 versets** : tous les versets présents, numérotation, `pre-wrap`, vrai défilement, fermeture, pas de débordement horizontal | PASS | PASS | PASS |
| Recherches, clics, ouvertures, fermetures : aucune erreur JS ni requête vers `data/notes/**` | PASS | PASS | PASS |
| Activation au **clavier** des résultats et des prières (Entrée), retour au psaume, fermeture (Échap), reprise du focus | PASS | Non testé | Non testé |

**Cas particulier des prières multiples :** la vérification dynamique du catalogue public (1 158 psaumes/677 prières) n'a trouvé **aucun psaume comportant deux prières ayant toutes deux des liens réciproques complets**. Il serait donc inexact de présenter le test de « plusieurs prières réelles » comme un succès documentaire. Pour tester malgré tout la capacité logicielle, un jeu de données **synthétique, injecté exclusivement dans Chromium** a ajouté temporairement une deuxième prière à 17/105. Les deux identifiants distincts sont apparus, toutes deux ont été ouvertes séparément et les retours n'ont fait disparaître aucune des deux : **PASS fonctionnel en simulation**. Cette donnée de test **n'est ni enregistrée dans le corpus, ni publiée**. Le cas « deux prières réelles authentiquement reliées » reste **non démontrable avec ce catalogue**.

## 3. Conservation et périmètre

Diff par rapport au HEAD de référence : `js/biblaw.js`, `css/biblaw.css`, `index.html`, `scripts/smoke_reader_070.mjs`, `.github/workflows/verify-reader-070.yml`, plus **adaptation mécanique de trois assertions de la CI existante** dans `.github/workflows/validate-search-ui.yml` (nouvelle signature du lecteur / texte de rendu). La CI thématique existante est repassée au vert, workflow **#41327064481 SUCCESS**. Les workflows des missions **068 et 069** étaient également **SUCCESS** après la modification fonctionnelle du lecteur, avant l'ajustement final du script de test.

**Aucun changement à** `data/catalog.json`, `data/corpus/**`, `data/prayers/**`, `data/notes/**`, `data/browser-search-catalog.json`, aux statuts de validation, aux identifiants ni au résolveur de compatibilité. Pas de réaudit PDF, pas de modification des **1 158 psaumes**, **677 prières**, **11 notes historiques publiées**, **29 cas compatibles** ou **18 groupes** de résolution. Les limitations historiques non restaurées (dont les **1 679 caractères** de 26/189) sont intactes.

**Réserves :** aucun essai sur appareil physique ; 390 et 320 px sont des émulations Chromium. Plusieurs prières par psaume sont validées **par simulation d'interface**, mais pas par un exemple complet actuellement présent dans le catalogue public. Les 10 notes déjà publiées mais non authentifiées demeurent distinctement averties et n'ont pas été rendues contextuelles.

**Livraison :** PR #72 **toujours DRAFT**, aucun merge, aucun déploiement. **STOP après rapport**.
