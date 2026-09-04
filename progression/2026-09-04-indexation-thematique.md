# 2026-09-04 — Passage à l’indexation thématique

## Décision et méthode

Le corpus structuré n’est pas encore un index thématique. Chaque texte traité est suivi d’une indexation éditoriale. Chaque thème possède son fichier dans `data/themes/` et s’enrichit avec les nouveaux textes. On réutilise un thème existant plutôt que créer un doublon, on relie les thèmes à des passages précis, on distingue occurrence lexicale et pertinence thématique, et seules les ambiguïtés éditoriales réelles sont consignées dans `data/incoherences.json`.

Chaque psaume est traité avec sa prière associée lorsqu’elle enrichit réellement les thèmes. Les erreurs techniques déterministes sont corrigées directement ; seules les ambiguïtés de sens nécessitant une décision humaine interrompent le travail.

## Psaumes 105–112 — réalisés

105 : Lumière, Renaissance, Monde divin, Mensonge et illusion, Dévotion, Non-savoir, Intelligence supérieure.
106 : enrichissements + création de Discernement, Authenticité et vérité, Connaissance de soi, Âme.
107 : Nature et Mère, Libre arbitre et autonomie ; enrichissements du discernement, de l’âme et de l’illusion.
108 : Interdépendance et universel, Anges et vertus.
109 : Stabilité et enracinement, Tradition de la Lumière, Œuvre et soutien mutuel.
110 : Équilibre des mondes, Responsabilité et conséquences.
111 : Nutrition et nourriture intérieure, Essentiel et simplicité.
112 : approfondissement majeur d’Authenticité et vérité et du corps collectif de l’œuvre.

## Psaume 113 + prière 9 — réalisés

Titre : « Retrouve la terre de ta tradition », pages 1108–1112.

`Tradition de la Lumière` est fortement enrichi : racines, terre, continuité des ancêtres, mémoire historique et lien entre passé, présent et futur.

Nouveau thème :
- `Ancêtres et mémoire` : retrouver l’origine, marcher avec ceux qui ont précédé, reprendre consciemment une œuvre déjà commencée et éviter de recommencer indéfiniment les mêmes expériences.

## Psaume 114 + prière 10 — réalisés

Titre : « Les rois de la Lumière », pages 1113–1116.

Nouveaux thèmes :
- `Royauté de la Lumière` : dignité, service, accueil, unification des règnes, Père venant régner lorsque les mondes sont harmonisés.
- `Partage et générosité` : vie comme don, partage de ce qui est sain et réellement travaillé, refus de la séduction et de l’empoisonnement par des contenus faux ou non assimilés.

Le psaume enrichit aussi les axes Œuvre et soutien mutuel, Stabilité et enracinement, Interdépendance et universel et Lumière.

## Psaume 115 + prière 11 — réalisés

Titre : « Comment former ton corps d’éternité », pages 1117–1122.

Nouveaux thèmes :
- `Corps d’éternité` : formation simultanée du corps terrestre et du corps céleste, formation des organes de perception du monde supérieur, corps de compréhension et corps d’action juste.
- `Incarnation et réalisation` : puiser l’inspiration dans le supérieur et la conduire jusque dans une forme terrestre, ne pas remplacer l’action par la prière passive, préparer les conditions concrètes permettant l’incarnation correcte d’une œuvre.

## Psaume 116 + prière 12 — réalisés

Titre : « Les dangers de l’intelligence technologique », pages 1123–1129.

Nouveaux thèmes :
- `Constance et persévérance` : aller jusqu’au bout de la pensée, de la parole et de l’œuvre ; l’accomplissement fortifie, l’inachevé affaiblit.
- `Technologie et intelligence électrique` : index fidèle à la cosmologie propre du psaume concernant technologie, électricité, influences subtiles et asservissement. Ces formulations sont enregistrées comme doctrine du texte et non comme validation scientifique externe.

## Psaume 117 — réalisé

Titre : « Une œuvre primordiale pour l’humanité », pages 1130–1132. Aucun texte de prière directement associé.

Nouveau thème :
- `Cultes des quatre Archanges` : cultes du feu, de l’eau, de l’air et de la terre, quatre sceaux, quatre temples, ancrage terrestre de l’alliance et réconciliation des règnes.

Le psaume enrichit également Œuvre et soutien mutuel, Équilibre des mondes, Interdépendance et universel et Incarnation et réalisation.

## Psaume 118 + prière 13 — réalisés

Titre : « 5 questions fondamentales à se poser », pages 1133–1135.

Nouveau thème :
- `Éveil et présence consciente` : lecture vivifiante des textes sacrés, concentration, attention, présence à la nourriture, à la parole, à la prière et au sommeil, direction de la vie depuis le centre et l’âme plutôt que par automatisme.

Le psaume renforce également Incarnation et réalisation : la Lumière doit toucher le plan physique et recevoir un corps concret dans la vie.

## État d’avancement

- Psaumes 105 à 118 : indexés thématiquement.
- Prières associées 1 à 13 : traitées lorsqu’elles s’appliquent ; le psaume 117 n’a pas de prière associée.
- Psaumes 119 à 130 : structurés, à indexer séquentiellement.
- Aucun cas de sens réellement ambigu nécessitant une décision humaine n’a été rencontré sur 113–118.

## Suite

Poursuivre avec le psaume 119 et sa prière, puis avancer sans interruption jusqu’à 130 tant qu’aucune ambiguïté éditoriale réelle n’exige l’utilisateur. À la fin de la tranche 105–130 : revue transversale des synonymes, chevauchements, hiérarchies et relations entre thèmes ; vérification des références ; préparation des données destinées au moteur et au bouton `Index`, qui doit afficher uniquement les thèmes éditorialement constitués.
