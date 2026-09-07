# Audit des contrats et frontières de production — 2026-09-07

## Portée

Cette passe a commencé par un diagnostic de `main`, des workflows, du pipeline canonique, de `SEARCH-CONTRACT.md`, du rapport de validation, des fichiers de passation, des commits récents et des tests existants. Aucun enrichissement sémantique externe n’a été utilisé.

Le dépôt n’a actuellement qu’une branche Git active, `main`, et aucun PR. Les expérimentations historiques pertinentes sont donc distinguées par leurs chemins et leur rôle dans `main`, notamment le pilote d’extraction du livre 17 et les anciens psaumes `data/corpus/<archange>/...`.

## Défauts génériques trouvés et corrigés

### 1. Publication Pages insuffisamment conditionnée

Un même HEAD pouvait auparavant avoir un audit d’intégrité canonique rouge et être malgré tout déployé par Pages, car le workflow public ne vérifiait que deux contrats UI.

La publication vérifie désormais avant déploiement :

- contrat UI public ;
- annuaire thématique public ;
- runtime thématique ;
- intégrité prières/notes et fraîcheur du bundle ;
- indépendance des identifiants historiques ;
- requêtes de production de référence ;
- recherche documentaire par numéro.

Un HEAD incohérent est donc refusé avant upload/déploiement.

### 2. Pilote livre 17 écrivant dans des données partagées de production

Le pilote `extract_book17.py` conserve volontairement ses anciens identifiants `michael-psalm-*` et ses fichiers historiques. Il n’a pas été supprimé ni converti artificiellement en source canonique.

Une frontière explicite a été ajoutée avec `normalize_book17_production_attachments.py` :

- les cibles des prières partagées sont normalisées vers les identités canoniques `book-17-psalm-*` ;
- les notes extraites sont copiées sous leurs identités canoniques pour la production ;
- les fichiers de notes legacy restent conservés comme artefacts historiques mais sont retirés du catalogue de production ;
- le bundle navigateur est reconstruit après cette frontière.

Le workflow livre 17 ne se déclenche plus sur tout `data/**` et utilise `checkout@v6`.

### 3. Réparations PDF effaçant des métadonnées d’attachement

Les réparateurs de psaumes aux frontières documentaires connues reconstruisaient certains objets et perdaient leurs `prayerIds`.

La réparation générique et le réparateur spécifique du livre 32 restaurent désormais une réciproque uniquement lorsqu’une prière existante déclare explicitement `appliesToPsalmId` égal à l’identité canonique exacte du psaume. Aucun rattachement n’est inféré par numéro, proximité ou contenu lexical.

### 4. Pipeline validant des fichiers qu’il ne publiait pas

Le pipeline canonique pouvait normaliser et auditer prières/notes dans son workspace, puis ne pas inclure ces fichiers dans son commit bot.

Le workflow `validate-thematic-index.yml` publie désormais les mêmes catégories de données auditées : corpus documentaire réparé, prières, notes, catalogue, sorties thématiques et bundle navigateur.

## Runtime : candidat validé avant remplacement

`build_thematic_search_runtime.py` ne remplace plus directement le runtime public.

Ordre actuel :

1. construire un fichier candidat ;
2. comparer exactement ses alias avec la projection du `theme-search-index.json` validé ;
3. comparer exactement ses voisins avec la projection du graphe `psalm-cooccurrence` validé ;
4. vérifier `semanticMerging: false`, les ambiguïtés et les identités thématiques ;
5. remplacer atomiquement le runtime public seulement si le candidat est valide ;
6. revalider indépendamment le runtime commité dans le pipeline et avant Pages.

Le runtime reste une projection de navigation. Il ne crée aucune identité ou relation sémantique.

## Validité puis ranking

`SEARCH-CONTRACT.md` formalise désormais deux étapes distinctes :

1. une relation thème–psaume doit être admise dans l’index canonique et validée ;
2. seulement ensuite `central`, `important`, `related` et l’ordre déterministe peuvent classer les résultats.

Un score, une fréquence, une proximité lexicale, une sous-chaîne ou une cooccurrence ne peut jamais créer ou admettre une relation thématique.

## Idées évaluées mais non ajoutées

### `confidence` / `unknown` généralisés

Non retenus à ce stade. Les relations thématiques canoniques disposent déjà de champs plus précis : `directness`, versets justificatifs, `teaching`, `importance` et validation. Ajouter une probabilité générique créerait une incertitude artificielle ou dupliquerait ces statuts. Les vraies ambiguïtés éditoriales restent traçables dans `data/incoherences.json`.

### Nouveau champ de « niveau de garantie »

Non retenu comme champ persistant. Les distinctions nécessaires existent déjà dans le modèle : occurrence littérale, relation éditorialement indexée, identité canonique, alias ambigu et connexion de cooccurrence avec `semanticClaim: false`. `SEARCH-CONTRACT.md` les rend maintenant explicites sans dupliquer les données.

### Manifest `implemented/tested/verified`

Non retenu. Les requêtes de référence ont déjà des audits exécutables, et leur vérification avant Pages apporte une garantie plus forte qu’un statut manuel susceptible de devenir périmé.

### Lazy loading / progressive disclosure supplémentaires

Aucun changement ajouté faute de problème mesuré. L’annuaire thématique possède déjà un rendu progressif/lazy protégé par `audit_theme_directory_ui.py`. Le bundle de recherche reste de taille maîtrisée et aucun profil de performance ne justifie encore une nouvelle architecture de chargement.

### Personnalisation / visibilité

Aucune infrastructure ajoutée : aucun parcours personnalisé n’existe actuellement. Si cette fonctionnalité apparaît plus tard, la règle est de conserver un corpus canonique unique et de gérer séparément la visibilité/préférence, sans dupliquer le contenu.

## État vérifié en fin de passe

Le pipeline canonique complet a réussi après correction des frontières de production et a publié ses sorties auditées. Un commit humain ultérieur a déclenché Pages sur cet état réparé : runtime, intégrité documentaire, indépendance des identifiants historiques, requêtes de référence et recherche par numéro ont tous passé avant le déploiement GitHub Pages, qui a réussi.

Les artefacts historiques sont conservés ; ils ne sont simplement plus confondus avec les dépendances de production.
