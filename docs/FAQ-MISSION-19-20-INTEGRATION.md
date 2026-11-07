# BIBLAW — Mission 19/20 : contrat d'intégration technique (préparation seulement)

**État :** PR #75 DRAFT, intégration non exécutée, aucun changement des données publiques.  
**Autorité :** `docs/FAQ-MISSION-19-20-STAGING.json` (trois nouveaux articles) + `docs/FAQ-MISSION-19-20-ROUTING.json` (19 formulations vers leurs cibles).  
**Règle :** conserver les 102 articles antérieurs et ne pas créer 19 copies d'articles existants.

## 1. Deux types d'objets distincts

- Une **réponse canonique** est un article complet avec `id`, `title`, `answer`, références tirées de la carte `verifiedPsalms`. Trois projets seulement sont nouveaux.
- Une **formulation alternative** est une requête de recherche/navigation qui renvoie à l'`id` d'une réponse canonique, sans répéter le corps du texte.

Le fichier de routage contient 19 entrées :
- `new` (3) : créer une seule future entrée pour chacune des trois nouvelles réponses ;
- `redirect_new` (2) : renvoyer à l'une de ces entrées nouvelles ; aucun nouvel article ;
- `reuse` (12) : pointer un identifiant parmi les 102 FAQ, **sans réécriture** ni copie ;
- `unsupported` (2) : garder l'absence motivée dans la traçabilité éditoriale ; ne pas la présenter comme une réponse sourcée.

Cela donne, après autorisation de publication future, **105 réponses distinctes** et **19 formulations d'accès** (sans compter leurs titres déjà indexés). Les douze formulations `reuse` renvoient à **neuf réponses existantes distinctes**. Deux formulations supplémentaires pointent vers la nouvelle réponse A.

## 2. Format des trois réponses préparées

Le fichier `docs/FAQ-MISSION-19-20-STAGING.json` reprend la forme des fichiers `data/faq-092.json` à `data/faq-098.json` :

```json
{
  "version": 1,
  "verifiedPsalms": { "michael:254": 37 },
  "questions": [
    {
      "id": "faq-conscience-mort-19",
      "title": "Que devient notre conscience après la mort ?",
      "answer": "La Bible essénienne enseigne que..."
    }
  ]
}
```

Le fichier réellement préparé comprend **trois articles**, **neuf psaumes distincts**, **18 citations textuelles cliquables à terme**, et les numéros de versets précis. Le motif de citation attendu par `linkedReferences()` dans `js/biblaw-faq.js` est `(psaume 254 de Michaël, versets 1 à 9)` ou `(psaume 14 d'Ouriel, versets 4 à 12 et 16)`. Aucune référence ne doit être reconstruite par simple similarité de mots.

Le script `scripts/check_faq_19_20_staging.py` contrôle :
1. existence et unicité des 102 FAQ initiales ;
2. non-collision des trois nouveaux `id` ;
3. présence d'une réponse développée commençant exactement par « La Bible essénienne enseigne que » ;
4. correspondance de chaque archange/psaume/verset du brouillon avec le JSON canonique ;
5. caractère analysable de toutes les citations ;
6. correspondance de chacune des 19 formulations avec une cible réelle ou une absence motivée.

## 3. Changements techniques **à effectuer ultérieurement**, seulement après accord de publication

1. Déplacer **une copie validée** du JSON de staging vers un futur fichier de données publiques (par exemple `data/faq-099.json`), sans toucher aux 102 textes précédents.
2. Dans `js/biblaw-faq.js` : ajouter un unique chargement du nouveau fichier, appeler `linkedReferences()` avec les décomptes exacts (7, 5, 6), et ajuster le garde-fou `questions.length===102` à 105. **Ne pas désactiver** les validations.
3. Dans l'interface, implémenter les 19 formulations comme **alias de navigation** mappés vers les réponses de `ROUTING.json`. Un alias ouvre la même réponse source. Les deux entrées `unsupported` ne doivent pas apparaître comme des réponses canoniques.
4. Actualiser `scripts/check_faq_integrity.mjs` (décompte total, nouvelle famille, citations et liens), ainsi que les tests du chargement FAQ et de la navigation sur mobile/ordinateur.
5. Vérifier que les 18 liens vers les psaumes s'ouvrent dans le catalogue public : le format et les versets ont été préparés, mais le comportement après intégration doit encore être testé en navigateur.
6. Ne fusionner ou déployer qu'avec validation explicite du propriétaire et coordination de la conversation principale.

## 4. Risques à exclure lors de l'intégration

- **Collision avec PR #74 :** le catalogue de référence est la branche de son audit éditorial. Rebase/merge contrôlé nécessaire à l'intégration future ; **ne pas** fusionner #72 ou #74 depuis cette mission.
- **Comptage bloquant :** le chargeur actuel contient des listes et nombres attendus codés en dur. Ajouter des fichiers sans adapter ces gardes-fous ferait échouer la FAQ.
- **Confusion des connaissances :** la règle de rédaction interdit les ajouts scientifiques externes et les affirmations non présentes dans le texte. Les formulations n°6 et n°8 ne peuvent pas recevoir artificiellement une réponse.
- **Éditorial :** la vérification machine prouve l'existence des mots dans le PDF source ; elle ne remplace pas la relecture des nuances doctrinales. La vérification approfondie et ses réserves sont consignées dans le bilan final.

**Ce document décrit un dossier prêt pour la phase d'intégration ; la phase d'intégration elle-même est volontairement interdite dans la PR #75.**
