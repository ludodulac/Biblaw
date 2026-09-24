# BIBLAW-LINGUISTIC-OCCURRENCES-003 — audit qualité PORTE

## Portée et provenance

Audit adversarial de la PR #21, sans modification de l'adjudication pilote. La branche 003 dérive du HEAD #21 `64a7a1306abe73885195f95974812d2a0100c27e`.

Point de provenance critique : le fichier `data/linguistic/pilots/porte.json` contient les résultats et leurs étiquettes d'evidence, mais **le code exact qui a produit les classifications PROVISIONAL n'a pas été commité dans #21**. L'implémentation employée pendant 002 est donc reconstruite ci-dessous à partir de l'exécution ayant généré le fichier ; cette absence de générateur versionné interdit de considérer l'adjudication comme pleinement reproductible.

## Heuristique 002 reconstruite exactement

```text
nounBefore =
  (début ou espace/guillemet/parenthèse)
  + {la, une, cette, ma, ta, sa, notre, votre, leur, chaque, aucune,
     quelle, seule, grande, petite, sainte, même, dernière, première}
  immédiatement avant "porte"

nounCollocation =
  {ouvrir, ouvre, ouvres, ouvrent, fermer, ferme, fermes, ferment,
   franchir, franchit, franchis, devant, derrière, jusqu’à, vers}
  + {la, une, cette, sa, ma, ta, notre, votre, leur}
  immédiatement avant "porte"

nounAfter =
  immédiatement après "porte":
  {de, du, des, ouvrant, ouverte, fermée, sera, s’ouvre, est, entre}

verbBefore =
  immédiatement avant "porte":
  {je, tu, il, elle, on, nous, vous, ils, elles, qui, qu’il, qu’elle,
   cela, ça, ceci, chacun, personne}

verbAfter =
  immédiatement après "porte":
  {en, sur, dans, à, au, aux, le, la, les, un, une, des, ce, cet,
   cette, ces, son, sa, ses, mon, ma, mes, ton, ta, tes, notre, votre,
   leur, leurs, aucun, aucune, tous, toute, toutes, plusieurs, chaque}

imperative =
  début de contexte ou ponctuation forte avant "Porte/porte"
  ET verbAfter

ordre de décision:
  si nounBefore OU nounCollocation OU (NON verbBefore ET nounAfter)
      => NOUN / PROVISIONAL
  sinon si verbBefore OU imperative OU (NON nounBefore ET verbAfter)
      => VERB_PORTER / PROVISIONAL
  sinon => UNKNOWN
```

Ces patrons sont des **indices**, pas des règles grammaticales absolues.

### Limites NOUN

`nounBefore` détecte utilement des déterminants/adjectifs fréquents mais sa liste est fermée. `nounCollocation` est lexicalement étroite. `nounAfter` est dangereux : `de/des` peuvent introduire le complément d'un verbe PORTER (« porte des mondes », « porte de vrai »). Faux positifs NOUN observés pour cette raison. Faux négatifs possibles avec déterminants/adjectifs absents de la liste, inversion, citation ou structure poétique.

### Limites VERB

`verbBefore` ne couvre qu'une petite liste de sujets/pronoms immédiatement adjacents. `verbAfter` confond complément verbal et complément suivant un nom. Exemple réel : « ouvrir une telle porte dans… » : `dans` déclenche le cadre verbal alors que « porte » est nominal. L'impératif est incomplet face aux clitiques liés par tiret (`porte-le`, `porte-la`, `porte-les`). Faux négatifs nombreux avec sujets nominaux, relatives à clitique objet, coordinations et inversions.

## Échantillonnage indépendant

L'audit `scripts/audit_linguistic_porte_quality.py` sélectionne 24 NOUN, 24 VERB_PORTER et 24 UNKNOWN, soit **72 occurrences**. Dans chaque catégorie : tri stable par `occurrenceId`, puis sélection gloutonne visant d'abord des combinaisons distinctes `recordType/bookNumber/field/evidence`, puis remplissage jusqu'au quota. La sélection n'utilise pas l'ordre du fichier et est reproductible.

Le JSON `data/linguistic/audits/porte-003-audit.json` conserve les 72 contextes sélectionnés.

## Erreurs PROVISIONAL certaines détectées

1. `occ-4210e70fcbe4e1d65b894181`
   - contexte : « ... ouvrir une telle porte dans votre époque troublée »
   - actuel : VERB_PORTER
   - proposé : NOUN
   - responsable : verb-frame (`dans` après porte, tandis que `telle` n'est pas reconnu par nounBefore/nounCollocation)
   - cause : complément prépositionnel après un nom pris pour cadre verbal.

2. `occ-f5043c17057a47db9e0b5eed`
   - contexte : « ... une œuvre vivante qui, à travers un corps, porte des mondes... »
   - actuel : NOUN
   - proposé : VERB_PORTER
   - responsable : noun-frame (`des` après porte)
   - cause : déterminant du complément d'objet pris pour indice nominal.

3. `occ-a18d1242395f001f1889f138`
   - contexte : « ... ce que l’homme porte de vrai en lui... »
   - actuel : NOUN
   - proposé : VERB_PORTER
   - responsable : noun-frame (`de` après porte)
   - cause identique.

4. `occ-75cd0c3a829334cbf3d2165c`
   - contexte : « Si l’homme porte des vertus... »
   - actuel : NOUN
   - proposé : VERB_PORTER
   - responsable : noun-frame (`des` après porte)
   - cause identique.

5. `occ-8a55dd99471758e92a13b630`
   - contexte : « ... ce que l’homme porte de vrai, de beau... »
   - actuel : NOUN
   - proposé : VERB_PORTER
   - responsable : noun-frame (`de` après porte)
   - cause identique.

Ces cinq cas sont des sentinelles minimales, pas une affirmation que les 1 039 PROVISIONAL restants sont tous corrects.

## Les 145 UNKNOWN

Inspection adversariale des UNKNOWN :

- **A — véritable ambiguïté linguistique démontrée : 0**
- **B — décidables pour un humain mais non couverts par les heuristiques : 122**
- **C — problème de segmentation : 23**
- **D — autre phénomène nécessitant une famille séparée : 0**

Les 23 cas C sont des éléments de composés tels que `porte-parole`, `porte-Parole`, `porte-drapeau`, `porte-bonheur`, `porte-monnaie`, `porte-à-faux`. Ils ne doivent pas être traités comme occurrences autonomes du nom `porte` ou du verbe `porter`.

Trois autres formes avec tiret — `porte-le`, `porte-les`, `porte-la` — sont au contraire des verbes PORTER avec clitique et font partie des 122 cas B.

Exemples B manifestes : « l’homme ne porte pas sur lui... », « Porte uniquement ce qui t’élève... », « Ne porte avec toi que... », « la terre qui le porte », « porte-la dans ta vie ».

Le zéro AMBIGUOUS du pilote n'est donc pas expliqué par une impossibilité de représenter l'ambiguïté ; simplement, aucun des contextes inspectés ne justifie actuellement deux analyses POS concurrentes. Les UNKNOWN observés relèvent surtout d'une couverture heuristique insuffisante ou d'une segmentation erronée.

## Segmentation sur l'ensemble des 1 184

30 occurrences ont un tiret adjacent :
- 3 verbes avec clitique : à conserver comme PORTER ;
- 27 éléments de composés : à exclure du pilote de la forme autonome `porte` ou à représenter explicitement comme composés.

Parmi les 27 composés, l'état actuel est :
- NOUN : 4 ;
- VERB_PORTER : 0 ;
- UNKNOWN : 23.

Cela signifie que le total technique 1 184 est reproductible selon le tokenizer de #21, mais qu'il n'est **pas encore un total linguistique propre de la forme autonome PORTE**. Sous la convention « forme autonome, clitiques verbaux admis, composés exclus », le total serait 1 157. Cette convention doit être décidée et testée avant intégration.

## Précision

Aucun taux global de précision n'est publié. Un taux serait trompeur sans gold set indépendant et adjudication humaine traçable de l'échantillon. Le présent audit démontre déjà des faux positifs dans les deux directions et un défaut de segmentation systémique.

## Politique PROVISIONAL -> VALIDATED proposée

Une analyse ne passe à VALIDATED que si :
1. l'occurrence et son contexte original sont stables et audités ;
2. la segmentation est explicitement validée ;
3. une justification morphosyntaxique traçable est enregistrée ;
4. la décision provient soit d'une validation humaine explicite, soit d'une règle générique versionnée dont le domaine de validité est déterminant et couverte par des tests contradictoires ;
5. un contrôle indépendant n'a pas produit d'analyse concurrente plausible ;
6. la version de l'analyse, la méthode et l'auteur/type de validation sont conservés.

Un score numérique seul ne suffit jamais. Une règle automatique locale par mot ne doit pas auto-promouvoir VALIDATED.

## Industrialisation

A — règles locales par mot : acceptables comme pilotes/diagnostics, non comme architecture principale ; coût et exceptions croissent sans contrôle.

B — règles morphosyntaxiques génériques : utiles pour des cas déterminants (déterminants, clitiques, accord, structure locale), à versionner et tester sur plusieurs lexèmes.

C — analyse NLP externe/modèle : peut proposer des analyses et réduire le travail manuel, mais doit rester une source PROVISIONAL avec provenance/version ; aucune dépendance externe n'est ajoutée en 003.

D — hybride : recommandé. Index documentaire déterministe + analyse morphosyntaxique générique + propositions NLP éventuelles + UNKNOWN/AMBIGUOUS conservés + validation humaine traçable pour les cas publiés comme fiables.

## Décisions

**NO-GO fusion #21 en l'état.** Raisons bloquantes : générateur de l'adjudication PROVISIONAL non versionné, cinq erreurs certaines déjà démontrées, 27 composés mélangés à la forme autonome.

**GO limité pour poursuivre l'architecture**, mais **NO-GO pour industrialiser la classification à grande échelle** avant correction de la segmentation, versionnement du générateur d'analyse et création d'un protocole de validation indépendant/gold set.

Aucune UI, aucun corpus canonique, aucun thème et aucun runtime public ne sont modifiés par 003.
