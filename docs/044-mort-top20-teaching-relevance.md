# BIBLAW-044 — Pertinence des 20 premiers résultats du thème Mort

Question : « Que devient l'homme après la mort ? »

Source : corpus canonique, 20 psaumes entiers, artefact GitHub Actions `biblaw-044-mort-top20-canonical-evidence` (run 38881509892). Ordre reproduit à partir de `js/biblaw.js` : importance, numéro de psaume, identifiant. Pas de preuve Chromium supplémentaire.

**Catégories :** A réponse directe, B pertinent indirectement, C mention / notion Mort sans réponse précise, D hors sujet.

| Rang | Livre / Psaume | Archange | Catégorie | Justification et versets |
|---:|---|---|:---:|---|
| 1 | 03/005 | Raphaël | A | v.16 et 18 : continuité de l'enseignement après la mort du corps. |
| 2 | 20/111 | Ouriel | C | v.2 et 6 : opposition vie divine / monde mortel, sans devenir post-mortem. |
| 3 | 19/112 | Raphaël | B | v.7 : continuité de conscience et lien avec l'âme au-delà de la mort. |
| 4 | 19/118 | Raphaël | B | v.7-10 : séparation et peur de mourir ; préparation intérieure, sans description explicite de l'après-mort. |
| 5 | 19/121 | Raphaël | A | v.1-5 : réincarnation et continuité de conscience après la mort. |
| 6 | 18/130 | Gabriel | B | v.5-8 : identification au corps mortel et conséquences existentielles. |
| 7 | 21/140 | Michaël | C | v.10 et 15 : paroles mortes opposées à la vie transmise. |
| 8 | 22/144 | Gabriel | C | v.4 : impersonalité et purification du corps mortel. |
| 9 | 23/147 | Raphaël | C | v.9-14 : pensées et monde de la mort ; pas de description de l'après-mort. |
| 10 | 21/148 | Michaël | C | v.3 et 11 : valeur des paroles vivantes face au monde de la mort. |
| 11 | 21/150 | Michaël | C | v.12 et 19 : symboles profanés et œil de la mort. |
| 12 | 22/152 | Gabriel | B | v.12 et 22 : continuité de l'œuvre et image de l'eau, pertinence indirecte. |
| 13 | 22/155 | Gabriel | A | v.1-3 : description explicite des mondes rencontrés après la mort. |
| 14 | 22/159 | Gabriel | A | v.8 et 16 : passage vers d'autres mondes et êtres rencontrés. |
| 15 | 21/161 | Michaël | A | v.37 et 40 : poursuite possible du travail et devenir après la mort. |
| 16 | 27/162 | Raphaël | B | v.6 : destinée mortelle et semence d'immortalité, lien indirect. |
| 17 | 27/163 | Raphaël | C | v.5 : savoir mort opposé à esprit de vie. |
| 18 | 28/166 | Ouriel | C | v.3 et 43 : vision juste et exemple du semeur, pas de devenir post-mortem. |
| 19 | 25/167 | Michaël | B | v.3-6 : identité au corps et réalité intérieure, lien indirect. |
| 20 | 27/169 | Raphaël | C | v.15 : serpent et peur comme aspect mortel de la vie. |

**Bilan : A = 5 ; B = 6 ; C = 9 ; D = 0.** Cette classification porte sur la réponse à la question précise, et non sur la validité de la relation générale Mort.

## Extraits canoniques exacts

- Livre 19, psaume 121, v.5 : « Toi qui te demandes si après ta mort tu vas te réincarner ou aller dans un monde d’éternité, sache que l’immortalité commence par la conscience. »
- Livre 22, psaume 155, v.2 : « Sachez que ce que vous vivez durant votre vie avec l’eau qui vous entoure, c’est cela que vous devrez passer après la mort, c’est cette eau que vous rencontrerez. Elle sera vaste comme un océan. »
- Livre 22, psaume 159, v.8 : « Après la mort du corps, a lieu le passage qui conduit l’homme vers les autres mondes. »
- Livre 21, psaume 161, v.40 : « Après la mort, l’homme perd en général le souvenir de son incarnation terrestre et va dans un autre monde où il se fait une autre vie en correspondance avec les organes qu’il s’est faits ou qui ont été faits en lui par certaines intelligences. »

## Diagnostic

Le thème général **Mort** recouvre des enseignements sur le corps mortel, les paroles mortes, la peur de la mort, la vie spirituelle et le passage après le décès. Le classement actuel donne priorité à l'importance éditoriale pour le **thème**, pas à l'adéquation avec une **question précise**. Dans les 12 premiers résultats, seul le psaume 121 (rang 5) est une réponse directe selon ce classement ; trois autres réponses directes se trouvent aux rangs 13–15. Cela ne justifie pas de supprimer les relations générales Mort.

**Correction minimale recommandée, non implémentée :** introduire un classement secondaire *pour les questions précises*, fondé sur les versets déjà indexés et une preuve textuelle vérifiable, en conservant les relations et le classement général lorsque l'utilisateur demande simplement « Mort ». Ne pas déduire la pertinence de la seule présence des mots. Tester ensuite dans Chromium les classements et les références.
