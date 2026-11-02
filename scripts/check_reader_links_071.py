#!/usr/bin/env python3
"""071: inspect existing prayer IDs/reciprocal references, not source PDFs or editorial content."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
bundle=json.loads((ROOT/"data/browser-search-catalog.json").read_text(encoding="utf-8"))
rows=bundle["records"]; by_id={r["id"]:r for r in rows}
psalms=[r for r in rows if r.get("recordType")=="psalm"]
prayers=[r for r in rows if r.get("recordType")=="master-prayer"]
notes=[r for r in rows if r.get("recordType")=="note"]
assert len(rows)==len(by_id)==1846, "Browser bundle has missing/duplicate records"
assert (len(psalms),len(prayers),len(notes))==(1158,677,11)
catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"))
catalog_prayers=[p for p in catalog["records"] if p.startswith("data/prayers/")]
assert len(catalog_prayers)==len(prayers), "The browser build omitted a catalogued prayer"
assert {json.loads((ROOT/p).read_text(encoding="utf-8"))["id"] for p in catalog_prayers}=={p["id"] for p in prayers}, "Prayer catalog and browser IDs differ"

by_psalm=defaultdict(list)
missing_targets=[];not_reciprocal=[]
for p in prayers:
    target=p.get("appliesToPsalmId")
    by_psalm[target].append(p["id"])
    ps=by_id.get(target)
    if not ps or ps.get("recordType")!="psalm":missing_targets.append((p["id"],target))
    elif p["id"] not in ps.get("prayerIds",[]):not_reciprocal.append((p["id"],target))
multi_source={id:ids for id,ids in by_psalm.items() if len(ids)>1}
multi_reciprocal={id:[pid for pid in ids if pid in by_id[id].get("prayerIds",[])] for id,ids in multi_source.items() if id in by_id}
multi_reciprocal={id:ids for id,ids in multi_reciprocal.items() if len(ids)>1}
broken_forward=[(ps["id"],pid) for ps in psalms for pid in ps.get("prayerIds",[])
                if pid not in by_id or by_id[pid].get("recordType")!="master-prayer" or by_id[pid].get("appliesToPsalmId")!=ps["id"]]
counts=Counter(len(ps.get("prayerIds",[])) for ps in psalms)
out={"counts":{"psalms":len(psalms),"prayers":len(prayers),"notes":len(notes),"cataloguedPrayerFiles":len(catalog_prayers)},
     "psalmPrayerIdsDistribution":dict(sorted(counts.items())),
     "multiplePrayerSourceTargets":multi_source,
     "multiplePrayerReciprocalTargets":multi_reciprocal,
     "prayersWithMissingPsalmTarget":missing_targets,
     "prayersWithoutReciprocalPsalmLink":not_reciprocal,
     "psalmBackLinksWithMissingOrWrongPrayer":broken_forward,
     "noteStatuses":dict(Counter(n.get("validation",{}).get("status","unknown") for n in notes))}
print("BIBLAW-071 PRAYER-LINK ANALYSIS "+json.dumps(out,ensure_ascii=False))
