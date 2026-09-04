# Données structurées Biblaw

Le PDF original reste la source documentaire. Les fichiers JSON constituent la
base éditoriale versionnée et révisable. Les futurs index de recherche seront
générés depuis ces JSON et ne devront jamais devenir la source de vérité.

## États de validation

- `machine-extracted-needs-human-review` : découpage automatique à relire.
- `pilot-needs-human-review` : interprétation initiale à valider.
- `validated` : texte et rattachements comparés au PDF par une personne.

## Règle fondamentale

Le texte source, les résumés et les interprétations restent dans des champs
distincts. Toute loi, pratique, recommandation ou relation thématique doit
conserver une référence vers les versets ou notes qui la justifient.
