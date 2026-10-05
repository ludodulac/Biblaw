#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "linguistic" / "sense-catalog.json"
DEFAULT_GOLD_GLOB = "*-sense-gold.json"
ALLOWED_STATUSES = {"VALIDATED", "UNCERTAIN"}
FORBIDDEN_ENTRY_KEYS = {
    "context", "contextExcerpt", "phrase", "modelText",
    "spacy", "stanza", "reason", "reasoning", "comment", "comments",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: top-level JSON must be an object")
    return value


def validate_catalog(catalog: dict) -> dict[tuple[str, str], set[str]]:
    assert catalog.get("schemaVersion") == 1
    assert catalog.get("purpose") == "linguistic-possible-senses"
    entries = catalog.get("entries")
    assert isinstance(entries, list) and entries

    index: dict[tuple[str, str], set[str]] = {}
    for entry in entries:
        assert isinstance(entry, dict)
        lemma = entry.get("lemma")
        pos = entry.get("partOfSpeech")
        assert isinstance(lemma, str) and lemma.strip()
        assert isinstance(pos, str) and pos.strip()
        key = (lemma, pos)
        assert key not in index, f"duplicate catalog target: {key}"

        policy = entry.get("decisionPolicy")
        assert isinstance(policy, str) and policy.strip()

        senses = entry.get("senses")
        assert isinstance(senses, list) and senses
        sense_ids: set[str] = set()
        for sense in senses:
            assert isinstance(sense, dict)
            sense_id = sense.get("senseId")
            label = sense.get("label")
            definition = sense.get("definition")
            assert isinstance(sense_id, str) and sense_id.strip()
            assert sense_id not in sense_ids, f"duplicate senseId in {key}: {sense_id}"
            assert isinstance(label, str) and label.strip()
            assert isinstance(definition, str) and definition.strip()
            sense_ids.add(sense_id)
        index[key] = sense_ids
    return index


def validate_gold(gold: dict, catalog_index: dict[tuple[str, str], set[str]], source: str) -> None:
    assert gold.get("schemaVersion") == 1
    assert gold.get("purpose") == "human-validated-occurrence-sense-gold"

    provenance = gold.get("provenance")
    assert isinstance(provenance, dict)
    assert provenance.get("validationType") == "human-audited"
    assert provenance.get("status") == "VALIDATED"

    target = gold.get("target")
    assert isinstance(target, dict)
    lemma = target.get("lemma")
    pos = target.get("partOfSpeech")
    assert isinstance(lemma, str) and lemma.strip()
    assert isinstance(pos, str) and pos.strip()
    target_key = (lemma, pos)
    assert target_key in catalog_index, f"{source}: target missing from sense catalog"
    catalog_senses = catalog_index[target_key]

    entries = gold.get("entries")
    assert isinstance(entries, list) and entries
    occurrence_ids: list[str] = []
    recalculated = Counter({sense_id: 0 for sense_id in catalog_senses})
    recalculated["UNCERTAIN"] = 0

    for entry in entries:
        assert isinstance(entry, dict)
        assert set(entry) == {"occurrenceId", "adjudicationStatus", "senseId"}, (
            f"{source}: gold entries must contain only occurrenceId, adjudicationStatus, senseId"
        )
        assert not (set(entry) & FORBIDDEN_ENTRY_KEYS)

        occurrence_id = entry.get("occurrenceId")
        status = entry.get("adjudicationStatus")
        sense_id = entry.get("senseId")
        assert isinstance(occurrence_id, str) and occurrence_id.strip()
        assert status in ALLOWED_STATUSES
        occurrence_ids.append(occurrence_id)

        if status == "VALIDATED":
            assert isinstance(sense_id, str) and sense_id in catalog_senses
            recalculated[sense_id] += 1
        else:
            assert sense_id is None
            recalculated["UNCERTAIN"] += 1

    assert len(occurrence_ids) == len(set(occurrence_ids)), f"{source}: duplicate occurrenceId"
    assert occurrence_ids == sorted(occurrence_ids), f"{source}: entries are not lexically sorted"

    stored_counts = gold.get("counts")
    assert isinstance(stored_counts, dict)
    assert stored_counts == dict(recalculated), (
        f"{source}: counts mismatch stored={stored_counts} recalculated={dict(recalculated)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--gold", type=Path, action="append")
    args = parser.parse_args()

    catalog = load_json(args.catalog)
    catalog_index = validate_catalog(catalog)

    gold_paths = args.gold
    if gold_paths is None:
        gold_paths = sorted((ROOT / "data" / "linguistic" / "gold").glob(DEFAULT_GOLD_GLOB))
    assert gold_paths, "no semantic gold files found"

    for path in gold_paths:
        validate_gold(load_json(path), catalog_index, str(path))

    total_senses = sum(len(v) for v in catalog_index.values())
    print(
        f"LINGUISTIC_SENSE_CONTRACT = PASS · "
        f"{len(catalog_index)} catalog target(s) · {total_senses} sense(s) · "
        f"{len(gold_paths)} gold file(s)"
    )


if __name__ == "__main__":
    main()
