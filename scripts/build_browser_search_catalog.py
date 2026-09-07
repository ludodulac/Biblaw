#!/usr/bin/env python3
"""Bundle browser-searchable corpus records into one deterministic JSON payload.

Avoids making more than a thousand individual HTTP requests from GitHub Pages.
No semantic transformation is performed.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data'/'catalog.json'
OUT=ROOT/'data'/'browser-search-catalog.json'

def main():
    catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
    records=[]
    missing=[]
    for rel in catalog.get('records',[]):
        path=ROOT/rel
        if not path.exists():
            missing.append(rel); continue
        obj=json.loads(path.read_text(encoding='utf-8'))
        if obj.get('recordType') in {'theme','book'}: continue
        records.append(obj)
    if missing:
        raise SystemExit(f'Missing catalog records: {missing[:10]}')
    payload={'schemaVersion':1,'purpose':'browser-search-corpus-bundle','recordCount':len(records),'records':records}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(f'Browser search catalog: {len(records)} records -> {OUT.relative_to(ROOT)}')
if __name__=='__main__': main()
