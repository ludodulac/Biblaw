#!/usr/bin/env python3
"""Index the explicitly named historical teachers in all canonical Biblaw Psalms.

This is a documentary name index, not a claim that every occurrence praises
a person or that two figures belong to the same spiritual tradition.
Only the 1,158 canonical Psalm files are read (never legacy duplicates/notes).
The excerpts are verbatim fragments of the cited verses, not AI summaries.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSALMS = ROOT / "data" / "corpus" / "books"

# Curated proper-name vocabulary. A person is included only if their name
# occurs as a bounded word in a canonical verse, except the four names
# explicitly requested by the site's owner (shown as 'not found' if absent).
# Spelling variants refer to the same named person; titles such as "Christ"
# or "maître" alone are deliberately NOT enough to infer an identity.
MASTERS = (
    ("jesus", "Jésus", ("Jésus", "Jesus", "Yeshoua", "Yeshua", "Jeshua"), True),
    ("mani", "Mani", ("Mani", "Manès", "Manes"), True),
    ("bouddha", "Bouddha", ("Bouddha", "Buddha", "Siddhartha", "Gautama", "Shakyamuni", "Sakyamuni"), True),
    ("moise", "Moïse", ("Moïse", "Moise", "Moshé", "Moshe"), True),
    ("abraham", "Abraham", ("Abraham",), False),
    ("aristote", "Aristote", ("Aristote",), False),
    ("confucius", "Confucius", ("Confucius", "Kong Fu Tse", "Kong Fu-Tse"), False),
    ("david", "David", ("David",), False),
    ("elie", "Élie", ("Élie", "Elie", "Elijah"), False),
    ("enoch", "Énoch", ("Énoch", "Hénoch", "Enoch", "Henoch"), False),
    ("francois-assise", "François d’Assise", ("François d’Assise", "François d'Assise", "Saint François d’Assise", "Saint François d'Assise"), False),
    ("hermes", "Hermès", ("Hermès", "Hermes", "Hermès Trismégiste", "Hermes Trismegiste"), False),
    ("jean-baptiste", "Jean-Baptiste", ("Jean-Baptiste", "Jean le Baptiste", "Jean Baptiste"), False),
    ("krishna", "Krishna", ("Krishna", "Krichna", "Krsna"), False),
    ("lao-tseu", "Lao-Tseu", ("Lao-Tseu", "Lao Tseu", "Laozi", "Lao-Tzu", "Lao Tzu"), False),
    ("mahomet", "Mahomet", ("Mahomet", "Mohammed", "Muhammad", "Mohamed", "Muhammed"), False),
    ("melchisedek", "Melchisédech", ("Melchisédech", "Melchisedek", "Melchisédek", "Melchisedec"), False),
    ("noe", "Noé", ("Noé", "Noe"), False),
    ("orphee", "Orphée", ("Orphée", "Orphee"), False),
    ("platon", "Platon", ("Platon",), False),
    ("pythagore", "Pythagore", ("Pythagore",), False),
    ("rama", "Rama", ("Rama", "Râma"), False),
    ("salomon", "Salomon", ("Salomon",), False),
    ("socrate", "Socrate", ("Socrate",), False),
    ("thot", "Thot", ("Thot", "Thoth"), False),
    ("zoroastre", "Zoroastre", ("Zoroastre", "Zarathoustra", "Zarathustra", "Zarathus(h)tra"), False),
)

def normalize(value: str) -> str:
    value = value.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(c for c in unicodedata.normalize("NFKD", value)
                   if not unicodedata.combining(c))

def pattern_for(names: tuple[str, ...]) -> re.Pattern:
    terms = []
    for name in names:
        # Spaces, apostrophes and dashes vary in historical transcriptions.
        key = normalize(name)
        escaped = re.escape(key).replace(r"\ ", r"[\s\-‑–—]+")
        escaped = escaped.replace(r"\-", r"[\s\-‑–—]+")
        escaped = escaped.replace("’", "['’]").replace("'", "['’]")
        terms.append(escaped)
    return re.compile(r"(?<![a-z])(?:" + "|".join(sorted(set(terms), key=len, reverse=True)) + r")(?![a-z])")

def snippet(original: str, match: re.Match, width: int = 215) -> str:
    """Human-readable verbatim context around a match (no invented paraphrase)."""
    text = re.sub(r"\s+", " ", original).strip()
    if len(text) <= width:
        return text
    # Match offsets are from normalized text. Unicode decompositions can change
    # string lengths, so locate a nearby term in normalized text then take an
    # approximately matching position in the original, falling back safely.
    offset = match.start()
    before = max(0, offset - 77)
    after = min(len(text), before + width)
    before = max(0, after - width)
    if before:
        boundary = text.find(" ", before, min(before + 16, len(text)))
        if boundary > 0:
            before = boundary + 1
    if after < len(text):
        boundary = text.rfind(" ", max(before, after - 16), after)
        if boundary > before:
            after = boundary
    return ("…" if before else "") + text[before:after].strip() + ("…" if after < len(text) else "")

def generate(destination: Path) -> dict:
    files = sorted(PSALMS.glob("book-*/psalm-*.json"))
    records = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    records = [record for record in records if record.get("recordType") == "psalm"]
    ids = [r["id"] for r in records]
    if len(records) != 1158 or len(set(ids)) != len(ids):
        raise ValueError(f"Expected 1,158 distinct canonical Psalms, got {len(ids)}")
    compiled = [(key, label, pattern_for(forms), always)
                for key, label, forms, always in MASTERS]
    findings = defaultdict(list)
    seen_verse = set()
    for record in records:
        if not isinstance(record.get("verses"), list):
            raise ValueError(f"Psalm has no verses: {record['id']}")
        for verse in record["verses"]:
            text = verse.get("text", "")
            number = verse["number"]
            if not isinstance(text, str) or not isinstance(number, int):
                raise ValueError(f"Invalid verse in {record['id']}")
            normalized = normalize(text)
            for key, _, matcher, _ in compiled:
                match = matcher.search(normalized)
                if match is None:
                    continue
                identity = (key, record["id"], number)
                if identity in seen_verse:
                    raise ValueError(f"Duplicate verse match: {identity}")
                seen_verse.add(identity)
                findings[key].append({
                    "recordId": record["id"], "archangel": record["archangel"],
                    "psalm": record["number"], "book": record["book"]["number"],
                    "verse": number, "excerpt": snippet(text, match),
                })
    entries = []
    for key, label, _, always in compiled:
        refs = findings[key]
        if not refs and not always:
            continue
        by_psalm = {}
        for ref in refs:
            rec_id = ref["recordId"]
            if rec_id not in by_psalm:
                by_psalm[rec_id] = {
                    "recordId": rec_id, "archangel": ref["archangel"],
                    "psalm": ref["psalm"], "book": ref["book"], "verses": []
                }
            by_psalm[rec_id]["verses"].append({
                "number": ref["verse"], "excerpt": ref["excerpt"]
            })
        sources = sorted(by_psalm.values(), key=lambda r: (r["book"], r["psalm"]))
        entries.append({
            "id": key, "label": label, "psalmCount": len(sources),
            "verseCount": len(refs), "sources": sources
        })
    entries.sort(key=lambda e: normalize(e["label"]))
    output = {
        "schemaVersion": 1, "psalmCount": len(records),
        "method": "Index documentaire des noms explicitement cités dans les versets des 1 158 psaumes canoniques. Extraits textuels sans interprétation ; un nom cité n’implique ni approbation ni filiation spirituelle. Le nom d’un maître non trouvé n’est jamais assorti d’une référence inventée.",
        "entries": entries
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    # Recheck that each reference resolves to an exact canonical Psalm and verse.
    by_id = {r["id"]: r for r in records}
    for entry in entries:
        matcher = next(pattern for key, _, pattern, _ in compiled if key == entry["id"])
        for source in entry["sources"]:
            record = by_id[source["recordId"]]
            verses = {v["number"]: v["text"] for v in record["verses"]}
            for ref in source["verses"]:
                assert ref["number"] in verses
                assert matcher.search(normalize(verses[ref["number"]]))
                assert ref["excerpt"].strip()
    result = {"psalms": len(records), "masters": len(entries),
              "withMentions": sum(e["verseCount"] > 0 for e in entries),
              "links": sum(e["verseCount"] for e in entries)}
    print("Maîtres de la tradition Biblaw:", result)
    return result

if __name__ == "__main__":
    generate(ROOT / "data" / "masters-public.json")
