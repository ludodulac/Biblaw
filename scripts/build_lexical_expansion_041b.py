#!/usr/bin/env python3
"""041B product runtime from canonical psalm vocabulary and SHA-pinned Morphalou."""
import argparse,csv,io,json,re,zipfile
from collections import defaultdict,Counter
from pathlib import Path
from build_lexical_expansion_runtime import MORPHALOU_SHA256,MORPHALOU_MEMBER,sha256_file,browser_key,morph_norm
from build_linguistic_occurrence_index import ROOT,CATALOG,TOKEN_RE,fields
def generate(morph):
    if sha256_file(morph)!=MORPHALOU_SHA256:raise ValueError("Morphalou checksum mismatch")
    catalog=json.loads(CATALOG.read_text(encoding="utf8"))
    psalms=[x for x in catalog["records"] if re.fullmatch(r"data/corpus/books/book-\d+/psalm-\d+\.json",x)]
    assert len(psalms)==1158
    freq=Counter()
    for path in psalms:
        obj=json.loads((ROOT/path).read_text(encoding="utf8"))
        for _,_,text in fields(obj):
            freq.update(browser_key(m.group()) for m in TOKEN_RE.finditer(text))
    vocab={k for k in freq if k and " " not in k}
    # Independent dictionary memberships; do not use spaCy POS per occurrence.
    membership=defaultdict(set);category_by_pair=defaultdict(set)
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
                if category!="Verbe" and not category.startswith("Nom"):continue
                key=browser_key(lemma)
                if not key or " " in key or (category=="Verbe" and key in ("etre","avoir")):continue
                form=row[9]
                candidates=[form] if form else []
                if category=="Verbe":candidates.append(lemma)
                for raw_form in candidates:
                    fkey=browser_key(raw_form)
                    if fkey not in vocab:continue
                    if category=="Verbe":
                        # Conservative initial stem: never prefix-only membership.
                        if not key.endswith(("er","ir","re")) or len(key)<=5:continue
                        if not fkey.startswith(key[:-2]):continue
                    elif category=="Nom":
                        # Require independent dictionary confirmation of each form.
                        if not (fkey==key or fkey.startswith(key)):continue
                    membership[fkey].add(("Verbe" if category=="Verbe" else "Nom",key))
                    category_by_pair[(category,key)].add(fkey)
    # No form can anchor competing morphological families, even across POS.
    unique={}
    for form,groups in membership.items():
        verbs={g for g in groups if g[0]=="Verbe"}
        nouns={g for g in groups if g[0]=="Nom"}
        # Prefer a unique verb-family analysis over a noun homograph:
        # search remains textual and never claims token-level grammatical certainty.
        # Multiple verb lemmas remain excluded rather than arbitrarily combined.
        if len(verbs)==1:unique[form]=next(iter(verbs))
        elif not verbs and len(nouns)==1:unique[form]=next(iter(nouns))
    grouped=defaultdict(list)
    for form,group in unique.items():grouped[group].append(form)
    groups=[sorted(set(forms)) for _,forms in sorted(grouped.items()) if len(set(forms))>=2]
    groups.sort(key=lambda g:g[0])
    seen=[form for g in groups for form in g]
    assert len(seen)==len(set(seen))
    assert not any(form in ("etre","avoir") for g in groups for form in g)
    return {"v":1,"m":MORPHALOU_SHA256,"g":groups},freq,membership
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--morphalou",required=True);a.add_argument("--output",required=True);a.add_argument("--report",required=True);args=a.parse_args()
    runtime,freq,membership=generate(Path(args.morphalou))
    Path(args.output).write_text(json.dumps(runtime,ensure_ascii=False,separators=(",",":"),sort_keys=True)+"\n",encoding="utf8")
    lookup={form:g for g in runtime["g"] for form in g}
    report={"source":"Morphalou 3.1","sha256":MORPHALOU_SHA256,"psalms":1158,"groups":len(runtime["g"]),"anchors":len(lookup),"cases":{}}
    for term in ("pain","pains","maison","maisons","aimer","chanter","garder","parler"):
        forms=lookup.get(term,[])
        report["cases"][term]={"canonical_token_frequency":freq[term],"additional_forms":[x for x in forms if x!=term],"group_size":len(forms),"has_option":len(forms)>1}
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("REPORT_041B="+json.dumps(report,ensure_ascii=False),flush=True)
