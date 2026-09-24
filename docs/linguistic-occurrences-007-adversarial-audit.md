# BIBLAW-LINGUISTIC-OCCURRENCES-007 — audit adversarial SUIS

Baseline auditée : PR #24 HEAD `a869e2a2c748d672a764fade0d4c6c815276d0ce`.

Cette mission cherche des contre-exemples. Elle ne modifie ni le pilote SUIS ni le moteur de #24.

## Résultats établis

La reconstruction depuis le corpus confirme 631 occurrences tokenisées de `suis` et la partition 615 AUTONOMOUS, 1 VERB_CLITIC, 5 VERB_INVERSION, 10 COMPOUND_ELEMENT. Les 16 non-AUTONOMOUS ont été relues : le clitique est `suis-le`, les cinq inversions sont `suis-je`, et les dix composés sont `Je-Suis`.

Une recherche indépendante sur le corpus brut trouve aussi une occurrence `Suisje` et une occurrence `JeSuis`. Elles ne sont pas des occurrences `suis` selon le tokenizer actuel. Ce n'est pas une erreur d'offset de l'index 631, mais une limite du contrat lexical actuel qui doit rester visible.

Les 14 gold ont été relus dans leur contexte. Leurs lemmes/POS annoncés sont confirmés. Pour `je me suis servi`, la conclusion stockée est seulement lemma=être, POS=VERB. La fonction auxiliaire dans la construction pronominale est une observation grammaticale de l'audit, pas une dimension encodée par le modèle.

Les quatre VERB_SUIVRE automatiques sont confirmés : `suis-le`, `Suis le maître`, et deux `tu suis ...`.

L'échantillon UNKNOWN reproductible confirme une couverture volontairement faible : de nombreux cas manifestes de ÊTRE restent UNKNOWN, notamment des identités nominales et négations. Aucun faux positif n'en découle.

## Erreur structurelle certaine : VERB_INVERSION n'est pas encore générique

Le code de #24 reconnaît un tiret directement suivi d'un pronom sujet. Cela couvre correctement les cinq `suis-je` observés.

Mais les sondes structurelles :
- `porte-t-il`
- `marche-t-elle`
- `a-t-il`

sont classées COMPOUND_ELEMENT, et non VERB_INVERSION.

Cause : le segment immédiatement après le premier tiret est `t`; le moteur ne représente pas le `-t-` euphonique avant le pronom sujet.

Conclusion : VERB_INVERSION est correct pour SUIS, mais sa prétention de segmentation française générique est fausse/incomplète. #24 doit être corrigée avant fusion si cette catégorie doit être présentée comme générique.

## Couplage segmentation → adjudication

Dans `suis-config.json`, `VERB_INVERSION` est explicitement mappé vers `VERB_ETRE`. Le moteur structurel ne décide pas lui-même ÊTRE : il retourne seulement la segmentation, puis la configuration lexicale SUIS effectue le mapping. La séparation des couches existe donc techniquement.

Cependant ce mapping est une connaissance spécifique à SUIS et doit rester identifié comme telle.

## Généricité réelle

A — indexation multi-mots : solide. L'indexeur est paramétré par surface et n'a pas été modifié pour SUIS.

B — segmentation multi-phénomènes : partielle. AUTONOMOUS / VERB_CLITIC / COMPOUND_ELEMENT sont réutilisés ; VERB_INVERSION couvre le cas direct `verbe-pronom` mais pas `verbe-t-pronom`.

C — représentation multi-analyses : solide au niveau du schéma/configuration. Plusieurs catégories, lemmes et POS sont data-driven.

D — désambiguïsation : encore partielle. Le moteur possède un chemin legacy PORTE codé en dur et un chemin configurable pour SUIS. Les règles SUIS sont des regex lexicales configurées ; cela démontre une infrastructure de règles, pas encore un analyseur morphosyntaxique général.

## Décision audit

Aucun faux positif certain n'a été trouvé parmi les 116 VERB_ETRE inspectés par familles/règles ni parmi les 4 VERB_SUIVRE exhaustivement relus.

L'erreur certaine porte sur la généricité structurelle annoncée de VERB_INVERSION, pas sur les cinq occurrences SUIS actuellement classées.

Recommandation : NO-GO fusion #24 en l'état ; corriger et tester la segmentation d'inversion générique, puis réexécuter PORTE + SUIS. Ne pas commencer un troisième pilote avant cette correction.
