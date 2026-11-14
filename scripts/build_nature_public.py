#!/usr/bin/env python3
"""Index explicit mentions of natural elements in all canonical Biblaw Psalms.

This is a documentary lexical index: a verse mentioning "vent" may speak in
a metaphor, and such an occurrence is not presented as a doctrinal explanation.
The only textual sources are the 1,158 canonical Psalms in data/corpus/books/.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
LEXICON = ROOT / "data" / "nature-lexicon.json"
REQUIRED = {"riviere", "montagne", "nuage", "foret", "vent", "pluie"}


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
            raise ValueError(f"Empty natural-element spelling: {variant!r}")
        words.append(r"[\s\-\u2010-\u2015]+".join(re.escape(part) for part in pieces))
    words.sort(key=len, reverse=True)
    return re.compile(
        r"(?<![a-z0-9])(?:" + "|".join(dict.fromkeys(words)) + r")(?![a-z0-9])"
    )


def acceptable(element_id: str, text: str, match: re.Match) -> bool:
    """Exclude common non-nature uses where a noun has another sense."""
    preceding = text[max(0, match.start() - 42):match.start()]
    following = text[match.end():min(len(text), match.end() + 30)]
    word = text[match.start():match.end()]
    # Distinguish "il lave" (verb) from volcanic lava.
    if element_id == "lave" and re.search(
        r"(?:^|[^a-z])(?:il|elle|on|je|tu|se|me|te|nous|vous|ils|elles)\s+$", preceding
    ):
        return False
    # "Rose" can be a colour; "une rose" is a flower. "roses" may be adjective.
    if element_id == "rose" and not re.search(
        r"(?:^|[^a-z])(?:une|la|les|des|aux|de|du|ma|ta|sa|ses|mes|tes|ces|cette|leurs|"
        r"notre|votre|leur|quelques|plusieurs|fleur de)\s+$", preceding
    ):
        return False
    # "vague" can be an adjective.
    if element_id == "vague" and re.search(
        r"(?:^|[^a-z])(?:idee|pens[eé]e|vision|notion|image|concept)\s+$", preceding
    ):
        return False
    # "il gèle" vs gel, and "la glace" could be an ice cream or mirror.
    # They stay as lexical occurrences where context is not decisively clear.
    # "un air" is sometimes a tune or an expression, not atmospheric air.
    if element_id == "air" and (
        re.search(r"(?:^|[^a-z])(?:l'|de l'|un|cet)\s*air\s+(?:de|triste|joyeux)", preceding + word + following)
        or re.search(r"(?:^|[^a-z])(?:avoir|a|avait|pris|prend)\s+l'air\s+$", preceding)
    ):
        return False
    # "lumière du jour" is a physical description or image, still retained.
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
        raise ValueError("Unsupported nature lexicon schema")
    definitions = lexicon["entries"]
    ids = [entry["id"] for entry in definitions]
    if len(ids) != len(set(ids)) or not REQUIRED.issubset(set(ids)):
        raise ValueError("Duplicates or missing requested examples in nature lexicon")
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
                raise ValueError(f"Unverifiable natural-element citation {definition['label']} / {ref}")
        sources = sorted(per_psalm.values(), key=lambda r: (r["book"], r["psalm"]))
        entries.append({
            "id": definition["id"],
            "label": definition["label"],
            "category": definition["category"],
            "psalmCount": len(sources),
            "verseCount": len(rows),
            "sources": sources,
        })

    entries.sort(key=lambda r: normalize(r["label"]))
    public = {
        "schemaVersion": 1,
        "psalmCount": len(corpus),
        "testedNames": len(definitions),
        "method": (
            "Index des mentions explicites des éléments naturels dans les 1 158 psaumes canoniques. "
            "Les extraits reprennent le texte du verset et mènent à sa lecture complète. "
            "La présence d’un nom ne prouve pas qu’il désigne un phénomène physique : "
            "les images et significations spirituelles se comprennent dans leur contexte."
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
    print("Éléments naturels Biblaw:", stats)
    print("Exemples demandés:",
          [(e["label"], e["verseCount"]) for e in entries if e["id"] in REQUIRED])
    print("Éléments les plus cités:",
          ", ".join(f"{e['label']} ({e['verseCount']})"
                    for e in sorted(entries, key=lambda e: -e["verseCount"])[:30]))
    return stats


if __name__ == "__main__":
    generate(ROOT / "data" / "nature-public.json")
