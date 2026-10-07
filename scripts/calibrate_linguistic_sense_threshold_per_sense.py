#!/usr/bin/env python3
import json
from evaluate_linguistic_sense_classifier import ROOT,K,sources,feats,train,pred,fold
from calibrate_linguistic_sense_threshold import inner_fold
O=ROOT/"data/linguistic/audits/sense-threshold-per-sense-025.json"
TARGET=.95
def choose(xs):
 best=None
 for t in sorted({score for y,p,score in xs},reverse=True):
  a=[x for x in xs if x[2]>=t]; precision=sum(y==p for y,p,_ in a)/len(a)
  if precision>=TARGET:
   candidate=(len(a),-t,precision,t)
   if best is None or candidate>best: best=candidate
 return {"threshold":None,"selectedCount":0,"precision":None} if best is None else {"threshold":best[3],"selectedCount":best[0],"precision":best[2]}
def thresholds(oof,classes):
 return {c:choose([x for x in oof if x[1]==c]) for c in classes}
def grouped_oof(rows,classes,targets,splitter):
 out=[]
 for k in range(K):
  te=[r for r in rows if splitter(r[1]["recordId"])==k]; tr=[r for r in rows if splitter(r[1]["recordId"])!=k]
  if not te: continue
  if {r[1]["recordId"] for r in te}&{r[1]["recordId"] for r in tr}: raise SystemExit("record group leak")
  if set(r[2] for r in tr)!=set(classes): raise SystemExit("missing training class")
  model=train(tr,classes,targets)
  for key,o,y in te:
   p,score=pred(model,classes,feats(o["context"],targets[key]["forms"])); out.append((y,p,score))
 return out
def main():
 rows,_goldids,targets,_allowed=sources(); classes=sorted({r[2] for r in rows}); folds=[]; outer_predictions=[]
 for outer in range(K):
  outer_test=[r for r in rows if fold(r[1]["recordId"])==outer]; outer_train=[r for r in rows if fold(r[1]["recordId"])!=outer]
  test_groups={r[1]["recordId"] for r in outer_test}; train_groups={r[1]["recordId"] for r in outer_train}
  if test_groups&train_groups: raise SystemExit(f"outer {outer}: record group leak")
  inner=grouped_oof(outer_train,classes,targets,lambda rid,o=outer:inner_fold(rid,o))
  if len(inner)!=len(outer_train): raise SystemExit(f"outer {outer}: incomplete inner OOF")
  ps=thresholds(inner,classes); model=train(outer_train,classes,targets); per={c:{"predictedCount":0,"autoAcceptCount":0,"correctCount":0,"incorrectCount":0} for c in classes}
  for key,o,y in outer_test:
   p,score=pred(model,classes,feats(o["context"],targets[key]["forms"])); per[p]["predictedCount"]+=1; accepted=ps[p]["threshold"] is not None and score>=ps[p]["threshold"]
   outer_predictions.append((y,p,score,accepted))
   if accepted:
    per[p]["autoAcceptCount"]+=1; per[p]["correctCount"]+=int(y==p); per[p]["incorrectCount"]+=int(y!=p)
  folds.append({"outerFold":outer,"outerTestCount":len(outer_test),"thresholds":ps,"perSenseId":per})
 full_oof=grouped_oof(rows,classes,targets,fold); final_candidates=thresholds(full_oof,classes); summary={}
 for c in classes:
  predicted=sum(p==c for y,p,s,a in outer_predictions); selected=[x for x in outer_predictions if x[1]==c and x[3]]; correct=sum(y==p for y,p,s,a in selected); n=len(selected); precision=correct/n if n else None
  summary[c]={"predictedCount":predicted,"autoAcceptCount":n,"correctCount":correct,"incorrectCount":n-correct,"independentPrecision":precision,"coverageAmongPredictions":n/predicted if predicted else 0,"decision":"CERTIFIED_AUTO_ACCEPT" if n>=20 and precision is not None and precision>=TARGET else "REVIEW_ONLY","candidateThreshold":final_candidates[c]["threshold"]}
 certified=[v for v in summary.values() if v["decision"]=="CERTIFIED_AUTO_ACCEPT"]; decision="PER_SENSE_CALIBRATION_PASS" if certified and all(v["independentPrecision"]>=TARGET for v in certified) else "PER_SENSE_CALIBRATION_FAIL"
 report={"schemaVersion":1,"purpose":"independent-per-sense-threshold-calibration","validatedCount":len(rows),"targetPrecision":TARGET,"outerFoldCount":K,"method":"5-fold deterministic nested CV grouped by recordId; per-sense thresholds selected only from inner OOF predictions grouped by predicted senseId","antiLeak":{"outerTestUsedForThresholdSelection":False,"recordGroupLeak":False},"folds":folds,"perSenseId":summary,"decision":decision}
 O.parent.mkdir(parents=True,exist_ok=True); O.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); print(json.dumps(report,ensure_ascii=False,sort_keys=True))
if __name__=="__main__": main()
