# 2026-09-04 — Indexation thématique du livre 17 de Michaël

## Méthode permanente

Le corpus structuré et l’index thématique sont deux couches distinctes. Chaque texte validé est lu éditorialement ; les thèmes existants sont enrichis avant d’en créer de nouveaux. Les références sont reliées à des passages précis. Une occurrence lexicale ne suffit pas à constituer une pertinence thématique. Les prières sont intégrées lorsqu’elles apportent une matière sémantique réelle. Les erreurs techniques déterministes sont corrigées directement ; seules les ambiguïtés éditoriales authentiques vont dans `data/incoherences.json`.

Les affirmations cosmologiques ou doctrinales sont indexées comme contenu du corpus, sans être transformées en affirmations scientifiques externes.

## Tranche 105–118

105–112 : première constitution des thèmes Lumière, Renaissance, Monde divin, Mensonge et illusion, Dévotion, Non-savoir, Intelligence supérieure, Discernement, Authenticité et vérité, Connaissance de soi, Âme, Nature et Mère, Libre arbitre et autonomie, Interdépendance et universel, Anges et vertus, Stabilité et enracinement, Tradition de la Lumière, Œuvre et soutien mutuel, Équilibre des mondes, Responsabilité et conséquences, Nutrition et nourriture intérieure, Essentiel et simplicité.

113 : Ancêtres et mémoire ; approfondissement de Tradition de la Lumière.
114 : Royauté de la Lumière ; Partage et générosité.
115 : Corps d’éternité ; Incarnation et réalisation.
116 : Constance et persévérance ; Technologie et intelligence électrique.
117 : Cultes des quatre Archanges. Aucun texte de prière directement associé.
118 : Éveil et présence consciente.

## Continuation 1 — psaumes 119 à 122

119 + prière 14 : `Pureté et conformité divine`. Grande règle : distinguer les mondes, préparer un réceptacle conforme et ne pas projeter les intérêts humains sur le monde divin.

120 + prière 15 : `Bien commun`. Harmonisation des points de vue dans une intelligence supérieure commune, cercle comme espace de vérité, vigilance et réalisation terrestre.

121 + prière 16 : `Choix et croisée des chemins`. Le choix est relié au maintien de l’âme et de la conscience individuelle, au discernement et à un engagement réellement assumé.

122 + prière 17 : `Temple vivant de la Mère`. Terre intérieure et extérieure capable de recevoir une semence supérieure ; nature comme temple vivant ; attention sensorielle et intention consciente dans le contact avec les règnes.

## Continuation 2 — psaumes 123 à 126

123 + prière 18 : `Le vrai et l’imitation`. Distinction entre réalité vécue, association effective, masques, images et imitation extérieure.

124 + prière 19 : `Conscience et transformation intégrale`. La conscience comme terre de la deuxième naissance ; assimilation d’une semence de sagesse jusqu’à l’action et à la transformation de l’être.

125 + prière 20 : approfondissement d’`Équilibre des mondes`. Formulation centrale : unir les mondes sans les mélanger ; l’homme est l’intermédiaire responsable qui doit connaître les lois de chaque plan et adapter intelligemment le passage entre eux.

126 + prière 21 : approfondissement d’`Authenticité et vérité`. Le thème de l’hypocrisie n’est volontairement pas créé séparément : le texte renforce la cohérence intérieur/extérieur, l’abandon des masques et de l’autojustification et la priorité donnée au fait d’être soi-même vrai plutôt que de juger le faux chez autrui.

## Continuation 3 — psaumes 127 à 130

127 + prière 22 : `Protection des règnes de la Mère`. Passage de la compassion abstraite à l’action organisée pour les minéraux, végétaux, animaux et autres règnes ; responsabilité de ne pas laisser la cruauté et l’indifférence devenir normales.

128 + prière 23 : `Enseignement à vivre`. La sagesse doit être assimilée comme une nourriture, devenir pensée, orientation, action et œuvre concrète plutôt que rester parole contemplée.

129 + prière 24 : `Légèreté et maîtrise de soi`. Se connaître, se stabiliser, mettre de l’ordre dans sa propre maison et cesser de transférer son désordre ou son poids sur les autres êtres et mondes.

130 + prière 25 : `Porte du feu et lien ciel-terre`. Le culte du feu comme porte et structure de continuité entre ciel et terre ; accomplissement des quatre cultes, protection des règnes et préparation d’une terre nettoyée pour une nouvelle semence.

## État atteint

- Psaumes Michaël 105 à 130 : indexation thématique éditoriale de première passe terminée.
- Prières du livre 17 : intégrées dans la passe thématique lorsqu’elles sont associées aux psaumes traités.
- Les thèmes constitués sont enregistrés dans `data/themes/` et déclarés dans `data/catalog.json`.
- Aucun nouveau cas n’a nécessité une décision humaine pendant les continuations 119–130.

## Étape suivante

La prochaine phase n’est plus de créer des thèmes psaume après psaume dans cette tranche. Il faut maintenant effectuer une revue transversale 105–130 : détecter les synonymes et quasi-doublons, décider des thèmes parents/enfants et relations, vérifier les références et les fichiers orphelins, puis produire un index dérivé reproductible destiné au moteur de recherche et au bouton `Index`. Le bouton ne devra afficher que les thèmes éditorialement constitués, jamais les simples titres de psaumes.
