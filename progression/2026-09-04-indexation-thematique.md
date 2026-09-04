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

Pour chaque livre, l’analyse prend en compte le titre du livre, l’Archange, l’ordre des psaumes, les titres de tous les psaumes, les notes éditoriales liées au livre ou aux psaumes, les passages des psaumes eux-mêmes et les relations entre les psaumes à l’échelle du livre.

Les titres sont des **indices de compréhension**, pas des thèmes automatiques. Les notes servent de contexte éditorial et peuvent modifier ou préciser l’interprétation d’un passage.

Les prières restent liées aux psaumes pour l’affichage et l’export mais **ne sont pas indexées thématiquement dans cette phase**.

## Définition d’un thème

Le mot « thème » est pris au sens large : un être, un élément, un objet, un lieu, une pratique, un symbole ou un concept peut constituer un thème s’il porte un enseignement significatif dans le texte.

Exemples : Chouette, Assemblée, Feu, Eau, Pierre, Arbre, Cerf, Mère, Père, Ange, Prière, Temple, Âme, Mort, Lumière, Sagesse, Travail, Nourriture, Alliance, etc.

L’index n’est pas une liste de mots. Une occurrence lexicale isolée ne suffit pas. Un thème est retenu lorsque le passage affirme, définit, distingue, relie, prescrit, interdit ou développe réellement quelque chose à son sujet. Inversement, un passage peut nourrir un thème sans employer son terme exact.

Pour chaque relation thème ↔ psaume, l’analyse conserve au minimum l’importance (`central`, `important`, `related`), le caractère direct ou symbolique, les versets concernés, ce que le passage enseigne, et la référence structurée permettant de retrouver Archange, livre et psaume.

Cette structure permettra de classer les psaumes importants pour un thème, de distinguer les enseignements par Archange et de produire des synthèses transversales sans aplatir leurs différences.

## Chaîne documentaire livres 1–10

Une chaîne automatique extrait et valide les dix premiers livres du PDF source. La numérotation des psaumes est suivie par Archange d’un livre au suivant. Les cas typographiques irréguliers sont traités par règles reproductibles.

Le cas Raphaël 16 (« Le secret de l’aigle ») était absorbé dans la numérotation du psaume précédent dans le PDF extrait. Il a été séparé automatiquement ; les numéros imprimés d’origine 22–29 restent conservés dans `sourceNumber` tandis que les versets du psaume 16 sont normalisés 1–8.

Une seconde règle reproductible traite maintenant les **titres de psaumes coupés sur plusieurs lignes** dans le PDF. Elle a notamment réparé Raphaël 19, désormais correctement intitulé « L’homme doit être conscient de ses associations spirituelles » dans le corpus. La correction est marquée `wrappedTitleNormalized` dans les métadonnées d’extraction.

État documentaire actuel : livres 1–10 extraits, validation structurelle `passed`, aucun trou de psaume, aucun trou de versets selon la structure normalisée, titres et notes conservés, prières exclues des paquets de lecture thématique.

Les paquets de lecture sont produits sous `data/thematic-index/source-packs/`.

## Indexation éditoriale réalisée

### Livre 1 — Michaël — « Trouve ton propre chemin »

Statut : **indexation thématique éditoriale complète de première passe**.

Fichier : `data/thematic-index/books/book-01.json`.

L’axe central du livre relie conscience, orientation de la vie, Lumière, monde divin, Terre/Mère, vertus, responsabilité, préparation, discernement, amour, fidélité, feu et âme.

Les réalités concrètes significatives sont bien traitées comme thèmes lorsqu’elles portent un enseignement : Cerf, Pierre, Arbre, Tortue, Eau, Montagne, Cendre, animaux, corps, cœur, Mère et Père notamment.

### Livre 2 — Gabriel — « Le secret des 3 mondes »

Statut : **indexation thématique éditoriale complète de première passe**.

Fichier : `data/thematic-index/books/book-02.json`.

Axe central : l’homme vit entre plusieurs plans reliés par des échanges. Pour accueillir le divin, il doit purifier l’eau de ses relations, organiser son corps et sa vie, développer une vie intérieure consciente, établir des alliances réelles et incarner concrètement ce qu’il reçoit.

Thèmes structurants : Eau, trois mondes, aura, relations, guérison, alliance, monde divin, cœur, corps, vie intérieure, purification, communauté, engagement, création, âme, amour, générosité, travail sur soi, connaissance de soi, cycles et harmonie.

Particularité forte de Gabriel dans ce livre : l’**eau** devient un modèle transversal de circulation, purification, fécondation, échange et guérison entre êtres et mondes.

### Livre 3 — Raphaël — « Respire avec les Anges »

Statut : **indexation thématique éditoriale complète de première passe**.

Fichier : `data/thematic-index/books/book-03.json`.

Axe central : Raphaël décrit l’homme comme un être respiratoire reliant corps, âme, esprit, nature et mondes invisibles. La respiration consciente, l’air, l’éther, la méditation et l’éveil des organes permettent de transformer la condition mortelle en support d’immortalité et d’unir esprit et matière.

Thèmes structurants : Respiration, Air, Souffle, Âme, Corps, Immortalité, Méditation, Esprit et matière, Anges, Éther, Semence, Bénédiction, Communauté, Nature, Organes, Clarté, Mémoire ancestrale, Légèreté, Papillon et Aigle.

Particularités fortes :

- la **respiration** est un langage et un médiateur entre les mondes ;
- l’**air** est présenté comme être et porteur de messages ;
- le **corps** est un organisme cosmique composé d’organes correspondant à des régions et intelligences plus vastes ;
- l’**Aigle** enseigne calme, hauteur et méditation ;
- le **Papillon** enseigne légèreté, finesse et approche délicate du subtil ;
- la **mémoire ancestrale** est décrite comme inscrite jusque dans les cellules et susceptible d’être guérie et conduite vers la Lumière.

## Travaux antérieurs Michaël 105–130

Les fichiers thématiques produits auparavant pour Michaël 105–130 sont conservés comme **prototype de méthode** et comme matière réutilisable. Ils ne doivent pas être considérés comme l’indexation finale tant que leurs livres respectifs n’ont pas été retraités dans la nouvelle méthode complète : contexte du livre, titres, notes, lecture de tous les psaumes, puis synthèse à l’échelle du livre.

Les prières utilisées dans cette ancienne passe ne doivent plus être prises comme source primaire pour l’indexation thématique actuelle.

## Cible produit confirmée

Le moteur final doit permettre la recherche dans les **Psaumes seulement**, dans les **annexes seulement**, ou dans **Psaumes + annexes** ; classer les psaumes les plus importants pour un thème selon l’analyse éditoriale et non selon la fréquence des mots ; afficher les principes, fonctions, conditions, dangers, relations et différences par Archange ; ouvrir le psaume complet dans une vue de type PDF ; exporter le **psaume seul** ou le **psaume + prière associée**.

Le bouton `Index` devra afficher uniquement les thèmes effectivement constitués par l’analyse éditoriale, pas automatiquement les titres de psaumes ni tous les mots rencontrés.

## Étape suivante

1. Construire un répertoire thématique dérivé à partir des fichiers `data/thematic-index/books/book-*.json`, avec regroupement des occurrences et classement des psaumes par importance.
2. Continuer dans l’ordre canonique/source : livre 4, puis livre 5, etc.
3. Consolider progressivement les thèmes transversaux tout en préservant les différences d’enseignement entre Archanges.
4. Ne faire remonter dans `data/incoherences.json` que les ambiguïtés éditoriales réelles.
