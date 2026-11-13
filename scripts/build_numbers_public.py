#!/usr/bin/env python3
"""Read-only index of explicit numbers in all 1,158 canonical Biblaw Psalms.

Never infer numerical symbolism. Scan only the verse *text*, not Psalm
numbering, editorial notes or file names. Every public link is checked
against a canonical verse; no canonical text is modified.
"""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "books"
OUTPUT = ROOT / "data" / "numbers-public.json"

UNITS = {
    0: "zero", 1: "un", 2: "deux", 3: "trois", 4: "quatre",
    5: "cinq", 6: "six", 7: "sept", 8: "huit", 9: "neuf",
    10: "dix", 11: "onze", 12: "douze", 13: "treize",
    14: "quatorze", 15: "quinze", 16: "seize", 17: "dix sept",
    18: "dix huit", 19: "dix neuf"
}
TENS = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante"}

def french(n: int) -> str:
    if n in UNITS: return UNITS[n]
    if n in TENS: return TENS[n]
    if n < 70:
        tens, unit = divmod(n, 10)
        return TENS[tens * 10] + (" et un" if unit == 1 else " " + UNITS[unit])
    if n < 80:
        return "soixante" + (" et onze" if n == 71 else " " + french(n - 60))
    if n == 80: return "quatre vingt"
    return "quatre vingt " + french(n - 80)

def norm(value: str) -> str:
    value = value.casefold().replace("œ", "oe").replace("æ", "ae")
    value = "".join(c for c in unicodedata.normalize("NFKD", value)
                    if not unicodedata.combining(c))
    return value.replace("-", " ").replace("’", "'").replace("\u00a0", " ")

# Explicit spellings (0–99), hundreds and thousands; avoid "un"/"une" as
# standalone articles. Ordinals are only included when numeric (e.g. "3e")
# or for transparent "premier jour" / "première semaine" phrases.
FORMS: dict[str, int] = {}
for n in range(0, 100):
    if n == 1: continue
    FORMS[french(n)] = n
FORMS.update({
    "vingt et une": 21, "trente et une": 31, "quarante et une": 41,
    "cinquante et une": 51, "soixante et une": 61, "cent": 100,
    "cents": 100, "mille": 1000, "zero": 0, "zéro": 0,
    "une seule": 1, "un seul": 1, "un unique": 1, "une unique": 1,
    "premier jour": 1, "premiere semaine": 1, "premier mois": 1,
})
for k in (2, 3, 4, 5, 6, 7, 8, 9):
    FORMS[french(k) + " cent"] = k * 100
    FORMS[french(k) + " cents"] = k * 100
    FORMS[french(k) + " mille"] = k * 1000

# Match longest expressions first; never count "quatre" and "vingt" inside
# "quatre-vingt". Numeric form 21 is distinct from a page or psalm ID.
WORDS = re.compile(
    r"(?<![a-z0-9])(?:" +
    "|".join(re.escape(word) for word in sorted(FORMS, key=len, reverse=True)) +
    r")(?![a-z0-9])"
)
DIGITS = re.compile(r"(?<![a-z0-9])(?:\d{1,3}(?:[ \u00a0]\d{3})+|\d{1,4})(?![a-z0-9])")
RANK = re.compile(r"(?<![a-z0-9])(\d{1,3})(?:er|ere|e|eme)(?![a-z0-9])")
DAY = re.compile(r"\b(?:jour|jours|journee|journees|semaine|semaines|mois|an|ans|annee|annees|nuit|nuits|fois)\b")
THEME = re.compile(r"\b(?:chiffre|chiffres|nombre|nombres|numerolog|septenaire)\w*\b")
STRIP_PUNCT = " ,.;:!?()[]«»\"'"
MAX_NUMBER = 9999

def mentions(verse_text: str) -> list[dict]:
    t = norm(verse_text)
    matches: list[tuple[int, int, int, str]] = []
    for m in WORDS.finditer(t):
        number = FORMS[m.group()]
        matches.append((m.start(), m.end(), number, "lettres"))
    for m in RANK.finditer(t):
        number = int(m.group(1))
        if number <= MAX_NUMBER:
            matches.append((m.start(), m.end(), number, "rang"))
    for m in DIGITS.finditer(t):
        number = int(m.group().replace(" ", ""))
        if number <= MAX_NUMBER:
            matches.append((m.start(), m.end(), number, "chiffres"))
    matches.sort(key=lambda row: (row[0], -(row[1] - row[0])))
    picked: list[dict] = []
    occupied: list[tuple[int, int]] = []
    for start, end, number, kind in matches:
        if any(start < b and end > a for a, b in occupied): continue
        # Ignore footnote markers adjoining letters (already covered by
        # boundary checks); reject typographic decimals like "1,5".
        if kind == "chiffres" and ((start and t[start-1] in ".,") or
                                  (end < len(t) and t[end] in ".,"
                                   and end + 1 < len(t) and t[end+1].isdigit())):
            continue
        occupied.append((start, end))
        following = t[end:min(len(t), end+32)]
        is_duration = bool(DAY.search(following))
        picked.append({"number": number, "kind": kind,
                       "duration": is_duration,
                       "matched": verse_text[max(0,start):min(len(verse_text),end)]})
    return picked

def generate(destination: Path = OUTPUT) -> dict:
    records = []
    for path in sorted(CORPUS.glob("book-*/psalm-*.json")):
        psalm = json.loads(path.read_text(encoding="utf-8"))
        if psalm.get("recordType") == "psalm":
            records.append(psalm)
    if len(records) != 1158 or len({x["id"] for x in records}) != 1158:
        raise ValueError("Expected 1158 unique canonical Psalms")
    by_number: dict[int, list] = defaultdict(list)
    conceptual: list[dict] = []
    examples: dict[int, list] = defaultdict(list)
    for psalm in records:
        for verse in psalm["verses"]:
            txt = verse["text"]
            for m in mentions(txt):
                occurrence = {
                    "recordId": psalm["id"],
                    "archangel": psalm["archangel"],
                    "psalm": psalm["number"],
                    "verse": verse["number"],
                    "duration": m["duration"],
                    "kind": m["kind"],
                }
                by_number[m["number"]].append(occurrence)
                if len(examples[m["number"]]) < 40:
                    examples[m["number"]].append({**occurrence, "excerpt": txt[:360]})
            if THEME.search(norm(txt)):
                conceptual.append({
                    "recordId": psalm["id"], "archangel": psalm["archangel"],
                    "psalm": psalm["number"], "verse": verse["number"],
                })
    numbers = []
    for n, refs in sorted(by_number.items()):
        # avoid duplicate references for multiple occurrences of the same
        # number within one verse while preserving duration if any.
        grouped = {}
        for ref in refs:
            key = (ref["recordId"], ref["verse"])
            if key not in grouped:
                grouped[key] = dict(ref)
            else:
                grouped[key]["duration"] |= ref["duration"]
        passages = list(grouped.values())
        psalm_count = len({r["recordId"] for r in passages})
        durations = [x for x in passages if x["duration"]]
        # Pick genuinely observed contexts, prioritising durations / actions;
        # never fabricate a symbolic meaning from the value of a number.
        samples = []
        for item in sorted(examples[n], key=lambda x: (not x["duration"], x["recordId"])):
            if (item["recordId"], item["verse"]) in {
                (s["recordId"], s["verse"]) for s in samples
            }: continue
            samples.append(item)
            if len(samples) == 5: break
        numbers.append({
            "value": n, "label": str(n),
            "summary": (f"Le nombre {n} est mentionné explicitement dans "
                        f"{len(passages)} verset{'s' if len(passages)>1 else ''} "
                        f"de {psalm_count} psaume{'s' if psalm_count>1 else ''}. "
                        "Les passages ci-dessous montrent ses usages dans le texte ; "
                        "ils ne lui attribuent pas automatiquement une valeur symbolique."),
            "references": passages, "examples": samples,
            "durationCount": len(durations),
        })
    payload = {
        "schemaVersion": 1,
        "scope": "1 158 psaumes canoniques de Biblaw ; texte des versets uniquement.",
        "method": ("Recherche des nombres écrits en chiffres et en lettres (0–99, "
                   "centaines et milliers usuels) et de quelques rangs chiffrés ; "
                   "« un / une » isolés sont exclus pour éviter les articles. "
                   "Les listes sont descriptives, pas une interprétation numérologique."),
        "psalmCount": len(records),
        "entries": numbers,
        "numberTerms": conceptual,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    result = {
        "psalms": len(records), "numbers": len(numbers),
        "links": sum(len(x["references"]) for x in numbers),
        "conceptualVerses": len(conceptual),
        "numbersWithDurations": sum(bool(x["durationCount"]) for x in numbers),
        "outputBytes": destination.stat().st_size,
    }
    print("Biblaw chiffres/nombres:", result, flush=True)
    for n in (3, 4, 7, 12, 21, 40):
        match = next((e for e in numbers if e["value"] == n), None)
        if not match:continue
        print(f"EXEMPLES {n}: {len(match['references'])} versets "
              f"({match['durationCount']} durées)", flush=True)
        for item in match["examples"][:4]:
            print(" ", item["recordId"], item["verse"],repr(item["excerpt"][:185]),flush=True)
    return result

if __name__ == "__main__":
    generate()
