# BIBLAW — mission 061 : preuves des corrections documentaires

Le rapport source de la mission 060 est conservé dans l'artefact de GitHub Actions du run 39389492831.
L'examen ciblé des 77 notes est conservé dans l'artefact biblaw-notes-evidence-061 du run 39433962159 (77 comparaisons avec le PDF original, pages et extraits).
La lecture ciblée des limites de section du PDF est dans les journaux du run 39434402401.

## 5 contaminations confirmées corrigées

| Note | Page(s) originales du PDF | Raison de la coupure | Ancien blob Git |
|---|---|---|---|
| book-05-psalm-036-note-001 | 270-271 | Texte du psaume ajouté à la fin de la note à partir de « meilleur fruit » ; le PDF le place dans la continuation du psaume. | bd01a68338f2f170de8197abbd6c53e83c4b3a2f |
| book-22-psalm-150-note-001 | 1849-1850 | Texte principal du psaume ajouté après la note, à partir de « se propager dans tous les mondes » ; le PDF le montre au début de la p. 1850, avant le verset 33. | a5581224995b590f857acd4ddebb6e964ef0d724 |
| book-44-psalm-285-note-002 | 4653-4654 | Le PDF affiche distinctement la rubrique « autres textes de l’Archange Michaël », suivie de textes étrangers à la note. | 09d483c7f20918e3241d598774b60145df766417 |
| book-44-psalm-285-note-003 | 4720-4721 | Le PDF affiche distinctement la rubrique « autres textes de l’Archange Raphaël », suivie de versets et d'autres textes. | 0ea8784be8059f19442d8d0361c399cff8ed5e6e |
| book-44-psalm-285-note-004 | 4724-4726 | Le PDF distingue les « autres textes de l’Archange Ouriel » ; le reste provenait de ces autres textes et non de la note. | 3b33a32b160697d425891d417acdedc2d347a597 |

Le contenu qui n'appartenait pas aux notes n'a **pas** été retiré du PDF ni du corpus canonique. Les versions intégrales des fichiers extraits restent disponibles dans les blobs Git originaux (SHA ci-dessus).

## État et limites

- 77 dossiers signalés par 060 passés en revue, sans relancer l'audit des 280.
- 5 contaminations de texte corrigées dans les seuls fichiers extraits hors catalogue.
- 72 autres dossiers non corrigés faute de preuve suffisamment déterminante pour une modification sûre.
- Les trois notes du livre 44 conservent une question de rattachement : elles ne figurent pas parmi les noteIds du psaume 285 et ne doivent donc **pas** être publiées.
- Aucun des 77 dossiers n'est promu automatiquement au statut « validé ». Une confirmation éditoriale/typographique reste requise pour leur publication.
- Les 1 158 psaumes, 676 prières, 11 notes publiques, catalogues, moteur de recherche et classements restent inchangés.

## Comment consulter les preuves

PDF original : Bible essénienne (classée par livres).pdf, aux pages indiquées ci-dessus.
Artefact GitHub Actions 061 : fichier per-note-proof.json contenant pour chaque note les extraits des pages source, les alignements et les alertes.
