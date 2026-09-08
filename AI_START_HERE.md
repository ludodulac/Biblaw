# Biblaw — point d’entrée rapide pour une nouvelle conversation

Ce fichier est un **routeur**, pas une nouvelle source de vérité. Il évite de reconstruire toute l’architecture mentale du dépôt avant une modification ciblée.

## Avant toute écriture

1. vérifier le HEAD réel de `main` et les PR ouverts ;
2. lire `progression/PASSATION-NOUVELLE-CONVERSATION.md` pour les invariants et frontières courantes ;
3. lire **seulement** le contrat de la zone touchée ;
4. lire `data/thematic-index/validation-report.json` si la modification touche corpus/thèmes/recherche ;
5. lire `data/incoherences.json` uniquement si la modification touche une décision éditoriale ou une ambiguïté connue.

Les compteurs courants viennent des rapports générés, jamais de ce document.

## Routage par zone

### Corpus documentaire

Source canonique : `data/corpus/books/`, plus les prières/notes cataloguées concernées.

À lire : passation + règles documentaires du script concerné. Les anomalies PDF connues sont décrites dans la passation.

Boucle courte :

```bash
python scripts/check_biblaw.py FAST --area corpus
```

Après une modification de corpus ne nécessitant pas de réindexation sémantique :

```bash
python scripts/check_biblaw.py TARGETED --area corpus
```

Si extraction PDF, réparateur documentaire, numérotation ou générateur sémantique change : **FULL**.

### Indexation thématique canonique

Source canonique : `data/thematic-index/books/book-XX.json` ou le générateur sémantique qui produit réellement la relation.

Contrat : `data/thematic-index/SEARCH-CONTRACT.md`, en particulier **admissibilité avant classement**.

Boucle courte, sans régénération :

```bash
python scripts/check_biblaw.py FAST --area thematic
```

Après une modification ciblée des livres thématiques déjà canoniques ou d’un générateur strictement aval :

```bash
python scripts/check_biblaw.py TARGETED --area thematic
```

Cette commande utilise `scripts/rebuild_thematic_derivatives.py` et reconstruit seulement les projections déterministes aval. Elle ne rejoue ni les réparations PDF ni les 44 passes sémantiques profondes.

Si un script `complete_*`, `deepen_*`, `ground_*`, `finalize_*`, `repair_*` ou une source PDF/corpus amont change : **FULL**.

### Recherche

Sources de comportement : `js/biblaw.js` et les générateurs thématiques concernés. Le contrat sémantique est `data/thematic-index/SEARCH-CONTRACT.md`.

Boucle courte :

```bash
python scripts/check_biblaw.py FAST --area search
```

Avant de terminer un changement du moteur ou du runtime :

```bash
python scripts/check_biblaw.py TARGETED --area search
```

Si la modification change les sources thématiques elles-mêmes, utiliser plutôt `TARGETED --area thematic` puis le contrôle recherche.

### Interface publique

Sources : `index.html`, `css/biblaw.css`, `css/theme-index.css`, `js/biblaw.js`.

Règle : ne jamais masquer en CSS/JS un défaut venant du corpus, de la normalisation, de l’index ou du runtime.

Boucle courte :

```bash
python scripts/check_biblaw.py FAST --area ui
```

Avant de terminer :

```bash
python scripts/check_biblaw.py TARGETED --area ui
```

Une vérification automatisée de l’UI n’équivaut pas à un test visuel manuel dans un navigateur.

## Carte canonique → généré

### Chaîne documentaire

`PDF / source pack`  
→ réparateurs/extracteurs explicitement audités  
→ `data/corpus/books/` + pièces jointes canoniques  
→ `data/catalog.json`  
→ `scripts/build_browser_search_catalog.py`  
→ `data/browser-search-catalog.json`  
→ audits d’attachements / références legacy  
→ interface.

### Chaîne thématique

`data/thematic-index/books/book-XX.json`  
→ synchronisation/normalisation documentaire explicite  
→ `validate_thematic_index.py` (**admissibilité**)  
→ `theme-directory.json` (annuaire éditorial complet)  
→ `theme-directory-public.json` (projection runtime compacte, auditée)  
→ `theme-quality-audit.json`  
→ `theme-search-index.json`  
→ `theme-connections.json` (`semanticClaim: false`)  
→ `theme-search-runtime.json` candidat validé puis remplacement atomique  
→ `browser-search-catalog.json`  
→ audits de recherche  
→ interface.

Le navigateur public charge `theme-directory-public.json`, jamais l’annuaire éditorial complet. `scripts/audit_public_theme_directory.py` vérifie que cette projection conserve exactement les champs runtime nécessaires pour tous les thèmes et toutes leurs relations, sans modifier versets d’appui, enseignements, importance ou scores.

Ne jamais corriger durablement `theme-directory.json`, `theme-directory-public.json`, `theme-search-index.json`, `theme-connections.json`, `theme-search-runtime.json`, `theme-quality-audit.json` ou `browser-search-catalog.json` à la main.

## Niveaux de validation

### FAST

But : boucle d’édition. Syntaxe + intégrité de la zone + sentinelles déjà disponibles. Ne doit pas devenir une validation finale.

### TARGETED

But : changement cohérent d’une zone. Régénère uniquement ce que cette zone rend déterministement obsolète et lance ses contrats/non-régressions.

### FULL

```bash
python scripts/check_biblaw.py FULL
```

But : changement transversal, modification amont, générateur sémantique/documentaire, ou validation finale d’un lot à risque. Rejoue le pipeline canonique complet puis les contrats de production/recherche/UI. Le FULL nécessite les dépendances du pipeline PDF (`pdftotext`/Poppler dans la CI).

## Rapport différentiel compact

Avant une modification générée, le baseline naturel est `HEAD`. Après la génération ciblée :

```bash
python scripts/report_biblaw_diff.py
```

Après avoir commité le lot, comparer au parent :

```bash
python scripts/report_biblaw_diff.py --base HEAD~1
```

Le rapport montre uniquement les écarts significatifs : compteurs, thèmes, relations thème–psaume ajoutées/supprimées, reclassifications, changements de preuves, alias ajoutés/supprimés/retargetés, ambiguïtés, erreurs/warnings et changements des requêtes sentinelles. Il ne modifie aucun artefact.

## Sentinelles et outils de revue

Les régressions de recherche sont bloquées principalement par `scripts/audit_production_search_queries.py`, complété par :

- `scripts/audit_psalm_number_search.py` — numéros répétés, `22 commandements` non interprété comme numéro ;
- `scripts/audit_browser_search_indexes.py` — index navigateur pré-calculés ;
- `scripts/validate_thematic_search_runtime.py` — ambiguïtés et projection exacte du runtime ;
- `scripts/audit_public_theme_directory.py` — équivalence de la projection compacte publique avec l’annuaire canonique pour tous les champs runtime.

Le bug réel **Assemblée / Sainte Assemblée** est couvert par des assertions dans `audit_production_search_queries.py`. `scripts/audit_assembly_theme_context.py` reste disponible comme outil **descriptif de revue éditoriale** : il imprime les contextes et co-présences mais n’est pas une barrière de validation et n’est donc pas exécuté automatiquement dans FAST/TARGETED/FULL.

Les sentinelles couvrent notamment : littéral simple, expression littérale, thème canonique, alias observé (`argent spirituel`), alias ambigu, double lecture thème/texte, zéro thème attendu, absence de fallback substring/proximité, ordre Central → Important → Lié et numéro présent dans plusieurs livres.

Un bug corrigé doit devenir une sentinelle lorsqu’il peut être reproduit de façon déterministe.

## Frontières historiques à ne pas réintroduire

- `data/corpus/<archange>/...` : anciens psaumes historiques, hors production ;
- `data/thematic-index/prototypes/` : prototypes, hors index canonique ;
- artefacts legacy du pilote Livre 17 : conservés historiquement, normalisés uniquement à la frontière de production.

Les contrôles exécutables `audit_legacy_psalm_references.py` et `audit_corpus_attachments.py` priment sur une vérification manuelle équivalente lorsqu’ils viennent de passer.

## Avant de déclarer un lot terminé

- le rapport différentiel ne montre pas de variation inexpliquée ;
- les sentinelles pertinentes passent ;
- les ambiguïtés attendues restent explicites ;
- aucun artefact généré n’a été corrigé manuellement ;
- TARGETED suffit pour un changement réellement local ; FULL est requis dès qu’une couche amont/transversale a changé ;
- Pages reste la dernière barrière de production, pas le premier endroit où détecter un défaut de données.
