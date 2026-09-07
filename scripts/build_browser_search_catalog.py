#!/usr/bin/env python3
"""Bundle browser-searchable corpus records into one deterministic JSON payload.

Avoids making more than a thousand individual HTTP requests from GitHub Pages.
Canonical Psalms live under data/corpus/books/. Older archangel-scoped Psalm files
remain in the repository for historical/documentary purposes but must not be
published as duplicate search records.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'catalog.json'
OUT = ROOT / 'data' / 'browser-search-catalog.json'
CANONICAL_PSALM_PREFIX = 'data/corpus/books/'


def main():
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    records = []
    missing = []
    legacy_psalms_skipped = []

    for rel in catalog.get('records', []):
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        obj = json.loads(path.read_text(encoding='utf-8'))
        record_type = obj.get('recordType')
        if record_type in {'theme', 'book'}:
            continue
        if record_type == 'psalm' and not rel.startswith(CANONICAL_PSALM_PREFIX):
            legacy_psalms_skipped.append(rel)
            continue
        records.append(obj)

    if missing:
        raise SystemExit(f'Missing catalog records: {missing[:10]}')

    missing_ids = [index for index, record in enumerate(records) if not str(record.get('id', '')).strip()]
    if missing_ids:
        raise SystemExit(f'Browser records without id at positions: {missing_ids[:10]}')

    id_counts = Counter(record['id'] for record in records)
    duplicate_ids = sorted(record_id for record_id, count in id_counts.items() if count > 1)
    if duplicate_ids:
        raise SystemExit(f'Duplicate record ids in browser bundle: {duplicate_ids[:10]}')

    psalms = [record for record in records if record.get('recordType') == 'psalm']
    payload = {
        'schemaVersion': 1,
        'purpose': 'browser-search-corpus-bundle',
        'recordCount': len(records),
        'records': records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(
        f'Browser search catalog: {len(records)} unique-id records, {len(psalms)} canonical psalms, '
        f'{len(legacy_psalms_skipped)} legacy psalms skipped -> {OUT.relative_to(ROOT)}'
    )


if __name__ == '__main__':
    main()
