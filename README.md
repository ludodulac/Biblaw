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

## État courant

Les nombres courants ne sont volontairement pas recopiés ici :

- `data/thematic-index/validation-report.json` est la source des compteurs canoniques, erreurs et avertissements ;
- `data/thematic-index/theme-search-runtime.json` porte les compteurs de thèmes, alias et ambiguïtés du runtime ;
- `data/thematic-index/theme-quality-audit.json` porte les contrôles de fragmentation/qualité de recherche.

Cela évite qu’une documentation manuelle devienne plus ancienne que les artefacts réellement validés.

## Architecture principale

### Corpus

- `data/corpus/books/` — psaumes canoniques structurés par livre ;
- `data/catalog.json` — catalogue documentaire ;
- `data/browser-search-catalog.json` — bundle utilisé par le navigateur.

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
- `css/theme-index.css`
- `js/biblaw.js`

Les sorties générées doivent être modifiées par leurs sources ou générateurs, pas à la main.

## Développement et validation

Le point d’entrée rapide pour une nouvelle conversation ou une intervention ciblée est :

`AI_START_HERE.md`

Les validations proportionnées sont regroupées sans remplacer les audits existants :

```bash
python scripts/check_biblaw.py FAST --area search
python scripts/check_biblaw.py TARGETED --area thematic
python scripts/check_biblaw.py FULL
```

Pour voir rapidement ce qu’une modification a changé dans les artefacts et les requêtes sentinelles :

```bash
python scripts/report_biblaw_diff.py
```

Après un commit, comparer au parent avec :

```bash
python scripts/report_biblaw_diff.py --base HEAD~1
```

Le pipeline canonique complet reste `scripts/run_canonical_thematic_pipeline.py`. Les raccourcis FAST/TARGETED servent uniquement à réduire les recalculs inutiles pendant une modification locale ; ils ne remplacent pas FULL lorsqu’une couche amont ou transversale change.

## Développement local de l’interface

Le site est statique. Pour l’ouvrir localement avec les `fetch()` de données fonctionnels :

```bash
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000/`.

Ouvrir directement `index.html` avec le protocole `file://` peut empêcher le chargement des fichiers JSON selon les règles du navigateur.

## Reprise du projet

Commencer par `AI_START_HERE.md`, qui route vers la passation, le contrat et les audits réellement utiles à la zone touchée. Ne relire les notes historiques de `progression/` que lorsqu’elles sont pertinentes pour cette zone ou qu’une décision antérieure doit être retracée.
