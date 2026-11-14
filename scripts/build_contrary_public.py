#!/usr/bin/env python3
"""Build a sourced index of words/expressions under the heading "Forces contraires".

The categories are documentary reading aids, NOT a theological assertion that
all indexed terms, beings or physical phenomena are intrinsically evil. For
instance "électricité" is a neutral physical phenomenon. The exact source
verses are always shown, including context to check the intended meaning.
Only the 1,158 canonical Psalms are indexed; no fabricated references.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
LEXICON = ROOT / "data" / "contrary-lexicon.json"
REQUIRED = {"usurpateur", "tenebres", "esprits-tenebreux", "electricite"}


def normalize(value: str) -> str:
    value = value.casefold().replace("œ", "oe").replace("æ", "ae")
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def make_pattern(variants: list[str]) -> re.Pattern:
    words = []
    for variant in variants:
        pieces = re.split(r"[\s\-\u2010-\u2015]+", normalize(variant.strip()))
        if not pieces or not all(pieces):
            raise ValueError(f"Empty contrary-term spelling: {variant!r}")
        words.append(r"[\s\-\u2010-\u2015]+".join(re.escape(part) for part in pieces))
    words.sort(key=len, reverse=True)
    return re.compile(
        r"(?<![a-z0-9])(?:" + "|".join(dict.fromkeys(words)) + r")(?![a-z0-9])"
    )


def acceptable(term_id: str, normalized: str, match: re.Match) -> bool:
    """Reject a few frequent grammatical uses of ambiguous isolated words.

    This filter cannot replace human interpretation of a spiritual passage.
    The public interface explicitly presents citations as lexical matches.
    """
    before = normalized[max(0, match.start() - 45):match.start()]
    # "Il envie" is a verb; the user expects the notion of envy, not a
    # potentially unrelated conjugated use (and other noun uses remain).
    if term_id == "envie" and re.search(
        r"(?:^|[^a-z])(?:il|elle|je|tu|on|nous|vous|ils|elles)\s+$", before
    ):
        return False
    # "Une ruine" or "les ruines" names ruin, but "il ruine" is verbal.
    if term_id == "ruine" and re.search(
        r"(?:^|[^a-z])(?:il|elle|je|tu|on|nous|vous|ils|elles)\s+$", before
    ):
        return False
    # The noun "conflit" is not a classification of a dark entity; that
    # distinction belongs to the explanatory note, never the search filter.
    return True


def short_excerpt(original: str, found: re.Match, width: int = 245) -> str:
    """Show the original wording (apart from whitespace), centering the match."""
    text = re.sub(r"\s+", " ", original).strip()
    if len(text) <= width:
        return text
    # Map accent-normalized indices back to the original Unicode string.
    positions = []
    for i, char in enumerate(original):
        positions.extend([i] * len(normalize(char)))
    if not positions:
        return text[:width]
    anchor = positions[min(found.start(), len(positions) - 1)]
    start = max(0, anchor - 85)
    end = min(len(original), start + width)
    start = max(0, end - width)
    if start:
        boundary = original.find(" ", start, min(len(original), start + 20))
        if boundary != -1:
            start = boundary + 1
    if end < len(original):
        boundary = original.rfind(" ", max(start, end - 20), end)
        if boundary > start:
            end = boundary
    fragment = re.sub(r"\s+", " ", original[start:end]).strip()
    return ("…" if start else "") + fragment + ("…" if end < len(original) else "")


def generate(destination: Path) -> dict:
    lexicon = json.loads(LEXICON.read_text(encoding="utf-8"))
    if lexicon.get("schemaVersion") != 1:
        raise ValueError("Unsupported contrary lexicon schema")
    definitions = lexicon["entries"]
    ids = [entry["id"] for entry in definitions]
    if len(ids) != len(set(ids)) or not REQUIRED.issubset(set(ids)):
        raise ValueError("Duplicates or missing requested terms in contrary lexicon")
    patterns = [(entry, make_pattern(entry["forms"])) for entry in definitions]
    files = sorted(CORPUS.glob("book-*/psalm-*.json"))
    corpus = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    corpus = [psalm for psalm in corpus if psalm.get("recordType") == "psalm"]
    psalms = {psalm["id"]: psalm for psalm in corpus}
    if len(corpus) != 1158 or len(psalms) != 1158:
        raise ValueError(f"Canonical source must contain 1,158 distinct Psalms: {len(corpus)}")

    mentions = defaultdict(list)
    for psalm in corpus:
        book = psalm.get("book", {}).get("number")
        if not isinstance(book, int):
            raise ValueError(f"Missing book number in {psalm['id']}")
        for verse in psalm["verses"]:
            original = verse["text"]
            normalized = normalize(original)
            for entry, regex in patterns:
                found = next(
                    (m for m in regex.finditer(normalized) if acceptable(entry["id"], normalized, m)),
                    None
                )
                if found is None:
                    continue
                mentions[entry["id"]].append({
                    "recordId": psalm["id"],
                    "book": book,
                    "archangel": psalm["archangel"],
                    "psalm": psalm["number"],
                    "verse": verse["number"],
                    "excerpt": short_excerpt(original, found),
                })

    entries = []
    for definition, regex in patterns:
        rows = mentions[definition["id"]]
        if not rows and definition["id"] not in REQUIRED:
            continue
        per_psalm = {}
        for ref in rows:
            source = per_psalm.setdefault(ref["recordId"], {
                "recordId": ref["recordId"],
                "archangel": ref["archangel"],
                "psalm": ref["psalm"],
                "book": ref["book"],
                "verses": [],
            })
            source["verses"].append({"number": ref["verse"], "excerpt": ref["excerpt"]})
            original_record = psalms[ref["recordId"]]
            actual = next((v["text"] for v in original_record["verses"] if v["number"] == ref["verse"]), None)
            if actual is None or not any(
                acceptable(definition["id"], normalize(actual), match)
                for match in regex.finditer(normalize(actual))
            ):
                raise ValueError(f"Unverifiable contrary-term citation {definition['label']} / {ref}")
        sources = sorted(per_psalm.values(), key=lambda r: (r["book"], r["psalm"]))
        entries.append({
            "id": definition["id"],
            "label": definition["label"],
            "category": definition["category"],
            "definition": definition["definition"],
            "psalmCount": len(sources),
            "verseCount": len(rows),
            "sources": sources,
        })

    entries.sort(key=lambda r: normalize(r["label"]))
    public = {
        "schemaVersion": 1,
        "psalmCount": len(corpus),
        "testedNames": len(definitions),
        "notice": lexicon["editorialNotice"],
        "method": (
            "Index de termes précis et de leurs formes grammaticales attestées dans les "
            "1 158 psaumes canoniques. Chaque extrait est relié au verset exact. "
            "Ce classement lexical ne prouve ni une présence surnaturelle, ni un jugement "
            "de valeur porté par le psaume : lisez chaque passage en contexte."
        ),
        "categories": list(dict.fromkeys(d["category"] for d in definitions)),
        "entries": entries,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(public, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    stats = {
        "psalms": len(corpus),
        "tested": len(definitions),
        "present": sum(e["verseCount"] > 0 for e in entries),
        "citations": sum(e["verseCount"] for e in entries),
    }
    print("Forces contraires Biblaw:", stats)
    print("Exemples demandés:",
          [(e["label"], e["verseCount"]) for e in entries if e["id"] in REQUIRED])
    print("Termes les plus cités:",
          ", ".join(f"{e['label']} ({e['verseCount']})"
                    for e in sorted(entries, key=lambda e: -e["verseCount"])[:30]))
    return stats


if __name__ == "__main__":
    generate(ROOT / "data" / "contrary-public.json")
