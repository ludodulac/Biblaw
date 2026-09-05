# Extension thématique des livres 27 à 44

Date : 2026-09-06

## Source et règle d'analyse

La seule source documentaire et doctrinale autorisée reste `Bible essénienne (classée par livres).pdf` et les données structurées qui en sont extraites dans le dépôt.

Aucun site internet, commentaire externe, autre édition, résumé, vidéo, podcast ou connaissance doctrinale extérieure ne doit confirmer, compléter ou corriger l'analyse. L'analyse thématique décrit aussi neutralement que possible ce que les textes présentent, associent, distinguent, prescrivent ou mettent en garde. Une inférence est admise uniquement lorsqu'elle repose sur le texte ; une ambiguïté réellement irréductible dans le PDF doit être inscrite dans `data/incoherences.json`.

Les prières restent liées aux psaumes mais ne sont pas utilisées comme matériau primaire de l'index thématique.

## Extension documentaire

Le pipeline documentaire couvre maintenant l'ensemble de l'édition : livres 1 à 44. Des chaînes distinctes extraient et valident 1-10, 11-20, 21-30, 31-40 et 41-44, puis reconstruisent les source packs thématiques.

Un résumé compact de `data/pilot/book-inventory.json` est généré dans `data/pilot/book-inventory-summary.json`. Il établit, uniquement à partir du PDF, que cette édition contient 44 livres numérotés de 1 à 44. Les quatre derniers sont :

- 41 — `La responsabilité d’un parent` ;
- 42 — `L’état ultime de la paix` ;
- 43 — `La guérison par les vertus` ;
- 44 — `L’énergie de l’argent`.

## Index thématique

Le pipeline canonique a été prolongé jusqu'au livre 44. Chaque relation thématique conserve ses versets d'appui et le contexte du livre reste une couche secondaire : il peut aider au classement et à l'explication, mais il ne peut pas fabriquer un thème absent du passage.

Après la première intégration des quatre livres finaux, `data/thematic-index/validation-report.json` a atteint :

- 44 livres ;
- 1 151 analyses de psaumes ;
- 9 647 relations thématiques ;
- aucune erreur ni aucun avertissement structurel.

Ce résultat est un jalon de couverture canonique, pas la fin de l'analyse sémantique. Les passes automatiques à grande échelle constituent une base reproductible. Elles doivent être suivies d'une passe sémantique plus profonde livre par livre afin d'identifier aussi les thèmes réellement enseignés sans occurrence lexicale directe, de préciser les lois et principes, les relations entre thèmes, les formulations fortes et l'importance relative des psaumes.

La couche `data/thematic-index/book-contexts.json` est également généralisée à tous les livres indexés. Les contextes générés restent secondaires par rapport aux preuves locales et peuvent être raffinés lors de la passe sémantique profonde.

## Numérotation éditoriale particulière découverte dans le PDF

L'audit PDF détaillé a montré qu'un titre de psaume n'est pas toujours suivi d'un redémarrage au verset 1. Dans plusieurs cas, le PDF imprime explicitement un nouveau numéro et un nouveau titre de psaume tout en poursuivant la numérotation des versets du texte précédent.

Cette particularité doit être préservée telle qu'elle apparaît dans le PDF. Elle ne doit ni être renumérotée artificiellement, ni être interprétée automatiquement comme une erreur. Un psaume de ce type porte désormais une indication structurée `sourceNumberingPreserved`, avec son premier numéro de verset imprimé.

Cas audités :

- livre 23, psaume 128 — `Ne sois pas un rêveur` : versets imprimés 49 à 82 ;
- livre 26, psaume 186 — `Que le désir d’apprendre soit plus grand que vos certitudes` : versets imprimés 23 à 50 ;
- livre 35, psaume 215 — `La clé magique pour attirer à soi ce que l’on souhaite` : versets imprimés 26 à 46 ;
- livre 36, psaume 217 — `Es-tu prêt à écouter le point de vue de la Lumière ?` : versets imprimés 16 à 40 ;
- livre 38, psaume 260 — `Tu n’éduqueras pas des enfants dans l’esclavage` : versets imprimés 23 à 54.

Ces cinq frontières ont été établies uniquement à partir du PDF grâce aux rapports détaillés de `data/pilot/missing-psalm-audits/`. Elles relèvent d'une réparation documentaire déterministe et ne nécessitent pas d'arbitrage doctrinal.

`scripts/repair_known_pdf_psalm_anomalies.py` reconstruit ces psaumes à leur titre explicite, conserve leur numérotation imprimée et retire du psaume précédent le texte qui avait été avalé par l'extracteur générique.

## Fin du livre 44 et textes annexes

Le psaume 285 du livre 44 avait absorbé après son verset 16 le début du `Témoignage de l'Ange de la Nation Essénienne`, puis d'autres textes annexes avec leurs propres numérotations. Cela créait de faux doublons et des versets hors ordre.

La frontière documentaire auditée est le début du titre `TÉMOIGNAGE DE L’ANGE` à l'intérieur de la fin extraite du verset 16. La réparation conserve les versets 1 à 16 du psaume et détache le reste de son corps principal. Le texte annexe n'est pas considéré comme perdu : le PDF demeure source d'autorité et une structuration propre des annexes sera effectuée dans la phase dédiée aux textes annexes.

## Garde-fous

- `scripts/sync_thematic_documentary_status.py` empêche de déclarer un livre thématiquement complet lorsque son corpus présente un psaume manquant ou une séquence réellement mal formée.
- Les séquences commençant au-dessus de 1 ne sont acceptées que lorsqu'elles sont explicitement marquées comme numérotation source auditée et qu'elles restent contiguës.
- Les corrections documentaires sont rejouables dans les workflows d'extraction concernés.
- Une anomalie technique déterministe ne doit pas remplir `data/incoherences.json`; seules les ambiguïtés réelles du PDF doivent y entrer.

## Suite

1. terminer et valider les réextractions qui appliquent les réparations auditées aux blocs 21-30, 31-40 et 41-44 ;
2. reconstruire les source packs et relancer l'index thématique après ces corrections documentaires ;
3. vérifier le nouvel état complet des 44 livres ;
4. lancer la passe sémantique profonde, livre par livre, sur l'ensemble des 44 livres ;
5. effectuer ensuite les synthèses transversales par thème et par Archange, toujours exclusivement à partir du PDF.
