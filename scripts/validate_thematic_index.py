#!/usr/bin/env python3
"""Validate editorial thematic-index book files against the structured psalm corpus."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"
OUT = ROOT / "data/thematic-index/validation-report.json"
ALLOWED_IMPORTANCE = {"central", "important", "related"}
ALLOWED_DIRECTNESS = {"direct", "symbolic", "editorial", "indirect"}

errors = []
warnings = []
stats = {"books": 0, "psalmAnalyses": 0, "themeRelations": 0}

for path in sorted(BOOKS.glob("book-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    book = data.get("book", {})
    book_no = book.get("number")
    if not isinstance(book_no, int):
        errors.append({"file": str(path.relative_to(ROOT)), "type": "missing-book-number"})
        continue
    stats["books"] += 1
    seen_psalms = set()
    for psalm in data.get("psalmAnalyses", []):
        stats["psalmAnalyses"] += 1
        record_id = psalm.get("recordId")
        if not record_id or record_id in seen_psalms:
            errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "type": "duplicate-or-missing-psalm-analysis"})
            continue
        seen_psalms.add(record_id)
        number = psalm.get("number")
        source_path = CORPUS / f"book-{book_no:02d}" / f"psalm-{int(number):03d}.json" if isinstance(number, int) else None
        if not source_path or not source_path.exists():
            errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "type": "missing-source-psalm"})
            continue
        source = json.loads(source_path.read_text(encoding="utf-8"))
        if source.get("id") != record_id:
            errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "type": "record-id-mismatch", "sourceId": source.get("id")})
        source_title = source.get("title")
        if psalm.get("title") != source_title:
            warnings.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "type": "title-out-of-sync", "indexedTitle": psalm.get("title"), "sourceTitle": source_title})
        valid_verses = {v.get("number") for v in source.get("verses", [])}
        seen_themes = set()
        for rel in psalm.get("themes", []):
            stats["themeRelations"] += 1
            theme_id = rel.get("themeId")
            if not theme_id or theme_id in seen_themes:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "duplicate-or-missing-theme-id"})
            seen_themes.add(theme_id)
            if not str(rel.get("label") or "").strip():
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "missing-theme-label"})
            if rel.get("importance") not in ALLOWED_IMPORTANCE:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "invalid-importance", "value": rel.get("importance")})
            if rel.get("directness") not in ALLOWED_DIRECTNESS:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "invalid-directness", "value": rel.get("directness")})
            if not str(rel.get("teaching") or "").strip():
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "missing-teaching"})
            refs = rel.get("verseNumbers", [])
            if not refs:
                warnings.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "no-verse-reference"})
            missing = [v for v in refs if v not in valid_verses]
            if missing:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "invalid-verse-reference", "verseNumbers": missing})
        for note_id in psalm.get("notesUsed", []):
            candidates = list(NOTES.glob(f"book-*/{note_id}.json"))
            if not candidates:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "noteId": note_id, "type": "missing-note-reference"})

status = "passed" if not errors else "failed"
report = {"schemaVersion": 1, "status": status, "stats": stats, "errors": errors, "warnings": warnings}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Thematic validation: {status}; {len(errors)} errors; {len(warnings)} warnings")
if errors:
    raise SystemExit(1)
