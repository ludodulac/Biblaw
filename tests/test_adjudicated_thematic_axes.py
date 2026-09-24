#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"scripts"))
from validate_adjudicated_thematic_axes import load,validate
P=ROOT/"data/experiments/adjudicated-thematic-axes/mort.json"; d=load(P)
assert validate(d,{"axes":3,"subaxes":2,"distinctions":1})
assert validate(copy.deepcopy(d),{"axes":3,"subaxes":2,"distinctions":1})
els=d["elements"]; assert sum(e["kind"]=="axis" for e in els)==3; assert sum(e["kind"]=="subaxis" for e in els)==2; assert len(d["distinctions"])==1
ids=[x["id"] for x in els+d["distinctions"]]; assert len(ids)==len(set(ids))
assert all(e["evidenceRefs"] for e in els) and all(x["evidenceRefs"] for x in d["distinctions"])
# Generic shape probes: no semantic adjudication, only schema capability.
g=copy.deepcopy(d); g["elements"]=[e for e in g["elements"] if e["kind"]!="subaxis"]; g["distinctions"]=[]; assert validate(g)
g=copy.deepcopy(d); g["distinctions"]=g["distinctions"]*2; g["distinctions"][1]=copy.deepcopy(g["distinctions"][1]); g["distinctions"][1]["id"]="DISTINCTION_02"; assert validate(g)
assert any(e["kind"]=="complement" and e["parentId"] for e in els); assert any(e["kind"]=="complement" and e["parentId"] is None for e in els)
# Validator rejection probes.
for mutate in ("duplicate","badparent","badconfidence","noproof","nosides","badrecord","badtheme"):
    x=copy.deepcopy(d)
    if mutate=="duplicate": x["elements"][1]["id"]=x["elements"][0]["id"]
    elif mutate=="badparent": x["elements"][2]["parentId"]="NOPE"
    elif mutate=="badconfidence": x["elements"][0]["confidence"]="CERTAIN"
    elif mutate=="noproof": x["elements"][0]["evidenceRefs"]=[]
    elif mutate=="nosides": x["distinctions"][0]["sides"]=[]
    elif mutate=="badrecord": x["elements"][0]["evidenceRefs"]=["book-99-psalm-999"]
    elif mutate=="badtheme": x["theme"]["themeId"]="theme-does-not-exist"
    try: validate(x)
    except AssertionError: pass
    else: raise AssertionError(f"validator accepted {mutate}")
print("PASS: artifact, determinism, counts, parents, records, provenance, unique IDs, evidence, generic-shape probes, rejection probes")
