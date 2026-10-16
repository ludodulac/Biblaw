#!/usr/bin/env python3
"""042B3: apply ONLY editorially verified 042B2 verse references to canonical thematic book sources.
The original 042B2 evidence JSON is SHA256-pinned. Never infer a relation from keyword matches.
"""
import hashlib,json,argparse,re
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data/thematic-index/editorial-pain-de-vie.json"
def read(p):return json.loads(Path(p).read_text(encoding="utf8"))
def main():
 p=argparse.ArgumentParser();p.add_argument("--evidence",required=True);args=p.parse_args()
 manifest=read(MANIFEST);raw=Path(args.evidence).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==manifest["evidenceSha256"],"042B2 evidence SHA mismatch"
 evidence=json.loads(raw);expected={(rid,int(v)) for rid,vs in manifest["verifiedVerseRefs"].items() for v in vs}
 verified={(x["record_id"],int(x["verse"])):x for x in evidence["passages"] if (x["record_id"],int(x["verse"])) in expected}
 assert len(expected)==30 and len(manifest["verifiedVerseRefs"])==26
 assert set(verified)==expected,"Manifest references missing in 042B2 canonical extraction"
 old=read(ROOT/"data/thematic-index/theme-search-index.json")
 assert not any(t["themeId"]==manifest["themeId"] for t in old["themes"])
 existing={a["queryKey"] for a in old["aliases"]}
 assert not (set(manifest["aliases"])|{"pain de vie"}) & existing,"Existing alias collision"
 bybook=defaultdict(dict)
 for rid,vs in manifest["verifiedVerseRefs"].items():
  match=re.fullmatch(r"book-(\d+)-psalm-(\d+)",rid);assert match,rid
  bybook[int(match.group(1))][rid]=sorted(vs)
 for book,psalms in sorted(bybook.items()):
  path=ROOT/f"data/thematic-index/books/book-{book:02d}.json";data=read(path)
  for psalm in data["psalmAnalyses"]:
   rid=psalm["recordId"]
   if rid not in psalms:continue
   assert not any(t["themeId"]==manifest["themeId"] for t in psalm["themes"])
   verses=psalms[rid]
   for v in verses:
    item=verified[(rid,v)]
    corpus=read(ROOT/f"data/corpus/books/book-{book:02d}/psalm-{int(psalm['number']):03d}.json")
    assert next((x["text"] for x in corpus["verses"] if x["number"]==v),None)==item["text"],f"Verse evidence differs: {rid} v{v}"
    assert item["exact_terms"],"Not a bread occurrence"
   excerpt=verified[(rid,verses[0])]["text"]
   # Use the canonical text itself as the teaching evidence: no generated paraphrase or inferred interpretation.
   teaching="Pain de vie — "+excerpt
   psalm["themes"].append({"themeId":manifest["themeId"],"label":manifest["label"],"importance":"important","directness":"symbolic","verseNumbers":verses,"teaching":teaching})
  path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("042B3 EDITORIAL_SOURCE_PASS",len(expected),"verses",len(manifest["verifiedVerseRefs"]),"psalms",len(bybook),"books")
if __name__=="__main__":main()
