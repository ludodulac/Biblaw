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

# Editorial summaries may refer to a different extracted note number.
# Report candidates only; do not alter archival IDs or editorial records.
def keywords(value):
    return {word for word in re.findall(r"[a-zà-ÿ]{5,}", clean(value))}

suspected_links = []
for path in published:
    editorial = json.loads(path.read_text(encoding="utf-8"))
    summary_words = keywords(editorial.get("summary") or editorial.get("text"))
    if len(summary_words) < 4:
        continue
    group = by_psalm.get(editorial["appliesTo"]["recordId"], [])
    scores = sorted(
        ((len(summary_words & keywords(note.get("text"))), note["id"]) for note in group),
        reverse=True,
    )
    if not scores:
        continue
    best_score, best_id = scores[0]
    current_score = next((score for score, note_id in scores if note_id == editorial["id"]), 0)
    if best_id != editorial["id"] and best_score >= 3 and best_score >= current_score + 2:
        suspected_links.append((editorial["id"], best_id, current_score, best_score))

print(f"Archive: {len(records)} notes, {len(by_psalm)} psalms, {len(published)} editorial notes")
print(f"Potential source overlaps and structural anomalies: {len(flags)}")
for row in flags:
    print("REVIEW | " + " | ".join(row))
print("These flags require examination against the original PDF; no text was changed.")

print(f"Editorial-to-archive links requiring review: {len(suspected_links)}")
for editorial_id, candidate_id, current_score, best_score in suspected_links:
    print(f"LINK_REVIEW | {editorial_id} | possible {candidate_id} | overlap {current_score} vs {best_score}")
