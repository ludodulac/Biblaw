# Normalisation des identifiants et contextes thématiques — 2026-09-07

## But

Ranger les doublons purement techniques d’identifiants thématiques sans appauvrir la richesse contextuelle du corpus.

## Principe éditorial confirmé

Le sens d’un thème n’a pas à être réduit à une définition globale unique.

Un terme peut recevoir plusieurs éclairages complémentaires selon l’Archange, le livre et le psaume. La source de sens reste le corpus interne : psaume, versets d’appui et `teaching` documentaire. Une analogie externe ne doit pas servir à fusionner, renommer ou définir un thème canonique.

Conséquence :

- plusieurs explications contextuelles d’un même thème sont conservées ;
- un même libellé ne suffit jamais, à lui seul, à prouver une fusion ;
- une consolidation d’identifiants n’est autorisée que lorsqu’il s’agit d’une variante technique auditée ;
- une ambiguïté sémantique réelle reste visible dans le runtime de recherche.

## Quatre collisions techniques résolues

Les contextes internes ont été comparés avant consolidation. Les variantes suivantes ont été normalisées :

- `corps-deau` → `corps-d-eau` ;
- `corps-dimmortalite` → `corps-d-immortalite` ;
- `microcosme-macrocosme` → `microcosme-et-macrocosme` ;
- `royaut-e-interieure` et `royauté-interieure` → `royaute-interieure`.

Les libellés, niveaux d’importance, directness, versets d’appui et enseignements n’ont pas été réécrits pour imposer une définition unique.

### Exemple « Corps d’eau »

Le psaume 72 du livre 10 décrit le premier corps subtil autour du physique comme une eau où circulent influences, forces et intelligences.

Le psaume 149 du livre 22 décrit le corps d’eau comme le milieu subtil qui entoure et relie pensées, états d’âme, volontés et influences.

Ces formulations sont conservées comme deux éclairages contextuels du même thème canonique `corps-d-eau`.

## Protection technique

`scripts/normalize_known_theme_identifiers.py` contient uniquement une petite liste explicite de migrations déjà auditées. Il ne découvre aucune équivalence par ressemblance lexicale.

Le script :

- normalise les IDs connus ;
- refuse tout ID legacy en mode `--check` ;
- ne supprime une relation doublonnée après normalisation que si les deux relations sont strictement identiques ;
- échoue si deux relations différentes entreraient en collision.

Les générateurs qui réintroduisaient deux anciens IDs ont été corrigés à la source :

- `scripts/deepen_book20_semantic_part5.py` ;
- `scripts/deepen_book21_semantic_part1.py`.

Le pipeline canonique normalise et vérifie avant reconstruction, puis revérifie après tous les générateurs.

## État canonique après reconstruction

- 44 livres ;
- 1158 psaumes analysés ;
- 10409 relations thématiques ;
- 1247 thèmes canoniques ;
- 1339 alias de recherche ;
- 5 ambiguïtés sémantiques explicites ;
- 0 collision technique de libellé dans le répertoire ;
- 0 relation sans versets d’appui ;
- 0 relation sans `teaching`.

Le nombre de relations est resté à 10409 : aucune relation vers un psaume n’a été perdue pendant le nettoyage des identifiants.

## Cinq ambiguïtés conservées volontairement

Les formulations suivantes correspondent encore à plusieurs IDs canoniques et ne sont pas considérées comme des doublons techniques :

- `alliance de lumiere` ;
- `nutrition subtile` ;
- `service du monde divin` ;
- `temple interieur` ;
- `transmission aux generations`.

Elles restent explicitement désambiguïsées par le moteur. Toute éventuelle décision future doit repartir des contextes internes de leurs psaumes, pas de la seule ressemblance des libellés.

## CI

La validation de recherche vérifie désormais conjointement :

- couverture 1158 / 1158 / 1158 ;
- aucun couple thème/psaume dupliqué ;
- `semanticMerging: false` ;
- `connectionMeaning: psalm-cooccurrence-only` ;
- 0 collision technique de répertoire ;
- cohérence entre le nombre d’ambiguïtés du runtime et le rapport qualité ;
- les 12 requêtes de production ;
- l’audit Assemblée / Sainte Assemblée ;
- la recherche par numéro de psaume ;
- les index navigateur préconstruits.

Dernier workflow `Validate thematic search UI` après adaptation des audits : succès complet.
