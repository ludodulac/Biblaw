#!/usr/bin/env python3
"""Write a compact, deterministic summary of the PDF-derived book inventory."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'data/pilot/book-inventory.json'
out=ROOT/'data/pilot/book-inventory-summary.json'
data=json.loads(src.read_text(encoding='utf-8'))
books=data.get('books',[])
summary={
  'source':data.get('source'),
  'status':'derived-from-book-inventory',
  'bookCount':len(books),
  'minBookNumber':min((b.get('bookNumber') for b in books if isinstance(b.get('bookNumber'),int)),default=None),
  'maxBookNumber':max((b.get('bookNumber') for b in books if isinstance(b.get('bookNumber'),int)),default=None),
  'books':[{'bookNumber':b.get('bookNumber'),'title':b.get('title'),'pdfPages':b.get('pdfPages')} for b in books]
}
out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Inventory contains {summary['bookCount']} books; max={summary['maxBookNumber']}")
