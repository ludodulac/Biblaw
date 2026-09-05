#!/usr/bin/env python3
"""Extract canonical books 41-44 by reusing the proven books 1-10 extractor."""
from pathlib import Path
BASE=Path(__file__).with_name('extract_books_01_10.py')
source=BASE.read_text(encoding='utf-8')
source=source.replace('REPORT = ROOT / "data/pilot/books-01-10-extraction-report.json"','REPORT = ROOT / "data/pilot/books-41-44-extraction-report.json"')
source=source.replace('selected = [b for b in inventory["books"] if 1 <= b["bookNumber"] <= 10]','selected = [b for b in inventory["books"] if 41 <= b["bookNumber"] <= 44]')
source=source.replace('next_expected = {"michael": 1, "gabriel": 1, "raphael": 1, "ouriel": 1}','''next_expected = {"michael": 1, "gabriel": 1, "raphael": 1, "ouriel": 1}\nfor prior_no in range(1, 41):\n    prior_dir = ROOT / "data/corpus/books" / f"book-{prior_no:02d}"\n    if not prior_dir.exists():\n        continue\n    for prior_path in prior_dir.glob("psalm-*.json"):\n        prior = json.loads(prior_path.read_text(encoding="utf-8"))\n        slug = prior.get("archangel")\n        number = prior.get("number")\n        if slug in next_expected and isinstance(number, int):\n            next_expected[slug] = max(next_expected[slug], number + 1)''')
source=source.replace('"scope": "books-01-10"','"scope": "books-41-44"')
source=source.replace('print(f"Extracted {len(report)} books with first-verse recovery")','print(f"Extracted {len(report)} final books 41-44 with first-verse recovery")')
required=['books-41-44-extraction-report.json','41 <= b["bookNumber"] <= 44','for prior_no in range(1, 41)','"scope": "books-41-44"']
missing=[x for x in required if x not in source]
if missing: raise RuntimeError(f'Unable to adapt base extractor; missing replacements: {missing}')
exec(compile(source,str(BASE),'exec'),{'__name__':'__main__','__file__':str(BASE)})
