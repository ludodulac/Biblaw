# 🌸 BIBLAW — MISSION 068 — VALIDATION ET INTÉGRATION

**Périmètre :** branche `feat/052-search-ui`, PR #72 DRAFT. Aucun déploiement, aucune fusion. Code vérifié avant ce rapport : `222ebc10f4a1c019e43c795e80a533fb5f20c304`.

## 1. GitHub Actions — PASS ciblé

- `verify-notes-067.yml` : **SUCCESS** (run [41183266587](https://github.com/ludodulac/Biblaw/actions/runs/41183266587), SHA `7d63216e...`). Contrôle 1 158 psaumes, 677 prières et restaurations 067.
- `066-sync-browser-bundle.yml` : **SUCCESS** (run [41183266630](https://github.com/ludodulac/Biblaw/actions/runs/41183266630), SHA `7d63216e...`) ; il reconstruit le navigateur, audite les pièces jointes, exécute le résolveur 066 et la vérification 067. L'échec antérieur [41183157658](https://github.com/ludodulac/Biblaw/actions/runs/41183157658) a été corrigé sur ce passage ultérieur.
- `verify-notes-066-finalisation.yml` : **SUCCESS** (run [41183157633](https://github.com/ludodulac/Biblaw/actions/runs/41183157633), SHA `25b9c172...`). Attention : ce workflow lance le résolveur 066 puis `verify_067.py`, **pas** le script historique `verify_066_finalisation.py` (ce dernier présuppose 676 prières et compare à `HEAD^` ; il n'est donc plus utilisable tel quel sur 068). Ne pas interpréter ce PASS comme l'exécution de ce script historique.
- Vérification 068 complète, sans déploiement : **SUCCESS**, [run 41321998893](https://github.com/ludodulac/Biblaw/actions/runs/41321998893). `verify_067.py`, `resolve_note_occurrences_066.py --check`, `audit_corpus_attachments.py`, création de `_site`, puis vrai Chromium.
- Validation des recherches et index : **SUCCESS**, [run 41322242365](https://github.com/ludodulac/Biblaw/actions/runs/41322242365), SHA `222ebc10...`. Les assertions obsolètes des tests 041C, de la lecture de documents et des recherches par numéro ont été alignées avec le comportement déjà en place.

## 2. Catalogue et prières — PASS

- Catalogue canonique : **1 963 chemins**, dont **1 158 psaumes**, **677 prières** et **11 notes**.
- Bundle navigateur à jour et fidèle aux sources : **1 846 enregistrements** = 1 158 psaumes + 677 prières + 11 notes ; audit d'intégrité et unicité **PASS**.
- Nouvelle `ouriel-book-24-prayer-036` : **1 968 caractères**, liée au psaume `book-24-psalm-141`, référencée et lisible sur ordinateur/mobile.
- Correction UI : une précédente `Map` ne retenait qu'une prière par psaume. L'éditeur affiche désormais **toutes** les prières publiques ayant un rattachement réciproque au psaume lorsque l'option « Prières » est active. Les 677 prières restent également consultables directement.

## 3. Notes visibles et authenticité — ÉTAT EXACT

- **11 notes déjà présentes** dans le catalogue navigateur, sans nouvel ajout de note ni modification du contrat d'export : **1** a `validation.status=validated`, les **10 autres** ne possèdent pas cette validation humaine (statuts machine ou révision à faire). Leur consultation indépendante préexistante reste inchangée.
- Affichage contextuel ajouté aux psaumes et prières **uniquement** pour les notes déjà publiques qui ont `validation.status=validated`, un texte, un ID unique et un rattachement réciproque vérifié.
- Cas réel affiché : `book-17-psalm-105-note-001`, **1 occurrence** sur le psaume 105 du livre 17. Cas négatif testé : `book-17-psalm-109-note-001` n'est **pas** élevé au rang de « note authentifiée » (validation machine).
- Les **29 cas compatibles de 066 ne sont pas authentifiés automatiquement** ; pas d'import du répertoire privé `data/notes/books/` vers Pages ; pas de nouvelle note publiée ni de composite exposé par ce correctif. Les anciennes notes non humaines déjà diffusées dans le catalogue constituent une limite éditoriale persistante à traiter par une décision distincte.

## 4. Résolveur — PASS technique, non publié

- `resolve_note_occurrences_066.py --check` **PASS réel sur GitHub Actions** : **18 groupes physiques / 36 identifiants historiques**.
- Registre 066 intact ; résolveur Python disponible pour les anciens IDs, sans désigner arbitrairement un identifiant élu.
- Il n'existe pas de résolveur JavaScript public pour les 29 cas compatibles : **pas d'exposition avant authentification éditoriale et validation d'un contrat de publication**.

## 5. Essais Chromium — PASS réel, appareils simulés

La nouvelle action 068 a servi le vrai contenu `_site` en HTTP local (aucun déploiement) et parcouru le DOM avec Chromium :

- **Ordinateur 1280 px, mobile 390 px et mobile 320 px : PASS** dans les trois cas.
- Recherche par mot « lumière » ; recherche thématique « sainte assemblée » ; ouverture d'un résultat, fermeture et navigation ; consultation intégrale d'un psaume ; consultation directe de Pr.36 ; liste des 677 prières ; présence de la seule note contextuelle authentifiée ; absence de chargement HTTP de `data/notes/**` : **PASS**.
- Aucun essai sur téléphone physique ni navigateur Safari n'a été effectué ; la validation mobile correspond à des émulations Chromium avec tactile.

## 6. Protection historique

Aucun fichier de `data/corpus/**`, `data/prayers/**`, `data/notes/**`, `data/catalog.json` ou `data/browser-search-catalog.json` n'a été modifié par 068. Diff avec `fee614c9...` : exclusivement UI, tests et workflows ciblés. Les textes historiques de `26/189` (dont **1 679 caractères** à protéger), les continuations non démontrées et les identifiants anciens n'ont pas été retouchés. Cela ne constitue **pas** une nouvelle preuve de restauration des continuations restantes.

## 7. Bloquants non levés

1. Authenticité éditoriale des **29 cas compatibles**, non réglée et non déduite du résolveur ; certains anciens enregistrements du catalogue public restent sans validation humaine.
2. Pas de résolveur d'alias historiques intégré au navigateur (choix délibéré pour éviter une publication indue).
3. Continuations et composites historiques hors 067, notamment `26/189` et Pr.102 du livre 35, toujours protégés mais non déclarés restaurés.
4. Appareils physiques non testés ; les 3 profils Chromium sont vérifiés.

**Livraison :** correctif dans `js/biblaw.js`, test `scripts/smoke_notes_068.mjs`, workflow `verify-integration-068.yml`, alignements minimaux des assertions CI existantes. **PR #72 conservée DRAFT, pas de fusion, pas de déploiement. STOP.**
