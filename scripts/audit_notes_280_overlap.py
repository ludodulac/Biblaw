#!/usr/bin/env python3
"""Read-only triage of the 280 extracted notes; flags are NOT source corrections."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data/notes/books"
records = []
for path in sorted(ARCHIVE.glob("book-*/*.json")):
    note = json.loads(path.read_text(encoding="utf-8"))
    note["_path"] = str(path.relative_to(ROOT))
    records.append(note)
assert len(records) == 280, "Expected 280 extracted notes"
assert len({n["id"] for n in records}) == len(records), "Duplicate identifiers"

by_psalm = defaultdict(list)
for note in records:
    by_psalm[note["appliesTo"]["recordId"]].append(note)

def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()

flags = []
for psalm, group in sorted(by_psalm.items()):
    for i, first in enumerate(group):
        for second in group[i + 1:]:
            a, b = clean(first.get("text")), clean(second.get("text"))
            if not a or not b:
                flags.append((psalm, first["id"], second["id"], "empty text"))
            elif a == b:
                flags.append((psalm, first["id"], second["id"], "identical transcription"))
            elif min(len(a), len(b)) >= 100 and (a in b or b in a):
                flags.append((psalm, first["id"], second["id"], "one transcription contains another"))

published = sorted((ROOT / "data/notes").glob("book-*-psalm-*-note-*.json"))
archived_by_id = {n["id"]: n for n in records}
for path in published:
    item = json.loads(path.read_text(encoding="utf-8"))
    if item["id"] not in archived_by_id:
        flags.append((item["appliesTo"]["recordId"], item["id"], "-", "published ID absent from archive"))
    elif clean(item.get("summary")) and clean(item.get("summary")) == clean(archived_by_id[item["id"]].get("text")):
        pass  # exact text agreement needs no review

print(f"Archive: {len(records)} notes, {len(by_psalm)} psalms, {len(published)} editorial notes")
print(f"Potential source overlaps and structural anomalies: {len(flags)}")
for row in flags:
    print("REVIEW | " + " | ".join(row))
print("These flags require examination against the original PDF; no text was changed.")
