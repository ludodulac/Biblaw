#!/usr/bin/env python3
"""Reject legacy Psalm ids and noncanonical files inside production data.

The historical Psalm files under data/corpus/<archangel>/ and thematic prototypes under
`data/thematic-index/prototypes/` are intentionally retained and are not scanned as canonical data.
Canonical production data must refer to Psalms with `book-XX-psalm-NNN` ids. The canonical thematic
books directory must contain exactly `book-01.json` through `book-44.json` and nothing else.
This audit detects structure and exact ID-shaped strings; it never infers or rewrites a target.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMATIC_BOOKS = ROOT / "data/thematic-index/books"
LEGACY_RE = re.compile(r"^(?:michael|gabriel|raphael|ouriel)-psalm-\d+$")

SCAN_GLOBS = (
    "data/corpus/books/**/*.json",
    "data/prayers/*.json",
    "data/notes/*.json",
    "data/thematic-index/books/*.json",
)


def walk(value, pointer: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{pointer}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{pointer}[{index}]")
    elif isinstance(value, str):
        yield pointer, value


issues: list[str] = []

expected_thematic_books = {f"book-{number:02d}.json" for number in range(1, 45)}
actual_entries = {path.name for path in THEMATIC_BOOKS.iterdir()} if THEMATIC_BOOKS.exists() else set()
missing_books = sorted(expected_thematic_books - actual_entries)
unexpected_entries = sorted(actual_entries - expected_thematic_books)
if missing_books:
    issues.append("missing canonical thematic book files: " + ", ".join(missing_books))
if unexpected_entries:
    issues.append("unexpected entries in canonical thematic books directory: " + ", ".join(unexpected_entries))

paths = sorted({path for pattern in SCAN_GLOBS for path in ROOT.glob(pattern)})
json_files = 0
string_values = 0

for path in paths:
    if not path.is_file():
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    json_files += 1
    for pointer, value in walk(data):
        string_values += 1
        if LEGACY_RE.fullmatch(value):
            issues.append(f"{path.relative_to(ROOT)} {pointer} = {value}")

print(
    f"LEGACY_REFERENCE_AUDIT files={json_files} strings={string_values} "
    f"thematicBooks={len(actual_entries)} issues={len(issues)}"
)
if issues:
    raise SystemExit("Canonical production structure/reference audit failed:\n- " + "\n- ".join(issues))
print(
    "Canonical production audit OK: 44 thematic books, no extra canonical-book entries, "
    "and no dependency on historical Psalm ids"
)
