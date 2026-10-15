#!/usr/bin/env python3
"""039H: blind lexical overlap evaluation of BIEN; Gold read only after predictions."""
import collections, hashlib, json, pathlib, re, sys
from experiment_039f_wiktionary import request,extract,toks
from build_linguistic_occurrence_index import ROOT,occurrences
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=True)
catalog=json.loads((ROOT/"data/linguistic/sense-catalog.json").read_text())
senses=catalog["entries"][0]["senses"]
status,data,error=request({"action":"query","prop":"revisions","rvprop":"content","rvslots":"main","format":"json","titles":"bien","formatversion":2})
if error: raise SystemExit("WIKTIONARY_HTTP_ERROR "+error)
page=data["query"]["pages"][0]; raw=page.get("revisions",[{}])[0].get("slots",{}).get("main",{}).get("content","")
m=re.search(r"^==\s*\{\{langue\|fr\}\}\s*==",raw,re.M)
if not m:raise SystemExit("NO_FRENCH_SECTION")
tail=raw[m.end():];end=re.search(r"^==[^=]",tail,re.M);raw=tail[:end.start()] if end else tail
defs=[d for d in extract(raw) if d["pos_heading"] in ("nom","nom commun","substantif")]
(OUT/"definitions.json").write_text(json.dumps({"source":"https://fr.wiktionary.org/wiki/bien","status":"EXPERIMENTAL","definitions":defs},ensure_ascii=False,indent=2))
# Mapping uses ONLY independently authored canonical sense definitions, never Gold.
mapping=[]
for i,d in enumerate(defs):
 scores={s["senseId"]:len(toks(d["definition"]) & toks(s["definition"]+" "+s["label"])) for s in senses}
 top=max(scores.values());w=[k for k,v in scores.items() if v==top]
 mapping.append({"definition_index":i,"candidate_scores":scores,"mapped_sense":w[0] if top>0 and len(w)==1 else None,"status":"HEURISTIC_UNVERIFIED"})
(OUT/"mapping.json").write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
eligible=[(d,m["mapped_sense"]) for d,m in zip(defs,mapping) if m["mapped_sense"]]
# No mapping is asserted reliable: results are exploratory, not valid accuracy.
forms=["bien","biens"]; byid={}
for form in forms:
 for o in occurrences(form):byid[o["occurrenceId"]]=o
gold=[]
for form in forms:
 p=ROOT/f"data/linguistic/gold/{form}-noun-sense-gold.json"
 if p.exists():gold+=json.loads(p.read_text())["entries"]
gold=[g for g in gold if g.get("adjudicationStatus")=="VALIDATED" and g["occurrenceId"] in byid]
gold=sorted(gold,key=lambda g:g["occurrenceId"])
def baseline(context):
 scores=[len(toks(context)&toks(d["definition"])) for d,_ in eligible]
 if not scores:return None,scores
 v=max(scores);w=[i for i,x in enumerate(scores) if x==v]
 return (eligible[w[0]][1] if v>0 and len(w)==1 else None),scores
def improved(context):
 # Generic IDF over definition collection: downweight common definition words.
 terms=[toks(d["definition"]) for d,_ in eligible]; df=collections.Counter(x for ts in terms for x in ts)
 ct=toks(context);scores=[sum(1/df[t] for t in ct&ts) for ts in terms]
 if not scores:return None,scores
 v=max(scores);w=[i for i,x in enumerate(scores) if x==v]
 return (eligible[w[0]][1] if v>0 and len(w)==1 else None),scores
predictions=[]
for g in gold:
 o=byid[g["occurrenceId"]]; b,bs=baseline(o["context"]);p,ps=improved(o["context"])
 predictions.append({"occurrenceId":g["occurrenceId"],"context":o["context"],"baseline":b,"baseline_scores":bs,"improved":p,"improved_scores":ps,"status":"EXPERIMENTAL"})
(OUT/"predictions-blind.json").write_text(json.dumps(predictions,ensure_ascii=False,indent=2))
# Gold loaded only for scoring below, never used in mapping, scores or threshold.
truth={g["occurrenceId"]:g["senseId"] for g in gold}
metrics={}
for key in ("baseline","improved"):
 accepted=[p for p in predictions if p[key] is not None];correct=sum(p[key]==truth[p["occurrenceId"]] for p in accepted)
 matrix={s["senseId"]:{z:0 for z in [*[x["senseId"] for x in senses],"ABSTAIN"]} for s in senses}
 for p in predictions:matrix[truth[p["occurrenceId"]]][p[key] or "ABSTAIN"]+=1
 metrics[key]={"evaluated":len(predictions),"proposals":len(accepted),"abstentions":len(predictions)-len(accepted),"correct":correct,"coverage":len(accepted)/len(predictions) if predictions else None,"retained_precision":correct/len(accepted) if accepted else None,"accuracy_all":correct/len(predictions) if predictions else None,"confusion_matrix":matrix}
reliable=False # lexical mapping cannot be independently validated without external sense alignment
report={"http_status":status,"definitions_noun":len(defs),"mapped_heuristically":len(eligible),"mapping_reliability":"UNVERIFIED","evaluation_status":"EVALUATION_BLOCKED","reason":"Definition-to-canonical-sense alignment is heuristic and unverified independently; scores are diagnostics, not certified semantic accuracy.","metrics_exploratory_only":metrics,"gold_count":len(gold),"source":"Wiktionary CC BY-SA 4.0; attribution required"}
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
