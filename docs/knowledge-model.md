# Modèle de connaissance Biblaw

L'application finale doit fonctionner sans intelligence artificielle connectée.
Elle s'appuie sur un corpus vérifié, un index construit à l'avance et des dossiers
thématiques éditoriaux qui s'enrichissent progressivement.

## Quatre objets à ne pas confondre

1. **Terme** : forme tapée par la personne, par exemple `chouette`.
2. **Sens** : signification proposée pour lever une ambiguïté, par exemple animal,
   symbole de vision ou animal totémique associé à Michaël.
3. **Thème** : sujet transversal, par exemple vision, discernement ou
   transformation des imperfections.
4. **Référence** : preuve exacte dans un psaume, un verset, une prière, une note,
   une introduction ou une annexe.

Une interprétation ou une synthèse ne remplace jamais la référence source.

## Deux formes de dialogue observées dans le PDF

Le corpus emploie au moins deux formes qu'il faut conserver :

- la question d'Olivier Manitara porte elle-même un numéro de verset ;
- une phrase éditoriale comme `Olivier Manitara demanda alors à l'Archange`
  introduit une question non numérotée entre deux versets, puis la numérotation de
  la réponse de l'Archange reprend.

Les questions ne doivent donc pas être forcées dans la liste des versets. Le champ
`dialogueSegments` mémorise leur position, leur locuteur, leur éventuel numéro de
verset et la formule éditoriale qui permet d'identifier le locuteur.

## Dossier thématique évolutif

Un fichier de thème est un dossier éditorial révisable. Il commence par une liste
d'occurrences puis peut devenir un « puits de réponses » contenant :

- une présentation générale ;
- des sous-thèmes ;
- des significations et ambiguïtés déjà arbitrées ;
- des principes, lois, conseils et pratiques ;
- des questions fréquentes et réponses préparées ;
- les références exactes justifiant chaque élément ;
- un état de validation et un historique de révision.

## Parcours de recherche hors ligne

1. La personne saisit un terme ou une expression.
2. L'outil normalise l'orthographe et propose les termes proches.
3. S'il existe plusieurs sens, il présente d'abord un écran de désambiguïsation.
4. La personne choisit un ou plusieurs sens et sous-thèmes.
5. Elle filtre les sources : psaumes, prières, notes, introductions, annexes ou
   autres textes.
6. L'outil affiche les occurrences, les versets et les dossiers thématiques.
7. La personne sélectionne les éléments à consulter ou à exporter.

## Unités consultables et exportables

- verset seul ;
- sélection de versets ;
- psaume complet ;
- prière seule ;
- bloc canonique `psaume + prière rattachée` ;
- note ou texte annexe ;
- dossier thématique avec ses références.

Le bloc `psaume + prière` est une vue composée. Le psaume et la prière restent
deux enregistrements indépendants reliés par `appliesToPsalmId`, car tous les
psaumes ne possèdent pas de prière.

## Formats de sortie prévus

- lecture à l'écran ;
- page imprimable ;
- téléchargement texte ;
- téléchargement JSON pour les données ;
- PDF généré à partir d'une sélection ;
- lien interne stable vers chaque psaume, verset, prière ou thème.

## Architecture de construction

Les JSON de `data/` sont la source éditoriale. Les fichiers de `dist/` seront
reconstruits automatiquement : index des mots, index des expressions, index des
thèmes, relations et vues composées. Aucun index généré ne doit être corrigé à la
main.
