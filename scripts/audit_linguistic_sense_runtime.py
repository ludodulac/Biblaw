#!/usr/bin/env python3
from __future__ import annotations

from audit_linguistic_sense_contract import load_json
from build_linguistic_sense_runtime import DEFAULT_OUTPUT, build_runtime

FORBIDDEN_KEYS = {
    "context", "contextExcerpt", "phrase", "text", "modelText",
    "spacy", "stanza", "reason", "reasoning", "comment", "comments",
    "definition",
}


def _forbidden_key_present(value) -> bool:
    if isinstance(value, dict):
        if set(value) & FORBIDDEN_KEYS:
            return True
        return any(_forbidden_key_present(item) for item in value.values())
    if isinstance(value, list):
        return any(_forbidden_key_present(item) for item in value)
    return False


def validate_runtime_shape(runtime: dict) -> None:
    assert set(runtime) == {"v", "purpose", "generator", "targets"}
    assert runtime["v"] == 1
    assert runtime["purpose"] == "linguistic-sense-runtime"
    assert runtime["generator"] == "scripts/build_linguistic_sense_runtime.py"
    assert isinstance(runtime["targets"], list)

    target_keys: set[tuple[str, str, str]] = set()
    occurrence_ids: set[str] = set()
    expected_target_order: list[tuple[str, str, str]] = []

    for target in runtime["targets"]:
        assert set(target) == {
            "normalizedForm", "lemma", "partOfSpeech", "senses", "validated", "uncertain"
        }
        key = (target["normalizedForm"], target["lemma"], target["partOfSpeech"])
        assert key not in target_keys, f"DUPLICATE_SEMANTIC_RUNTIME_TARGET: {key}"
        target_keys.add(key)
        expected_target_order.append(key)

        assert isinstance(target["senses"], list) and target["senses"]
        sense_ids: set[str] = set()
        for sense in target["senses"]:
            assert set(sense) == {"senseId", "label"}
            sense_id = sense["senseId"]
            assert isinstance(sense_id, str) and sense_id
            assert sense_id != "UNCERTAIN"
            assert sense_id not in sense_ids
            assert isinstance(sense["label"], str) and sense["label"]
            sense_ids.add(sense_id)

        validated_ids: list[str] = []
        for item in target["validated"]:
            assert isinstance(item, list) and len(item) == 2
            occurrence_id, sense_id = item
            assert isinstance(occurrence_id, str) and occurrence_id
            assert isinstance(sense_id, str) and sense_id in sense_ids
            assert occurrence_id not in occurrence_ids, f"DUPLICATE_RUNTIME_OCCURRENCE_ID: {occurrence_id}"
            occurrence_ids.add(occurrence_id)
            validated_ids.append(occurrence_id)
        assert validated_ids == sorted(validated_ids)

        assert isinstance(target["uncertain"], list)
        assert target["uncertain"] == sorted(target["uncertain"])
        for occurrence_id in target["uncertain"]:
            assert isinstance(occurrence_id, str) and occurrence_id
            assert occurrence_id not in occurrence_ids, f"DUPLICATE_RUNTIME_OCCURRENCE_ID: {occurrence_id}"
            occurrence_ids.add(occurrence_id)

    assert expected_target_order == sorted(expected_target_order)
    assert not _forbidden_key_present(runtime), "runtime contains forbidden contextual/textual data"


def main() -> None:
    expected = build_runtime()
    actual = load_json(DEFAULT_OUTPUT)
    assert actual == expected, "runtime differs from deterministic reconstruction"
    validate_runtime_shape(actual)
    validated = sum(len(target["validated"]) for target in actual["targets"])
    uncertain = sum(len(target["uncertain"]) for target in actual["targets"])
    print(
        f"LINGUISTIC_SENSE_RUNTIME_AUDIT = PASS · "
        f"{len(actual['targets'])} target(s) · "
        f"{validated} validated · {uncertain} uncertain"
    )


if __name__ == "__main__":
    main()
