# BIBLAW — 063B — dix verdicts documentés (2026-10-21)

**État : TERMINÉ — suivi documentaire.** Dix notes du lot 063B ont été examinées **antérieurement** dans la mission historique 063. Ici : **0 validation nouvelle, 0 correction nouvelle**, un statut **CORRIGÉE ET VALIDÉE antérieur**, neuf **NON RÉSOLUES** (ancien statut `INCERTAINE`). Aucun texte de note n'a été modifié.

## Sources et limites de preuve

- [Rapport 063 antérieur](../../reports/notes-063/RAPPORT.md), rubrique « Tableau des 33 vérifications individuelles », identifiants 11–20 ; [décisions source 063](../../reports/notes-063/decisions.json), `rows[10:20]` : preuve écrite, pages PDF, marqueurs, motifs et corrections de l'audit historique.
- [Rapport 062](../../reports/notes-062/RAPPORT.md) et [décisions 062](../../reports/notes-062/decisions.json) : origine du lot de notes incertaines ; [PROGRESS.md](PROGRESS.md) : découpage autorisé.
- Travaux PDF préexistants : [Actions 39574187140](https://github.com/ludodulac/Biblaw/actions/runs/39574187140), [39574713801](https://github.com/ludodulac/Biblaw/actions/runs/39574713801), [39574989431](https://github.com/ludodulac/Biblaw/actions/runs/39574989431), tous SUCCESS au contrôle GitHub 063B. Trois artefacts conservés/non expirés, consultables via les runs (expiration annoncée le 19 janvier 2027).
- Précision : les artefacts bruts sont référencés et leur existence vérifiée ; aucune nouvelle inspection indépendante du PDF ou téléchargement de ces artefacts n'a été réalisée. Le statut de la note 28 est **repris tel quel** du rapport 063, qui décrit la preuve de correction ; son fichier courant `data/notes/books/book-28/book-28-psalm-158-note-001.json` a été lu de façon ciblée et existe.
- Pour les neuf autres, les éléments historiques **ne suffisent pas à valider** un second appel imprimé ni à corriger le texte sans hypothèse. Les conserver intégralement et non publiées.

## Registre 063B — verdict + preuve + incertitude pour chacun

| N° | Note ID | Page originale | Verdict (hérité de 063) | Correction historique | Preuve existante et incertitude résiduelle |
|---:|---|---:|---|---|---|
| 1 | `book-26-psalm-172-note-002` | 2375 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2375, appel imprimé déclaré 1, typographie 9 pt ; Le même appel de note imprimé est revendiqué par 002 et 003 ; la distinction entre deux notes autonomes n'est pas démontrée. |
| 2 | `book-26-psalm-172-note-003` | 2375 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2375, appel imprimé déclaré 1, typographie 9 pt ; Le même appel de note imprimé est revendiqué par 002 et 003 ; la distinction entre deux notes autonomes n'est pas démontrée. |
| 3 | `book-26-psalm-181-note-002` | 2415 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2415, appel imprimé déclaré 1, typographie 9 pt ; Un seul appel imprimé semble correspondre à 002 et 003 ; pas de preuve de deux notes distinctes. |
| 4 | `book-26-psalm-181-note-003` | 2415 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2415, appel imprimé déclaré 1, typographie 9 pt ; Un seul appel imprimé semble correspondre à 002 et 003 ; pas de preuve de deux notes distinctes. |
| 5 | `book-26-psalm-182-note-002` | 2418 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2418, appel imprimé déclaré 1, typographie 9 pt ; 002 et 003 renvoient à une même note imprimée ; identification univoque manquante. |
| 6 | `book-26-psalm-182-note-003` | 2418 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2418, appel imprimé déclaré 1, typographie 9 pt ; 002 et 003 renvoient à une même note imprimée ; identification univoque manquante. |
| 7 | `book-26-psalm-189-note-002` | 2453 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2453, appel imprimé déclaré 1, typographie 9 pt ; Double potentiel de note-003, numéro imprimé divergent ; ne pas supprimer ni fusionner sans preuve. |
| 8 | `book-27-psalm-169-note-002` | 2534 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2534, appel imprimé déclaré 1, typographie 9 pt ; Double potentiel de note-004, numéro imprimé divergent ; ne pas supprimer ni fusionner sans preuve. |
| 9 | `book-28-psalm-158-note-001` | 2589 | **CORRIGÉE ET VALIDÉE (historique 063)** | Suffixe parasite retiré (226 car.) (063 antérieure) | Rapport 063 p. 2589, appel imprimé déclaré 1, typographie 9 pt ; Le rapport 063 atteste la note imprimée, son numéro local et son psaume ; suffixe parasite de 226 caractères retiré lors de 063 ; aucune correction supplémentaire en 063B. |
| 10 | `book-29-psalm-216-note-002` | 2831 | **NON RÉSOLUE (INCERTAINE selon 063)** | Aucune | Rapport 063 p. 2831, appel imprimé déclaré 1, typographie 9 pt ; Le texte extrait ne correspond pas intégralement à sa fin imprimée ; délimitation et numéro non confirmés. |

## Décision opérationnelle

- **1 seule note** historiquement CORRIGÉE ET VALIDÉE : `book-28-psalm-158-note-001`, page 2589, suffixe parasite de **226 caractères** déjà éliminé. Aucun nouveau statut « validé » en 063B.
- **8 notes** avec doubles d'appel / numéro non démontré ; **1 note** avec discordance de fin de texte PDF ; **9 NON RÉSOLUES**, sans fusion, suppression, renumérotation ni correction hypothétique.
- Origine des motifs : `reason`, `claimDuplicate` et `siblingDuplicate` de `reports/notes-063/decisions.json`. Pour les cas à deux fichiers JSON, les dossiers sont **distincts mais liés**, sans création de preuve supplémentaire.
- Aucune opération sur 060–063A, sur les quatre incertaines de 063A, sur le PDF, sur les 1 158 psaumes, les 676 prières, le catalogue et les 11 notes publiques. PR DRAFT inchangée, sans fusion ni déploiement.
- **Prochaine mission : 063C**, non commencée.
