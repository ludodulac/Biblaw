#!/usr/bin/env python3
"""Reapply source-audited verse/note boundaries after PDF extraction.

These are deterministic documentary repairs, not editorial interpretations. The
script is deliberately exact and idempotent: it only moves a known source tail
from a known note back to the known interrupted verse. It also removes one known
duplicate note emitted by the extractor when a concrete verse attachment exists.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"

REPAIRS = [
    (14, 86, 6, "book-14-psalm-086-note-001", "pouvez compter, mais plutôt comme un dissipateur détournant les forces à l’œuvre et vous empêchant de toucher l’essentiel."),
    (14, 87, 7, "book-14-psalm-087-note-001", "œuvre collective divine. La porte est ouverte. Alors, engagez-vous sur le chemin du service de la Lumière. Votre engagement ouvrira la porte pour beaucoup d’autres et c’est ainsi que la fleur d’une nouvelle conscience grandira sur la terre."),
    (14, 110, 6, "book-14-psalm-110-note-001", "fermé dans votre propre vie. Alors je ne pourrai plus m’approcher de vous, car la résonance ne sera plus là. Ce sera l’avènement du monde des sans-âmes."),
    (15, 77, 5, "book-15-psalm-077-note-001", "hommes tout en comprenant et éclairant toutes les formes d’existence se manifestant autour de lui et en lui."),
    (15, 78, 15, "book-15-psalm-078-note-004", "dans plusieurs mondes tout en étant un homme ou une femme dans le monde des hommes."),
    (16, 86, 14, "book-16-psalm-086-note-002", "être. Vivez dans la grandeur de la Lumière et non dans la petitesse des hommes qui veulent se passer de la Lumière pour se glorifier eux-mêmes."),
]

DUPLICATE_NOTES = [
    (15, 78, "book-15-psalm-078-note-003", "book-15-psalm-078-note-004"),
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compact(text: str) -> str:
    return " ".join(text.split())


changes = []

for book, psalm_no, verse_no, note_id, tail in REPAIRS:
    psalm_path = CORPUS / f"book-{book:02d}" / f"psalm-{psalm_no:03d}.json"
    note_path = NOTES / f"book-{book:02d}" / f"{note_id}.json"
    if not psalm_path.exists() or not note_path.exists():
        continue
    psalm = load(psalm_path)
    note = load(note_path)
    verse = next((v for v in psalm.get("verses", []) if v.get("number") == verse_no), None)
    if verse is None:
        raise SystemExit(f"Missing audited verse {book}:{psalm_no}:{verse_no}")

    changed = False
    ntext = compact(note.get("text", ""))
    vtext = compact(verse.get("text", ""))
    tail_c = compact(tail)

    if ntext.endswith(tail_c):
        note["text"] = ntext[:-len(tail_c)].rstrip()
        changed = True
    if not vtext.endswith(tail_c):
        verse["text"] = compact(vtext + " " + tail_c)
        changed = True

    if changed:
        psalm.setdefault("extraction", {})["sourceBackedInlineNoteSplitNormalized"] = True
        note.setdefault("validation", {})["sourceBackedInlineNoteSplitNormalized"] = True
        save(psalm_path, psalm)
        save(note_path, note)
        changes.append({"recordId": psalm.get("id"), "noteId": note_id, "verse": verse_no})

for book, psalm_no, duplicate_id, canonical_id in DUPLICATE_NOTES:
    duplicate = NOTES / f"book-{book:02d}" / f"{duplicate_id}.json"
    canonical = NOTES / f"book-{book:02d}" / f"{canonical_id}.json"
    psalm_path = CORPUS / f"book-{book:02d}" / f"psalm-{psalm_no:03d}.json"
    if duplicate.exists() and canonical.exists() and psalm_path.exists():
        d = load(duplicate)
        c = load(canonical)
        # Remove only the audited extractor duplicate: same source page and marker,
        # while the canonical record has a concrete verse attachment.
        if (d.get("source", {}).get("pdfPage") == c.get("source", {}).get("pdfPage")
                and d.get("appliesTo", {}).get("marker") == c.get("appliesTo", {}).get("marker")
                and c.get("appliesTo", {}).get("verse") is not None):
            duplicate.unlink()
            psalm = load(psalm_path)
            psalm["noteIds"] = [nid for nid in psalm.get("noteIds", []) if nid != duplicate_id]
            psalm.setdefault("extraction", {})["duplicateEditorialNoteRemoved"] = True
            save(psalm_path, psalm)
            changes.append({"recordId": psalm.get("id"), "removedDuplicateNote": duplicate_id})

print(json.dumps({"changes": changes}, ensure_ascii=False, indent=2))
