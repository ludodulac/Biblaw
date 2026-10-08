#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from build_linguistic_occurrence_index import ROOT,occurrences,norm
DEFAULT_PROPOSALS=ROOT/"data/linguistic/audits/sense-classifier-023a.json"
DEFAULT_CALIBRATION=ROOT/"data/linguistic/audits/sense-threshold-per-sense-025.json"
DEFAULT_OUTPUT=ROOT/"data/linguistic/review/sense-review-queue-026.json"
CAT=ROOT/"data/linguistic/sense-catalog.json";FORM=ROOT/"data/linguistic-semantic-form-runtime.json"
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def validate_sources(proposals,calibration):
 if proposals.get("schemaVersion")!=1 or proposals.get("purpose")!="automatic-sense-classifier-evaluation" or not isinstance(proposals.get("unseenProposals"),list): raise SystemExit("INVALID_PROPOSALS_CONTRACT")
 if calibration.get("schemaVersion")!=1 or calibration.get("purpose")!="independent-per-sense-threshold-calibration" or not isinstance(calibration.get("perSenseId"),dict): raise SystemExit("INVALID_CALIBRATION_CONTRACT")
def form_target_map(runtime):
 out={}
 for t in runtime["targets"]:
  key=(t["lemma"],t["partOfSpeech"])
  for f in t["forms"]: out.setdefault(norm(f),set()).add(key)
 return out
def resolve_target(surface,form_targets):
 keys=form_targets.get(norm(surface),set())
 if not keys: raise SystemExit("UNRESOLVED_PROPOSAL_TARGET")
 if len(keys)!=1: raise SystemExit("AMBIGUOUS_PROPOSAL_TARGET")
 return next(iter(keys))
def build(proposals_path,calibration_path):
 proposals=load(proposals_path);calibration=load(calibration_path);validate_sources(proposals,calibration)
 cat=load(CAT);runtime=load(FORM);catalog={(e["lemma"],e["partOfSpeech"]):e for e in cat["entries"]};targets=form_target_map(runtime)
 rows=proposals["unseenProposals"]; ids=[p.get("occurrenceId") for p in rows]
 if len(ids)!=len(set(ids)): raise SystemExit("DUPLICATE_PROPOSAL_OCCURRENCE_ID")
 entries=[];eligible=0
 for p in sorted(rows,key=lambda x:x["occurrenceId"]):
  for field in ("occurrenceId","surfaceForm","proposedSenseId","score"):
   if field not in p: raise SystemExit("INVALID_PROPOSAL_ENTRY")
  key=resolve_target(p["surfaceForm"],targets)
  if key not in catalog: raise SystemExit("PROPOSAL_TARGET_MISSING_FROM_CATALOG")
  matches=[o for o in occurrences(p["surfaceForm"]) if o["occurrenceId"]==p["occurrenceId"]]
  if len(matches)!=1: raise SystemExit("PROPOSAL_OCCURRENCE_NOT_UNIQUE_IN_CANONICAL_CORPUS")
  o=matches[0];senses=catalog[key]["senses"];byid={s["senseId"]:s for s in senses};sid=p["proposedSenseId"]
  if sid not in byid: raise SystemExit("PROPOSED_SENSE_MISSING_FROM_CATALOG")
  cal=calibration["perSenseId"].get(sid)
  if not isinstance(cal,dict) or "decision" not in cal or "candidateThreshold" not in cal: raise SystemExit("MISSING_CALIBRATION_FOR_PROPOSED_SENSE")
  threshold=cal["candidateThreshold"]
  if cal["decision"]=="CERTIFIED_AUTO_ACCEPT" and threshold is not None and p["score"]>=threshold: eligible+=1;continue
  entries.append({"occurrenceId":p["occurrenceId"],"recordId":o["recordId"],"surfaceForm":p["surfaceForm"],"lemma":key[0],"partOfSpeech":key[1],"proposedSenseId":sid,"proposedSenseLabel":byid[sid]["label"],"score":p["score"],"context":o["context"],"availableSenses":[{"senseId":s["senseId"],"label":s["label"]} for s in senses]})
 return {"schemaVersion":1,"purpose":"linguistic-sense-human-review-queue","generator":"scripts/build_linguistic_sense_review_queue.py","reviewCount":len(entries),"autoAcceptEligibleCount":eligible,"entries":entries}
def render(report): return json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
def main():
 p=argparse.ArgumentParser();p.add_argument("--proposals",type=Path,default=DEFAULT_PROPOSALS);p.add_argument("--calibration",type=Path,default=DEFAULT_CALIBRATION);p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT);a=p.parse_args()
 report=build(a.proposals,a.calibration);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(render(report),encoding="utf-8")
 print(json.dumps({"reviewCount":report["reviewCount"],"autoAcceptEligibleCount":report["autoAcceptEligibleCount"],"surfaceForms":sorted({e["surfaceForm"] for e in report["entries"]}),"targets":sorted({e["lemma"]+"/"+e["partOfSpeech"] for e in report["entries"]})},ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
