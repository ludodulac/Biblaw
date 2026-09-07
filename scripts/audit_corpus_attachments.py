#!/usr/bin/env python3
"""Audit prayer/note attachments against canonical Psalm records.

The audit is conservative: it never infers a canonical note target from a Psalm number alone.
Legacy note targets are accepted as migration candidates only when one canonical Psalm matches
all available internal evidence: archangel + Psalm number, reciprocal canonical noteId,
source-page overlap, and (when present) the referenced verse.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog.json"
CANONICAL_ROOT = ROOT / "data/corpus/books"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def pages(obj: dict) -> set[int]:
    source = obj.get("source") or {}
    raw = source.get("pdfPages") or source.get("printedPages") or source.get("printedPage") or []
    if isinstance(raw, int):
        raw = [raw]
    return {int(value) for value in raw if str(value).isdigit()}


canonical_psalms = []
for path in sorted(CANONICAL_ROOT.glob("book-*/psalm-*.json")):
    obj = load(path)
    if obj.get("recordType") == "psalm":
        canonical_psalms.append(obj)

canonical_by_id = {p["id"]: p for p in canonical_psalms}
assert len(canonical_by_id) == len(canonical_psalms), "duplicate canonical Psalm ids"

catalog = load(CATALOG)
record_paths = [ROOT / rel for rel in catalog.get("records", [])]
prayer_paths = [p for p in record_paths if "/prayers/" in p.as_posix()]
note_paths = [p for p in record_paths if "/notes/" in p.as_posix()]

errors = []
legacy_note_migrations = []
canonical_note_targets = 0
prayer_targets = 0

for path in prayer_paths:
    prayer = load(path)
    if prayer.get("recordType") != "master-prayer":
        continue
    target_id = prayer.get("appliesToPsalmId")
    target = canonical_by_id.get(target_id)
    if not target:
        errors.append(f"prayer {prayer.get('id')} targets non-canonical/missing Psalm {target_id}")
        continue
    prayer_targets += 1
    if prayer.get("id") not in (target.get("prayerIds") or []):
        errors.append(f"prayer {prayer.get('id')} lacks reciprocal prayerIds entry on {target_id}")
    if pages(prayer) and pages(target) and not (pages(prayer) & pages(target)):
        errors.append(f"prayer {prayer.get('id')} has no source-page overlap with {target_id}")

legacy_re = re.compile(r"^(michael|gabriel|raphael|ouriel)-psalm-(\d+)$")
note_suffix_re = re.compile(r"-note-(\d+)$")

for path in note_paths:
    note = load(path)
    if note.get("recordType") != "note":
        continue
    applies = note.get("appliesTo") or {}
    target_id = applies.get("recordId")
    verse = applies.get("verse")

    if target_id in canonical_by_id:
        canonical_note_targets += 1
        target = canonical_by_id[target_id]
        if verse is not None and int(verse) not in {int(v.get("number")) for v in target.get("verses", []) if v.get("number") is not None}:
            errors.append(f"note {note.get('id')} references missing verse {verse} on {target_id}")
        continue

    match = legacy_re.match(str(target_id or ""))
    suffix_match = note_suffix_re.search(str(note.get("id") or ""))
    if not match or not suffix_match:
        errors.append(f"note {note.get('id')} has unsupported non-canonical target {target_id}")
        continue

    archangel, number_text = match.groups()
    number = int(number_text)
    suffix = suffix_match.group(1)
    candidates = []
    for psalm in canonical_psalms:
        if psalm.get("archangel") != archangel or int(psalm.get("number", -1)) != number:
            continue
        expected_note_id = f"{psalm['id']}-note-{suffix}"
        reciprocal = expected_note_id in (psalm.get("noteIds") or [])
        overlap = bool(pages(note) & pages(psalm)) if pages(note) and pages(psalm) else False
        verse_ok = verse is None or int(verse) in {int(v.get("number")) for v in psalm.get("verses", []) if v.get("number") is not None}
        if reciprocal and overlap and verse_ok:
            candidates.append((psalm, expected_note_id))

    if len(candidates) != 1:
        errors.append(
            f"note {note.get('id')} legacy target {target_id} has {len(candidates)} fully evidenced canonical candidates"
        )
        continue

    psalm, canonical_note_id = candidates[0]
    legacy_note_migrations.append({
        "path": str(path.relative_to(ROOT)),
        "oldNoteId": note.get("id"),
        "newNoteId": canonical_note_id,
        "oldTargetId": target_id,
        "newTargetId": psalm["id"],
        "verse": verse,
        "sourcePageOverlap": sorted(pages(note) & pages(psalm)),
    })

print(
    f"ATTACHMENTS canonicalPsalms={len(canonical_psalms)} prayers={len(prayer_paths)} "
    f"prayerCanonicalTargets={prayer_targets} notes={len(note_paths)} "
    f"canonicalNoteTargets={canonical_note_targets} legacyNoteMigrations={len(legacy_note_migrations)}"
)
for item in legacy_note_migrations:
    print(
        f"NOTE_MIGRATION {item['oldNoteId']} -> {item['newNoteId']} | "
        f"{item['oldTargetId']} -> {item['newTargetId']} | pages={item['sourcePageOverlap']}"
    )

if errors:
    raise SystemExit("Attachment audit failed:\n- " + "\n- ".join(errors))

print("Corpus attachment audit OK")
