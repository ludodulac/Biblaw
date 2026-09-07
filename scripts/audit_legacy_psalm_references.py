#!/usr/bin/env python3
"""Reject legacy archangel-scoped Psalm ids inside canonical production data.

The historical Psalm files under data/corpus/<archangel>/ are intentionally retained and are not
scanned here. Canonical production data must refer to Psalms with `book-XX-psalm-NNN` ids instead.
This audit only detects exact ID-shaped strings; it does not infer or rewrite a target.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


paths = sorted({path for pattern in SCAN_GLOBS for path in ROOT.glob(pattern)})
issues: list[str] = []
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

print(f"LEGACY_REFERENCE_AUDIT files={json_files} strings={string_values} issues={len(issues)}")
if issues:
    raise SystemExit("Legacy Psalm references remain in canonical data:\n- " + "\n- ".join(issues))
print("Legacy Psalm reference audit OK: canonical production data is independent of historical Psalm ids")
