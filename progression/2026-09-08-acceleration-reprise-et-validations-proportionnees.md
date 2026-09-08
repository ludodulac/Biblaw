# Accélération de la reprise et validations proportionnées — 2026-09-08

## Objectif

Réduire le temps nécessaire pour comprendre une zone de Biblaw, modifier la bonne couche et vérifier une régression, sans affaiblir la sémantique, la traçabilité, la reproductibilité ni les capacités existantes.

Cette passe n’introduit aucune nouvelle architecture de données. Elle orchestre les sources, générateurs et audits existants et ajoute seulement un rebuild aval ciblé, un routeur de validations et un rapport différentiel compact.

## Audit initial

### Déjà bien couvert

- séparation stricte recherche documentaire par numéro / recherche thématique / recherche littérale ;
- admissibilité canonique avant ranking ;
- alias ambigus préservés explicitement ;
- absence de fallback thématique par substring ou proximité ;
- graphe de cooccurrence avec `semanticClaim: false` ;
- runtime construit comme candidat, validé puis remplacé atomiquement ;
- frontières de production protégeant les anciens psaumes et artefacts historiques ;
- régressions de bugs réels, notamment Assemblée / Sainte Assemblée et recherche par numéro ;
- barrière Pages avant publication.

### Friction réelle

- la reprise obligeait une conversation à reconstituer manuellement quels documents et scripts sont réellement nécessaires ;
- les commandes de validation étaient dispersées ;
- un changement purement aval pouvait conduire à rejouer le pipeline canonique complet : réparations PDF, extraction et passes sémantiques profondes des 44 livres ;
- les écarts entre deux générations étaient difficiles à lire sans inspecter de gros JSON ;
- des compteurs runtime étaient recopiés dans le README et pouvaient devenir obsolètes ;
- le workflow recherche recalculait les mêmes comptages littéraux à deux endroits ;
- `audit_assembly_theme_context.py`, descriptif et sans assertion, était exécuté comme s’il constituait une barrière de régression.

### Automatisable sans risque sémantique

- routage par zone ;
- commandes composées FAST / TARGETED / FULL ;
- reconstruction des seuls dérivés thématiques après validation de la source canonique ;
- diff compact des compteurs, relations, alias, ambiguïtés, ranking et sentinelles ;
- transformation de comportements historiques en sentinelles déterministes ;
- pré-calcul des fragments textuels normalisés dans les audits, sans modifier la règle de correspondance.

### Inutilement coûteux / non retenu

- ne pas rejouer les 44 passes profondes pour un changement strictement aval ;
- ne pas ajouter de cache sémantique ou de parallélisation complexe sans profilage ;
- ne pas créer trois infrastructures CI distinctes pour FAST/TARGETED/FULL ;
- ne pas recopier les nombres dynamiques dans plusieurs documents ;
- ne pas ajouter une nouvelle couche de recherche approximative pour accélérer ;
- ne pas exécuter automatiquement un script descriptif qui ne peut pas faire échouer une régression.

## Chemin de reprise

Nouveau routeur : `AI_START_HERE.md`.

Il ne remplace pas la passation ni `SEARCH-CONTRACT.md`. Il indique simplement :

- quelle source canonique modifier selon la zone ;
- quels artefacts sont générés ;
- quel contrat lire ;
- quelles commandes exécuter ;
- quand une validation TARGETED suffit ;
- quand FULL reste obligatoire ;
- quelles frontières historiques ne doivent jamais revenir en production.

Le README pointe désormais vers ce routeur et ne recopie plus les compteurs runtime. Les nombres courants restent dans les rapports générés.

## Carte canonique vers généré

### Documentaire

`PDF/source pack`
→ réparations/extraction auditées
→ corpus canonique + prières/notes
→ catalogue
→ bundle navigateur
→ audits d’attachements / références historiques
→ interface.

### Thématique

`data/thematic-index/books/book-XX.json`
→ synchronisation/normalisation explicite
→ `validate_thematic_index.py`
→ annuaire
→ audit qualité
→ index d’alias
→ graphe de cooccurrence
→ runtime candidat validé puis remplacement atomique
→ bundle navigateur
→ audits de recherche
→ interface.

La validation canonique intervient avant les dérivés afin qu’une relation inadmissible soit rejetée à la source plutôt que découverte dans l’UI.

## Validations proportionnées

Nouveau routeur : `scripts/check_biblaw.py`.

### FAST

Boucle d’édition non destructive : syntaxe, intégrité locale et sentinelles de la zone.

Exemples :

```bash
python scripts/check_biblaw.py FAST --area search
python scripts/check_biblaw.py FAST --area thematic
```

### TARGETED

Validation d’un changement cohérent d’une zone. La variante thématique utilise `scripts/rebuild_thematic_derivatives.py`, qui valide d’abord les livres canoniques puis reconstruit uniquement les projections aval.

```bash
python scripts/check_biblaw.py TARGETED --area thematic
```

Cette commande ne rejoue pas les réparations PDF ni les passes `complete/deepen/ground/finalize`.

### FULL

```bash
python scripts/check_biblaw.py FULL
```

FULL conserve le pipeline canonique complet et les audits finaux. Il est requis dès qu’une source documentaire, un réparateur PDF ou un générateur sémantique amont change.

## Rebuild thématique ciblé

`scripts/rebuild_thematic_derivatives.py` exécute :

1. garde des identifiants techniques connus ;
2. synchronisation documentaire et métadonnées explicites ;
3. validation canonique des relations ;
4. annuaire ;
5. audit qualité ;
6. index d’alias et validation ;
7. cooccurrences et validation ;
8. runtime candidat + validation ;
9. bundle navigateur ;
10. audits d’attachements et de références historiques.

Il ne doit être utilisé que lorsque les passes sémantiques profondes et les sources PDF/corpus n’ont pas changé.

## Sentinelles renforcées

`audit_production_search_queries.py` protège explicitement :

- mots et expressions littérales avec frontières de mots ;
- absence de faux positif d’expression non contiguë ;
- thème canonique ;
- alias observé non ambigu (`argent spirituel` → `argent`) ;
- alias ambigu (`alliance de lumière`) ;
- absence de thème générique pour `assemblée` ;
- thème distinct `sainte assemblée` ;
- coexistence des niveaux Central / Important / Lié sur un thème large ;
- versets et `teaching` obligatoires ;
- couverture canonique complète.

Les audits séparés continuent à protéger les numéros répétés et les index navigateur pré-calculés.

`audit_assembly_theme_context.py` est conservé comme outil de revue éditoriale : il affiche les co-présences et exemples contextuels sans en tirer de relation sémantique. Comme il ne contient pas d’assertion, il n’est plus exécuté automatiquement comme une validation. La vraie régression Assemblée / Sainte Assemblée reste bloquée dans `audit_production_search_queries.py`.

## Rapport différentiel

`scripts/report_biblaw_diff.py` compare le working tree à un ref Git (`HEAD` par défaut) et montre seulement :

- compteurs canoniques ;
- erreurs/warnings ;
- thèmes ajoutés/supprimés ;
- relations thème–psaume ajoutées/supprimées ;
- reclassifications `importance` ;
- changements de preuves (`directness`, versets, `teaching`) ;
- alias ajoutés/supprimés/retargetés ;
- ambiguïtés ;
- variations significatives des métriques de ranking ;
- changements des requêtes sentinelles.

Il normalise les fragments textuels une seule fois par état comparé, sans approximation de la recherche. La CI l’exécute sur un `HEAD` propre afin de vérifier que l’outil lui-même reste exécutable et non divergent.

## Mesure du gain observé

Comparaison de runs GitHub Actions sur le même workflow de recherche, hors temps variable de checkout :

- avant suppression du scan littéral dupliqué et optimisation de l’audit : environ **24 s** de validations ;
- après : environ **6,6 s** de validations ;
- `audit_production_search_queries.py` seul : environ **10,4 s → 1,8 s**.

Les sorties sentinelles restent identiques : mêmes comptages littéraux, mêmes thèmes résolus, mêmes ambiguïtés et mêmes rangs. Le gain vient du pré-calcul et de la suppression de travail déterministe dupliqué, pas d’une réduction de couverture.

Ces temps sont des mesures de runs CI observés et peuvent varier selon le runner ; ils servent à vérifier l’ordre de grandeur du gain, pas de SLA.

## Capacités volontairement inchangées

- aucune relation thématique n’est créée par fréquence, proximité ou cooccurrence ;
- aucune ambiguïté n’est résolue automatiquement ;
- la recherche littérale reste complète et distincte ;
- les numéros de psaume retournent toutes les correspondances valides ;
- aucun thème n’est supprimé pour améliorer les performances ;
- les artefacts générés restent reproductibles depuis leurs sources ;
- Pages reste la barrière finale de production ;
- le pipeline FULL reste disponible et inchangé dans son rôle.

## Coût restant

Le FULL reste volontairement lourd : il réexécute les réparations documentaires et les passes sémantiques profondes sur 44 livres avant de reconstruire les projections et audits. Cette lenteur protège les changements amont. Aucune mise en cache sémantique ni parallélisation n’a été ajoutée sans mesure préalable de déterminisme, dépendances et gain réel.

Le principal gain de cette passe vient donc de ne plus utiliser FULL pour les modifications qui sont démontrablement aval et locales, tout en conservant FULL pour les changements qui peuvent affecter le sens ou la source canonique.
