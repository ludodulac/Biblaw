# Progression — livres 11 à 13 et fiabilisation du pipeline

Date : 2026-09-05

## État atteint

- Les livres 11 à 20 disposent d'un corpus extrait et de paquets source thématiques.
- Le livre 11, Raphaël — *Sortir de l'illusion*, est indexé thématiquement.
- Le livre 12, Ouriel — *Les clés du bonheur*, est indexé thématiquement.
- Le livre 13, Michaël — *Le lien avec les Anges*, est maintenant indexé sur ses 28 psaumes (77 à 104).
- Les prières restent hors de l'indexation thématique primaire.
- Les notes éditoriales sont utilisées comme contexte et synchronisées dans les analyses concernées.

## Lecture éditoriale du livre 13

Le livre 13 définit le lien avec les Anges comme une alliance réelle entre des êtres. Une vertu angélique est traitée comme un être vivant doté d'une évolution propre : elle ne doit être ni exploitée, ni oubliée, ni réduite à une expérience subjective. La possibilité d'une alliance dépend notamment de la fidélité, de la parole tenue, du respect, de la pureté, du discernement, de la stabilité et de la capacité à donner un corps concret à la vertu et à l'œuvre.

Le livre relie cette alliance à la relation avec la Mère et les règnes. La rupture avec les Anges est explicitement rapprochée de la séparation déjà produite par l'humanité avec les animaux, les végétaux, les minéraux et la Mère. Cette relation doit donc rester un axe transversal important lors des consolidations futures.

## Correction documentaire : notes continuées sur plusieurs pages

Un nouveau cas déterministe a été identifié dans Michaël 100 : une note éditoriale commençait en bas de la page PDF 822 et se poursuivait au début de la page 823. L'extracteur avait conservé le début dans l'objet note mais collé la continuation au verset 25.

La normalisation `scripts/normalize_notes_resumed_verses.py` a été étendue pour reconnaître les notes qui se poursuivent en tête de la page PDF suivante avant la reprise exacte des versets. Le fragment confirmé par la source est alors réuni à la note et retiré du verset s'il y a été recollé.

La note de Michaël 100 est rattachée éditorialement au verset 21, où se trouve son appel.

## Fiabilisation des workflows

Les workflows d'extraction 1–10 et 11–20 écrivaient parfois simultanément les mêmes répertoires générés. La validation pouvait réussir puis échouer uniquement au moment du `git push` à cause d'un commit concurrent.

Les deux workflows d'extraction partagent désormais un groupe de concurrence commun afin d'être exécutés séquentiellement.

Le répertoire thématique était également écrit à la fois par le workflow de validation thématique et par un workflow de construction séparé. Le workflow de construction automatique a été ramené à un déclenchement manuel ; la validation thématique reste le producteur normal du répertoire. Les écritures thématiques sont elles aussi sérialisées.

## Suite

1. Confirmer le nouveau run documentaire 11–20 et la matérialisation automatique de la note complète de Michaël 100.
2. Confirmer le rapport thématique avec le livre 13 inclus.
3. Continuer livre par livre à partir du livre 14, Gabriel, en conservant le même niveau d'analyse : titres et notes comme contexte, thèmes concrets et abstraits, passages probants, importance et enseignement.
4. Ne solliciter une validation humaine que lorsqu'une ambiguïté éditoriale ou sémantique réelle ne peut pas être résolue par la structure ou la source documentaire.
