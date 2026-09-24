#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("occ",ROOT/"scripts/build_linguistic_occurrence_index.py");occ=importlib.util.module_from_spec(s);s.loader.exec_module(occ)
forms=["marche","compte","livre","veille","aide","garde","reste","passe","juste","suis","sens","tour"]
for form in forms:
 xs=occ.occurrences(form)
 print(json.dumps({"form":form,"count":len(xs),"sample":[{"id":x["occurrenceId"],"context":x["context"]} for x in xs[:12]]},ensure_ascii=False))
