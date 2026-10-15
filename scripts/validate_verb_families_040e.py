#!/usr/bin/env python3
"""040E: conservative intersection of 040D spaCy inventory and pinned Morphalou 3.1."""
import csv,hashlib,io,json,sys,unicodedata,zipfile
from collections import defaultdict
from pathlib import Path
from build_lexical_expansion_runtime import MORPHALOU_SHA256,MORPHALOU_MEMBER,sha256_file,morph_norm

inventory=Path(sys.argv[1]); morph=Path(sys.argv[2]); out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
assert sha256_file(morph)==MORPHALOU_SHA256,"Morphalou source hash mismatch"
def read(name):
    with (inventory/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
data=read("verbes-corpus-040d.csv")
ambiguous={r["forme"] for r in read("formes-ambigues-040d.csv")}
unknown={r["forme"] for r in read("formes-non-reconnues-040d.csv")}
aux={"être","avoir"}
def norm(s):return unicodedata.normalize("NFC",s).casefold()
def parse(s):
    items=[]
    for x in s.split("; "):
        if not x:continue
        form,count=x.rsplit(" (",1);items.append((form,int(count[:-1])))
    return items
wanted={(norm(row["infinitif"]),norm(form)) for row in data if norm(row["infinitif"]) not in aux for form,_ in parse(row["formes_observees"])}
confirmed=set(); seen_lemmas=set()
with zipfile.ZipFile(morph) as z:
    with z.open(MORPHALOU_MEMBER) as raw,io.TextIOWrapper(raw,encoding="utf-8-sig",newline="") as f:
        started=False;lemma="";category=""
        for line in f:
            if not started:
                if line.startswith("GRAPHIE;ID;CATÉGORIE;"):started=True
                continue
            row=next(csv.reader([line],delimiter=";"))
            if len(row)<18:continue
            if row[0]:lemma,category=row[0],row[2]
            elif row[2]:category=row[2]
            if category!="Verbe":continue
            key=norm(lemma);seen_lemmas.add(key)
            form=row[9]
            if form and (key,norm(form)) in wanted:confirmed.add((key,norm(form)))
            # Infinitive itself is an observed form and a Morphalou verb lemma.
            if (key,key) in wanted:confirmed.add((key,key))
def stem(lemma):
    if lemma.endswith(("er","ir","re")) and len(lemma)>5:return lemma[:-2]
    return None
rows=[]; amb_rows=[]; unsupported_rows=[];valid_forms=set();excluded_forms=set()
validated_occ=0;all_occ=0;statuses=defaultdict(int)
for row in data:
    lemma=norm(row["infinitif"])
    if lemma in aux:continue
    base=stem(lemma);good=[];bad=[];uncertain=[]
    for form,count in parse(row["formes_observees"]):
        form=norm(form);all_occ+=count
        if form in ambiguous or form in unknown:
            uncertain.append((form,count,"AMBIGUOUS_CONTEXT" if form in ambiguous else "UNKNOWN"))
        elif (lemma,form) not in confirmed:
            bad.append((form,count,"NOT_CONFIRMED_BY_MORPHALOU"))
        elif base is None or not form.startswith(base):
            bad.append((form,count,"INITIAL_STEM_NOT_ESTABLISHED"))
        else:
            good.append((form,count));validated_occ+=count;valid_forms.add((lemma,form))
    if uncertain:status="AMBIGUOUS"
    elif good:status="VALIDATED_CANDIDATE"
    else:status="UNSUPPORTED"
    statuses[status]+=1
    for form,count,why in uncertain:amb_rows.append((lemma,form,count,why))
    for form,count,why in bad:unsupported_rows.append((lemma,form,count,why));excluded_forms.add((lemma,form))
    rows.append({"infinitif":lemma,"radical_retenu":base or "","formes_observees":"; ".join(f"{f} ({c})" for f,c in good),
      "nombre_formes":len(good),"occurrences_couvertes":sum(c for _,c in good),"statut_validation":status,
      "source_morphologique":"Morphalou 3.1 ATILF LGPL-LR sha256:"+MORPHALOU_SHA256,
      "ambiguites":"; ".join(f for f,_,_ in uncertain)})
rows.sort(key=lambda r:(-r["occurrences_couvertes"],r["infinitif"]))
def write(name,fields,items):
    with (out/name).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(fields);w.writerows(items)
write("familles-verbales-040e.csv",list(rows[0]),([r[k] for k in rows[0]] for r in rows) if False else ([r[k] for k in rows[0].keys()] for r in rows))
write("formes-ambigues-040e.csv",["infinitif","forme","occurrences","raison"],amb_rows)
write("formes-non-confirmees-040e.csv",["infinitif","forme","occurrences","raison"],unsupported_rows)
report={"mission":"BIBLAW-OCCV2-040E","source":"Morphalou 3.1 ATILF/CNRS, official dataset mirror datasets-CNRS/Morphalou","version":"3.1","license":"LGPL-LR","sha256":MORPHALOU_SHA256,
"total_verbs_examined":len(rows),"validated_families":statuses["VALIDATED_CANDIDATE"],"ambiguous_families":statuses["AMBIGUOUS"],"unsupported_families":statuses["UNSUPPORTED"],
"validated_distinct_lemma_form_pairs":len(valid_forms),"excluded_distinct_lemma_form_pairs":len(excluded_forms)+len(amb_rows),
"covered_occurrences":validated_occ,"total_verb_occurrences_040d":222535,"occurrence_coverage":validated_occ/222535,
"observed_non_aux_verb_occurrences":all_occ,
"coverage_family":statuses["VALIDATED_CANDIDATE"]/len(rows),"coverage_forms":len(valid_forms)/len(wanted),
"tests":{},"verification":"AUTOMATIC_CROSS_RESOURCE_CANDIDATE_NOT_HUMAN_VERIFIED",
"limitations":["Morphalou form/lemma membership is type-level, not contextual disambiguation","Ambiguous 040D forms excluded from confirmed forms","Simple conservative -er/-ir/-re stem rule excludes irregular or unclear roots","040D strict whole-token occurrence counts only"]}
assert all_occ<=222535 and sum(int(r["occurrences_couvertes"]) for r in rows)==validated_occ
assert not ({a for a,b in valid_forms}&aux)
assert valid_forms.issubset(confirmed)
assert all(form.startswith(stem(lemma)) for lemma,form in valid_forms)
for term in ("aimer","chanter","garder","parler"):
    candidate=next((r for r in rows if r["infinitif"]==term),None)
    report["tests"][term]={"in_040d":candidate is not None,"in_morphalou":term in seen_lemmas,"validated_forms":candidate["nombre_formes"] if candidate else 0}
(out/"rapport-040e.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("REPORT_040E="+json.dumps(report,ensure_ascii=False),flush=True)
