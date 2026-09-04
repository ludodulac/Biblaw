#!/usr/bin/env python3
"""Validate Michaël book 17 records after deterministic PDF extraction.

This script does not replace prior human validations. It verifies that the
machine-generated records are internally consistent with the extraction report,
relations, dialogue rules, notes and prayers, then marks passing records as
`machine-validated` when --apply is used.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT_PATH = DATA / "pilot" / "book-17-extraction-report.json"
VALIDATION_REPORT_PATH = DATA / "pilot" / "book-17-validation-report.json"
METHOD = "automated-structural-and-source-consistency-v1"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_psalm(expected: dict, apply: bool) -> dict:
    number = expected["psalm"]
    psalm_id = f"michael-psalm-{number:03d}"
    path = DATA / "corpus" / "michael" / f"psalm-{number:03d}.json"
    errors: list[str] = []

    if not path.exists():
        return {"psalm": number, "status": "failed", "errors": [f"missing {path.relative_to(ROOT)}"]}

    record = load(path)
    if record.get("id") != psalm_id:
        fail(errors, f"id mismatch: {record.get('id')!r}")
    if record.get("recordType") != "psalm":
        fail(errors, "recordType is not psalm")
    if record.get("archangel") != "michael":
        fail(errors, "archangel is not michael")
    if record.get("book", {}).get("number") != 17:
        fail(errors, "book number is not 17")
    if record.get("number") != number:
        fail(errors, f"psalm number mismatch: {record.get('number')!r}")

    verses = record.get("verses") or []
    verse_numbers = [v.get("number") for v in verses]
    expected_numbers = list(range(1, expected["verses"] + 1))
    if verse_numbers != expected_numbers:
        fail(errors, f"verse sequence mismatch: expected 1..{expected['verses']}")

    page_start, page_end = expected["pages"]
    printed_pages = record.get("source", {}).get("printedPages") or []
    if not printed_pages or printed_pages[0] != page_start or printed_pages[-1] != page_end:
        fail(errors, f"printed page range mismatch: expected {page_start}-{page_end}, got {printed_pages}")

    verse_by_number = {v.get("number"): v for v in verses}
    for verse in verses:
        n = verse.get("number")
        if not isinstance(verse.get("text"), str) or not verse["text"].strip():
            fail(errors, f"verse {n}: empty text")
        pages = verse.get("sourcePages") or []
        if not pages or any(not isinstance(p, int) or p < page_start or p > page_end for p in pages):
            fail(errors, f"verse {n}: invalid sourcePages {pages}")
        if verse.get("speechRole") == "question" and verse.get("speakerId") != "olivier-manitara":
            fail(errors, f"verse {n}: question not attributed to Olivier Manitara")

    dialogues = record.get("dialogueSegments") or []
    if len(dialogues) != expected["questions"]:
        fail(errors, f"dialogue count mismatch: expected {expected['questions']}, got {len(dialogues)}")
    seen_dialogue_ids: set[str] = set()
    for dialogue in dialogues:
        did = dialogue.get("id")
        if not did or did in seen_dialogue_ids:
            fail(errors, f"invalid or duplicate dialogue id: {did!r}")
        seen_dialogue_ids.add(did)
        if dialogue.get("speakerId") != "olivier-manitara" or dialogue.get("speechRole") != "question":
            fail(errors, f"{did}: dialogue attribution/role mismatch")
        numbering = dialogue.get("numbering")
        if numbering == "numbered-verse":
            vn = dialogue.get("verseNumber")
            verse = verse_by_number.get(vn)
            if not verse:
                fail(errors, f"{did}: referenced verse {vn} does not exist")
            else:
                if verse.get("speakerId") != "olivier-manitara" or verse.get("speechRole") != "question":
                    fail(errors, f"{did}: referenced verse is not an Olivier question")
                if dialogue.get("text") != verse.get("text"):
                    fail(errors, f"{did}: dialogue text differs from verse {vn}")
        elif numbering == "unnumbered-interlude":
            after = dialogue.get("positionAfterVerse")
            before = dialogue.get("positionBeforeVerse")
            if after is not None and after not in verse_by_number:
                fail(errors, f"{did}: positionAfterVerse {after} does not exist")
            if before is not None and before not in verse_by_number:
                fail(errors, f"{did}: positionBeforeVerse {before} does not exist")
        else:
            fail(errors, f"{did}: unknown numbering {numbering!r}")

    note_ids = record.get("noteIds") or []
    if len(note_ids) != expected["notes"]:
        fail(errors, f"note count mismatch: expected {expected['notes']}, got {len(note_ids)}")
    for note_id in note_ids:
        note_path = DATA / "notes" / f"{note_id}.json"
        if not note_path.exists():
            fail(errors, f"missing note {note_id}")
            continue
        note = load(note_path)
        if note.get("id") != note_id:
            fail(errors, f"note id mismatch in {note_id}")
        if note.get("appliesTo", {}).get("recordId") != psalm_id:
            fail(errors, f"{note_id}: appliesTo.recordId mismatch")
        if not str(note.get("text", "")).strip():
            fail(errors, f"{note_id}: empty note text")

    expected_prayer = expected.get("prayer")
    prayer_ids = record.get("prayerIds") or []
    if expected_prayer is None:
        if prayer_ids:
            fail(errors, f"unexpected prayers: {prayer_ids}")
    else:
        expected_prayer_id = f"michael-book-17-prayer-{expected_prayer:03d}"
        if prayer_ids != [expected_prayer_id]:
            fail(errors, f"prayerIds mismatch: expected [{expected_prayer_id!r}], got {prayer_ids}")
        prayer_path = DATA / "prayers" / f"{expected_prayer_id}.json"
        if not prayer_path.exists():
            fail(errors, f"missing prayer {expected_prayer_id}")
        else:
            prayer = load(prayer_path)
            if prayer.get("id") != expected_prayer_id:
                fail(errors, f"{expected_prayer_id}: id mismatch")
            if prayer.get("number") != expected_prayer:
                fail(errors, f"{expected_prayer_id}: number mismatch")
            if prayer.get("appliesToPsalmId") != psalm_id:
                fail(errors, f"{expected_prayer_id}: appliesToPsalmId mismatch")
            if not str(prayer.get("text", "")).strip():
                fail(errors, f"{expected_prayer_id}: empty prayer text")

    status = "passed" if not errors else "failed"
    if apply and not errors:
        validation = record.setdefault("validation", {})
        if validation.get("status") != "validated":
            validation["status"] = "machine-validated"
            validation["validatedOn"] = date.today().isoformat()
            validation["method"] = METHOD
            checks = validation.setdefault("checks", {})
            checks.update({
                "verseSequenceComplete": True,
                "verseCountMatchesExtractionReport": True,
                "sourcePageRangeMatchesExtractionReport": True,
                "dialogueRelationsConsistent": True,
                "noteRelationsConsistent": True,
                "prayerRelationsConsistent": True,
            })
            write(path, record)

        for note_id in note_ids:
            note_path = DATA / "notes" / f"{note_id}.json"
            note = load(note_path)
            if note.get("validation", {}).get("status") != "validated":
                note.setdefault("validation", {}).update({
                    "status": "machine-validated",
                    "validatedOn": date.today().isoformat(),
                    "method": METHOD,
                })
                write(note_path, note)

        for prayer_id in prayer_ids:
            prayer_path = DATA / "prayers" / f"{prayer_id}.json"
            prayer = load(prayer_path)
            if prayer.get("validation", {}).get("status") != "validated":
                prayer.setdefault("validation", {}).update({
                    "status": "machine-validated",
                    "validatedOn": date.today().isoformat(),
                    "method": METHOD,
                })
                write(prayer_path, prayer)

    return {"psalm": number, "status": status, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write machine-validated status to passing records")
    args = parser.parse_args()

    report = load(REPORT_PATH)
    results = []
    for expected in report.get("records", []):
        if expected.get("psalm") == 105:
            # Human-validated reference record: never rewritten by this validator.
            results.append({"psalm": 105, "status": "human-reference", "errors": []})
            continue
        results.append(validate_psalm(expected, args.apply))

    failed = [r for r in results if r["status"] == "failed"]
    validation_report = {
        "book": 17,
        "archangel": "michael",
        "method": METHOD,
        "applied": args.apply,
        "status": "passed" if not failed else "exceptions-found",
        "humanReferencePsalm": 105,
        "machineValidatedPsalms": [r["psalm"] for r in results if r["status"] == "passed"],
        "exceptions": failed,
        "results": results,
    }
    write(VALIDATION_REPORT_PATH, validation_report)

    if args.apply:
        report["validation"] = {
            "method": METHOD,
            "status": "machine-validated" if not failed else "exceptions-found",
            "humanReferencePsalm": 105,
            "machineValidatedPsalms": validation_report["machineValidatedPsalms"],
            "exceptions": [r["psalm"] for r in failed],
        }
        write(REPORT_PATH, report)

    print(json.dumps(validation_report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
