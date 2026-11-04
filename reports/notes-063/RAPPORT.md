# BIBLAW — MISSION 063 : preuve et décisions sur 30 + 3 notes

## Résultat

| Contrôle | Nombre |
|---|---:|
| Notes vérifiées (mission 062) | **30** |
| Rattachements distincts du livre 44 réexaminés | **3** |
| VALIDÉE sans modification | **1** |
| CORRIGÉE ET VALIDÉE | **10** |
| INCERTAINE | **22** (dont les 3 du livre 44) |
| Fichiers de notes modifiés | **11** (10 validés + note 1 livre 44 : texte corrigé, rattachement incertain) |
| Notes ajoutées au catalogue | **0** |

## Méthode et preuves

Les identifiants des 30 notes proviennent **exclusivement** des dossiers INCERTAINE du rapport 062. Trois notes supplémentaires (livre 44, psaume 285, notes 2–4) ont été examinées séparément. Aucun audit 060, 061 ou 062 n'a été recommencé.

Source exclusive : `Bible essénienne (classée par livres).pdf` dans le dépôt (4 744 pages). La vérification confronte le début ET la fin de chaque note à la typographie de bas de page dans le PDF, y compris les tirets insécables des appels de notes, la valeur du numéro *imprimé localement* (qui peut revenir à 1 sur une autre page), la page canonique et le lien `psaume.noteIds`.

Précaution supplémentaire : des fichiers extraits sont des **doublons d'une même note imprimée**. Les doublons connus ont été conservés tels quels, en INCERTAINE : un texte correct ne prouve pas l'existence de deux notes distinctes. De même, une note qui se poursuit sur une autre page n'est jamais tronquée automatiquement.

- [Preuves PDF 063 : examen ciblé des 33 notes, transcription et mise en page](https://github.com/ludodulac/Biblaw/actions/runs/39574187140)
- [Complément typographique : notes non détectées et livre 44](https://github.com/ludodulac/Biblaw/actions/runs/39574713801)
- [Preuves de segmentation des notes : tirets insécables, marqueurs, doublons, texte intégral](https://github.com/ludodulac/Biblaw/actions/runs/39574989431)
- [Rapport des 72 notes de la mission 062](../notes-062/RAPPORT.md)

## Tableau des 33 vérifications individuelles

| Identifiant | Page PDF | Anomalie initiale | Preuve examinée | Correction éventuelle | Statut final |
|---|---:|---|---|---|---|
| `book-08-psalm-050-note-001` | 485 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (163 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (163 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-16-psalm-086-note-002` | 1025 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (144 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (144 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-18-psalm-124-note-001` | 1256 | limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Note imprimée tronquée en fin de page ; continuation à vérifier** | Aucune | **INCERTAINE** |
| `book-20-psalm-104-note-001` | 1461 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (394 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (394 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-20-psalm-109-note-001` | 1480 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (104 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (104 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-20-psalm-124-note-002` | 1556 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (146 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (146 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-21-psalm-143-note-001` | 1652 | limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Note imprimée tronquée en fin de page ; continuation à vérifier** | Aucune | **INCERTAINE** |
| `book-21-psalm-150-note-001` | 1692 | typographie ou début de note non confirmé ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (150 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (150 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-23-psalm-133-note-003` | 1960 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Double possible de 'book-23-psalm-133-note-004' au même appel PDF ; extraction conservée** | Aucune | **INCERTAINE** |
| `book-25-psalm-167-note-001` | 2217 | limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Note imprimée tronquée en fin de page ; continuation à vérifier** | Aucune | **INCERTAINE** |
| `book-26-psalm-172-note-002` | 2375 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-172-note-002, book-26-psalm-172-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-172-note-003` | 2375 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-172-note-002, book-26-psalm-172-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-181-note-002` | 2415 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-181-note-002, book-26-psalm-181-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-181-note-003` | 2415 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-181-note-002, book-26-psalm-181-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-182-note-002` | 2418 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-182-note-002, book-26-psalm-182-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-182-note-003` | 2418 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-26-psalm-182-note-002, book-26-psalm-182-note-003** | Aucune | **INCERTAINE** |
| `book-26-psalm-189-note-002` | 2453 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Double possible de 'book-26-psalm-189-note-003' au même appel PDF ; extraction conservée** | Aucune | **INCERTAINE** |
| `book-27-psalm-169-note-002` | 2534 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Double possible de 'book-27-psalm-169-note-004' au même appel PDF ; extraction conservée** | Aucune | **INCERTAINE** |
| `book-28-psalm-158-note-001` | 2589 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (226 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (226 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-29-psalm-216-note-002` | 2831 | numéro imprimé différent du numéro JSON ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte PDF ne concorde pas intégralement avec la fin extraite** | Aucune | **INCERTAINE** |
| `book-30-psalm-193-note-001` | 2860 | typographie ou début de note non confirmé ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (213 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (213 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-30-psalm-200-note-002` | 2901 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Double possible de 'book-30-psalm-200-note-003' au même appel PDF ; extraction conservée** | Aucune | **INCERTAINE** |
| `book-31-psalm-201-note-002` | 3092 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-31-psalm-201-note-002, book-31-psalm-201-note-003** | Aucune | **INCERTAINE** |
| `book-31-psalm-201-note-003` | 3092 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Plusieurs JSON renvoient à une seule note imprimée : book-31-psalm-201-note-002, book-31-psalm-201-note-003** | Aucune | **INCERTAINE** |
| `book-31-psalm-203-note-001` | 3099 | limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte intégral, numéro local et psaume confirmés ; aucune correction** | Aucune | **VALIDÉE** |
| `book-32-psalm-203-note-001` | 3199 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (479 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (479 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-35-psalm-214-note-002` | 3485 | numéro imprimé différent du numéro JSON ; page PDF non attribuée au psaume | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Page PDF non rattachée au psaume actuellement indiqué** | Aucune | **INCERTAINE** |
| `book-36-psalm-233-note-001` | 3651 | appel de note non identifié dans la mise en page PDF ; page PDF non attribuée au psaume ; limites du texte non prouvées | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte parasite final retiré (586 caractères) ; note, numéro local et psaume confirmés** | Suffixe parasite retiré (586 car.) | **CORRIGÉE ET VALIDÉE** |
| `book-37-psalm-250-note-002` | 3690 | numéro imprimé différent du numéro JSON | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Double possible de 'book-37-psalm-250-note-003' au même appel PDF ; extraction conservée** | Aucune | **INCERTAINE** |
| `book-44-psalm-285-note-001` | 4648 | rattachement canonique non réciproque ; page PDF non attribuée au psaume | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Suffixe hors note retiré (197 caractères) ; texte d’une section distincte, pas du psaume 285** | Suffixe parasite retiré (197 car.), rattachement non validé | **INCERTAINE** |
| `book-44-psalm-285-note-002` | 4653 | 061 : texte nettoyé, rattachement au psaume 285 non démontré | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte déjà corrigé en 061 et conservé ; annexe / autre texte distinct, pas du psaume 285** | Aucune | **INCERTAINE** |
| `book-44-psalm-285-note-003` | 4720 | 061 : texte nettoyé, rattachement au psaume 285 non démontré | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte déjà corrigé en 061 et conservé ; annexe / autre texte distinct, pas du psaume 285** | Aucune | **INCERTAINE** |
| `book-44-psalm-285-note-004` | 4724 | 061 : texte nettoyé, rattachement au psaume 285 non démontré | Page PDF à contrôler : note imprimée non confirmée. **Conclusion : Texte déjà corrigé en 061 et conservé ; annexe / autre texte distinct, pas du psaume 285** | Aucune | **INCERTAINE** |

## Vérification distincte : livre 44, psaume 285

Le psaume canonique 285 du livre 44 n'occupe que les pages **4636–4637** du PDF et ne référence aucune note (`noteIds: []`). Les notes 2, 3 et 4 apparaissent respectivement en pages **4653**, **4720** et **4724**, dans d'autres écrits (notamment les textes annexés et les « 7 règles fondamentales »). Elles ne peuvent pas être rattachées au psaume 285. Les corrections de texte de la mission 061 sont **préservées**, les trois fichiers restent **INCERTAINE**. Aucun nouvel identifiant de psaume n'a été inventé.

La note 1 (p. 4648) relève elle aussi d'un texte distinct (« Dialogue avec Dieu dans le feu ... »). Son passage parasite a été éliminé avec preuve PDF ; son rattachement reste **INCERTAINE**.

## Sécurité

Les **1 158 psaumes**, **676 prières** et **11 notes publiques** restent inchangés. Aucun texte nouveau n'est ajouté au catalogue, aucun changement de recherche, suggestion, interface ou thème. La PR #72 demeure DRAFT et aucun déploiement ni fusion n'a été effectué.

