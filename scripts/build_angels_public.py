#!/usr/bin/env python3
"""Build documentary indexes of Gabriel's 12 Anges-perles and 144 Anges-fils.

Authoritative labels: data/anges-gabriel.json (2024 Google Drive document).
Evidence: all 1,158 canonical Psalms (data/corpus/books), never other corpora.
A lexical match does NOT assert that a Psalm speaks about an angelic being.
Every citation is verified against the exact source verse and deduplicated.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
VOCAB = ROOT / "data" / "anges-gabriel.json"


def norm(text: str) -> str:
    lowered = str(text).lower().replace("œ", "oe").replace("æ", "ae")
    return "".join(char for char in unicodedata.normalize("NFD", lowered)
                   if not unicodedata.combining(char))


def spellings(name: str) -> list[str]:
    word = norm(name)
    variants = [word]
    if not word.endswith(("s", "x", "z")):
        variants.append(word + "s")
    extras = {
        "cache": ["caches", "cachee", "cachees"],
        "travail": ["travaux"],
        "sacre": ["sacree", "sacres", "sacrees"],
        "bon sens": ["bons sens"],
        "bonne disposition": ["bonnes dispositions"],
        "soutien mutuel": ["soutiens mutuels"],
        "bien": ["biens"],
    }
    variants.extend(extras.get(word, []))
    return list(dict.fromkeys(variants))


def expression(name: str) -> re.Pattern[str]:
    variants = [
        r"[\s\-\u2010-\u2015]+".join(map(re.escape, spelling.split()))
        for spelling in spellings(name)
    ]
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(variants) + r")(?![a-z0-9])")


def excerpt(original: str, match: re.Match[str], max_length: int = 245) -> str:
    text = re.sub(r"\s+", " ", str(original)).strip()
    if len(text) <= max_length:
        return text
    index = 0
    position = 0
    for index, char in enumerate(text):
        width = len(norm(char))
        if position + width > match.start():
            break
        position += width
    begin = max(0, index - 75)
    end = min(len(text), begin + max_length)
    begin = max(0, end - max_length)
    if begin:
        cut = text.find(" ", begin)
        if cut >= 0 and cut - begin < 20:
            begin = cut + 1
    if end < len(text):
        cut = text.rfind(" ", begin, end)
        if cut > begin and end - cut < 20:
            end = cut
    return ("…" if begin else "") + text[begin:end].strip() + ("…" if end < len(text) else "")


def generate(destination: Path) -> dict:
    source = json.loads(VOCAB.read_text(encoding="utf-8"))
    perles = source["perles"]
    if source.get("schemaVersion") != 1 or len(perles) != 12:
        raise ValueError("Gabriel's 12 perles are required")
    definitions = []
    for parent in perles:
        if len(parent["fils"]) != 12:
            raise ValueError(f"Expected 12 children: {parent['label']}")
        definitions.append({"kind": "perle", "label": parent["label"], "parentId": None})
        for child in parent["fils"]:
            definitions.append({"kind": "fils", "label": child, "parentId": parent["id"]})
    names = [item["label"] for item in definitions]
    if len(names) != 156 or len(set(names)) != 156:
        raise ValueError("Expected 156 distinct labels: 12 perles and 144 children")
    patterns = [(definition, expression(definition["label"])) for definition in definitions]

    files = sorted(CORPUS.glob("book-*/psalm-*.json"))
    records = [json.loads(file.read_text(encoding="utf-8")) for file in files]
    records = [record for record in records if record.get("recordType") == "psalm"]
    by_id = {record["id"]: record for record in records}
    if len(records) != 1158 or len(by_id) != 1158:
        raise ValueError(f"Expected 1158 canonical Psalms, got {len(records)}")
    sources = {item["label"]: {} for item in definitions}
    for record in records:
        if not isinstance(record.get("book", {}).get("number"), int):
            raise ValueError(f"Invalid book: {record['id']}")
        for verse in record["verses"]:
            original = verse["text"]
            normalized = norm(original)
            for entry, regex in patterns:
                found = regex.search(normalized)
                if not found:
                    continue
                group = sources[entry["label"]].setdefault(record["id"], {
                    "recordId": record["id"],
                    "book": record["book"]["number"],
                    "archangel": record["archangel"],
                    "psalm": record["number"],
                    "verses": [],
                })
                group["verses"].append({
                    "number": verse["number"],
                    "excerpt": excerpt(original, found),
                })

    public = []
    for entry in definitions:
        groups = sorted(sources[entry["label"]].values(),
                        key=lambda item: (item["book"], item["psalm"]))
        verse_count = sum(len(item["verses"]) for item in groups)
        for group in groups:
            original = by_id[group["recordId"]]
            indexed = {verse["number"]: verse["text"] for verse in original["verses"]}
            seen = set()
            for verse in group["verses"]:
                number = verse["number"]
                if number in seen or number not in indexed:
                    raise ValueError(f"Duplicate or nonexistent verse: {original['id']}:{number}")
                seen.add(number)
                if not expression(entry["label"]).search(norm(indexed[number])):
                    raise ValueError(f"Unverified match: {entry['label']} in {original['id']}:{number}")
                if not verse["excerpt"] or len(verse["excerpt"]) > 250:
                    raise ValueError(f"Malformed excerpt: {entry['label']} in {original['id']}")
        public.append({**entry, "psalmCount": len(groups),
                       "verseCount": verse_count, "sources": groups})
    data = {
        "schemaVersion": 1,
        "psalmCount": len(records),
        "perlesCount": 12,
        "filsCount": 144,
        "entryCount": len(public),
        "method": ("Recherche lexicale dans les 1 158 psaumes canoniques, "
                   "sans synonymes inventés ni lecture spirituelle automatique. "
                   "Chaque occurrence renvoie au livre, au psaume et au verset exact."),
        "entries": public,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8")
    stats = {"psalms": len(records), "perles": 12, "fils": 144,
             "labelsFound": sum(item["verseCount"] > 0 for item in public),
             "citations": sum(item["verseCount"] for item in public)}
    print("Anges de Gabriel Biblaw:", stats)
    return stats


if __name__ == "__main__":
    generate(ROOT / "data" / "angels-public.json")
