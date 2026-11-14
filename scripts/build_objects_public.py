#!/usr/bin/env python3
"""Build a source-verified index of concrete objects named in canonical Psalms.

The catalogue is a *lexical documentary index*, not a semantic interpretation
of the archangels' teachings. Every public link refers to an actual verse from
the canonical 1,158 Psalm JSON files, never a guessed reference or a note.
Unattested candidate names are hidden, except the two names specifically
requested by the site owner (avion and cerf-volant).
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
VOCABULARY = ROOT / "data" / "objects-lexicon.json"
MUST_SHOW = {"avion", "cerf-volant"}


def norm(text: str) -> str:
    text = text.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(ch))


def object_pattern(forms: list[str]) -> re.Pattern:
    alternatives = []
    for raw in forms:
        key = norm(raw.strip())
        if not key:
            raise ValueError("Empty lexical object variant")
        # Treat normal spaces, nonbreaking spaces, and common hyphens as
        # equivalent only inside a declared multiword spelling.
        pieces = re.split(r"[\s\-\u2010-\u2015\u2011]+", key)
        escaped = r"[\s\-\u2010-\u2015]+" .join(re.escape(p) for p in pieces)
        alternatives.append(escaped)
    alternatives.sort(key=len, reverse=True)
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(dict.fromkeys(alternatives)) +
                      r")(?![a-z0-9])")


def keeps_object_mention(object_id: str, normalized: str, match: re.Match) -> bool:
    """Avoid major common-verb and fixed-expression false positives."""
    # 'En train de travailler' is not a means of transport.
    around = normalized[max(0, match.start() - 16): min(len(normalized), match.end() + 16)]
    if object_id == "train" and re.search(r"\ben\s+train\s+de\b", around):
        # If the verse says 'en train de ...' but also describes an actual train,
        # the second occurrence is still preserved.
        before = normalized[max(0, match.start() - 4):match.start()]
        if before.rstrip().endswith("en"):
            return False
    if object_id == "lit":
        # 'Il lit', 'elle lit', 'on lit' are reading verbs.
        previous = normalized[max(0, match.start() - 35):match.start()]
        token = normalized[match.start():match.end()]
        if token == "lit" and not re.search(
            r"(?:^|[^a-z])(?:un|le|du|au|son|mon|ton|notre|votre|leur|ce|dans un|sur le|sur un|sous le)\s+$",
            previous
        ):
            return False
    if object_id == "porte":
        # 'Il porte', 'tu portes', 'la parole porte' are verbs, not doors.
        previous = normalized[max(0, match.start() - 40):match.start()]
        if not re.search(
            r"(?:^|[^a-z])(?:la|une|les|des|aux|du|de la|sa|ses|ma|mes|ta|tes|notre|nos|votre|vos|leur|leurs|cette|ces|celles des|devant la)\s+$",
            previous
        ):
            return False
    if object_id == "livre":
        preceding = normalized[max(0, match.start() - 35):match.start()]
        token = normalized[match.start():match.end()]
        if token == "livre" and not re.search(
            r"(?:^|[^a-z])(?:un|le|du|au|son|mon|ton|notre|votre|leur|ce|dans un|dans le|de ce|des)\s+$",
            preceding
        ):
            # A specific 'livre de ...' is a book, but 'se livre à ...' isn't.
            after = normalized[match.end():match.end() + 40]
            if not re.match(r"\s+d(?:e|u|es)\s+\w+", after):
                return False
    if object_id == "photographie":
        preceding = normalized[max(0, match.start() - 22):match.start()]
        token = normalized[match.start():match.end()]
        if token in {"photo", "photos"} and re.search(r"\bappareils?\s+$", preceding):
            return False
    return True


def excerpt(original: str, found: re.Match, limit: int = 240) -> str:
    # Use the exact Psalm wording. Normalize only whitespace for display.
    if len(original) <= limit:
        return re.sub(r"\s+", " ", original).strip()
    # Map the normalized match offsets back onto the source Unicode text.
    positions = []
    for pos, character in enumerate(original):
        positions.extend([pos] * len(norm(character)))
    position = positions[min(found.start(), len(positions) - 1)]
    start = max(0, position - 75)
    end = min(len(original), start + limit)
    start = max(0, end - limit)
    if start:
        blank = original.find(" ", start, min(start + 17, len(original)))
        if blank > start:
            start = blank + 1
    if end < len(original):
        blank = original.rfind(" ", max(start, end - 16), end)
        if blank > start:
            end = blank
    text = re.sub(r"\s+", " ", original[start:end]).strip()
    return ("…" if start else "") + text + ("…" if end < len(original) else "")


def generate(destination: Path) -> dict:
    catalog = json.loads(VOCABULARY.read_text(encoding="utf-8"))
    assert catalog["schemaVersion"] == 1
    definitions = catalog["entries"]
    ids = [entry["id"] for entry in definitions]
    if not definitions or len(set(ids)) != len(ids):
        raise ValueError("Objects vocabulary is empty or contains duplicate object IDs")
    if not MUST_SHOW.issubset(ids):
        raise ValueError("Required examples avion and cerf-volant are missing")
    patterns = [(entry, object_pattern(entry["forms"])) for entry in definitions]
    files = sorted(CORPUS.glob("book-*/psalm-*.json"))
    psalms = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    psalms = [record for record in psalms if record.get("recordType") == "psalm"]
    by_id = {record["id"]: record for record in psalms}
    if len(psalms) != 1158 or len(by_id) != 1158:
        raise ValueError(f"Expected 1,158 distinct canonical Psalms; found {len(psalms)}")
    found = defaultdict(list)
    for psalm in psalms:
        book = psalm.get("book", {}).get("number")
        if not isinstance(book, int):
            raise ValueError(f"Psalm without book number: {psalm['id']}")
        for verse in psalm.get("verses", []):
            if not isinstance(verse.get("number"), int) or not isinstance(verse.get("text"), str):
                raise ValueError(f"Malformed verse in {psalm['id']}")
            normalized = norm(verse["text"])
            for entry, pattern in patterns:
                match = next((m for m in pattern.finditer(normalized)
                              if keeps_object_mention(entry["id"], normalized, m)), None)
                if match is None:
                    continue
                found[entry["id"]].append({
                    "recordId": psalm["id"],
                    "archangel": psalm["archangel"],
                    "psalm": psalm["number"],
                    "book": book,
                    "verse": verse["number"],
                    "excerpt": excerpt(verse["text"], match),
                })
    result_entries = []
    for definition, pattern in patterns:
        matches = found[definition["id"]]
        if not matches and definition["id"] not in MUST_SHOW:
            continue
        sources_by_id = {}
        for verse in matches:
            source = sources_by_id.setdefault(verse["recordId"], {
                "recordId": verse["recordId"], "archangel": verse["archangel"],
                "psalm": verse["psalm"], "book": verse["book"], "verses": [],
            })
            source["verses"].append({
                "number": verse["verse"], "excerpt": verse["excerpt"],
            })
        sources = sorted(sources_by_id.values(), key=lambda o: (o["book"], o["psalm"]))
        result_entries.append({
            "id": definition["id"], "label": definition["label"],
            "category": definition["category"], "psalmCount": len(sources),
            "verseCount": len(matches), "sources": sources,
        })
        for verse in matches:
            source_psalm = by_id[verse["recordId"]]
            text = next((v["text"] for v in source_psalm["verses"]
                         if v["number"] == verse["verse"]), None)
            if text is None or not any(
                keeps_object_mention(definition["id"], norm(text), match)
                for match in pattern.finditer(norm(text))
            ):
                raise ValueError(f"Unverifiable source for {definition['label']}: {verse}")
    result_entries.sort(key=lambda o: norm(o["label"]))
    result = {
        "schemaVersion": 1, "psalmCount": len(psalms),
        "testedObjectNames": len(definitions),
        "method": (
            "Les noms d’objets ont été recherchés dans les versets des 1 158 psaumes canoniques. "
            "Seules les mentions textuelles vérifiables sont présentées. Un objet peut être cité "
            "comme exemple, comparaison ou symbole ; son nom seul ne permet pas d’attribuer "
            "un enseignement particulier. Les extraits permettent de lire le contexte original."
        ),
        "categories": list(dict.fromkeys(d["category"] for d in definitions)),
        "entries": result_entries,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False,
                                      separators=(",", ":")) + "\n", encoding="utf-8")
    stats = {
        "psalms": len(psalms),
        "tested": len(definitions),
        "objects": sum(bool(entry["verseCount"]) for entry in result_entries),
        "links": sum(entry["verseCount"] for entry in result_entries),
    }
    print("Objets concrets Biblaw:", stats)
    print("Exemples demandés:",
          [(entry["label"], entry["verseCount"]) for entry in result_entries
           if entry["id"] in MUST_SHOW])
    print("Objets principaux:", ", ".join(
        f"{entry['label']} ({entry['verseCount']})"
        for entry in sorted(result_entries, key=lambda e: -e["verseCount"])[:35]))
    return stats


if __name__ == "__main__":
    generate(ROOT / "data" / "objects-public.json")
