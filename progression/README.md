# Progression de Biblaw

Ce dossier est l’archive permanente de l’avancement du projet.

## Règle de travail

Chaque tranche du corpus suit désormais le même cycle :

1. **Extraction fidèle** depuis le PDF : psaumes, versets, prières, notes, pages, locuteurs et dialogues.
2. **Validation structurelle** : cohérence des numéros, pagination, rattachements, locuteurs et relations documentaires.
3. **Indexation thématique éditoriale** : lecture du texte, création ou enrichissement de thèmes existants, sous-thèmes, sens et références précises vers les passages.
4. **Consolidation transversale périodique** : fusion de doublons, synonymes, hiérarchies, relations entre thèmes et préparation des données destinées au moteur de recherche sémantique.

Un thème n’est pas recréé à chaque texte : s’il existe déjà, les nouvelles références et nuances sont ajoutées à son index. Un nouveau thème est créé seulement lorsqu’il apporte un concept distinct.

Les erreurs techniques déterministes doivent être corrigées dans les scripts ou les données. Les ambiguïtés éditoriales réelles sont consignées dans `data/incoherences.json`.

## État de référence

- Michaël, livre 17, psaumes 105 à 130 : corpus extrait et structuré.
- Psaume 105 : validation humaine de référence.
- Psaumes 106 à 130 : validation automatique structurelle.
- Indexation thématique générale : commencée à partir du psaume 105.
- Le thème `Chouette` reste le pilote historique d’un thème structuré avec sens, sous-thèmes et preuves.

Les fichiers datés de ce dossier décrivent les décisions de méthode et l’état d’avancement concret.