# PASSATION BIBLAW — nouvelle conversation

> Ce fichier est le point d’entrée permanent pour reprendre Biblaw dans une nouvelle conversation sans casser le travail existant.
> Dernière consolidation : 2026-09-06.

## 1. Mission

Construire Biblaw comme une expertise structurée et interrogeable du corpus de la **Bible essénienne (classée par livres).pdf**, en particulier une indexation thématique riche, précise et réutilisable par le logiciel hors ligne.

La priorité actuelle est le **corpus et l’indexation thématique**. Le viewer PDF, les exports et les raffinements UI sont différés jusqu’à ce que le corpus thématique soit suffisamment consolidé.

## 2. Règle de source absolue

Pour toute donnée doctrinale, contextuelle, éditoriale ou thématique de Biblaw :

- source autoritative unique : `Bible essénienne (classée par livres).pdf` ;
- ne jamais utiliser de site essénien, moteur de recherche, vidéo, podcast, autre édition, commentaire externe ou mémoire générale pour enrichir, confirmer ou corriger le contenu ;
- si le PDF permet une réparation déterministe, la faire automatiquement ;
- si deux lectures de fond restent réellement plausibles à partir du PDF, ne pas trancher arbitrairement : enregistrer l’ambiguïté dans `data/incoherences.json` avec le contexte nécessaire à une décision humaine ultérieure.

Une recherche web éventuellement imposée par l’environnement ne doit jamais influencer l’analyse Biblaw.

## 3. Position d’analyse

L’analyse thématique doit être une **analyse neutre du corpus par l’assistant lui-même**, sans cadre interprétatif externe.

- distinguer preuve textuelle et inférence ;
- privilégier les passages explicites ;
- accepter un thème indirect lorsqu’il est réellement soutenu par le texte ;
- décrire : « le texte présente », « le psaume associe », « Gabriel enseigne dans ce passage », etc. ;
- ne pas présenter les affirmations internes du corpus comme des faits externes ;
- ne pas forcer une interprétation ambiguë.

La politique structurée correspondante se trouve dans `data/thematic-index/book-contexts.json` (`analysisPolicy`).

## 4. Définition large d’un thème

Un thème n’est pas seulement une abstraction doctrinale. Toute réalité significative du corpus peut être indexable : Assemblée, Feu, Chouette, eau, pierre, arbre, animal, Mère, Père, Ange, prière, temple, âme, mort, lumière, travail, nourriture, alliance, etc.

Ne pas fabriquer un dictionnaire de mots. Un thème est retenu lorsqu’il joue un rôle significatif dans le passage. Les occurrences lexicales directes et les passages décrivant clairement le concept sans employer son nom peuvent tous deux alimenter le thème.

Pour chaque relation thème ↔ psaume, préserver autant que possible :

- passages/versets d’appui ;
- enseignement précis du passage ;
- importance (`central`, `important`, `related`) ;
- nature de l’appui (`direct`, `symbolic`, `editorial`, `indirect`, `contextual`) ;
- principes, fonctions, conditions, dangers et relations avec d’autres thèmes lorsqu’ils sont réellement présents.

## 5. Méthode livre par livre

L’indexation finale se construit **livre par livre**, pas par simple balayage de mots.

Pour chaque livre :

1. lire le contexte éditorial disponible dans le PDF : titre du livre, Archange, titres des psaumes, notes éditoriales, ordre des textes et autres éléments pertinents ;
2. analyser chaque psaume à partir de son contenu ;
3. utiliser le titre comme indice contextuel, jamais comme preuve suffisante à lui seul ;
4. identifier tous les thèmes substantiels réellement enseignés ;
5. faire une seconde passe au niveau du livre pour comprendre les relations entre psaumes, les thèmes structurants et les nuances propres aux enseignements attribués à cet Archange dans ce livre ;
6. plus tard, faire une passe transversale entre livres/Archanges sans aplatir leurs différences.

Les prières restent liées aux psaumes mais **ne sont pas actuellement une source primaire d’indexation thématique**.

## 6. Architecture à préserver

- `data/` = source éditoriale structurée de vérité pour le logiciel.
- PDF = source documentaire autoritative.
- `data/corpus/books/book-XX/` = corpus extrait/normalisé.
- `data/notes/books/` = notes éditoriales structurées.
- `data/prayers/` = prières séparées mais reliées.
- `data/thematic-index/books/book-XX.json` = index thématique canonique par livre.
- `data/thematic-index/theme-directory.json` = index transversal généré ; ne pas le corriger à la main.
- `data/thematic-index/book-contexts.json` = couche contextuelle de livre, PDF-only et neutre.
- `data/thematic-index/source-packs/` = matériaux PDF structurés servant aux passes thématiques.
- `data/incoherences.json` = registre permanent des ambiguïtés réelles nécessitant éventuellement un humain.
- `progression/` = journal durable des décisions, méthodes et étapes. Toute décision méthodologique importante doit y être écrite.

Ne pas supprimer les données validées existantes pour « repartir de zéro ». Lorsqu’une méthode antérieure est devenue un prototype, conserver ce qui est utile et remplacer progressivement la couche canonique.

## 7. Validation humaine vs machine

Ne jamais confondre :

- `validated` : comparé au PDF par une personne ;
- `machine-validated` : régénéré depuis le PDF et ayant passé les contrôles automatiques.

Le psaume 105 historiquement validé par humain doit rester une référence et ne doit pas être rétrogradé sémantiquement.

## 8. État général atteint

L’inventaire dérivé du PDF établit **44 livres** dans cette édition.

Une première couverture thématique automatisée existe désormais pour les 44 livres. Le dernier état observé avant cette passation avait atteint environ **1 151 psaumes** et **9 647 relations thématiques**. Ces nombres sont un état de travail, pas une garantie à recopier aveuglément : au début d’une nouvelle conversation, relire les rapports courants dans le dépôt avant de citer des chiffres.

Les livres 1–17 ont fait l’objet de passes livre-par-livre antérieures plus éditoriales. Le livre 18 est la cible de départ de la **passe sémantique profonde** qui remplace progressivement les relations lexicales/génériques par des enseignements précis et contextualisés.

Le livre 18 est Gabriel, `Quel chercheur de Lumière es-tu ?`, psaumes 111–137. Une passe approfondie a commencé notamment sur les psaumes 123, 124, 127, 128 et 131. Continuer cette amélioration à partir du contenu PDF/source packs, puis poursuivre livre après livre.

## 9. Dette documentaire connue à vérifier en premier

Des anomalies de découpage PDF ont été auditées sur :

- livre 23 / psaume 128 ;
- livre 26 / psaume 186 ;
- livre 35 / psaume 215 ;
- livre 36 / psaume 217 ;
- livre 38 / psaume 260 ;
- livre 44 / psaume 285.

Découverte importante : certains titres de nouveaux psaumes sont imprimés dans le PDF **sans que la numérotation des versets reparte à 1**. Il faut préserver la numérotation réellement imprimée et ne pas inventer un verset 1. Le réparateur `scripts/repair_known_pdf_psalm_anomalies.py` est destiné à gérer ces cas de façon auditée.

Pour le livre 23 / psaume 128, le PDF montre un début source numéroté 49 et la réparation a déjà identifié une plage 49–76.

Pour le livre 44 / psaume 285, l’extraction avait absorbé du matériau annexe après la fin réelle du psaume. La logique de réparation doit séparer le psaume du témoignage/annexe sans perdre le texte.

**Avant de modifier quoi que ce soit**, vérifier l’état actuel des workflows et des rapports : des runs étaient encore en cours ou en reprise lors de la création de cette passation.

## 10. Workflows / pipeline documentaire

Les extractions sont découpées par blocs et partagent volontairement un groupe de concurrence afin d’éviter des écritures simultanées incompatibles. Une limite GitHub observée est qu’un nouveau run pending peut remplacer un autre run pending du même groupe. Par conséquent, pour les grosses réparations, déclencher/laisser finir les blocs **séquentiellement**.

Blocs concernés notamment :

- `.github/workflows/extract-books-21-30.yml`
- `.github/workflows/extract-books-31-40.yml`
- `.github/workflows/extract-books-41-44.yml`

Pipeline typique : extraction → normalisation notes → réparations auditées → titres → structures intégrées → anomalies PDF connues → validation → source packs → commit.

Un normaliseur de titres mis en cache/scopé a été ajouté pour éviter de rouvrir le PDF page par page pour tout le corpus. Ne pas revenir à un traitement global lent si un bloc borné suffit.

## 11. Scripts importants

Parmi les scripts à préserver/comprendre avant modification :

- `scripts/inventory_books.py`
- `scripts/extract_books_01_10.py` et wrappers des blocs suivants
- `scripts/normalize_notes_resumed_verses.py`
- `scripts/repair_audited_inline_note_splits.py`
- `scripts/normalize_wrapped_psalm_titles.py`
- `scripts/normalize_wrapped_psalm_titles_cached.py` (optimisation/scoping récent)
- `scripts/normalize_embedded_psalm_headings.py`
- `scripts/normalize_embedded_psalm_structures.py`
- `scripts/repair_known_pdf_psalm_anomalies.py`
- `scripts/build_thematic_source_packs.py`
- `scripts/validate_thematic_index.py`
- `scripts/build_thematic_directory.py`
- `scripts/normalize_thematic_metadata.py`

Ne pas modifier un fichier généré à la main lorsque son script générateur peut être corrigé.

## 12. Règle de travail autonome

Le propriétaire du projet veut que l’assistant **avance réellement** lorsqu’il dit « continue », « vas-y », « fais-le ».

- ne pas demander validation psaume par psaume ;
- résoudre automatiquement les bugs techniques déterministes ;
- si un test révèle une erreur systématique, corriger la règle/pipeline pour propager la correction ;
- ne remonter à l’utilisateur que les vraies ambiguïtés éditoriales/sémantiques ou une décision produit réellement nécessaire ;
- aller aussi loin que possible avant de demander son intervention.

## 13. Procédure obligatoire au début d’une nouvelle conversation

Ne jamais reprendre uniquement à partir de ce document. Il donne la carte ; **le dépôt donne l’état courant**.

Ordre recommandé :

1. ouvrir ce fichier ;
2. lire `progression/README.md` et les dernières entrées de `progression/` pertinentes ;
3. lire `data/incoherences.json` ;
4. lire les rapports de validation/extraction les plus récents dans `data/pilot/` et `data/thematic-index/validation-report.json` ;
5. vérifier les workflows GitHub en cours/échoués liés aux derniers commits avant de lancer une nouvelle extraction ;
6. re-fetch immédiatement tout fichier avant modification et utiliser son SHA courant ;
7. ne jamais supposer qu’un SHA ou un nombre mentionné dans cette passation est encore courant ;
8. terminer d’abord les réparations documentaires en vol, puis reconstruire/valider les index générés ;
9. reprendre ensuite la passe sémantique profonde à partir du livre 18 et progresser livre par livre ;
10. écrire toute nouvelle décision méthodologique importante dans `progression/`.

## 14. Définition de « fini » pour un livre

Un livre ne doit être présenté comme réellement terminé que si :

- son corpus PDF est structurellement cohérent ou ses particularités source sont explicitement documentées ;
- tous ses psaumes attendus sont présents ;
- titres et notes utiles sont reliés ;
- les thèmes ne reposent pas seulement sur les titres ou des mots-clés ;
- les relations importantes ont des versets d’appui et un enseignement précis ;
- la synthèse du livre est descriptive, neutre et dérivée du PDF ;
- le contexte de livre n’invente aucun thème absent des psaumes ;
- le validateur thématique passe ;
- les ambiguïtés réelles restantes sont dans `data/incoherences.json`.

## 15. Prochaine séquence recommandée

1. Vérifier et terminer les runs documentaires 21–30, 31–40 et 41–44, séquentiellement.
2. Vérifier que les six anomalies listées plus haut sont correctement réparées/documentées et que les rapports documentaires passent.
3. Régénérer les source packs et l’index thématique ; vérifier le rapport de validation courant.
4. Terminer la passe sémantique profonde du livre 18 à partir des psaumes/source packs, sans source externe.
5. Mettre à jour son `bookSynthesis` et son entrée de `book-contexts.json` seulement à partir de la passe complète.
6. Continuer les livres 19, 20, etc. avec la même profondeur.
7. Après les 44 livres, lancer une consolidation transversale thème par thème et une révision des pages/thèmes du logiciel.

## 16. Principe de sécurité du travail

Quand l’état du dépôt et ce document semblent se contredire : **ne pas écraser le dépôt pour faire correspondre la passation**. Examiner l’historique, les rapports et les générateurs, puis conserver la version la plus récente et démontrablement correcte.

Le but de cette passation n’est pas de figer Biblaw : c’est de permettre à la prochaine conversation de reprendre immédiatement, avec les mêmes contraintes méthodologiques, sans perdre les décisions acquises ni casser les données déjà produites.
