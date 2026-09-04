#!/usr/bin/env python3
"""Build the first Biblaw structured-data pilot from the source PDF.

The script intentionally extracts only Michael, psalm 26. It is a validation
fixture for the corpus model, not yet the full-book importer.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
OUTPUT = ROOT / "data" / "corpus" / "michael" / "psalm-026.json"


def extract_pages(first: int, last: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def clean_page_noise(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if re.match(r"^Livre 5 \|", stripped, re.IGNORECASE):
            continue
        if stripped in {"251", "252"}:
            continue
        lines.append(line)
    return "\n".join(lines)


def normalize_wrapped_text(text: str) -> str:
    text = re.sub(r"-\n\s*", "", text)
    text = re.sub(r"\n\s*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_verses(text: str) -> list[dict[str, object]]:
    title = re.search(
        r"26\s+L\s*e secret de la chouette pour\s+transformer ses imperfections",
        text,
        flags=re.IGNORECASE,
    )
    if not title:
        raise RuntimeError("Psalm 26 title was not found")
    body = text[title.end() :]
    matches = list(re.finditer(r"(?m)^\s*(\d{1,2})\.\s+", body))
    verses = []
    for index, match in enumerate(matches):
        number = int(match.group(1))
        if number < 1 or number > 12:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        verse_text = normalize_wrapped_text(body[match.end() : end])
        verses.append(
            {
                "number": number,
                "text": verse_text,
                "sourcePages": [251] if number <= 8 else [252],
            }
        )
    if [verse["number"] for verse in verses] != list(range(1, 13)):
        raise RuntimeError("Expected verses 1 through 12")
    return verses


def main() -> None:
    raw = clean_page_noise(extract_pages(251, 252))
    record = {
        "id": "michael-psalm-026",
        "recordType": "psalm",
        "archangel": "michael",
        "book": {"number": 5, "title": "Homme, redeviens un mage"},
        "number": 26,
        "title": "Le secret de la chouette pour transformer ses imperfections",
        "source": {
            "document": "Bible essénienne (classée par livres).pdf",
            "printedPages": [251, 252],
        },
        "verses": parse_verses(raw),
        "notes": [],
        "masterPrayer": None,
        "conceptIds": ["concept-chouette", "concept-imperfection", "concept-obscurite"],
        "validation": {
            "status": "machine-extracted-needs-human-review",
            "checks": {"verseSequenceComplete": True, "verseCount": 12},
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
