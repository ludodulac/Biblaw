# 2026-09-04 — Passage à l’indexation thématique

## Décision

Le corpus structuré n’est pas encore un index thématique. À partir de maintenant, chaque texte traité doit être suivi d’une indexation éditoriale.

L’objectif est de construire progressivement un index de tous les thèmes réellement présents dans la Bible essénienne. Chaque thème possède son propre fichier dans `data/themes/` et s’enrichit à mesure que de nouveaux psaumes, prières, notes et autres textes sont intégrés.

## Méthode

Pour chaque texte : identifier les thèmes réellement enseignés ; distinguer thème principal, sous-thèmes et nuances de sens ; relier chaque entrée à des passages précis ; réutiliser un thème existant plutôt que créer un doublon ; créer un nouveau thème lorsqu’un concept distinct apparaît ; distinguer occurrence lexicale et pertinence thématique ; consigner uniquement les ambiguïtés éditoriales réelles dans `data/incoherences.json`.

## Première tranche

La première tranche thématique est Michaël, psaumes 105 à 130, déjà structurée. Chaque psaume est traité avec sa prière associée lorsque celle-ci enrichit réellement les thèmes.

## Psaume 105 — réalisé

Création des premiers index généraux : Lumière, Renaissance, Monde divin, Mensonge et illusion, Dévotion, Non-savoir, Intelligence supérieure. Le thème Chouette reste le pilote historique antérieur.

## Psaume 106 — réalisé

Texte : « Comment discerner le vrai du faux », pages 1074–1075. Prière 2 : pages 1075–1076.

Thèmes existants enrichis :
- `Lumière` : ajout de la distinction entre Lumière vécue et revendication de servir la Lumière ; la prière ajoute la Lumière comme tradition vivante et force d’éclairement.
- `Mensonge et illusion` : ajout des faux guides, intelligences trompeuses, illusionnistes eux-mêmes illusionnés, faux moi et distinction entre être et paraître.

Nouveaux index créés :
- `Discernement` : ne pas suivre aveuglément, reconnaître l’être authentique, critères du vrai et du faux.
- `Authenticité et vérité` : connaissance de soi dans la vérité, accord entre être et parole, vérité reconnue à son résultat.
- `Connaissance de soi` : observation, redressement et sortie des faux moi.
- `Âme` : langage pur de l’âme, parole qui nourrit l’âme et âme vivante participant à la vie.

Le psaume 106 montre la règle d’enrichissement : lorsqu’un thème du psaume 105 réapparaît, son fichier est complété au lieu d’être dupliqué.

## État d’avancement

- Psaume 105 + prière 1 : indexés.
- Psaume 106 + prière 2 : indexés.
- Psaumes 107 à 130 : structurés, à indexer séquentiellement.

## Suite

Poursuivre avec le psaume 107 et sa prière. À la fin de 105–130, revoir transversalement les thèmes pour fusionner les synonymes éventuels, préciser les hiérarchies et préparer le traitement destiné au moteur de recherche sémantique. Le bouton `Index` doit afficher les thèmes éditorialement constitués, pas une liste automatique de mots.