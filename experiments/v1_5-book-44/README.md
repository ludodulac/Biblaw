# Expérience V1.5 — livre 44

Couche strictement expérimentale. Elle ne remplace ni `data/documentary-extractions/**`, ni `data/thematic-index/**`, ni aucun runtime public.

Source unique de la projection : `data/documentary-extractions/psalms/book-44/psalm-260.json` à `psalm-285.json`.

Le fichier dérivé `subjects.json` est produit par `scripts/experimental_v15_book44.py build`. Il conserve, pour chaque sujet primaire, `recordId`, `psalmNumber`, `localId`, `localSubject`, `verseNumbers`, `evidence`, `documentaryNote` et `sourcePath`. Les champs `search.*` sont uniquement des normalisations techniques dérivées ; ils ne remplacent jamais les formulations primaires.

`consolidation-pilot.json` est le prototype de consolidation contrôlée limité aux six entrées `argent`, `œuvre`, `vie intérieure`, `vertus`, `responsabilité`, `terre`. Ces entrées restent expérimentales : ce ne sont ni des `themeId` globaux ni une ontologie. Chaque famille contient des fonctions locales documentées et seulement des références `(recordId, localId)` vers les sujets primaires. Le script hydrate toujours ces références depuis V1.5 ; aucune copie du `localSubject` ne devient une nouvelle source.

Un même sujet peut appartenir à plusieurs familles lorsque les deux relations sont documentaires. Les sujets non concernés restent volontairement hors du prototype. Aucun rattachement n'est inféré automatiquement par présence lexicale.

Commandes :

```bash
python scripts/experimental_v15_book44.py build
python scripts/experimental_v15_book44.py check
python scripts/experimental_v15_book44.py search "vie intérieure"
python scripts/experimental_v15_book44.py consolidated "vie intérieure"
python scripts/experimental_v15_book44.py consolidation-stats
python scripts/experimental_v15_book44.py compare
```

`build` est déterministe : ordre des psaumes puis ordre source des sujets, JSON sérialisé avec clés stables et sans horodatage. `check` reconstruit en mémoire et vérifie 26 psaumes, l'unicité `(recordId, localId)`, la traçabilité, l'égalité exacte du nombre de sujets entre sources et projection, l'existence de chaque sujet rattaché et l'ensemble exact des six familles.

`search` est la représentation B : recherche lexicale explicable sur `localSubject`, `documentaryNote` et les citations d'`evidence`.

`consolidated` est la représentation C : entrée transverse exacte vers une famille, puis fonctions documentaires distinctes, puis sujets primaires hydratés avec psaumes, versets, preuves et provenance.

`compare` produit côte à côte les six requêtes de `comparative-queries.json` selon A = index thématique actuel, B = recherche lexicale V1.5 primaire, C = consolidation contrôlée V1.5. Aucun de ces mécanismes ne modifie le moteur public.
