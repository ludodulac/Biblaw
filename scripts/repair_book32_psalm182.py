#!/usr/bin/env python3
"""Repair Book 32 Psalm 182 from the authoritative PDF only.

The generic extraction skipped the explicit Psalm 182 heading because its printed
verse numbering continues at 28. This deterministic repair reconstructs the Psalm
from its explicit heading through the heading of Psalm 183, preserving source
verse numbering exactly and updating Book 32 metadata.
"""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'Bible essénienne (classée par livres).pdf'
BOOK=ROOT/'data/corpus/books/book-32'
NOTES=ROOT/'data/notes/books/book-32'

def unwrap(s):
    s=re.sub(r'-\n\s*','',s); s=re.sub(r'\n\s*',' ',s)
    return re.sub(r'\s+',' ',s).strip()

def page_at(text,offset,default):
    ms=list(re.finditer(r'\[\[PAGE (\d+)\]\]',text[:offset]))
    return int(ms[-1].group(1)) if ms else default

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    raw=subprocess.run(['pdftotext','-layout','-f','3109','-l','3117',str(PDF),'-'],check=True,capture_output=True,text=True).stdout
    chunks=[]
    for i,p in enumerate(raw.split('\f')):
        if not p.strip(): continue
        page=3109+i
        lines=[]
        for line in p.splitlines():
            s=line.strip()
            if re.search(r'(?i)\bLivre\s+32\s*\|',s) or s==str(page): continue
            lines.append(line)
        chunks.append(f'\n[[PAGE {page}]]\n'+'\n'.join(lines))
    text=''.join(chunks)
    h182=re.search(r'(?mi)^\s*182\s+N\s*ul\s+ne\s+peut\s+aller\s+vers\s+l[’\']\s*esprit.*$',text)
    h183=re.search(r'(?mi)^\s*183\s+.*(?:valeur|vraie valeur).*$' ,text[h182.end():] if h182 else '')
    if not h182 or not h183: raise RuntimeError('Audited Psalm 182/183 boundary not found')
    end=h182.end()+h183.start()
    segment=text[h182.end():end]
    # Remove footnotes without swallowing following verses/pages.
    note_re=re.compile(r'(?ms)^\s*(\d+)\s*[‑-]\s+(.*?)(?=^\s*\d+\s*[‑-]\s+|^\s*\d{1,3}[.]\s+|^\s*\[\[PAGE \d+\]\]|\Z)')
    notes=[]
    for m in note_re.finditer(segment):
        notes.append({'marker':int(m.group(1)),'text':unwrap(re.sub(r'\[\[PAGE \d+\]\]','',m.group(2))),'page':page_at(segment,m.start(),3109)})
    body=note_re.sub('',segment)
    matches=list(re.finditer(r'(?m)^\s*(\d{1,3})[.]\s+',body))
    verses=[]
    for i,m in enumerate(matches):
        stop=matches[i+1].start() if i+1<len(matches) else len(body)
        txt=unwrap(re.sub(r'\[\[PAGE \d+\]\]','',body[m.end():stop]))
        if txt: verses.append({'number':int(m.group(1)),'text':txt,'sourcePages':[page_at(body,m.start(),3109)]})
    nums=[v['number'] for v in verses]
    if not nums or nums[0]!=28 or nums!=list(range(28,nums[-1]+1)):
        raise RuntimeError(f'Unexpected Psalm 182 source numbering: {nums}')
    # Guard that Psalm 183 was not included.
    if any('Trouve ta valeur en redonnant' in v['text'] for v in verses): raise RuntimeError('Psalm 183 spillover')
    meta=json.loads((BOOK/'book.json').read_text(encoding='utf-8'))
    note_ids=[]
    for i,n in enumerate(notes,1):
        nid=f'book-32-psalm-182-note-{i:03d}'; note_ids.append(nid)
        write(NOTES/f'{nid}.json',{'id':nid,'recordType':'note','archangel':'ouriel','bookNumber':32,'appliesTo':{'recordId':'book-32-psalm-182','marker':n['marker'],'verse':None},'text':n['text'],'source':{'document':PDF.name,'pdfPage':n['page']},'validation':{'status':'machine-extracted-source-boundary-audited'}})
    rec={'id':'book-32-psalm-182','recordType':'psalm','archangel':'ouriel','book':{'number':32,'title':meta['title']},'number':182,'title':'Nul ne peut aller vers l’esprit sans passer par la matière','source':{'document':PDF.name,'pdfPages':sorted({p for v in verses for p in v['sourcePages']})},'verses':verses,'noteIds':note_ids,'extraction':{'headingBasis':'audited-explicit-heading-with-source-continuing-verse-numbering','sourceNumberingPreserved':True,'sourceFirstVerse':28,'auditedMissingPsalmRepair':True},'validation':{'status':'machine-extracted-source-boundary-audited','checks':{'verseCount':len(verses),'verseSequenceStartsAtOne':False,'verseSequenceContiguousFromSourceFirst':True}}}
    write(BOOK/'psalm-182.json',rec)
    ids=set(meta.get('psalmIds',[])); ids.add(rec['id']); meta['psalmIds']=sorted(ids,key=lambda x:int(x.rsplit('-',1)[1]))
    allnotes=set(meta.get('noteIds',[])); allnotes.update(note_ids); meta['noteIds']=sorted(allnotes)
    meta.setdefault('numbering',{})['expectedStart']=182
    meta['numbering']['nextExpected']=208
    write(BOOK/'book.json',meta)
    print(f'Repaired Book 32 Psalm 182: source verses {nums[0]}-{nums[-1]}, pages {rec["source"]["pdfPages"]}, notes {len(note_ids)}')

if __name__=='__main__': main()
