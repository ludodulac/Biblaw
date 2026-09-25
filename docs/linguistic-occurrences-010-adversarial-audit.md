# BIBLAW-LINGUISTIC-OCCURRENCES-010 — audit adversarial indépendant

Baseline auditée : PR #27 HEAD `41d08cb4da1a45b13d027835c0844c49ecde81ed`.
Aucune correction de #27 n'est incluse ici.

## Reconstruction 009

Reconstruction indépendante : 1890 brut, 1890 AUTONOMOUS ; ADJECTIVE 564, ADVERB 150, NOUN 28, UNKNOWN 1148, AMBIGUOUS 0.

Répartition par cadre :
- copular-predicate-adjective : 262
- prenominal-adjective : 302
- modal-adverb-before-infinitive : 72
- adverb-before-determiner : 78
- substantivized-adjective : 28

## Gold 24 relu

Les 24 contextes ont été relus avec le contexte de l'occurrence et le résultat automatique. Les 18 sorties automatiques concordent avec la lecture 009 ; les 6 autres restent UNKNOWN. Aucune contradiction automatique n'a été trouvée.

Une réserve terminologique importante subsiste sur les cinq gold étiquetés NOUN : les rationales parlent elles-mêmes de « substantivized adjective/noun ». Le système choisit conventionnellement NOUN pour « le juste / dans le juste », mais #27 n'explicite pas suffisamment si NOUN signifie catégorie lexicale ou convention de représentation d'un adjectif substantivé. Ce n'est pas une erreur de contexte, mais une ambiguïté du modèle/gold qui doit être explicitée avant de considérer ces labels comme vérité linguistique indépendante.

## Audit des cinq cadres

### prenominal-adjective — 302 JUSTE

Échantillon JUSTE : sa juste place, une juste identification, le juste discernement, une juste discipline, la juste compréhension, le juste équilibre. Ces lectures sont adjectivales.

Falsification hors JUSTE : avec un lexème ADJ+NOUN tel que ROSE, le cadre classe `un rose bonbon` comme ADJECTIVE, alors que `rose` est ici le nom d'une teinte (« un rose ») et `bonbon` la modifie. Donc déterminant + cible + mot lexical n'est pas une preuve générique suffisante.

Verdict : générique dans son intention, TROP LARGE.

### copular-predicate-adjective — 262 JUSTE

Échantillon : préparation est juste ; cela est juste ; monde du Père est juste ; parole est juste ; Dieu est juste. Les sorties inspectées sont défendables.

Les contre-exemples déjà connus `il est juste là` et `il est juste enfermé` restent UNKNOWN grâce au resserrement de 009.

Sonde hors JUSTE : `ce courant est fort.` avec FORT ADJ/ADV produit ADJECTIVE, lecture correcte.

Verdict : structure générique plausible mais TROP ÉTROITE : de nombreux adjectifs évidents coordonnés ou suivis d'un complément restent UNKNOWN. Aucun faux positif certain trouvé dans l'échantillon JUSTE.

### adverb-before-determiner — 78 JUSTE

Échantillon : c'est juste un moyen ; elle est juste une présence ; devient juste une terre ; c'est juste une illusion. Lectures adverbiales défendables.

Sonde hors JUSTE : `c'est même une évidence` produit ADV, lecture correcte.

Hypothèse cachée : ce n'est pas « cible + déterminant » qui prouve ADV ; la règle dépend fortement du cadre copulaire/existentiel gauche et de la compatibilité lexicale ADV fournie par la configuration.

Verdict : générique mais ÉTROIT / conditionnel ; aucun faux positif JUSTE certain trouvé dans l'échantillon.

### modal-adverb-before-infinitive — 72 JUSTE

Échantillon : veut juste concrétiser ; devez juste entrer ; peux juste vivre ; faut juste survoler ; doit juste s'organiser. Lectures ADV défendables.

Sonde hors JUSTE : `il faut bien comprendre` avec BIEN ADV/NOUN produit ADV.

Limite : le code ne vérifie pas réellement que le mot suivant est morphologiquement un infinitif ; il accepte un mot lexical quelconque après le modal. Le nom du cadre promet donc davantage que la preuve syntaxique implémentée. La compatibilité lexicale ADV réduit le risque mais ne transforme pas le mot suivant en infinitif.

Verdict : générique dans son intention mais TROP LARGE par rapport à son nom/justification morphosyntaxique.

### substantivized-adjective — 28 JUSTE

Échantillon : le juste et l'injuste ; le vrai, le juste, le bon ; par le juste ; dans le juste. La substantivation est réelle.

Mais le moteur retourne POS=NOUN. En français, ces emplois peuvent être analysés comme adjectifs substantivés/nominalisés ; décider que le POS de sortie est NOUN est une convention de modèle, pas une conséquence nécessaire du cadre graphique.

Sonde hors JUSTE : `le vrai, le beau` reproduit la même convention.

Verdict : structure de substantivation réutilisable, mais DÉPENDANCE DE CONVENTION non suffisamment explicitée dans #27.

## UNKNOWN

Échantillonnage reproductible par familles :
- début de champ : 2
- fin de champ : 79
- copule : 92
- préposition : 251
- coordination : 186
- négation : 193
- déterminant après cible : 81
- infinitif-like : 8

Cas évidents correctement laissés UNKNOWN par manque de règle :
- `être honnête et juste` → ADJ humain
- `le dosage n'est pas juste` → ADJ humain
- `mais juste survivre` → ADV humain
- `c'est juste comprendre le processus` → ADV humain
- `ils voulaient juste être rassurés` → ADV humain

Ces faux négatifs renseignent la couverture, pas la précision.

## Recherche AMBIGUOUS

Recherche ciblée dans les familles copule, coordination, frontière, déterminant, préposition et poésie. Aucun cas n'a été retenu comme véritablement double avec suffisamment de contexte pour imposer AMBIGUOUS. Le zéro reste défendable pour ce pilote, sans être une propriété générale de JUSTE.

## Échantillon adversarial indépendant hors gold 009

Sélection figée avant toute correction, dans les zones à risque, sans recouvrement volontaire avec le gold 009 :
- occ-fdccbcc0695b26ebb50f060b — `le juste discernement` — auto ADJ — humain ADJ — concordant
- occ-406c78a20321f8feb409f6bd — `le juste retour` — auto ADJ — humain ADJ — concordant
- occ-3bd59781e5f0d64ac81a9290 — `cela est juste.` — auto ADJ — humain ADJ — concordant
- occ-07142990dba162c79e306be1 — `monde du Père est juste` — auto ADJ — humain ADJ — concordant
- occ-fba4535682a6bf3d6a52d2a6 — `C'est juste un sursaut` — auto ADV — humain ADV — concordant
- occ-c1ff671d76ec8401a8c61c44 — `elle est juste une présence` — auto ADV — humain ADV — concordant
- occ-27398b2dbbc1e3f2837d6759 — `veut juste concrétiser` — auto ADV — humain ADV — concordant
- occ-72d21d6832a51e9d64f3cdc6 — `faut juste survoler` — auto ADV — humain ADV — concordant
- occ-cc396f3ef1de0feb070e1975 — `le juste et l'injuste` — auto NOUN — humain SUBSTANTIVATION ; concordant seulement sous convention POS=NOUN
- occ-b8cf42184458525f28388b09 — `honnête et juste` — auto UNKNOWN — humain ADJ — abstention
- occ-91095bfbacbabcbbc5cab1c8 — `mais juste survivre` — auto UNKNOWN — humain ADV — abstention
- occ-63fc344b12b3369ed2a4a5b2 — `c'est juste comprendre` — auto UNKNOWN — humain ADV — abstention

Contradiction lexicale certaine JUSTE dans cet échantillon : 0.
Réserve de convention : 1 famille, substantivation → NOUN.

## Dépendances lexicales cachées / industrialisation

Aucun `if word == juste`, surface JUSTE ou analysisId JUSTE n'a été trouvé dans les cinq cadres.

Mais leur activation est candidate-spécifique via `genericRules` et leur sortie dépend de `genericPosMap`. Cette architecture est saine comme mécanisme de configuration, mais une règle activée n'est pas pour autant universellement valide pour tous les lexèmes partageant les mêmes POS.

La falsification ROSE montre précisément cette limite.

## Régressions

Les audits 009, PORTE 004, SUIS 006 et inversion 008 sont exécutés sans modification du moteur de #27.
