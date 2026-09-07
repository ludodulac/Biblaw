#!/usr/bin/env python3
"""Migrate deterministic prayer/note attachments to canonical Psalm ids.

Only corpus-internal, uniquely evidenced mappings are changed. Ambiguous/unproven cases are left
untouched and must remain visible to the attachment audit / incoherence register.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog.json"
BOOK_ROOT = ROOT / "data/corpus/books"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: dict):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pages(obj: dict) -> set[int]:
    source = obj.get("source") or {}
    raw = source.get("pdfPages") or source.get("printedPages") or source.get("printedPage") or []
    if isinstance(raw, int):
        raw = [raw]
    return {int(v) for v in raw if str(v).isdigit()}


def same_document(a: dict, b: dict) -> bool:
    return bool((a.get("source") or {}).get("document")) and (a.get("source") or {}).get("document") == (b.get("source") or {}).get("document")


def source_connected(child: dict, psalm: dict) -> bool:
    """True for source-page overlap or immediate printed adjacency in the same document."""
    child_pages, psalm_pages = pages(child), pages(psalm)
    if not child_pages or not psalm_pages or not same_document(child, psalm):
        return False
    if child_pages & psalm_pages:
        return True
    return min(child_pages) - max(psalm_pages) == 1


psalm_paths: dict[str, Path] = {}
psalms: dict[str, dict] = {}
for path in sorted(BOOK_ROOT.glob("book-*/psalm-*.json")):
    obj = load(path)
    if obj.get("recordType") == "psalm":
        psalms[obj["id"]] = obj
        psalm_paths[obj["id"]] = path

legacy_re = re.compile(r"^(michael|gabriel|raphael|ouriel)-psalm-(\d+)$")
note_suffix_re = re.compile(r"-note-(\d+)$")


def identity_candidates(archangel: str, number: int):
    return [p for p in psalms.values() if p.get("archangel") == archangel and int(p.get("number", -1)) == number]


catalog = load(CATALOG)
records = list(catalog.get("records", []))
record_set = set(records)

changed_psalms: set[str] = set()
changed_prayers = 0
renamed_notes = 0
unresolved_notes = []

# 1) Canonicalize legacy prayer targets from corpus-internal evidence:
# explicit book number + archangel + Psalm number + same source document + overlapping/adjacent pages.
# Then repair reciprocal prayerIds when needed.
for rel in list(records):
    if not rel.startswith("data/prayers/"):
        continue
    path = ROOT / rel
    prayer = load(path)
    if prayer.get("recordType") != "master-prayer":
        continue
    prayer_id = prayer.get("id")
    target_id = prayer.get("appliesToPsalmId")
    target = psalms.get(target_id)

    if target is None:
        match = legacy_re.match(str(target_id or ""))
        if not match:
            raise SystemExit(f"Unsupported prayer target: {prayer_id} -> {target_id}")
        archangel, number_text = match.groups()
        prayer_book = int(prayer.get("bookNumber", -1))
        candidates = []
        for psalm in identity_candidates(archangel, int(number_text)):
            psalm_book = int((psalm.get("book") or {}).get("number", -2))
            if psalm_book == prayer_book and source_connected(prayer, psalm):
                candidates.append(psalm)
        if len(candidates) != 1:
            raise SystemExit(f"Prayer {prayer_id} has {len(candidates)} deterministic canonical candidates")
        target = candidates[0]
        prayer["appliesToPsalmId"] = target["id"]
        dump(path, prayer)
        changed_prayers += 1

    prayer_ids = list(target.get("prayerIds") or [])
    if prayer_id not in prayer_ids:
        if not source_connected(prayer, target):
            raise SystemExit(f"Cannot add reciprocal prayer link without overlapping/adjacent source evidence: {prayer_id} -> {target['id']}")
        prayer_ids.append(prayer_id)
        target["prayerIds"] = sorted(set(prayer_ids))
        changed_psalms.add(target["id"])

# 2) Canonicalize legacy note ids/targets only when the canonical Psalm already contains the reciprocal
# canonical note id, source pages overlap, and any verse pointer exists on that Psalm.
for rel in list(records):
    if not rel.startswith("data/notes/"):
        continue
    old_path = ROOT / rel
    note = load(old_path)
    if note.get("recordType") != "note":
        continue
    applies = note.get("appliesTo") or {}
    target_id = applies.get("recordId")
    if target_id in psalms:
        continue

    match = legacy_re.match(str(target_id or ""))
    suffix_match = note_suffix_re.search(str(note.get("id") or ""))
    if not match or not suffix_match:
        unresolved_notes.append(note.get("id"))
        continue

    archangel, number_text = match.groups()
    suffix = suffix_match.group(1)
    verse = applies.get("verse")
    candidates = []
    for psalm in identity_candidates(archangel, int(number_text)):
        canonical_note_id = f"{psalm['id']}-note-{suffix}"
        reciprocal = canonical_note_id in (psalm.get("noteIds") or [])
        overlap = bool(pages(note) & pages(psalm)) if pages(note) and pages(psalm) and same_document(note, psalm) else False
        verse_ok = verse is None or int(verse) in {int(v.get("number")) for v in psalm.get("verses", []) if v.get("number") is not None}
        if reciprocal and overlap and verse_ok:
            candidates.append((psalm, canonical_note_id))

    if len(candidates) != 1:
        unresolved_notes.append(note.get("id"))
        continue

    psalm, new_note_id = candidates[0]
    new_rel = f"data/notes/{new_note_id}.json"
    new_path = ROOT / new_rel
    if new_path.exists() and new_path != old_path:
        raise SystemExit(f"Note destination already exists: {new_rel}")

    note["id"] = new_note_id
    note.setdefault("appliesTo", {})["recordId"] = psalm["id"]
    dump(old_path, note)
    if new_path != old_path:
        old_path.rename(new_path)
        index = records.index(rel)
        records[index] = new_rel
        record_set.discard(rel)
        if new_rel in record_set:
            raise SystemExit(f"Duplicate catalog path after note rename: {new_rel}")
        record_set.add(new_rel)
    renamed_notes += 1

for psalm_id in sorted(changed_psalms):
    dump(psalm_paths[psalm_id], psalms[psalm_id])

catalog["records"] = records
dump(CATALOG, catalog)

print(
    f"Attachment migration: prayersCanonicalized={changed_prayers} "
    f"psalmsReciprocalPrayerLinksUpdated={len(changed_psalms)} notesCanonicalized={renamed_notes}"
)
print("Unresolved notes left untouched:", ", ".join(sorted(str(x) for x in unresolved_notes)) or "none")
