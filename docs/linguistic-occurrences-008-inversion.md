# BIBLAW-LINGUISTIC-OCCURRENCES-008 — correction structurelle de l'inversion

## Stratégie Git

La branche `fix/linguistic-occurrences-008` part du HEAD de l'audit #25, donc contient #24 + les preuves 007 + la correction 008. La PR consolidée cible directement `main`. Ainsi #24 et #25 ne doivent pas être fusionnées séparément si la PR 008 est retenue.

## Cause 007 confirmée

#24 ne reconnaissait que `verbe-pronom`. Le segment `t` de `verbe-t-pronom` était donc pris pour le premier élément après le tiret et la forme devenait COMPOUND_ELEMENT.

## Contrat conservateur VERB_INVERSION

Le moteur reconnaît deux graphies structurelles :
- cible + tiret + pronom direct ;
- cible + tiret + `t` + tiret + pronom de 3e personne singulier.

Tirets reconnus : ASCII `-`, U+2011 `‑`, U+2013 `–`, U+2014 `—`. La casse est neutralisée par `casefold()`.

Pronoms directs reconnus de façon conservatrice : `je, tu, il, elle, on, ils, elles`.

Pronoms après `-t-` : `il, elle, on`.

`nous` et `vous` ne sont volontairement pas affirmés comme inversion par la graphie seule : le corpus contient massivement des impératifs/pronominaux tels que `aide-nous`, `rappelez-vous`, `ouvrez-vous`. Cette restriction privilégie la précision et devra être levée seulement avec une preuve morphosyntaxique supplémentaire.

Le moteur exige aussi que la configuration du candidat contienne au moins une analyse possible de POS VERB avant d'utiliser VERB_INVERSION dans l'adjudication. Cela protège notamment la famille corpus `rayon-je` : un tiret + `je` n'est pas à lui seul une preuve de verbalité.

Ce garde ne choisit aucun lemme. Il établit seulement qu'une analyse verbale fait partie des possibilités lexicales du candidat.

## T euphonique

Le `t` n'est ni un clitique objet, ni un lemme, ni un composé. Il est consommé uniquement dans le patron graphique `-t-` immédiatement suivi de `il/elle/on`.

## Corpus

Recherche exhaustive graphique sur les champs canoniques : 3231 candidats `mot-pronom` / `mot-t-pronom`.

- 3041 candidats directs ;
- 190 candidats avec `-t-` euphonique ;
- 705 familles graphiques distinctes ;
- tiret ASCII : 2563 ;
- tiret U+2011 : 668.

Parmi les directs, 2012 portent `nous/vous` et sont explicitement considérés comme graphiquement ambigus, non comme inversions certaines. 1029 utilisent le sous-ensemble direct conservateur.

Les 190 `-t-` comprennent notamment : `a-t-il`, `a-t-elle`, `marche-t-il`, `ouvre-t-il`, `parle-t-on`, `va-t-il`, `va-t-elle`, avec variantes ASCII et U+2011. L'inventaire exhaustif des familles est produit par `scripts/audit_corpus_inversions_008.py`.

Le corpus révèle aussi `rayon-je` / `rayon‑je`, preuve que la graphie directe seule ne suffit pas à affirmer un verbe.

## Non-régression

Les sondes permanentes couvrent :
`suis-je`, `Suis-je`, `porte-t-il`, `Porte-t-il`, `marche-t-elle`, `Marche-t-elle`, `a-t-il`, `A-t-il`, plus des variantes Unicode.

Contre-exemples : `porte-parole`, `porte-monnaie`, `porte-à-faux`, `Je-Suis`, `porte-t-shirt`, début de champ sans tiret, `suis-le`, et `rayon-je` avec candidat non verbal.

La reconstruction versionnée confirme zéro dérive des artefacts PORTE et SUIS.
