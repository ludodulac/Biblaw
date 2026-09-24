# BIBLAW-LINGUISTIC-OCCURRENCES-006 — sélection du deuxième pilote

Baseline : main 55a06f8ed291d9aa7a4bc58d9516ba46d65f0afc.

La sélection a été faite par mesure du corpus avec l'indexeur documentaire existant, avant création de la configuration du pilote.

| Surface | Occurrences brutes | Analyses possibles | Analyses observées dans le corpus | Difficulté |
| --- | ---: | --- | --- | --- |
| marche | 224 | marche/NOUN ; marcher/VERB | les deux | proche du schéma NOM/VERBE déjà rencontré avec PORTE |
| compte | 222 | compte/NOUN ; compter/VERB | les deux | nombreuses locutions figées (« prendre en compte », « rendre compte ») |
| aide | 61 | aide/NOUN ; aider/VERB | les deux | bon homographe mais effectif plus faible |
| garde | 99 | garde/NOUN ; garder/VERB | les deux | clitiques et locutions (« mise en garde »), mais encore NOM/VERBE |
| suis | 631 | être/VERB ; suivre/VERB | les deux | deux lemmes au même POS ; clitique « suis-le » ; inversion « suis-je » ; graphie lexicalisée « Je-Suis » |

## Candidat retenu : SUIS

SUIS est retenu parce qu'il teste une ambiguïté différente de PORTE : la partie du discours ne suffit plus à séparer les analyses. Les deux lectures attestées sont VERB/être et VERB/suivre. Le corpus expose en outre des structures absentes du pilote PORTE : inversion interrogative « suis-je », clitique objet « suis-le » et graphie composée/lexicalisée « Je-Suis ».

La découverte de « suis-je » impose une généralisation structurelle : VERB_INVERSION. Cette catégorie est définie par une frontière tiret + pronom sujet et n'est pas codée comme exception lexicale pour SUIS.

La graphie « Je-Suis » reste COMPOUND_ELEMENT : elle n'est ni l'inversion interrogative ni un clitique objet.

La politique demeure précision avant couverture : les règles propres aux deux lemmes de SUIS vivent dans suis-config.json ; le moteur structurel ne contient aucune branche conditionnelle sur le mot « suis ».
