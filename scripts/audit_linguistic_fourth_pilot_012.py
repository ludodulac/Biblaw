#!/usr/bin/env python3
import json,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("adj",R/"scripts/build_linguistic_adjudication.py"); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cfg=json.loads((R/"data/linguistic/pilots/compte-config.json").read_text(encoding="utf-8"))
gold=json.loads((R/"data/linguistic/gold/compte-gold.json").read_text(encoding="utf-8"))
raw,adj,inv=m.build(cfg); by={x["occurrenceId"]:x for x in adj["analyses"]}; ro={x["occurrenceId"]:x for x in raw["occurrences"]}
assert raw["occurrenceCount"]==222
assert len({x["occurrenceId"] for x in raw["occurrences"]})==222
contr=[]; correct=[]; unknown=[]; ambiguous=[]
for g in gold["entries"]:
 a=by[g["occurrenceId"]]
 if a["category"]==g["category"]: correct.append(g["occurrenceId"])
 elif a["status"]=="UNKNOWN": unknown.append(g["occurrenceId"])
 elif a["status"]=="AMBIGUOUS": ambiguous.append(g["occurrenceId"])
 else: contr.append({"id":g["occurrenceId"],"expected":g["category"],"actual":a["category"],"context":ro[g["occurrenceId"]]["context"]})
assert not contr, contr
classified=[{"id":a["occurrenceId"],"category":a["category"],"evidence":a["evidence"],"context":ro[a["occurrenceId"]]["context"]} for a in adj["analyses"] if a["status"]=="PROVISIONAL" and a["category"]!="OTHER"]
print(json.dumps({"raw":raw["occurrenceCount"],"segmentation":adj["segmentationCounts"],"counts":adj["counts"],"gold":{"correct":len(correct),"unknown":len(unknown),"ambiguous":len(ambiguous),"contradictory":len(contr)},"classified":classified},ensure_ascii=False))
