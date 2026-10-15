#!/usr/bin/env python3
"""040D: position-based diagnostic and conservative canonical occurrence alignment."""
import csv,json,re,sys
from collections import Counter,defaultdict
from pathlib import Path
import spacy
from build_linguistic_occurrence_index import ROOT,CATALOG,TOKEN_RE,norm,fields,oid

OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("040d-output")
OUT.mkdir(parents=True,exist_ok=True)
nlp=spacy.load("fr_core_news_sm",disable=["ner"])
catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
psalms=[p for p in catalog["records"] if re.fullmatch(r"data/corpus/books/book-\d+/psalm-\d+\.json",p)]
assert len(psalms)==1158, f"Unexpected canonical psalms {len(psalms)}"
sources=[]
for rel in psalms:
    record=json.loads((ROOT/rel).read_text(encoding="utf-8"))
    assert record["recordType"]=="psalm"
    for field,verse,text in fields(record):
        sources.append((record["id"],field,verse,text))
print("PSALMS",len(psalms),"FIELDS",len(sources),flush=True)

verbs=defaultdict(Counter); analyses=defaultdict(Counter); unknown=Counter()
causes=Counter(); examples=defaultdict(list); aligned_before=aligned_after=unaligned_before=unaligned_after=0
verb_occurrences=0; canonical_total=0; analyzed_total=0; mapped_ids=set(); recovered_ids=set()
for (rid,field,verse,text),doc in zip(sources,nlp.pipe((s[-1] for s in sources),batch_size=24,n_process=1)):
    canonical=[(m.start(),m.end(),norm(m.group()),oid(rid,field,verse,m.start(),m.end())) for m in TOKEN_RE.finditer(text)]
    canonical_total+=len(canonical)
    by_span={(a,b):(key,identifier) for a,b,key,identifier in canonical}
    # A canonical token can contain multiple spaCy tokens, e.g. l'aime -> l' + aime.
    # Such partial matches count as aligned for diagnostic purposes but NEVER as
    # a verified verbal attribution to a canonical occurrence.
    for tok in doc:
        if tok.is_space or tok.is_punct: continue
        key=norm(tok.text)
        if not key or not any(ch.isalpha() for ch in key): continue
        analyzed_total+=1
        a,b=tok.idx,tok.idx+len(tok.text)
        if text[a:b]!=tok.text: raise AssertionError("spaCy offsets differ from source")
        exact=by_span.get((a,b))
        if exact and exact[0]==key:
            aligned_before+=1;aligned_after+=1
            kind="EXACT"
            target=(a,b,exact[0],exact[1])
        else:
            unaligned_before+=1
            covering=[item for item in canonical if item[0]<=a and b<=item[1]]
            if len(covering)==1:
                target=covering[0];aligned_after+=1
                kind="CONTAINED_DIFFERENT_TOKENIZATION"
            else:
                target=None;unaligned_after+=1
                if any(item[0]<b and a<item[1] for item in canonical):
                    kind="CROSS_BOUNDARY"
                elif any(ch in tok.text for ch in ("-","‐","‑","–","—")):
                    kind="HYPHEN_OR_COMPOUND"
                elif any(ch in tok.text for ch in ("'","’")):
                    kind="APOSTROPHE_OR_ELISION"
                else:
                    kind="NO_CANONICAL_TOKEN"
        if kind!="EXACT":
            causes[kind]+=1
            if len(examples[kind])<12:
                examples[kind].append({"recordId":rid,"field":field,"verse":verse,"token":tok.text,"start":a,"end":b,"source":text[max(0,a-35):min(len(text),b+35)],"canonicalToken":text[target[0]:target[1]] if target else None})
        lemma=norm(tok.lemma_)
        if kind=="EXACT":
            identifier=target[3]
            assert identifier==oid(rid,field,verse,a,b)
            assert identifier not in mapped_ids, "Duplicate canonical occurrence"
            mapped_ids.add(identifier)
            if tok.pos_ in ("VERB","AUX") and lemma and lemma!="-pron-":
                verbs[lemma][key]+=1;verb_occurrences+=1
                analyses[key][(lemma,tok.pos_)]+=1
            elif tok.pos_ in ("X","") or not lemma:
                unknown[key]+=1
            else:
                analyses[key][(lemma,tok.pos_)]+=1
        elif target is not None:
            # Do not assign partial spaCy tokens to a whole canonical occurrence.
            # Retain observed POS as a diagnostic only.
            if tok.pos_ in ("VERB","AUX"):
                recovered_ids.add(target[3])
        elif tok.pos_ in ("VERB","AUX"):
            unknown[key]+=1
assert analyzed_total==aligned_before+unaligned_before
assert analyzed_total==aligned_after+unaligned_after
ambiguous={form for form,groups in analyses.items() if any(p in ("VERB","AUX") for _,p in groups)
           and (len({lemma for lemma,_ in groups})>1 or any(p not in ("VERB","AUX") for _,p in groups))}
aux={"être","avoir"}
rows=[]
for lemma,forms in verbs.items():
    amb=sorted(set(forms)&ambiguous)
    rows.append({"infinitif":lemma,"formes_observees":"; ".join(f"{k} ({v})" for k,v in sorted(forms.items(),key=lambda x:(-x[1],x[0]))),
                 "nombre_total_occurrences":sum(forms.values()),"nombre_formes_differentes":len(forms),
                 "statut_verification":"AUXILIARY_SEPARATE" if lemma in aux else ("AUTOMATIC_AMBIGUOUS" if amb else "AUTOMATIC_PROVISIONAL"),
                 "ambiguites":"; ".join(amb)})
rows.sort(key=lambda x:(-x["nombre_total_occurrences"],x["infinitif"]))
def csvout(name,header,items):
    with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f);w.writerow(header);w.writerows(items)
csvout("verbes-corpus-040d.csv",["infinitif","formes_observees","nombre_total_occurrences","nombre_formes_differentes","statut_verification","ambiguites"],([r[k] for k in ("infinitif","formes_observees","nombre_total_occurrences","nombre_formes_differentes","statut_verification","ambiguites")] for r in rows))
csvout("formes-ambigues-040d.csv",["forme","analyses_automatiques","occurrences_analysees"],((form,"; ".join(f"{lemma}/{pos} ({n})" for (lemma,pos),n in sorted(analyses[form].items())),sum(analyses[form].values())) for form in sorted(ambiguous)))
csvout("formes-non-reconnues-040d.csv",["forme","occurrences_non_reconnues"],sorted(unknown.items(),key=lambda x:(-x[1],x[0])))
diagnostic={"source":"canonical psalm text and spaCy original character offsets","categories":{"A":"CONTAINED_DIFFERENT_TOKENIZATION: spaCy token wholly within one canonical token, not safely attributable to whole occurrence","B":"CROSS_BOUNDARY: spaCy token overlaps but crosses canonical boundary","C":"NO_CANONICAL_TOKEN/HYPHEN_OR_COMPOUND/APOSTROPHE_OR_ELISION: no complete canonical token containment"},"causes":dict(causes),"examples":dict(examples),"potential_partial_verb_occurrence_ids":len(recovered_ids),"policy":"Partial alignment is diagnostic only; no approximate verb attribution or occurrence IDs."}
(OUT/"diagnostic-alignement-040d.json").write_text(json.dumps(diagnostic,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
summary={"mission":"BIBLAW-OCCV2-040D","psalms":len(psalms),"fields":len(sources),"total_canonical_tokens":canonical_total,"total_analyzed_tokens":analyzed_total,
"aligned_tokens_before":aligned_before,"unaligned_tokens_before":unaligned_before,
"aligned_tokens_after":aligned_after,"unaligned_tokens_after":unaligned_after,
"alignment_coverage":aligned_after/analyzed_total if analyzed_total else 0,
"strict_canonical_coverage":aligned_before/analyzed_total if analyzed_total else 0,
"total_verbs_excluding_auxiliaries":sum(r["infinitif"] not in aux for r in rows),
"total_distinct_verb_forms":len({form for forms in verbs.values() for form in forms}),
"total_verb_occurrences":verb_occurrences,"ambiguous_distinct_forms":len(ambiguous),
"unknown_distinct_forms":len(unknown),"auxiliaries":{x:sum(verbs[x].values()) for x in sorted(aux)},
"verification":"AUTOMATIC_PROVISIONAL_NOT_HUMAN_VERIFIED",
"interpretation":"Improved technical token alignment; conservative whole-occurrence verb attribution unchanged from 040C.",
"limitations":["Partial token matches are not safe canonical verbal assignments","spaCy morphological and POS classifications not human verified","Technical coverage is not linguistic accuracy","Unknown forms only reflect model X/empty and unmatched verbal tokens"]}
assert sum(r["nombre_total_occurrences"] for r in rows)==verb_occurrences
assert aligned_before==len(mapped_ids)
(OUT/"rapport-040d.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SUMMARY_040D="+json.dumps(summary,ensure_ascii=False),flush=True)
print("ALIGNMENT_CAUSES="+json.dumps(causes,ensure_ascii=False),flush=True)
