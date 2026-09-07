# PASSATION BIBLAW — nouvelle conversation

> Point d’entrée permanent pour reprendre Biblaw sans casser le travail validé.
> Dernière consolidation : 2026-09-07.

## 1. Mission

Construire Biblaw comme une expertise structurée et interrogeable du corpus de la **Bible essénienne (classée par livres).pdf**, en particulier une indexation thématique riche, précise et navigable dans le site.

Le but n’est pas de produire une interprétation définitive des psaumes. Le travail consiste à **indexer, répertorier et relier** les thèmes, notions, images, entités, oppositions, répétitions et correspondances présents dans le corpus afin de permettre une recherche utile.

## 2. Position d’analyse à respecter absolument

Le propriétaire du projet a explicitement demandé une position neutre et humble :

- ne pas prétendre « comprendre réellement » ou épuiser le sens des psaumes ;
- accepter qu’ils puissent avoir plusieurs niveaux de lecture ;
- ne pas écarter un thème parce qu’il paraît inhabituel, symbolique, métaphysique ou étranger à une culture extérieure ;
- décrire les affirmations du corpus comme des affirmations internes au corpus, pas comme des faits externes vérifiés ;
- distinguer explicite, contextuel, symbolique, indirect, éditorial ;
- relier les psaumes pour la recherche sans transformer une cooccurrence en synonymie, causalité ou vérité doctrinale.

Les formulations recommandées sont documentaires : « le texte présente », « le psaume associe », « ce passage relie », « dans ce psaume… ».

## 3. Source absolue

Pour toute donnée doctrinale, contextuelle, éditoriale ou thématique :

- source autoritative unique : `Bible essénienne (classée par livres).pdf` et les source packs dérivés du PDF ;
- aucune source externe pour enrichir, confirmer ou corriger le contenu sémantique ;
- les prières restent liées aux psaumes mais ne sont pas une source primaire de thèmes ;
- si une ambiguïté de fond reste réellement indécidable à partir du corpus, la documenter dans `data/incoherences.json`.

## 4. État canonique validé

Rapport courant : `data/thematic-index/validation-report.json`.

État validé :

- `status`: `passed`
- **44 livres**
- **1158 analyses de psaumes**
- **10406 relations thématiques**
- **0 erreur**
- **0 avertissement**

Ne jamais recopier ces nombres aveuglément dans une future conversation : relire le rapport courant avant de les citer.

Tous les livres 1–44 ont été amenés à la profondeur canonique `deep-content-grounded`.

## 5. Anomalies documentaires connues et déjà intégrées à la méthode

Cas particuliers à préserver :

1. Livre 15 / Psaume 75 : numérotation source 15–27 ; le Psaume 76 repart ensuite à 1.
2. Livre 23 / Psaume 128 : source imprimée 49–82, canonique 1–34, offset 48 ; question après 22, réponse 23. Toujours renuméroter après extraction brute.
3. Livre 26 / Psaume 186 : source 23–50.
4. Livre 32 / Psaume 182 : source 28–50, restauré depuis le PDF.
5. Livre 35 / Psaume 215 : source 26–46.
6. Livre 36 / Psaume 217 : source 16–36.
7. Livre 38 / Psaume 260 : source 23–54.
8. Livre 44 / Psaume 285 : versets 1–16 seulement ; annexe finale détachée.

Ne pas « réparer » ces cas selon une attente conventionnelle si le PDF montre une autre structure.

## 6. Architecture thématique canonique

Fichiers importants :

- `data/thematic-index/books/book-XX.json` : analyses thématiques canoniques par livre ;
- `data/thematic-index/theme-directory.json` : annuaire transversal généré ; ne pas éditer à la main ;
- `data/thematic-index/theme-search-index.json` : alias de recherche ;
- `data/thematic-index/theme-connections.json` : graphe neutre de cooccurrence dans les psaumes ;
- `data/thematic-index/theme-search-runtime.json` : runtime compact navigateur ;
- `data/thematic-index/SEARCH-CONTRACT.md` : contrat sémantique de la recherche ;
- `data/browser-search-catalog.json` : bundle navigateur unique ;
- `data/incoherences.json` : ambiguïtés nécessitant éventuellement une décision humaine.

Scripts associés :

- `scripts/build_thematic_directory.py`
- `scripts/build_thematic_search_index.py`
- `scripts/validate_thematic_search_index.py`
- `scripts/build_thematic_connections.py`
- `scripts/validate_thematic_connections.py`
- `scripts/build_thematic_search_runtime.py`
- `scripts/build_browser_search_catalog.py`
- `scripts/audit_thematic_search_quality.py`
- `scripts/run_canonical_thematic_pipeline.py`

Toujours modifier le générateur plutôt qu’un fichier généré lorsque cela s’applique.

## 7. Qualité de l’index de recherche

Audit courant :

- 1250 thèmes ;
- 1342 alias normalisés ;
- 9 alias ambigus ;
- `semanticMerging: false` ;
- 13121 arêtes de cooccurrence thème↔thème environ ;
- aucune relation thématique sans versets ni enseignement dans l’audit de qualité validé.

Règles importantes :

- un alias ne vaut pas fusion sémantique ;
- une cooccurrence ne vaut pas synonymie ;
- ne pas fusionner automatiquement les quasi-doublons lexicaux ;
- ne pas supprimer automatiquement les thèmes singleton ;
- les thèmes composites ne sont pas des erreurs par principe ;
- les classements de résultats ne sont pas une hiérarchie de vérité.

## 8. État du site et de la recherche

Site : `https://ludodulac.github.io/Biblaw/`

Fichiers principaux :

- `index.html`
- `css/biblaw.css`
- `js/biblaw.js`
- `.github/workflows/validate-search-ui.yml`

État UI actuellement voulu :

- champ de recherche vide au chargement ;
- plus d’exemple « chouette » prérempli ;
- **Psaumes** coché par défaut ;
- Prières, Notes, Annexes décochés par défaut ;
- filtre Livre supprimé ;
- filtre Archange conservé ;
- mode `Thèmes` + mode `Mots et phrases` ;
- résultats thématiques classés **Central → Important → Lié**, puis ordre déterministe ;
- versets d’appui affichés dans « Passage concerné » ;
- `teaching` utilisé comme repère contextuel sans le présenter comme sens définitif ;
- « Thèmes également présents dans ce psaume » en bas de chaque carte thématique ;
- « Thèmes présents dans ce psaume » à la fin du psaume ouvert ;
- thèmes secondaires cliquables pour navigation transversale ;
- surlignage des mots réellement recherchés dans les extraits et dans le psaume ouvert ;
- le surlignage reste lexical : il ne fabrique pas une occurrence parce qu’un thème a été indexé.

## 9. Normalisation française de requête

La recherche thématique neutralise actuellement les articles initiaux simples :

- `l’assemblée` ↔ `assemblée`
- `la sainte assemblée` ↔ `sainte assemblée`

Articles neutralisés au début : `l`, `le`, `la`, `les`, `un`, `une`, `des`.

Cette souplesse est **uniquement une normalisation de requête**. Ne pas transformer cela en fusion sémantique.

Exemple important :

- `assemblée` et `l’assemblée` peuvent converger ;
- `sainte assemblée` et `la sainte assemblée` peuvent converger ;
- **`assemblée` et `sainte assemblée` ne doivent pas être fusionnés automatiquement.**

## 10. Distinction recherche thématique / recherche textuelle — cas « Dieu »

Dernier problème observé par l’utilisateur : en tapant **« Dieu »** en mode Thèmes, un seul psaume pouvait apparaître, alors que le mot « Dieu » apparaît littéralement dans de nombreux psaumes.

Le comportement a été corrigé côté interface sans modifier artificiellement l’index :

- si une requête correspond à un thème indexé, le mode Thèmes continue d’afficher les psaumes réellement indexés sous ce thème ;
- en parallèle, le moteur compte les occurrences littérales dans les psaumes ;
- si des occurrences textuelles existent, l’interface affiche **« Deux lectures de cette recherche »** et propose **« Voir les occurrences textuelles »** ;
- ce bouton bascule vers `Mots et phrases` sans perdre la requête ;
- un test CI exige désormais que `Dieu` ait plus d’une occurrence textuelle dans les psaumes et que cette route soit exposée.

C’est une décision produit importante : **ne pas élargir automatiquement le thème « Dieu » à tous les psaumes contenant le mot Dieu**. Le thème indexé et l’occurrence lexicale sont deux objets différents.

La prochaine conversation doit vérifier visuellement ce comportement sur le site avant d’aller plus loin.

## 11. État Git / CI au moment de cette passation

HEAD `main` observé :

- commit `ce088d8744d9c0322391232c3aa3e43dec5de35b`
- message : `Validate thematic and textual search distinction`

Workflows associés à ce HEAD :

- `Validate thematic search UI` run `34080396578` : **success** ;
- `Publier Biblaw sur GitHub Pages` run `34080396605` : **success**.

Toujours re-vérifier le HEAD et les workflows au début d’une nouvelle conversation.

## 12. Pipeline canonique et publication

Le pipeline canonique :

- régénère les couches thématiques ;
- génère le runtime compact ;
- génère `data/browser-search-catalog.json` ;
- valide l’ensemble ;
- publie les sorties générées de façon race-safe en cas de commits concurrents.

Le bundle navigateur contient actuellement 1876 enregistrements et évite >1000 requêtes HTTP individuelles au chargement du site.

La publication canonique a déjà été rendue tolérante aux courses de push : ne pas revenir à une publication naïve non-fast-forward.

## 13. Travail éditorial volontairement différé

Ne pas générer maintenant de grand résumé général automatique pour chaque thème.

Décision du propriétaire : les **synthèses thématiques globales** seront une phase éditoriale séparée, lorsque l’index et le corpus seront considérés comme suffisamment stabilisés.

À ce moment-là, chaque synthèse devra :

- examiner toutes les occurrences ;
- tenir compte des versets, contextes, niveaux d’importance et connexions ;
- distinguer les manières différentes dont un même thème apparaît ;
- employer des formulations contextuelles (« dans tels psaumes… », « ailleurs… ») plutôt qu’une définition définitive (« ce thème signifie… »).

## 14. Prochaine séquence recommandée

Priorité immédiate : **audit de recherche réel**, pas nouvelle couche sémantique massive.

1. Ouvrir le site déployé et tester de bout en bout :
   - `Dieu`
   - `alliance`
   - `alliance de lumière`
   - `lumière`
   - `assemblée`
   - `l’assemblée`
   - `sainte assemblée`
   - `la sainte assemblée`
   - `argent`
   - `chouette`
   - `abeille`
   - `22 commandements`
2. Pour chaque requête, vérifier :
   - résolution du bon thème ;
   - distinction thème / occurrences textuelles ;
   - ordre Central → Important → Lié ;
   - versets d’appui ;
   - surlignage ;
   - thèmes secondaires en bas ;
   - navigation vers un autre thème ;
   - ouverture du psaume complet.
3. Corriger uniquement les problèmes techniques ou de présentation déterministes.
4. Si un problème vient de l’index sémantique lui-même, remonter à la relation canonique/source pack et au PDF ; ne pas corriger par une règle UI arbitraire.
5. Après cet audit, décider si la couche recherche est assez stable pour lancer la future phase de synthèses thématiques éditoriales.

## 15. Règle d’autonomie

Quand le propriétaire dit « continue », « vas-y », « fais-le » : avancer réellement.

- ne pas demander validation étape par étape ;
- résoudre les problèmes techniques déterministes automatiquement ;
- corriger les générateurs/pipelines plutôt que les sorties générées ;
- ne demander l’avis humain que pour une vraie ambiguïté éditoriale/sémantique ou une décision produit ;
- si une ambiguïté peut être documentée sans bloquer, utiliser `data/incoherences.json` et continuer.

## 16. Procédure de reprise dans une nouvelle conversation

Ordre conseillé :

1. lire ce fichier ;
2. lire les dernières entrées pertinentes de `progression/` ;
3. lire `data/incoherences.json` ;
4. lire `data/thematic-index/validation-report.json` ;
5. vérifier HEAD `main` et les workflows GitHub récents ;
6. re-fetch tout fichier avant modification et utiliser son SHA courant ;
7. vérifier le site déployé ;
8. reprendre par l’audit des requêtes de la section 14 ;
9. ne jamais utiliser de source externe pour une décision thématique ;
10. écrire toute nouvelle décision méthodologique importante dans `progression/`.

## 17. Principe final

Si cette passation et le dépôt semblent se contredire, **le dépôt courant, les rapports et les générateurs priment**. Ne jamais écraser un état plus récent pour faire correspondre le code à ce document.

Le but de la passation est de permettre à la prochaine conversation de reprendre immédiatement avec les mêmes règles de neutralité, de traçabilité et de prudence, sans perdre les décisions acquises ni casser l’index canonique.
