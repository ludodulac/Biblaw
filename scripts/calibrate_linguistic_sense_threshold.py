#!/usr/bin/env python3
import json
from collections import Counter
from evaluate_linguistic_sense_classifier import ROOT,K,sources,feats,train,pred,policy
O=ROOT/"data/linguistic/audits/sense-threshold-calibration-024.json"
TARGET=.95
def inner_fold(record_id,outer_fold):
 import hashlib
 return int(hashlib.sha256(("inner:"+str(outer_fold)+":"+record_id).encode()).hexdigest()[:8],16)%K
def main():
 rows,_goldids,targets,_allowed=sources(); classes=sorted({r[2] for r in rows}); folds=[]; accepted=[]
 for outer in range(K):
  outer_test=[r for r in rows if __import__("evaluate_linguistic_sense_classifier").fold(r[1]["recordId"])==outer]
  outer_train=[r for r in rows if __import__("evaluate_linguistic_sense_classifier").fold(r[1]["recordId"])!=outer]
  inner_oof=[]
  for inner in range(K):
   te=[r for r in outer_train if inner_fold(r[1]["recordId"],outer)==inner]
   tr=[r for r in outer_train if inner_fold(r[1]["recordId"],outer)!=inner]
   if not te: continue
   if set(r[2] for r in tr)!=set(classes): raise SystemExit(f"outer {outer} inner {inner}: missing training class")
   model=train(tr,classes,targets)
   for key,o,y in te:
    p,score=pred(model,classes,feats(o["context"],targets[key]["forms"])); inner_oof.append((y,p,score))
  if len(inner_oof)!=len(outer_train): raise SystemExit(f"outer {outer}: incomplete inner OOF")
  pol=policy(inner_oof); threshold=pol["threshold"]; model=train(outer_train,classes,targets); selected=[]
  for key,o,y in outer_test:
   p,score=pred(model,classes,feats(o["context"],targets[key]["forms"]))
   if threshold is not None and score>=threshold: selected.append((y,p))
  correct=sum(y==p for y,p in selected); count=len(selected)
  folds.append({"outerFold":outer,"outerTestCount":len(outer_test),"innerOofCount":len(inner_oof),"threshold":threshold,"innerSelectedCount":pol["oofCount"],"innerSelectedPrecision":pol["oofPrecision"],"autoAcceptCount":count,"correctCount":correct,"incorrectCount":count-correct,"precision":correct/count if count else None})
  accepted.extend(selected)
 total=len(accepted); correct=sum(y==p for y,p in accepted); per={}
 for c in classes:
  xs=[(y,p) for y,p in accepted if p==c]; cc=sum(y==p for y,p in xs)
  per[c]={"autoAcceptCount":len(xs),"correctCount":cc,"incorrectCount":len(xs)-cc,"precision":cc/len(xs) if xs else None}
 precision=correct/total if total else None; aggregate={"outerTestExampleCount":len(rows),"autoAcceptCount":total,"correctCount":correct,"incorrectCount":total-correct,"precision":precision,"coverage":total/len(rows)}
 report={"schemaVersion":1,"purpose":"independent-sense-threshold-calibration","method":"5-fold deterministic outer CV grouped by recordId; threshold selected only by deterministic 5-fold inner CV grouped by recordId within each outer-train partition","validatedCount":len(rows),"outerFoldCount":K,"targetPrecision":TARGET,"folds":folds,"aggregate":aggregate,"perSenseId":per,"decision":"CALIBRATION_PASS" if total>=20 and precision is not None and precision>=TARGET else "CALIBRATION_FAIL"}
 O.parent.mkdir(parents=True,exist_ok=True);O.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
 print(json.dumps(report,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
