#!/usr/bin/env python3
import json
from build_linguistic_occurrence_index import ROOT
Q=ROOT/"data/linguistic/review/sense-review-queue-026.json"; P23=ROOT/"data/linguistic/audits/sense-classifier-023a.json"; P25=ROOT/"data/linguistic/audits/sense-threshold-per-sense-025.json"; CAT=ROOT/"data/linguistic/sense-catalog.json"; GOLD=ROOT/"data/linguistic/gold"
def main():
 q=json.loads(Q.read_text()); p23=json.loads(P23.read_text()); p25=json.loads(P25.read_text()); cat=json.loads(CAT.read_text())
 assert q["schemaVersion"]==1 and q["purpose"]=="linguistic-sense-human-review-queue"
 ids=[e["occurrenceId"] for e in q["entries"]]; assert len(ids)==len(set(ids))==q["reviewCount"]; assert ids==sorted(ids)
 proposals={p["occurrenceId"]:p for p in p23["unseenProposals"]}; assert set(ids)<=set(proposals)
 goldids=set()
 for p in sorted(GOLD.glob("*-sense-gold.json")):
  x=json.loads(p.read_text()); goldids.update(e.get("occurrenceId") for e in x.get("entries",[]))
 assert not (set(ids)&goldids)
 catalogs={(e["lemma"],e["partOfSpeech"]):{s["senseId"]:s["label"] for s in e["senses"]} for e in cat["entries"]}
 for e in q["entries"]:
  senses=catalogs[(e["lemma"],e["partOfSpeech"])]; assert e["context"].strip(); assert e["proposedSenseId"] in senses; assert e["proposedSenseLabel"]==senses[e["proposedSenseId"]]
  assert e["availableSenses"]==[{"senseId":sid,"label":label} for sid,label in senses.items()]
  p=proposals[e["occurrenceId"]]; assert e["surfaceForm"]==p["surfaceForm"] and e["score"]==p["score"]
  cal=p25["perSenseId"].get(e["proposedSenseId"],{}); threshold=cal.get("candidateThreshold")
  assert not (cal.get("decision")=="CERTIFIED_AUTO_ACCEPT" and threshold is not None and e["score"]>=threshold)
 excluded=set(proposals)-set(ids)
 for oid in excluded:
  p=proposals[oid]; cal=p25["perSenseId"].get(p["proposedSenseId"],{}); threshold=cal.get("candidateThreshold")
  assert cal.get("decision")=="CERTIFIED_AUTO_ACCEPT" and threshold is not None and p["score"]>=threshold
 assert q["autoAcceptEligibleCount"]==len(excluded)
 print("PASS reviewCount=%d autoAcceptEligible=%d goldInReview=0"%(q["reviewCount"],len(excluded)))
if __name__=="__main__": main()
