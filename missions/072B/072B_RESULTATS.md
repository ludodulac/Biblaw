# 🌸 BIBLAW — MISSION 072B — RÉSULTATS

**Référence vérifiée avant intervention :** `30f13ffd3f9106aeb49d1ae8bf5903bd15dc3a95` · **Branche :** `feat/052-search-ui` · **PR #72 :** DRAFT, non fusionnée · **Correctif testé :** `10ac7c810eb717afe93a2c26e0327a5e5d17708d`.

## 1. Notes examinées et méthode

**288 notes historiques réelles lues**, par **29 lots de dix** (dernier lot : huit) : **282 notes de `data/notes/books/` et 6 notes historiques d'alias `michael-psalm-...`**. Les 11 notes déjà incluses au navigateur ont été recoupées par leur fichier publié et ne sont pas comptées deux fois. Aucun PDF n'a été ré-audité.

L'analyse est fondée sur le **texte ou le résumé réel des fichiers JSON**, non sur les titres de psaumes voisins. Le premier lot de dix avait déjà été **classé manuellement et justifié** dans `missions/072/NOTES_THEMES_LOT_001.md`, que le générateur réutilise. Les **278 autres notes** ont reçu des **propositions thématiques automatiques, justifiées par des expressions présentes dans leur contenu**, à confirmer éditorialement. Ne pas confondre cette couverture technique avec 288 validations humaines. Une note peut avoir jusqu'à quatre thèmes ; un thème peut renvoyer à plusieurs notes. Une proposition n'authentifie jamais le contenu.

**Correspondances et preuves :** `scripts/build_note_themes_072B.py` relit les notes **dix par dix** et régénère `data/note-themes-working-072B.json` (index historique privé, IDs, thèmes, indices textuels, source, statut, lot, incertitudes) et `data/note-themes-public-072B.json` (uniquement des IDs appartenant aux onze notes déjà publiques). Le fichier historique est volontairement **non diffusé et non commité**, mais son générateur demeure dans GitHub ; il est également fourni temporairement comme artefact GitHub Actions.

## 2. Thèmes identifiés et effectifs

**43 thèmes proposés au total**, dont **13 thèmes disponibles dans le navigateur** pour les **11 notes précédemment publiques**. Les comptes se recouvrent volontairement, une note ayant plusieurs thèmes. « Publiques » n'implique **aucune validation humaine**.

| Thème | Notes historiques associées | Notes déjà publiques |
|---|---:|---:|
| Alliance avec le monde divin | 27 | 1 |
| Archanges et anges | 4 | 0 |
| Bénédiction et lumière | 36 | 0 |
| Célébrations archangéliques | 65 | 2 |
| Commandements et lois | 6 | 0 |
| Consécration des lieux | 5 | 0 |
| Corps et âme | 19 | 0 |
| Dates et événements historiques | 49 | 6 |
| Eau sacrée | 18 | 0 |
| Éducation et discipline | 2 | 0 |
| Enseignements des archanges | 30 | 0 |
| Famille et filiation | 4 | 0 |
| Feu et flammes | 20 | 4 |
| Gouvernement et organisation | 2 | 0 |
| Guérison et soins | 4 | 0 |
| Histoire des Esséniens | 7 | 0 |
| Huile d’Ouriel | 1 | 0 |
| Lieux et géographie | 16 | 1 |
| Méditation et prière | 19 | 1 |
| Monde invisible | 2 | 0 |
| Montagnes sacrées | 10 | 0 |
| Mort et passage | 1 | 0 |
| Nation essénienne | 31 | 0 |
| Nature et règnes | 6 | 1 |
| Offrandes et dons | 2 | 0 |
| Olivier Manitara | 44 | 3 |
| Paroles et adresses | 33 | 2 |
| Pierres sacrées | 16 | 0 |
| Pratiques de la vie intérieure | 9 | 0 |
| Prêtrise et initiation | 14 | 1 |
| Pyramides de pierres | 7 | 0 |
| Références aux évangiles | 29 | 0 |
| Références aux psaumes | 31 | 2 |
| Religions et traditions | 8 | 0 |
| Rituels et cultes | 15 | 0 |
| Ronde des Archanges | 36 | 1 |
| Statues sacrées | 9 | 0 |
| Symboles et nombres sacrés | 16 | 0 |
| Temples esséniens | 32 | 0 |
| Terre et humanité | 19 | 1 |
| Textes sacrés | 7 | 0 |
| Vie quotidienne essénienne | 2 | 0 |
| Villages esséniens | 21 | 0 |

**20 notes dont le classement n'est pas suffisamment justifié à ce stade :**

`book-07-psalm-032-note-001` · `book-07-psalm-039-note-001` · `book-07-psalm-047-note-001` · `book-09-psalm-070-note-001` · `book-10-psalm-057-note-001` · `book-13-psalm-081-note-001` · `book-14-psalm-099-note-002` · `book-15-psalm-077-note-001` · `book-18-psalm-127-note-001` · `book-19-psalm-113-note-001` · `book-20-psalm-124-note-002` · `book-21-psalm-150-note-001` · `book-21-psalm-150-note-002` · `book-21-psalm-162-note-001` · `book-21-psalm-163-note-001` · `book-23-psalm-146-note-001` · `book-29-psalm-212-note-001` · `book-31-psalm-190-note-001` · `book-31-psalm-203-note-001` · `book-32-psalm-197-note-002`

Aucune catégorie n'a été inventée pour ces 20 fiches ; elles demeurent dans les données historiques. Les 268 autres associations de thèmes (dont le premier lot) ne doivent pas être traitées comme un contrôle humain intégral.

## 3. Interface modifiée

- Zone des cases **Psaumes / Prières / Notes** conservée ; à droite de **Notes : « Ouvrir ▾ »**.
- Ouverture de « Notes » : sous les cases, liste **alphabétique française des thèmes**, champ de **recherche d'un thème**, filtres de thèmes et option **« Toutes les notes »**.
- Clic sur un thème : liste des **notes déjà accessibles** de ce thème ; clic sur une note : lecture de son texte et **avertissement d'authentification existant** ; même note retrouvable sous plusieurs thèmes.
- La recherche par mot ou expression avec la case **Notes** est **indépendante** du classement thématique et continue à fonctionner : `Nom de la Mère` → **deux notes publiques**.
- Les thèmes des notes sont un index **distinct** des thèmes des psaumes.
- L'allowlist du site contient seulement `data/note-themes-public-072B.json`, généré à la construction ; **aucune note historique privée ni fichier de travail ne part dans le site**.

## 4. Tests et preuves

**Workflow** [BIBLAW 072B — GitHub Actions 41516258844](https://github.com/ludodulac/Biblaw/actions/runs/41516258844) : **SUCCESS** sur `10ac7c810eb717afe93a2c26e0327a5e5d17708d`.

**Python : PASS** — 288 IDs uniques, 29 lots, 43 thèmes, 20 incertains, onze IDs publics strictement contrôlés et aucun ajout au catalogue. **Chromium : PASS à 1280, 390 et 320 px**, interactions simulées sur ordinateur/mobile : menu ouvert/fermé, tri, filtre, thème avec deux notes, note rattachée à quatre thèmes, lecture et avertissements, recherche dans les notes et retour aux psaumes. **Zéro appel au répertoire privé `data/notes/**`**. Tests tactiles simulés, **pas de téléphone physique**.

Artefacts privés, disponibles **7 jours** dans GitHub Actions :
- [Prévisualisation testée de BIBLAW](https://github.com/ludodulac/Biblaw/actions/runs/41516258844/artifacts/13175437928)
- [Index de travail des 288 notes, avec thèmes et indices](https://github.com/ludodulac/Biblaw/actions/runs/41516258844/artifacts/13173379966)

Pour tester la prévisualisation : extraire l'archive, exécuter `python -m http.server 4173` dans le dossier contenant `index.html`, puis ouvrir `http://localhost:4173/index.html`. `file://` ne convient pas car le navigateur doit charger des fichiers JSON.

## 5. Fichiers modifiés et limitations

`js/biblaw.js`, `index.html`, `css/biblaw.css`, `scripts/build_note_themes_072B.py`, `scripts/build_pages_site.py`, `scripts/smoke_notes_072B.mjs`, `.github/workflows/verify-notes-072B.yml`, et ce rapport. **Aucun texte de psaume, de prière ou de note, aucun identifiant historique, aucune validation et aucune autorisation de publication modifiés**.

**Réserve de qualité documentaire :** 278 propositions lexicales à revoir humainement, dont 20 dossiers sans thème suffisant. L'index thématique n'est pas une authentification. **PR #72 DRAFT ; aucune fusion ni aucun déploiement. STOP.**
