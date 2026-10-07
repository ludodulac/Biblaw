#!/usr/bin/env python3
import json
from pathlib import Path
from build_linguistic_occurrence_index import ROOT,occurrences,norm
P23=ROOT/"data/linguistic/audits/sense-classifier-023a.json"
P25=ROOT/"data/linguistic/audits/sense-threshold-per-sense-025.json"
CAT=ROOT/"data/linguistic/sense-catalog.json"
FORM=ROOT/"data/linguistic-semantic-form-runtime.json"
OUT=ROOT/"data/linguistic/review/sense-review-queue-026.json"
def main():
 p23=json.loads(P23.read_text()); p25=json.loads(P25.read_text()); cat=json.loads(CAT.read_text()); runtime=json.loads(FORM.read_text())
 catalog={(e["lemma"],e["partOfSpeech"]):e for e in cat["entries"]}
 form_targets={}
 for t in runtime["targets"]:
  for f in t["forms"]: form_targets.setdefault(norm(f),[]).append((t["lemma"],t["partOfSpeech"]))
 occ_by_id={}
 for proposal in p23["unseenProposals"]:
  for key in form_targets.get(norm(proposal["surfaceForm"]),[]):
   for o in occurrences(proposal["surfaceForm"]):
    if o["occurrenceId"]==proposal["occurrenceId"]: occ_by_id[o["occurrenceId"]]=(key,o)
 entries=[]; eligible=0
 for p in sorted(p23["unseenProposals"],key=lambda x:x["occurrenceId"]):
  resolved=occ_by_id.get(p["occurrenceId"])
  if not resolved: raise SystemExit("proposal occurrence not found in canonical corpus/runtime")
  key,o=resolved
  if key not in catalog: raise SystemExit("target missing from sense catalog")
  senses=catalog[key]["senses"]; byid={s["senseId"]:s for s in senses}; sid=p["proposedSenseId"]
  if sid not in byid: raise SystemExit("proposed sense missing from catalog")
  calibration=p25["perSenseId"].get(sid,{})
  certified=calibration.get("decision")=="CERTIFIED_AUTO_ACCEPT"; threshold=calibration.get("candidateThreshold")
  if certified and threshold is not None and p["score"]>=threshold:
   eligible+=1; continue
  entries.append({"occurrenceId":p["occurrenceId"],"recordId":o["recordId"],"surfaceForm":p["surfaceForm"],"lemma":key[0],"partOfSpeech":key[1],"proposedSenseId":sid,"proposedSenseLabel":byid[sid]["label"],"score":p["score"],"context":o["context"],"availableSenses":[{"senseId":s["senseId"],"label":s["label"]} for s in senses]})
 report={"schemaVersion":1,"purpose":"linguistic-sense-human-review-queue","generator":"scripts/build_linguistic_sense_review_queue.py","reviewCount":len(entries),"autoAcceptEligibleCount":eligible,"entries":entries}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"reviewCount":len(entries),"autoAcceptEligibleCount":eligible,"surfaceForms":sorted({e["surfaceForm"] for e in entries}),"targets":sorted({e["lemma"]+"/"+e["partOfSpeech"] for e in entries})},ensure_ascii=False,sort_keys=True))
if __name__=="__main__": main()
