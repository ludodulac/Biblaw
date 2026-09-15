# Expérience V1.5 — livre 44

Couche strictement expérimentale. Elle ne remplace ni `data/documentary-extractions/**`, ni `data/thematic-index/**`, ni aucun runtime public.

Source unique : `data/documentary-extractions/psalms/book-44/psalm-260.json` à `psalm-285.json`.

Le fichier dérivé `subjects.json` est produit par `scripts/experimental_v15_book44.py build`. Il conserve, pour chaque sujet primaire, `recordId`, `psalmNumber`, `localId`, `localSubject`, `verseNumbers`, `evidence`, `documentaryNote` et `sourcePath`. Les champs `search.*` sont uniquement des normalisations techniques dérivées ; ils ne remplacent jamais les formulations primaires.

Commandes :

```bash
python scripts/experimental_v15_book44.py build
python scripts/experimental_v15_book44.py check
python scripts/experimental_v15_book44.py search "vie intérieure"
python scripts/experimental_v15_book44.py compare
```

`build` est déterministe : ordre des psaumes puis ordre source des sujets, JSON sérialisé avec clés stables et sans horodatage. `check` reconstruit en mémoire et vérifie 26 psaumes, l'unicité `(recordId, localId)`, la traçabilité, et l'égalité exacte du nombre de sujets entre sources et projection.

`search` effectue une recherche lexicale explicable sur `localSubject`, `documentaryNote` et les citations d'`evidence`. Aucun regroupement, alias éditorial ou `themeId` V1.5 n'est créé.

`compare` exécute les requêtes de `comparative-queries.json` sur la projection V1.5 et, séparément, sur `data/thematic-index/books/book-44.json`. Cette comparaison est expérimentale et ne modifie aucun moteur public.