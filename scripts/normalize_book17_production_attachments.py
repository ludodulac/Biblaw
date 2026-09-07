#!/usr/bin/env python3
"""Normalize Book 17 pilot attachments at the production boundary.

The historical Book 17 extractor intentionally writes legacy `michael-psalm-NNN`
records under `data/corpus/michael/` for its pilot validation workflow. Those
legacy Psalm records are retained. Shared production attachments, however, must
refer to canonical `book-17-psalm-NNN` identities.

This script therefore:
- canonicalizes Book 17 prayer targets in-place;
- copies legacy-extracted note payloads to their canonical note identities;
- preserves the legacy note files as historical extraction artifacts;
- removes those legacy note artifacts from `data/catalog.json` while ensuring
  the canonical note records are catalogued.

It does not infer semantics, delete source data, or modify canonical Psalm text.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CATALOG = DATA / "catalog.json"
PRAYER_RE = re.compile(r"^michael-book-17-prayer-(\d{3})\.json$")
LEGACY_NOTE_RE = re.compile(r"^michael-psalm-(\d+)-note-(\d{3})\.json$")
LEGACY_PSALM_ID_RE = re.compile(r"^michael-psalm-(\d+)$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_psalm_id(number: int) -> str:
    return f"book-17-psalm-{number}"


prayer_updates = 0
for path in sorted((DATA / "prayers").glob("michael-book-17-prayer-*.json")):
    if not PRAYER_RE.match(path.name):
        continue
    prayer = load(path)
    target = str(prayer.get("appliesToPsalmId") or "")
    match = LEGACY_PSALM_ID_RE.fullmatch(target)
    if not match:
        continue
    number = int(match.group(1))
    prayer["appliesToPsalmId"] = canonical_psalm_id(number)
    write(path, prayer)
    prayer_updates += 1

canonical_note_paths: set[str] = set()
legacy_note_paths: set[str] = set()
note_updates = 0
for path in sorted((DATA / "notes").glob("michael-psalm-*-note-*.json")):
    match = LEGACY_NOTE_RE.fullmatch(path.name)
    if not match:
        continue
    number = int(match.group(1))
    suffix = match.group(2)
    legacy_rel = path.relative_to(ROOT).as_posix()
    legacy_note_paths.add(legacy_rel)

    note = load(path)
    canonical_id = f"book-17-psalm-{number}-note-{suffix}"
    note["id"] = canonical_id
    applies = note.setdefault("appliesTo", {})
    applies["recordId"] = canonical_psalm_id(number)

    canonical_path = DATA / "notes" / f"{canonical_id}.json"
    write(canonical_path, note)
    canonical_note_paths.add(canonical_path.relative_to(ROOT).as_posix())
    note_updates += 1

catalog = load(CATALOG)
records = list(catalog.get("records", []))
records = [record for record in records if record not in legacy_note_paths]
records.extend(canonical_note_paths)
catalog["records"] = sorted(set(records))
write(CATALOG, catalog)

print(
    "BOOK17_PRODUCTION_BOUNDARY "
    f"prayerTargetsCanonicalized={prayer_updates} "
    f"canonicalNotesRefreshed={note_updates} "
    f"legacyNotesPreserved={len(legacy_note_paths)} "
    f"catalogRecords={len(catalog['records'])}"
)
