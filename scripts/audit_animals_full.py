#!/usr/bin/env python3
"""Audit read-only: 1,158 canonical Psalms + their attached notes against animal index.

This lexical inventory surfaces candidates for human reading, not automatic classifications.
No canonical text or public site asset is modified.
"""
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def norm(s):
    s = s.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
def matcher(forms):
    x = "|".join(re.escape(norm(w)) for w in forms)
    return re.compile(r"(?<![a-z])(?:" + x + r")(?![a-z])")
species = """
Albatros|albatros
Alouette|alouette alouettes
Anguille|anguille anguilles
Autruche|autruche autruches
Baleine|baleine baleines
Bison|bison bisons
Blaireau|blaireau blaireaux
Buffle|buffle buffles
Cafard|cafard cafards blatte blattes
Carpe|carpe carpes
Castor|castor castors
Chacal|chacal chacals
Chameau|chameau chameaux
Chamois|chamois
Chevreuil|chevreuil chevreuils
Chèvre|chèvre chèvres
Cigale|cigale cigales
Cigogne|cigogne cigognes
Corbeau|corbeau corbeaux
Cormoran|cormoran cormorans
Crapaud|crapaud crapauds
Crocodile|crocodile crocodiles
Daim|daim daims daine daines
Dinde|dinde dindes dindon dindons
Écureuil|écureuil écureuils
Éléphant|éléphant éléphants
Épervier|épervier éperviers
Faucon|faucon faucons
Fennec|fennec fennecs
Fourmilier|fourmilier fourmiliers
Gazelle|gazelle gazelles
Geai|geai geais
Girafe|girafe girafes
Gorille|gorille gorilles
Grillon|grillon grillons
Grenouille|grenouille grenouilles
Grue|grue grues
Hérisson|hérisson hérissons
Héron|héron hérons
Hibou|hibou hiboux
Hirondelle|hirondelle hirondelles
Hippopotame|hippopotame hippopotames
Huppe|huppe huppes
Jaguar|jaguar jaguars
Kangourou|kangourou kangourous
Koala|koala koalas
Lama|lama lamas
Léopard|léopard léopards
Lièvre|lièvre lièvres
Limace|limace limaces
Loutre|loutre loutres
Luci ole|luciole lucioles
Lynx|lynx
Marmotte|marmotte marmottes
Mésange|mésange mésanges
Merle|merle merles
Moineau|moineau moineaux
Moule|moule moules
Oie|oie oies
Ours|ours ourse ourses ourson oursons
Panda|panda pandas
Paon|paon paons
Pélican|pélican pélicans
Perdrix|perdrix
Phoque|phoque phoques
Pigeon|pigeon pigeons
Pintade|pintade pintades
Pou|pou poux
Poule|poule poules poulet poulets poussin poussins
Puce|puce puces
Punaise|punaise punaises
Rat|rat rats
Renard|renard renards renarde renardes
Rhinocéros|rhinocéros
Rossignol|rossignol rossignols
Sanglier|sanglier sangliers
Scorpion|scorpion scorpions
Singe|singe singes
Sphinx|sphinx
Taureau|taureau taureaux
Tourterelle|tourterelle tourterelles
Truite|truite truites
Vautour|vautour vautours
Zèbre|zèbre zèbres
Abeille|abeille abeilles
Agneau|agneau agneaux
Aigle|aigle aigles
Âne|âne ânes
Araignée|araignée araignées
Biche|biche biches
Boeuf|bœuf bœufs boeuf boeufs
Bouc|bouc boucs
Canard|canard canards caneton canetons
Caméléon|caméléon caméléons
Cerf|cerf cerfs
Chat|chat chats chatte chattes
Cheval|cheval chevaux jument juments poulain poulains
Chenille|chenille chenilles
Chien|chien chiens chienne chiennes
Chouette|chouette chouettes
Coccinelle|coccinelle coccinelles
Cobra|cobra cobras
Colombe|colombe colombes
Coq|coq coqs
Coquillage|coquillage coquillages
Cygne|cygne cygnes
Dauphin|dauphin dauphins
Dragon|dragon dragons
Escargot|escargot escargots
Flamant rose|flamant rose flamants roses
Fouine|fouine fouines
Fourmi|fourmi fourmis
Guêpe|guêpe guêpes
Huître|huître huîtres
Insecte|insecte insectes
Lapin|lapin lapins lapine lapines
Lézard|lézard lézards
Libellule|libellule libellules
Licorne|licorne licornes
Lion|lion lions lionne lionnes
Loup|loup loups louve louves louveteau louveteaux
Mouche|mouche mouches
Moustique|moustique moustiques
Mouton|mouton moutons brebis brebi
Oiseau|oiseau oiseaux oisillon oisillons
Papillon|papillon papillons
Perroquet|perroquet perroquets
Phénix|phénix phoenix
Pieuvre|pieuvre pieuvres
Poisson|poisson poissons
Pourceau|pourceau pourceaux cochon cochons porc porcs truie truies
Requin|requin requins
Salamandre|salamandre salamandres
Serpent|serpent serpents
Souris|souris
Taupe|taupe taupes
Tigre|tigre tigres
Tique|tique tiques
Tortue|tortue tortues
Vache|vache vaches
Veau|veau veaux
Ver|ver vers
Vipère|vipère vipères
"""
# Unlike the published lexicon, here "vers" is intentionally excluded:
# ambiguous preposition vastly inflates references to the animal "ver".
species=species.replace("brebis brebi","brebis").replace("Ver|ver vers","Ver|ver")
# Delimiter / whitespace separation intentionally treats multiword "flamant rose" specially.
patterns={}
for line in species.strip().splitlines():
    label,forms=line.split("|",1)
    terms=forms.split() if label!="Flamant rose" else ["flamant rose","flamants roses"]
    patterns[label]=matcher(terms)
animal_entries=json.loads((ROOT/"data/animals-editorial.json").read_text())["entries"]
existing={norm(e["label"]) for e in animal_entries}
indexed_patterns={e["id"]:matcher(e["forms"]) for e in animal_entries}
records=[]
for p in sorted((ROOT/"data/corpus/books").glob("book-*/psalm-*.json")):
    r=json.loads(p.read_text())
    if r.get("recordType")=="psalm":
        records.append(r)
assert len(records)==1158, len(records)
notes=[]
for p in sorted((ROOT/"data/notes/books").glob("book-*/*.json")):
    r=json.loads(p.read_text())
    if r.get("recordType")=="note":notes.append(r)
occur=defaultdict(list)
title_hits=defaultdict(list)
for r in records:
    record=r["id"];title=norm(r.get("title",""))
    title_restricted=re.sub(r"cerf[\s\-]+volant","",title)
    for label,pat in patterns.items():
        if pat.search(title_restricted):
            title_hits[label].append((record,r.get("title","")))
    for verse in r.get("verses",[]):
        t=norm(verse["text"])
        for label,pat in patterns.items():
            if pat.search(t) and not (label=="Cerf" and re.search(r"\bcerf[\s\-]+volant\b",t) and not re.search(r"\bcerfs?\b(?![\s\-]+volant)",t)):
                occur[label].append((record,verse["number"],verse["text"]))
missing=[]
for label,arr in occur.items():
    other_names={"Boeuf":"Bœuf","Chat":"Chat noir","Lion":"Lion et lionne","Serpent":"Serpent tentateur","Ver":"Ver"}
    covered=norm(other_names.get(label,label)) in existing
    # Not automatically considered covered if presence of only a broad class (e.g. 'Insecte')
    if not covered:
        missing.append((label,len(arr),len({v[0] for v in arr}),title_hits[label],arr))
missing.sort(key=lambda z:(-len(z[3]),-z[2],-z[1],z[0]))
print("ANIMAL_AUDIT_START")
print(f"CORPUS: {len(records)} PSAUMES, {len(notes)} NOTES, {len(animal_entries)} FICHES, {len(existing)} LIBELLES UNIQUES")
print(f"SPECIES_LEXICON: {len(patterns)} groups; missing represented species groups: {len(missing)}")
for label,count,psalms,titles,arr in missing:
    print("MISSING",label,"verses",count,"psalms",psalms,"titles",len(titles))
    for record,title in titles[:3]:print("  TITLE",record,repr(title)[:135])
    for record,v,body in arr[:3]:print("  VERSE",record,v,repr(body)[:250])
print("INDEXED_ENTRIES_WITH_NO_LEXICAL_OCCURRENCES:")
for e in animal_entries:
    matches=[(r["id"],v["number"]) for r in records for v in r.get("verses",[]) if indexed_patterns[e["id"]].search(norm(v["text"]))]
    if not matches:print("  EMPTY",e["id"],e["label"])
print("TOTEM_WORD_IN_VERSES:")
hit=0
for r in records:
    for v in r.get("verses",[]):
        t=norm(v["text"])
        if re.search(r"\btotem(s)?\b|\banimal(-|\s)guide(s)?\b",t):
            hit+=1
            if hit<=75:print("  TOTEM",r["id"],v["number"],repr(v["text"])[:600])
print("TOTEM_VERSES_COUNT:",hit)
print("ANIMAL_TITLES:")
for label,arr in sorted(title_hits.items()):
    if arr:print("  TITLES",label,len(arr),";".join(str(z[0])+":"+str(z[1])[:90] for z in arr[:4]))
print("ANIMAL_NOTES_POTENTIAL:")
note_hits=0
for n in notes:
    words=norm(n.get("text",""))
    ls=[label for label,pat in patterns.items() if pat.search(words)]
    unknown=[x for x in ls if x in [y[0] for y in missing]]
    if unknown:
        note_hits+=1
        if note_hits<=55:print("  NOTE",n["id"],"/".join(unknown[:10]),repr(n.get("text",""))[:260])
print("NOTES_MISSING_SPECIES_COUNT:",note_hits)
print("ANIMAL_AUDIT_END")
