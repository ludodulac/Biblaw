#!/usr/bin/env python3
"""Publish a documented guide to magic plus literal references from all Biblaw Psalms.

The curated guide cites exact canonical verses. The separate lexical concordance
records explicit words regardless of their symbolic or doctrinal meaning.
Neither is presented as proof that supernatural influences or spells are real.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
CURATED = ROOT / "data" / "magic-curated.json"

LEXICAL_GROUPS = (
    ("magie-magique", "Magie, magique, magiquement",
     r"\b(?:magie|magies|magique|magiques|magiquement)\b"),
    ("mages", "Mages, magiciens et magiciennes",
     r"\b(?:mage|mages|magicien|magiciens|magicienne|magiciennes)\b"),
    ("alchimie", "Alchimie et transmutation",
     r"\b(?:alchimie|alchimies|alchimique|alchimiques|alchimiste|alchimistes|transmutation|transmutations|transmuter|transmuer)\b"),
    ("rites", "Rites et rituels",
     r"\b(?:rite|rites|rituel|rituels|rituelle|rituelles)\b"),
    ("envoutement", "Envoûtement et désenvoûtement",
     r"\b(?:desenvout[a-z]*|envout[a-z]*)\b"),
    ("objets", "Objets et expressions magiques",
     r"\b(?:(?:baguette|baguettes|chaine|chaines|sceau|sceaux|signature|signatures|ecriture|ecritures|haricot|haricots|formule|formules)\s+(?:magique|magiques)|talisman|talismans|amulette|amulettes|sortilege|sortileges|sorcier|sorciere|sorciers|sorcieres|sorcellerie|incantation|incantations|enchantement|enchantements)\b"),
)


def normalize(text: str) -> str:
    value = text.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def excerpt(original: str, start: int, width: int = 220) -> str:
    """Excerpt from the canonical text around a match, not a paraphrase."""
    map_to_original = []
    for index, character in enumerate(original):
        map_to_original.extend([index] * len(normalize(character)))
    if not map_to_original:
        return ""
    center = map_to_original[min(start, len(map_to_original) - 1)]
    left = max(0, center - 65)
    right = min(len(original), left + width)
    left = max(0, right - width)
    if left:
        stop = original.find(" ", left, min(left + 25, len(original)))
        if stop != -1:
            left = stop + 1
    if right < len(original):
        stop = original.rfind(" ", max(left, right - 25), right)
        if stop > left:
            right = stop
    piece = re.sub(r"\s+", " ", original[left:right]).strip()
    return ("…" if left else "") + piece + ("…" if right < len(original) else "")


def generate(destination: Path) -> dict:
    guide = json.loads(CURATED.read_text(encoding="utf-8"))
    if guide.get("schemaVersion") != 1 or len(guide.get("parts", [])) < 8:
        raise ValueError("Magic-curated guide must contain at least eight categories")

    files = sorted(CORPUS.glob("book-*/psalm-*.json"))
    records = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    records = [record for record in records if record.get("recordType") == "psalm"]
    psalms = {record["id"]: record for record in records}
    if len(records) != 1158 or len(psalms) != 1158:
        raise ValueError("Expected 1,158 distinct canonical Psalms")

    checked_curated_verses = 0
    for part in guide["parts"]:
        if not part.get("label") or not part.get("entries"):
            raise ValueError("Invalid magic category")
        for item in part["entries"]:
            if not item.get("title") or not item.get("summary") or not item.get("references"):
                raise ValueError("Invalid magic subject")
            for ref in item["references"]:
                psalm = psalms.get(ref["recordId"])
                if not psalm:
                    raise ValueError(f"Unknown Psalm in magic guide: {ref}")
                verse_numbers = {v["number"] for v in psalm["verses"]}
                if not ref["verses"] or any(not isinstance(v, int) or v not in verse_numbers for v in ref["verses"]):
                    raise ValueError(f"Invalid cited verse in magic guide: {ref}")
                checked_curated_verses += len(ref["verses"])

    patterns = [(group_id, title, re.compile(expression))
                for group_id, title, expression in LEXICAL_GROUPS]
    mentions = {group_id: defaultdict(list) for group_id, _, _ in patterns}
    for record in records:
        for verse in record["verses"]:
            original = verse["text"]
            normalized = normalize(original)
            for group_id, _, pattern in patterns:
                match = pattern.search(normalized)
                if match is None:
                    continue
                mentions[group_id][record["id"]].append({
                    "number": verse["number"],
                    "excerpt": excerpt(original, match.start()),
                })

    entries = []
    all_refs = set()
    lexical_verses = 0
    for group_id, label, _ in patterns:
        sources = []
        for record_id, rows in mentions[group_id].items():
            record = psalms[record_id]
            # Each verse may appear in several search families but only once per family.
            numbers = [row["number"] for row in rows]
            if len(numbers) != len(set(numbers)):
                raise ValueError(f"Duplicate magic citation: {record_id}/{group_id}")
            sources.append({
                "recordId": record_id,
                "verses": numbers,
                "excerpt": rows[0]["excerpt"],
            })
            lexical_verses += len(numbers)
            all_refs.add(record_id)
        sources.sort(key=lambda s: (
            psalms[s["recordId"]]["book"]["number"],
            psalms[s["recordId"]]["number"]
        ))
        if not sources:
            continue
        verse_count = sum(len(source["verses"]) for source in sources)
        entries.append({
            "title": label,
            "summary": f"{len(sources)} psaumes et {verse_count} versets où ces mots apparaissent explicitement. Il s’agit de mentions textuelles, pas d’une validation de leur sens spirituel.",
            "kind": "lexical",
            "references": sources,
        })

    if len(entries) < 5 or lexical_verses < 150:
        raise ValueError(f"Magic concordance unexpectedly incomplete: {lexical_verses} verses")
    guide["parts"].append({
        "id": "toutes-les-mentions",
        "label": "Toutes les mentions dans les psaumes",
        "intro": "Inventaire de mots présents dans les 1 158 psaumes : magie, mage, alchimie, rituels, envoûtement et objets magiques. Ces recherches sont purement lexicales : un verset contenant un mot ne développe pas forcément tout le thème.",
        "entries": entries,
    })
    guide["psalmCount"] = len(psalms)
    guide["curatedVerseLinks"] = checked_curated_verses
    guide["lexicalVerseLinks"] = lexical_verses
    guide["lexicalPsalmCount"] = len(all_refs)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(guide, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "psalms": len(psalms),
        "parts": len(guide["parts"]),
        "curatedVerses": checked_curated_verses,
        "lexicalVerses": lexical_verses,
        "lexicalPsalms": len(all_refs),
    }


if __name__ == "__main__":
    output = ROOT / "data" / "magic-public.json"
    print(generate(output))
