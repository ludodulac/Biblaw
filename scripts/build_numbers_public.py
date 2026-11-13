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
    1: "un", 2: "deux", 3: "trois", 4: "quatre",
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
    if n in (0, 1): continue
    FORMS[french(n)] = n
FORMS.update({
    "vingt et une": 21, "trente et une": 31, "quarante et une": 41,
    "cinquante et une": 51, "soixante et une": 61, "cent": 100,
    "cents": 100, "mille": 1000,
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
    r"dimensions?|regles?|centres?|sens|enseignements?|alliance|unite|"
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
        "summary": "Les quatre éléments s’unissent dans le monde divin (Michaël, psaume 28, verset 3).",
        "sources": [("book-05-psalm-028", 3)],
    },
    3: {
        "title": "Les trois mondes et les trois centres",
        "summary": "Gabriel distingue les mondes spirituel, aurique et physique ; Raphaël évoque trois centres de l’être : pensée, ressenti et volonté.",
        "sources": [("book-02-psalm-001", 2), ("book-03-psalm-019", 5)],
    },
    4: {
        "title": "Les quatre éléments et l’unité",
        "summary": "Michaël décrit la communion avec les quatre éléments et leur union dans le monde divin (psaume 28).",
        "sources": [("book-05-psalm-028", 1), ("book-05-psalm-028", 3)],
    },
    7: {
        "title": "Sept jours et sept années",
        "summary": "Gabriel distingue des périodes de sept jours et de sept années dans son enseignement sur la purification (psaume 45).",
        "sources": [("book-06-psalm-045", 8), ("book-06-psalm-045", 12)],
    },
    12: {
        "title": "Les douze perles et les douze porteurs",
        "summary": "Gabriel associe les douze perles de son collier à douze porteurs protecteurs (psaume 200).",
        "sources": [("book-30-psalm-200", 9), ("book-30-psalm-200", 31)],
    },
    21: {
        "title": "La méthode des vingt et un jours",
        "summary": "Gabriel propose vingt et un jours d’observation intérieure pour apprendre à rencontrer son âme (psaume 17, versets 6–7).",
        "sources": [("book-02-psalm-017", 6), ("book-02-psalm-017", 7),
                    ("book-08-psalm-034", 1)],
    },
}



# Only words genuinely adjacent to a number give it a subject.
# Vague forms such as "3 choses" or "2 personnes" are excluded.
TOPIC_FORMS = {
  "centres":"centre centres",
  "sens":"sens",
  "mondes":"monde mondes",
  "éléments":"element elements",
  "archanges":"archange archanges",
  "forces":"force forces",
  "vertus":"vertu vertus",
  "principes":"principe principes",
  "lois":"loi lois",
  "portes":"porte portes",
  "états":"etat etats",
  "étapes":"etape etapes",
  "aspects":"aspect aspects",
  "rayons":"rayon rayons",
  "piliers":"pilier piliers",
  "cercles":"cercle cercles",
  "degrés":"degre degres",
  "sphères":"sphere spheres",
  "dimensions":"dimension dimensions",
  "couleurs":"couleur couleurs",
  "règnes":"regne regnes",
  "corps":"corps",
  "sceaux":"sceau sceaux",
  "temples":"temple temples",
  "perles":"perle perles",
  "porteurs":"porteur porteurs",
  "formes":"forme formes",
  "processus":"processus",
  "prières":"priere prieres",
  "méditations":"meditation meditations",
  "exercices":"exercice exercices",
  "initiations":"initiation initiations",
  "épreuves":"epreuve epreuves",
  "consécrations":"consecration consecrations",
  "rituels":"rituel rituels",
  "travaux":"travail travaux",
  "règles":"regle regles",
  "jours":"jour jours",
  "journées":"journee journees",
  "semaines":"semaine semaines",
  "mois":"mois",
  "années":"annee annees an ans",
  "nuits":"nuit nuits",
  "cycles":"cycle cycles",
  "phases":"phase phases",
  "passages":"passage passages",
  "enseignements":"enseignement enseignements",
}
TOPIC_BY_FORM = {form: label for label, forms in TOPIC_FORMS.items() for form in forms.split()}
ADJECTIVES = {"grand","grands","grande","grandes","petit","petits","petites",
              "premier","premiers","premiere","premieres","principal","principaux",
              "principales","different","differents","differentes","divin","divins",
              "divine","divines","sacre","sacres","sacrees","subtils","subtiles"}
TOPIC_DESCRIPTIONS = {
  (3, "centres"): "Pensée, ressenti et volonté (Raphaël, psaume 19).",
  (3, "mondes"): "Monde spirituel, monde aurique et monde physique (Gabriel, psaume 1).",
  (4, "éléments"): "Les quatre éléments dans l’enseignement de Michaël (psaume 28).",
  (12, "perles"): "Les douze perles du collier de Gabriel (psaume 200).",
  (21, "jours"): "Les vingt et un jours d’observation intérieure (Gabriel, psaume 17).",
}

def phrase_topics(text: str, number: int) -> list[str]:
    """Topic phrases ordered by their first actual occurrence in the verse."""
    normalized = norm(text)
    labels: list[str] = []
    for mention in mentions(text):
        if mention["number"] != number: continue
        next_words = re.findall(r"[a-z]+", normalized[mention["end"]:][:65])[:4]
        index = 0
        while index < min(2, len(next_words)) and next_words[index] in ADJECTIVES:
            index += 1
        if index < len(next_words):
            noun = next_words[index]
            if noun in TOPIC_BY_FORM:
                label = TOPIC_BY_FORM[noun]
                if label not in labels:
                    labels.append(label)
    return labels

def short_verse_phrase(text: str, number: int) -> str:
    """A short, literal passage around the number, never an invented theme.

    Long verses are cut at word boundaries; the title retains a recognizable
    fragment of the canonical verse. Numbers such as '3 choses' remain findable.
    """
    clean = " ".join(text.split())
    hit = next((item for item in mentions(clean) if item["number"] == number), None)
    if not hit:
        return clean[:92].rsplit(" ", 1)[0] + ("…" if len(clean) > 92 else "")
    # Normalization can alter offsets very slightly on rare ligatures; this
    # is used for presentation only, and verse links remain exact IDs.
    left = max(0, hit["start"] - 15)
    right = min(len(clean), max(hit["end"] + 66, left + 40))
    if left > 0:
        next_space = clean.find(" ", left, min(len(clean), left + 20))
        if next_space >= 0:
            left = next_space + 1
    if right < len(clean):
        last_space = clean.rfind(" ", left + 35, right)
        if last_space > left:
            right = last_space
    phrase = clean[left:right].strip(" ,;:.!?'«»\"")
    return ("…" if left else "") + phrase + ("…" if right < len(clean) else "")


def group_topics(number: int, references: list[dict], by_id: dict) -> list[dict]:
    """Partition the cited verses into distinct, named subjects.

    Each source verse belongs to exactly one group, even if it mentions several
    numeric subjects. Each source title is a short quote from that verse,
    rather than a repeated title such as '3 centres' for 34 different verses.
    """
    buckets: dict[str, dict] = defaultdict(dict)
    singletons: list[dict] = []
    used_titles: set[str] = set()
    for ref in references:
        verse = next(v for v in by_id[ref["recordId"]]["verses"]
                     if v["number"] == ref["verse"])
        labels = phrase_topics(verse["text"], number)
        # Prefer the first explicit expression in the verse. A later
        # expression cannot cause the same verse to be shown a second time.
        primary = labels[0] if labels else ""
        title = short_verse_phrase(verse["text"], number)
        if title.casefold() in used_titles:
            # Two verses can start with an identical formula. Show a longer,
            # authentic excerpt when possible rather than repeat its heading.
            title = context_excerpt(verse["text"], number, limit=185)
        if title.casefold() in used_titles:
            # Identical repeated quotations still refer to different Psalms.
            # Add the exact location only as the last disambiguation step.
            title += f" — psaume {ref['psalm']}, v. {ref['verse']}"
        used_titles.add(title.casefold())
        ref["title"] = title
        if primary:
            key = (ref["recordId"], ref["verse"])
            buckets[primary].setdefault(key, ref)
        else:
            singletons.append(ref)
    groups = [{
        "key": label, "label": f"{number} {label}",
        "summary": TOPIC_DESCRIPTIONS.get((number, label), ""),
        "references": list(buckets[label].values()),
    } for label in sorted(buckets, key=lambda k: (-len(buckets[k]), k))]
    # Do not create 'Autres passages': every remainder has its own short
    # clickable excerpt and is listed once, with one source link beneath it.
    for ref in singletons:
        groups.append({
            "key": f"extrait-{ref['recordId']}-{ref['verse']}",
            "label": ref["title"], "summary": "", "references": [ref],
        })
    all_locations = [(ref["recordId"], ref["verse"])
                     for group in groups for ref in group["references"]]
    assert len(all_locations) == len(references) == len(set(all_locations)), (
        f"Duplicate or lost verse in number {number} topics"
    )
    return groups


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
        # "21e siècle" is a historical date marker, not a symbolic cycle.
        if kind == "rang" and re.match(r"\s+siecle\b", following):
            continue
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
                       "start": start, "end": end,
                       "matched": verse_text[max(0,start):min(len(verse_text),end)]})
    return picked

def context_excerpt(text: str, number: int, limit: int = 440) -> str:
    """Show the teaching around the actual number, not just the verse start."""
    if len(text) <= limit: return text
    hit = next((m for m in mentions(text) if m["number"] == number), None)
    if not hit: return text[:limit].rstrip() + "…"
    start = max(0, hit["start"] - 165)
    stop = min(len(text), start + limit)
    if stop - start < limit: start = max(0, stop - limit)
    return ("…" if start else "") + text[start:stop].rstrip() + (
        "…" if stop < len(text) else ""
    )

def generate(destination: Path = OUTPUT) -> dict:
    records = []
    for path in sorted(CORPUS.glob("book-*/psalm-*.json")):
        psalm = json.loads(path.read_text(encoding="utf-8"))
        if psalm.get("recordType") == "psalm":
            records.append(psalm)
    if len(records) != 1158 or len({x["id"] for x in records}) != 1158:
        raise ValueError("Expected 1158 unique canonical Psalms")
    by_id = {record["id"]: record for record in records}
    by_number: dict[int, list] = defaultdict(list)
    conceptual: list[dict] = []
    examples: dict[int, list] = defaultdict(list)
    for psalm in records:
        for verse in psalm["verses"]:
            txt = verse["text"]
            for m in mentions(txt):
                if m["number"] == 0:
                    continue
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
                    examples[m["number"]].append({**occurrence, "excerpt": context_excerpt(txt, m["number"])})
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
        # Editorial examples may mention the number even if its context
        # is too far from the token for the automatic proximity check.
        # Include those specifically reviewed verses in the index too.
        editorial = EDITORIAL.get(n)
        if editorial:
            for rid, verse in editorial["sources"]:
                record = next((p for p in records if p["id"] == rid), None)
                selected = next((v for v in record["verses"] if v["number"] == verse), None) if record else None
                mentions_in_verse = [m for m in mentions(selected["text"]) if m["number"] == n] if selected else []
                if not mentions_in_verse:
                    raise ValueError(f"Editorial reference without named number {n}: {rid}, {verse}")
                if (rid, verse) not in grouped:
                    occurrence = mentions_in_verse[0]
                    grouped[(rid, verse)] = {
                        "recordId": rid, "archangel": record["archangel"],
                        "psalm": record["number"], "verse": verse,
                        "duration": occurrence["duration"], "kind": "editorial",
                        "category": occurrence["category"] or "symbole",
                    }
        passages = list(grouped.values())
        topics = group_topics(n, passages, by_id)
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
                    "kind": "editorial", "excerpt": context_excerpt(text, n),
                })
        samples = []
        valid_locations = set(grouped)
        for item in (candidate_examples if editorial else
                     sorted(candidate_examples, key=lambda x: (not x["duration"], x["recordId"]))):
            if (item["recordId"], item["verse"]) not in valid_locations:
                continue
            if (item["recordId"], item["verse"]) in {
                (s["recordId"], s["verse"]) for s in samples
            }: continue
            samples.append(item)
            if len(samples) == 5: break
        topic_reference_titles = {
            (ref["recordId"], ref["verse"]): ref["title"] for ref in passages
        }
        for sample in samples:
            sample["title"] = topic_reference_titles[
                (sample["recordId"], sample["verse"])
            ]
        categories = {ref["category"] for ref in passages}
        category_names = [
            name for category, name in [
                ("cycle", "des durées et des cycles"),
                ("pratique", "des pratiques et des étapes de travail"),
                ("symbole", "des images symboliques et des structures d’enseignement")
            ] if category in categories
        ]
        named = [t["label"] for t in topics if not t["key"].startswith("extrait-")]
        # A number without a documented teaching and without a named topic
        # should not acquire an invented general interpretation.
        if not editorial and not named and len(passages) < 2:
            continue
        numbers.append({
            "value": n, "label": str(n),
            "title": editorial["title"] if editorial else
                (", ".join(named[:2]) if named else "Passages à consulter"),
            "summary": editorial["summary"] if editorial else "",
            "topics": topics,
            "references": passages, "examples": samples,
            "durationCount": len(durations),
            "practiceCount": sum(ref["category"] == "pratique" for ref in passages),
        })
    payload = {
        "schemaVersion": 1,
        "scope": "1 158 psaumes canoniques de Biblaw ; texte des versets uniquement.",
        "method": ("Sélection de passages qui associent explicitement un nombre à "
                   "des exercices, durées, cycles, éléments ou symboles. "
                   "Les simples comptages et le zéro sans enseignement documenté "
                   "ne sont pas présentés. Les références sont regroupées par "
                   "expressions réellement présentes dans les psaumes, telles que « 3 centres ».") ,
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
    for n in (2, 3, 4, 5, 7, 12, 21, 40):
        match = next((e for e in numbers if e["value"] == n), None)
        if not match:continue
        print(f"EXEMPLES {n}: {len(match['references'])} versets "
              f"({match['durationCount']} durées)", flush=True)
        print("  GROUPES", [(t["label"],len(t["references"])) for t in match["topics"][:14]],flush=True)
        for item in match["examples"][:4]:
            print(" ", item["recordId"], item["verse"],repr(item["excerpt"][:185]),flush=True)
    return result

if __name__ == "__main__":
    generate()
