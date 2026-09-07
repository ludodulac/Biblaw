# Modèle de connaissance Biblaw

Biblaw doit fonctionner comme une application statique sans intelligence artificielle connectée au moment de la consultation. Elle s’appuie sur un corpus vérifié, des analyses éditoriales canoniques et des index générés à l’avance.

## Objets à ne pas confondre

1. **Requête** : ce que la personne saisit dans le champ de recherche.
2. **Référence documentaire** : psaume, verset, prière, note ou annexe identifiable dans le corpus.
3. **Thème canonique** : sujet éditorial explicitement relié à des passages avec un `themeId`, un niveau d’importance, des versets d’appui et un repère `teaching`.
4. **Alias de recherche** : forme normalisée explicitement reliée à un ou plusieurs thèmes canoniques.
5. **Occurrence textuelle** : présence littérale d’un mot ou d’une expression dans le texte du corpus.
6. **Connexion thématique** : cooccurrence de deux thèmes dans les mêmes psaumes ; elle n’implique ni synonymie ni causalité.

Une synthèse ou une interprétation ne remplace jamais la référence source.

## Trois intentions de recherche

### 1. Accès documentaire par numéro

Une requête comme `105` ou `psaume 105` cherche le champ documentaire `number`.

Plusieurs livres peuvent porter le même numéro. Le moteur présente alors toutes les correspondances, sans choisir arbitrairement un psaume.

### 2. Recherche thématique

La résolution suit exclusivement :

1. normalisation de la requête ;
2. alias explicitement présent dans le runtime ;
3. à défaut, libellé ou identifiant canonique exact après normalisation ;
4. sinon aucun thème.

Il n’existe pas de rapprochement sémantique automatique par sous-chaîne, ressemblance lexicale ou fréquence de mots.

Un alias peut pointer vers plusieurs `themeId`. Dans ce cas l’ambiguïté doit rester visible et l’utilisateur peut choisir le thème canonique voulu.

### 3. Recherche textuelle

Le mode `Mots et phrases` recherche la formulation littérale et contiguë dans le texte affiché du corpus. Les identifiants sémantiques ne doivent jamais créer artificiellement une occurrence textuelle.

La présence d’un mot dans de nombreux psaumes ne suffit pas à créer un thème.

## Normalisation de requête

Les accents, apostrophes et ponctuations sont neutralisés pour la recherche. Certains articles français initiaux (`l`, `le`, `la`, `les`, `un`, `une`, `des`) peuvent être ignorés comme commodité de requête.

Cette normalisation est strictement lexicale. Elle ne fusionne pas les concepts.

Exemple validé :

- `la sainte assemblée` peut résoudre `Sainte Assemblée` ;
- `assemblée` ne doit pas être redirigé vers `Sainte Assemblée`.

## Niveaux des relations thématiques

Une relation entre un thème et un psaume porte un niveau d’importance éditoriale :

- `central` ;
- `important` ;
- `related`.

L’interface les présente dans l’ordre **Central → Important → Lié**. Cet ordre organise la recherche ; il n’est pas une hiérarchie de vérité doctrinale.

Chaque relation canonique doit conserver ses versets d’appui et un `teaching` formulé comme repère contextuel.

## Deux formes de dialogue observées dans le PDF

Le corpus emploie au moins deux formes qu’il faut conserver :

- la question d’Olivier Manitara porte elle-même un numéro de verset ;
- une phrase éditoriale comme `Olivier Manitara demanda alors à l’Archange` introduit une question non numérotée entre deux versets, puis la numérotation de la réponse reprend.

Les questions ne doivent donc pas être forcées dans la liste des versets. Le champ `dialogueSegments` mémorise leur position, leur locuteur, leur éventuel numéro de verset et la formule éditoriale qui permet d’identifier le locuteur.

## Dossier thématique évolutif

Un thème est un dossier éditorial révisable. Il commence par des relations sourcées vers des psaumes et pourra, dans une phase éditoriale ultérieure, accueillir des synthèses plus riches.

Les synthèses globales sont volontairement différées tant que la couche de recherche et l’index ne sont pas considérés comme suffisamment stabilisés.

Une future synthèse devra toujours rester traçable vers les passages concernés et distinguer les différents contextes du thème plutôt que d’imposer une définition unique.

## Navigation transversale

`theme-connections.json` relie des thèmes qui apparaissent dans les mêmes psaumes.

La seule signification garantie est la **cooccurrence de psaumes**. Une connexion doit être présentée comme navigation (« thèmes également présents »), jamais comme équivalence de sens.

## Unités consultables et exportables

- verset seul ;
- sélection de versets ;
- psaume complet ;
- prière seule ;
- bloc documentaire `psaume + prière rattachée` ;
- note ou texte annexe ;
- thème avec ses références.

Le bloc `psaume + prière` est une vue composée. Le psaume et la prière restent deux enregistrements indépendants reliés par `appliesToPsalmId`, car tous les psaumes ne possèdent pas de prière.

## Architecture actuelle

### Sources documentaires

- `data/corpus/books/` — psaumes canoniques par livre ;
- `data/catalog.json` — catalogue des enregistrements ;
- PDF source et source packs dérivés.

### Sources éditoriales thématiques

- `data/thematic-index/books/book-XX.json` — relations canoniques par livre ;
- `data/incoherences.json` — décisions ou ambiguïtés éditoriales tracées.

### Sorties générées

- `data/browser-search-catalog.json` ;
- `data/thematic-index/theme-directory.json` ;
- `data/thematic-index/theme-search-index.json` ;
- `data/thematic-index/theme-connections.json` ;
- `data/thematic-index/theme-search-runtime.json`.

Ces sorties doivent être reconstruites par leurs scripts. **Aucune sortie générée ne doit être corrigée à la main.**

## Contrôles

Le pipeline et les audits doivent notamment garantir :

- couverture identique entre psaumes navigateur, analyses canoniques et index thématique ;
- absence de doublons `(psaume, thème)` ;
- présence des versets d’appui et des `teaching` ;
- conservation des alias ambigus ;
- séparation entre thème et occurrence textuelle ;
- recherche documentaire correcte des numéros répétés ;
- reproductibilité du bundle navigateur.

Le contrat opérationnel détaillé est dans `data/thematic-index/SEARCH-CONTRACT.md`.
