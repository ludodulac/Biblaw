# 🌸 BIBLAW — MISSION 067 — RÉSOLUTION DES 8 DERNIÈRES ANOMALIES

## Statut des huit cas (base récupérable `491bf927ca06f20ca16ee052d6e5be90f4a1933a`)

| Identifiant | Résultat | Preuve préexistante | Changement enregistré |
|---|---|---|---|
| `21/137/001` | **CORRIGÉE** | 064-09/065-06, PDF p.1619–1620, pied de 8 tokens et continuation Pr.32 | Note coupée au pied exact ; suite de **362 caractères** ajoutée sans perte à Pr.32 ; lien note→prière réciproque. |
| `21/160/001` | **CORRIGÉE** | 064-10/065-06, p.1747–1748, pied de 19 tokens, appel v.46 | Pied isolé ; suite de **1 889 caractères** jointe à Pr.54 (livre 21), v.46 précisé. |
| `23/145/001` | **CORRIGÉE** | 064-12/065-06, p.2020–2021, pied de 30 tokens, appel v.37 | Pied isolé ; suite de **1 205 caractères** jointe à Pr.41, v.37 précisé. |
| `24/141/001` | **CORRIGÉE** | 064-12/065-06, p.2134–2135, pied de 50 tokens, mention imprimée **Pr.36** | Pied isolé ; **Pr.36 créée** sous `ouriel-book-24-prayer-036.json` avec les **1 968 caractères** intégralement récupérés du composite et son rattachement au psaume 141. |
| `26/169/001` | **CORRIGÉE** | 064-12/065-07, p.2361–2362, pied de 24 tokens, appel v.35 | Pied isolé ; suite de **1 883 caractères** jointe à Pr.54 (livre 26), v.35 précisé. |
| `29/212/001` | **CORRIGÉE** | 064-14/065-12, p.2813–2814, pied de 4 tokens sous **Pr.102** | Pied isolé ; suite de **953 caractères** jointe à Pr.102 (livre 29) ; lien note→prière réciproque. |
| `07/035/005` | **SÉCURISÉE PAR COMPATIBILITÉ** | 064-03/065-05, PDF p.387 | Identité exacte `note-005.text == note-003.text + " 2 - " + note-004.text` ; ancien composite conservé à l'identique, retiré uniquement de la liste des notes physiques actives, déplacé vers `legacyCompositeNoteIds067`. Les deux vrais pieds restent dans `noteIds`. |
| `12/077/001` | **CORRIGÉE** | 064-05/065-05, PDF p.764 : trois pieds imprimés et trois appels au v.1 | Note 001 ramenée au pied 1, nouvelles notes `002` et `003` correspondant aux marqueurs locaux 2 et 3 ; ajout de trois `noteIds` réciproques. Intégralité exacte des **484 caractères** conservée dans `recovery067.originalText`. |

## Conservation et limites

- **7 corrections techniques, 1 compatibilité réversible, 0 cas laissé sans intervention**, mais **aucune authentification éditoriale automatique** et aucune fusion d'identifiants arbitraire.
- Chaque note tronquée conserve son ancien `text` et son blob Git dans `recovery067`. Chaque prière complétée conserve son ancien `text` et le SHA antérieur ; `prayer.text = ancien + continuation`. Le nouveau Pr.36 est reconstitué exactement depuis le suffixe imprimé `" Pr. 36. "` de la note précédente.
- **ATTENTION :** les décisions de reconstruction reposent sur les **preuves visuelles déjà archivées des missions 064/065** et les extractions source intactes ; **le PDF original n'a pas été rouvert directement en 067**. La garantie démontrée concerne la conservation caractère par caractère des fragments disponibles, **pas une nouvelle collation éditoriale intégrale avec les pages originales**.
- Pr.54 livre26 récupère la continuation des **1 883 caractères** identifiée dans la note `26/169` ; elle reste également conservée dans `recovery067`. **Ne pas confondre** avec la prière Pr.54 livre21 (1 889 caractères), restaurée séparément.
- Les **1 679 caractères historiques de `26/189/002`**, la continuation de **Pr.102 livre35** et tous les autres composites historiques hors des huit cas restent **strictement hors périmètre et inchangés**. Ils ne sont pas déclarés restaurés dans leurs destinations.
- Le corpus préexistant comptait **1 158 psaumes et 676 prières**. La création documentée de **Pr.36 livre24** porte le total attendu à **1 158 psaumes et 677 prières**. Le catalogue passe de 1 962 à 1 963 références ; le catalogue de recherche public doit être reconstruit avant d'affirmer que la prière est visible dans l'interface.
- Le résolveur physique 066 et son registre de 18 occurrences restent inchangés ; le composite `07/035/005` conserve une entrée de compatibilité historique sans remplacer les véritables pieds imprimés.

## Tests et livraison

Vérifications spécialisées automatisées : `scripts/verify_067.py`, GitHub Action `verify-notes-067.yml`; régénération et audit du catalogue navigateur par `066-sync-browser-bundle.yml`. **Ne déclarer PASS que si la campagne CI sur le HEAD livré est effectivement réussie.** Aucune publication, aucun déploiement, aucune fusion de la PR #72.

**STOP — après résultats des vérifications, sans nouveau lot ni examen d'autres notes.**
