#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from build_linguistic_occurrence_index import ROOT,occurrences,norm
from build_linguistic_sense_review_queue import DEFAULT_PROPOSALS,DEFAULT_CALIBRATION,DEFAULT_OUTPUT,CAT,FORM,load,validate_sources,form_target_map,resolve_target
GOLD=ROOT/"data/linguistic/gold"
def main():
 p=argparse.ArgumentParser();p.add_argument("--queue",type=Path,default=DEFAULT_OUTPUT);p.add_argument("--proposals",type=Path,default=DEFAULT_PROPOSALS);p.add_argument("--calibration",type=Path,default=DEFAULT_CALIBRATION);a=p.parse_args()
 q=load(a.queue);props=load(a.proposals);calib=load(a.calibration);validate_sources(props,calib)
 assert q.get("schemaVersion")==1 and q.get("purpose")=="linguistic-sense-human-review-queue" and q.get("generator")=="scripts/build_linguistic_sense_review_queue.py"
 ids=[e["occurrenceId"] for e in q["entries"]];assert len(ids)==len(set(ids))==q["reviewCount"];assert ids==sorted(ids)
 plist=props["unseenProposals"];pids=[x["occurrenceId"] for x in plist];assert len(pids)==len(set(pids));proposals={x["occurrenceId"]:x for x in plist};assert set(ids)<=set(proposals)
 goldids=set()
 for path in sorted(GOLD.glob("*-sense-gold.json")):
  x=load(path);source=x.get("provenance",{}).get("sourceReview");same_queue=False
  if source:
   review=load(ROOT/source);review_queue=review.get("sourceQueue")
   same_queue=bool(review_queue) and load(ROOT/review_queue)==q
  if not same_queue: goldids.update(e.get("occurrenceId") for e in x.get("entries",[]))
 assert not(set(ids)&goldids)
 cat=load(CAT);catalog={(e["lemma"],e["partOfSpeech"]):e for e in cat["entries"]};targets=form_target_map(load(FORM))
 for e in q["entries"]:
  p0=proposals[e["occurrenceId"]];key=resolve_target(p0["surfaceForm"],targets);assert key==(e["lemma"],e["partOfSpeech"]) and key in catalog
  matches=[o for o in occurrences(p0["surfaceForm"]) if o["occurrenceId"]==e["occurrenceId"]];assert len(matches)==1;assert e["recordId"]==matches[0]["recordId"] and e["context"]==matches[0]["context"] and e["context"].strip()
  senses=catalog[key]["senses"];byid={s["senseId"]:s["label"] for s in senses};assert e["proposedSenseId"]==p0["proposedSenseId"] in byid;assert e["proposedSenseLabel"]==byid[e["proposedSenseId"]]
  assert e["availableSenses"]==[{"senseId":s["senseId"],"label":s["label"]} for s in senses];assert e["surfaceForm"]==p0["surfaceForm"] and e["score"]==p0["score"]
  c=calib["perSenseId"].get(e["proposedSenseId"]);assert isinstance(c,dict) and "decision" in c and "candidateThreshold" in c;t=c["candidateThreshold"]
  assert not(c["decision"]=="CERTIFIED_AUTO_ACCEPT" and t is not None and e["score"]>=t)
 excluded=set(proposals)-set(ids)
 for oid in excluded:
  p0=proposals[oid];resolve_target(p0["surfaceForm"],targets);c=calib["perSenseId"].get(p0["proposedSenseId"]);assert isinstance(c,dict);t=c.get("candidateThreshold")
  assert c.get("decision")=="CERTIFIED_AUTO_ACCEPT" and t is not None and p0["score"]>=t
 assert q["autoAcceptEligibleCount"]==len(excluded)
 try: resolve_target("x",{"x":{("a","A"),("b","B")}})
 except SystemExit as e: assert str(e)=="AMBIGUOUS_PROPOSAL_TARGET"
 else: raise AssertionError("ambiguous target was not rejected")
 print("PASS reviewCount=%d autoAcceptEligible=%d goldInReview=0 ambiguousTargetRejected=1"%(q["reviewCount"],len(excluded)))
if __name__=="__main__":main()
