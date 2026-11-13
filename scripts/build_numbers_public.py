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
    # Do not index "un seul", "une seule" or "premier jour": these are
    # usually ordinary grammar, not teachings about the number 1.
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
DAY = re.compile(r"\b(?:jours?|journees?|semaines?|mois|ans?|annees?|nuits?|fois)\b")
PRACTICE = re.compile(
    r"\b(?:exercices?|pratiques?|travaux|travail|meditations?|prieres?|"
    r"initiations?|consecrations?|etapes?|epreuves?|methodes?|"
    r"rituels?|celebrations?|preparations?|purifications?)\b"
)
SYMBOL = re.compile(
    r"\b(?:elements?|archanges?|mondes?|perles?|porteurs?|"
    r"forces?|vertus?|principes?|lois?|portes?|spheres?|etats?|"
    r"rayons?|piliers?|degres?|sceaux?|cercles?|corps|regnes?|"
    r"dimensions?|regles?|centres?|enseignements?|alliance|unite|"
    r"temples?|choses?)\b"
)
THEME = re.compile(r"\b(?:chiffre|chiffres|nombre|nombres|numerologie|numerologique|septenaire)\b")
MAX_NUMBER = 9999

# The one is indexed only when the text explicitly makes it symbolic,
# not when an indefinite article means "one thing".
ONE_EVIDENCE = {("book-05-psalm-028", 3)}
# Short editorial summaries checked against the verses listed alongside them.
# The wording attributes teachings to the Psalm, without adopting them as
# scientific facts or inventing a universal numerological meaning.
EDITORIAL = {
    1: {
        "title": "L’unité — le 4 qui s’élève vers le 1",
        "summary": "Dans le psaume 28 de Michaël (livre 5), le texte décrit le secret du 4 qui s’élève vers le 1 : les quatre éléments s’unissent dans le monde divin. Il s’agit d’une image d’unité, et non du simple fait qu’une chose est seule.",
        "sources": [("book-05-psalm-028", 3)],
    },
    3: {
        "title": "Les trois mondes et leurs rapports",
        "summary": "Dans le psaume 1 de Gabriel (livre 2), trois mondes sont distingués sous le monde divin : le monde spirituel, le monde aurique et le monde physique. Le chiffre 3 apparaît aussi dans d’autres comparaisons et indications concrètes.",
        "sources": [("book-02-psalm-001", 2)],
    },
    4: {
        "title": "Les quatre éléments et l’unité",
        "summary": "Michaël présente les quatre éléments comme la base d’un travail de purification et de construction intérieure (psaume 28, livre 5). Le texte évoque l’union des quatre éléments et leur rapport au divin. D’autres psaumes mentionnent aussi les quatre Archanges.",
        "sources": [("book-05-psalm-028", 1), ("book-05-psalm-028", 3)],
    },
    7: {
        "title": "Sept jours, sept années : cycles de purification",
        "summary": "Dans le psaume 45 de Gabriel (livre 6), le chiffre 7 est utilisé pour décrire des périodes de purification : 7 jours dans un cas et 7 années dans d’autres. Le psaume 41 du même livre évoque également 7 années de transformation. Il s’agit d’enseignements du texte, non de durées médicalement démontrées.",
        "sources": [("book-06-psalm-045", 8), ("book-06-psalm-045", 12)],
    },
    12: {
        "title": "Les douze perles et les douze porteurs",
        "summary": "Gabriel évoque son collier à 12 perles, lié dans son enseignement à un travail préparatoire et à 12 porteurs protecteurs du monde divin (psaume 200, livre 30). Cette figure n’est pas présentée comme une définition universelle du nombre 12.",
        "sources": [("book-30-psalm-200", 9), ("book-30-psalm-200", 31)],
    },
    21: {
        "title": "La méthode des vingt et un jours",
        "summary": "Gabriel donne une méthode de 21 jours pour apprendre à observer sa vie intérieure et à rencontrer son âme : s’arrêter, observer ses pensées et sentiments, puis créer un espace intérieur de consultation régulière (psaume 17, livre 2, versets 6–7). Ouriel évoque également une présence annoncée pendant 21 jours après une célébration (psaume 34, livre 8).",
        "sources": [("book-02-psalm-017", 6), ("book-02-psalm-017", 7),
                    ("book-08-psalm-034", 1)],
    },
}


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
        # A number is pertinent only when attached to a documented
        # symbolic structure, a practice or a temporal cycle. A random
        # count of people or objects is not a "meaning of the number".
        following = t[end:min(len(t), end+58)]
        preceding = t[max(0, start-26):start]
        context = preceding + " " + following
        is_duration = bool(DAY.search(following[:40]))
        practical = bool(PRACTICE.search(context))
        symbolic = bool(SYMBOL.search(context))
        duration_relevant = is_duration and not (
            re.search(r"\bil y a\s*$", preceding) or
            re.search(r"\ben l'an\s*$", preceding)
        )
        category = ("cycle" if duration_relevant else
                    "pratique" if practical else
                    "symbole" if symbolic else None)
        # 1 is treated only via explicitly verified symbolic verses below.
        picked.append({"number": number, "kind": kind,
                       "duration": duration_relevant,
                       "category": category,
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
                if m["number"] == 1:
                    if (psalm["id"], verse["number"]) not in ONE_EVIDENCE:
                        continue
                elif m["category"] is None:
                    continue
                occurrence = {
                    "recordId": psalm["id"],
                    "archangel": psalm["archangel"],
                    "psalm": psalm["number"],
                    "verse": verse["number"],
                    "duration": m["duration"],
                    "kind": m["kind"],
                    "category": m["category"] or "symbole",
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
        editorial = EDITORIAL.get(n)
        priority = list(editorial["sources"]) if editorial else []
        for rid, verse in priority:
            record = next((psalm for psalm in records if psalm["id"] == rid), None)
            selected = next((v for v in record["verses"] if v["number"] == verse), None) if record else None
            if not selected or not any(m["number"] == n for m in mentions(selected["text"])):
                raise ValueError(f"Editorial reference without named number {n}: {rid}, {verse}")
        candidate_examples = list(examples[n])
        if editorial:
            for rid, verse in reversed(priority):
                record = next(p for p in records if p["id"] == rid)
                text = next(v["text"] for v in record["verses"] if v["number"] == verse)
                candidate_examples.insert(0, {
                    "recordId": rid, "archangel": record["archangel"],
                    "psalm": record["number"], "verse": verse,
                    "duration": any(m["duration"] for m in mentions(text) if m["number"] == n),
                    "kind": "editorial", "excerpt": text[:360],
                })
        samples = []
        for item in (candidate_examples if editorial else
                     sorted(candidate_examples, key=lambda x: (not x["duration"], x["recordId"]))):
            if (item["recordId"], item["verse"]) in {
                (s["recordId"], s["verse"]) for s in samples
            }: continue
            samples.append(item)
            if len(samples) == 5: break
        categories = {ref["category"] for ref in passages}
        category_names = [
            name for category, name in [
                ("cycle", "des durées et des cycles"),
                ("pratique", "des pratiques et des étapes de travail"),
                ("symbole", "des images symboliques et des structures d’enseignement")
            ] if category in categories
        ]
        numbers.append({
            "value": n, "label": str(n),
            "title": editorial["title"] if editorial else
                " ; ".join(category_names).capitalize(),
            "summary": editorial["summary"] if editorial else (
                f"Le nombre {n} apparaît dans des passages qui évoquent " +
                ", ".join(category_names) + ". "
                "Les versets sont présentés sans attribuer au nombre un sens universel "
                "que le texte ne formule pas."),
            "references": passages, "examples": samples,
            "durationCount": len(durations),
            "practiceCount": sum(ref["category"] == "pratique" for ref in passages),
        })
    payload = {
        "schemaVersion": 1,
        "scope": "1 158 psaumes canoniques de Biblaw ; texte des versets uniquement.",
        "method": ("Sélection de passages qui associent explicitement un nombre à "
                   "des exercices, durées, cycles, éléments ou symboles. "
                   "Les chiffres servant seulement à compter des objets ou des personnes "
                   "sont écartés ; le 1 n’apparaît que lorsqu’une unité est enseignée. "
                   "Ces repérages sont documentaires et peuvent nécessiter une lecture du contexte."),
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
