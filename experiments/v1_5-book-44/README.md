# Expérience V1.5 — livre 44

Couche strictement expérimentale. Elle ne remplace ni `data/documentary-extractions/**`, ni `data/thematic-index/**`, ni aucun runtime public.

Source unique de la projection : `data/documentary-extractions/psalms/book-44/psalm-260.json` à `psalm-285.json`.

Le fichier dérivé `subjects.json` peut être produit par `scripts/experimental_v15_book44.py build`. Il conserve, pour chaque sujet primaire, la traçabilité V1.5 ; il n'est pas requis par la surface de navigation, qui hydrate directement les 26 sources primaires.

`consolidation-pilot.json` est le prototype de consolidation contrôlée limité aux six entrées `argent`, `œuvre`, `vie intérieure`, `vertus`, `responsabilité`, `terre`. Chaque famille contient des fonctions locales documentées et seulement des références `(recordId, localId)` vers les sujets primaires.

`relation-nature-audit.json` qualifie uniquement les 65 rattachements déjà présents dans C : `DIRECT`, `FONCTIONNEL`, et support de `RESIDUEL`. Cet axe reste distinct des fonctions documentaires.

## Surface de navigation C

`navigation-c.html` est une surface locale, statique et supprimable. Elle ne contient aucune copie manuelle des 65 rattachements. Elle charge :

- `consolidation-pilot.json` pour famille → fonction documentaire → références ;
- `relation-nature-audit.json` pour la nature DIRECT/FONCTIONNEL/RESIDUEL ;
- les 26 fichiers V1.5 primaires pour `localSubject`, versets, evidence, note et provenance ;
- `data/thematic-index/books/book-44.json` uniquement pour le panneau comparatif A/B/C.

Depuis la racine du dépôt :

```bash
python -m http.server 8000
```

puis ouvrir `http://localhost:8000/experiments/v1_5-book-44/navigation-c.html`.

La vue principale impose l'ordre : requête transverse → DIRECT → FONCTIONNEL → fonctions documentaires → sujets primaires → psaumes/versets/preuves/provenance. `RESIDUEL` n'est affiché que s'il contient réellement des rattachements. Le panneau « Comparer A / B / C » conserve A = index thématique, B = recherche lexicale V1.5 et C = consolidation qualifiée, sans ranking ni score ajouté.

Au chargement, la surface refuse de fonctionner si elle ne retrouve pas exactement six familles, 65 rattachements, 46 DIRECT et 19 FONCTIONNEL. Les références C sont ensuite hydratées depuis les sources V1.5 : le texte primaire n'est pas réécrit dans la surface.

## Contrôles en ligne de commande

```bash
python scripts/experimental_v15_book44.py check
python scripts/experimental_v15_book44_relation_audit.py check
python scripts/experimental_v15_book44_relation_audit.py stats
python scripts/experimental_v15_book44_relation_audit.py show "vie intérieure"
python scripts/experimental_v15_book44_relation_audit.py compare
```

Le script d'audit vérifie exactement les six familles, les 65 rattachements uniques, l'égalité exacte entre C et l'audit, l'existence des références primaires, les qualifications reconnues et les rattachements multiples. Aucun mécanisme expérimental n'est branché au moteur public.
