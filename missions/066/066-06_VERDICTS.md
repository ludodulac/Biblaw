# 🌸 BIBLAW — MISSION 066-06 — PIED COMPOSITE ET IDENTIFIANTS CONCURRENTS 33/230

**Statut : TERMINÉE — 2/2 notes du plan examinées ; 0 authentifiée, 0 corrigée et authentifiée, 2 NON RÉSOLUES. Aucun fichier canonique modifié.**

## Reprise et mandat officiel

- Dépôt `ludodulac/Biblaw`, branche `feat/052-search-ui`, PR #72 **OPEN / DRAFT, non fusionnée** à l'unique vérification initiale ; HEAD d'entrée `1b2c9b017d97ab52f5ec46a63a5c85c6ddd1f2bb`.
- Le [plan 066-06](066_PLAN.md) impose exclusivement `book-33-psalm-230-note-002` et `book-33-psalm-230-note-003`, et la séparation **conceptuelle** de l'unique pied imprimé de six tokens de la suite versifiée 23–25. La mission 066-07 reste hors périmètre.
- [Protocole 066-02](066-02_PROTOCOL.md) : **source → appel → pied → candidats** ; **FAIT ÉTABLI** distinct de **HYPOTHÈSE** et de toute **DÉCISION ÉDITORIALE de Ludo** ; garantie de conservation intégrale avant réduction de composite.
- Preuves archivées : [064-18_VERDICTS.md](../064/064-18_VERDICTS.md) et [065-10_VERDICTS.md](../065/065-10_VERDICTS.md) ; p. **3268–3269** déjà inspectées avec captures et disposition typographique. Artefacts A `12601790662` ([Action 40199143472](https://github.com/ludodulac/Biblaw/actions/runs/40199143472)) et `12601056941` ([Action 40199370107](https://github.com/ludodulac/Biblaw/actions/runs/40199370107)), **non expirés**.
- Trois JSON lus **sans mutation** au HEAD d'entrée : note 002 (blob `309d5778174894d5af3eb9edb384b07a73fd1e59`), note 003 (blob `7c3c34e8adb4a2d6456aa73c8b76ffa02a71781f`), psaume 33/230 (blob `9b0d1185b2bb9f1f8dd402dab501ac8d063ccc25`). Aucun PDF original rouvert, aucun audit général ni nouveau workflow.

## Fiche commune : provenance source → appel → pied → candidats

| Étape | FAIT ÉTABLI | Limite |
|---|---|---|
| **Source imprimée** | Un **seul pied local n°1** de **6 tokens**, PDF **p.3268**, texte « Voir les psaumes 225 et 226. ». | Un pied ne démontre pas deux identités canoniques. |
| **Appel** | Psaume **33/230, verset 14**, « bons amis¹ », selon 064-18. Le verset 14 est dans le JSON du psaume sur p.3268. | L'appel exact ne choisit pas le numéro de fichier à garder. |
| **Candidat 002** | `text` **578 caractères**, p.3268, `marker=1`, `verse=null`. Début égal au texte du pied puis versets **23, 24, 25** numérotés. | Texte **composite** : le pied seul ne constitue pas tout ce champ. |
| **Candidat 003** | `text` **28 caractères**, six tokens du pied seul, p.3268, `marker=1`, `verse=14`. | Une meilleure découpe/valeur de verset ne prouve pas la provenance de l'ID. |
| **Conservation du suffixe** | Comparaison **caractère par caractère PASS** : `text_002 === text_003 + " " + "23. " + v23 + " 24. " + v24 + " 25. " + v25`. Les **549 caractères** de texte versifié, hors espace avant « 23. », sont intégralement présents dans le psaume p.3269. | Toute éventuelle réduction de 002 doit conserver texte et provenance, et résoudre aussi la concurrence d'IDs. |
| **Références et statut** | `noteIds` comporte **002 et 003**, chacune une fois ; `validation.status=machine-extracted-needs-review` pour les deux. | Deux références ne créent pas deux pieds imprimés, ni une authentification. |

**Convention de comptage :** les verdicts 064/065 emploient **106 tokens** pour la composite (six du pied + 100 du corps). Un découpage simple des chaînes actuelles sur les espaces obtient **102 unités = 6 + 96**. Cette différence de méthode n'affecte pas la preuve **exacte** de conservation (28 + 1 + 549 = **578 caractères**). Les chiffres historiques sont préservés et non réinterprétés comme une comparaison échouée.

## Verdict individuel 1 — `book-33-psalm-230-note-002`

- **FAIT ÉTABLI :** une extraction composite, dans laquelle les **28 premiers caractères** sont exactement le pied imprimé unique p.3268 ; la suite des **549 caractères** correspond **à l'identique** aux versets numérotés 23–25, déjà enregistrés p.3269 dans le psaume. `appliesTo.verse=null`, mais `noteIds` du psaume contient 002.
- **HYPOTHÈSE :** un artefact d'extraction a concaténé une note à la fin du corps du psaume. La raison de la génération de 002 n'est pas démontrée ; sa nature composite n'établit **pas** à elle seule qu'il faut conserver 003.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** frontière de segmentation du texte **entièrement démontrée** ; suffixe canonique sauvegardé dans les versets. **Aucune correction JSON autonome sûre** : réduire 002 à six tokens ne tranche pas le conflit avec 003. **0 édition effectuée.**
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** choix sourcé d'un ID canonique 002 ou 003, ou règle explicite d'alias/archivage non destructive ; autorisation des fichiers et du traitement de `text`, `appliesTo`, `validation` et des `noteIds`.
- **Preuves manquantes :** provenance du numéro d'identifiant et mandat de réconciliation des références. **VERDICT : NON RÉSOLUE.**

## Verdict individuel 2 — `book-33-psalm-230-note-003`

- **FAIT ÉTABLI :** texte de six tokens correspondant **exactement** au pied unique imprimé p.3268, appel au verset 14 ; 002 revendique le même pied sous forme d'un préfixe de composite. `appliesTo.verse=14` et `noteIds` cohérents comme **relations techniques**, sans preuve d'unicité d'identité.
- **HYPOTHÈSE :** 003 pourrait être un second extrait plus propre d'une même occurrence imprimée ; sa forme plus complète en métadonnées **ne prouve pas** qu'il soit historiquement canonique.
- **CORRECTION TECHNIQUE CERTAINE IDENTIFIÉE :** transcription exacte du pied de six tokens et position de l'appel établies ; aucune correction lexicale nécessaire, mais **aucun changement sûr** d'ID ou de références sans arbitrage.
- **DÉCISION ÉDITORIALE NÉCESSITANT LUDO :** attribuer explicitement l'identité du seul pied, préserver les deux provenances et autoriser l'éventuel alias/archivage et les changements `noteIds`.
- **Preuves manquantes :** historique probant ou règle validée déterminant le titulaire canonique de l'unique pied. **VERDICT : NON RÉSOLUE.**

## Conditions d'une résolution future — NON EXÉCUTÉES

1. Préserver les **SHA et textes complets** des deux notes et du psaume, ainsi que les preuves archivées des pages 3268–3269.
2. Consigner une décision explicite de Ludo sur l'identité 002/003 et le mode non destructif de résolution (primaire/alias ou neutralisation documentée).
3. **Avant tout retrait du suffixe**, vérifier la conservation intégrale de sa chaîne exacte dans les versets 23, 24 et 25 ; ne pas choisir un ID sur le seul critère de découpage.
4. Après autorisation spécifique seulement, tester un pied logique par appel, absence de `noteIds` orphelins, aucune perte de texte et diff limité aux fichiers autorisés ; ni déploiement ni fusion implicite.

## Contrôles documentaires spécialisés (lecture seule)

- **PASS** — Plan 066-06 exactement deux notes.
- **PASS** — Inventaire 066-06 mentionne chaque note.
- **PASS** — Protocole 066-02 applicable source→appel→pied→candidats.
- **PASS** — Suivi 066-06 non commencé, pas de rapport dans STATE.
- **PASS** — IDs des deux notes et recordId du psaume.
- **PASS** — Même source imprimée/page 3268/marqueur 1.
- **PASS** — Préfixe note 002 exactement identique au texte de la note 003.
- **PASS** — Composite 002 = texte 003 + espace + versets 23–25 numérotés.
- **PASS** — Suffixe du composite entièrement égal aux versets, 549 caractères.
- **PASS** — Longueurs calculées réelles 578 et 28, champ textLength absent.
- **PASS** — Versets 23–25 conservés aux pages 3269.
- **PASS** — Verset 14 d'appel déclaré en page 3268.
- **PASS** — Verset null pour note 002 et verset 14 pour 003.
- **PASS** — Deux références noteIds sans doublon d'ID dans le psaume.
- **PASS** — Pages 3268 et 3269 dans le périmètre du psaume.
- **PASS** — Statuts machine des deux notes non authentifiés.
- **PASS** — Écart connu de convention de comptage : espaces 102 vs 106 rapportés.
- **PASS** — Aucune altération nécessaire pour établir la conservation du suffixe.

**18/18 PASS** ; les contrôles sont ciblés sur les deux notes et le psaume. L'unicité du pied imprimé provient des contrôles visuels **déjà effectués en 064** ; aucun PDF original rouvert et aucune Action nouvelle.

**STOP : 066-06 TERMINÉE ; 2 NON RÉSOLUES, zéro authentification/correction. Cumul 066 : 14/44 dossiers revus en 066-03 à 066-06, 44 anomalies restant NON RÉSOLUES (2 corrigées et authentifiées en 065). 066-07 NON COMMENCÉE ; PR #72 toujours DRAFT, sans fusion.**
