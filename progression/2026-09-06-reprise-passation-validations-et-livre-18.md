# Reprise de passation — validations documentaires et passe profonde du livre 18

Date : 2026-09-06

## Périmètre et règles conservées

- `progression/PASSATION-NOUVELLE-CONVERSATION.md` a été relu avant intervention.
- Le PDF reste l’unique source de vérité pour le contenu éditorial, doctrinal, contextuel et thématique.
- Aucun contenu externe n’a été utilisé pour la passe sémantique.
- `main` est la cible courante ; aucun changement n’a été fait sur une ancienne branche ou une page de test.
- Les corrections ont été limitées aux données dérivées ou scripts concernés, sans réextraire ni écraser le corpus validé.

## Validation documentaire 41–44

Le rapport `data/pilot/books-41-44-validation-report.json` était devenu obsolète après son run initial : un run ultérieur d’un autre bloc avait réappliqué le réparateur partagé et corrigé `book-44/psalm-285.json` en détachant l’annexe finale après le verset 16.

Le corpus courant du psaume 285 du livre 44 était donc déjà correct (pages 4636–4637, versets 1–16, marqueur d’audit de détachement de l’annexe), tandis que le rapport 41–44 conservait encore l’ancien diagnostic. Le rapport dérivé a été rafraîchi sans toucher au corpus. Les livres 41 à 44 sont maintenant signalés sans psaume manquant ni séquence de versets invalide.

## Passe sémantique profonde du livre 18

Le script `scripts/deepen_book18_semantic.py` existait déjà pour les psaumes 123, 124, 127, 128 et 131, mais le workflow de validation thématique ne l’exécutait pas. Cela préservait les analyses profondes déjà présentes grâce au générateur canonique 18–20, mais les enrichissements futurs du script n’étaient pas reproductibles automatiquement.

Le workflow `.github/workflows/validate-thematic-index.yml` a donc été ajusté de façon minimale :

1. `scripts/deepen_book18_semantic.py` fait désormais partie des chemins déclencheurs ;
2. la passe profonde est exécutée juste après `scripts/complete_books18_20_thematic.py`, avant synchronisation documentaire, normalisation, contexte, validation et reconstruction du répertoire thématique.

Les psaumes 125 et 126 ont été lus depuis le source pack PDF-only et ajoutés à la passe profonde :

- psaume 125 : préparation, temple, monde divin, pureté, lois, espace sacré, libération, Mère, nature, Alliance, discipline ;
- psaume 126 : œil, eau, regard, destinée, sagesse, apparences, influences, éducation du regard, Mère comme modèle symbolique, Bien, espoir.

Un premier run a révélé une ancienne référence invalide dans l’analyse profonde du psaume 127 : le thème `eau` citait les versets 29–30 alors que le corpus courant s’arrête au verset 20. La correction a été faite uniquement dans le générateur profond, en conservant les références réellement présentes (3, 6, 7, 8, 10, 14, 15).

Après correction, le workflow complet passe : génération canonique, passe profonde, synchronisation documentaire, normalisation, construction des contextes, validation thématique et reconstruction du répertoire.

État validé après ce run :

- 44 livres ;
- 1 156 analyses de psaumes ;
- 9 739 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

## Suite immédiate préparée

La lecture PDF-only a été poursuivie sur les psaumes 129 et 130, sans encore les déclarer terminés dans la passe profonde.

Axes déjà identifiés pour la prochaine écriture ciblée :

- psaume 129, « Nutrition et digestion: les cycles de construction du corps subtil » : constitution d’un corps correspondant à ce que l’on veut recevoir, nutrition au sens physique et subtil, activité créatrice quotidienne, digestion nocturne, sommeil, destinée, déchets subtils, protection par une tradition vivante, concentration sur l’essentiel et maîtrise de la vie ;
- psaume 130, « Qu’est-ce que la mort ? » : reconnaissance envers la Mère et les règnes, distinction entre partie mortelle et partie immortelle, attachement au corps et aux biens, générosité et don comme chemin de vie, construction d’un corps supérieur par les actes, mort présentée dans le texte comme conséquence, responsabilité, générations futures et œuvre concrète de Lumière.

Le livre 18 reste en passe sémantique profonde en cours. Sa synthèse de livre ne doit être considérée comme finalisée qu’après lecture profonde de l’ensemble des psaumes restant à auditer.