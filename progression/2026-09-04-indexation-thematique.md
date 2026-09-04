# 2026-09-04 — Passage à l’indexation thématique

## Décision et méthode

Le corpus structuré n’est pas encore un index thématique. Chaque texte traité est suivi d’une indexation éditoriale. Chaque thème possède son fichier dans `data/themes/` et s’enrichit avec les nouveaux textes. On réutilise un thème existant plutôt que créer un doublon, on relie les thèmes à des passages précis, on distingue occurrence lexicale et pertinence thématique, et seules les ambiguïtés éditoriales réelles sont consignées dans `data/incoherences.json`.

Chaque psaume est traité avec sa prière associée lorsqu’elle enrichit réellement les thèmes. Les erreurs techniques déterministes sont corrigées directement ; seules les ambiguïtés de sens nécessitant une décision humaine interrompent le travail.

## 105–109 — réalisés

105 : premiers index généraux — Lumière, Renaissance, Monde divin, Mensonge et illusion, Dévotion, Non-savoir, Intelligence supérieure.

106 : enrichissement de Lumière et Mensonge et illusion ; création de Discernement, Authenticité et vérité, Connaissance de soi, Âme.

107 : enrichissement de Mensonge et illusion, Discernement, Âme, Connaissance de soi, Intelligence supérieure, Lumière ; création de Nature et Mère et Libre arbitre et autonomie.

108 : enrichissement de Nature et Mère et Lumière ; création d’Interdépendance et universel et Anges et vertus.

109 : création de Stabilité et enracinement, Tradition de la Lumière, Œuvre et soutien mutuel.

## Psaume 110 + prière 6 — réalisés

Titre : « L’équilibre des mondes », pages 1091–1097.

Nouveaux thèmes :
- `Équilibre des mondes` : conformité aux lois de la vie, vision juste, unification de la pensée, du cœur et de la volonté avec une intelligence supérieure.
- `Responsabilité et conséquences` : traces laissées aux autres êtres, loi de la semence et de la récolte, responsabilité étendue aux règnes.

Thèmes enrichis : Interdépendance et universel, Discernement. Le véritable bien commun est explicitement élargi aux sept règnes de l’alliance du Père et de la Mère.

## Psaume 111 + prière 7 — réalisés

Titre : « Dans la nutrition, les plus grands secrets de l’univers », pages 1098–1102.

Nouveaux thèmes :
- `Nutrition et nourriture intérieure` : nourriture physique et symbolique, maturité des fruits, assimilation des idées et traditions, entretien de la flamme sacrée et des différents étages de l’être.
- `Essentiel et simplicité` : sortir de la surcharge d’idées et de préoccupations, revenir à ce qui est vrai, utile, bénéfique et assimilable.

Thème enrichi : Discernement, avec un nouveau sens lié à la maturité d’une idée ou d’une tradition : ne pas absorber une nouveauté non éprouvée ni conserver une forme ancienne devenue morte.

## Psaume 112 + prière 8 — réalisés

Titre : « N’attendez pas d’être purs, soyez vrais », pages 1103–1107.

Thème majeur enrichi : `Authenticité et vérité`. Le psaume distingue explicitement vérité et perfection : être vrai consiste à reconnaître ce que l’on porte, cesser les masques et justifications et incarner ce que l’on reconnaît comme vrai.

`Œuvre et soutien mutuel` est également enrichi : la sagesse doit recevoir un corps collectif et universel, un organisme vivant capable d’agir et de parler dans le monde.

Le psaume confirme aussi les axes Responsabilité et conséquences, Tradition de la Lumière, Anges et vertus et Lumière.

## État d’avancement

- Psaumes 105 à 112 + prières 1 à 8 : indexés thématiquement.
- Psaumes 113 à 130 : structurés, à indexer séquentiellement.
- Aucun cas de sens réellement ambigu nécessitant une décision humaine n’a été rencontré dans 107–112.

## Suite

Poursuivre avec le psaume 113 et sa prière puis avancer sans interruption tant qu’aucune ambiguïté éditoriale réelle ne nécessite l’utilisateur. À la fin de 105–130 : revue transversale des synonymes, chevauchements et hiérarchies ; vérification des références ; préparation des données destinées au moteur de recherche et au bouton `Index`, qui doit afficher uniquement les thèmes éditorialement constitués.
