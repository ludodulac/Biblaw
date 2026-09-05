# Livre 14 — Gabriel — La maîtrise du corps

Date : 2026-09-05

## État

Le livre 14 est traité intégralement dans le nouvel index thématique éditorial : psaumes 82 à 110, soit 29 psaumes. Les titres sont utilisés comme indices de lecture, les notes comme contexte éditorial et documentaire, et les prières restent exclues de l’indexation thématique principale.

Fichier d’expertise : `data/thematic-index/books/book-14.json`.

## Axe du livre

Gabriel enseigne la maîtrise du corps comme un art d’organisation de toute la vie : corps physique, sens, eau intérieure, relations et œuvres doivent devenir des supports conscients du monde divin. Le livre relie continuellement préparation, discipline, incarnation de la Lumière, savoir vivant, action, union, purification de l’eau des relations, corps collectif, responsabilité et dialogue avec la Mère, les règnes, les Anges et les mondes subtils.

La maîtrise n’est pas un rejet du corps : le corps doit être éduqué, harmonisé et placé à sa juste fonction de serviteur et d’allié afin que l’être intérieur puisse devenir maître de sa destinée et que la Lumière reçoive un corps sur la terre.

## Entrées thématiques particulièrement structurantes

Le livre enrichit fortement les thèmes `corps`, `maitrise-de-soi`, `eau`, `corps-interieur`, `lumiere`, `oeuvre`, `savoir-vivant`, `union`, `corps-collectif`, `tradition`, `relations`, `guerison`, `interdependance`, `responsabilite`, `preparation`, `sens-subtils`, `discernement`, `ame` et `famille`.

Il apporte aussi des thèmes précis qui doivent rester recherchables en tant que tels : `biche`, `nenuphar`, `canigou`, `serpent-de-la-sagesse`, `serpent-de-la-destruction`, `clairvoyance`, `tissage-des-relations`, `guerison-des-relations`, `assimilation`, `regard`, `fleur`, `cycle`, `individualite-consciente` et `enracinement`.

## Correctif documentaire découvert pendant l’indexation

L’analyse du livre a révélé un défaut déterministe du normaliseur de notes : dans trois cas, la fin d’un verset interrompu par une note avait été absorbée par la note éditoriale. Les cas audités sont Gabriel 86:6, 87:7 et 110:6. Ils ne constituent pas des ambiguïtés éditoriales et ne sont donc pas ajoutés au registre des incohérences.

`scripts/normalize_notes_resumed_verses.py` contient désormais des réparations exactes et idempotentes, adossées au texte source, afin que ces séparations verset/note ne réapparaissent pas lors d’une nouvelle extraction.

## Validation thématique

L’ajout du livre 14 porte l’index à 14 livres, 365 analyses de psaumes et 1 165 relations thématiques. Une première validation a signalé uniquement trois valeurs `contextual` non autorisées par l’ancien enum du validateur, pour Canigou, Nénuphar et Biche. Le modèle éditorial ayant besoin de cette relation contextuelle (notamment lorsqu’une note éclaire un thème), le validateur a été corrigé pour accepter `contextual` au lieu de rabattre artificiellement ces cas sur `direct`.

## Suite

Poursuivre avec le livre 15 à partir de ses source packs déjà générés, en conservant la même méthode : analyse du livre entier, psaume par psaume, puis synthèse inter-psaumes et enrichissement transversal des thèmes.
