#!/usr/bin/env python3
"""042B2: corpus-wide, read-only extraction; automatic categories are NOT editorial validation."""
import argparse, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXACT=re.compile(r"(?<!\w)(pain|pains)(?!\w)",re.I|re.U)
RELATED=re.compile(r"(?<!\w)(nourriture|nourritures|nourrir|nourrit|nourrissent|manger|mange|mangent|mangé|blé)(?!\w)",re.I|re.U)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="data/editorial-evidence/042b2-pain-candidates.json")
    args=ap.parse_args()
    files=sorted((ROOT/"data/corpus/books").glob("book-*/psalm-*.json"))
    if len(files)!=1158:raise RuntimeError(f"Expected 1158 canonical psalms, got {len(files)}")
    entries=[];related=[];counts=Counter();unique=set()
    for path in files:
        psalm=json.loads(path.read_text(encoding="utf-8"))
        verses=psalm["verses"];book=psalm["book"]["number"];number=psalm["number"]
        for i,v in enumerate(verses):
            txt=v["text"]; hits=EXACT.findall(txt); conn=RELATED.findall(txt)
            if not hits and not conn:continue
            entry={"record_id":psalm["id"],"book":book,"psalm":number,"archangel":psalm["archangel"],"title":psalm["title"],"verse":v["number"],"text":txt,
                "context_before":verses[i-1]["text"] if i else None,
                "context_after":verses[i+1]["text"] if i+1<len(verses) else None,
                "exact_terms":[h.lower() for h in hits],"related_terms":[h.lower() for h in conn],
                "editorial_classification":"UNREVIEWED","editorial_justification":None,
                "verified_teaching":False,"theme_decision":None}
            if hits:
                entries.append(entry);unique.add(psalm["id"]);counts.update(h.lower() for h in hits)
            else:related.append(entry)
    payload={"mission":"BIBLAW-042B2","source":"data/corpus/books/book-*/psalm-*.json","psalms_scanned":len(files),
        "pain_occurrences":counts["pain"],"pains_occurrences":counts["pains"],
        "pain_verses":sum("pain" in x["exact_terms"] for x in entries),
        "pains_verses":sum("pains" in x["exact_terms"] for x in entries),
        "unique_psalms":len(unique),"passages":entries,"related_candidates":related,
        "note":"All classifications UNREVIEWED until manual contextual reading; related candidates are not proof of bread teachings."}
    out=ROOT/args.output;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in payload.items() if k not in ("passages","related_candidates")},ensure_ascii=False))
    print("exact_passages",len(entries),"related_candidates",len(related),"output",out)
if __name__=="__main__":main()
