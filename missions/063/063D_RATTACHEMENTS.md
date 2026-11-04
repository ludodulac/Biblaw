# BIBLAW — 063D — rattachements du livre 44, notes 002 à 004
*Date : 2026-10-21. Statut : TERMINÉ comme mission de **documentation**, avec 3 rattachements **NON RÉSOLUS**.*

## Verdict de rattachement

**0 psaume de rattachement positivement confirmé ; 3 rattachements NON RÉSOLUS.** Le psaume 285 du livre 44 est explicitement **exclu** pour les trois notes : son enregistrement canonique `data/corpus/books/book-44/psalm-285.json` porte `noteIds: []` et provient uniquement des pages PDF **4636–4637**, alors que les notes 002–004 proviennent d'autres sections aux pages 4653, 4720 et 4724. Les numéros présents dans le chemin/les champs `id` et `appliesTo.recordId` sont des références **d'extraction**, pas une preuve de rattachement.

| Note extraite (identifiant inchangé) | Page source | Section documentaire attestée dans 061 | Psaume exact confirmé | Verdict | Justification probante |
|---|---:|---|---|---|---|
| `book-44-psalm-285-note-002` | 4653 | Autres textes de l’Archange Michaël (pages 4653–4654) | **Aucun** | **NON RÉSOLU** (ancien `INCERTAINE`) | Rupture de rubrique typographique déjà attestée en 061 ; note extraite p. 4653 ; le supplément a été retiré sans authentifier un psaume. |
| `book-44-psalm-285-note-003` | 4720 | Autres textes de l’Archange Raphaël (pages 4720–4721) | **Aucun** | **NON RÉSOLU** (ancien `INCERTAINE`) | Rupture de rubrique typographique déjà attestée en 061 ; note extraite p. 4720 ; annexe / autre écrit, aucun numéro de psaume démontré. |
| `book-44-psalm-285-note-004` | 4724 | Autres textes de l’Archange Ouriel (pages 4724–4726) | **Aucun** | **NON RÉSOLU** (ancien `INCERTAINE`) | Rupture de rubrique typographique déjà attestée en 061 ; note extraite p. 4724 ; rien ne démontre un rattachement à un psaume précis. |

## Pièces existantes consultées (sans refaire les audits)

1. [Mission 061 — preuves des frontières](../../reports/notes-061/CONFIRMED_BOUNDARIES.md) : tableau des 5 contaminations, dont les trois lignes 44/285/002–004 ; notes nettoyées aux pages 4653–4654, 4720–4721 et 4724–4726 ; **rattachements non prouvés**. Artefact existant [Actions 39433962159](https://github.com/ludodulac/Biblaw/actions/runs/39433962159), `biblaw-notes-evidence-061`.
2. [Mission 062 — rapport](../../reports/notes-062/RAPPORT.md), section « Cas distincts : livre 44… » : 002/003/004 sont **hors** des 72 dossiers 062 et hors des 30 de son suivi ; leurs identifiants ne figurent pas dans `noteIds` du psaume 285.
3. [Mission 063 — rapport](../../reports/notes-063/RAPPORT.md), section « Vérification distincte : livre 44, psaume 285 » et [décisions 063](../../reports/notes-063/decisions.json) : les textes sont d'**autres écrits** (annexes, notamment « 7 règles fondamentales ») ; les trois verdicts restent **INCERTAINE**. Preuves déjà produites : [Actions 39574187140](https://github.com/ludodulac/Biblaw/actions/runs/39574187140), [39574713801](https://github.com/ludodulac/Biblaw/actions/runs/39574713801) et [39574989431](https://github.com/ludodulac/Biblaw/actions/runs/39574989431). Artefacts GitHub présents/non expirés le 21 octobre 2026.
4. Vérification ciblée des trois JSON `data/notes/books/book-44/book-44-psalm-285-note-00{2,3,4}.json` : `appliesTo.recordId` vaut toujours `book-44-psalm-285`, marqueur local `1`, état technique `machine-extracted-needs-review` ; ceci est une **incohérence de métadonnée non rectifiée**, non une preuve de lien. Le fichier canonique `psalm-285.json` a `noteIds: []`.

## Conclusion et limites

**Chaque exclusion de 285 est documentée ; aucun autre numéro de psaume n'est démontré.** Les sections sources ne sont pas établies comme des psaumes canoniques. Attribuer les notes à un autre psaume à partir de la seule proximité de pages serait spéculatif. Les trois fichiers restent inchangés, non publiés et au verdict **NON RÉSOLU**. La note `book-44-psalm-285-note-001` dépend exclusivement du suivi 063C : **aucun changement** de son verdict, de son fichier ni de son cas.

Aucun chargement du PDF, aucune nouvelle comparaison typographique ni correction. La mission 063D a pour seul résultat le présent registre et l'actualisation de suivi ; **063E non commencée**, PR #72 toujours DRAFT, aucune fusion ou mise en production.
