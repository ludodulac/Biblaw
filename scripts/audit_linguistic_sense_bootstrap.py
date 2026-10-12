#!/usr/bin/env python3
"""Audit a neutral bootstrap packet against canonical corpus occurrence extraction."""
import argparse
import json
from pathlib import Path
from build_linguistic_occurrence_index import norm, occurrences

FORBIDDEN = {"senseId", "proposedSenseId", "selectedSenseId", "decision", "score", "threshold"}


def require(condition, code):
    if not condition:
        raise SystemExit(code)


def no_semantic_fields(value):
    if isinstance(value, dict):
        return not (FORBIDDEN & value.keys()) and all(no_semantic_fields(v) for v in value.values())
    if isinstance(value, list):
        return all(no_semantic_fields(v) for v in value)
    return True


def audit(packet):
    require(packet.get("schemaVersion") == 1 and packet.get("purpose") == "linguistic-sense-bootstrap-review", "INVALID_BOOTSTRAP_CONTRACT")
    target = packet.get("target")
    require(isinstance(target, dict) and all(isinstance(target.get(k), str) and target[k].strip() for k in ("normalizedForm", "lemma", "partOfSpeech")), "INVALID_BOOTSTRAP_TARGET")
    require(target["normalizedForm"] == norm(target["normalizedForm"]), "INVALID_NORMALIZED_FORM")
    rows = packet.get("occurrences")
    require(isinstance(rows, list) and bool(rows) and packet.get("occurrenceCount") == len(rows), "INVALID_OCCURRENCE_COUNT")
    require(no_semantic_fields(packet), "FORBIDDEN_SEMANTIC_FIELD")
    ids = [row.get("occurrenceId") for row in rows]
    require(all(isinstance(oid, str) for oid in ids) and ids == sorted(ids) and len(ids) == len(set(ids)), "INVALID_OCCURRENCE_IDS")
    canonical = sorted(occurrences(target["normalizedForm"]), key=lambda row: row["occurrenceId"])
    require(rows == canonical, "CANONICAL_OCCURRENCE_MISMATCH")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", type=Path, required=True)
    args = parser.parse_args()
    audit(json.loads(args.bootstrap.read_text(encoding="utf-8")))
    print("BOOTSTRAP_AUDIT = PASS; CANONICAL_OCCURRENCE_MATCH = PASS")


if __name__ == "__main__":
    main()
