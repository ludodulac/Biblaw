# BIBLAW-LINGUISTIC-OCCURRENCES-009 — troisième pilote JUSTE

## Sélection depuis le corpus

Comptes selon le même contrat documentaire que l'indexeur :
- marche 224
- compte 222
- livre 77
- veille 25
- aide 61
- garde 99
- reste 266
- passe 281
- juste 1890
- sens 1415
- tour 97

Évaluation qualitative :
- MARCHE : NOUN/VERB, nombreux contextes évidents mais proche du test PORTE.
- COMPTE : NOUN/VERB avec locutions prendre/rendre/se rendre compte ; utile mais encore proche de PORTE.
- GARDE/AIDE/RESTE/PASSE : surtout NOUN/VERB, valeur de généralisation moindre.
- SENS : NOUN / VERB sentir, volumineux et intéressant, mais reproduit largement le contraste nominal/verbal.
- JUSTE : ADJ / ADV / substantivation nominale réellement attestés ; prédicatif, épithète, restriction adverbiale, coordination et constructions figées. Difficulté nouvelle et forte valeur pour la désambiguïsation.

JUSTE est retenu pour la nouveauté des catégories, pas pour son seul volume.

## Analyses attestées

- ADJECTIVE, lemma juste, POS ADJ
- ADVERB, lemma juste, POS ADV
- NOUN, lemma juste, POS NOUN (substantivation : « le juste »)

Les 1890 occurrences sont AUTONOMOUS dans le contrat actuel.

## UNKNOWN / AMBIGUOUS

UNKNOWN = le moteur ne possède pas de preuve suffisamment sûre pour choisir une analyse.
AMBIGUOUS = au moins deux analyses candidates restent réellement compatibles avec le contexte disponible.

Une recherche active a été menée sur les copules, fins de phrase, coordinations, « juste là/ici », « juste avant/après », substantivations et constructions poétiques. Aucun cas réel n'a été jugé assez solidement double pour créer artificiellement AMBIGUOUS. Le compteur reste donc 0.

## Règles A — génériques françaises

Le moteur contient cinq cadres réutilisables, activés par configuration et mappés vers les POS disponibles du lexème :
1. prenominal-adjective : déterminant + cible + tête lexicale, avec exclusion des coordinations substantivantes ;
2. copular-predicate-adjective : copule + cible seulement devant frontière/coordination compatible ;
3. adverb-before-determiner : portée restrictive devant groupe déterminé uniquement après cadre copulaire/existentiel compatible ;
4. modal-adverb-before-infinitive : modal français configuré dans le moteur + cible + complément infinitif ;
5. substantivized-adjective : déterminant + cible devant frontière/coordination.

Ces règles ne contiennent ni « juste » ni un autre mot pilote.

## Règles B — connaissances lexicales configurées

JUSTE configure uniquement :
- ses trois analyses candidates ;
- lemma/POS/catégorie ;
- le mapping POS -> catégorie ;
- les règles génériques qu'il autorise.

Aucune règle regex propre à JUSTE n'est utilisée.

## Audit adversarial

Une première version trop large a été rejetée parce que « juste + préposition » produisait de faux ADV :
- la façon juste de vivre ;
- la vision juste des imperfections ;
- une attitude intérieure juste pour agir.

Le cadre a été supprimé.

Le premier prédicat copulaire était aussi trop large et aurait transformé en ADJECTIVE :
- il est juste là ;
- il est juste enfermé.

Il a été resserré aux frontières/coordinations sûres.

Sondes permanentes vérifient ces anciens faux positifs.

Sont également couverts : casse, ponctuation, début/fin de champ par l'indexeur, élision dans les cadres, déterminants, modaux, coordination et substantivation. Les phénomènes sans preuve suffisante restent UNKNOWN.

## Résultat final automatique

Total brut : 1890.

Segmentation :
- AUTONOMOUS 1890
- VERB_CLITIC 0
- COMPOUND_ELEMENT 0

Adjudication :
- ADJECTIVE PROVISIONAL 564
- ADVERB PROVISIONAL 150
- NOUN PROVISIONAL 28
- UNKNOWN 1148
- AMBIGUOUS 0

Couverture PROVISIONAL : 742 / 1890 = 39.26 %. Cette couverture n'est pas un objectif et n'est pas une mesure de précision.

## Gold indépendant

24 occurrences human-audited, couvrant ADJ, ADV, NOUN, cadres faciles et difficiles, ainsi que des cas volontairement hors couverture automatique.

Résultat :
- correct automatique 18
- UNKNOWN 6
- AMBIGUOUS 0
- contradictoire 0

Ce petit gold est un contrôle de non-contradiction, pas une estimation statistique de précision globale.

## Régressions

PORTE reconstruit exactement :
1184 brut ; 1154 AUTONOMOUS ; 3 VERB_CLITIC ; 27 COMPOUND_ELEMENT ; 268 NOUN ; 369 VERB_PORTER ; 520 UNKNOWN. Zéro dérive.

SUIS reconstruit exactement :
631 brut ; 615 AUTONOMOUS ; 1 VERB_CLITIC ; 10 COMPOUND_ELEMENT ; 5 VERB_INVERSION ; 116 VERB_ETRE ; 4 VERB_SUIVRE ; 501 UNKNOWN. Zéro dérive.

Les sondes 008 restent permanentes : suis-je, porte-t-il, marche-t-elle, a-t-il.

## Industrialisation

009 démontre qu'une partie utile de la désambiguïsation peut être exprimée par des règles françaises réutilisables + configuration lexicale. Mais l'ajout de JUSTE a encore nécessité de modifier le moteur Python pour introduire des cadres ADJ/ADV/NOUN et leur audit adversarial.

Il n'est donc pas encore démontré que 20 mots supplémentaires seraient essentiellement un travail de données/configuration. La réponse actuelle est B : le moteur devrait encore évoluer régulièrement. Industrialisation 20 mots : NO-GO à ce stade.
