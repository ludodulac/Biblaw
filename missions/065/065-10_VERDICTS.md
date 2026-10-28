# 🌸 BIBLAW — MISSION 065-10 — VERDICTS DU DEUXIÈME LOT C

**Statut : TERMINÉE — 4/4 examinées, 0 AUTHENTIFIÉE, 0 CORRIGÉE ET AUTHENTIFIÉE, 4 NON RÉSOLUES.**

## Reprise et méthode

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 OPEN/DRAFT lors de l'unique vérification initiale ; HEAD de départ `30ed73e5d54bd0575f4e244c88e63196149fe134`, identique au HEAD communiqué. Aucun résultat 065-10 n'existait (rapport absent, suivi NON COMMENCÉE).
- Périmètre officiel 065-10 : les quatre identifiants ci-dessous, classe C. Aucun retraitement des lots 065-02 à 065-09.
- **Preuves archivées réutilisées** : seulement les inspections ciblées [064-18](../064/064-18_VERDICTS.md) p.3268–3269 (artefact **12601790662**), et [064-19](../064/064-19_VERDICTS.md) p.3479 (artefact **12650754088**) ; les deux artefacts ont été confirmés disponibles et non expirés. Le PDF source n'a pas été rouvert.
- Sources canoniques consultées en lecture seule : les **quatre JSON de note**, les **deux psaumes** associés, et la **prière autonome Pr.102** du livre 35 (`data/prayers/raphael-book-35-prayer-102.json`). L'analyse a confirmé les copies de pieds et les suffixes composites ; les deux identifiants par cas réclament chaque fois **un seul pied imprimé**.
- **Règle éditoriale :** ni présence d'un préfixe conforme, ni marqueur identique, ni `noteIds` réciproques ne distinguent à eux seuls deux identifiants prétendant représenter le même pied. Aucune correction arbitraire, aucune perte de texte des versets ou des prières ; aucune nouvelle GitHub Action.

## Verdicts individuels

### 1. `book-33-psalm-230-note-002`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-10) :** **NON RÉSOLUE**.
- **Identité du pied, rattachement, doublons et anomalie :** Le champ `text` de 106 tokens commence par la note imprimée **unique n°1 p.3268** (« Voir les psaumes 225 et 226. », 6 tokens), mais enchaîne à tort **les versets 23, 24 et 25 du psaume 230** (100 tokens, p.3269). La suite de 549 caractères du JSON a été comparée **à l'identique** à la concaténation numérotée des textes canoniques des versets 23–25. La note 003 revendique déjà le **même pied unique, le même appel et la même page**. `appliesTo.verse` de 002 est null ; 003 contient le v.14. Même si la contamination est établie, choisir cet ID et le promouvoir reviendrait à résoudre arbitrairement une double identité. Le psaume comporte les deux IDs dans `noteIds`.
- **Preuves :** [064-18_VERDICTS.md](../064/064-18_VERDICTS.md), [GitHub Actions #40199143472](https://github.com/ludodulac/Biblaw/actions/runs/40199143472), artefact de preuve A `12601790662` (p.3268–3269) ; `data/notes/books/book-33/book-33-psalm-230-note-002.json` (blob `309d5778174894d5af3eb9edb384b07a73fd1e59`) ; `data/corpus/books/book-33/psalm-230.json` (blob `9b0d1185b2bb9f1f8dd402dab501ac8d063ccc25`) ; versets 23–25 du psaume et autre ID concurrent du même lot.
- **Preuve manquante pour authentifier/corriger :** Preuve de la seule identité canonique à maintenir pour le pied n°1 du v.14 et réconciliation sûre des deux IDs et de `psalm-230.noteIds`. Un découpage de 002 à 6 tokens seul ne résout pas cette collision.
- **Correction :** Aucune : 002 et psaume inchangés ; les versets ne sont pas supprimés.

### 2. `book-33-psalm-230-note-003`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-10) :** **NON RÉSOLUE**.
- **Identité du pied, rattachement, doublons et anomalie :** Le JSON reproduit **exactement le pied imprimé n°1 de six tokens**, appelé au **verset 14** (« bons amis¹ »), et la p.3268 appartient au psaume 230. Mais la même occurrence, unique sur cette page, est revendiquée par **002** sous forme composite. Deux fichiers pour un seul pied imprimé : le numéro ordinal 003 et la concordance du texte ne prouvent pas l'identifiant canonique. Aucune seconde note imprimée ne distingue ces deux IDs. `noteIds` du psaume les contient tous deux.
- **Preuves :** [064-18_VERDICTS.md](../064/064-18_VERDICTS.md), [GitHub Actions #40199143472](https://github.com/ludodulac/Biblaw/actions/runs/40199143472), artefact de preuve A `12601790662` (p.3268) ; `data/notes/books/book-33/book-33-psalm-230-note-003.json` (blob `7c3c34e8adb4a2d6456aa73c8b76ffa02a71781f`) ; `data/corpus/books/book-33/psalm-230.json` (blob `9b0d1185b2bb9f1f8dd402dab501ac8d063ccc25`) ; versets 23–25 du psaume et autre ID concurrent du même lot.
- **Preuve manquante pour authentifier/corriger :** Preuve documentaire ou règle explicite établissant l'identifiant conservé et le traitement du doublon 002, puis mise en cohérence des références du psaume avec autorisation spécifique.
- **Correction :** Aucune : pas de promotion par simple concordance ni choix arbitraire.

### 3. `book-35-psalm-213-note-002`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-10) :** **NON RÉSOLUE**.
- **Identité du pied, rattachement, doublons et anomalie :** Le **pied imprimé n°1** au **verset 19** du psaume 213 (p.3479) se limite aux 55 premiers tokens, de « Les nombreux rituels donnés » à « rituel du désenvoûtement. ». Le JSON **de 455 tokens** ajoute environ 400 tokens de continuation de la **prière Pr.102** (« J’honore l’air précieux… Amin. »). Le JSON **003 est strictement identique** aux 2 286 caractères du champ `text` de 002, sur la même page et le même appel. Le fichier autonome `raphael-book-35-prayer-102.json` existe et renvoie au psaume 213, mais son `text` n'a que **137 caractères** (« Je t’invoque, ô mon Père Raphaël… ») et ne conserve ni le début ni la fin de la continuation contaminante de 1 951 caractères. Couper la note isolément entraînerait une perte de texte dans les fichiers canoniques et ne résoudrait pas les deux IDs concurrents.
- **Preuves :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md), [GitHub Actions #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710), artefact de preuve A `12650754088` (p.3479) ; `data/notes/books/book-35/book-35-psalm-213-note-002.json` (blob `c4b483dd01621aac901761607266d553b3c9d9f6`) ; `data/corpus/books/book-35/psalm-213.json` (blob `aac58b6a049891b6a16583f8c8de3a7516146382`) ; `data/prayers/raphael-book-35-prayer-102.json` (vérification de l'incomplétude de la continuation de la prière).
- **Preuve manquante pour authentifier/corriger :** Conservation canonique fidèle de la suite Pr.102 sous son identité de prière et arbitrage documentaire de l'unique ID correspondant au pied n°1, puis réconciliation des références. La modification de prières/psaumes est interdite dans cette mission.
- **Correction :** Aucune : aucun suffixe de prière tronqué ni ID dédoublonné.

### 4. `book-35-psalm-213-note-003`

- **Ancien verdict (064) :** NON RÉSOLUE.
- **Nouveau verdict (065-10) :** **NON RÉSOLUE**.
- **Identité du pied, rattachement, doublons et anomalie :** Le JSON 003 a exactement le **même texte composite de 455 tokens** que 002, le même pied imprimé de **55 tokens** p.3479 et le même marqueur 1. Le champ `appliesTo.verse=19` correspond au verset appelant, mais ne démontre pas un second pied : **une seule note imprimée** est documentée. Le suffixe provient de la continuation de Pr.102, absente du texte de la prière autonome, qui n'en contient actuellement que le début. Le psaume possède deux `noteIds` concurrents. Ni la bonne valeur de verset, ni une identité lexicale ne permettent d'authentifier indépendamment le fichier 003.
- **Preuves :** [064-19_VERDICTS.md](../064/064-19_VERDICTS.md), [GitHub Actions #40326164710](https://github.com/ludodulac/Biblaw/actions/runs/40326164710), artefact de preuve A `12650754088` (p.3479) ; `data/notes/books/book-35/book-35-psalm-213-note-003.json` (blob `4d8ff04bcc065a9a29099072e3d628d3fc7bd08d`) ; `data/corpus/books/book-35/psalm-213.json` (blob `aac58b6a049891b6a16583f8c8de3a7516146382`) ; `data/prayers/raphael-book-35-prayer-102.json` (vérification de l'incomplétude de la continuation de la prière).
- **Preuve manquante pour authentifier/corriger :** Mêmes deux blocages : conservation de toute la continuation de Pr.102, puis preuve de l'identifiant unique et réconciliation de `noteIds` sans choix arbitraire ni édition de prière interdite.
- **Correction :** Aucune : 003 et autres fichiers canoniques intacts.

## Contrôles spécialisés documentaires

- **PASS** — quatre IDs exacts du plan 065-10.
- **PASS** — quatre identifiants distincts.
- **PASS** — anciens et nouveaux verdicts inchangés NON RÉSOLUE.
- **PASS** — rapport 064-18/A : note 33/230/002 contient le pied 6 tokens et les versets 23–25 du psaume.
- **PASS** — 33/230/002 : suite exacte des versets 23–25 constatée par comparaison textuelle ciblée.
- **PASS** — 33/230/003 : même pied unique imprimé n°1 p.3268, sans deuxième identité prouvée.
- **PASS** — rapport 064-19/A : un seul pied de 55 tokens en p.3479 pour les deux IDs.
- **PASS** — 35/213/002 et 003 : champ text strictement identique (comparaison ciblée).
- **PASS** — Pr.102 autonome liée à 35/213 mais continuation de la note absente.
- **PASS** — aucun verdict ni note d'un lot antérieur modifié.
- **PASS** — aucun PDF original rouvert ni nouvelle GitHub Action lancée.
- **PASS** — le suivi initial 065-10 est non commencé et le HEAD de base possède un arbre.

**12/12 vérifications documentaires et structurales ciblées PASS** (contrôles des JSON et comparaisons textuelles ciblées déjà effectuées, non nouvelle certification du PDF ni nouvelle exécution d'un workflow). Les incohérences sont **détectées**, pas corrigées ni authentifiées.

## Clôture

- **065-10 : 4/4 revues, 0 AUTHENTIFIÉE, 0 CORRIGÉE, 4 NON RÉSOLUES**. Deux conflits d'identité distincts : 33/230/002–003 et 35/213/002–003. Le second inclut une continuation Pr.102 non entièrement conservée dans le fichier autonome.
- **Cumul 065 : 34/46 notes réexaminées, 2 anomalies résolues, 44 NON RÉSOLUES, 12 non encore réexaminées**. Les 146 authentifications historiques 064 et les verdicts 065 antérieurs restent inchangés.
- Aucun JSON de note, psaume, prière, moteur, interface ou catalogue modifié ; aucune suppression, publication, déploiement, fusion, réparation des workflows généraux ou relecture du PDF. **STOP après 065-10 ; 065-11 NON COMMENCÉE.**
