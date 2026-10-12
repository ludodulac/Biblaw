#!/usr/bin/env python3
"""Run the canonical target-scoped semantic review pipeline."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, *arguments):
    subprocess.run([sys.executable, str(HERE / script), *map(str, arguments)], check=True)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_targets(proposals, calibration, lemma, pos):
    expected = {"lemma": lemma, "partOfSpeech": pos}
    if proposals.get("target") != expected or calibration.get("target") != expected:
        raise SystemExit("TARGET_MISMATCH")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lemma", required=True)
    parser.add_argument("--pos", required=True)
    parser.add_argument("--proposals-output", type=Path, required=True)
    parser.add_argument("--calibration-output", type=Path, required=True)
    parser.add_argument("--queue-output", type=Path, required=True)
    args = parser.parse_args()
    run("evaluate_linguistic_sense_classifier.py", "--lemma", args.lemma, "--pos", args.pos, "--output", args.proposals_output)
    run("calibrate_linguistic_sense_threshold_per_sense.py", "--lemma", args.lemma, "--pos", args.pos, "--output", args.calibration_output)
    proposals, calibration = read(args.proposals_output), read(args.calibration_output)
    verify_targets(proposals, calibration, args.lemma, args.pos)
    run("build_linguistic_sense_review_queue.py", "--proposals", args.proposals_output, "--calibration", args.calibration_output, "--output", args.queue_output)
    run("audit_linguistic_sense_review_pipeline.py", "--lemma", args.lemma, "--pos", args.pos, "--proposals", args.proposals_output, "--calibration", args.calibration_output, "--queue", args.queue_output)
    queue = read(args.queue_output)
    print("\n".join((
        "PREPARE_REVIEW = PASS",
        f"TARGET = {args.lemma} / {args.pos}",
        f"PROPOSALS = {args.proposals_output}",
        f"CALIBRATION = {args.calibration_output}",
        f"QUEUE = {args.queue_output}",
        f"VALIDATED_TRAINING_COUNT = {proposals['evaluation']['validatedCount']}",
        f"UNSEEN_PROPOSAL_COUNT = {len(proposals['unseenProposals'])}",
        f"REVIEW_COUNT = {queue['reviewCount']}",
        f"AUTO_ACCEPT_ELIGIBLE_COUNT = {queue['autoAcceptEligibleCount']}",
    )))


if __name__ == "__main__":
    main()
