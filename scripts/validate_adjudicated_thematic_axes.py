#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONF={"FORT","MOYEN","FAIBLE"}; KINDS={"axis","subaxis","complement"}
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def public_theme_ids():
    data=load(ROOT/"data/thematic-index/theme-search-index.json")
    rows=data if isinstance(data,list) else data.get("themes",data.get("entries",[]))
    return {x["themeId"] for x in rows if isinstance(x,dict) and "themeId" in x}
def canonical_record(record_id,theme_id):
    m=re.fullmatch(r"book-(\d+)-psalm-(\d+)",record_id)
    assert m, f"invalid evidenceRef {record_id}"
    path=ROOT/f"data/thematic-index/books/book-{int(m.group(1)):02d}.json"
    assert path.exists(), f"missing sourceRef {path}"
    book=load(path)
    matches=[p for p in book.get("psalmAnalyses",[]) if p.get("recordId")==record_id]
    assert len(matches)==1, f"missing/incoherent recordId {record_id}"
    ps=matches[0]
    assert any(t.get("themeId")==theme_id for t in ps.get("themes",[])), f"evidence {record_id} lacks theme {theme_id}"
    return path,ps
def validate(data, expected_counts=None):
    assert data.get("contract")=="adjudicated-thematic-axes"
    theme_id=data.get("theme",{}).get("themeId")
    assert theme_id in public_theme_ids(), f"unknown public theme {theme_id}"
    elements=data.get("elements",[]); distinctions=data.get("distinctions",[])
    ids=[x.get("id") for x in elements+distinctions]
    assert None not in ids and len(ids)==len(set(ids)), "duplicate/missing id"
    by_id={x["id"]:x for x in elements}
    for e in elements:
        assert e.get("kind") in KINDS, f"unknown status {e.get('kind')}"
        assert e.get("confidence") in CONF, "invalid confidence"
        assert e.get("justification","").strip(), "missing bounded justification"
        refs=e.get("evidenceRefs",[]); assert refs, f"substantive element without evidence {e['id']}"
        parent=e.get("parentId")
        if e["kind"]=="axis": assert parent is None, "axis cannot have parent"
        if e["kind"]=="subaxis":
            assert parent in by_id, "orphan subaxis"
            assert by_id[parent]["kind"] in {"axis","subaxis"}, "invalid subaxis parent"
        if e["kind"]=="complement" and parent is not None:
            assert parent in by_id and by_id[parent]["kind"] in {"axis","subaxis"}, "invalid complement parent"
        for r in refs: canonical_record(r,theme_id)
    for d in distinctions:
        assert d.get("kind")=="distinction"
        assert d.get("confidence") in CONF
        assert d.get("justification","").strip()
        assert d.get("evidenceRefs"), "distinction without evidence"
        sides=d.get("sides",[]); assert len(sides)>=2 and all(s.get("id") for s in sides), "distinction without sides"
        for s in sides:
            for rid in s.get("relatedElementIds",[]): assert rid in by_id and by_id[rid]["kind"] in {"axis","subaxis"}
        for r in d["evidenceRefs"]: canonical_record(r,theme_id)
    if expected_counts:
        assert sum(e["kind"]=="axis" for e in elements)==expected_counts["axes"]
        assert sum(e["kind"]=="subaxis" for e in elements)==expected_counts["subaxes"]
        assert len(distinctions)==expected_counts["distinctions"]
    return True
if __name__=="__main__":
    p=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"data/experiments/adjudicated-thematic-axes/mort.json"
    validate(load(p),{"axes":3,"subaxes":2,"distinctions":1} if p.name=="mort.json" else None)
    print("PASS")
