# 🌸 BIBLAW — MISSION 064-20 — AUTHENTIFICATION DES 2 DERNIÈRES NOTES

**Reprise officielle :** dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT ; HEAD initial `e957aa1eede9fa8d214df5cbd9ae2a5966701998`, vérifié sur GitHub. Les 190 notes des missions 064-01 à 064-19 ne sont pas réexaminées, les 46 anciennes anomalies restent intactes. Les deux identifiants proviennent de [064_PLAN.md](064_PLAN.md) (catégorie 060).

## Sources et méthode

Source originale : `Bible essénienne (classée par livres).pdf` (4 744 pages). **Sept pages pertinentes examinées visuellement** : p.4173–4175 et p.4177–4180. Images de pages ×2, `note-proof.json`, positions et typographie conservées dans l'artefact GitHub **12669079049** (`biblaw-064-20-proof`), [action réussie #40365783606](https://github.com/ludodulac/Biblaw/actions/runs/40365783606). Les appels imprimés, début/fin des pieds, numéros, rattachements et identité des autres notes ont été examinés **sur les images**. La concordance de tokens seule n'attribue jamais un verdict.

| Identifiant exact | PDF / appel | Verdict | Début, fin, identité et preuve |
|---|---|---|---|
| `book-41-psalm-275-note-001` | p.4174 ; **psaume 275, verset 12** (renvoi ¹ après « bon dosage ») | **AUTHENTIFIÉE** | Un seul pied sous le filet : n° imprimé **1**, police **9 pt**, **16/16 tokens** correspondant intégralement à « Il s'agit de son psaume 250, « Trouver le juste dosage des qualités et des défauts ». » ; ni reprise de verset ni texte parasite. Page **4174** dans les pages canoniques [4173–4176] ; `noteIds` réciproque, aucune note concurrente du psaume. Pas de correction. |
| `book-41-psalm-276-note-001` | p.4178 ; **psaume 276, verset 5** (renvoi ¹ après « jubilé ») | **AUTHENTIFIÉE** | Un seul pied sous le filet : n° imprimé **1**, police **9 pt**, **12/12 tokens**, texte exact « C'est-à-dire avant la prochaine célébration de l'Archange Michaël. ». Début et fin intégralement sur p.4178 ; page canonique [4178–4182], `noteIds` réciproque et aucune identité concurrente. Pas de correction. |

## Tests spécialisés et CI

- Première action [#40365613140](https://github.com/ludodulac/Biblaw/actions/runs/40365613140) : **FAILURE technique transitoire**, le script hérité exigeait 5 cibles alors que le lot final contient 2 notes ; aucune erreur documentaire ni aucune donnée canonique modifiée.
- Correction du seul garde du script `len(TARGETS)==2`, commit `0bc8fbedb1268a0dcb6deed92989f3c381499841` ; **preuve spécialisée #40365783606 SUCCESS** avec captures et contrôles réels. Un garde supplémentaire de correspondance, d'unicité et de réciprocité est ajouté dans la clôture, à exécuter au dernier HEAD.
- À l'entrée de 064-20 : **45 SUCCESS / 48 runs**, trois échecs généraux déjà connus : [Browser smoke - lexical occurrence expansion #40327915444](https://github.com/ludodulac/Biblaw/actions/runs/40327915444) (contrat lexical historique), [BIBLAW 058 corpus browse mobile #40327915133](https://github.com/ludodulac/Biblaw/actions/runs/40327915133) (Playwright/Chromium vs Ubuntu 26.04), [Audit theme entry identity #40327915491](https://github.com/ludodulac/Biblaw/actions/runs/40327915491) (garde des changements anciens de `js/biblaw.js`). Aucun correctif hors périmètre.

**Vérification GitHub Actions sur le HEAD documentaire `b25309f298ed230d27cfde2c5cc389c51b50f8d9`** : **49 workflows PR, 46 SUCCESS et 3 FAILURE**. La [preuve spécialisée #40366841221](https://github.com/ludodulac/Biblaw/actions/runs/40366841221) est **SUCCESS** avec la garde finale portant sur les deux notes ; les trois échecs sont exactement les workflows généraux préexistants : [Browser smoke - lexical occurrence expansion #40366840695](https://github.com/ludodulac/Biblaw/actions/runs/40366840695), [BIBLAW 058 corpus browse mobile #40366840646](https://github.com/ludodulac/Biblaw/actions/runs/40366840646) et [Audit theme entry identity #40366840990](https://github.com/ludodulac/Biblaw/actions/runs/40366840990). Aucune nouvelle régression, aucune réparation hors périmètre.

## Décision et clôture

**064-20 : 2/2 AUTHENTIFIÉES, 0 CORRIGÉE, 0 NON RÉSOLUE.** Les deux `validation.status` historiques restent `machine-extracted-needs-review` : il s'agit de verdicts éditoriaux documentés, **pas** d'une publication technique. Aucun texte source de note, psaume ou prière n'a été modifié.

**064 entier : 192/192 examinées, 146 AUTHENTIFIÉES dont 10 CORRIGÉES ET AUTHENTIFIÉES, 46 NON RÉSOLUES, 0 restante.** Les 46 dossiers demeurent non authentifiés ; seule la phase d'examen initial est clôturée. Inventaire complet et renvois vers les vingt rapports : [REPORT.md](REPORT.md).

PR #72 **OPEN/DRAFT** ; aucune fusion, aucune publication, aucun déploiement, aucune modification d'interface ou de corpus. **STOP après 064-20.**
