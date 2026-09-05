#!/usr/bin/env python3
"""Audit known missing Psalm boundaries directly from the authoritative PDF.

This is documentary diagnostics only. It never interprets doctrine and never uses external
sources. The output preserves nearby raw lines and numbered-verse candidates so a deterministic
repair can be written without guessing.
"""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
OUT=ROOT/'data/pilot/missing-psalm-boundary-audit.json'
CASES=[
 {'book':23,'psalm':128,'pages':[1924,1931],'heading':r'128\s+.*rêveur'},
 {'book':26,'psalm':186,'pages':[2433,2441],'heading':r'186\s+.*désir.*apprendre'},
 {'book':35,'psalm':215,'pages':[3482,3488],'heading':r'215\s+.*clé magique'},
 {'book':36,'psalm':217,'pages':[3579,3588],'heading':r'217\s+.*prêt.*écouter'},
 {'book':38,'psalm':260,'pages':[3864,3875],'heading':r'260\s+.*éduqueras pas des enfants'},
]
def pdftext(first,last):
 return subprocess.run(['pdftotext','-layout','-f',str(first),'-l',str(last),str(PDF),'-'],check=True,capture_output=True,text=True).stdout
def compact(s): return re.sub(r'\s+',' ',s).strip()
report=[]
for case in CASES:
 raw=pdftext(*case['pages']); lines=raw.splitlines(); hi=None
 for i,line in enumerate(lines):
  if re.search(case['heading'],compact(line),re.I): hi=i; break
 # looser fallback by Psalm number
 if hi is None:
  for i,line in enumerate(lines):
   if re.match(rf'^\s*{case["psalm"]}\s+',line): hi=i; break
 start=max(0,(hi or 0)-25); end=min(len(lines),(hi or 0)+140)
 window=lines[start:end]
 numbered=[]
 for j,line in enumerate(window,start):
  m=re.match(r'^\s*(\d{1,3})[.]\s+(.*)',line)
  if m: numbered.append({'lineIndex':j,'verse':int(m.group(1)),'text':compact(m.group(2))})
 headings=[]
 for j,line in enumerate(window,start):
  m=re.match(r'^\s*(\d{2,3})\s+([^0-9].{2,})$',line)
  if m: headings.append({'lineIndex':j,'number':int(m.group(1)),'text':compact(m.group(2))})
 report.append({**case,'headingLineIndex':hi,'windowStart':start,'windowEnd':end,'lines':[{'lineIndex':j,'text':compact(line)} for j,line in enumerate(window,start) if compact(line)],'numberedVerseCandidates':numbered,'headingCandidates':headings})
OUT.write_text(json.dumps({'source':PDF.name,'policy':'PDF-only documentary audit; no external sources','cases':report},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Audited {len(report)} missing Psalm boundaries')
