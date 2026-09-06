#!/usr/bin/env python3
"""Audit known Psalm extraction anomalies directly from the authoritative PDF.

Documentary diagnostics only: no external source, no doctrinal interpretation. Each case gets a
small standalone report so its raw neighborhood can be inspected without truncating the others.
"""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
OUTDIR=ROOT/'data/pilot/missing-psalm-audits'
CASES=[
 {'book':15,'psalm':75,'pages':[914,923],'heading':r'^75\s+O\s*n\s+reconnaît\s+un\s+homme\s+à\s+ses\s+œuvres'},
 {'book':23,'psalm':128,'pages':[1922,1932],'heading':r'128\s+.*rêveur'},
 {'book':26,'psalm':186,'pages':[2431,2442],'heading':r'186\s+.*désir.*apprendre'},
 {'book':35,'psalm':215,'pages':[3480,3490],'heading':r'215\s+.*clé magique'},
 {'book':36,'psalm':217,'pages':[3577,3590],'heading':r'217\s+.*prêt.*écouter'},
 {'book':38,'psalm':260,'pages':[3862,3877],'heading':r'260\s+.*éduqueras pas des enfants'},
 {'book':44,'psalm':285,'pages':[4302,4312],'heading':r'285\s+'},
]
def pdftext(first,last):
 return subprocess.run(['pdftotext','-layout','-f',str(first),'-l',str(last),str(PDF),'-'],check=True,capture_output=True,text=True).stdout
def compact(s): return re.sub(r'\s+',' ',s).strip()
def page_chunks(first,raw):
 return [(first+i,p) for i,p in enumerate(raw.split('\f'))]
def heading_match(line,case):
 s=compact(line)
 return bool(re.search(case['heading'],s,re.I))
OUTDIR.mkdir(parents=True,exist_ok=True)
summary=[]
for case in CASES:
 raw=pdftext(*case['pages']); lines=raw.splitlines(); hi=next((i for i,line in enumerate(lines) if heading_match(line,case)),None)
 all_headings=[]
 for i,line in enumerate(lines):
  s=compact(line); m=re.match(r'^(\d{2,3})\s+([^0-9].{2,})$',s)
  if m and len(m.group(2).split())<=30: all_headings.append({'lineIndex':i,'number':int(m.group(1)),'text':m.group(2)})
 before=[h for h in all_headings if hi is not None and h['lineIndex']<hi][-3:]
 after=[h for h in all_headings if hi is not None and h['lineIndex']>hi][:3]
 start=max(0,(hi or 0)-80); end=min(len(lines),(hi or 0)+300)
 numbered=[]
 for i in range(start,end):
  s=compact(lines[i]); m=re.match(r'^(\d{1,3})[.]\s+(.*)',s)
  if m: numbered.append({'lineIndex':i,'verse':int(m.group(1)),'text':m.group(2)})
 seq=[x['verse'] for x in numbered]
 resets=[{'atIndex':i,'previous':seq[i-1] if i else None,'current':v} for i,v in enumerate(seq) if i and v<=seq[i-1]]
 ones=[x for x in numbered if x['verse']==1]
 pages=[]
 for pageno,page in page_chunks(case['pages'][0],raw):
  plines=[compact(x) for x in page.splitlines() if compact(x)]
  relevant=[]
  for i,s in enumerate(plines):
   if heading_match(s,case) or re.match(r'^\d{1,3}[.]\s+',s): relevant.append({'line':i,'text':s})
  if relevant: pages.append({'pdfPage':pageno,'relevantLines':relevant})
 report={
  'source':PDF.name,'policy':'PDF-only documentary audit; no external sources',**case,
  'headingLineIndex':hi,'nearestHeadingsBefore':before,'nearestHeadingsAfter':after,
  'numberedVerseCandidates':numbered,'verseSequence':seq,'sequenceResetsOrDuplicates':resets,
  'verseOneCandidates':ones,'pageRelevantLines':pages,
  'assessment':{'safeToAutoRepair':False,'reason':'Diagnostic only; repair must be explicitly encoded after inspecting this report.'}
 }
 path=OUTDIR/f'book-{case["book"]:02d}-psalm-{case["psalm"]:03d}.json'
 path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 summary.append({'book':case['book'],'psalm':case['psalm'],'headingFound':hi is not None,'verseOneCount':len(ones),'sequenceResetCount':len(resets),'report':str(path.relative_to(ROOT))})
(ROOT/'data/pilot/missing-psalm-boundary-audit.json').write_text(json.dumps({'source':PDF.name,'policy':'PDF-only documentary audit; no external sources','cases':summary},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Audited {len(summary)} Psalm extraction anomalies')