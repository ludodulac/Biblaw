# Contrat de recherche thématique Biblaw

Ce document décrit comment les données de `data/thematic-index/` doivent être utilisées par le moteur de recherche du site. Il ne constitue pas une interprétation doctrinale des Psaumes.

## Principe général

Biblaw distingue trois intentions de recherche qui ne doivent pas être mélangées :

1. **accès documentaire par numéro de psaume** : retrouver le ou les psaumes portant exactement ce numéro ;
2. **recherche thématique** : retrouver les psaumes reliés à un thème éditorial canonique ;
3. **recherche textuelle** : retrouver les endroits où un mot ou une expression apparaît littéralement dans le corpus.

Aucune de ces lectures ne doit fabriquer les résultats d'une autre. Une occurrence textuelle ne crée pas un thème ; un thème indexé ne crée pas une occurrence littérale ; un numéro de psaume n'est ni un mot-clé ni un thème.

L’indexation sert à repérer, classer et relier des passages pour la recherche. Les Psaumes peuvent porter plusieurs niveaux de lecture. Un thème, un classement ou une connexion ne doit donc jamais être présenté comme une explication exhaustive, exclusive ou définitive du texte.

Les affirmations contenues dans les champs `teaching` décrivent ce qui est relevé dans le corpus pour faciliter la recherche. Elles restent des formulations d’indexation liées aux versets cités.

## Accès documentaire par numéro

Une requête composée uniquement d'un entier positif, avec ou sans le préfixe `psaume` (par exemple `105` ou `psaume 105`), est interprétée comme une recherche documentaire de numéro.

- le numéro doit correspondre exactement au champ `number` du psaume ;
- plusieurs livres peuvent contenir le même numéro : le moteur doit alors afficher **toutes** les correspondances, sans en choisir une arbitrairement ;
- les résultats sont distingués par leur Archange, leur livre, leur titre et leur référence documentaire ;
- le filtre Archange reste applicable ;
- une formulation contenant d'autres mots (`22 commandements`, par exemple) ne doit pas être requalifiée en recherche par numéro.

Cette recherche ne modifie aucune donnée thématique.

## Sources dérivées

### `theme-directory.json`

Répertoire global dérivé des analyses livre par livre.

- un `themeId` désigne une entrée thématique éditoriale ;
- `label` est le libellé d’affichage canonique dérivé de l’usage observé ;
- `labelVariants` conserve les autres libellés réellement présents pour ce même identifiant ;
- `topPsalms` classe les occurrences par importance éditoriale (`central`, `important`, `related`) ;
- les répartitions par Archange sont des facettes de navigation, pas des équivalences d’enseignement.

Le fichier est généré et ne doit pas être modifié à la main.

### `theme-search-index.json`

Couche d’alias destinée à améliorer le rappel de recherche sans faire de rapprochement sémantique implicite.

- les accents, apostrophes, ponctuations et variantes de libellés sont normalisés pour la recherche ;
- plusieurs `themeId` peuvent volontairement répondre au même alias ;
- `ambiguous: true` signifie précisément que le moteur doit conserver plusieurs résultats possibles ;
- `semanticMerging: false` interdit d’interpréter un alias partagé comme une identité sémantique.

Le moteur ne doit jamais fusionner automatiquement deux thèmes simplement parce que leurs libellés se ressemblent.

### `theme-connections.json`

Graphe de navigation entre thèmes calculé à partir de leur présence commune dans les mêmes Psaumes.

- `relationshipType: psalm-cooccurrence` est la seule signification garantie ;
- `semanticClaim: false` signifie qu’une arête ne prouve ni synonymie, ni causalité, ni accord doctrinal ;
- le `score` sert uniquement à classer les cooccurrences répétées ou fortes ;
- `topSharedPsalms` permet toujours de revenir aux passages qui justifient la connexion de navigation.

Une connexion affichée dans le site devrait être formulée comme « thèmes également présents dans ces Psaumes » ou « thèmes fréquemment associés dans l’index », jamais comme « ce thème signifie » ou « ce thème est équivalent à ».

## Résolution d'une recherche thématique

Le moteur applique uniquement la séquence suivante :

1. normaliser la requête comme la couche d'alias ;
2. essayer les formes de requête autorisées, notamment la neutralisation d'un article initial français ;
3. résoudre un **alias explicitement présent** dans le runtime ;
4. à défaut, accepter un **libellé canonique ou un identifiant canonique exact** après normalisation ;
5. à défaut, ne retourner **aucun thème**.

Il n'existe pas de fallback thématique par sous-chaîne, proximité lexicale ou ressemblance de libellé. Une requête thématique non résolue peut proposer séparément la recherche textuelle si des occurrences littérales existent.

Pour les résultats thématiques :

- conserver tous les identifiants lorsqu'un alias est explicitement ambigu ;
- classer les Psaumes selon l’importance éditoriale `Central → Important → Lié`, puis de manière déterministe ;
- permettre le filtrage par Archange ;
- afficher les versets justificatifs et le champ `teaching` avec chaque résultat ;
- proposer les thèmes voisins uniquement comme navigation transversale fondée sur la cooccurrence ;
- permettre à l’utilisateur d’ouvrir le Psaume complet pour replacer chaque résultat dans son contexte.

Les résultats textuels ou thématiques ne doivent pas être reclassés selon la seule fréquence brute des mots lorsque l’analyse éditoriale fournit déjà un niveau d’importance.

## Exemple éditorial : « Assemblée » et « Sainte Assemblée »

`Sainte Assemblée` est un thème canonique distinct lorsqu'il est explicitement soutenu par les passages éditorialement retenus. La requête `sainte assemblée` peut donc résoudre ce thème.

`Assemblée` reste une formulation textuelle plus générale tant qu'aucun thème canonique générique distinct n'est établi. La requête `assemblée` ne doit donc pas être redirigée vers `Sainte Assemblée` par simple inclusion lexicale.

La neutralisation de l'article (`la sainte assemblée` → `sainte assemblée`, `l'assemblée` → `assemblée`) est une commodité de requête seulement ; elle ne fusionne pas les deux concepts.

## Ce qui ne doit pas être fait automatiquement

- fusionner des thèmes sur la seule base de la proximité lexicale ;
- résoudre un thème par simple inclusion de chaîne ou voisinage de mots ;
- créer un thème parce qu'un mot apparaît fréquemment dans le corpus ;
- supprimer un thème parce qu’il n’apparaît que dans un seul Psaume ;
- considérer un thème composite comme une erreur sans relecture du corpus ;
- transformer une cooccurrence en relation doctrinale ;
- présenter une synthèse de livre comme le sens unique du livre ;
- indexer les prières comme source thématique primaire dans cette couche ;
- utiliser une source externe pour compléter le contenu doctrinal ou symbolique du corpus.

## Contrôles

- `validation-report.json` contrôle l’intégrité de l’index thématique principal ;
- `theme-quality-audit.json` recense les situations de fragmentation ou de libellés à examiner sans les corriger automatiquement ;
- `validate_thematic_search_index.py` contrôle la couche d’alias ;
- `validate_thematic_connections.py` contrôle le graphe de cooccurrence ;
- `audit_production_search_queries.py` vérifie les requêtes de production et la séparation thème/texte ;
- `audit_psalm_number_search.py` vérifie la recherche documentaire par numéro.

Toute consolidation éditoriale ultérieure doit rester traçable vers les Psaumes et versets concernés.
