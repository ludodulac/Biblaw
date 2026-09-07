#!/usr/bin/env python3
"""Guard the browser-side indexes that avoid rebuilding/scanning stable corpus structures."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'js' / 'biblaw.js').read_text(encoding='utf-8')

required = (
    'recordById: new Map()',
    'psalmsByNumber: new Map()',
    'normalizedFragmentsById: new Map()',
    'state.recordById = new Map(state.records.map(r => [r.id, r]))',
    'state.psalmsByNumber = new Map()',
    'state.normalizedFragmentsById = new Map()',
    'state.normalizedFragmentsById.set(r.id,textFragments(r).map(norm).filter(Boolean))',
    'state.psalmsByNumber.get(number)||[]',
    'state.recordById.get(o.recordId)',
    'state.recordById.get(id)',
    'const allowed = selectedTypes(), a = $(\'archangelFilter\').value, needle=norm(query)',
    'literalTextMatch(r, needle)',
)
for needle in required:
    assert needle in JS, f'missing prebuilt browser index contract: {needle}'

for forbidden in (
    "Number(r.number)===number",
    "state.records.find(x=>x.id===id)",
    "byId=new Map(state.records.filter(r=>r.recordType==='psalm')",
    "textFragments(r).some(fragment => literalIncludes(fragment, query))",
):
    assert forbidden not in JS, f'costly per-query scan/rebuild returned: {forbidden}'

print('Browser search indexes OK: IDs, Psalm numbers and normalized text are prebuilt once at load')
