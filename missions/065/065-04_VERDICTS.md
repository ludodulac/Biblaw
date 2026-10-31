# 🌸 BIBLAW — MISSION 065-04 — VERDICTS DU TROISIÈME LOT

**STATUT : TERMINÉE — quatre notes réexaminées, aucune authentifiée ni corrigée, quatre NON RÉSOLUES.**

## Sources et périmètre

Quatre identifiants du lot 065-04 de [065_PLAN.md](065_PLAN.md), exclusivement. Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT au contrôle initial, HEAD `b8d118742da366bbe3f1b737b11d91cd78ef00b0`. Le PDF original **n'a pas été rouvert** : les rapports ciblés 064-15/B (PDF p.2971) et 064-19/A–B (PDF p.3495) contiennent les observations visuelles antérieures établissant une unique note imprimée par paire. La disponibilité des artefacts GitHub correspondants a été vérifiée (non expirés) ; leurs ZIP n'ont pas été retéléchargés.

Quatre JSON de notes et deux JSON de psaumes ont été examinés **en lecture seule** : mêmes textes et marqueurs pour les deux membres de chaque paire, `source.pdfPage` identique, `noteIds` réciproques et pages dans le psaume. Dans chacune des deux paires, le premier ID possède `appliesTo.verse=null` et le second `verse=20`. Cette différence ne permet pas de choisir un ID canonique : aucune deuxième note imprimée n'est attestée et aucune règle de provenance ne tranche entre les extractions.

## Verdicts individuels

### 1. `book-30-psalm-215-note-004`

- **Ancien verdict : NON RÉSOLUE. Nouveau verdict : NON RÉSOLUE.**
- **Anomalie et justification :** Un seul pied imprimé n°1 de 17 tokens est établi p.2971, associé au renvoi du verset 20 (« Père Michaël »). Les deux fichiers 004 et 005 contiennent le même texte, la même page et le même marqueur. Le champ verse de 004 est null.
- **Preuves documentaires :** [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; [Actions #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177) ; artefact `12577911782` (rendu et relevé p.2971 déjà examinés en 064). `data/notes/books/book-30/book-30-psalm-215-note-004.json` (blob `b4d01b16fe5e9e2629f5d4032d6dca95d0075b3d`), `data/corpus/books/book-30/psalm-215.json` (pages source, `noteIds`) ; concurrent `book-30-psalm-215-note-005`.
- **Preuve manquante pour lever l'incertitude :** Une preuve de provenance désignant l'identifiant canonique entre 004 et 005, ainsi qu'une méthode de réconciliation des noteIds sans supprimer un lien par supposition.
- **Correction effectuée :** aucune ; données canoniques et statut `machine-extracted-needs-review` conservés.

### 2. `book-30-psalm-215-note-005`

- **Ancien verdict : NON RÉSOLUE. Nouveau verdict : NON RÉSOLUE.**
- **Anomalie et justification :** La concordance complète de 17 tokens et le rattachement au verset 20 sont documentés, mais une seule occurrence imprimée existe. Le fichier 004 revendique la même note : le verse 20 renseigné dans 005 ne suffit pas à départager les deux identifiants.
- **Preuves documentaires :** [064-15_VERDICTS.md](../064/064-15_VERDICTS.md) ; [Actions #40137565177](https://github.com/ludodulac/Biblaw/actions/runs/40137565177) ; artefact `12577911782` (rendu et relevé p.2971 déjà examinés en 064). `data/notes/books/book-30/book-30-psalm-215-note-005.json` (blob `aa1b33222e08ae532a783c372271d61a7b49200f`), `data/corpus/books/book-30/psalm-215.json` (pages source, `noteIds`) ; concurrent `book-30-psalm-215-note-004`.
- **Preuve manquante pour lever l'incertitude :** Une attribution d'identité sourcée indépendamment de l'ordre d'extraction et du seul champ verse, avec plan de mise en cohérence des références.
- **Correction effectuée :** aucune ; données canoniques et statut `machine-extracted-needs-review` conservés.

### 3. `book-35-psalm-218-note-002`

- **Ancien verdict : NON RÉSOLUE. Nouveau verdict : NON RÉSOLUE.**
- **Anomalie et justification :** L'unique pied imprimé n°1 de 45 tokens p.3495, appelé au verset 20 (« enfant »), est revendiqué à l'identique par 002 et 003. Le JSON 002 a verse null mais le même texte, marqueur et psaume.
- **Preuves documentaires :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; [Actions #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710) ; artefact `12650754088` (rendu et relevé p.3495 déjà examinés en 064). `data/notes/books/book-35/book-35-psalm-218-note-002.json` (blob `2afd3c4729ac89a1e21fa77b69af203b3d1b3ef2`), `data/corpus/books/book-35/psalm-218.json` (pages source, `noteIds`) ; concurrent `book-35-psalm-218-note-003`.
- **Preuve manquante pour lever l'incertitude :** La traçabilité prouvant quel identifiant représente la seule occurrence imprimée, puis le traitement sans perte des références noteIds.
- **Correction effectuée :** aucune ; données canoniques et statut `machine-extracted-needs-review` conservés.

### 4. `book-35-psalm-218-note-003`

- **Ancien verdict : NON RÉSOLUE. Nouveau verdict : NON RÉSOLUE.**
- **Anomalie et justification :** Le pied n°1 de 45/45 tokens et le renvoi au verset 20 sont déjà établis p.3495, mais 002 revendique exactement la même occurrence. Le champ verse 20 de 003 ne prouve pas à lui seul la préférence canonique pour cet ID.
- **Preuves documentaires :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md) ; [Actions #40326861034](https://github.com/ludodulac/Biblaw/actions/runs/40326861034) ; artefact `12651183390` (rendu et relevé p.3495 déjà examinés en 064). `data/notes/books/book-35/book-35-psalm-218-note-003.json` (blob `37bdc0453dacb9a59f18feff9ec6652ead96c5c4`), `data/corpus/books/book-35/psalm-218.json` (pages source, `noteIds`) ; concurrent `book-35-psalm-218-note-002`.
- **Preuve manquante pour lever l'incertitude :** Une preuve d'attribution canonique indépendante de la métadonnée issue de l'extraction, ainsi que la gestion sûre du second identifiant.
- **Correction effectuée :** aucune ; données canoniques et statut `machine-extracted-needs-review` conservés.

## Contrôles spécialisés

**12/12 contrôles documentaires ciblés PASS**, effectués à partir des métadonnées et rapports de preuve consultés, sans réexécuter de GitHub Actions. Contrôles : 4 IDs du seul lot 065-04, tous distincts ; 4 verdicts antérieurs NON RÉSOLUE issus de 064-15/064-19 ; égalité des textes 30/215/004–005 ; égalité des textes 35/218/002–003 ; marqueur n°1 identique pour chacune des deux paires ; même page et même psaume pour les deux membres de chaque paire ; p.2971 et p.3495 dans les pages source des psaumes ; présence des deux identifiants concurrents dans noteIds de chaque psaume ; 30/215 : verse null face à verse 20 ; 35/218 : verse null face à verse 20 ; constat source d'un unique pied de 17 tokens / 45 tokens par paire ; existence des trois artefacts utiles et quatre blobs de note distincts.

Les doublons sont préexistants ; aucun doublon, statut authentifié, correction ou référence canonique n'est introduit. Aucun workflow général relancé ou réparé.

## Clôture et garde

**065-04 : 4/4 notes réexaminées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.** Les deux identités concurrentes par pied restent non départagées.

**Cumul 065 : 12/46 notes réexaminées, 0 résolue, 46 toujours NON RÉSOLUES ; 34 notes restant à réexaminer.** Les 146 authentifications de 064 restent inchangées. Aucun fichier canonique, psaume, prière, interface ou catalogue modifié ; aucune publication, déploiement ni fusion. **STOP ; 065-05 non commencée.**
