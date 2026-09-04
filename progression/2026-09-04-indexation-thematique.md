# 2026-09-04 — Reprise de l’indexation thématique livre par livre

## Décision méthodologique actuelle

L’indexation thématique repart méthodologiquement de zéro, **livre par livre**, sans supprimer le corpus documentaire déjà extrait et validé. Les travaux thématiques antérieurs sur Michaël 105–130 sont conservés comme prototype exploratoire, mais ne constituent plus la référence finale de méthode.

Le corpus structuré et l’expertise thématique sont deux couches distinctes :

- `data/corpus/` contient les textes documentaires structurés ;
- `data/thematic-index/` contient l’analyse éditoriale directement exploitable par le logiciel ;
- `progression/` documente la méthode et l’avancement ;
- `data/incoherences.json` reste le registre permanent des ambiguïtés éditoriales réelles nécessitant une décision humaine.

Les erreurs techniques déterministes doivent être corrigées automatiquement dans les scripts et ne doivent pas être transformées en demandes de validation humaine.

## Unité de travail : le livre entier

Pour chaque livre, l’analyse prend en compte :

1. le titre du livre ;
2. l’Archange ;
3. l’ordre des psaumes ;
4. les titres de tous les psaumes ;
5. les notes éditoriales liées au livre ou aux psaumes ;
6. les passages des psaumes eux-mêmes ;
7. les relations entre les psaumes à l’échelle du livre.

Les titres sont des **indices de compréhension**, pas des thèmes automatiques. Les notes servent de contexte éditorial et peuvent modifier ou préciser l’interprétation d’un passage.

Les prières restent liées aux psaumes pour l’affichage et l’export mais **ne sont pas indexées thématiquement dans cette phase**.

## Définition d’un thème

Le mot « thème » est pris au sens large : un être, un élément, un objet, un lieu, une pratique, un symbole ou un concept peut constituer un thème s’il porte un enseignement significatif dans le texte.

Exemples : Chouette, Assemblée, Feu, Eau, Pierre, Arbre, Cerf, Mère, Père, Ange, Prière, Temple, Âme, Mort, Lumière, Sagesse, Travail, Nourriture, Alliance, etc.

L’index n’est pas une liste de mots. Une occurrence lexicale isolée ne suffit pas. Un thème est retenu lorsque le passage affirme, définit, distingue, relie, prescrit, interdit ou développe réellement quelque chose à son sujet. Inversement, un passage peut nourrir un thème sans employer son terme exact.

Pour chaque relation thème ↔ psaume, l’analyse conserve au minimum :

- l’importance (`central`, `important`, `related`) ;
- le caractère direct ou symbolique ;
- les versets concernés ;
- ce que le passage enseigne ;
- l’Archange, le livre et le psaume par la référence structurée.

Cette structure permettra ensuite de classer les psaumes importants pour un thème, de distinguer les enseignements par Archange et de produire des synthèses transversales sans aplatir leurs différences.

## Chaîne documentaire livres 1–10

Une chaîne automatique a été mise en place pour extraire et valider les dix premiers livres du PDF source. La numérotation des psaumes est suivie par Archange d’un livre au suivant. Les cas typographiques irréguliers sont traités par règles reproductibles.

Le cas Raphaël 16 (« Le secret de l’aigle ») était absorbé dans la numérotation du psaume précédent dans le PDF extrait. Il a été séparé automatiquement ; les numéros imprimés d’origine 22–29 restent conservés dans `sourceNumber` tandis que les versets du psaume 16 sont normalisés 1–8.

État documentaire actuel :

- livres 1–10 extraits ;
- validation structurelle : `passed` ;
- aucun trou de psaume ;
- aucun trou de versets selon la structure normalisée ;
- titres et notes conservés ;
- prières exclues des paquets de lecture thématique.

Les paquets de lecture sont produits sous `data/thematic-index/source-packs/`.

## Indexation éditoriale réalisée

### Livre 1 — Michaël — « Trouve ton propre chemin »

Statut : **indexation thématique éditoriale complète de première passe**.

Fichier : `data/thematic-index/books/book-01.json`.

L’axe central du livre relie conscience, orientation de la vie, Lumière, monde divin, Terre/Mère, vertus, responsabilité, préparation, discernement, amour, fidélité, feu et âme.

Les réalités concrètes significatives sont bien traitées comme thèmes lorsqu’elles portent un enseignement : par exemple le Cerf, la Pierre, l’Arbre, la Tortue, l’Eau, la Montagne, la Cendre, les animaux, le corps, le cœur, la Mère et le Père.

### Livre 2 — Gabriel — « Le secret des 3 mondes »

Statut : **indexation thématique éditoriale complète de première passe**.

Fichier : `data/thematic-index/books/book-02.json`.

Axe central : l’homme vit entre plusieurs plans reliés par des échanges. Pour accueillir le divin, il doit purifier l’eau de ses relations, organiser son corps et sa vie, développer une vie intérieure consciente, établir des alliances réelles et incarner concrètement ce qu’il reçoit.

Thèmes structurants : Eau, trois mondes, aura, relations, guérison, alliance, monde divin, cœur, corps, vie intérieure, purification, communauté, engagement, création, âme, amour, générosité, travail sur soi, connaissance de soi, cycles et harmonie.

Particularité forte de Gabriel dans ce livre : l’**eau** devient un modèle transversal de circulation, purification, fécondation, échange et guérison entre êtres et mondes.

## Travaux antérieurs Michaël 105–130

Les fichiers thématiques produits auparavant pour Michaël 105–130 sont conservés comme **prototype de méthode** et comme matière réutilisable. Ils ne doivent pas être considérés comme l’indexation finale tant que leurs livres respectifs n’ont pas été retraités dans la nouvelle méthode complète : contexte du livre, titres, notes, lecture de tous les psaumes, puis synthèse à l’échelle du livre.

Les prières utilisées dans cette ancienne passe ne doivent plus être prises comme source primaire pour l’indexation thématique actuelle.

## Cible produit confirmée

Le moteur final doit permettre :

- recherche dans les **Psaumes seulement** ;
- recherche dans les **annexes seulement** ;
- recherche dans **Psaumes + annexes** ;
- classement des psaumes les plus importants pour un thème selon l’analyse éditoriale, pas selon la fréquence des mots ;
- affichage de l’expertise d’un thème : principes, fonctions, conditions, dangers, relations et différences par Archange ;
- ouverture du psaume complet dans une vue de type PDF ;
- export du **psaume seul** ou du **psaume + prière associée**.

Le bouton `Index` devra afficher uniquement les thèmes effectivement constitués par l’analyse éditoriale, pas automatiquement les titres de psaumes ni tous les mots rencontrés.

## Étape suivante

Continuer dans l’ordre canonique/source : livre 3, puis livre 4, etc. Pour chaque livre : lecture des paquets, analyse de tous les psaumes, synthèse du livre, stockage dans `data/thematic-index/books/`, puis consolidation progressive des thèmes transversaux. Les ambiguïtés réelles seulement doivent remonter dans `data/incoherences.json`.
