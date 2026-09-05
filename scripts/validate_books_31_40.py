#!/usr/bin/env python3
"""Validate documentary extraction of canonical books 31-40."""
from pathlib import Path
BASE=Path(__file__).with_name('validate_books_01_10.py')
source=BASE.read_text(encoding='utf-8')
source=source.replace('OUT = ROOT / "data/pilot/books-01-10-validation-report.json"','OUT = ROOT / "data/pilot/books-31-40-validation-report.json"')
source=source.replace('for book_no in range(1,11):','for book_no in range(31,41):')
source=source.replace('"scope":"books-01-10"','"scope":"books-31-40"')
required=['books-31-40-validation-report.json','range(31,41)','"scope":"books-31-40"']
missing=[x for x in required if x not in source]
if missing: raise RuntimeError(f'Unable to adapt base validator; missing replacements: {missing}')
exec(compile(source,str(BASE),'exec'),{'__name__':'__main__','__file__':str(BASE)})
