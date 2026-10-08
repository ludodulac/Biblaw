#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"data/linguistic/sense-catalog.json"
def load(path):
    with Path(path).open(encoding="utf-8") as h: value=json.load(h)
    if not isinstance(value,dict): raise AssertionError(f"{path}: top-level JSON must be object")
    return value
def norm(value): return unicodedata.normalize("NFC",value).casefold()
def repo_path(path):
    p=Path(path)
    try: return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError: raise AssertionError("review must be inside repository")
def build(review_path,review_mission,confirmation_mission):
    review_path=Path(review_path); review=load(review_path)
    if review.get("reviewType")!="SUPERVISION_REVIEW": raise AssertionError("REVIEW_TYPE_NOT_SUPERVISION_REVIEW")
    if review.get("validationStatus")!="USER_CONFIRMED": raise AssertionError("REVIEW_NOT_USER_CONFIRMED")
    source_queue=review.get("sourceQueue")
    if not isinstance(source_queue,str) or not source_queue: raise AssertionError("MISSING_SOURCE_QUEUE")
    queue=load(ROOT/source_queue); qentries=queue.get("entries")
    decisions=review.get("entries")
    if not isinstance(qentries,list) or not isinstance(decisions,list) or not decisions: raise AssertionError("INVALID_REVIEW_OR_QUEUE_ENTRIES")
    qids=[e.get("occurrenceId") for e in qentries]; dids=[e.get("occurrenceId") for e in decisions]
    if len(qids)!=len(set(qids)) or len(dids)!=len(set(dids)): raise AssertionError("DUPLICATE_OCCURRENCE_ID")
    if set(qids)!=set(dids): raise AssertionError("REVIEW_QUEUE_COVERAGE_MISMATCH")
    qmap={e["occurrenceId"]:e for e in qentries}
    tuples={(norm(qmap[oid]["surfaceForm"]),qmap[oid]["lemma"],qmap[oid]["partOfSpeech"]) for oid in dids}
    if len(tuples)!=1: raise AssertionError("MIXED_REVIEW_TARGETS")
    normalized_form,lemma,pos=next(iter(tuples))
    catalog=load(CATALOG); targets=[e for e in catalog.get("entries",[]) if e.get("lemma")==lemma and e.get("partOfSpeech")==pos]
    if len(targets)!=1: raise AssertionError("CATALOG_TARGET_NOT_UNIQUE")
    sense_ids=[s.get("senseId") for s in targets[0].get("senses",[])]
    if not sense_ids or len(sense_ids)!=len(set(sense_ids)): raise AssertionError("INVALID_CATALOG_SENSES")
    rows=[]; counts=Counter({sid:0 for sid in sense_ids})
    for d in decisions:
        oid=d["occurrenceId"]; selected=d.get("selectedSenseId"); available={s.get("senseId") for s in qmap[oid].get("availableSenses",[])}
        if selected not in available or selected not in sense_ids: raise AssertionError(f"INVALID_SELECTED_SENSE:{oid}")
        rows.append({"occurrenceId":oid,"adjudicationStatus":"VALIDATED","senseId":selected}); counts[selected]+=1
    rows.sort(key=lambda e:e["occurrenceId"]); counts["UNCERTAIN"]=0
    return {"schemaVersion":1,"purpose":"human-validated-occurrence-sense-gold","target":{"normalizedForm":normalized_form,"lemma":lemma,"partOfSpeech":pos},"provenance":{"validationType":"user-confirmed","reviewMission":review_mission,"confirmationMission":confirmation_mission,"sourceReview":repo_path(review_path),"status":"VALIDATED"},"entries":rows,"counts":dict(counts)}
def render(gold): return (json.dumps(gold,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def main():
    p=argparse.ArgumentParser();p.add_argument("--review",required=True,type=Path);p.add_argument("--output",required=True,type=Path);p.add_argument("--review-mission",required=True);p.add_argument("--confirmation-mission",required=True);a=p.parse_args()
    data=render(build(a.review,a.review_mission,a.confirmation_mission));a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(data)
    print(f"PASS target={build(a.review,a.review_mission,a.confirmation_mission)['target']['normalizedForm']} entries={len(build(a.review,a.review_mission,a.confirmation_mission)['entries'])}")
if __name__=="__main__": main()
