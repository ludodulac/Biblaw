#!/usr/bin/env python3
"""Repair audited Psalm extraction anomalies using the authoritative PDF only.

Five Psalms have explicit headings in the PDF but their first printed verse does not restart at 1;
the numbering continues from the preceding text/Psalm. The generic extractor intentionally skips
such headings. This script reconstructs those exact Psalm segments without renumbering them and,
where applicable, removes the duplicated tail from the preceding Psalm.

The final Psalm 285 of book 44 is also repaired by detaching the annex text that begins after its
verse 16. No doctrinal interpretation is performed; these are documentary boundary repairs.
"""
from __future__ import annotations
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
CORPUS=ROOT/'data/corpus/books'
NOTES=ROOT/'data/notes/books'

CASES=[
 {'book':23,'psalm':128,'previous':None,'next':129,'pages':[1922,1932],'startVerse':49,'title':'Ne sois pas un rêveur','heading':r'128\s+.*rêveur','nextHeading':r'129\s+.*réincarnation'},
 {'book':26,'psalm':186,'previous':185,'next':187,'pages':[2431,2442],'startVerse':23,'title':'Que le désir d’apprendre soit plus grand que vos certitudes','heading':r'186\s+.*désir.*apprendre','nextHeading':r'187\s+.*tradition'},
 {'book':35,'psalm':215,'previous':214,'next':216,'pages':[3480,3490],'startVerse':26,'title':'La clé magique pour attirer à soi ce que l’on souhaite','heading':r'215\s+.*clé magique','nextHeading':r'216\s+.*fidélité'},
 {'book':36,'psalm':217,'previous':216,'next':218,'pages':[3577,3590],'startVerse':16,'title':'Es-tu prêt à écouter le point de vue de la Lumière ?','heading':r'217\s+.*prêt.*écouter','nextHeading':r'218\s+.*engagements'},
 {'book':38,'psalm':260,'previous':259,'next':261,'pages':[3862,3877],'startVerse':23,'title':'Tu n’éduqueras pas des enfants dans l’esclavage','heading':r'260\s+.*éduqueras pas des enfants','nextHeading':r'261\s+.*maladie.*remède'},
]

def unwrap(value:str)->str:
 value=re.sub(r'-\n\s*','',value); value=re.sub(r'\n\s*',' ',value); return re.sub(r'\s+',' ',value).strip()
def clean_page(book_no,page_no,raw):
 lines=[]
 for line in raw.splitlines():
  s=line.strip()
  if re.search(rf'(?i)\bLivre\s+{book_no}\s*\|',s): continue
  if s==str(page_no): continue
  lines.append(line)
 return '\n'.join(lines)
def page_text(book_no,first,last):
 raw=subprocess.run(['pdftotext','-layout','-f',str(first),'-l',str(last),str(PDF),'-'],check=True,capture_output=True,text=True).stdout
 pages=[]
 for i,p in enumerate(raw.split('\f')):
  if p.strip(): pages.append((first+i,clean_page(book_no,first+i,p)))
 return ''.join(f'\n[[PAGE {p}]]\n{text}' for p,text in pages)
def page_at(text,offset,default):
 found=list(re.finditer(r'\[\[PAGE (\d+)\]\]',text[:offset])); return int(found[-1].group(1)) if found else default
def strip_markers(v): return re.sub(r'\[\[PAGE \d+\]\]','',v)
def write(path,data): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(s): return re.sub(r'\s+',' ',s).strip().lower().replace('’',"'")

def locate_line(text,pattern,start=0):
 for m in re.finditer(r'(?m)^.*$',text[start:]):
  if re.search(pattern,re.sub(r'\s+',' ',m.group(0)).strip(),re.I): return start+m.start(),start+m.end()
 return None

def extract_case(c):
 text=page_text(c['book'],*c['pages']); target=locate_line(text,c['heading'])
 if not target: raise RuntimeError(f"Target heading not found: {c}")
 nxt=locate_line(text,c['nextHeading'],target[1])
 if not nxt: raise RuntimeError(f"Next heading not found: {c}")
 segment=text[target[1]:nxt[0]]
 # Remove editorial footnotes from the Psalm body while preserving them as note records.
 note_pattern=re.compile(r'(?ms)^\s*(\d+)\s*-\s+(.*?)(?=^\s*\d+\s*-\s+|\Z)')
 notes=[{'marker':int(m.group(1)),'text':unwrap(strip_markers(m.group(2))),'page':page_at(segment,m.start(),c['pages'][0])} for m in note_pattern.finditer(segment)]
 body=note_pattern.sub('',segment)
 matches=list(re.finditer(r'(?m)^\s*(\d{1,3})[.]\s+',body)); verses=[]
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else len(body); txt=unwrap(strip_markers(body[m.end():end]))
  if txt: verses.append({'number':int(m.group(1)),'text':txt,'sourcePages':[page_at(body,m.start(),c['pages'][0])]})
 nums=[v['number'] for v in verses]
 expected=list(range(c['startVerse'],max(nums,default=c['startVerse']-1)+1))
 if not nums or nums!=expected: raise RuntimeError(f"Unexpected source numbering for book {c['book']} Psalm {c['psalm']}: {nums}")
 # Guard against accidentally parsing the next Psalm.
 if nums[0]!=c['startVerse']: raise RuntimeError(f"Wrong first source verse for {c}")
 book_dir=CORPUS/f"book-{c['book']:02d}"; note_dir=NOTES/f"book-{c['book']:02d}"
 # If the skipped heading made the previous Psalm swallow this segment, trim only after proving
 # that its first swallowed verse matches the PDF-derived first verse.
 if c['previous'] is not None:
  prev_path=book_dir/f"psalm-{c['previous']:03d}.json"; prev=json.loads(prev_path.read_text(encoding='utf-8'))
  pv=prev.get('verses',[]); idx=next((i for i,v in enumerate(pv) if v.get('number')==c['startVerse']),None)
  if idx is None: raise RuntimeError(f"Previous Psalm does not contain expected swallowed verse for {c}")
  if norm(pv[idx].get('text',''))[:90]!=norm(verses[0]['text'])[:90]: raise RuntimeError(f"Previous Psalm boundary text mismatch for {c}")
  prev['verses']=pv[:idx]; prev['source']['pdfPages']=sorted({p for v in prev['verses'] for p in v.get('sourcePages',[])})
  prev.setdefault('extraction',{})['auditedFollowingPsalmBoundaryRepaired']=True
  prev.setdefault('validation',{})['checks']={'verseCount':len(prev['verses']),'verseSequenceStartsAtOne':bool(prev['verses'] and prev['verses'][0]['number']==1)}
  write(prev_path,prev)
 # Replace any prior target-specific notes produced by this repair, but never delete unrelated source files.
 note_ids=[]
 for i,note in enumerate(notes,1):
  nid=f"book-{c['book']:02d}-psalm-{c['psalm']:03d}-note-{i:03d}"; note_ids.append(nid)
  write(note_dir/f'{nid}.json',{'id':nid,'recordType':'note','archangel':json.loads((book_dir/'book.json').read_text(encoding='utf-8')).get('archangel'),'bookNumber':c['book'],'appliesTo':{'recordId':f"book-{c['book']:02d}-psalm-{c['psalm']:03d}",'marker':note['marker'],'verse':None},'text':note['text'],'source':{'document':PDF.name,'pdfPage':note['page']},'validation':{'status':'machine-extracted-source-boundary-audited'}})
 meta=json.loads((book_dir/'book.json').read_text(encoding='utf-8'))
 record={'id':f"book-{c['book']:02d}-psalm-{c['psalm']:03d}",'recordType':'psalm','archangel':meta.get('archangel'),'book':{'number':c['book'],'title':meta.get('title')},'number':c['psalm'],'title':c['title'],'source':{'document':PDF.name,'pdfPages':sorted({p for v in verses for p in v['sourcePages']})},'verses':verses,'noteIds':note_ids,'extraction':{'headingBasis':'audited-explicit-heading-with-source-continuing-verse-numbering','sourceNumberingPreserved':True,'sourceFirstVerse':c['startVerse']},'validation':{'status':'machine-extracted-source-boundary-audited','checks':{'verseCount':len(verses),'verseSequenceStartsAtOne':False,'verseSequenceContiguousFromSourceFirst':True}}}
 write(book_dir/f"psalm-{c['psalm']:03d}.json",record)
 ids=set(meta.get('psalmIds',[])); ids.add(record['id']); meta['psalmIds']=sorted(ids,key=lambda x:int(x.rsplit('-',1)[1]))
 bn=set(meta.get('noteIds',[])); bn.update(note_ids); meta['noteIds']=sorted(bn)
 write(book_dir/'book.json',meta)
 print(f"Repaired book {c['book']} Psalm {c['psalm']}: source verses {nums[0]}-{nums[-1]}")

def repair_book44_final_psalm():
 path=CORPUS/'book-44'/'psalm-285.json'
 if not path.exists(): return
 data=json.loads(path.read_text(encoding='utf-8')); verses=data.get('verses',[])
 # The actual final Psalm ends at verse 16, where the annex title starts inside the extracted tail.
 v16=next((v for v in verses if v.get('number')==16),None)
 if not v16: raise RuntimeError('Book 44 Psalm 285 verse 16 not found')
 marker=re.search(r'\s*T[ÉE]MOIGNAGE\s+DE\s+L[’\']ANGE',v16.get('text',''),re.I)
 if not marker: raise RuntimeError('Audited final annex marker not found in book 44 Psalm 285 verse 16')
 v16['text']=v16['text'][:marker.start()].strip()
 data['verses']=[v for v in verses if isinstance(v.get('number'),int) and 1<=v['number']<=16]
 # Deduplicate defensively while preserving first occurrence; 1-16 must now be exact.
 by={}
 for v in data['verses']: by.setdefault(v['number'],v)
 data['verses']=[by[n] for n in sorted(by)]
 nums=[v['number'] for v in data['verses']]
 if nums!=list(range(1,17)): raise RuntimeError(f'Unexpected repaired book44 Psalm285 numbering: {nums}')
 data['noteIds']=[]
 data['source']['pdfPages']=sorted({p for v in data['verses'] for p in v.get('sourcePages',[])})
 data.setdefault('extraction',{})['auditedFinalAnnexDetached']=True
 data.setdefault('validation',{})['status']='machine-extracted-source-boundary-audited'
 data['validation']['checks']={'verseCount':16,'verseSequenceStartsAtOne':True}
 write(path,data)
 meta_path=CORPUS/'book-44'/'book.json'; meta=json.loads(meta_path.read_text(encoding='utf-8'))
 removed=set(meta.get('noteIds',[])); removed={x for x in removed if not x.startswith('book-44-psalm-285-note-')}; meta['noteIds']=sorted(removed)
 write(meta_path,meta)
 print('Repaired book 44 Psalm 285: detached annex spillover after verse 16')

def main():
 for c in CASES:
  # Only run when this extracted book exists; makes script safe across range-specific workflows.
  if (CORPUS/f"book-{c['book']:02d}"/'book.json').exists(): extract_case(c)
 repair_book44_final_psalm()
if __name__=='__main__': main()
