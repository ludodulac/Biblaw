#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC_RUNTIME = ROOT / "data" / "linguistic-sense-runtime.json"
OCCURRENCE_BUILDER = ROOT / "scripts" / "build_linguistic_occurrence_index.py"
DEFAULT_OUTPUT = ROOT / "data" / "linguistic-sense-browser-runtime.json"
GENERATOR = "scripts/build_linguistic_sense_browser_runtime.py"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: top-level JSON must be an object")
    return value


def load_occurrence_builder():
    spec = importlib.util.spec_from_file_location("linguistic_occurrence_index", OCCURRENCE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load linguistic occurrence index builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_browser_runtime() -> dict:
    semantic = load_json(SEMANTIC_RUNTIME)
    assert semantic.get("v") == 1
    assert semantic.get("purpose") == "linguistic-sense-runtime"
    source_targets = semantic.get("targets")
    assert isinstance(source_targets, list)

    occurrence_builder = load_occurrence_builder()
    target_keys: set[tuple[str, str, str]] = set()
    global_occurrence_ids: set[str] = set()
    targets: list[dict] = []

    for source_target in source_targets:
        normalized_form = source_target["normalizedForm"]
        lemma = source_target["lemma"]
        pos = source_target["partOfSpeech"]
        target_key = (normalized_form, lemma, pos)
        if target_key in target_keys:
            raise RuntimeError(f"DUPLICATE_SEMANTIC_RUNTIME_TARGET: {target_key}")
        target_keys.add(target_key)

        locations = {
            row["occurrenceId"]: {
                "recordId": row["recordId"],
                "recordType": row.get("recordType"),
                "verseNumber": row.get("verseNumber"),
            }
            for row in occurrence_builder.occurrences(normalized_form)
        }

        senses = source_target.get("senses")
        assert isinstance(senses, list) and senses
        sense_ids = [sense["senseId"] for sense in senses]
        buckets = {
            sense_id: defaultdict(lambda: {"occurrenceCount": 0, "verseNumbers": set()})
            for sense_id in sense_ids
        }

        for occurrence_id, sense_id in source_target.get("validated", []):
            if occurrence_id in global_occurrence_ids:
                raise RuntimeError(f"DUPLICATE_RUNTIME_OCCURRENCE_ID: {occurrence_id}")
            global_occurrence_ids.add(occurrence_id)
            location = locations.get(occurrence_id)
            if location is None:
                raise RuntimeError(f"MISSING_SEMANTIC_OCCURRENCE_LOCATION: {occurrence_id}")
            if sense_id not in buckets:
                raise RuntimeError(f"UNKNOWN_RUNTIME_SENSE_ID: {sense_id}")
            record_id = location["recordId"]
            if not isinstance(record_id, str) or not record_id:
                raise RuntimeError(f"EMPTY_SEMANTIC_RECORD_ID: {occurrence_id}")
            bucket = buckets[sense_id][record_id]
            bucket["occurrenceCount"] += 1
            verse_number = location["verseNumber"]
            if verse_number is not None:
                bucket["verseNumbers"].add(int(verse_number))

        uncertain = source_target.get("uncertain", [])
        for occurrence_id in uncertain:
            if occurrence_id in global_occurrence_ids:
                raise RuntimeError(f"DUPLICATE_RUNTIME_OCCURRENCE_ID: {occurrence_id}")
            global_occurrence_ids.add(occurrence_id)
            if occurrence_id not in locations:
                raise RuntimeError(f"MISSING_SEMANTIC_OCCURRENCE_LOCATION: {occurrence_id}")

        projected_senses = []
        for source_sense in senses:
            sense_id = source_sense["senseId"]
            records = [
                [
                    record_id,
                    values["occurrenceCount"],
                    sorted(values["verseNumbers"]),
                ]
                for record_id, values in sorted(buckets[sense_id].items())
            ]
            projected_senses.append({
                "senseId": sense_id,
                "label": source_sense["label"],
                "occurrenceCount": sum(record[1] for record in records),
                "records": records,
            })

        targets.append({
            "normalizedForm": normalized_form,
            "lemma": lemma,
            "partOfSpeech": pos,
            "senses": projected_senses,
            "uncertainOccurrenceCount": len(uncertain),
        })

    targets.sort(key=lambda target: (
        target["normalizedForm"],
        target["lemma"],
        target["partOfSpeech"],
    ))
    return {
        "v": 1,
        "purpose": "linguistic-sense-browser-runtime",
        "generator": GENERATOR,
        "targets": targets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    runtime = build_browser_runtime()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(runtime, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    validated = sum(
        sense["occurrenceCount"]
        for target in runtime["targets"]
        for sense in target["senses"]
    )
    uncertain = sum(target["uncertainOccurrenceCount"] for target in runtime["targets"])
    print(
        f"LINGUISTIC_SENSE_BROWSER_RUNTIME_BUILD = PASS · "
        f"{len(runtime['targets'])} target(s) · "
        f"{validated} validated · {uncertain} uncertain"
    )


if __name__ == "__main__":
    main()
