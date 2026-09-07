#!/usr/bin/env python3
"""Reject legacy Psalm ids and noncanonical files inside production data.

Historical Psalm files under `data/corpus/<archangel>/`, legacy extraction notes that are
not catalogued, and thematic prototypes under `data/thematic-index/prototypes/` are retained
but are not production inputs. Canonical production data must refer to Psalms with
`book-XX-psalm-NNN` ids. The canonical thematic books directory must contain exactly
`book-01.json` through `book-44.json` and nothing else.

This audit follows production boundaries rather than directory presence alone:
- canonical corpus files under `data/corpus/books/`;
- catalogued prayers and notes;
- canonical thematic book files;
- the generated browser bundle actually served to users.

It detects structure and exact ID-shaped strings; it never infers or rewrites a target.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
THEMATIC_BOOKS = DATA / "thematic-index/books"
CATALOG = DATA / "catalog.json"
BROWSER_BUNDLE = DATA / "browser-search-catalog.json"
LEGACY_RE = re.compile(r"^(?:michael|gabriel|raphael|ouriel)-psalm-\d+$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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

catalog = load(CATALOG)
records = catalog.get("records") or []
production_attachment_paths = {
    ROOT / rel
    for rel in records
    if isinstance(rel, str) and (rel.startswith("data/prayers/") or rel.startswith("data/notes/"))
}

paths = set((DATA / "corpus/books").glob("**/*.json"))
paths.update(THEMATIC_BOOKS.glob("*.json"))
paths.update(production_attachment_paths)
if BROWSER_BUNDLE.exists():
    paths.add(BROWSER_BUNDLE)

json_files = 0
string_values = 0
for path in sorted(paths):
    if not path.is_file():
        issues.append(f"production path missing: {path.relative_to(ROOT)}")
        continue
    data = load(path)
    json_files += 1
    for pointer, value in walk(data):
        string_values += 1
        if LEGACY_RE.fullmatch(value):
            issues.append(f"{path.relative_to(ROOT)} {pointer} = {value}")

print(
    f"LEGACY_REFERENCE_AUDIT files={json_files} strings={string_values} "
    f"thematicBooks={len(actual_entries)} cataloguedAttachments={len(production_attachment_paths)} "
    f"issues={len(issues)}"
)
if issues:
    raise SystemExit("Canonical production structure/reference audit failed:\n- " + "\n- ".join(issues))
print(
    "Canonical production audit OK: 44 thematic books, no extra canonical-book entries, "
    "and no production dependency on historical Psalm ids"
)
