#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, io, json, tempfile, urllib.request, zipfile
from pathlib import Path
from build_linguistic_occurrence_index import CATALOG, ROOT, TOKEN_RE, fields, norm, searchable

MORPHALOU_URL="https://huggingface.co/datasets/datasets-CNRS/Morphalou/resolve/2b5dec836bef836a184d157ba3f71755bf55d523/Morphalou3.1_formatCSV_toutEnUn.zip?download=true"
MORPHALOU_SHA256="4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333"
MORPHALOU_SIZE=38062358
MORPHALOU_MEMBER="Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv"
SENSE_RUNTIME=ROOT/"data/linguistic-sense-runtime.json"
OUTPUT=ROOT/"data/linguistic-semantic-form-runtime.json"
POS_MAP={"Nom commun":"NOUN","Adjectif qualificatif":"ADJ","Adverbe":"ADV","Verbe":"VERB"}

def corpus_vocabulary():
 catalog=json.loads(CATALOG.read_text(encoding="utf-8")); vocabulary=set()
 for rel in catalog["records"]:
  path=ROOT/rel
  if not path.exists(): raise SystemExit(f"missing catalog record: {rel}")
  obj=json.loads(path.read_text(encoding="utf-8"))
  if not searchable(rel,obj): continue
  for _field,_verse,text in fields(obj):
   vocabulary.update(norm(m.group()) for m in TOKEN_RE.finditer(text))
 return vocabulary

def semantic_targets():
 payload=json.loads(SENSE_RUNTIME.read_text(encoding="utf-8"))
 targets=[{k:t[k] for k in ("normalizedForm","lemma","partOfSpeech")} for t in payload["targets"]]
 return sorted(targets,key=lambda t:(t["normalizedForm"],t["lemma"],t["partOfSpeech"]))

def obtain_morphalou():
 tmp=tempfile.NamedTemporaryFile(prefix="morphalou-3.1-",suffix=".zip",delete=False); path=Path(tmp.name)
 try:
  with urllib.request.urlopen(MORPHALOU_URL) as response,tmp:
   while chunk:=response.read(1024*1024): tmp.write(chunk)
 except Exception:
  path.unlink(missing_ok=True); raise
 return path

def verify_source(path):
 if path.stat().st_size!=MORPHALOU_SIZE: raise SystemExit(f"Morphalou size mismatch: {path.stat().st_size} != {MORPHALOU_SIZE}")
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest!=MORPHALOU_SHA256: raise SystemExit(f"Morphalou SHA-256 mismatch: {digest}")

def morphalou_forms(path,targets,vocabulary):
 wanted={(t["lemma"],t["partOfSpeech"]):t for t in targets}
 found={(t["normalizedForm"],t["lemma"],t["partOfSpeech"]):set() for t in targets}
 with zipfile.ZipFile(path) as archive:
  if MORPHALOU_MEMBER not in archive.namelist(): raise SystemExit(f"missing Morphalou member: {MORPHALOU_MEMBER}")
  with archive.open(MORPHALOU_MEMBER) as raw:
   text=io.TextIOWrapper(raw,encoding="utf-8-sig",newline="")
   rows=csv.reader(text,delimiter=";")
   header=None
   for candidate in rows:
    if len(candidate)>=3 and [cell.strip() for cell in candidate[:3]]==["GRAPHIE","ID","CATÉGORIE"]:
     header=[cell.strip() for cell in candidate]
     break
   if header is None: raise SystemExit("Morphalou CSV header not found")
   if "GRAPHIE_1" not in header: raise SystemExit("Morphalou GRAPHIE_1 column not found")
   reader=csv.DictReader(text,fieldnames=header,delimiter=";"); lemma=category=None
   for row in reader:
    if row.get("GRAPHIE"): lemma=row["GRAPHIE"].strip()
    if row.get("CATÉGORIE"): category=row["CATÉGORIE"].strip()
    pos=POS_MAP.get(category or ""); target=wanted.get((lemma,pos))
    if target is None: continue
    surface=(row.get("GRAPHIE_1") or "").strip()
    if not surface: continue
    normalized=norm(surface)
    if normalized in vocabulary:
     key=(target["normalizedForm"],target["lemma"],target["partOfSpeech"]); found[key].add(normalized)
 return found

def build(source):
 verify_source(source); targets=semantic_targets(); forms=morphalou_forms(source,targets,corpus_vocabulary()); runtime_targets=[]
 for target in targets:
  key=(target["normalizedForm"],target["lemma"],target["partOfSpeech"]); values=sorted(forms[key])
  if not values: raise SystemExit(f"no corpus-attested Morphalou forms for target: {key}")
  runtime_targets.append({**target,"forms":values})
 return {"v":1,"purpose":"linguistic-semantic-form-runtime","morphalouSha256":MORPHALOU_SHA256,"targets":runtime_targets}

def main():
 source=obtain_morphalou()
 try:
  payload=build(source); OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 finally: source.unlink(missing_ok=True)
 print(f"PASS targets={len(payload['targets'])} forms={sum(len(t['forms']) for t in payload['targets'])}")

if __name__=="__main__": main()
