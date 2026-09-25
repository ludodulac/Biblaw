#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('g',R/'scripts/build_linguistic_adjudication.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for stem in ('porte','suis'):
 cfg=json.loads((R/f'data/linguistic/pilots/{stem}-config.json').read_text())
 rr,aa,ii=g.build(cfg);old=json.loads((R/f'data/linguistic/pilots/{stem}.json').read_text())
 diffs=[]
 ob={x['occurrenceId']:x for x in old['analyses']}
 for x in aa['analyses']:
  if x!=ob[x['occurrenceId']]:diffs.append({'new':x,'old':ob[x['occurrenceId']]})
 print(json.dumps({'stem':stem,'newCounts':aa['counts'],'oldCounts':old['counts'],'newSeg':aa['segmentationCounts'],'oldSeg':old['segmentationCounts'],'diffCount':len(diffs),'diffs':diffs[:30]},ensure_ascii=False))
