#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from build_linguistic_user_confirmed_gold import ROOT, build, render
SCRIPTS=ROOT/"scripts"
SEMANTIC=ROOT/"data/linguistic-sense-runtime.json"
BROWSER=ROOT/"data/linguistic-sense-browser-runtime.json"
def run(name):
    subprocess.run([sys.executable,str(SCRIPTS/name)],cwd=ROOT,check=True)
def load(path):
    with Path(path).open(encoding="utf-8") as h:return json.load(h)
def main():
    p=argparse.ArgumentParser();p.add_argument("--review",required=True,type=Path);p.add_argument("--gold-output",required=True,type=Path);p.add_argument("--review-mission",required=True);p.add_argument("--confirmation-mission",required=True);a=p.parse_args()
    gold=build(a.review,a.review_mission,a.confirmation_mission)
    a.gold_output.parent.mkdir(parents=True,exist_ok=True);a.gold_output.write_bytes(render(gold))
    run("audit_linguistic_sense_contract.py")
    run("build_linguistic_sense_runtime.py");run("audit_linguistic_sense_runtime.py")
    run("build_linguistic_sense_browser_runtime.py");run("audit_linguistic_sense_browser_runtime.py")
    semantic=load(SEMANTIC);browser=load(BROWSER)
    print("PROMOTION = PASS");print(f"REVIEW = {a.review.as_posix()}");print(f"GOLD = {a.gold_output.as_posix()}")
    t=gold["target"];print(f"TARGET = {t['normalizedForm']} / {t['lemma']} / {t['partOfSpeech']}")
    print(f"VALIDATED = {sum(1 for e in gold['entries'] if e['adjudicationStatus']=='VALIDATED')}")
    print(f"SEMANTIC_RUNTIME_TARGETS = {len(semantic['targets'])}")
    print(f"SEMANTIC_RUNTIME_VALIDATED = {sum(len(t['validated']) for t in semantic['targets'])}")
    print(f"BROWSER_RUNTIME_TARGETS = {len(browser['targets'])}")
if __name__=="__main__": main()
