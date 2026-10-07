#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DEC=ROOT/"data/linguistic/review/sense-review-decisions-027.json"
def main():
 d=json.loads(DEC.read_text(encoding="utf-8")); assert d["schemaVersion"]==1; assert d["purpose"]=="linguistic-sense-supervision-review-decisions"; assert d["reviewType"]=="SUPERVISION_REVIEW"; assert d["validationStatus"]=="USER_CONFIRMED"; assert "human-audited" not in json.dumps(d,ensure_ascii=False).casefold()
 source=d["sourceQueue"]; q=json.loads((ROOT/source).read_text(encoding="utf-8")); qe={e["occurrenceId"]:e for e in q["entries"]}; ids=[e["occurrenceId"] for e in d["entries"]]; assert len(ids)==len(set(ids)); assert set(ids)==set(qe)
 agreement=0
 for e in d["entries"]:
  src=qe[e["occurrenceId"]]; assert e["selectedSenseId"] in {s["senseId"] for s in src["availableSenses"]}; assert e["queueProposedSenseId"]==src["proposedSenseId"]; expected=e["selectedSenseId"]==e["queueProposedSenseId"]; assert e["modelAgreement"] is expected; agreement+=int(expected)
 assert d["counts"]=={"reviewed":len(ids),"modelAgreement":agreement,"modelCorrection":len(ids)-agreement}
 print("PASS reviewed=%d modelAgreement=%d modelCorrection=%d"%(len(ids),agreement,len(ids)-agreement))
if __name__=="__main__": main()
