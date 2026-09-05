# Extension thématique des livres 27 à 44

Date : 2026-09-06

## Source et règle d'analyse

La seule source documentaire et doctrinale autorisée reste `Bible essénienne (classée par livres).pdf` et les données structurées qui en sont extraites dans le dépôt.

Aucun site internet, commentaire externe, autre édition, résumé, vidéo, podcast ou connaissance doctrinale extérieure ne doit confirmer, compléter ou corriger l'analyse. L'analyse thématique décrit aussi neutralement que possible ce que les textes présentent, associent, distinguent, prescrivent ou mettent en garde. Une inférence est admise uniquement lorsqu'elle repose sur le texte ; une ambiguïté réellement irréductible dans le PDF doit être inscrite dans `data/incoherences.json`.

Les prières restent liées aux psaumes mais ne sont pas utilisées comme matériau primaire de l'index thématique.

## Extension documentaire

Le pipeline documentaire a été prolongé au-delà des livres 21-30 :

- extraction et validation des livres 31-40 ;
- préparation de l'extraction finale des livres 41-44 ;
- génération de source packs thématiques après normalisation ;
- conservation séparée des anomalies techniques afin qu'elles ne contaminent pas l'index sémantique.

Un résumé compact de `data/pilot/book-inventory.json` est désormais généré dans `data/pilot/book-inventory-summary.json`. Il établit, uniquement à partir du PDF, que cette édition contient 44 livres numérotés de 1 à 44. Les quatre derniers sont :

- 41 — `La responsabilité d’un parent` ;
- 42 — `L’état ultime de la paix` ;
- 43 — `La guérison par les vertus` ;
- 44 — `L’énergie de l’argent`.

## Index thématique

Le pipeline canonique a été étendu aux livres 27-30 puis 31-40. Chaque relation thématique conserve ses versets d'appui et le contexte du livre reste une couche secondaire : il peut aider au classement et à l'explication, mais il ne peut pas fabriquer un thème absent du passage.

Au dernier état validé avant l'intégration des quatre livres finaux, `data/thematic-index/validation-report.json` comptait 40 livres, 1 047 analyses de psaumes et 8 427 relations thématiques, sans erreur ni avertissement structurel.

Les passes automatiques à grande échelle constituent une base canonique et reproductible. Elles devront être suivies d'une passe sémantique plus profonde livre par livre afin d'identifier aussi les thèmes réellement enseignés sans occurrence lexicale directe, de préciser les lois/principes, les relations entre thèmes et l'importance relative des psaumes.

## Anomalies documentaires déterministes à réparer

Les rapports d'extraction ont isolé plusieurs psaumes dont le titre est visible dans le PDF mais dont la séparation n'a pas été reconstruite correctement par l'extracteur :

- livre 23, psaume 128 — `Ne sois pas un rêveur` ;
- livre 26, psaume 186 — `Que le désir d’apprendre soit plus grand que vos certitudes` ;
- livre 35, psaume 215 — `La clé magique pour attirer à soi ce que l’on souhaite` ;
- livre 36, psaume 217 — `Es-tu prêt à écouter le point de vue de la Lumière ?` ;
- livre 38, psaume 260 — `Tu n’éduqueras pas des enfants dans l’esclavage`.

Ces cas ne sont pas envoyés à l'utilisateur comme ambiguïtés doctrinales. Un audit dédié (`scripts/audit_missing_psalm_boundaries.py`) extrait leurs voisinages directement du PDF afin de déterminer si une réparation mécanique et sûre est possible. Une véritable ambiguïté ne sera créée dans `data/incoherences.json` que si le PDF lui-même ne permet pas de trancher.

## Suite

1. terminer l'extraction/validation documentaire des livres 41-44 ;
2. produire leurs index thématiques canoniques et reconstruire le répertoire transversal ;
3. réparer les frontières documentaires déterministes identifiées ci-dessus ;
4. consolider les contextes de tous les livres à partir du corpus PDF uniquement ;
5. lancer ensuite la passe sémantique profonde et transversale sur l'ensemble des 44 livres.
