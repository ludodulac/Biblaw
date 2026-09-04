# 2026-09-04 — Livres 4 à 7 et fiabilisation de la chaîne thématique

## Avancement éditorial

La reprise thématique livre par livre est maintenant réalisée jusqu’au **livre 7 inclus** :

- livre 1 — Michaël — `data/thematic-index/books/book-01.json` ;
- livre 2 — Gabriel — `data/thematic-index/books/book-02.json` ;
- livre 3 — Raphaël — `data/thematic-index/books/book-03.json` ;
- livre 4 — Ouriel — `data/thematic-index/books/book-04.json` ;
- livre 5 — Michaël — `data/thematic-index/books/book-05.json` ;
- livre 6 — Gabriel — `data/thematic-index/books/book-06.json` ;
- livre 7 — Raphaël — `data/thematic-index/books/book-07.json`.

Chaque fichier contient une synthèse à l’échelle du livre puis une analyse de chaque psaume avec thèmes significatifs, importance, caractère direct/symbolique, versets de preuve et enseignement associé. Les titres servent de contexte ; les notes sont lues comme contexte éditorial ; les prières restent exclues de cette indexation thématique.

## Livre 4 — Ouriel — « Vous êtes l’espoir d’un monde »

Axe fort : conduire l’inspiration supérieure jusqu’à la réalisation terrestre. Ouriel insiste sur stabilité, persévérance, perfection des œuvres, vérité, silence, vie intérieure créatrice, destinée, harmonie avec les règnes et union entre hauteurs et profondeurs.

Des réalités concrètes sont constituées comme thèmes lorsqu’elles portent la loi du passage : montagne, arbre, pierre, animaux, jardin intérieur, huile d’Ouriel, silence, corps, œuvre et nature notamment.

## Livre 5 — Michaël — « Homme, redeviens un mage »

Axe fort : voie opérative du mage. La vérité est reçue dans le silence ; les sens et les trois centres doivent être orientés ; le feu et les quatre éléments deviennent des forces de construction ; l’imperfection doit être transformée plutôt que niée ; la puissance créatrice doit prendre corps dans des œuvres collectives et durables.

Thèmes structurants : Mage, Feu, Vérité, Silence, Pureté, Maîtrise, Pouvoir créateur, Quatre éléments, Pensée, Trois centres, Chouette, Licorne, Fourmis, Loup et Agneau, Graal, Pyramide de Lumière, Nation Essénienne, Communauté, Ronde des Archanges, Tradition de la Lumière.

Les animaux sont conservés comme thèmes à part entière lorsqu’ils enseignent une loi : la Chouette pour la vision dans l’imperfection, la Licorne pour l’union verticale et la pureté, la Fourmi pour le but et le soutien mutuel, le Loup et l’Agneau pour la maîtrise des polarités.

## Livre 6 — Gabriel — « Vivre avec son âme »

Axe fort : l’âme comme eau vivante. Gabriel développe une science de la circulation : source, fleuve, océan, miroir, fécondation, échange, réceptivité, purification et transformation. La stagnation de l’eau correspond régulièrement à une vie intérieure coupée de sa source ou non mise en pratique.

Thèmes structurants : Âme, Eau, Source, Fleuve, Océan, Pureté, Réceptivité, Échange, Fécondation, Miroir, Respect, Discipline, Temple, École de Dieu, Maître, Joie, Gratitude, Beauté, Son, Musique, Homme-arbre, Œil, Soleil, Corps-Âme-Esprit, Nation Essénienne, Vertus, Anges, Nature et Impersonnalité.

Particularité transversale confirmée de Gabriel : l’eau n’est pas seulement un symbole ; elle fournit un modèle des relations entre les mondes, de la qualité des échanges, de la fécondation et de la vie de l’âme.

## Livre 7 — Raphaël — « Les clés de l’immortalité »

Axe fort : déterminer ce qui, dans l’homme, peut réellement devenir immortel et construire les organes capables de respirer dans l’éternité. L’immortalité n’est pas la conservation des enveloppes mortelles mais l’éveil du germe subtil, la construction d’un corps de Lumière et la respiration consciente dans les mondes supérieurs.

Thèmes structurants : Immortalité, Souffle, Air, Respiration, Méditation, Sérénité, Conscience, Pensée, Volonté, Corps de Lumière, Germe divin, Enveloppes, Tradition, Maître, Anges, Nature, Résurrection et Vision.

Les thèmes concrets significatifs incluent notamment : Arbre de vie, Oiseau du soleil, Pierre, Plante/Fleur, Oignon, Ruche/Reine, Aigle, Souris, Plume de l’esprit, Air, Pluie. Ces images sont indexées parce qu’elles portent un enseignement propre et reproductible, pas simplement parce qu’elles apparaissent dans le texte.

## Réparation documentaire majeure : notes de bas de page et reprise du texte

Une erreur systématique de l’extracteur a été découverte : dans certains psaumes, une note de bas de page pouvait absorber la reprise du texte principal et donc faire disparaître un ou plusieurs versets du corpus.

Le correctif a été généralisé dans `scripts/normalize_notes_resumed_verses.py`. Il ne repose plus sur deux exceptions ponctuelles : il vérifie la continuité attendue de la numérotation et la retrouve dans la page PDF source avant de restituer le texte au psaume et de nettoyer la note.

La réparation a récupéré automatiquement des versets dans les livres 3, 5, 6, 7, 8, 9 et 10. La passe complète n’a laissé aucun cas `unresolved` et aucun cas `remaining`. Ces cas sont des erreurs techniques déterministes et ne doivent pas être inscrits dans `data/incoherences.json`.

La chaîne livres 1–10 exécute désormais dans le même workflow :

1. extraction depuis le PDF ;
2. réparation des versets repris après notes ;
3. normalisation des titres coupés ;
4. normalisation des titres incorporés ;
5. validation structurelle ;
6. reconstruction des paquets de lecture thématique ;
7. commit synchronisé du corpus, des notes, des rapports et des paquets.

Cela évite qu’un corpus corrigé et les paquets servant à l’indexation thématique divergent.

## Validation thématique et index logiciel

`data/thematic-index/books/` est la source éditoriale de l’expertise. `scripts/build_thematic_directory.py` produit le répertoire transversal dérivé `data/thematic-index/theme-directory.json` avec occurrences, Archanges concernés et classement des psaumes par importance.

Le logiciel utilise maintenant ce vrai répertoire pour le bouton **Index** et pour la recherche thématique. Il n’utilise plus automatiquement les titres de psaumes ni les `conceptIds` comme faux thèmes.

Le validateur contrôle notamment l’existence des psaumes et versets référencés, les niveaux d’importance, les doublons et la synchronisation des titres. Le workflow a été fiabilisé afin que chaque nouveau fichier éditorial de livre déclenche cette chaîne de normalisation, validation et reconstruction du répertoire.

Dernier état confirmé avant l’ajout des livres 6 et 7 : **5 livres, 118 psaumes, 459 relations thématiques, 0 erreur, 0 avertissement**. Les livres 6 et 7 sont ensuite entrés dans la chaîne de validation automatique.

## Règles qui restent en vigueur

- un titre est un indice de compréhension, pas automatiquement un thème ;
- une note est un contexte éditorial à lire ;
- une prière reste liée à son psaume mais n’est pas indexée thématiquement dans cette phase ;
- un animal, un objet, un élément ou un lieu devient un thème s’il porte réellement un enseignement ;
- l’index n’est jamais une simple liste lexicale ;
- les erreurs déterministes sont corrigées dans la chaîne ;
- seules les ambiguïtés éditoriales réelles sont ajoutées dans `data/incoherences.json` ;
- après chaque livre, une synthèse interne doit consolider les relations entre les psaumes avant la future synthèse transversale par thème et par Archange.

## Étape suivante

Poursuivre dans l’ordre source avec le **livre 8**, puis les livres 9 et 10, en utilisant le corpus désormais réparé et synchronisé. Après les dix premiers livres, effectuer une première consolidation transversale des thèmes déjà communs aux Archanges sans supprimer leurs différences de sens.
