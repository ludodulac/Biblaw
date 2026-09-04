#!/usr/bin/env python3
"""Validate documentary extraction of canonical books 11-20.

Validation logic remains single-sourced in validate_books_01_10.py; this wrapper
changes only the scope and output report.
"""
from pathlib import Path

BASE = Path(__file__).with_name("validate_books_01_10.py")
source = BASE.read_text(encoding="utf-8")
source = source.replace(
    'OUT = ROOT / "data/pilot/books-01-10-validation-report.json"',
    'OUT = ROOT / "data/pilot/books-11-20-validation-report.json"',
)
source = source.replace(
    'for book_no in range(1,11):',
    'for book_no in range(11,21):',
)
source = source.replace(
    '"scope":"books-01-10"',
    '"scope":"books-11-20"',
)
required = [
    'books-11-20-validation-report.json',
    'range(11,21)',
    '"scope":"books-11-20"',
]
missing = [token for token in required if token not in source]
if missing:
    raise RuntimeError(f"Unable to adapt base validator; missing replacements: {missing}")
exec(compile(source, str(BASE), "exec"), {"__name__": "__main__", "__file__": str(BASE)})
