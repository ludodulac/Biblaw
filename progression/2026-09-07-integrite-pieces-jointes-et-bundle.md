# Biblaw — intégrité des prières, notes et bundle navigateur

Date : 2026-09-07

## But

Fiabiliser les rattachements documentaires autour des psaumes sans introduire d'interprétation sémantique. Les corrections de cette étape portent uniquement sur les identifiants, les liens réciproques et la synchronisation entre sources canoniques et bundle navigateur.

## État validé

L'audit permanent `scripts/audit_corpus_attachments.py` vérifie actuellement :

- **1158 psaumes canoniques** sous `data/corpus/books/` ;
- **676 prières** cataloguées ;
- **676 cibles de prière distinctes** ;
- **11 notes externes** cataloguées ;
- **11 cibles de note distinctes** ;
- **265 `noteIds` internes/éditoriaux** présents dans les psaumes sans fichier `data/notes/*.json` autonome ;
- **1 renvoi croisé de note vers un psaume**, désormais canonique ;
- **1845 enregistrements** dans le bundle navigateur ;
- **31 anciens psaumes legacy** conservés historiquement mais exclus du bundle de production.

## Migrations effectuées

Les anciens rattachements `michael-psalm-*` présents dans des prières et notes ont été remplacés uniquement lorsque la correspondance canonique était démontrée par les données internes : Archange, numéro, livre lorsqu'il est explicite, document source, pages qui se chevauchent ou se suivent immédiatement, et lien réciproque quand le modèle le fournit.

Résultat de la migration déterministe :

- 24 cibles de prières de Michaël ont été canonicalisées ;
- 8 psaumes ont récupéré un `prayerIds` réciproque manquant ;
- 11 notes externes sont maintenant nommées et rattachées avec des IDs `book-XX-psalm-NNN` ;
- le cas `book-21-psalm-143-note-002` a été rattaché au psaume 143 du livre 21 à partir du lien réciproque canonique et de la continuité des pages 1652–1654 ;
- son renvoi `michael-psalm-026` a été remplacé par `book-05-psalm-026` après comparaison interne : même livre 5, même Michaël, même numéro 26, même titre, mêmes pages 251–252 et même texte.

Le script et le workflow temporaires de migration ont ensuite été supprimés. Il ne reste qu'un audit permanent en lecture seule.

## Contrat permanent

Une prière externe doit :

- avoir un ID unique ;
- cibler un psaume canonique existant ;
- avoir le même Archange et le même livre ;
- être déclarée réciproquement dans `prayerIds` ;
- être reliée au même document source avec pages superposées ou immédiatement adjacentes.

Une note externe doit :

- avoir un ID unique ;
- cibler un psaume canonique existant ;
- avoir le même Archange ;
- être déclarée réciproquement dans `noteIds` ;
- être reliée au même document source avec pages superposées ou immédiatement adjacentes ;
- référencer un verset existant lorsqu'un numéro de verset est fourni.

Les `noteIds` internes aux psaumes ne sont pas assimilés automatiquement à des notes externes : beaucoup représentent des notes éditoriales incorporées au corpus et n'ont volontairement aucun enregistrement autonome.

Tout `crossReferences` qui ressemble à un ID de psaume doit utiliser un ID canonique `book-XX-psalm-NNN` existant. Aucun numéro seul n'est résolu automatiquement, car de nombreux numéros de psaume sont répétés dans plusieurs livres.

## Synchronisation navigateur

Le workflow `.github/workflows/rebuild-browser-search-catalog.yml` surveille maintenant aussi `data/notes/**` et `data/prayers/**`.

L'audit compare les objets sources et les objets réellement publiés dans `data/browser-search-catalog.json` par égalité complète pour :

- les 1158 psaumes canoniques ;
- les 676 prières ;
- les 11 notes externes.

Ainsi, une source corrigée avec un bundle navigateur périmé fait échouer la validation.

## Règle de reprise

Ne pas reconstruire de lien prière/note/renvoi à partir du numéro du psaume seul. Utiliser les preuves documentaires internes au corpus et échouer explicitement si plusieurs candidats restent possibles.
