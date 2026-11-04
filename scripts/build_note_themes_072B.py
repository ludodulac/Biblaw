#!/usr/bin/env python3
"""072B: reproducible, *provisional* note-theme crosswalk. Never publish historic notes.

Read actual JSON note text/summary, in batches of TEN. Reuse audited labels from
missions/072/NOTES_THEMES_LOT_001.md. Remaining labels are evidence-backed lexical
proposals, NOT human thematic validation or source authentication.
The private crosswalk contains IDs/evidence only and is never copied to Pages.
"""
from __future__ import annotations
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BOOK_NOTES=ROOT/"data/notes/books"
OUT_PRIVATE=ROOT/"data/note-themes-working-072B.json"
OUT_PUBLIC=ROOT/"data/note-themes-public-072B.json"
LOT_001=ROOT/"missions/072/NOTES_THEMES_LOT_001.md"

def normalize(value):
    t=unicodedata.normalize("NFD",str(value or "")).lower()
    t="".join(ch for ch in t if unicodedata.category(ch)!="Mn")
    return t.replace("’","'").replace("œ","oe").replace("æ","ae")

# Conservative theme labels: patterns apply to the content only, never to file names,
# neighboring Psalms, source metadata, titles or alleged sense classifications.
# Repeated synonyms intentionally converge on the same theme.
RULES=[
("Célébrations archangéliques",r"\bcelebration(?:s)?\b|\bsolstice\b|\bequinoxe\b"),
("Méditation et prière",r"\bprier(?:es|e|s)?\b|\bmeditat(?:ion|ions|if|ifs|ive|ives)\b|\binvocation(?:s)?\b"),
("Temples esséniens",r"\btemple(?:s)?\b|\bsanctuaire(?:s)?\b"),
("Consécration des lieux",r"\bconsacr(?:er|ation|e|ee|es)\b.{0,80}\b(?:lieu|espace|terre|temple)\b|\b(?:lieu|espace|terre|temple)\b.{0,80}\bconsacr"),
("Pyramides de pierres",r"\bpyramide(?:s)?\b"),
("Textes sacrés",r"\btextes?\s+sacr(?:e|es)\b|\bparole\s+de\s+dieu\b|\becritures?\s+sacrees?\b"),
("Enseignements des archanges",r"\benseignement(?:s)?\b|\btransmi(?:s|se|sses)\b|\btransmission\b"),
("Olivier Manitara",r"\bolivier\s+manitara\b"),
("Montagnes sacrées",r"\bmontagne(?:s)?\b|\bmontsegur\b"),
("Statues sacrées",r"\bstatue(?:s)?\b|\beffigie(?:s)?\b"),
("Villages esséniens",r"\bvillages?\s+essenien(?:s)?\b|\bterranova\b|\bvillage\s+de\s+l.erable\b"),
("Pierres sacrées",r"\bpierre(?:s)?\b|\bjade\b|\bnephrite\b|\bactinolite\b|\bcristal\b"),
("Huile d’Ouriel",r"\bhuile\s+d.ouriel\b|\bhuile\s+sacr(?:e|ee)\b"),
("Vie quotidienne essénienne",r"\bvie\s+quotidienne\b|\bhygiene\s+corporelle\b|\balimentation\b|\btravail\s+quotidien\b"),
("Ronde des Archanges",r"\bronde\s+des\s+archanges\b|\bcycle(?:s)?\s+de\s+.{0,18}celebration"),
("Alliance avec le monde divin",r"\balliance(?:s)?\b|\bpacte(?:s)?\b|\bun(?:ion|i)\s+avec\s+(?:dieu|le\s+(?:monde\s+)?divin)\b"),
("Eau sacrée",r"\beau(?:x)?\b|\bsource(?:s)?\b|\bfontaine(?:s)?\b|\briviere(?:s)?\b"),
("Feu et flammes",r"\bfeu(?:x)?\b|\bflamme(?:s)?\b|\bbrasier\b"),
("Bénédiction et lumière",r"\blumiere\b|\bbenediction(?:s)?\b|\bbenir\b|\bbeni(?:e|s|es)?\b"),
("Nation essénienne",r"\bnation\s+essenienne\b|\bpeuple\s+essenien\b|\beglise\s+essenienne\b"),
("Archanges et anges",r"\b(?:ange(?:s)?|archange(?:s)?)\b.{0,75}\b(?:monde(?:s)?\s+divin|dieux|hierarchie|regne(?:s)?)\b|\bregne(?:s)?\b.{0,40}\b(?:ange|archange)\b"),
("Prêtrise et initiation",r"\bpret(?:re|res|resse|resses)\b|\binitiat(?:ion|ions|ique|iques)\b|\bconsacration\s+a\s+la\s+pretrise\b"),
("Rituels et cultes",r"\brituel(?:s)?\b|\bculte(?:s)?\b|\bautel(?:s)?\b|\bceremonie(?:s)?\b"),
("Dates et événements historiques",r"\b(?:19|20)\d{2}\b|\bhiver\b|\bete\b|\bprintemps\b|\bautomne\b|\bepoque\b"),
("Lieux et géographie",r"\bfrance\b|\bquebec\b|\bgabon\b|\bsaint.girons\b|\bcanada\b|\bterre\s+des\s+cathares\b"),
("Références aux psaumes",r"\b(?:psaume(?:s)?|verset(?:s)?)\s+\d+\b|\bvoir\s+(?:les?\s+)?(?:psaumes?|versets?)\b"),
("Références aux évangiles",r"\bevangile\b|\bmatthieu\b|\bjean\b|\bluc\b|\bmarc\b|\bbible\b"),
("Symboles et nombres sacrés",r"\bsymbol(?:e|es|ique|iques)\b|\b\d+\s+(?:marches|regnes|commandements|sceaux)\b|\bsceau(?:x)?\b"),
("Commandements et lois",r"\bcommandement(?:s)?\b|\bloi(?:s)?\s+(?:divine|sacree|universelle)\b"),
("Nature et règnes",r"\b(?:arbre(?:s)?|animal(?:aux|s)?|chouette(?:s)?|oiseau(?:x)?|totem(?:ique|iques)?|regne(?:s)?\s+de\s+la\s+creation)\b"),
("Guérison et soins",r"\bgueri(?:son|r|t|s)\b|\btherapeutique(?:s)?\b|\bbaume(?:s)?\b|\bsoin(?:s)?\b"),
("Corps et âme",r"\bcorps\b|\bame(?:s)?\b|\besprit(?:s)?\b"),
("Monde invisible",r"\bmonde(?:s)?\s+subtil(?:s)?\b|\binvisible\b|\betre(?:s)?\s+celeste(?:s)?\b"),
("Mort et passage",r"\bmort(?:s)?\b|\bdefunt(?:s)?\b|\breincarnation\b|\bapres.vie\b"),
("Famille et filiation",r"\bfamille(?:s)?\b|\bancetre(?:s)?\b|\bparent(?:s)?\b|\benfant(?:s)?\b"),
("Histoire des Esséniens",r"\bessenien(?:s)?\b.{0,90}\b(?:histoire|tradition|origine|fonde|rene)\b|\b(?:histoire|tradition|origine)\b.{0,90}\bessenien"),
("Religions et traditions",r"\breligion(?:s)?\b|\bcathare(?:s)?\b|\bchretien(?:s|ne|nes)?\b|\bjuif(?:s|ve|ves)?\b"),
("Éducation et discipline",r"\beducation\b|\bdiscipline\b|\bappren(?:dre|tissage)\b|\bformation\b"),
("Gouvernement et organisation",r"\bgouvernement\b|\borganis(?:ation|er)\b|\binstitution(?:s)?\b"),
("Paroles et adresses",r"\bs.adresse\s+(?:ici\s+)?a\b|\bil\s+s.agit\s+d(?:u|e\s+la)\b|\bl.archange\s+(?:parle|s.adresse)\b"),
("Pratiques de la vie intérieure",r"\bsilence\b|\bconscience\b|\bintelligence\s+superieure\b|\bpensee(?:s)?\b"),
("Offrandes et dons",r"\boffrande(?:s)?\b|\bdon(?:s)?\s+(?:de\s+|a\s+)\b"),
("Terre et humanité",r"\bhumanite\b|\bterre\b|\bmonde\s+des\s+hommes\b"),
]

# 072C: fine-grained keyword entries based on the owner's example A.
# These are text-evidenced indexing proposals, not human-authenticated topics.
FINE_RULES=[
("Montagne sacrée",r"\bmontagne(?:s)?\s+sacree(?:s)?\b"),
("Montagne",r"\bmontagne(?:s)?\b"),
("Retraite",r"\bretraite(?:s)?\b"),
("7 prêtres",r"\b7\s+pretres\b"),
("Prêtres",r"\bpretres?\b"),
("Mondes subtils",r"\bmondes?\s+subtils?\b"),
("Prière",r"\bprier(?:e|es|s)?\b|\bprie(?:nt|r|z)?\b"),
("Méditation",r"\bmeditat(?:ion|ions|if|ifs|ive|ives)\b|\bmediter\b"),
("Énergie",r"\benergies?\b"),
("Force",r"\bforces?\b"),
("Forces sacrées",r"\bforces?\s+sacrees?\b"),
("Célébration",r"\bcelebration(?:s)?\b"),
("Archange",r"\barchanges?\b"),
("Silence",r"\bsilence\b"),
("Esséniens",r"\besseniens?\b"),
("Lumière",r"\blumiere\b"),
("Bénédiction",r"\bbenediction(?:s)?\b|\bbenie?s?\b"),
("Pyramide",r"\bpyramides?\b"),
("Pierres",r"\bpierres?\b"),
("Textes sacrés",r"\btextes?\s+sacres?\b"),
("Consécration",r"\bconsacr(?:ation|er|e|ee|es)\b"),
("Statue",r"\bstatues?\b"),
("Temple",r"\btemples?\b"),
("Fontaine",r"\bfontaines?\b"),
("Source d’eau",r"\bsources?\s+d.eau\b"),
("Source naturelle",r"\bsources?\s+naturelles?\b"),
("Eau",r"\beaux?\b"),
("Eau bénie",r"\beaux?\s+benies?\b"),
("Rivière",r"\brivieres?\b"),
("Océan",r"\bocean\b"),
("Village essénien",r"\bvillages?\s+esseniens?\b"),
("Terranova",r"\bterranova\b"),
("France",r"\bfrance\b"),
("Québec",r"\bquebec\b"),
("Gabon",r"\bgabon\b"),
("Olivier Manitara",r"\bolivier\s+manitara\b"),
("Michaël",r"\bmichael\b"),
("Gabriel",r"\bgabriel\b"),
("Raphaël",r"\braphael\b"),
("Ouriel",r"\bouriel\b"),
("Enseignement",r"\benseignements?\b"),
("Psaume",r"\bpsaumes?\b"),
("Prêtrise",r"\bpretrise\b"),
("Rituel",r"\brituels?\b"),
("Feu",r"\bfeux?\b"),
("Flamme",r"\bflammes?\b"),
("Alliance",r"\balliances?\b"),
("Monde divin",r"\bmonde\s+divin\b"),
("Terre",r"\bterre\b"),
("Corps",r"\bcorps\b"),
("Âme",r"\bames?\b"),
("Nature",r"\bnature\b"),
("Hiver",r"\bhiver\b"),
("Été",r"\bete\b"),
("Printemps",r"\bprintemps\b"),
("Automne",r"\bautomne\b"),
]
OWNER_A_ID="book-01-psalm-004-note-001"
OWNER_A_LABELS=["Montagne sacrée","Montagne","Retraite","7 prêtres","Mondes subtils",
                "Prière","Méditation","Énergie","Force","Forces sacrées",
                "Célébration","Archange","Silence"]

# The first ten have already been examined manually in the existing project.
# Read that first-lot markdown as data, keeping its stated evidence (no hidden reclassification).
def validated_first_lot():
    rows={}
    for line in LOT_001.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| book-"):continue
        cols=[v.strip() for v in line.strip().strip("|").split("|")]
        if len(cols)!=3:raise RuntimeError("Bad Lot 001 row: "+line)
        rows[cols[0]]={"themes":[v.strip() for v in cols[1].split(";")],
                       "evidence":[cols[2]]}
    assert len(rows)==10,"First hand-examined lot must have 10 notes"
    return rows

def propose(note,first):
    ident=note.get("id","")
    content=(note.get("text") or note.get("summary") or "").strip()
    if not content:return {"themes":[],"evidence":[],"review":"missing-text"}
    folded=normalize(content)
    if ident==OWNER_A_ID:
        return {"themes":OWNER_A_LABELS[:],"evidence":["classement fourni par Ludo"],
                "review":"owner-validated-keywords"}
    fine=[]
    for name,pat in FINE_RULES:
        hit=re.search(pat,folded,re.I)
        if hit:fine.append({"name":name,"evidence":hit.group(0)[:90]})
    # Keep previously reviewed broad labels as complementary navigation,
    # but never let them suppress the more precise text-grounded keywords.
    broad=[]
    if ident in first:
        broad=[{"name":name,"evidence":"first-lot manual review"} for name in first[ident]["themes"]]
    else:
        for name,pat in RULES:
            hit=re.search(pat,folded,re.I)
            if hit:broad.append({"name":name,"evidence":hit.group(0)[:90]})
    chosen=[]
    seen=set()
    for item in fine+broad:
        if item["name"] not in seen:
            chosen.append(item);seen.add(item["name"])
    return {"themes":[x["name"] for x in chosen],
            "evidence":[x["evidence"] for x in chosen],
            "review":"proposed-fine-keywords-needs-review" if chosen else "unclassified-evidence-insufficient"}

def main():
    first=validated_first_lot()
    paths=sorted([*BOOK_NOTES.glob("book-*/book-*-note-*.json"),
                  *(ROOT/"data/notes").glob("michael-psalm-*-note-*.json")])
    # Legacy alias files are real readable notes, but remain unpublished; they
    # are included separately under their original IDs, never merged or promoted.
    # Historic notes under books/ are not part of the public Browser corpus.
    assert len(paths)>=200,"Expected historic note archive to be present"
    inventory=[]
    issues=[]
    for batch_start in range(0,len(paths),10):
        batch=paths[batch_start:batch_start+10]
        for path in batch:
            try:note=json.loads(path.read_text(encoding="utf-8"))
            except (ValueError,UnicodeError) as e:
                issues.append({"path":str(path.relative_to(ROOT)),"reason":"invalid-json: "+str(e)})
                continue
            if note.get("recordType")!="note" or not note.get("id"):
                issues.append({"path":str(path.relative_to(ROOT)),"reason":"not-a-note"})
                continue
            decision=propose(note,first)
            inventory.append({"id":note["id"],"path":str(path.relative_to(ROOT)),
                              "sourceValidation":note.get("validation",{}).get("status","unknown"),
                              **decision,"lot":batch_start//10+1,"visibility":"private-historic"})
    assert len(inventory)==len(paths)-len(issues),"A historic note was silently dropped"
    by_id={n["id"]:n for n in inventory}
    assert len(by_id)==len(inventory),"Duplicate historic IDs require manual review"
    public_catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"))["records"]
    public_paths=[ROOT/p for p in public_catalog if p.startswith("data/notes/")]
    assert len(public_paths)==11,"Do not expand public note set"
    public_ids=[]
    for path in public_paths:
        note=json.loads(path.read_text(encoding="utf-8"))
        ident=note["id"];public_ids.append(ident)
        assigned=propose(note,first)
        if ident in by_id:
            record=by_id[ident]
            record["visibility"]="already-public"
            # Public note has the actual text/summary that users see.
            record["themes"]=assigned["themes"]
            record["evidence"]=assigned["evidence"]
            record["review"]=assigned["review"]
            record["sourceValidation"]=note.get("validation",{}).get("status","unknown")
        else:
            issues.append({"id":ident,"reason":"public-note-not-found-in-historical-books"})
            inventory.append({"id":ident,"path":str(path.relative_to(ROOT)),"visibility":"already-public",
                "lot":(len(paths)+len(public_ids)-1)//10+1,"sourceValidation":note.get("validation",{}).get("status","unknown"),
                **assigned})
    # Every historic note and every already-public ID is present exactly once.
    seen=set()
    for n in inventory:
        assert n["id"] not in seen,n["id"]
        seen.add(n["id"])
    thematic=defaultdict(list)
    for n in inventory:
        for label in n["themes"]:
            thematic[label].append(n["id"])
    themes=[{"label":label,"noteIds":sorted(set(ids)),"count":len(set(ids))}
            for label,ids in sorted(thematic.items(),key=lambda x:normalize(x[0]))]
    public_set=set(public_ids)
    public_themes=[{"label":t["label"],"noteIds":[i for i in t["noteIds"] if i in public_set]}
                  for t in themes]
    public_themes=[{**t,"count":len(t["noteIds"])} for t in public_themes if t["noteIds"]]
    # Prevent exposing metadata, text, filenames, statuses of nonpublic notes.
    assert {i for t in public_themes for i in t["noteIds"]}.issubset(public_set)
    assert len(public_set)==len(public_ids)==11
    private={"version":1,"status":"provisional-theme-proposals-not-human-authentication",
         "noteCount":len(inventory),"lotSize":10,"historicalLots":(len(paths)+9)//10,
         "publicNoteIds":sorted(public_ids),"notes":inventory,"themes":themes,"issues":issues,
         "uncertainIds":[n["id"] for n in inventory if n["review"] in ("missing-text","unclassified-evidence-insufficient")]}
    public={"version":1,"purpose":"note-theme-navigation-already-public-only",
            "notAnAuthentication":True,"publicNoteCount":11,"themes":public_themes}
    OUT_PRIVATE.parent.mkdir(parents=True,exist_ok=True)
    OUT_PRIVATE.write_text(json.dumps(private,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT_PUBLIC.write_text(json.dumps(public,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("BIBLAW-072B LOTS",private["historicalLots"],"historic notes",len(paths),
          "distinct indexed notes",len(inventory),"public",len(public_ids),
          "themes",len(themes),"uncertain",len(private["uncertainIds"]))
    print("BIBLAW-072B THEMES",json.dumps([{"theme":t["label"],"total":t["count"],
       "public":sum(i in public_set for i in t["noteIds"])} for t in themes],ensure_ascii=False))
    if issues:print("BIBLAW-072B ISSUES",json.dumps(issues,ensure_ascii=False))
    print("BIBLAW-072B UNCERTAIN",json.dumps(private["uncertainIds"],ensure_ascii=False))

if __name__=="__main__":
    main()
