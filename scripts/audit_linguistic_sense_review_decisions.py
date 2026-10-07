#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEC=ROOT/"data/linguistic/review/sense-review-decisions-027.json"
def main():
 d=json.loads(DEC.read_text(encoding="utf-8"))
 assert d["schemaVersion"]==1
 assert d["purpose"]=="linguistic-sense-supervision-review-decisions"
 assert d["reviewType"]=="SUPERVISION_REVIEW"
 assert d["validationStatus"]=="PROPOSED_FOR_USER_CONFIRMATION"
 assert "human-audited" not in json.dumps(d,ensure_ascii=False).casefold()
 assert "validated" not in d["validationStatus"].casefold()
 source=d["sourceQueue"]; assert source=="data/linguistic/review/sense-review-queue-026.json"
 q=json.loads((ROOT/source).read_text(encoding="utf-8"))
 qe={e["occurrenceId"]:e for e in q["entries"]}; de=d["entries"]; ids=[e["occurrenceId"] for e in de]
 assert len(ids)==len(set(ids))
 assert set(ids)==set(qe) and len(ids)==len(qe)
 agreement=0
 for e in de:
  src=qe[e["occurrenceId"]]; available={s["senseId"] for s in src["availableSenses"]}
  assert e["selectedSenseId"] in available
  assert e["queueProposedSenseId"]==src["proposedSenseId"]
  expected=e["selectedSenseId"]==e["queueProposedSenseId"]; assert e["modelAgreement"] is expected
  agreement+=int(expected)
 expected_counts={"reviewed":len(de),"modelAgreement":agreement,"modelCorrection":len(de)-agreement}
 assert d["counts"]==expected_counts
 print("PASS reviewed=%d modelAgreement=%d modelCorrection=%d"%(len(de),agreement,len(de)-agreement))
if __name__=="__main__": main()
