# Biblaw

Biblaw est une interface web légère de recherche et de navigation dans le corpus structuré de la **Bible essénienne (classée par livres)**.

Le projet combine :

- le corpus documentaire structuré des psaumes ;
- une indexation thématique éditoriale traçable vers les versets ;
- une recherche littérale de mots et d’expressions ;
- un accès direct par numéro de psaume ;
- une navigation transversale entre thèmes fondée sur leur cooccurrence dans les mêmes psaumes.

Site de production : `https://ludodulac.github.io/Biblaw/`

## Principes

Biblaw est un outil d’indexation et de recherche, pas un système d’interprétation définitive du corpus.

- les thèmes décrivent des relations éditoriales explicites et sourcées ;
- une occurrence de mot ne crée pas automatiquement un thème ;
- une cooccurrence entre thèmes ne signifie ni synonymie ni causalité ;
- plusieurs thèmes pouvant répondre au même alias restent explicitement distincts ;
- aucune source externe n’est utilisée pour enrichir le contenu sémantique du corpus.

Le contrat détaillé est dans `data/thematic-index/SEARCH-CONTRACT.md`.

## Recherche

### Par numéro de psaume

Saisir directement un entier positif, par exemple `105`, ou `psaume 105`.

Le moteur recherche le champ documentaire `number`. Plusieurs livres pouvant porter le même numéro, **toutes les correspondances** sont affichées au lieu d’en choisir une arbitrairement. Le filtre Archange reste applicable.

### Par thème

Le mode **Thèmes** résout uniquement :

1. les alias explicitement générés ;
2. les libellés ou identifiants canoniques exacts après normalisation.

Il n’existe pas de fallback thématique par simple sous-chaîne ou proximité lexicale.

Les résultats sont classés **Central → Important → Lié**, puis de façon déterministe. Les versets justificatifs et le champ contextuel `teaching` sont affichés avec les résultats.

### Par mots et phrases

Le mode **Mots et phrases** recherche une formulation littérale et contiguë dans le texte affiché du corpus. Il ne s’appuie pas sur les identifiants sémantiques pour fabriquer des occurrences textuelles.

Lorsqu’une même requête possède une lecture thématique et des occurrences littérales, l’interface garde les deux lectures séparées et permet de passer de l’une à l’autre.

## État canonique

Toujours considérer `data/thematic-index/validation-report.json` comme source courante des compteurs.

Au 7 septembre 2026, le pipeline validé contient :

- 44 livres ;
- 1158 analyses de psaumes ;
- 10409 relations thématiques ;
- 0 erreur ;
- 0 avertissement.

Le runtime de recherche contient 1251 thèmes, 1343 alias et 9 alias ambigus conservés explicitement.

## Architecture principale

### Corpus

- `data/corpus/books/` — psaumes canoniques structurés par livre ;
- `data/catalog.json` — catalogue documentaire ;
- `data/browser-search-catalog.json` — bundle compact utilisé par le navigateur.

Le bundle de production publie uniquement les psaumes canoniques sous `data/corpus/books/`. Les anciens fichiers de psaumes conservés sous `data/corpus/<archange>/` ne doivent pas être réintroduits dans la recherche navigateur.

### Index thématique

- `data/thematic-index/books/book-XX.json` — analyses canoniques par livre ;
- `data/thematic-index/theme-directory.json` — répertoire transversal généré ;
- `data/thematic-index/theme-search-index.json` — index d’alias généré ;
- `data/thematic-index/theme-connections.json` — graphe de cooccurrence ;
- `data/thematic-index/theme-search-runtime.json` — runtime compact ;
- `data/thematic-index/SEARCH-CONTRACT.md` — règles de recherche ;
- `data/incoherences.json` — registre des cas éditoriaux ambigus ou résolus.

### Interface

- `index.html`
- `css/biblaw.css`
- `js/biblaw.js`

### Pipeline et audits

- `scripts/run_canonical_thematic_pipeline.py`
- `scripts/build_browser_search_catalog.py`
- `scripts/audit_thematic_search_quality.py`
- `scripts/audit_production_search_queries.py`
- `scripts/audit_psalm_number_search.py`
- `scripts/audit_assembly_theme_context.py`

Les sorties générées doivent être modifiées par leurs générateurs, pas à la main.

## Validation

Les workflows GitHub Actions contrôlent notamment :

- l’intégrité de l’index canonique ;
- la reproductibilité du bundle navigateur ;
- la syntaxe du JavaScript ;
- le contrat de l’interface de recherche ;
- la séparation thème / texte ;
- la conservation des alias ambigus ;
- la recherche par numéro de psaume ;
- les requêtes de production de référence.

GitHub Pages publie le contenu de `main` après les mises à jour.

## Développement local

Le site est statique. Pour l’ouvrir localement avec les `fetch()` de données fonctionnels :

```bash
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000/`.

Ouvrir directement `index.html` avec le protocole `file://` peut empêcher le chargement des fichiers JSON selon les règles du navigateur.

## Reprise du projet

Avant une intervention importante, lire :

1. `progression/PASSATION-NOUVELLE-CONVERSATION.md` ;
2. les dernières notes dans `progression/` ;
3. `data/incoherences.json` ;
4. `data/thematic-index/validation-report.json` ;
5. `data/thematic-index/SEARCH-CONTRACT.md`.

Puis vérifier le HEAD de `main` et les workflows récents avant toute écriture.
