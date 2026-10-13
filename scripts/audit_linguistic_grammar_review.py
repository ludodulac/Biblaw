#!/usr/bin/env python3
"""Verify that grammatical supervision decisions apply only to prior UNKNOWNs."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def audit():
    for path in sorted((ROOT/"data/linguistic/review").glob("*-grammar-review-*.json")):
        review=read(path)
        pilot=read(ROOT/review["sourcePilot"])
        inventory=read(ROOT/review["sourceOccurrences"])
        unknown={x["occurrenceId"] for x in pilot["analyses"] if x["category"]=="UNKNOWN"}
        inventory_ids={x["occurrenceId"] for x in inventory["occurrences"]}
        decisions=review["decisions"]
        ids=[x["occurrenceId"] for x in decisions]
        assert len(ids)==len(set(ids)) and set(ids)<=unknown&inventory_ids
        assert review["provenance"]["reviewType"]=="SUPERVISION_REVIEW"
        assert review["provenance"]["validationStatus"]=="SUPERVISION_CONFIRMED"
        assert all(x["sourcePilotCategory"]=="UNKNOWN" for x in decisions)
        assert all(x["selectedPartOfSpeech"] in ("NOUN","VERB") for x in decisions)
        assert all((x["selectedLemma"],x["selectedPartOfSpeech"],x["selectedCategory"]) in
                   [("garde","NOUN","NOUN_GARDE"),("garder","VERB","VERB_GARDER")] for x in decisions) if review["normalizedForm"]=="garde" else True
        if review["normalizedForm"]=="garde":
            assert len(decisions)==23 and len(unknown)==23
            assert sum(x["selectedPartOfSpeech"]=="NOUN" for x in decisions)==3
            assert sum(x["selectedPartOfSpeech"]=="VERB" for x in decisions)==20
    print("GRAMMAR_REVIEW_AUDIT=PASS")
if __name__=="__main__":
    audit()
