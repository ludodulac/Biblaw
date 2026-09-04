#!/usr/bin/env python3
"""Repair main-text verses swallowed by footnote extraction.

The PDF text stream can place a footnote between two pieces of the main psalm text. The
base extractor historically let a single `N - ...` footnote consume everything until the
next psalm, which swallowed resumed verses. Repairs below are documentary and explicit;
a detector then fails on any additional note that still contains a likely resumed verse,
so new cases cannot silently pass.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/corpus/books"
NOTES = ROOT / "data/notes/books"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_or_append_verse(psalm: dict, number: int, text: str, page: int) -> None:
    verses = psalm.setdefault("verses", [])
    existing = next((v for v in verses if v.get("number") == number), None)
    value = re.sub(r"\s+", " ", text).strip()
    if existing:
        existing["text"] = value
        existing["sourcePages"] = [page]
    else:
        verses.append({"number": number, "text": value, "sourcePages": [page]})
        verses.sort(key=lambda v: v.get("number", 0))


repairs = 0

# Michaël 35: verse 12 was appended to the only footnote on the page.
p = CORPUS / "book-05/psalm-035.json"
n = NOTES / "book-05/book-05-psalm-035-note-001.json"
if p.exists() and n.exists():
    psalm, note = read(p), read(n)
    marker = " 12. Rappelle-toi :"
    if marker in note.get("text", ""):
        before, after = note["text"].split(marker, 1)
        note["text"] = before.strip()
        replace_or_append_verse(psalm, 12, "Rappelle-toi :" + after, 268)
        psalm.setdefault("extraction", {})["resumedVerseAfterFootnoteNormalized"] = True
        psalm.setdefault("validation", {}).setdefault("checks", {})["verseCount"] = len(psalm["verses"])
        write(p, psalm); write(n, note); repairs += 1

# Michaël 36: the footnote interrupts verse 8; its printed continuation then verse 9
# were both swallowed. The exact documentary boundary is fixed here from the source page.
p = CORPUS / "book-05/psalm-036.json"
n = NOTES / "book-05/book-05-psalm-036-note-001.json"
if p.exists() and n.exists():
    psalm, note = read(p), read(n)
    footnote = "Les guides et les protecteurs de l’alliance de Lumière de la Nation Essénienne sont les 4 règnes supérieurs du Père : les maîtres, les Anges, les Archanges et les Dieux."
    continuation = "meilleur fruit, avec les meilleures couleurs, les meilleures formes, et ta vie sera apaisée. Mais sache encore que tout ceci n’est qu’un des visages de la mort."
    verse9 = "Cherche l’autre visage et unis-toi à lui. Il est au-delà des apparences, il est beaucoup plus grand que le corps et les œuvres, les pensées et les aspirations nées du corps. En vérité, il est le chemin de la résurrection et de la vie."
    current = note.get("text", "")
    if current.startswith(footnote) and " 9. Cherche l’autre visage" in current:
        note["text"] = footnote
        v8 = next((v for v in psalm.get("verses", []) if v.get("number") == 8), None)
        if v8 and not v8.get("text", "").rstrip().endswith("visages de la mort."):
            v8["text"] = re.sub(r"\s+", " ", v8["text"].rstrip() + " " + continuation).strip()
        replace_or_append_verse(psalm, 9, verse9, 270)
        psalm.setdefault("extraction", {})["resumedVerseAfterFootnoteNormalized"] = True
        psalm.setdefault("validation", {}).setdefault("checks", {})["verseCount"] = len(psalm["verses"])
        write(p, psalm); write(n, note); repairs += 1

# Guardrail: after known repairs, no note should contain an apparent resumed verse.
suspicious = []
pattern = re.compile(r"(?:^|\s)(\d{1,3})\.\s+[A-ZÀ-ÖØ-ÝÉÈÊÎÔÛÇ]")
for note_path in sorted(NOTES.glob("book-*/*.json")):
    note = read(note_path)
    found = pattern.search(note.get("text", ""))
    if found:
        suspicious.append({"path": str(note_path.relative_to(ROOT)), "verseLikeNumber": int(found.group(1))})

print(f"Normalized {repairs} known note/resumed-verse cases")
if suspicious:
    print(json.dumps({"unknownSuspiciousNotes": suspicious}, ensure_ascii=False, indent=2))
    raise SystemExit("Unknown note contains a verse-like continuation; inspect source before accepting corpus")
