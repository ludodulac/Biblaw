#!/usr/bin/env python3
"""Audit runtime provenance, canonical occurrence references and byte reproducibility."""
import json
from pathlib import Path
from build_linguistic_grammar_browser_runtime import ROOT, DEFAULT, build, read
from audit_linguistic_grammar_review import audit as review_audit

def audit():
    review_audit()
    runtime=read(DEFAULT)
    assert runtime==build()
    assert runtime["v"]==1 and runtime["purpose"]=="linguistic-grammar-browser-runtime"
    for form in runtime["forms"]:
        review_path=next(p for p in sorted((ROOT/"data/linguistic/review").glob("*-grammar-review-*.json")) if read(p)["normalizedForm"]==form["normalizedForm"])
        inventory=read(ROOT/read(review_path)["sourceOccurrences"])
        rows={x["occurrenceId"]:x for x in inventory["occurrences"]}
        used=set()
        for analysis in form["analyses"]:
            ids=analysis["occurrenceIds"]
            assert len(ids)==len(set(ids)) and not (used & set(ids))
            used.update(ids)
            assert len(ids)==analysis["occurrenceCount"]
            expected={}
            for oid in ids:
                row=rows[oid]
                expected.setdefault(row["recordId"],[]).append(row)
            records=[[record_id,len(items),sorted({int(x["verseNumber"]) for x in items if x["verseNumber"] is not None})] for record_id,items in sorted(expected.items())]
            assert records==analysis["records"]
        if form["normalizedForm"]=="garde":
            counts={(a["lemma"],a["partOfSpeech"]):a["occurrenceCount"] for a in form["analyses"]}
            assert counts=={("garde","NOUN"):22,("garder","VERB"):70}
            assert len(used)==92 and len(rows)==99
            assert not (used & {x["occurrenceId"] for x in read(ROOT/read(review_path)["sourcePilot"])["analyses"] if x["segmentation"]=="COMPOUND_ELEMENT"})
    print("GRAMMAR_RUNTIME_AUDIT=PASS")
if __name__=="__main__":
    audit()
