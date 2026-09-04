#!/usr/bin/env python3
"""Validate Michaël book 17 records after deterministic PDF extraction.

Machine-detectable structural errors remain validation failures. Editorial cases
that cannot be decided safely are also written to data/incoherences.json so they
can be reviewed later without forcing a guess into the corpus.
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
INCOHERENCE_PATH = DATA / "incoherences.json"
METHOD = "automated-structural-and-source-consistency-v1"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def ambiguity_id(psalm: int, kind: str, verse: int | None = None) -> str:
    suffix = f"-verse-{verse:03d}" if verse is not None else ""
    return f"michael-book-17-psalm-{psalm:03d}-{kind}{suffix}"


def add_ambiguity(ambiguities: list[dict], psalm: int, kind: str, reason: str,
                  verse: dict | None = None, interpretation: str | None = None) -> None:
    number = verse.get("number") if verse else None
    entry = {
        "id": ambiguity_id(psalm, kind, number),
        "status": "open",
        "archangel": "michael",
        "book": 17,
        "psalm": psalm,
        "type": kind,
        "reason": reason,
        "detectedBy": METHOD,
    }
    if verse:
        entry.update({
            "verse": number,
            "text": verse.get("text", ""),
            "sourcePages": verse.get("sourcePages", []),
        })
    if interpretation:
        entry["machineInterpretation"] = interpretation
    ambiguities.append(entry)


def sync_incoherences(new_entries: list[dict]) -> None:
    registry = load(INCOHERENCE_PATH) if INCOHERENCE_PATH.exists() else {
        "schemaVersion": 1,
        "purpose": "Registre permanent des cas éditoriaux réellement ambigus nécessitant une vérification humaine.",
        "statuses": ["open", "resolved"],
        "entries": [],
    }
    existing = {e.get("id"): e for e in registry.get("entries", [])}
    detected_ids = {e["id"] for e in new_entries}
    for entry in new_entries:
        old = existing.get(entry["id"])
        if old and old.get("status") == "resolved":
            entry["status"] = "resolved"
            if "resolution" in old:
                entry["resolution"] = old["resolution"]
        existing[entry["id"]] = entry
    # Never delete historical decisions. Open machine-generated entries that are
    # no longer detected are marked resolved automatically with an audit note.
    for eid, old in existing.items():
        if eid not in detected_ids and old.get("status") == "open" and old.get("detectedBy") == METHOD:
            old["status"] = "resolved"
            old["resolution"] = "No longer detected by the current validation rules."
    registry["entries"] = sorted(existing.values(), key=lambda e: (e.get("archangel", ""), e.get("book", 0), e.get("psalm", 0), e.get("verse") or 0, e.get("id", "")))
    write(INCOHERENCE_PATH, registry)


def validate_psalm(expected: dict, apply: bool, ambiguities: list[dict]) -> dict:
    number = expected["psalm"]
    psalm_id = f"michael-psalm-{number:03d}"
    path = DATA / "corpus" / "michael" / f"psalm-{number:03d}.json"
    errors: list[str] = []

    if not path.exists():
        return {"psalm": number, "status": "failed", "errors": [f"missing {path.relative_to(ROOT)}"]}

    record = load(path)
    if record.get("id") != psalm_id: fail(errors, f"id mismatch: {record.get('id')!r}")
    if record.get("recordType") != "psalm": fail(errors, "recordType is not psalm")
    if record.get("archangel") != "michael": fail(errors, "archangel is not michael")
    if record.get("book", {}).get("number") != 17: fail(errors, "book number is not 17")
    if record.get("number") != number: fail(errors, f"psalm number mismatch: {record.get('number')!r}")

    verses = record.get("verses") or []
    verse_numbers = [v.get("number") for v in verses]
    expected_numbers = list(range(1, expected["verses"] + 1))
    if verse_numbers != expected_numbers: fail(errors, f"verse sequence mismatch: expected 1..{expected['verses']}")

    page_start, page_end = expected["pages"]
    printed_pages = record.get("source", {}).get("printedPages") or []
    if not printed_pages or printed_pages[0] != page_start or printed_pages[-1] != page_end:
        fail(errors, f"printed page range mismatch: expected {page_start}-{page_end}, got {printed_pages}")

    verse_by_number = {v.get("number"): v for v in verses}
    for verse in verses:
        n = verse.get("number")
        text = verse.get("text", "")
        if not isinstance(text, str) or not text.strip(): fail(errors, f"verse {n}: empty text")
        pages = verse.get("sourcePages") or []
        if not pages or any(not isinstance(p, int) or p < page_start or p > page_end for p in pages):
            fail(errors, f"verse {n}: invalid sourcePages {pages}")
        if verse.get("speechRole") == "question" and verse.get("speakerId") != "olivier-manitara":
            fail(errors, f"verse {n}: question not attributed to Olivier Manitara")
        # Do not guess on unresolved speaker semantics. A question attributed to
        # Michaël is allowed, but is recorded when it starts like a direct address.
        stripped = text.strip().lower()
        if "?" in text and verse.get("speakerId") == "archangel-michael" and (stripped.startswith("père") or stripped.startswith("ô père")):
            add_ambiguity(ambiguities, number, "speaker-attribution", "Interrogative direct address remains attributed to Michaël; human semantic review is useful.", verse, "archangel-michael")

    dialogues = record.get("dialogueSegments") or []
    if len(dialogues) != expected["questions"]: fail(errors, f"dialogue count mismatch: expected {expected['questions']}, got {len(dialogues)}")
    seen_dialogue_ids: set[str] = set()
    for dialogue in dialogues:
        did = dialogue.get("id")
        if not did or did in seen_dialogue_ids: fail(errors, f"invalid or duplicate dialogue id: {did!r}")
        seen_dialogue_ids.add(did)
        if dialogue.get("speakerId") != "olivier-manitara" or dialogue.get("speechRole") != "question": fail(errors, f"{did}: dialogue attribution/role mismatch")
        numbering = dialogue.get("numbering")
        if numbering == "numbered-verse":
            vn = dialogue.get("verseNumber"); verse = verse_by_number.get(vn)
            if not verse: fail(errors, f"{did}: referenced verse {vn} does not exist")
            else:
                if verse.get("speakerId") != "olivier-manitara" or verse.get("speechRole") != "question": fail(errors, f"{did}: referenced verse is not an Olivier question")
                if dialogue.get("text") != verse.get("text"): fail(errors, f"{did}: dialogue text differs from verse {vn}")
        elif numbering == "unnumbered-interlude":
            after = dialogue.get("positionAfterVerse"); before = dialogue.get("positionBeforeVerse")
            if after is not None and after not in verse_by_number: fail(errors, f"{did}: positionAfterVerse {after} does not exist")
            if before is not None and before not in verse_by_number: fail(errors, f"{did}: positionBeforeVerse {before} does not exist")
        else: fail(errors, f"{did}: unknown numbering {numbering!r}")

    note_ids = record.get("noteIds") or []
    if len(note_ids) != expected["notes"]: fail(errors, f"note count mismatch: expected {expected['notes']}, got {len(note_ids)}")
    for note_id in note_ids:
        note_path = DATA / "notes" / f"{note_id}.json"
        if not note_path.exists(): fail(errors, f"missing note {note_id}"); continue
        note = load(note_path)
        if note.get("id") != note_id: fail(errors, f"note id mismatch in {note_id}")
        if note.get("appliesTo", {}).get("recordId") != psalm_id: fail(errors, f"{note_id}: appliesTo.recordId mismatch")
        if not str(note.get("text", "")).strip(): fail(errors, f"{note_id}: empty note text")

    expected_prayer = expected.get("prayer"); prayer_ids = record.get("prayerIds") or []
    if expected_prayer is None:
        if prayer_ids: fail(errors, f"unexpected prayers: {prayer_ids}")
    else:
        expected_prayer_id = f"michael-book-17-prayer-{expected_prayer:03d}"
        if prayer_ids != [expected_prayer_id]: fail(errors, f"prayerIds mismatch: expected [{expected_prayer_id!r}], got {prayer_ids}")
        prayer_path = DATA / "prayers" / f"{expected_prayer_id}.json"
        if not prayer_path.exists(): fail(errors, f"missing prayer {expected_prayer_id}")
        else:
            prayer = load(prayer_path)
            if prayer.get("id") != expected_prayer_id: fail(errors, f"{expected_prayer_id}: id mismatch")
            if prayer.get("number") != expected_prayer: fail(errors, f"{expected_prayer_id}: number mismatch")
            if prayer.get("appliesToPsalmId") != psalm_id: fail(errors, f"{expected_prayer_id}: appliesToPsalmId mismatch")
            if not str(prayer.get("text", "")).strip(): fail(errors, f"{expected_prayer_id}: empty prayer text")

    status = "passed" if not errors else "failed"
    if apply and not errors:
        validation = record.setdefault("validation", {})
        if validation.get("status") != "validated":
            validation.update({"status": "machine-validated", "validatedOn": date.today().isoformat(), "method": METHOD})
            validation.setdefault("checks", {}).update({"verseSequenceComplete": True, "verseCountMatchesExtractionReport": True, "sourcePageRangeMatchesExtractionReport": True, "dialogueRelationsConsistent": True, "noteRelationsConsistent": True, "prayerRelationsConsistent": True})
            write(path, record)
        for note_id in note_ids:
            note_path = DATA / "notes" / f"{note_id}.json"; note = load(note_path)
            if note.get("validation", {}).get("status") != "validated":
                note.setdefault("validation", {}).update({"status": "machine-validated", "validatedOn": date.today().isoformat(), "method": METHOD}); write(note_path, note)
        for prayer_id in prayer_ids:
            prayer_path = DATA / "prayers" / f"{prayer_id}.json"; prayer = load(prayer_path)
            if prayer.get("validation", {}).get("status") != "validated":
                prayer.setdefault("validation", {}).update({"status": "machine-validated", "validatedOn": date.today().isoformat(), "method": METHOD}); write(prayer_path, prayer)
    return {"psalm": number, "status": status, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--apply", action="store_true"); args = parser.parse_args()
    report = load(REPORT_PATH); results = []; ambiguities: list[dict] = []
    for expected in report.get("records", []):
        if expected.get("psalm") == 105:
            results.append({"psalm": 105, "status": "human-reference", "errors": []}); continue
        results.append(validate_psalm(expected, args.apply, ambiguities))
    failed = [r for r in results if r["status"] == "failed"]
    validation_report = {"book": 17, "archangel": "michael", "method": METHOD, "applied": args.apply, "status": "passed" if not failed else "exceptions-found", "humanReferencePsalm": 105, "machineValidatedPsalms": [r["psalm"] for r in results if r["status"] == "passed"], "exceptions": failed, "editorialAmbiguities": [e["id"] for e in ambiguities], "results": results}
    write(VALIDATION_REPORT_PATH, validation_report)
    if args.apply:
        sync_incoherences(ambiguities)
        report["validation"] = {"method": METHOD, "status": "machine-validated" if not failed else "exceptions-found", "humanReferencePsalm": 105, "machineValidatedPsalms": validation_report["machineValidatedPsalms"], "exceptions": [r["psalm"] for r in failed], "editorialAmbiguities": validation_report["editorialAmbiguities"]}; write(REPORT_PATH, report)
    print(json.dumps(validation_report, ensure_ascii=False, indent=2)); return 1 if failed else 0

if __name__ == "__main__": raise SystemExit(main())
