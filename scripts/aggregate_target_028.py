#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_ROWS = 216012
EXPECTED_SHARDS = 16

def shadow_score(oid: str) -> str:
    return hashlib.sha256(("shadow028|" + oid).encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards-dir", required=True)
    ap.add_argument("--replay027", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--shadow-selection", required=True)
    args = ap.parse_args()

    shard_files = sorted(Path(args.shards_dir).glob("shard-*.json"))
    assert len(shard_files) == EXPECTED_SHARDS, [p.name for p in shard_files]

    all_rows = []
    shard_ids = []
    for p in shard_files:
        payload = json.loads(p.read_text(encoding="utf-8"))
        shard_ids.append(payload["shard"])
        assert payload["inputCount"] == len(payload["rows"])
        all_rows.extend(payload["rows"])
    assert sorted(shard_ids) == list(range(EXPECTED_SHARDS))
    assert len(all_rows) == EXPECTED_ROWS, len(all_rows)

    ids = [r["occurrenceId"] for r in all_rows]
    unique_ids = set(ids)
    assert len(unique_ids) == EXPECTED_ROWS
    duplicate_count = len(ids) - len(unique_ids)
    assert duplicate_count == 0

    all_rows.sort(key=lambda r: r["occurrenceId"])

    status_counts = Counter(r["status028"] for r in all_rows)
    assert sum(status_counts.values()) == EXPECTED_ROWS

    reason_counts = Counter()
    for r in all_rows:
        if r["status028"] != "MACHINE_SAFE":
            reason_counts.update(r["reasonCodes"])

    by_form = defaultdict(list)
    for r in all_rows:
        by_form[r["normalizedForm"]].append(r["status028"])
    assert len(by_form) == 10444, len(by_form)

    forms_at_least_one_safe = sum(any(s == "MACHINE_SAFE" for s in vals) for vals in by_form.values())
    forms_all_safe = sum(all(s == "MACHINE_SAFE" for s in vals) for vals in by_form.values())
    forms_mixed = sum(len(set(vals)) > 1 for vals in by_form.values())
    forms_zero_safe = sum(all(s != "MACHINE_SAFE" for s in vals) for vals in by_form.values())

    safe_pos = Counter(
        r["predictedBiblawLexicalPOS"]
        for r in all_rows
        if r["status028"] == "MACHINE_SAFE"
    )
    assert set(safe_pos).issubset({"NOUN","VERB","ADJ","ADV"})

    # Replay frozen 027-A selection against the stored 025 prediction reconstructed in prepare-target.
    replay = json.loads(Path(args.replay027).read_text(encoding="utf-8"))
    assert replay["count"] == 200
    by_id = {r["occurrenceId"]: r for r in all_rows}
    replay_match = 0
    replay_mismatches = []
    replay_eligible = 0
    replay_excluded_by_028_gate = 0
    for e in replay["items"]:
        # 027-C validated 200 positive cases, but 026 later excludes entire
        # normalized forms whenever ANY corpus occurrence has boundary risk.
        # Replay only the frozen 027 cases whose form is actually in the 028
        # target population; excluded forms are intentionally absent.
        if e["normalizedForm"] not in by_form:
            assert e["occurrenceId"] not in by_id, e["occurrenceId"]
            replay_excluded_by_028_gate += 1
            continue
        replay_eligible += 1
        r = by_id.get(e["occurrenceId"])
        assert r is not None, e["occurrenceId"]
        ok = (
            r["status028"] == "MACHINE_SAFE"
            and (r.get("predictedLemma") or "").casefold() == e["predictedLemma"].casefold()
            and r.get("predictedBiblawLexicalPOS") == e["predictedBiblawLexicalPOS"]
        )
        if ok:
            replay_match += 1
        else:
            replay_mismatches.append({
                "occurrenceId":e["occurrenceId"],
                "expectedLemma":e["predictedLemma"],
                "expectedPOS":e["predictedBiblawLexicalPOS"],
                "observedStatus":r["status028"],
                "observedLemma":r.get("predictedLemma"),
                "observedPOS":r.get("predictedBiblawLexicalPOS"),
            })
    assert replay_eligible == 142, replay_eligible
    assert replay_excluded_by_028_gate == 58, replay_excluded_by_028_gate
    assert replay_match == replay_eligible and not replay_mismatches, replay_mismatches[:10]

    shadow_rows = sorted(all_rows, key=lambda r:(shadow_score(r["occurrenceId"]), r["occurrenceId"]))[:2000]
    shadow_selection = {
        "mission":"BIBLAW-LEXICAL-INDUSTRIALIZATION-028-GHA",
        "selection":"SHA256('shadow028|' + occurrenceId), ascending, first 2000",
        "count":2000,
        "occurrenceIds":[r["occurrenceId"] for r in shadow_rows],
    }
    Path(args.shadow_selection).write_text(
        json.dumps(shadow_selection, ensure_ascii=False, separators=(",",":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )

    base = {
        "mission":"BIBLAW-LEXICAL-INDUSTRIALIZATION-028-GHA",
        "targetForms":10444,
        "targetOccurrences":EXPECTED_ROWS,
        "shardCount":EXPECTED_SHARDS,
        "totalRows":len(all_rows),
        "uniqueOccurrenceIds":len(unique_ids),
        "duplicateOccurrenceIds":duplicate_count,
        "missingTargetOccurrences":0,
        "statusCounts":dict(sorted(status_counts.items())),
        "formsWithAtLeastOneMachineSafe":forms_at_least_one_safe,
        "formsAllOccurrencesMachineSafe":forms_all_safe,
        "formsMixedSafeReviewUnknown":forms_mixed,
        "formsWithZeroMachineSafe":forms_zero_safe,
        "machineSafePosCounts":dict(sorted(safe_pos.items())),
        "nonSafeReasonCounts":dict(sorted(reason_counts.items())),
        "replay027":{
            "frozenCount":200,
            "eligibleIn028":replay_eligible,
            "excludedBy028Gate":replay_excluded_by_028_gate,
            "match":replay_match,
            "mismatch":0,
        },
        "rows":all_rows,
    }
    Path(args.output).write_text(
        json.dumps(base, ensure_ascii=False, separators=(",",":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k:v for k,v in base.items() if k != "rows"}, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
