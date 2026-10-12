#!/usr/bin/env python3
"""Prepare a neutral, deterministic human bootstrap packet from canonical occurrences."""
import argparse
import json
from pathlib import Path
from build_linguistic_occurrence_index import norm, occurrences


def build(form, lemma, pos):
    rows = sorted(occurrences(form), key=lambda row: row["occurrenceId"])
    if not rows:
        raise SystemExit("NO_OCCURRENCES")
    return {
        "schemaVersion": 1,
        "purpose": "linguistic-sense-bootstrap-review",
        "target": {"normalizedForm": norm(form), "lemma": lemma, "partOfSpeech": pos},
        "occurrenceCount": len(rows),
        "occurrences": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--form", required=True)
    parser.add_argument("--lemma", required=True)
    parser.add_argument("--pos", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not all((args.form.strip(), args.lemma.strip(), args.pos.strip())):
        parser.error("form, lemma and pos must be nonempty")
    packet = build(args.form, args.lemma, args.pos)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"BOOTSTRAP_BUILD = PASS; OCCURRENCE_COUNT = {packet['occurrenceCount']}")


if __name__ == "__main__":
    main()
