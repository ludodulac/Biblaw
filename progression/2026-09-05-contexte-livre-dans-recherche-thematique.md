# Contexte du livre dans la recherche thématique

Décision méthodologique ajoutée pendant l’indexation du livre 18, puis corrigée immédiatement : **le contexte doit provenir exclusivement du PDF de référence**.

## Source autorisée

La seule source doctrinale et éditoriale autorisée pour construire les contextes, thèmes, nuances et interprétations de Biblaw est :

- `Bible essénienne (classée par livres).pdf`.

Sont explicitement exclus de l’indexation et de l’enrichissement :

- sites internet esséniens ou non esséniens ;
- articles, podcasts, vidéos ou résumés externes ;
- autres éditions ou commentaires non présents dans le PDF ;
- mémoire générale ou connaissance externe utilisée pour compléter un manque du PDF.

Une source internet ne doit jamais confirmer, compléter, corriger ou contextualiser le contenu doctrinal du corpus. En cas de doute, on revient au PDF ; si le PDF reste ambigu, l’ambiguïté est enregistrée dans `data/incoherences.json` pour examen humain.

## Principe

Un passage appartient à un psaume, lui-même situé dans un livre qui possède un axe, un mouvement, un Archange et un ensemble de thèmes structurants. Toutes ces couches doivent être reconstruites uniquement à partir des éléments présents dans le PDF : titre du livre, attribution, introductions éventuelles, titres des psaumes, texte des psaumes, notes éditoriales, ordre des textes et annexes pertinentes.

La recherche future pourra restituer : preuve précise du psaume et des versets ; contexte du psaume ; contexte du livre ; nuance observable de l’Archange dans ce livre ; puis synthèse transversale entre livres. Toutes ces couches restent dérivées du même PDF source.

Le contexte ne crée jamais artificiellement un thème. Il sert à comprendre le sens, la nuance, l’importance et les relations d’un thème réellement présent dans le passage.

## Données

`data/thematic-index/book-contexts.json` porte désormais explicitement une `sourcePolicy` interdisant les sources externes. Les contextes des livres 17 et 18 sont marqués avec leur base PDF. Le livre 18 reste provisoire jusqu’à l’analyse complète de ses psaumes.

## Conséquence produit

Une recherche thématique pourra expliquer non seulement où un thème apparaît, mais dans quel mouvement d’enseignement du livre il apparaît, sans importer d’information extérieure au corpus choisi par l’utilisateur.

## Suite

Continuer l’indexation du livre 18 uniquement depuis les données extraites du PDF. À la consolidation globale, générer/réviser les contextes de tous les livres terminés avec la même règle PDF-only.
