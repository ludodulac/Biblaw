#!/usr/bin/env python3
from __future__ import annotations

from build_linguistic_sense_browser_runtime import (
    DEFAULT_OUTPUT,
    SEMANTIC_RUNTIME,
    build_browser_runtime,
    load_json,
)

FORBIDDEN_KEYS = {
    "context", "contextExcerpt", "phrase", "text", "modelText",
    "spacy", "stanza", "reason", "reasoning", "comment", "comments",
    "definition",
}


def forbidden_key_present(value) -> bool:
    if isinstance(value, dict):
        if set(value) & FORBIDDEN_KEYS:
            return True
        return any(forbidden_key_present(item) for item in value.values())
    if isinstance(value, list):
        return any(forbidden_key_present(item) for item in value)
    return False


def main() -> None:
    source = load_json(SEMANTIC_RUNTIME)
    expected = build_browser_runtime()
    actual = load_json(DEFAULT_OUTPUT)
    assert actual == expected, "browser runtime differs from deterministic reconstruction"
    assert actual.get("v") == 1
    assert actual.get("purpose") == "linguistic-sense-browser-runtime"
    assert not forbidden_key_present(actual), "browser runtime contains forbidden contextual/textual data"

    source_targets = {
        (target["normalizedForm"], target["lemma"], target["partOfSpeech"]): target
        for target in source["targets"]
    }
    seen_occurrences: set[str] = set()

    for target in actual["targets"]:
        key = (target["normalizedForm"], target["lemma"], target["partOfSpeech"])
        source_target = source_targets[key]
        source_counts = {sense["senseId"]: 0 for sense in source_target["senses"]}

        for occurrence_id, sense_id in source_target["validated"]:
            assert occurrence_id not in seen_occurrences
            seen_occurrences.add(occurrence_id)
            source_counts[sense_id] += 1

        for occurrence_id in source_target["uncertain"]:
            assert occurrence_id not in seen_occurrences
            seen_occurrences.add(occurrence_id)

        assert target["uncertainOccurrenceCount"] == len(source_target["uncertain"])
        runtime_sense_ids = {sense["senseId"] for sense in target["senses"]}
        assert "UNCERTAIN" not in runtime_sense_ids

        for sense in target["senses"]:
            sense_id = sense["senseId"]
            assert sense_id in source_counts
            assert sense["occurrenceCount"] == source_counts[sense_id]
            assert sum(record[1] for record in sense["records"]) == sense["occurrenceCount"]

            record_ids = []
            for record_id, occurrence_count, verse_numbers in sense["records"]:
                assert isinstance(record_id, str) and record_id
                assert isinstance(occurrence_count, int) and occurrence_count > 0
                assert verse_numbers == sorted(set(verse_numbers))
                record_ids.append(record_id)
            assert record_ids == sorted(record_ids)

    source_total = sum(
        len(target["validated"]) + len(target["uncertain"])
        for target in source["targets"]
    )
    assert len(seen_occurrences) == source_total
    print("LINGUISTIC_SENSE_BROWSER_RUNTIME_AUDIT = PASS")


if __name__ == "__main__":
    main()
