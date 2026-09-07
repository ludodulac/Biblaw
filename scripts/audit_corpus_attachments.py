#!/usr/bin/env python3
"""Audit canonical prayer/note attachments against canonical Psalm records.

This is a permanent integrity contract, not a migration helper. All catalogued prayer/note targets
must already use canonical `book-XX-psalm-NNN` ids. External relationships must be reciprocal and
supported by the same source document with overlapping or immediately adjacent printed/PDF pages.
A Psalm may also carry `noteIds` for embedded/editorial footnotes that have no standalone
`data/notes/*.json` record; those internal identifiers are not required to exist in the catalog.
No semantic inference or external source is used.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog.json"
CANONICAL_ROOT = ROOT / "data/corpus/books"
CANONICAL_PSALM_RE = re.compile(r"^book-\d{2}-psalm-\d+$")
LEGACY_PSALM_RE = re.compile(r"^(?:michael|gabriel|raphael|ouriel)-psalm-\d+$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def pages(obj: dict) -> set[int]:
    source = obj.get("source") or {}
    raw = source.get("pdfPages") or source.get("printedPages") or source.get("printedPage") or []
    if isinstance(raw, int):
        raw = [raw]
    result = set()
    for value in raw:
        try:
            result.add(int(value))
        except (TypeError, ValueError):
            pass
    return result


def same_document(a: dict, b: dict) -> bool:
    a_doc = (a.get("source") or {}).get("document")
    b_doc = (b.get("source") or {}).get("document")
    return bool(a_doc) and a_doc == b_doc


def source_connected(child: dict, psalm: dict) -> bool:
    child_pages, psalm_pages = pages(child), pages(psalm)
    if not child_pages or not psalm_pages or not same_document(child, psalm):
        return False
    return bool(child_pages & psalm_pages) or min(child_pages) - max(psalm_pages) == 1


canonical_by_id: dict[str, dict] = {}
for path in sorted(CANONICAL_ROOT.glob("book-*/psalm-*.json")):
    obj = load(path)
    if obj.get("recordType") != "psalm":
        continue
    psalm_id = str(obj.get("id") or "")
    if not CANONICAL_PSALM_RE.match(psalm_id):
        raise SystemExit(f"Non-canonical Psalm id in canonical tree: {path.relative_to(ROOT)} -> {psalm_id}")
    if psalm_id in canonical_by_id:
        raise SystemExit(f"Duplicate canonical Psalm id: {psalm_id}")
    canonical_by_id[psalm_id] = obj

catalog = load(CATALOG)
records = list(catalog.get("records", []))
if len(records) != len(set(records)):
    raise SystemExit("Duplicate paths in data/catalog.json")

prayer_rels = [rel for rel in records if rel.startswith("data/prayers/")]
note_rels = [rel for rel in records if rel.startswith("data/notes/")]
errors: list[str] = []
prayer_targets: set[str] = set()
note_targets: set[str] = set()
prayer_ids: set[str] = set()
external_note_ids: set[str] = set()

for rel in prayer_rels:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"catalog prayer path missing: {rel}")
        continue
    prayer = load(path)
    if prayer.get("recordType") != "master-prayer":
        errors.append(f"{rel} is not recordType master-prayer")
        continue
    prayer_id = str(prayer.get("id") or "")
    prayer_ids.add(prayer_id)
    if path.stem != prayer_id:
        errors.append(f"prayer filename/id mismatch: {rel} != {prayer_id}")
    target_id = str(prayer.get("appliesToPsalmId") or "")
    if LEGACY_PSALM_RE.match(target_id):
        errors.append(f"prayer {prayer_id} still targets legacy Psalm {target_id}")
        continue
    target = canonical_by_id.get(target_id)
    if not target:
        errors.append(f"prayer {prayer_id} targets missing/non-canonical Psalm {target_id}")
        continue
    prayer_targets.add(target_id)
    if prayer.get("archangel") != target.get("archangel"):
        errors.append(f"prayer {prayer_id} archangel differs from {target_id}")
    if int(prayer.get("bookNumber", -1)) != int((target.get("book") or {}).get("number", -2)):
        errors.append(f"prayer {prayer_id} bookNumber differs from {target_id}")
    if prayer_id not in (target.get("prayerIds") or []):
        errors.append(f"prayer {prayer_id} lacks reciprocal prayerIds entry on {target_id}")
    if not source_connected(prayer, target):
        errors.append(f"prayer {prayer_id} source is not overlapping/adjacent to {target_id}")

for rel in note_rels:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"catalog note path missing: {rel}")
        continue
    note = load(path)
    if note.get("recordType") != "note":
        errors.append(f"{rel} is not recordType note")
        continue
    note_id = str(note.get("id") or "")
    external_note_ids.add(note_id)
    if path.stem != note_id:
        errors.append(f"note filename/id mismatch: {rel} != {note_id}")
    applies = note.get("appliesTo") or {}
    target_id = str(applies.get("recordId") or "")
    if LEGACY_PSALM_RE.match(target_id):
        errors.append(f"note {note_id} still targets legacy Psalm {target_id}")
        continue
    target = canonical_by_id.get(target_id)
    if not target:
        errors.append(f"note {note_id} targets missing/non-canonical Psalm {target_id}")
        continue
    note_targets.add(target_id)
    if note.get("archangel") != target.get("archangel"):
        errors.append(f"note {note_id} archangel differs from {target_id}")
    if note_id not in (target.get("noteIds") or []):
        errors.append(f"external note {note_id} lacks reciprocal noteIds entry on {target_id}")
    if not source_connected(note, target):
        errors.append(f"note {note_id} source is not overlapping/adjacent to {target_id}")
    verse = applies.get("verse")
    if verse is not None:
        verse_numbers = {int(v["number"]) for v in target.get("verses", []) if v.get("number") is not None}
        try:
            verse_number = int(verse)
        except (TypeError, ValueError):
            errors.append(f"note {note_id} has invalid verse reference {verse!r}")
        else:
            if verse_number not in verse_numbers:
                errors.append(f"note {note_id} references missing verse {verse_number} on {target_id}")

# Prayer records are always standalone catalog objects, so every reciprocal Psalm prayerId must resolve.
# Psalm noteIds are intentionally different: many identify embedded/editorial footnotes and therefore
# do not need a standalone catalog record. Only external notes are checked in the forward direction above.
for psalm_id, psalm in canonical_by_id.items():
    for prayer_id in psalm.get("prayerIds") or []:
        if prayer_id not in prayer_ids:
            errors.append(f"{psalm_id} references missing/catalog-external prayer {prayer_id}")

embedded_note_id_count = sum(
    1
    for psalm in canonical_by_id.values()
    for note_id in (psalm.get("noteIds") or [])
    if note_id not in external_note_ids
)

print(
    f"ATTACHMENTS canonicalPsalms={len(canonical_by_id)} prayers={len(prayer_rels)} "
    f"prayerTargets={len(prayer_targets)} externalNotes={len(note_rels)} "
    f"externalNoteTargets={len(note_targets)} embeddedNoteIds={embedded_note_id_count}"
)

if errors:
    raise SystemExit("Attachment audit failed:\n- " + "\n- ".join(errors))

print("Corpus attachment audit OK: catalogued prayer/note targets canonical and reciprocal")
