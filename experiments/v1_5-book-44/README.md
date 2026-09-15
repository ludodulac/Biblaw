# Expérience V1.5 — livre 44

Couche strictement expérimentale. Elle ne remplace ni `data/documentary-extractions/**`, ni `data/thematic-index/**`, ni aucun runtime public.

Source unique de la projection : `data/documentary-extractions/psalms/book-44/psalm-260.json` à `psalm-285.json`.

Le fichier dérivé `subjects.json` est produit par `scripts/experimental_v15_book44.py build`. Il conserve, pour chaque sujet primaire, `recordId`, `psalmNumber`, `localId`, `localSubject`, `verseNumbers`, `evidence`, `documentaryNote` et `sourcePath`. Les champs `search.*` sont uniquement des normalisations techniques dérivées ; ils ne remplacent jamais les formulations primaires.

`consolidation-pilot.json` est le prototype de consolidation contrôlée limité aux six entrées `argent`, `œuvre`, `vie intérieure`, `vertus`, `responsabilité`, `terre`. Ces entrées restent expérimentales : ce ne sont ni des `themeId` globaux ni une ontologie. Chaque famille contient des fonctions locales documentées et seulement des références `(recordId, localId)` vers les sujets primaires. Le script hydrate toujours ces références depuis V1.5 ; aucune copie du `localSubject` ne devient une nouvelle source.

Un même sujet peut appartenir à plusieurs familles lorsque les deux relations sont documentaires. Les sujets non concernés restent volontairement hors du prototype. Aucun rattachement n'est inféré automatiquement par présence lexicale.

`relation-nature-audit.json` audite uniquement les 65 rattachements déjà présents dans C. Il ne crée aucun rattachement. Pour chaque triplet `(family, recordId, localId)`, il enregistre la nature expérimentale du lien : `DIRECT` lorsque la famille appartient à l'identité documentaire propre du sujet, `FONCTIONNEL` lorsque le sujet porte principalement une autre matière qui agit explicitement sur, envers ou à travers la famille, et `RESIDUEL` uniquement si l'hypothèse binaire ne suffit pas. Cette qualification est un axe distinct des fonctions documentaires déjà présentes dans `consolidation-pilot.json`.

Commandes :

```bash
python scripts/experimental_v15_book44.py build
python scripts/experimental_v15_book44.py check
python scripts/experimental_v15_book44.py search "vie intérieure"
python scripts/experimental_v15_book44.py consolidated "vie intérieure"
python scripts/experimental_v15_book44.py consolidation-stats
python scripts/experimental_v15_book44.py compare

python scripts/experimental_v15_book44_relation_audit.py check
python scripts/experimental_v15_book44_relation_audit.py stats
python scripts/experimental_v15_book44_relation_audit.py show "vie intérieure"
python scripts/experimental_v15_book44_relation_audit.py compare
```

`build` est déterministe : ordre des psaumes puis ordre source des sujets, JSON sérialisé avec clés stables et sans horodatage. Le contrôle historique vérifie la projection primaire et le prototype C.

Le contrôle de l'audit vérifie en plus : exactement les six familles, exactement les 65 rattachements existants et uniques, égalité exacte entre les rattachements de C et ceux qualifiés par l'audit, existence de chaque référence primaire, qualification reconnue `DIRECT`, `FONCTIONNEL` ou `RESIDUEL`, maintien observable des rattachements multiples et statistiques par famille.

`search` est la représentation B : recherche lexicale explicable sur `localSubject`, `documentaryNote` et les citations d'`evidence`.

`consolidated` est la représentation C historique : entrée transverse exacte vers une famille, puis fonctions documentaires distinctes, puis sujets primaires hydratés.

`show` est la représentation C auditée : entrée transverse → nature du rattachement → fonction documentaire → sujet primaire hydraté avec psaumes, versets, preuves et provenance. Elle permet de séparer les matières directement consacrées à la notion des matières qui entretiennent avec elle une relation fonctionnelle substantielle.

Le `compare` du script d'audit produit côte à côte les six requêtes selon A = index thématique actuel, B = recherche lexicale V1.5 primaire, C = consolidation contrôlée qualifiée par nature de relation. Aucun mécanisme n'est branché au moteur public.
