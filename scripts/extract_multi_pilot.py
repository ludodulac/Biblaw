#!/usr/bin/env python3
"""Extract four representative Archangel dialogue pilots from the source PDF."""
from __future__ import annotations
import json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
CONFIGS=[
 dict(archangel='gabriel',book=18,bookTitle='Quel chercheur de Lumière es-tu ?',number=112,title='Le vêtement blanc des Esséniens',first=1202,last=1206,psalmPages=[1202,1203,1204],prayer=1,prayerPages=[1204,1205,1206],verseCount=26,questionVerses=[14]),
 dict(archangel='raphael',book=19,bookTitle='Le secret de la pensée angélique',number=104,title='Le secret de la pensée angélique',first=1341,last=1345,psalmPages=[1341,1342,1343,1344],prayer=3,prayerPages=[1344,1345],verseCount=26,questionVerses=[22]),
 dict(archangel='ouriel',book=20,bookTitle='Aux portes de la Terre promise',number=105,title='Chaque épreuve est une chance',first=1464,last=1468,psalmPages=[1464,1465,1466,1467],prayer=2,prayerPages=[1467],verseCount=33,questionVerses=[18],nextPsalm=106),
 dict(archangel='gabriel',book=26,bookTitle="L'énergie créatrice",number=182,title="Que l’œuvre de la Nation Essénienne soit claire, pure et vraie",first=2417,last=2422,psalmPages=[2417,2418,2419,2420],prayer=66,prayerPages=[2420,2421],verseCount=30,questionVerses=[],nextPsalm=183,interludeAfter=18),
]

def extract(c):
 return subprocess.run(['pdftotext','-layout','-f',str(c['first']),'-l',str(c['last']),str(PDF),'-'],check=True,capture_output=True,text=True).stdout

def unwrap(s):
 s=re.sub(r'-\n\s*','',s); s=re.sub(r'\n\s*',' ',s); return re.sub(r'\s+',' ',s).strip()

def clean_furniture(raw,c):
 out=[]
 for line in raw.splitlines():
  s=line.strip()
  if re.match(r'^Livre \d+ \|',s,re.I) or (s.isdigit() and c['first']<=int(s)<=c['last']): continue
  out.append(line)
 return '\n'.join(out)

def note_blocks(raw):
 notes=[]
 pattern=r'(?m)^(\d+)\s*-\s+(.*?)(?=\n\s*\d+\s*\n?\f|\f)'
 for m in re.finditer(pattern,raw,re.S): notes.append((int(m.group(1)),unwrap(m.group(2))))
 return notes,re.sub(pattern,'',raw,flags=re.S)

def build(c):
 raw=extract(c)
 if c.get('nextPsalm'):
  boundary=re.search(rf'(?m)^\s*{c["nextPsalm"]}\s+[^\n]+',raw)
  if boundary: raw=raw[:boundary.start()]
 notes,raw=note_blocks(raw)
 if c['number']==182:
  notes=[n for n in notes if '2013' in n[1] and 'prêtr' in n[1].lower()]
 elif c['questionVerses']:
  notes=[n for n in notes if "questions d’Olivier" in n[1] or "questions d'Olivier" in n[1]]
 raw=clean_furniture(raw,c)
 title=re.search(rf'(?m)^\s*{c["number"]}\s+[^\n]+',raw)
 prayer_marker=re.search(rf'(?m)^\s*Pr\.\s*{c["prayer"]}\.\s*',raw)
 if not title or not prayer_marker: raise RuntimeError(f"Boundaries missing for {c['archangel']} {c['number']}")
 body=raw[title.end():prayer_marker.start()]
 dialogue=[]
 if c.get('interludeAfter'):
  im=re.search(r'Olivier Manitara demanda alors à L.Archange Gabriel\s*:\s*(.*?)(?=\n\s*19\.)',body,re.S|re.I)
  if not im: raise RuntimeError('Unnumbered Gabriel interlude missing')
  question=unwrap(im.group(1))
  dialogue.append(dict(id=f"{c['archangel']}-psalm-{c['number']:03d}-dialogue-001",speakerId='olivier-manitara',speechRole='question',text=question,numbering='unnumbered-interlude',verseNumber=None,positionAfterVerse=c['interludeAfter'],editorialCue="Olivier Manitara demanda alors à l’Archange Gabriel :",sourcePages=[2419]))
  body=body[:im.start()]+body[im.end():]
 matches=list(re.finditer(r'(?m)^\s*(\d{1,3})\.\s+',body)); verses=[]
 for i,m in enumerate(matches):
  n=int(m.group(1)); end=matches[i+1].start() if i+1<len(matches) else len(body)
  if n>c['verseCount']: continue
  role='question' if n in c['questionVerses'] else ('answer' if c['questionVerses'] and n>max(c['questionVerses']) else 'teaching')
  speaker=f"archangel-{c['archangel']}" if role!='question' else 'olivier-manitara'
  verses.append(dict(number=n,speakerId=speaker,speechRole=role,text=unwrap(body[m.end():end]),sourcePages=c['psalmPages']))
 for n in c['questionVerses']:
  v=next(v for v in verses if v['number']==n)
  dialogue.append(dict(id=f"{c['archangel']}-psalm-{c['number']:03d}-dialogue-{len(dialogue)+1:03d}",speakerId='olivier-manitara',speechRole='question',text=v['text'],numbering='numbered-verse',verseNumber=n,positionAfterVerse=n-1,editorialCue='Editorial note confirms that questions by Olivier Manitara were preserved as verses.',sourcePages=c['psalmPages']))
 if [v['number'] for v in verses]!=list(range(1,c['verseCount']+1)): raise RuntimeError(f"Verse sequence failed for {c['archangel']} {c['number']}")
 prayer_text=raw[prayer_marker.end():]
 if c.get('nextPsalm'):
  nm=re.search(rf'(?m)^\s*{c["nextPsalm"]}\s+[^\n]+',prayer_text)
  if nm: prayer_text=prayer_text[:nm.start()]
 prayer_text=unwrap(prayer_text)
 pid=f"{c['archangel']}-book-{c['book']:02d}-prayer-{c['prayer']:03d}"
 note_ids=[]
 note_records=[]
 for marker,note_text in notes:
  verse=c['questionVerses'][0] if c['questionVerses'] else (13 if c['number']==182 else None)
  nid=f"{c['archangel']}-psalm-{c['number']:03d}-note-{marker:03d}"; note_ids.append(nid)
  temporal=[]
  if '2009-2010' in note_text: temporal=[{'value':'2009-2010','kind':'edition-period'}]
  if '2013' in note_text: temporal=[{'value':'2013','kind':'historical-event-year'}]
  note_records.append(dict(id=nid,recordType='note',archangel=c['archangel'],appliesTo={'recordId':f"{c['archangel']}-psalm-{c['number']:03d}",'verse':verse,'marker':marker},text=note_text,source={'document':PDF.name,'printedPages':c['psalmPages']},temporalMentions=temporal,validation={'status':'machine-extracted-needs-human-review'}))
 psalm=dict(id=f"{c['archangel']}-psalm-{c['number']:03d}",recordType='psalm',archangel=c['archangel'],book={'number':c['book'],'title':c['bookTitle']},number=c['number'],title=c['title'],source={'document':PDF.name,'printedPages':c['psalmPages']},verses=verses,dialogueSegments=dialogue,noteIds=note_ids,prayerIds=[pid],contextIds=[f"{c['archangel']}-book-{c['book']:02d}-introduction"],temporalMentions=[],validation={'status':'machine-extracted-needs-human-review','checks':{'verseSequenceComplete':True,'verseCount':c['verseCount'],'prayerDetectedByAdjacency':True}})
 prayer=dict(id=pid,recordType='master-prayer',archangel=c['archangel'],bookNumber=c['book'],number=c['prayer'],speakerId='olivier-manitara',text=prayer_text,source={'document':PDF.name,'printedPages':c['prayerPages']},appliesToPsalmId=psalm['id'],attachment={'basis':'editorial-adjacency','description':f"Prayer {c['prayer']} is printed immediately after psalm {c['number']}."},validation={'status':'machine-extracted-needs-human-review'})
 return psalm,prayer,note_records

def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(path.relative_to(ROOT))

for config in CONFIGS:
 psalm,prayer,notes=build(config)
 write(ROOT/'data/corpus'/config['archangel']/f"psalm-{config['number']:03d}.json",psalm)
 write(ROOT/'data/prayers'/f"{prayer['id']}.json",prayer)
 for note in notes: write(ROOT/'data/notes'/f"{note['id']}.json",note)
