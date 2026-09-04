# 2026-09-04 — Reprise de l’indexation thématique livre par livre

## Décision

L’ancienne première passe thématique sur Michaël 105–130 est conservée comme prototype, mais elle n’est plus considérée comme l’index définitif.

La nouvelle indexation repart méthodologiquement de zéro dans `data/thematic-index/` sans toucher au corpus extrait et validé.

## Nouvelle unité de travail

Le travail se fait désormais :

1. livre par livre ;
2. psaume par psaume ;
3. en tenant compte du titre du livre, du titre du psaume, du texte intégral et des notes éditoriales disponibles ;
4. sans utiliser les prières annexes comme matière d’indexation thématique pour l’instant.

Les prières restent liées aux psaumes dans le corpus et pourront être affichées ou exportées plus tard, mais elles ne servent pas actuellement à construire les pages de thèmes.

## Définition d’un thème

Un thème n’est pas seulement une grande notion doctrinale et n’est pas non plus une simple liste de mots.

Une réalité concrète comme `Feu`, `Assemblée`, `Pierre`, `Animal`, `Arbre` ou `Chouette` peut devenir un thème dès qu’un passage lui attribue un enseignement significatif : définition, fonction, loi, relation, pratique, symbole, condition, danger, conséquence ou rôle.

Inversement, une occurrence lexicale sans apport de sens n’est pas indexée comme preuve thématique.

Chaque page de thème est conçue pour s’enrichir progressivement avec plusieurs psaumes puis plusieurs Archanges. Elle conserve :

- le résumé de ce que chaque Archange enseigne sur le thème ;
- les principes ou lois qui apparaissent ;
- les psaumes et versets sources ;
- l’importance de chaque psaume pour ce thème (`central`, `important`, `supporting`) ;
- les relations avec d’autres thèmes.

Cette structure doit permettre plus tard des recherches comme : « tout ce que la Bible dit sur l’Assemblée », « que dit Michaël sur le Feu ? », « comparer Michaël et Raphaël sur l’Âme », avec remontée des psaumes les plus importants.

## Structure créée

- `data/thematic-index/method.json` : méthode et règles.
- `data/thematic-index/books/michael-book-17.json` : suivi du livre 17.
- `data/thematic-index/themes/` : nouvelles pages thématiques cumulatives.

Le contexte `michael-book-17-introduction` est référencé par les psaumes mais aucun fichier correspondant n’a encore été localisé dans `data/`. Ce manque est technique/documentaire et n’empêche pas l’indexation à partir des titres, textes et notes disponibles.

## Michaël — Livre 17 « L’heure du choix »

### Psaume 105 — « Aux infidèles »

Traité avec sa note éditoriale. La note confirme la structure de dialogue autour du verset 9 et n’est pas utilisée artificiellement comme source de thème.

Thèmes substantiels identifiés : fidélité et infidélité, Lumière, connaissance de soi, mensonge et illusion, influences et mondes invisibles, renaissance, intelligence supérieure, feu, culte, dévotion et adoration, perception et sens, prière, non-savoir, pureté et vérité, monde divin, âme, sommeil et rêve, vie et mort.

### Psaume 106 — « Comment discerner le vrai du faux »

Le discernement est central. Création ou enrichissement de : discernement, authenticité, connaissance de soi, pureté et vérité, mensonge et illusion. Les pierres, plantes, animaux, maîtres et sages, ainsi que les Anges reçoivent des pages distinctes parce que le psaume leur attribue un rôle substantiel comme repères vers un chemin vrai ; ce n’est pas une simple extraction de noms.

### Psaume 107 — « Ne te laisse pas séduire par un monde artificiel »

Axes structurants : monde artificiel, sommeil/rêve/hypnose, vigilance, discernement, nature et Mère, animaux, âme, influences invisibles, libre arbitre, Ronde des Archanges, fidélité à une intelligence supérieure.

Correction méthodologique faite à ce stade : `Âme` et `Sommeil et rêve` sont séparés en deux pages afin que chaque notion reste réellement recherchable.

### Psaume 108 — « Honore ton Père et ta Mère »

Axes structurants : interdépendance, responsabilité, équilibre des mondes, hiérarchies, Père et Mère, nature et Mère, règnes, solidarité et soutien mutuel, Anges, Ronde des Archanges, âme, intelligence supérieure, royauté.

Ce psaume est un exemple de texte appelé à ressortir comme psaume majeur sur plusieurs thèmes simultanément.

## État actuel

- Nouvelle méthode active : oui.
- Livre en cours : Michaël, livre 17.
- Psaumes réindexés avec la nouvelle granularité : 105 à 108.
- Prières thématiquement indexées : non.
- Notes utilisées comme contexte éditorial : oui.
- Ancien index : conservé comme prototype, non utilisé comme référence finale.

## Suite

Continuer séquentiellement avec le psaume 109, enrichir les pages déjà ouvertes et créer de nouvelles pages uniquement lorsque le texte apporte un contenu thématique réel. Une fois le livre 17 terminé, effectuer une consolidation interne du livre avant de passer au livre suivant.
