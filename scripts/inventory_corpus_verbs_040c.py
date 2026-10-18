#!/usr/bin/env python3
"""040C: corpus-wide exploratory verb inventory; automatic, not human verification."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import spacy
from build_linguistic_occurrence_index import ROOT, CATALOG, TOKEN_RE, norm, fields

OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("040c-output")
OUT.mkdir(parents=True,exist_ok=True)
nlp=spacy.load("fr_core_news_sm",disable=["ner"])
catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
psalms=[p for p in catalog["records"] if re.fullmatch(r"data/corpus/books/book-\d+/psalm-\d+\.json",p)]
assert psalms, "No canonical psalms"
sources=[]
for rel in psalms:
    record=json.loads((ROOT/rel).read_text(encoding="utf-8"))
    assert record["recordType"]=="psalm"
    for field,verse,text in fields(record):
        sources.append((rel,record["id"],field,verse,text))
print("PSALMS",len(psalms),"FIELDS",len(sources),flush=True)
# Analyze real texts, preserve original corpus tokens for independent membership checks.
documents=nlp.pipe((row[-1] for row in sources),batch_size=24,n_process=1)
verb_counts=defaultdict(Counter)
surface_analyses=defaultdict(Counter)
unrecognized=Counter()
total_corpus_tokens=0
verb_occurrences=0
mismatches=0
examples=defaultdict(list)
for row,doc in zip(sources,documents):
    rel,rid,field,verse,text=row
    canonical=[(norm(m.group()),m.start(),m.end()) for m in TOKEN_RE.finditer(text)]
    total_corpus_tokens+=len(canonical)
    for tok in doc:
        if tok.is_space or tok.is_punct: continue
        key=norm(tok.text)
        if not key or not any(ch.isalpha() for ch in key): continue
        # Compare model token boundaries to canonical source text, never invent forms.
        start,end=tok.idx,tok.idx+len(tok.text)
        matches=[x for x in canonical if x[1]==start and x[2]==end and x[0]==key]
        if not matches:
            mismatches+=1
            continue
        lemma=norm(tok.lemma_)
        if tok.pos_ in ("VERB","AUX") and lemma and lemma!="-pron-":
            verb_counts[lemma][key]+=1
            surface_analyses[key][(lemma,tok.pos_)]+=1
            verb_occurrences+=1
            if len(examples[(lemma,key)])<2:
                examples[(lemma,key)].append({"recordId":rid,"verse":verse,"field":field,"offset":start})
        elif tok.pos_ in ("X","") or not lemma:
            unrecognized[key]+=1
        else:
            surface_analyses[key][(lemma,tok.pos_)]+=1
# Any form classified across different lemmas or verb/nonverb in context is flagged.
ambiguous_forms={form for form,analyses in surface_analyses.items()
                 if any(pos in ("VERB","AUX") for _,pos in analyses)
                 and (len({lemma for lemma,_ in analyses})>1
                      or any(pos not in ("VERB","AUX") for _,pos in analyses))}
auxiliary_lemmas={"être","avoir"}
rows=[]
for lemma,forms in verb_counts.items():
    ambiguity=sorted(form for form in forms if form in ambiguous_forms)
    status="AUXILIARY_SEPARATE" if lemma in auxiliary_lemmas else ("AUTOMATIC_AMBIGUOUS" if ambiguity else "AUTOMATIC_PROVISIONAL")
    rows.append({"infinitif":lemma,"formes_observees":"; ".join(f"{form} ({count})" for form,count in sorted(forms.items(),key=lambda x:(-x[1],x[0]))),
                 "nombre_total_occurrences":sum(forms.values()),"nombre_formes_differentes":len(forms),
                 "statut_verification":status,"ambiguites":"; ".join(ambiguity)})
rows.sort(key=lambda r:(-r["nombre_total_occurrences"],r["infinitif"]))
with (OUT/"verbes-corpus-040c.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["infinitif","formes_observees","nombre_total_occurrences","nombre_formes_differentes","statut_verification","ambiguites"])
    w.writeheader();w.writerows(rows)
with (OUT/"formes-ambigues-040c.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f);w.writerow(["forme","analyses_automatiques","occurrences_analysees"])
    for form in sorted(ambiguous_forms):
        analyses=surface_analyses[form]
        w.writerow([form,"; ".join(f"{lemma}/{pos} ({count})" for (lemma,pos),count in sorted(analyses.items())),sum(analyses.values())])
with (OUT/"formes-non-reconnues-040c.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f);w.writerow(["forme","occurrences_non_reconnues"]);w.writerows(sorted(unrecognized.items(),key=lambda x:(-x[1],x[0])))
summary={"mission":"BIBLAW-OCCV2-040C","source":"data/catalog.json, canonical book psalms only","method":"spaCy fr_core_news_sm POS and lemma; original canonical token boundaries cross-checked","verification":"AUTOMATIC_PROVISIONAL_NOT_HUMAN_VERIFIED","psalms":len(psalms),"fields":len(sources),"corpus_tokens":total_corpus_tokens,
"total_verbs_including_auxiliaries":len(rows),"total_verbs_excluding_auxiliaries":sum(r["infinitif"] not in auxiliary_lemmas for r in rows),
"total_distinct_verb_forms":len({form for forms in verb_counts.values() for form in forms}),
"total_verb_occurrences":verb_occurrences,"ambiguous_distinct_forms":len(ambiguous_forms),
"unknown_distinct_forms":len(unrecognized),"unknown_occurrences":sum(unrecognized.values()),
"token_boundary_mismatches":mismatches,
"auxiliaries":{lemma:sum(verb_counts[lemma].values()) for lemma in sorted(auxiliary_lemmas)},
"limitations":["Single automatic French NLP model, no independent human audit","POS/lemma model predictions may be wrong or miss verbs","Ambiguity is observed model disagreement, not a complete dictionary of possible lemmas","Unrecognized only means model X/empty or missing lemma, not all potential missed verbs","Infinitive labels are model lemmas; not independently dictionary-validated","Some spaCy tokenization differs from canonical index; unmatched tokens are excluded"]}
assert sum(r["nombre_total_occurrences"] for r in rows)==verb_occurrences
assert all(r["nombre_total_occurrences"]==sum(int(x.rsplit(" (",1)[1][:-1]) for x in r["formes_observees"].split("; ")) for r in rows)
(OUT/"rapport-040c.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SUMMARY_040C="+json.dumps(summary,ensure_ascii=False),flush=True)
print("TOP_VERBS="+json.dumps(rows[:20],ensure_ascii=False),flush=True)
