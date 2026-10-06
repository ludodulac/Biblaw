#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_linguistic_sense_contract import load_json, validate_catalog, validate_gold

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "linguistic" / "sense-catalog.json"
GOLD_DIR = ROOT / "data" / "linguistic" / "gold"
GOLD_GLOB = "*-sense-gold.json"
DEFAULT_OUTPUT = ROOT / "data" / "linguistic-sense-runtime.json"
GENERATOR = "scripts/build_linguistic_sense_runtime.py"


def _catalog_entries(catalog: dict) -> dict[tuple[str, str], dict]:
    return {
        (entry["lemma"], entry["partOfSpeech"]): entry
        for entry in catalog["entries"]
    }


def build_runtime() -> dict:
    catalog = load_json(CATALOG)
    catalog_index = validate_catalog(catalog)
    catalog_entries = _catalog_entries(catalog)

    gold_paths = sorted(GOLD_DIR.glob(GOLD_GLOB))
    assert gold_paths, "no semantic gold files found"

    targets: list[dict] = []
    target_keys: set[tuple[str, str, str]] = set()
    runtime_occurrence_ids: set[str] = set()

    for path in gold_paths:
        gold = load_json(path)
        validate_gold(gold, catalog_index, str(path))

        target = gold["target"]
        normalized_form = target.get("normalizedForm")
        lemma = target.get("lemma")
        pos = target.get("partOfSpeech")
        assert isinstance(normalized_form, str) and normalized_form.strip(), (
            f"{path}: target.normalizedForm must be non-empty"
        )

        runtime_key = (normalized_form, lemma, pos)
        if runtime_key in target_keys:
            raise RuntimeError(f"DUPLICATE_SEMANTIC_RUNTIME_TARGET: {runtime_key}")
        target_keys.add(runtime_key)

        catalog_entry = catalog_entries[(lemma, pos)]
        senses = [
            {"senseId": sense["senseId"], "label": sense["label"]}
            for sense in catalog_entry["senses"]
        ]

        validated: list[list[str]] = []
        uncertain: list[str] = []
        for entry in gold["entries"]:
            occurrence_id = entry["occurrenceId"]
            if occurrence_id in runtime_occurrence_ids:
                raise RuntimeError(f"DUPLICATE_RUNTIME_OCCURRENCE_ID: {occurrence_id}")
            runtime_occurrence_ids.add(occurrence_id)

            if entry["adjudicationStatus"] == "VALIDATED":
                validated.append([occurrence_id, entry["senseId"]])
            else:
                uncertain.append(occurrence_id)

        validated.sort(key=lambda item: item[0])
        uncertain.sort()
        targets.append({
            "normalizedForm": normalized_form,
            "lemma": lemma,
            "partOfSpeech": pos,
            "senses": senses,
            "validated": validated,
            "uncertain": uncertain,
        })

    targets.sort(key=lambda item: (
        item["normalizedForm"], item["lemma"], item["partOfSpeech"]
    ))
    return {
        "v": 1,
        "purpose": "linguistic-sense-runtime",
        "generator": GENERATOR,
        "targets": targets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    runtime = build_runtime()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(runtime, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    validated = sum(len(target["validated"]) for target in runtime["targets"])
    uncertain = sum(len(target["uncertain"]) for target in runtime["targets"])
    print(
        f"LINGUISTIC_SENSE_RUNTIME_BUILD = PASS · "
        f"{len(runtime['targets'])} target(s) · "
        f"{validated} validated · {uncertain} uncertain"
    )


if __name__ == "__main__":
    main()
