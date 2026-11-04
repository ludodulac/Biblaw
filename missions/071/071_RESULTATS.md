# 🌸 BIBLAW — MISSION 071 — VALIDATION UTILISATEUR

**Référence :** `ab04ab75630c243653e8ddf154790de3d47d00cb` · **branche :** `feat/052-search-ui` · **PR #72 : DRAFT** · **aucun merge / déploiement**.

## 1. Prévisualisation utilisable, sans publication

Le vrai site `_site/` a été reconstruit depuis la branche à partir de la liste autorisée de `scripts/build_pages_site.py`. Les contrôles Chromium ont utilisé **ce site assemblé**, servi localement par HTTP, et non un substitut ni le site en production.

**Artefact de la prévisualisation :** [Télécharger biblaw-071-preview.zip depuis GitHub Actions](https://github.com/ludodulac/Biblaw/actions/runs/41440453540/artifacts/13140830173) (**18 776 464 octets** dans l'archive, conservation programmée de **7 jours**, accès GitHub au dépôt nécessaire). La prévisualisation n'a pas d'URL de site public.

**Utilisation locale :** se connecter à GitHub, télécharger l'artefact, extraire le ZIP dans un dossier, ouvrir un terminal dans le dossier contenant `index.html`, exécuter `python -m http.server 4173`, puis ouvrir **`http://localhost:4173/index.html`** dans le navigateur. Ne pas ouvrir `index.html` directement en `file://` : le site charge des JSON par `fetch()`. Un autre serveur HTTP statique local est aussi possible. Sur téléphone, une consultation depuis le réseau local exige un serveur joignable depuis ce téléphone ; ceci **n'a pas été testé physiquement**.

### Anomalie réelle A — quatre ressources absentes de la version assemblée

- **Constat :** `index.html` référençait `css/theme-entry.css`, `js/theme-entry.js` et `js/theme-rubrics.js`, mais `build_pages_site.py` ne les incluait pas dans `_site/`. De plus, `js/theme-rubrics.js` demande `data/thematic-index/theme-rubrics-public.json`, lui aussi absent.
- **Cause :** liste des ressources publiques incomplète, sans perte des fichiers dans le dépôt.
- **Correction :** ajout **uniquement de ces quatre ressources déjà destinées au public** dans l'allowlist ; aucune ressource historique privée ajoutée.
- **Preuve :** vérification de chaque `script src`, CSS et JSON de rubrique réellement servi : **PASS** ; **aucune réponse HTTP locale en erreur** pendant les parcours Chromium ; panneau d'identité thématique visible et index ouvrable/fermable. Le contrôle explicite de `data/notes/**` reste négatif.

### Anomalie réelle B — notes authentifiées lisibles mais pas consultables en aller-retour depuis le psaume

- **Constat :** le psaume affichait intégralement la seule note validée, mais ne proposait aucun bouton pour l'ouvrir dans sa propre fiche puis revenir au psaume.
- **Cause :** composant `verifiedNotesBlock()` sans commande de navigation.
- **Correction :** bouton **« Consulter cette note authentifiée »** dans le seul composant réservé aux notes humaines validées et publiées ; il réutilise la pile de lecture de 070, sans changer les règles de validation ni exposer une fiche supplémentaire.
- **Preuve :** recherche `105` → `book-17-psalm-105` → `book-17-psalm-105-note-001` authentifiée → retour au même psaume → prière associée → retour → résultats : **PASS** dans les trois résolutions.

### Clarification fonctionnelle C — surlignage littéral et non qualification d'un sens

- **Constat :** la recherche exacte marque les occurrences de `bien` ou `biens` mais **ne comporte pas de sélection de sens opérationnelle** dans cette version (`state.semanticTargetsByForm` n'est pas alimentée). Le surlignage est donc **textuel**, et ne peut pas être interprété comme une attribution du sens « bien évaluatif », « avantage », ou « possession ».
- **Correction :** ajout d'un avertissement lisible en résultats par mots : **« Surlignage des mots uniquement : il ne valide pas leur sens dans le contexte. »**
- **Preuve :** recherche `bien` et `biens`, contrôle de cet avertissement, contrôle des textes réellement mis en évidence dans le dialogue et de l'absence d'une étiquette de sens inventée : **PASS de sécurité d'affichage**. **Aucune classification ni index sémantique modifié.** Une future recherche filtrée par sens et un marquage par occurrence restent **hors périmètre, non certifiés**.

## 2. Prières multiples — cause documentée

Analyse exhaustive des **métadonnées JSON déjà présentes**, sans rouvrir aucun PDF : `python scripts/check_reader_links_071.py`, **PASS**.

- **1 158 psaumes**, **677 prières** et **11 notes** dans le navigateur ; les **677 identifiants de prières** du catalogue source correspondent exactement aux **677** du bundle public : **aucun oubli à la construction du catalogue**.
- Distribution brute des `prayerIds` sur les psaumes : **481 psaumes avec zéro**, **676 avec un**, **1 avec deux**. En revanche, les **677 prières elles-mêmes ne déclarent jamais le même psaume source deux fois** : **zéro groupe source contenant deux prières réellement rattachées** et **zéro paire de rattachements doubles réciproques**.
- Un cas précis explique le psaume à deux identifiants : `book-35-psalm-214` contient `raphael-book-35-prayer-103` (**rattachement réciproque valide**) et `raphael-book-35-prayer-104` (**lien avant supplémentaire incorrect**). Le fichier de la prière 104 déclare expressément **`book-35-psalm-215`**, dont `prayerIds` contient bien 104. Ce rattachement conflictuel est **une anomalie de métadonnées historiques**, **pas une deuxième prière du psaume 214**.
- **Aucun rattachement n'a été inventé ni réattribué** : modifier les relations historiques sur la seule base de ce constat, sans décision éditoriale, dépasserait cette mission. Le lecteur n'affiche déjà que les liens **réciproques**, donc le lien parasite n'est pas une erreur d'affichage publique. **Il reste une réserve documentaire à corriger lors d'une validation éditoriale ciblée** ; il ne bloque pas le lecteur actuel.

## 3. Résultats utilisateurs testés

CI : [BIBLAW 071 — validation complète et ZIP privé — run 41440453540](https://github.com/ludodulac/Biblaw/actions/runs/41440453540) — **SUCCESS** sur le correctif `d9fa8b25fdbc786af42e4ce9e5623a59ff496de5`.

| Scénario vérifié par de vrais clics Playwright | Chromium 1280 | Chromium 390 tactile émulé | Chromium 320 tactile émulé |
|---|---|---|---|
| Recherche thématique `sainte assemblée` : **3 psaumes**, cartes canoniques, identité du thème, index ouvrable/fermable | PASS | PASS | PASS |
| Recherche littérale `lumière` : **1 048 psaumes**, **mêmes IDs dans la recherche et le catalogue**, compteur cohérent, marques sur le texte source, changements de recherches | PASS | PASS | PASS |
| `bien`, `biens` : marques littérales correctes et avertissement explicite d'absence de qualification sémantique | PASS | PASS | PASS |
| Filtres de **type de texte** : psaumes / prières / notes ; test exact `Nom de la Mère` donnant **deux notes historiques**, fiche non authentifiée correctement avertie | PASS | PASS | PASS |
| Filtre par archange : résultats du psaume 105 limités à **Michaël**, puis à **Gabriel** | PASS | PASS | PASS |
| Recherche → psaume → **note authentifiée** → retour → prière → retour → mêmes résultats et focus | PASS | PASS | PASS |
| Consultation directe de la prière **24/36**, corps intégral **1 968 caractères**, aller-retour au psaume source | PASS | PASS | PASS |
| Psaume long, **90 versets**, vrai défilement, numéros exacts, pas de débordement horizontal, fermeture accessible | PASS | PASS | PASS |
| Chargement de tous les fichiers locaux référencés, aucune erreur JS, aucune demande des notes privées `data/notes/**` | PASS | PASS | PASS |
| **Clavier** : Entrée (résultat et note), retour, Échap, restauration du focus | PASS | Non testé | Non testé |

Les vérifications ont servi le **contenu réel de la prévisualisation** et utilisé les trois tailles d'écran demandées. **Aucun test sur téléphone physique n'a été effectué.** Les tests des notes de 069 restent respectés : **1 note humainement validée ; 10 historiques sans validation humaine identifiables ; 0 nouvelle note publiée**.

## 4. Décision de publication

**A. Bloquants réels : aucun identifié dans les parcours et ressources testés après correction.** La prévisualisation fonctionnelle est prête **à être soumise à l'approbation de Ludo**, mais cette approbation n'a pas été donnée.

**B. Réserves non bloquantes :** lien `prayer-104` erroné supplémentaire dans les métadonnées du psaume `book-35-psalm-214` (ignoré par le lecteur réciproque) ; absence d'essai sur téléphone physique ; absence de deux prières réellement reliées à un même psaume dans les données actuelles ; pas de recherche sémantique par sens actuellement certifiée. Les dix notes historiques non authentifiées restent accessibles avec avertissements conformément à 069.

**C. Améliorations futures :** validation éditoriale de la relation parasite, véritable filtrage des occurrences par sens, retours utilisateur après essai de la prévisualisation.

**Périmètre de code modifié :** `scripts/build_pages_site.py`, `js/biblaw.js`, `scripts/check_reader_links_071.py`, `scripts/smoke_user_071.mjs`, `.github/workflows/verify-user-071.yml`, plus ce compte rendu. **Aucun changement** à `data/catalog.json`, `data/browser-search-catalog.json`, `data/corpus/**`, `data/prayers/**`, `data/notes/**`, aux identifiants, statuts, 29 cas compatibles ou 18 groupes du résolveur. Pas d'audit PDF, **PR #72 toujours DRAFT**, aucun merge ni déploiement.

**STOP.**
