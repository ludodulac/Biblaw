# BIBLAW — 064-SETUP — plan d'authentification éditoriale

**Créé le 2026-10-22. STATUT : PLANIFIÉ — AUCUNE VALIDATION EN 064-SETUP.**  
Dépôt : `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 toujours DRAFT. HEAD d'entrée : `b0cb9cf2a3b634de6138adbe8387c8a31e178ab5`.

## 1. Source historique et catégorie **exacte** reconstituée

Source autoritative : mission 060, [GitHub Actions run 39389492831](https://github.com/ludodulac/Biblaw/actions/runs/39389492831), artefact `biblaw-notes-audit-060` (fichiers `RAPPORT.md`, `summary.json`, `per-note.json`, `per-note.csv`). La méthode de catégorisation est celle de `scripts/audit_extracted_notes_060.py` ; il ne s'agit **pas** d'une catégorie « sans aucune alerte ».

**Critère 060 :** note non publiée (`is_published=false`), `pdf_text_coverage >= 0.8`, et **aucun indicateur structurel bloquant** parmi `missing_canonical_psalm, no_reciprocal_note_id, archangel_mismatch, book_number_mismatch, id_does_not_match_filename, record_type_not_note, invalid_source_marker, different_provenance_document, invalid_pdf_source_page, pdf_page_outside_psalm_source, empty_or_very_short_text, possible_section_text_contamination, published_note_text_differs`. Indice automatisé **insuffisant à lui seul** pour authentifier une note.

Sur les **280 notes extraites** de 060 : **11 déjà publiques** (hors catégorie), **269 non publiées** ; parmi celles-ci **192 candidates fortement corroborées / contrôle éditorial restant**, **77 autres dossiers initialement demandant examen plus poussé** (déjà repris dans les missions 061–063, à ne pas réauditer ici). Dans la catégorie des 192 : **141 sans alerte 060**, **51 avec au moins une alerte non bloquante** (**43** alertes de divergence entre numéro local imprimé et ordinal de fichier ; **11** alertes de texte inhabituellement long ; **3 candidats** cumulent les deux). Ces alertes restent des points à vérifier éditorialement, jamais une validation.

**Source de la ligne de preuve :** la colonne `Référence 060` pointe vers la **position 1-based** dans `per-note.json` / `per-note.csv` de l'artefact 060, avec la page PDF **rapportée par 060**. La clé documentaire est l'identifiant intégral, vérifiable dans ce fichier ; aucune page du PDF n'a été ouverte pendant 064-SETUP. **192 identifiants distincts** vérifiés dans leur **ordre original** (empreinte de contrôle FNV-1a 32 bits de la chaîne des 192 IDs séparés par virgule : `2719186`).

## 2. Exclusions par authentification antérieure

| Provenance | Déjà authentifiées dans les sources de suivi | En intersection avec ces 192 | Décision |
|---|---:|---:|---|
| Mission 062 : `reports/notes-062/decisions.json` | 42 corrigées et validées | **0** | Aucune de ces 42 n'est dans les 192 ; statut 062 préservé |
| Mission 063 : [bilan 063E](../063/063E_BILAN_FINAL.md) | 11 authentifiées (1 + 10) | **0** | Aucune de ces 11 n'est dans les 192 ; statut 063 préservé |
| 062 / 063 : cas explicitement incertains | 30 du suivi 062, dont 19 encore non résolues en 063 | **0** | Hors du nouveau plan ; ne pas recontrôler |
| Publiées avant 060 (constat de l'inventaire 060) | 11 notes publiques | **0** | Déjà publiques, explicitement exclues par `is_published=false` |

**Authentifiées à exclure de la catégorie 192 : 0.** **À authentifier : 192** ; **lots nécessaires : 20** (19 × 10 + 1 × 2). Les 42 + 11 authentifications historiques et les 11 notes publiques sont citées pour contrôle **sans les ajouter** aux 192 ni mélanger les dénominateurs ; pour leurs identifiants/verdicts, se référer aux registres historiques indiqués.

## 3. Vigilances documentaires particulières

- **5 candidats 060** nécessitent un contrôle prioritaire d'unicité face à un **autre identifiant NON RÉSOLU de 063** (pas un doublon démontré) : `book-23-psalm-133-note-004` face à `book-23-psalm-133-note-003` ; `book-26-psalm-189-note-003` face à `book-26-psalm-189-note-002` ; `book-27-psalm-169-note-004` face à `book-27-psalm-169-note-002` ; `book-30-psalm-200-note-003` face à `book-30-psalm-200-note-002` ; `book-37-psalm-250-note-003` face à `book-37-psalm-250-note-002`. **Ne pas retirer de la liste ni valider automatiquement** ; distinguer les appels imprimés lors des futures missions de lots.
- D'autres notes 060 appartiennent aux **mêmes psaumes** que des cas 063 incertains mais portent des identifiants distincts : une proximité de psaume n'est pas un doublon par elle-même. Exemple : `book-26-psalm-172-note-001` / 063 notes 002–003 ; ne pas conclure par analogie.
- Certains numéros de page apparaissent hors de l'ordre numérique entre notes du même psaume : **conserver sans tri secondaire** l'ordre de l'inventaire 060 ; ne pas le « réparer » sans preuve.
- **Aucune divergence de total :** l'extraction retrouvée reproduit le compteur historique de **192**. **Aucun identifiant dupliqué** dans les 192, ni avec les lots validés 062–063 / les incertitudes 063.
- **À la reprise** : relever les preuves de chaque note avant de changer `À AUTHENTIFIER` ; aucun changement au catalogue ni aux métadonnées par ce plan.

## 4. Lots de 10 maximum — registre individuel

**Légende :** chaque ligne est attribuée au lot indiqué par son titre ; `À AUTHENTIFIER` = **non authentifiée au niveau éditorial**, même si la machine avait signalé une bonne concordance. `Livre` et `Psaume présumé` proviennent de l'ID d'extraction et **ne constituent pas une attribution humaine validée**. Les alertes sont celles du rapport 060 + renvoi prudent aux dossiers 063. Chaque ID figure dans **un seul lot**.

### Lot 064-01 — 10 notes (book-01-psalm-004-note-001 → book-04-psalm-012-note-003)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-01-psalm-004-note-001` | 1 | 4 | 1 | `per-note.json[1]`, PDF p.70 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-01-psalm-004-note-002` | 1 | 4 | 2 | `per-note.json[2]`, PDF p.70 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-01-psalm-004-note-003` | 1 | 4 | 3 | `per-note.json[3]`, PDF p.70 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-01-psalm-010-note-001` | 1 | 10 | 1 | `per-note.json[4]`, PDF p.82 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-02-psalm-003-note-001` | 2 | 3 | 1 | `per-note.json[5]`, PDF p.105 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-02-psalm-012-note-001` | 2 | 12 | 1 | `per-note.json[6]`, PDF p.119 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-03-psalm-004-note-001` | 3 | 4 | 1 | `per-note.json[7]`, PDF p.150 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-04-psalm-012-note-001` | 4 | 12 | 1 | `per-note.json[8]`, PDF p.211 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-04-psalm-012-note-002` | 4 | 12 | 2 | `per-note.json[9]`, PDF p.211 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-04-psalm-012-note-003` | 4 | 12 | 3 | `per-note.json[10]`, PDF p.211 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-02 — 10 notes (book-05-psalm-035-note-001 → book-07-psalm-032-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-05-psalm-035-note-001` | 5 | 35 | 1 | `per-note.json[11]`, PDF p.268 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-06-psalm-034-note-001` | 6 | 34 | 1 | `per-note.json[13]`, PDF p.314 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-06-psalm-036-note-001` | 6 | 36 | 1 | `per-note.json[14]`, PDF p.318 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-06-psalm-040-note-002` | 6 | 40 | 2 | `per-note.json[16]`, PDF p.325 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-06-psalm-040-note-003` | 6 | 40 | 3 | `per-note.json[17]`, PDF p.325 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-06-psalm-045-note-001` | 6 | 45 | 1 | `per-note.json[18]`, PDF p.334 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-024-note-001` | 7 | 24 | 1 | `per-note.json[19]`, PDF p.357 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-024-note-002` | 7 | 24 | 2 | `per-note.json[20]`, PDF p.357 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-029-note-001` | 7 | 29 | 1 | `per-note.json[24]`, PDF p.369 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-032-note-001` | 7 | 32 | 1 | `per-note.json[25]`, PDF p.378 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-03 — 10 notes (book-07-psalm-032-note-002 → book-08-psalm-025-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-07-psalm-032-note-002` | 7 | 32 | 2 | `per-note.json[26]`, PDF p.381 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-032-note-003` | 7 | 32 | 3 | `per-note.json[27]`, PDF p.381 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-034-note-001` | 7 | 34 | 1 | `per-note.json[28]`, PDF p.384 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-035-note-003` | 7 | 35 | 3 | `per-note.json[31]`, PDF p.387 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-035-note-004` | 7 | 35 | 4 | `per-note.json[32]`, PDF p.387 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-035-note-005` | 7 | 35 | 5 | `per-note.json[33]`, PDF p.387 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-047-note-001` | 7 | 47 | 1 | `per-note.json[38]`, PDF p.415 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-07-psalm-047-note-002` | 7 | 47 | 2 | `per-note.json[39]`, PDF p.416 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-07-psalm-047-note-003` | 7 | 47 | 3 | `per-note.json[40]`, PDF p.416 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-08-psalm-025-note-001` | 8 | 25 | 1 | `per-note.json[41]`, PDF p.431 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-04 — 10 notes (book-08-psalm-025-note-002 → book-09-psalm-074-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-08-psalm-025-note-002` | 8 | 25 | 2 | `per-note.json[42]`, PDF p.432 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-08-psalm-025-note-003` | 8 | 25 | 3 | `per-note.json[43]`, PDF p.432 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-08-psalm-031-note-001` | 8 | 31 | 1 | `per-note.json[44]`, PDF p.444 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-08-psalm-033-note-001` | 8 | 33 | 1 | `per-note.json[45]`, PDF p.448 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-08-psalm-037-note-001` | 8 | 37 | 1 | `per-note.json[46]`, PDF p.457 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-08-psalm-041-note-001` | 8 | 41 | 1 | `per-note.json[47]`, PDF p.465 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-09-psalm-055-note-001` | 9 | 55 | 1 | `per-note.json[49]`, PDF p.512 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-09-psalm-062-note-001` | 9 | 62 | 1 | `per-note.json[51]`, PDF p.528 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-09-psalm-070-note-001` | 9 | 70 | 1 | `per-note.json[52]`, PDF p.545 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-09-psalm-074-note-001` | 9 | 74 | 1 | `per-note.json[53]`, PDF p.551 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-05 — 10 notes (book-09-psalm-074-note-002 → book-12-psalm-077-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-09-psalm-074-note-002` | 9 | 74 | 2 | `per-note.json[54]`, PDF p.551 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-10-psalm-059-note-001` | 10 | 59 | 1 | `per-note.json[56]`, PDF p.574 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-10-psalm-063-note-001` | 10 | 63 | 1 | `per-note.json[57]`, PDF p.584 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-10-psalm-068-note-001` | 10 | 68 | 1 | `per-note.json[58]`, PDF p.593 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-11-psalm-074-note-001` | 11 | 74 | 1 | `per-note.json[61]`, PDF p.690 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-12-psalm-057-note-001` | 12 | 57 | 1 | `per-note.json[62]`, PDF p.712 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-12-psalm-057-note-002` | 12 | 57 | 2 | `per-note.json[63]`, PDF p.713 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-12-psalm-060-note-001` | 12 | 60 | 1 | `per-note.json[64]`, PDF p.722 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-12-psalm-064-note-001` | 12 | 64 | 1 | `per-note.json[65]`, PDF p.731 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-12-psalm-077-note-001` | 12 | 77 | 1 | `per-note.json[66]`, PDF p.764 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-06 — 10 notes (book-13-psalm-081-note-001 → book-14-psalm-109-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-13-psalm-081-note-001` | 13 | 81 | 1 | `per-note.json[67]`, PDF p.778 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-13-psalm-099-note-001` | 13 | 99 | 1 | `per-note.json[68]`, PDF p.819 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-13-psalm-100-note-001` | 13 | 100 | 1 | `per-note.json[69]`, PDF p.822 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-086-note-001` | 14 | 86 | 1 | `per-note.json[70]`, PDF p.844 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-087-note-001` | 14 | 87 | 1 | `per-note.json[71]`, PDF p.847 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-099-note-001` | 14 | 99 | 1 | `per-note.json[73]`, PDF p.881 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-099-note-002` | 14 | 99 | 2 | `per-note.json[74]`, PDF p.881 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-100-note-001` | 14 | 100 | 1 | `per-note.json[75]`, PDF p.884 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-14-psalm-107-note-001` | 14 | 107 | 1 | `per-note.json[76]`, PDF p.904 | **À AUTHENTIFIER** | note longue |
| `book-14-psalm-109-note-001` | 14 | 109 | 1 | `per-note.json[77]`, PDF p.907 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-07 — 10 notes (book-14-psalm-110-note-001 → book-16-psalm-086-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-14-psalm-110-note-001` | 14 | 110 | 1 | `per-note.json[78]`, PDF p.908 | **À AUTHENTIFIER** | note longue |
| `book-15-psalm-077-note-001` | 15 | 77 | 1 | `per-note.json[79]`, PDF p.923 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-078-note-001` | 15 | 78 | 1 | `per-note.json[80]`, PDF p.926 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-078-note-002` | 15 | 78 | 2 | `per-note.json[81]`, PDF p.926 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-078-note-004` | 15 | 78 | 4 | `per-note.json[82]`, PDF p.927 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-15-psalm-096-note-001` | 15 | 96 | 1 | `per-note.json[83]`, PDF p.982 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-100-note-001` | 15 | 100 | 1 | `per-note.json[84]`, PDF p.990 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-101-note-001` | 15 | 101 | 1 | `per-note.json[85]`, PDF p.992 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-15-psalm-101-note-002` | 15 | 101 | 2 | `per-note.json[86]`, PDF p.992 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-16-psalm-086-note-001` | 16 | 86 | 1 | `per-note.json[87]`, PDF p.1024 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-08 — 10 notes (book-16-psalm-090-note-001 → book-19-psalm-112-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-16-psalm-090-note-001` | 16 | 90 | 1 | `per-note.json[89]`, PDF p.1033 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-16-psalm-090-note-002` | 16 | 90 | 2 | `per-note.json[90]`, PDF p.1034 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-16-psalm-095-note-001` | 16 | 95 | 1 | `per-note.json[91]`, PDF p.1046 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-16-psalm-098-note-001` | 16 | 98 | 1 | `per-note.json[92]`, PDF p.1053 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-17-psalm-115-note-001` | 17 | 115 | 1 | `per-note.json[96]`, PDF p.1122 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-18-psalm-129-note-001` | 18 | 129 | 1 | `per-note.json[105]`, PDF p.1284 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-18-psalm-137-note-001` | 18 | 137 | 1 | `per-note.json[106]`, PDF p.1326 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-107-note-001` | 19 | 107 | 1 | `per-note.json[108]`, PDF p.1357 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-111-note-001` | 19 | 111 | 1 | `per-note.json[109]`, PDF p.1373 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-112-note-001` | 19 | 112 | 1 | `per-note.json[110]`, PDF p.1377 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-09 — 10 notes (book-19-psalm-113-note-001 → book-21-psalm-137-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-19-psalm-113-note-001` | 19 | 113 | 1 | `per-note.json[111]`, PDF p.1383 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-118-note-001` | 19 | 118 | 1 | `per-note.json[112]`, PDF p.1407 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-119-note-001` | 19 | 119 | 1 | `per-note.json[113]`, PDF p.1413 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-19-psalm-126-note-001` | 19 | 126 | 1 | `per-note.json[114]`, PDF p.1445 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-20-psalm-110-note-001` | 20 | 110 | 1 | `per-note.json[117]`, PDF p.1487 | **À AUTHENTIFIER** | note longue |
| `book-20-psalm-117-note-001` | 20 | 117 | 1 | `per-note.json[118]`, PDF p.1518 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-20-psalm-124-note-001` | 20 | 124 | 1 | `per-note.json[119]`, PDF p.1554 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-20-psalm-129-note-001` | 20 | 129 | 1 | `per-note.json[121]`, PDF p.1577 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-20-psalm-129-note-002` | 20 | 129 | 2 | `per-note.json[122]`, PDF p.1579 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-21-psalm-137-note-001` | 21 | 137 | 1 | `per-note.json[123]`, PDF p.1619 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-10 — 10 notes (book-21-psalm-143-note-003 → book-21-psalm-164-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-21-psalm-143-note-003` | 21 | 143 | 3 | `per-note.json[127]`, PDF p.1654 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-21-psalm-143-note-004` | 21 | 143 | 4 | `per-note.json[128]`, PDF p.1653 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-21-psalm-149-note-001` | 21 | 149 | 1 | `per-note.json[129]`, PDF p.1684 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-150-note-002` | 21 | 150 | 2 | `per-note.json[131]`, PDF p.1692 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-157-note-001` | 21 | 157 | 1 | `per-note.json[132]`, PDF p.1726 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-160-note-001` | 21 | 160 | 1 | `per-note.json[133]`, PDF p.1747 | **À AUTHENTIFIER** | note longue |
| `book-21-psalm-161-note-001` | 21 | 161 | 1 | `per-note.json[134]`, PDF p.1753 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-162-note-001` | 21 | 162 | 1 | `per-note.json[135]`, PDF p.1759 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-163-note-001` | 21 | 163 | 1 | `per-note.json[136]`, PDF p.1766 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-21-psalm-164-note-001` | 21 | 164 | 1 | `per-note.json[137]`, PDF p.1769 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-11 — 10 notes (book-22-psalm-139-note-001 → book-23-psalm-133-note-004)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-22-psalm-139-note-001` | 22 | 139 | 1 | `per-note.json[138]`, PDF p.1785 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-22-psalm-155-note-001` | 22 | 155 | 1 | `per-note.json[141]`, PDF p.1876 | **À AUTHENTIFIER** | note longue |
| `book-22-psalm-159-note-001` | 22 | 159 | 1 | `per-note.json[143]`, PDF p.1896 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-22-psalm-163-note-001` | 22 | 163 | 1 | `per-note.json[144]`, PDF p.1914 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-23-psalm-128-note-001` | 23 | 128 | 1 | `per-note.json[145]`, PDF p.1929 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-23-psalm-129-note-001` | 23 | 129 | 1 | `per-note.json[146]`, PDF p.1935 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-23-psalm-129-note-002` | 23 | 129 | 2 | `per-note.json[147]`, PDF p.1935 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-23-psalm-129-note-003` | 23 | 129 | 3 | `per-note.json[148]`, PDF p.1936 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; note longue |
| `book-23-psalm-129-note-004` | 23 | 129 | 4 | `per-note.json[149]`, PDF p.1936 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-23-psalm-133-note-004` | 23 | 133 | 4 | `per-note.json[154]`, PDF p.1960 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; ⚠️ note jumelle potentielle du dossier 063 non résolu |

### Lot 064-12 — 10 notes (book-23-psalm-145-note-001 → book-26-psalm-189-note-003)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-23-psalm-145-note-001` | 23 | 145 | 1 | `per-note.json[156]`, PDF p.2020 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-23-psalm-146-note-001` | 23 | 146 | 1 | `per-note.json[157]`, PDF p.2023 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-24-psalm-141-note-001` | 24 | 141 | 1 | `per-note.json[159]`, PDF p.2134 | **À AUTHENTIFIER** | note longue |
| `book-26-psalm-169-note-001` | 26 | 169 | 1 | `per-note.json[164]`, PDF p.2361 | **À AUTHENTIFIER** | note longue |
| `book-26-psalm-172-note-001` | 26 | 172 | 1 | `per-note.json[165]`, PDF p.2373 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-26-psalm-176-note-001` | 26 | 176 | 1 | `per-note.json[168]`, PDF p.2392 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-26-psalm-178-note-001` | 26 | 178 | 1 | `per-note.json[169]`, PDF p.2397 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-26-psalm-181-note-001` | 26 | 181 | 1 | `per-note.json[170]`, PDF p.2412 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-26-psalm-189-note-001` | 26 | 189 | 1 | `per-note.json[177]`, PDF p.2452 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-26-psalm-189-note-003` | 26 | 189 | 3 | `per-note.json[179]`, PDF p.2453 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; ⚠️ note jumelle potentielle du dossier 063 non résolu |

### Lot 064-13 — 10 notes (book-27-psalm-158-note-001 → book-28-psalm-178-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-27-psalm-158-note-001` | 27 | 158 | 1 | `per-note.json[180]`, PDF p.2485 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-27-psalm-164-note-001` | 27 | 164 | 1 | `per-note.json[181]`, PDF p.2512 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-27-psalm-169-note-001` | 27 | 169 | 1 | `per-note.json[182]`, PDF p.2533 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-27-psalm-169-note-003` | 27 | 169 | 3 | `per-note.json[184]`, PDF p.2536 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-27-psalm-169-note-004` | 27 | 169 | 4 | `per-note.json[185]`, PDF p.2534 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; ⚠️ note jumelle potentielle du dossier 063 non résolu |
| `book-27-psalm-169-note-005` | 27 | 169 | 5 | `per-note.json[186]`, PDF p.2536 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-27-psalm-176-note-001` | 27 | 176 | 1 | `per-note.json[187]`, PDF p.2564 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-27-psalm-177-note-001` | 27 | 177 | 1 | `per-note.json[188]`, PDF p.2570 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-28-psalm-175-note-001` | 28 | 175 | 1 | `per-note.json[190]`, PDF p.2673 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-28-psalm-178-note-001` | 28 | 178 | 1 | `per-note.json[191]`, PDF p.2690 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-14 — 10 notes (book-29-psalm-194-note-001 → book-29-psalm-217-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-29-psalm-194-note-001` | 29 | 194 | 1 | `per-note.json[192]`, PDF p.2723 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-195-note-001` | 29 | 195 | 1 | `per-note.json[193]`, PDF p.2727 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-199-note-001` | 29 | 199 | 1 | `per-note.json[194]`, PDF p.2748 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-199-note-002` | 29 | 199 | 2 | `per-note.json[195]`, PDF p.2751 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-29-psalm-199-note-003` | 29 | 199 | 3 | `per-note.json[196]`, PDF p.2750 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-29-psalm-200-note-001` | 29 | 200 | 1 | `per-note.json[197]`, PDF p.2757 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-212-note-001` | 29 | 212 | 1 | `per-note.json[200]`, PDF p.2814 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-216-note-001` | 29 | 216 | 1 | `per-note.json[201]`, PDF p.2830 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-29-psalm-216-note-003` | 29 | 216 | 3 | `per-note.json[203]`, PDF p.2831 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-29-psalm-217-note-001` | 29 | 217 | 1 | `per-note.json[204]`, PDF p.2833 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-15 — 10 notes (book-30-psalm-192-note-001 → book-30-psalm-215-note-005)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-30-psalm-192-note-001` | 30 | 192 | 1 | `per-note.json[205]`, PDF p.2854 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-196-note-001` | 30 | 196 | 1 | `per-note.json[207]`, PDF p.2873 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-200-note-001` | 30 | 200 | 1 | `per-note.json[208]`, PDF p.2897 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-200-note-003` | 30 | 200 | 3 | `per-note.json[210]`, PDF p.2901 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; ⚠️ note jumelle potentielle du dossier 063 non résolu |
| `book-30-psalm-211-note-001` | 30 | 211 | 1 | `per-note.json[211]`, PDF p.2953 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-215-note-001` | 30 | 215 | 1 | `per-note.json[212]`, PDF p.2969 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-215-note-002` | 30 | 215 | 2 | `per-note.json[213]`, PDF p.2969 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-215-note-003` | 30 | 215 | 3 | `per-note.json[214]`, PDF p.2969 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-30-psalm-215-note-004` | 30 | 215 | 4 | `per-note.json[215]`, PDF p.2971 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-30-psalm-215-note-005` | 30 | 215 | 5 | `per-note.json[216]`, PDF p.2971 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |

### Lot 064-16 — 10 notes (book-31-psalm-181-note-001 → book-32-psalm-185-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-31-psalm-181-note-001` | 31 | 181 | 1 | `per-note.json[217]`, PDF p.2987 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-31-psalm-182-note-001` | 31 | 182 | 1 | `per-note.json[218]`, PDF p.2994 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-31-psalm-184-note-001` | 31 | 184 | 1 | `per-note.json[219]`, PDF p.3005 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-31-psalm-189-note-001` | 31 | 189 | 1 | `per-note.json[220]`, PDF p.3028 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-31-psalm-190-note-001` | 31 | 190 | 1 | `per-note.json[221]`, PDF p.3034 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-31-psalm-201-note-001` | 31 | 201 | 1 | `per-note.json[222]`, PDF p.3090 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-182-note-001` | 32 | 182 | 1 | `per-note.json[226]`, PDF p.3113 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-182-note-002` | 32 | 182 | 2 | `per-note.json[227]`, PDF p.3114 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-32-psalm-183-note-001` | 32 | 183 | 1 | `per-note.json[228]`, PDF p.3119 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-185-note-001` | 32 | 185 | 1 | `per-note.json[229]`, PDF p.3127 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-17 — 10 notes (book-32-psalm-185-note-002 → book-32-psalm-205-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-32-psalm-185-note-002` | 32 | 185 | 2 | `per-note.json[230]`, PDF p.3129 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-32-psalm-191-note-001` | 32 | 191 | 1 | `per-note.json[231]`, PDF p.3154 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-194-note-001` | 32 | 194 | 1 | `per-note.json[232]`, PDF p.3165 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-194-note-002` | 32 | 194 | 2 | `per-note.json[233]`, PDF p.3166 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-32-psalm-195-note-001` | 32 | 195 | 1 | `per-note.json[234]`, PDF p.3167 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-197-note-001` | 32 | 197 | 1 | `per-note.json[235]`, PDF p.3174 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-197-note-002` | 32 | 197 | 2 | `per-note.json[236]`, PDF p.3175 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-32-psalm-199-note-001` | 32 | 199 | 1 | `per-note.json[237]`, PDF p.3181 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-32-psalm-203-note-002` | 32 | 203 | 2 | `per-note.json[239]`, PDF p.3201 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-32-psalm-205-note-001` | 32 | 205 | 1 | `per-note.json[240]`, PDF p.3212 | **À AUTHENTIFIER** | note longue |

### Lot 064-18 — 10 notes (book-33-psalm-228-note-001 → book-35-psalm-209-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-33-psalm-228-note-001` | 33 | 228 | 1 | `per-note.json[241]`, PDF p.3258 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-33-psalm-230-note-001` | 33 | 230 | 1 | `per-note.json[242]`, PDF p.3267 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-33-psalm-230-note-002` | 33 | 230 | 2 | `per-note.json[243]`, PDF p.3268 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-33-psalm-230-note-003` | 33 | 230 | 3 | `per-note.json[244]`, PDF p.3268 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-33-psalm-243-note-001` | 33 | 243 | 1 | `per-note.json[247]`, PDF p.3314 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-34-psalm-218-note-001` | 34 | 218 | 1 | `per-note.json[248]`, PDF p.3326 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-34-psalm-218-note-002` | 34 | 218 | 2 | `per-note.json[249]`, PDF p.3326 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-34-psalm-228-note-001` | 34 | 228 | 1 | `per-note.json[251]`, PDF p.3377 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-34-psalm-242-note-001` | 34 | 242 | 1 | `per-note.json[252]`, PDF p.3440 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-35-psalm-209-note-001` | 35 | 209 | 1 | `per-note.json[254]`, PDF p.3460 | **À AUTHENTIFIER** | Alerte 060 : aucune |

### Lot 064-19 — 10 notes (book-35-psalm-213-note-002 → book-37-psalm-250-note-003)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-35-psalm-213-note-002` | 35 | 213 | 2 | `per-note.json[256]`, PDF p.3479 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; note longue |
| `book-35-psalm-213-note-003` | 35 | 213 | 3 | `per-note.json[257]`, PDF p.3479 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; note longue |
| `book-35-psalm-214-note-001` | 35 | 214 | 1 | `per-note.json[258]`, PDF p.3481 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-35-psalm-215-note-001` | 35 | 215 | 1 | `per-note.json[260]`, PDF p.3485 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-35-psalm-218-note-002` | 35 | 218 | 2 | `per-note.json[262]`, PDF p.3495 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-35-psalm-218-note-003` | 35 | 218 | 3 | `per-note.json[263]`, PDF p.3495 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-35-psalm-223-note-001` | 35 | 223 | 1 | `per-note.json[264]`, PDF p.3512 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-35-psalm-227-note-001` | 35 | 227 | 1 | `per-note.json[265]`, PDF p.3530 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-36-psalm-233-note-002` | 36 | 233 | 2 | `per-note.json[267]`, PDF p.3652 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID |
| `book-37-psalm-250-note-003` | 37 | 250 | 3 | `per-note.json[271]`, PDF p.3690 | **À AUTHENTIFIER** | marqueur PDF ≠ ordinal ID ; ⚠️ note jumelle potentielle du dossier 063 non résolu |

### Lot 064-20 — 2 notes (book-41-psalm-275-note-001 → book-41-psalm-276-note-001)
| Identifiant | Livre | Psaume présumé | N° note | Référence 060 | Statut | Vigilance |
|---|---:|---:|---:|---|---|---|
| `book-41-psalm-275-note-001` | 41 | 275 | 1 | `per-note.json[274]`, PDF p.4174 | **À AUTHENTIFIER** | Alerte 060 : aucune |
| `book-41-psalm-276-note-001` | 41 | 276 | 1 | `per-note.json[275]`, PDF p.4178 | **À AUTHENTIFIER** | Alerte 060 : aucune |

## 5. Contrôles de reprise

- **20 lots :** `064-01`(10), `064-02`(10), `064-03`(10), `064-04`(10), `064-05`(10), `064-06`(10), `064-07`(10), `064-08`(10), `064-09`(10), `064-10`(10), `064-11`(10), `064-12`(10), `064-13`(10), `064-14`(10), `064-15`(10), `064-16`(10), `064-17`(10), `064-18`(10), `064-19`(10), `064-20`(2).
- **Unicité garantie :** `192 retrouvées = 0 exclues + 192 à authentifier` ; un identifiant = exactement un lot ; 0 perte, 0 double compte ; les 20 lots couvrent les 192 en ordre 060.
- **Premier lot à ouvrir :** `064-01` (10 notes), dans une **autre mission/conversation**, uniquement après autorisation. Voir [PROGRESS.md](PROGRESS.md).
- Aucun PDF entier consulté, aucun texte biblique ou note extrait à nouveau, aucune validation/promotion/publication, aucun déploiement, aucune fusion.
