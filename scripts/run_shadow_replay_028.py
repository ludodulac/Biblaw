#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

def load_runner(path: Path):
    spec = importlib.util.spec_from_file_location("runner028", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-dir", required=True)
    ap.add_argument("--selection", required=True)
    ap.add_argument("--runner-script", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    selection = json.loads(Path(args.selection).read_text(encoding="utf-8"))
    wanted = set(selection["occurrenceIds"])
    assert len(wanted) == 2000

    rows = []
    for p in sorted((Path(args.target_dir) / "shards").glob("shard-*.json")):
        payload = json.loads(p.read_text(encoding="utf-8"))
        rows.extend(r for r in payload["rows"] if r["occurrenceId"] in wanted)
    assert len(rows) == 2000
    assert {r["occurrenceId"] for r in rows} == wanted
    rows.sort(key=lambda r:r["occurrenceId"])

    runner = load_runner(Path(args.runner_script))
    spa, spacy_version, spacy_model_version = runner.spacy_run(rows)
    sta, stanza_version = runner.stanza_run(rows)
    assert spacy_version == "3.8.16"
    assert spacy_model_version == "3.8.0"
    assert stanza_version == "1.14.0"

    out = []
    for row in rows:
        a = spa[row["occurrenceId"]]
        b = sta[row["occurrenceId"]]
        status, reasons = runner.classify(row, a, b)
        item = {
            "occurrenceId":row["occurrenceId"],
            "spacy":a,
            "stanza":b,
            "status028":status,
            "reasonCodes":reasons,
            "predictedLemma":a["externalLemma"] if status == "MACHINE_SAFE" else None,
            "predictedBiblawLexicalPOS":a["projectedPOS"] if status == "MACHINE_SAFE" else None,
        }
        out.append(item)

    result = {
        "mission":"BIBLAW-LEXICAL-INDUSTRIALIZATION-028-GHA",
        "kind":"SHADOW_REPLAY",
        "count":2000,
        "engineVersions":{
            "spacy":spacy_version,
            "fr_core_news_sm":spacy_model_version,
            "stanza":stanza_version,
            "stanzaResourcesVersion":"1.14.0",
        },
        "rows":out,
    }
    Path(args.output).write_text(
        json.dumps(result, ensure_ascii=False, separators=(",",":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("SHADOW_REPLAY_COUNT = 2000")

if __name__ == "__main__":
    main()
