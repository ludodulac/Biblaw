# 2026-09-04 — Passage à l’indexation thématique

## Décision

Le corpus structuré n’est pas encore un index thématique. À partir de maintenant, chaque texte traité doit être suivi d’une indexation éditoriale.

L’objectif est de construire progressivement un index de tous les thèmes réellement présents dans la Bible essénienne. Chaque thème possède son propre fichier dans `data/themes/` et s’enrichit à mesure que de nouveaux psaumes, prières, notes et autres textes sont intégrés.

## Méthode

Pour chaque texte :

- identifier les thèmes réellement enseignés ;
- distinguer thème principal, sous-thèmes et nuances de sens ;
- relier chaque entrée à des passages précis (recordId, versets, pages lorsque disponibles) ;
- réutiliser un thème existant plutôt que créer un doublon ;
- créer un nouveau thème lorsqu’un concept distinct apparaît ;
- conserver la différence entre simple occurrence lexicale et véritable pertinence thématique ;
- consigner uniquement les ambiguïtés éditoriales réelles dans `data/incoherences.json`.

## Première tranche

La première tranche thématique est Michaël, psaumes 105 à 130, déjà structurée. L’indexation commence par le psaume 105 et sa prière associée.

Le psaume 105 met notamment en évidence des ensembles doctrinaux robustes : Lumière, renaissance, monde divin, mensonge et illusion, dévotion, non-savoir, intelligence supérieure. La prière associée renforce plusieurs de ces axes et ajoute des relations au Père, à l’âme, à la filiation et à la libération de l’illusion.

## Travail réalisé sur le psaume 105

Les premiers index éditoriaux généraux ont été créés et enregistrés dans le catalogue :

- `data/themes/lumiere.json`
- `data/themes/renaissance.json`
- `data/themes/monde-divin.json`
- `data/themes/mensonge-et-illusion.json`
- `data/themes/devotion.json`
- `data/themes/non-savoir.json`
- `data/themes/intelligence-superieure.json`

Chaque fichier contient des sens, sous-thèmes et preuves reliées au psaume 105 et, lorsqu’elle apporte un enseignement pertinent, à sa prière associée. Ces thèmes devront être enrichis plutôt que recréés lorsque les psaumes suivants les abordent à nouveau.

Le thème `Chouette` reste le pilote historique antérieur à cette phase générale.

## État d’avancement de la tranche

- Psaume 105 : structure validée et première indexation thématique réalisée.
- Psaumes 106 à 130 : structure disponible ; indexation thématique à poursuivre séquentiellement.

## Suite

Une fois 105–130 thématiquement indexés, le bouton `Index` de l’interface devra afficher uniquement ces thèmes éditorialement constitués. Ensuite chaque nouvelle tranche suivra le cycle : extraction → validation → indexation thématique → enrichissement de l’index général.