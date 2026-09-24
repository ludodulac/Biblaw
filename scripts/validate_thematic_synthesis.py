#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def refs_in_synthesis(x):
    out=[]
    def walk(v):
        if isinstance(v,dict):
            if "evidenceRefs" in v: out.extend(v["evidenceRefs"])
            for z in v.values(): walk(z)
        elif isinstance(v,list):
            for z in v: walk(z)
    walk(x); return out
def validate():
    s=load(ROOT/"data/experiments/thematic-synthesis/mort.json")
    a=load(ROOT/"data/experiments/adjudicated-thematic-axes/mort.json")
    assert s["theme"]["themeId"]=="mort"
    assert len(s["mainAxes"])==3
    subs=[z for x in s["mainAxes"] for z in x.get("subaxes",[])]
    assert len(subs)==2 and len(s["distinctions"])==1
    axis_ids={x["id"] for x in a["elements"] if x["kind"] in {"axis","subaxis"}}
    assert {x["axisId"] for x in s["mainAxes"]}|{x["axisId"] for x in subs} == axis_ids
    allowed=set(sum((x["evidenceRefs"] for x in a["elements"]+a["distinctions"]),[]))
    used=set(refs_in_synthesis(s))
    assert used <= allowed, f"new evidenceRefs: {used-allowed}"
    assert len(s["essentialPsalms"])<=8 and all(x["recordId"] in allowed for x in s["essentialPsalms"])
    assert len(s["relatedThemes"])<=8
    assert sum(len(x.get("subaxes",[])) for x in s["mainAxes"])==2
    assert all(x.get("evidenceRefs") for x in s["mainAxes"]+subs+s["distinctions"])
    print(f"PASS axes=3 subaxes=2 distinctions=1 evidenceRefs={len(used)} essentials={len(s['essentialPsalms'])} related={len(s['relatedThemes'])}")
if __name__=="__main__": validate()
