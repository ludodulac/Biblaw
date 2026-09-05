#!/usr/bin/env python3
"""Extract canonical books 21-30 by reusing the proven books 1-10 extractor.

The extraction logic remains single-sourced in extract_books_01_10.py. This wrapper
changes only the requested range/report and derives each Archangel's next expected
Psalm number from already extracted books 1-20.
"""
from pathlib import Path

BASE = Path(__file__).with_name("extract_books_01_10.py")
source = BASE.read_text(encoding="utf-8")
source = source.replace(
    'REPORT = ROOT / "data/pilot/books-01-10-extraction-report.json"',
    'REPORT = ROOT / "data/pilot/books-21-30-extraction-report.json"',
)
source = source.replace(
    'selected = [b for b in inventory["books"] if 1 <= b["bookNumber"] <= 10]',
    'selected = [b for b in inventory["books"] if 21 <= b["bookNumber"] <= 30]',
)
source = source.replace(
    'next_expected = {"michael": 1, "gabriel": 1, "raphael": 1, "ouriel": 1}',
    '''next_expected = {"michael": 1, "gabriel": 1, "raphael": 1, "ouriel": 1}\nfor prior_no in range(1, 21):\n    prior_dir = ROOT / "data/corpus/books" / f"book-{prior_no:02d}"\n    if not prior_dir.exists():\n        continue\n    for prior_path in prior_dir.glob("psalm-*.json"):\n        prior = json.loads(prior_path.read_text(encoding="utf-8"))\n        slug = prior.get("archangel")\n        number = prior.get("number")\n        if slug in next_expected and isinstance(number, int):\n            next_expected[slug] = max(next_expected[slug], number + 1)''',
)
source = source.replace(
    '"scope": "books-01-10"',
    '"scope": "books-21-30"',
)
source = source.replace(
    'print(f"Extracted {len(report)} books with first-verse recovery")',
    'print(f"Extracted {len(report)} books 21-30 with first-verse recovery")',
)

required = [
    'books-21-30-extraction-report.json',
    '21 <= b["bookNumber"] <= 30',
    'for prior_no in range(1, 21)',
    '"scope": "books-21-30"',
]
missing = [token for token in required if token not in source]
if missing:
    raise RuntimeError(f"Unable to adapt base extractor; missing replacements: {missing}")

exec(compile(source, str(BASE), "exec"), {"__name__": "__main__", "__file__": str(BASE)})
