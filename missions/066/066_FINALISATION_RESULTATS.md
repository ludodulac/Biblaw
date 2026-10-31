# 🌸 BIBLAW — 066-FINALISATION — Résultats vérifiables

**Base restaurable :** `eeecd3ded92845640a8293ca26c6c4d1229acaaa`, qui succède au HEAD communiqué `fffabf4e66cadcb5c017f1dc759424ced6797729` (commit concurrent conservé). PR #72 OPEN/DRAFT au seul contrôle initial ; non fusionnée et aucun déploiement.

## 44 anomalies : 7 corrigées / 29 compatibles / 8 bloquées

**7 corrigées (A) :** 5 relations note→prière Pr.11/53/71/93/76 déjà mises en données, 22/155 pied séparé et verset 21 restauré, et désormais `21/143/003` reliée à Pr.38 (pied n°2 p.1654). En outre, l'ancien ID `21/143/002` du pied n°1 reçoit le même modèle compatible.

**29 compatibles (B), sans authentification éditoriale définitive :** 21 cas de l'accélération conservés ; 8 cas désormais protégés : `21/143/004` (composite exact de deux pieds 002/003 sous Pr.38), `29/199/002–003` (une seule note imprimée sous Pr.90 p.2751, page et verset de 003 corrigés), `35/213/002–003` (composite Pr.102 intact), `26/189/003` (historique et 1 679 caractères intacts), `23/129/003` (composite/004 intacts) et `29/216/003` (correction de « audelà » en « au-delà » dans 003 et ancien 002, avec textes initiaux sauvegardés). **Cinq regroupements ajoutés : 18 groupes / 36 IDs**, anciens identifiants accessibles par le résolveur, aucun ID élu.

**8 bloquées (C), sans écriture :**
- `21/137/001` : Pr.32 : conservation intégrale non démontrée.
- `21/160/001` : Pr.54 : prière incomplète, destination non prouvée.
- `23/145/001` : Pr.41 : destination de continuation non vérifiée.
- `24/141/001` : Pr.36 : prière manquante, destination non prouvée.
- `26/169/001` : Pr.54 : continuation 1883 caractères absente de prière autonome.
- `29/212/001` : Pr.102 : continuation absente de prière autonome.
- `07/035/005` : deux pieds fusionnés, références individuelles non garanties.
- `12/077/001` : trois pieds fusionnés, références individuelles non garanties.

## Conservation, réalité du fonctionnement, limites

- `29/216/002–003` ont leur ancien `text` complet dans `recovery066Finalisation.originalText`, correction orthographique enregistrée et réversible ; `29/199/003` conserve ses anciennes métadonnées p.2750/v.50 en récupération. Pour `21/143/004`, le champ `text` original reste intégral et sa segmentation `text(002)+" 2 - "+text(003)` est prouvée.
- Pr.38 et Pr.90 : champs `noteIds` nouveaux, références réciproques et liens psaume conservés ; **aucun texte de prière supprimé ou altéré**. Les 1 158 psaumes et 676 prières doivent passer le contrôle structurel spécialisé, sans réaudit PDF.
- **ALERTES NON LEVÉES :** les **1 679 caractères historiques de 26/189**, la suite Pr.102 livre35 (~1 951 caractères) et Pr.54 livre26 (1 883 caractères) **ne sont pas restaurés dans leurs destinations canoniques** ; anciens contenus complets NON TOUCHÉS.
- **Intégration au site public : NON, FAIL.** L'interface lit `data/browser-search-catalog.json` et seulement 11 notes y sont publiées ; `scripts/build_pages_site.py` interdit `data/notes/`. Insérer les notes extraites dans l'interface sans modifier ce contrat de publication et valider leur qualité ne serait pas une intégration sûre. Le résolveur Python du dépôt reste utilisable directement ; son exécution réelle doit être certifiée par GitHub Actions, pas par une assertion en mémoire.
- [Tests spécialisés](../../scripts/verify_066_finalisation.py) et [workflow non déployant](../../.github/workflows/verify-notes-066-finalisation.yml) ajoutés. Statut du run à confirmer avec les preuves CI ; ne pas annoncer PASS avant vérification.

**STOP — aucun choix arbitraire d'identité canonique ni suppression de texte.**
