#!/usr/bin/env python3
from __future__ import annotations
import ast, json
from build_linguistic_occurrence_index import ROOT, norm

RUNTIME=ROOT/"data/linguistic-semantic-form-runtime.json"
SENSE_RUNTIME=ROOT/"data/linguistic-sense-runtime.json"
BUILDER=ROOT/"scripts/build_linguistic_semantic_form_runtime.py"
EXPECTED_SHA="4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333"
TARGET_KEYS={"normalizedForm","lemma","partOfSpeech","forms"}
FORBIDDEN_DATA_KEYS={"context","senseId","validated","uncertain","occurrenceId","occurrences"}

def fail(message): raise SystemExit(f"FAIL: {message}")

def main():
 runtime=json.loads(RUNTIME.read_text(encoding="utf-8")); sense=json.loads(SENSE_RUNTIME.read_text(encoding="utf-8"))
 if runtime.get("v")!=1: fail("v must be 1")
 if runtime.get("purpose")!="linguistic-semantic-form-runtime": fail("unexpected purpose")
 if runtime.get("morphalouSha256")!=EXPECTED_SHA: fail("Morphalou SHA-256 mismatch")
 if set(runtime)!={"v","purpose","morphalouSha256","targets"}: fail("unexpected top-level data")
 canonical={(t["normalizedForm"],t["lemma"],t["partOfSpeech"]) for t in sense["targets"]}
 seen=set(); ordered=[]
 for target in runtime.get("targets",[]):
  if set(target)!=TARGET_KEYS: fail("unexpected target data")
  key=(target["normalizedForm"],target["lemma"],target["partOfSpeech"])
  if key not in canonical: fail(f"unknown semantic target: {key}")
  if key in seen: fail(f"duplicate target: {key}")
  seen.add(key); ordered.append(key); forms=target["forms"]
  if not forms: fail(f"empty forms: {key}")
  if forms!=sorted(forms) or len(forms)!=len(set(forms)): fail(f"forms not unique/deterministic: {key}")
  if any(form!=norm(form) for form in forms): fail(f"non-normalized form: {key}")
 if ordered!=sorted(ordered): fail("targets not deterministic")
 if seen!=canonical: fail("runtime does not cover every semantic target")
 def walk(value):
  if isinstance(value,dict):
   for key,child in value.items():
    if key in FORBIDDEN_DATA_KEYS: fail(f"forbidden contextual/sense occurrence key: {key}")
    walk(child)
  elif isinstance(value,list):
   for child in value: walk(child)
 walk(runtime)
 source=BUILDER.read_text(encoding="utf-8"); tree=ast.parse(source)
 literals={n.value.casefold() for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
 if {"bien","biens"}&literals: fail("word-specific literal in builder")
 compact="".join(source.casefold().split())
 for forbidden in ("rstrip(\"s\")","rstrip('s')","stripplural","singular/plural"):
  if forbidden in compact: fail(f"manual plural logic in builder: {forbidden}")
 print(f"PASS targets={len(seen)} forms={sum(len(t['forms']) for t in runtime['targets'])}")

if __name__=="__main__": main()
