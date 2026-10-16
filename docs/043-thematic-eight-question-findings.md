# BIBLAW 043 — pertinence thématique : huit questions

## Méthode et limites
Exécution réelle du moteur JavaScript `js/theme-suggestion-engine.js` avec `theme-directory-public.json` et `theme-search-runtime.json` issus de `main`. Audit automatique des huit questions dans `scripts/audit_043_eight_questions.js`. L'artefact CI `biblaw-043-eight-question-report` contient, pour chaque thème proposé, les `recordId`, `verseNumbers` et `teaching` éditoriaux (jusqu'à trois exemples par thème). Les nombres de psaumes sont les unions d'identifiants indexés, **pas une validation sémantique manuelle**.

## Résultats mesurés après la correction

| Question | Thèmes effectivement proposés (IDs) | Psaumes distincts accessibles | Constat |
|---|---|---:|---|
| Que disent les Archanges sur la peur ? | ancrage-des-quatre-archanges, archanges, ecriture-sur-la-terre, equilibre-sur-le-fil, peur, peur-et-doute, psaumes-de-la-ronde, quatre-archanges | 127 | Peur est présent mais noyé parmi des thèmes sur « Archanges ». |
| Comment développer la sagesse ? | corps-vaisseau-de-sagesse, corps-de-la-sagesse, corps-de-sagesse, pensee-de-sagesse, sagesse, sagesse-comme-bien-commun, sagesse-comme-liberation, sagesse-comme-solution | 271 | Sagesse retrouvé. |
| Que devient l'homme après la mort ? | vie-apres-la-mort-comme-continuite, chemin-de-l-homme-veritable, ciel-cree-par-l-homme, homme-a-la-frontiere-des-mondes, homme-canal-de-benediction, homme-et-femme, homme-intermediaire, homme-intermediaire-des-mondes | 8 | **Défaut confirmé : « mort » absent du top 8 malgré thème existant (161 relations)**. Les labels contenant « homme » saturent les places. |
| Comment cultiver l'amour ? | amour | 9 | Amour retrouvé ; exhaustivité éditoriale non démontrée. |
| Comment se libérer de la colère ? | dettes-et-liberation, liberation, liberation-des-regnes, liberation-par-la-pensee, sagesse-comme-liberation | 11 | Correction ciblée : « libérer » permet maintenant de retrouver « Libération ». **Colère n'est toujours pas un thème reconnu : pertinence des résultats non démontrée.** |
| Comment vivre avec les Anges ? | alliance-angelique, anges, meditation-comme-art-de-vivre, vertus-des-anges | 134 | Anges retrouvé. |
| Qu'est-ce que la véritable liberté ? | chemin-de-l-homme-veritable, homme-veritable, interet-veritable, liberte, liberte-comme-concept, liberte-et-choix, richesse, vie-veritable | 18 | Liberté retrouvé mais mélangé à « véritable ». |
| Comment nourrir son âme ? | ame, ame-collective, ame-de-la-vie, ame-et-autre-rive, assumer-son-humanite, corps-ame-esprit, donner-une-ame-a-l-oeuvre, eau-comme-ame | 275 | Âme retrouvé ; le sens de « nourrir » n'est pas résolu. |

## Une correction étroite
Dans `THEME_QUERY_EQUIVALENTS`, ajout de `liberer: ['liberer','liberation']`. Il s'agit d'un rapprochement lexical de la question vers le thème existant, **pas** d'une relation thématique ou d'un alias éditorial. Les fichiers sources de relations, le corpus, les Gold et les occurrences restent inchangés.

**Avant** : question « Comment se libérer de la colère ? » → 0 thème, 0 psaume.
**Après** : 5 thèmes proposés, 11 psaumes indexés accessibles, dont « Libération ».

## Vérifications
- Workflow initial : échec attendu du test de rappel « libérer », avec rapport des huit questions.
- Workflow après correction : **SUCCESS**, audit huit questions + benchmark existant Q120.
- Pas de changement HTML ni de navigation Chromium dans cette mission ; le moteur partagé est appelé directement sous Node.
- Aucune relation thématique nouvelle ; aucune preuve de « traitement de la colère » ne peut être revendiquée à partir des seuls 11 psaumes.

## À traiter ensuite
1. Prioriser « mort » dans « après la mort » sans perdre la spécificité « vie après la mort », avec tests de non-régression.
2. Examiner les versets canoniques sur la colère avant d'envisager un thème, alias ou relation.
3. Évaluer manuellement la pertinence des passages pour les huit questions ; l'audit actuel mesure la récupération indexée, pas la qualité doctrinale.
