#!/usr/bin/env python3
"""Audit the authoritative PDF around book 32 / Psalm 182, without modifying corpus."""
import json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
OUT=ROOT/'data/pilot/book-32-psalm-182-boundary-audit.json'
raw=subprocess.run(['pdftotext','-layout','-f','3112','-l','3117',str(PDF),'-'],check=True,capture_output=True,text=True).stdout
pages=raw.split('\f')
report={'source':PDF.name,'policy':'PDF-only documentary audit; no external sources','requestedPdfPages':[3112,3117],'pages':[]}
for i,page in enumerate(pages):
    pageno=3112+i
    lines=[re.sub(r'\s+',' ',x).strip() for x in page.splitlines() if x.strip()]
    relevant=[]
    for j,s in enumerate(lines):
        if re.match(r'^(18[0-4])(?:\s|\.|$)',s) or re.match(r'^\d{1,3}[.]\s+',s) or 'Nouvelle Alliance' in s:
            relevant.append({'line':j,'text':s})
    report['pages'].append({'pdfPage':pageno,'relevantLines':relevant,'allLines':lines})
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(OUT)
