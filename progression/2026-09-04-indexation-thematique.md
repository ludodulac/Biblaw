# 2026-09-04 — Passage à l’indexation thématique

## Décision

Le corpus structuré n’est pas encore un index thématique. À partir de maintenant, chaque texte traité doit être suivi d’une indexation éditoriale. L’objectif est de construire progressivement un index de tous les thèmes réellement présents dans la Bible essénienne. Chaque thème possède son propre fichier dans `data/themes/` et s’enrichit à mesure que de nouveaux psaumes, prières, notes et autres textes sont intégrés.

## Méthode permanente

Pour chaque texte : identifier les thèmes réellement enseignés ; distinguer thème principal, sous-thèmes et nuances de sens ; relier chaque entrée à des passages précis ; réutiliser un thème existant plutôt que créer un doublon ; créer un nouveau thème lorsqu’un concept distinct apparaît ; distinguer occurrence lexicale et pertinence thématique ; consigner uniquement les ambiguïtés éditoriales réelles dans `data/incoherences.json`.

Chaque psaume est traité avec sa prière associée lorsqu’elle enrichit réellement les thèmes. Les erreurs techniques déterministes sont corrigées directement ; seules les ambiguïtés de sens nécessitant une décision humaine doivent interrompre le travail.

## Psaumes 105–106 — réalisés

105 a établi les premiers index généraux : Lumière, Renaissance, Monde divin, Mensonge et illusion, Dévotion, Non-savoir, Intelligence supérieure. 106 a enrichi Lumière et Mensonge et illusion et créé Discernement, Authenticité et vérité, Connaissance de soi et Âme.

## Psaume 107 + prière 3 — réalisés

Titre : « Ne te laisse pas séduire par un monde artificiel », pages 1077–1080.

Thèmes enrichis : Mensonge et illusion, Discernement, Âme, Connaissance de soi, Intelligence supérieure, Lumière.

Nouveaux thèmes :
- `Nature et Mère` : nature vivante, fidélité à la Mère, sagesse animale, âme de la Mère.
- `Libre arbitre et autonomie` : fausse indépendance, domination qui retire intelligence et libre arbitre, responsabilité de penser et s’éveiller par soi-même.

Apport majeur : l’illusion est décrite comme un monde artificiel collectif nourri par la force de vie humaine ; le discernement devient une pratique de vigilance, d’observation intérieure et d’examen des actes derrière les paroles.

## Psaume 108 + prière 4 — réalisés

Titre : « Honore ton Père et ta Mère », pages 1081–1085.

Thèmes enrichis : Nature et Mère, Lumière. Le texte approfondit l’homme comme être relié aux règnes et aux hiérarchies et la Mère comme réalité originelle et vivante.

Nouveaux thèmes :
- `Interdépendance et universel` : la vie comme lien, responsabilité envers le tout, équilibre des mondes, homme à la frontière du visible et de l’invisible.
- `Anges et vertus` : Ange comme hiérarchie supérieure, vertu comme langage de l’âme et d’un monde supérieur, relation juste aux règnes.

## Psaume 109 + prière 5 — réalisés

Titre : « L’homme-girouette », pages 1086–1090.

Nouveaux thèmes :
- `Stabilité et enracinement` : sortir de l’instabilité des influences, devenir une terre et un socle, s’enraciner consciemment.
- `Tradition de la Lumière` : mémoire divine, sagesse des grands maîtres comme terre/corps/ciel, semence d’éternité et continuité de l’œuvre.
- `Œuvre et soutien mutuel` : sortir de l’existence centrée sur soi, bâtir ensemble, poser des œuvres durables pour le bien de tous.

Le psaume enrichit aussi les axes déjà établis : Intelligence supérieure, Nature et Mère, Lumière, Connaissance de soi et Interdépendance.

## État d’avancement

- Psaumes 105 à 109 + prières 1 à 5 : indexés thématiquement.
- Psaumes 110 à 130 : structurés, à indexer séquentiellement.
- Aucun cas de sens réellement ambigu nécessitant une décision humaine n’a été rencontré dans 107–109.

## Suite

Poursuivre avec 110 et sa prière, puis avancer sans interruption tant qu’aucune ambiguïté éditoriale réelle ne nécessite l’utilisateur. À la fin de 105–130, effectuer une revue transversale : synonymes, chevauchements, hiérarchies de thèmes, relations entre thèmes et préparation des données destinées au futur moteur. Le bouton `Index` devra afficher les thèmes éditorialement constitués et non des titres ou mots automatiquement extraits.
