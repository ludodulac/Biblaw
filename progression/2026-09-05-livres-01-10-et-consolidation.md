# Indexation thématique — livres 1 à 10 et première consolidation transversale

Date : 2026-09-05

## Jalon atteint

L’indexation canonique reprise depuis le premier livre couvre maintenant les livres 1 à 10 dans `data/thematic-index/books/`.

Rapport de validation après correction de la concurrence entre workflows :

- 10 livres ;
- 256 psaumes analysés ;
- 838 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

Le fichier de référence est `data/thematic-index/validation-report.json`.

## Méthode appliquée

Le travail est effectué livre par livre et non comme une simple recherche lexicale.

Pour chaque livre :

1. le titre du livre et l’Archange donnent le cadre ;
2. les titres des psaumes sont utilisés comme indices éditoriaux, jamais comme preuve automatique d’un thème ;
3. les notes sont prises en compte comme contexte et pour les relations éditoriales ;
4. chaque psaume est analysé sur son enseignement réel ;
5. les thèmes peuvent être abstraits ou concrets (animal, objet, élément, symbole, pratique, lieu, concept) lorsqu’ils portent une loi ou une fonction significative ;
6. chaque relation conserve importance, type de relation, versets et formulation de l’enseignement ;
7. un second passage au niveau du livre construit l’axe propre de l’Archange.

Les prières restent hors de l’indexation thématique actuelle. Elles ne sont pas utilisées pour créer ni enrichir l’expertise thématique.

## Première consolidation transversale

Une première couche transversale est créée dans :

`data/thematic-index/consolidations/books-01-10.json`

Elle ne remplace pas les preuves livre/psaume. Elle sert au logiciel pour comprendre les thèmes communs tout en préservant les nuances d’enseignement.

Signatures qui ressortent du premier bloc :

- Michaël : feu, conscience, choix, vérité, maîtrise, fidélité, fiabilité et puissance créatrice engagée ;
- Gabriel : eau, Source, âme, réceptivité, échange, mémoire, purification et transmission ;
- Raphaël : air, souffle, respiration, organes subtils et construction de l’immortalité ;
- Ouriel : terre, stabilité, alchimie, transformation, réalisation concrète et Bien commun.

La consolidation contient notamment des lectures transversales pour : Lumière, âme, Mère, pureté, discernement, responsabilité, alliance, parole, corps/corps subtils, Nation Essénienne/communauté et transformation.

Règle importante : une synthèse transversale ne doit jamais aplatir les différences entre Archanges. Pour une réponse précise ou un classement de psaumes, le logiciel doit toujours redescendre vers les relations livre/psaume et leurs versets.

## Fiabilisation technique

Le workflow `Validate thematic index` validait correctement les données des livres 9 et 10, mais échouait ensuite au moment de publier son rapport lorsqu’un workflow de reconstruction du répertoire thématique poussait simultanément sur `main`.

Le workflow a été rendu tolérant à cette concurrence avec synchronisation `pull --rebase` et tentatives de publication contrôlées. La validation complète a ensuite réussi et le rapport des dix livres a été publié.

## Suite

La séquence canonique continue maintenant avec le livre 11, puis les livres suivants par blocs de dix. La consolidation des livres 1–10 reste une première passe et sera enrichie à mesure que de nouveaux Archanges/livres apportent des sens, relations ou exceptions supplémentaires.

Le travail antérieur sur Michaël livre 17 reste un prototype méthodologique séparé ; il ne modifie pas l’ordre canonique de cette reprise depuis le livre 1.
