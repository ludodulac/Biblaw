#!/usr/bin/env python3
"""Validate editorial thematic-index book files against the structured psalm corpus.

This validator is the admissibility gate for canonical theme–Psalm relations. Ranking fields are
validated only after a relation has passed identity/evidence checks; they never create a relation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "data/thematic-index/books"
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"
METHOD = ROOT / "data/thematic-index/method.json"
OUT = ROOT / "data/thematic-index/validation-report.json"
ALLOWED_IMPORTANCE = {"central", "important", "related"}
ALLOWED_DIRECTNESS = {"direct", "symbolic", "editorial", "indirect", "contextual"}
EXPECTED_BOOK_FILES = {f"book-{number:02d}.json" for number in range(1, 45)}
EXPECTED_SEMANTIC_DEPTH = "deep-content-grounded"
EXPECTED_SEMANTIC_PASS = "deep-content-grounded-complete"
EXPECTED_METHOD_STATUS = "editorial-indexing-complete"

errors = []
warnings = []
stats = {"books": 0, "psalmAnalyses": 0, "themeRelations": 0}

method_contract = json.loads(METHOD.read_text(encoding="utf-8"))
importance_scale = method_contract.get("importanceScale") or {}
if set(importance_scale) != ALLOWED_IMPORTANCE:
    errors.append({
        "file": str(METHOD.relative_to(ROOT)),
        "type": "importance-scale-vocabulary-mismatch",
        "expected": sorted(ALLOWED_IMPORTANCE),
        "actual": sorted(importance_scale),
    })
for historical_value, canonical_value in (method_contract.get("historicalImportanceAliases") or {}).items():
    if historical_value in ALLOWED_IMPORTANCE or canonical_value not in ALLOWED_IMPORTANCE:
        errors.append({
            "file": str(METHOD.relative_to(ROOT)),
            "type": "invalid-historical-importance-alias",
            "historicalValue": historical_value,
            "canonicalValue": canonical_value,
        })

actual_entries = {path.name for path in BOOKS.iterdir()} if BOOKS.exists() else set()
missing_book_files = sorted(EXPECTED_BOOK_FILES - actual_entries)
unexpected_entries = sorted(actual_entries - EXPECTED_BOOK_FILES)
if missing_book_files:
    errors.append({"type": "missing-canonical-thematic-book-files", "files": missing_book_files})
if unexpected_entries:
    errors.append({"type": "unexpected-canonical-thematic-book-entries", "files": unexpected_entries})

for path in sorted(BOOKS.glob("book-*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    book = data.get("book", {})
    book_no = book.get("number")
    if not isinstance(book_no, int):
        errors.append({"file": str(path.relative_to(ROOT)), "type": "missing-book-number"})
        continue
    expected_filename = f"book-{book_no:02d}.json"
    if path.name != expected_filename:
        errors.append({
            "file": str(path.relative_to(ROOT)),
            "type": "book-number-filename-mismatch",
            "bookNumber": book_no,
            "expectedFilename": expected_filename,
        })
    stats["books"] += 1

    method = data.get("method") or {}
    analyses = data.get("psalmAnalyses", [])
    if method.get("status") != EXPECTED_METHOD_STATUS:
        errors.append({
            "file": str(path.relative_to(ROOT)),
            "type": "canonical-book-status-not-complete",
            "value": method.get("status"),
        })
    if method.get("semanticPass") != EXPECTED_SEMANTIC_PASS:
        errors.append({
            "file": str(path.relative_to(ROOT)),
            "type": "canonical-book-semantic-pass-not-complete",
            "value": method.get("semanticPass"),
        })
    if method.get("contentGrounding") != "complete":
        errors.append({
            "file": str(path.relative_to(ROOT)),
            "type": "canonical-book-content-grounding-not-complete",
            "value": method.get("contentGrounding"),
        })
    if method.get("deepPsalmCount") != len(analyses):
        errors.append({
            "file": str(path.relative_to(ROOT)),
            "type": "deep-psalm-count-mismatch",
            "declared": method.get("deepPsalmCount"),
            "actual": len(analyses),
        })

    seen_psalms = set()
    for psalm in analyses:
        stats["psalmAnalyses"] += 1
        record_id = psalm.get("recordId")
        if not record_id or record_id in seen_psalms:
            errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "type": "duplicate-or-missing-psalm-analysis"})
            continue
        seen_psalms.add(record_id)
        if psalm.get("semanticDepth") != EXPECTED_SEMANTIC_DEPTH:
            errors.append({
                "file": str(path.relative_to(ROOT)),
                "recordId": record_id,
                "type": "canonical-psalm-semantic-depth-not-deep",
                "value": psalm.get("semanticDepth"),
            })
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
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "no-verse-reference"})
            missing = [v for v in refs if v not in valid_verses]
            if missing:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "themeId": theme_id, "type": "invalid-verse-reference", "verseNumbers": missing})
        for note_id in psalm.get("notesUsed", []):
            candidates = list(NOTES.glob(f"book-*/{note_id}.json"))
            if not candidates:
                errors.append({"file": str(path.relative_to(ROOT)), "recordId": record_id, "noteId": note_id, "type": "missing-note-reference"})

if stats["books"] != 44:
    errors.append({"type": "canonical-book-count-mismatch", "expected": 44, "actual": stats["books"]})

status = "passed" if not errors else "failed"
report = {"schemaVersion": 1, "status": status, "stats": stats, "errors": errors, "warnings": warnings}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Thematic validation: {status}; {len(errors)} errors; {len(warnings)} warnings")
if errors:
    raise SystemExit(1)
