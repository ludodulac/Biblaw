# Contrat de l’interface publique — 2026-09-07

## Décision produit

L’interface publique Biblaw doit rester centrée sur la recherche et la consultation du corpus structuré.

Parcours attendu :

1. rechercher par thème, mot, expression ou numéro de psaume ;
2. afficher les résultats structurés ;
3. ouvrir un résultat avec le bouton **Voir** ;
4. consulter le texte dans Biblaw ;
5. proposer **Télécharger le texte** uniquement dans la fiche ouverte.

## Ce qui a été supprimé

L’ancien prototype de lecteur PDF ne fait plus partie du produit public :

- `reader.html` supprimé ;
- `app.js` supprimé ;
- `styles.css` supprimé ;
- lien `Lecteur PDF` retiré de l’atelier de validation ;
- lien `Validation` retiré de la page publique.

Les cartes de résultats ne contiennent plus de bouton `Voir dans le PDF`. Leur action principale est désormais `Voir`, qui ouvre l’enregistrement structuré dans `recordDialog`.

## Séparation public / éditorial

`validation.html` reste un atelier éditorial interne au dépôt et peut utiliser la référence PDF comme source de contrôle documentaire. Il ne doit pas être exposé dans la navigation de la page publique.

Cette distinction ne change pas la règle de source autoritative : le PDF reste la source de vérification éditoriale, mais l’utilisateur de Biblaw consulte le corpus structuré dans l’application.

## Garde-fou de déploiement

`scripts/audit_public_ui_contract.py` est exécuté avant chaque déploiement GitHub Pages.

Le déploiement échoue si :

- les fichiers du vieux lecteur réapparaissent ;
- `validation.html` ou `reader.html` est lié depuis `index.html` ;
- `Voir dans le PDF` ou un lien direct `.pdf#page=` réapparaît dans `js/biblaw.js` ;
- le bouton `Voir` structuré disparaît ;
- `Télécharger le texte` n’est plus dans la fiche ouverte.

Le workflow Pages avec ce garde-fou a été validé avec succès le 7 septembre 2026.
