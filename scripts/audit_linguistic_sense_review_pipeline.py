#!/usr/bin/env python3
"""Audit the cross-artifact contract, then invoke the canonical queue auditor."""
import argparse
import subprocess
import sys
from pathlib import Path
from prepare_linguistic_sense_review import HERE, read, verify_targets


def require(condition, code):
    if not condition:
        raise SystemExit(code)


def validate(proposals, calibration, queue, lemma, pos):
    verify_targets(proposals, calibration, lemma, pos)
    require(proposals.get("schemaVersion") == 1 and proposals.get("purpose") == "automatic-sense-classifier-evaluation", "INVALID_PROPOSALS_CONTRACT")
    require(calibration.get("schemaVersion") == 1 and calibration.get("purpose") == "independent-per-sense-threshold-calibration", "INVALID_CALIBRATION_CONTRACT")
    require(queue.get("schemaVersion") == 1 and queue.get("purpose") == "linguistic-sense-human-review-queue", "INVALID_QUEUE_CONTRACT")
    evaluation = proposals.get("evaluation", {})
    classes = evaluation.get("classes")
    per_sense = calibration.get("perSenseId")
    require(isinstance(classes, list) and isinstance(per_sense, dict) and set(classes) == set(per_sense), "CLASS_SET_MISMATCH")
    require(evaluation.get("validatedCount") == calibration.get("validatedCount"), "VALIDATED_COUNT_MISMATCH")
    unseen = proposals.get("unseenProposals")
    entries = queue.get("entries")
    require(isinstance(unseen, list) and isinstance(entries, list), "INVALID_REVIEW_ENTRIES")
    ids = [p["occurrenceId"] for p in unseen]
    review_ids = [e["occurrenceId"] for e in entries]
    require(len(ids) == len(set(ids)) and len(review_ids) == len(set(review_ids)) and set(review_ids) <= set(ids), "QUEUE_OCCURRENCE_MISMATCH")
    require(queue.get("reviewCount") == len(entries), "REVIEW_COUNT_MISMATCH")
    require(queue.get("autoAcceptEligibleCount") == len(unseen) - len(entries), "AUTO_ACCEPT_ELIGIBLE_COUNT_MISMATCH")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lemma", required=True)
    parser.add_argument("--pos", required=True)
    parser.add_argument("--proposals", type=Path, required=True)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    args = parser.parse_args()
    validate(read(args.proposals), read(args.calibration), read(args.queue), args.lemma, args.pos)
    subprocess.run([sys.executable, str(HERE / "audit_linguistic_sense_review_queue.py"), "--queue", str(args.queue), "--proposals", str(args.proposals), "--calibration", str(args.calibration)], check=True)
    print("PIPELINE_AUDIT = PASS")


if __name__ == "__main__":
    main()
