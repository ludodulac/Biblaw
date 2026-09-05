#!/usr/bin/env python3
"""Complete the per-book context layer from canonical PDF-derived thematic indexes.

Existing curated contexts are preserved. Missing books receive a conservative provisional
context derived only from their canonical thematic book file and corpus metadata. No external
knowledge is introduced and no theme is manufactured beyond indexed evidence.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BOOKS=ROOT/'data/thematic-index/books'
CORPUS=ROOT/'data/corpus/books'
OUT=ROOT/'data/thematic-index/book-contexts.json'
base=json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {
 'schemaVersion':3,
 'purpose':'Preserve the context of each book strictly from the Bible essénienne PDF corpus so thematic search can interpret a psalm occurrence inside its book without introducing external information.',
 'books':[]
}
base['schemaVersion']=max(3,base.get('schemaVersion',3))
base.setdefault('sourcePolicy',{
 'authoritativeSource':'Bible essénienne (classée par livres).pdf','externalSourcesAllowed':False,'internetSourcesAllowed':False,
 'rule':'Every book-context statement and thematic interpretation must be derived only from material present in the authoritative PDF.'})
base.setdefault('analysisPolicy',{
 'stance':'neutral-corpus-analysis','rule':'Describe what the text teaches, associates, distinguishes, prescribes, warns against or symbolizes without judging whether its claims are true or false and without importing an external doctrinal framework.','separateEvidenceFromInference':True,'preferExplicitEvidence':True,'ambiguityRule':'When materially different readings remain plausible from the PDF, do not force a conclusion; register the ambiguity in data/incoherences.json.'})
base.setdefault('interpretationRule','A theme occurrence is first grounded in the psalm and verses. Book context is a second interpretive layer derived only from the PDF and used to explain emphasis, sense, relations and ranking. It must never manufacture a theme absent from the psalm.')
existing={x.get('bookNumber'):x for x in base.get('books',[]) if isinstance(x.get('bookNumber'),int)}
for path in sorted(BOOKS.glob('book-[0-9][0-9].json')):
 data=json.loads(path.read_text(encoding='utf-8')); b=data.get('book',{}); n=b.get('number')
 if not isinstance(n,int) or n in existing: continue
 meta_path=CORPUS/f'book-{n:02d}'/'book.json'; meta=json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
 synthesis=data.get('bookSynthesis',{}); themes=synthesis.get('majorThemes',[])[:15]
 status=data.get('method',{}).get('status')
 existing[n]={
  'bookNumber':n,'title':b.get('title') or meta.get('title'),'archangel':b.get('archangel') or meta.get('archangel'),
  'status':'provisional-corpus-derived' if status!='editorial-indexing-complete' else 'corpus-derived',
  'sourceBasis':f"PDF book {n}: book title, Psalm order, Psalm titles, Psalm text and editorial notes represented in the canonical corpus.",
  'centralAxis':synthesis.get('centralAxis',''),
  'contextThemes':themes,
  'interpretiveLens':'Use the recurring themes and movement of this book only as a secondary lens after the local Psalm and verse evidence. Do not infer a theme from book context alone.',
  'archangelContribution':'Not separately generalized at this stage. Preserve the formulations of this book and derive any Archangel-level nuance only in the later transversal semantic pass.',
  'searchUse':'Use this context to nuance ranking and explanation while keeping Psalm/verse evidence primary. This generated context remains eligible for deeper semantic refinement.'
 }
base['books']=[existing[n] for n in sorted(existing)]
OUT.write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Book contexts: {len(base['books'])}")
