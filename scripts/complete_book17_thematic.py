import json
from pathlib import Path

P = Path('data/thematic-index/books/book-17.json')
data = json.loads(P.read_text(encoding='utf-8'))

A = [
(114,'Les rois de la Lumière',['royauté','unification','Bien commun'],[
 ('unification-des-mondes','Unification des mondes','central','direct',[1,3,11,21,22],'La royauté de Lumière consiste à accueillir, harmoniser et conduire ensemble les règnes et les mondes plutôt qu’à vivre isolé pour soi.'),
 ('generosite','Générosité','important','direct',[6,7,13,14,28],'Donner, partager et construire une œuvre plus grande que soi agrandit la vie et ouvre une relation juste avec les autres êtres.'),
 ('regnes','Règnes','important','direct',[3,5,21,26,29],'Pierres, plantes, animaux, humains et hiérarchies sont inclus dans une même responsabilité d’harmonisation et de Bien commun.')]),
(115,"Comment former ton corps d’éternité",['corps céleste','équilibre','accomplissement'],[
 ('corps-celeste','Corps céleste','central','direct',[2,5,6,8],'L’homme doit former simultanément son corps terrestre et un corps céleste, en transformant l’inspiration supérieure en œuvre concrète.'),
 ('equilibre-des-mondes','Équilibre des mondes','central','direct',[2,3,5,7],'La plénitude demande une tête reliée au divin et des pieds posés sur la terre, sans matérialisme exclusif ni fuite spirituelle.'),
 ('accomplissement','Accomplissement','important','direct',[13,14],'L’homme ne doit être passif dans aucun monde : il présente une œuvre accomplie et la reprend jusqu’à la rendre conforme.')]),
(116,"Les dangers de l’intelligence technologique",['constance','technologie','parole'],[
 ('constance','Constance','central','direct',[1,2,7,12],'La constance et la persévérance rendent l’homme capable de traverser le temps, les difficultés et les influences sans abandonner son orientation.'),
 ('parole','Parole','important','direct',[8,9,12],'Une parole prononcée doit être conduite jusqu’à l’accomplissement ; l’inachevé affaiblit la structure intérieure.'),
 ('influences','Influences','important','direct',[2,3,6,13],'Le système, les modes et certaines illusions spirituelles rendent l’homme influençable, instable et détaché de l’essentiel.')]),
(117,'Une œuvre primordiale pour l’humanité',['œuvre','cultes','quatre sceaux'],[
 ('oeuvre-divine','Œuvre divine','central','direct',[2,4,5,8,9,11,25],'L’œuvre collective donne au monde divin un corps et un lien concret avec la terre ; elle doit demeurer au-delà de l’existence individuelle.'),
 ('quatre-cultes','Quatre cultes','central','direct',[2,15,16,25],'Les cultes du feu, de l’eau, de l’air et de la terre sont présentés comme quatre portes à ouvrir et consacrer pour rétablir l’alliance.'),
 ('quatre-sceaux','Quatre Sceaux','important','direct',[12,13],'Les quatre Sceaux sont une structure de protection, d’intelligence et d’ancrage à poser sur la terre.')]),
(118,'5 questions fondamentales à se poser',['vie','attention','réalisation'],[
 ('vie-interieure','Vie intérieure','central','direct',[2,3,5,7],'Les pratiques ne valent que si elles rendent réellement vivant : l’habitude, la passivité et l’endormissement peuvent vider les formes sacrées de leur vie.'),
 ('concentration','Concentration','central','direct',[4,8],'La concentration permet d’entrer en communion avec l’intelligence d’un enseignement et d’orienter la vie vers une réalisation.'),
 ('realisation','Réalisation','important','direct',[6,7,8],'Le texte sacré est transmis pour toucher le plan physique : la lumière reçue doit obtenir un corps dans la vie.')]),
(119,'La grande règle pour s’approcher du monde divin',['pureté','correspondance','réceptacle'],[
 ('purete','Pureté','central','direct',[1,2,3,6],'Le monde divin ne peut être approché par ce qui lui est incompatible ; la pureté est une condition de correspondance et non une décoration morale.'),
 ('receptivite','Réceptivité','important','direct',[5,6],'La Lumière ne peut habiter un réceptacle incapable de la recevoir et de l’incarner.'),
 ('bien-commun','Bien commun','important','direct',[8],'La prière devient universelle lorsque l’homme prend en compte les règnes et œuvre pour une réalité supérieure plutôt que pour son seul intérêt.')]),
(120,'Le cercle du Bien commun',['Bien commun','cercle','intelligence supérieure'],[
 ('bien-commun','Bien commun','central','direct',[1,7,8],'Le Bien commun naît d’une alliance capable d’accueillir une intelligence supérieure et de la faire descendre jusque dans la réalité terrestre pour tous les êtres.'),
 ('cercle','Cercle','central','direct',[8],'Le cercle est l’espace d’assemblée où les points de vue peuvent être harmonisés autour d’une intelligence plus grande que les opinions individuelles.'),
 ('verite','Vérité','important','direct',[2,3,7,8],'La vérité n’est pas la petite vérité d’un individu : elle harmonise les points de vue et met chaque réalité à sa juste place.')]),
(121,"L’heure du choix",['âme','choix','deux humanités'],[
 ('ame','Âme','central','direct',[1,4,6,8,9,11,23],'L’âme est la lumière individuelle qui relie l’homme aux mondes supérieurs et dont la perte conduit à une conscience collective privée de véritable liberté.'),
 ('choix','Choix','central','direct',[13,14,15,17,21,23],'L’heure du choix oppose deux orientations de l’humanité ; le chemin doit être choisi consciemment avant que l’habitude et les conditionnements ne décident à la place de l’homme.'),
 ('regnes','Règnes','important','direct',[3,4,5],'La destinée de l’âme humaine est liée à celle des pierres, plantes et animaux que l’homme devait éclairer et conduire vers la libération.')]),
(122,'Le temple vivant de la Mère',['Mère','terre consacrée','temple vivant'],[
 ('mere','Mère','central','direct',[2,3,4],'Naître à la Mère signifie préparer intérieurement et extérieurement une terre consciente, pure et aimante où la Lumière puisse réellement se poser.'),
 ('terre-consacree','Terre consacrée','central','direct',[2,3],'La terre consacrée est le fondement concret des activités et des semences du monde supérieur ; sans elle, l’appel à la Lumière reste sans base.'),
 ('regnes','Règnes','important','direct',[3],'Minéraux, végétaux, animaux et éléments doivent retrouver une place vivante dans la réalité quotidienne du temple de la Mère.')]),
(123,"Le vrai et l’imitation du vrai",['vrai','imitation','discernement'],[
 ('verite','Vérité','central','direct',[1],'Le psaume distingue la réalité vivante de la vérité de ses formes imitées ; le critère est ce qui vit réellement et agit dans l’être.'),
 ('imitation','Imitation','central','direct',[1],'L’imitation peut reproduire l’apparence d’une réalité sacrée sans porter sa vie, son intelligence ni son origine.'),
 ('discernement','Discernement','important','direct',[1],'Discerner demande de ne pas confondre ressemblance extérieure et présence effective de la réalité supérieure.')]),
(124,'La flamme perpétuelle de la conscience',['flamme','conscience','vigilance'],[
 ('flamme-de-la-conscience','Flamme de la conscience','central','direct',[1],'La conscience est présentée comme une flamme à maintenir vivante plutôt qu’un état acquis une fois pour toutes.'),
 ('vigilance','Vigilance','important','direct',[1],'Entretenir la flamme demande une présence active qui empêche l’endormissement et la reprise mécanique de la vie.'),
 ('feu','Feu','important','symbolic',[1],'Le feu exprime ici la continuité d’une présence lumineuse capable d’éclairer et d’orienter l’existence.')]),
(125,'Le monde divin envoie son Fils',['deux mondes','intermédiaire','protection'],[
 ('equilibre-des-mondes','Équilibre des mondes','central','direct',[1,2,6,8,22,30],'L’homme doit vivre consciemment dans le matériel et le subtil, unir les mondes sans les mélanger et adapter la sagesse supérieure aux lois de la matière.'),
 ('intermediaire-des-mondes','Intermédiaire des mondes','central','direct',[7,8,10,22],'L’homme formé devient le passage organisé par lequel une intelligence supérieure peut toucher la matière sans confusion.'),
 ('protection-du-sacre','Protection du sacré','important','direct',[12,13,18,20,25],'La relation au divin exige un espace réservé, la pureté, des frontières justes et une Tradition capable de protéger la Lumière des mélanges spirituels.')]),
(126,"Enlever le masque de l’hypocrisie",['hypocrisie','masque','authenticité'],[
 ('hypocrisie','Hypocrisie','central','direct',[1],'Le masque spirituel est dénoncé lorsqu’une apparence de vertu ou de lumière cache une vie qui n’est pas conforme à ce qu’elle affirme.'),
 ('authenticite','Authenticité','central','direct',[1],'Enlever le masque signifie revenir à ce que l’on est réellement afin que la transformation parte d’une vérité reconnue.'),
 ('coherence-interieure','Cohérence intérieure','important','direct',[1],'La cohérence demande que parole, intention et actes cessent de vivre dans des mondes contradictoires.')]),
(127,'Dites non à la barbarie des hommes',['barbarie','règnes','responsabilité'],[
 ('barbarie','Barbarie','central','direct',[1],'La barbarie désigne la violence et l’inconscience humaines lorsqu’elles imposent leur monde aux autres êtres et détruisent les relations sacrées.'),
 ('regnes','Règnes','central','direct',[1],'Le rapport aux autres règnes devient un critère concret de civilisation spirituelle et de responsabilité humaine.'),
 ('responsabilite','Responsabilité','important','direct',[1],'Dire non à la barbarie implique une prise de position et des actes qui cessent d’alimenter les comportements destructeurs.')]),
(128,'Les Évangiles esséniens, une sagesse à vivre',['Évangiles','sagesse vécue','enseignement'],[
 ('evangiles-esseniens','Évangiles esséniens','central','direct',[1],'Les Évangiles sont abordés comme un enseignement destiné à devenir vie et pratique, non comme un objet de croyance ou d’érudition.'),
 ('sagesse-vecue','Sagesse vécue','central','direct',[1],'Une sagesse n’est pleinement reçue que lorsqu’elle transforme la manière de penser, sentir, vouloir et agir.'),
 ('enseignement','Enseignement','important','direct',[1],'Le rapport juste à l’enseignement consiste à l’étudier pour l’incarner et produire une œuvre correspondante.')]),
(129,'Ne pesez pas sur le monde, allégez votre vie',['légèreté','connaissance de soi','lois'],[
 ('legerete','Légèreté','central','direct',[8,9,10,13,16,18,32],'La légèreté consiste à cesser de transmettre aux autres mondes le poids de son désordre, de ses demandes et de ses contradictions.'),
 ('connaissance-de-soi','Connaissance de soi','central','direct',[11,15,17,20,21],'S’étudier permet de distinguer le vrai du faux en soi, de sortir des identifications passives et de remettre de l’ordre dans sa propre maison.'),
 ('lois-divines','Lois divines','important','direct',[2,3,4],'Le monde divin est structuré par des lois qui existent indépendamment des attentes humaines ; l’harmonie vient de l’accord avec elles.')]),
(130,'La porte du culte du feu',['culte du feu','porte','alliance'],[
 ('culte-du-feu','Culte du feu','central','direct',[1],'L’ouverture du culte du feu est présentée comme un acte concret rétablissant un lien entre la terre et un ciel supérieur.'),
 ('porte','Porte','central','symbolic',[1],'La porte symbolise le passage rendu de nouveau possible entre les mondes par une œuvre et une alliance incarnées.'),
 ('alliance','Alliance','important','direct',[1],'Le culte donne une forme terrestre durable à l’alliance avec la Lumière et empêche l’isolement de la terre.')])
]

existing = {x['number'] for x in data.get('psalmAnalyses', [])}
for n,title,signals,themes in A:
    if n in existing:
        continue
    data['psalmAnalyses'].append({
        'recordId': f'book-17-psalm-{n:03d}', 'number': n, 'title': title,
        'titleSignals': signals,
        'themes': [dict(themeId=i,label=l,importance=imp,directness=d,verseNumbers=v,teaching=t) for i,l,imp,d,v,t in themes]
    })
data['psalmAnalyses'].sort(key=lambda x:x['number'])
data['method']['status']='editorial-indexing-complete'
data['bookSynthesis']['centralAxis']="Michaël place l’homme à l’heure d’un choix qui doit devenir une œuvre : sortir de l’illusion et de l’inconstance, retrouver l’âme, la vérité et la connaissance de soi, puis équilibrer les mondes sans les mélanger. La Tradition, la Mère, les règnes, les quatre cultes et les œuvres collectives fournissent une terre concrète où la Lumière peut prendre corps. La fidélité se mesure à la cohérence, à l’accomplissement, au Bien commun et à la capacité de devenir un intermédiaire conscient qui protège le sacré tout en assumant pleinement l’incarnation."
for theme in ['choix','corps-celeste','constance','unification-des-mondes','bien-commun','quatre-cultes','quatre-sceaux','purete','receptivite','mere','terre-consacree','imitation','flamme-de-la-conscience','intermediaire-des-mondes','protection-du-sacre','hypocrisie','barbarie','sagesse-vecue','legerete','lois-divines','culte-du-feu']:
    if theme not in data['bookSynthesis']['majorThemes']:
        data['bookSynthesis']['majorThemes'].append(theme)
P.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('book 17 analyses:', len(data['psalmAnalyses']))
