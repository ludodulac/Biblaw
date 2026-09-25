#!/usr/bin/env python3
import importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("occ",ROOT/"scripts/build_linguistic_occurrence_index.py");occ=importlib.util.module_from_spec(s);s.loader.exec_module(occ)
forms=["marche","compte","livre","veille","aide","garde","reste","passe","juste","suis","sens","tour"]
for form in forms:
 xs=occ.occurrences(form)
 print(json.dumps({"form":form,"count":len(xs)},ensure_ascii=False))
xs=occ.occurrences("suis")
patterns={"JE_SUis":r"\bje\s+(?:me\s+)?suis\b","TU_SUis":r"\btu\s+suis\b","IMPERATIVE":r"(?:^|[.!?…:]\s*)Suis\b","CLITIC":r"\bsuis[-‑–—](?:le|la|les|lui|leur|en|y)\b","OTHER":r"\bsuis\b"}
for name,pat in patterns.items():
 out=[{"id":x["occurrenceId"],"context":x["context"]} for x in xs if re.search(pat,x["context"],re.I if name!="IMPERATIVE" else 0)]
 print(json.dumps({"bucket":name,"count":len(out),"sample":out[:30]},ensure_ascii=False))
