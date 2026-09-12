#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# Reproductible audit only: this script reads canonical data and writes a disposable report.
ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "thematic-index"
CORPUS = ROOT / "data" / "corpus" / "books"
OUT = ROOT / "ange-audit-pilot.json"
TARGET = "ange"
LEXICAL_RE = re.compile(r"(?<!\w)(ange|anges)(?!\w)", re.IGNORECASE)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

analyses = {}
all_theme_ids = Counter()
all_theme_labels = defaultdict(set)
for path in sorted((INDEX / "books").glob("book-*.json")):
    book = load(path)
    bnum = int(book["book"]["number"])
    for ps in book.get("psalmAnalyses", []):
        key = (bnum, int(ps["number"]))
        analyses[key] = {"book": book["book"], **ps}
        for th in ps.get("themes", []):
            all_theme_ids[th["themeId"]] += 1
            all_theme_labels[th["themeId"]].add(th.get("label", ""))

corpus = {}
for path in sorted(CORPUS.glob("book-*/psalm-*.json")):
    ps = load(path)
    key = (int(ps["book"]["number"]), int(ps["number"]))
    corpus[key] = ps

assert len(analyses) == 1158, len(analyses)
assert len(corpus) == 1158, len(corpus)

current_target = []
for key, analysis in sorted(analyses.items()):
    for th in analysis.get("themes", []):
        if th.get("themeId") == TARGET:
            ps = corpus[key]
            current_target.append({
                "recordId": analysis["recordId"],
                "archangel": ps["archangel"],
                "book": ps["book"],
                "number": ps["number"],
                "title": ps["title"],
                "importance": th.get("importance"),
                "teaching": th.get("teaching"),
                "verseNumbers": th.get("verseNumbers", []),
                "passages": [v for v in ps.get("verses", []) if v.get("number") in set(th.get("verseNumbers", []))],
            })

lexical_candidates = []
form_counts = Counter()
for key, ps in sorted(corpus.items()):
    matches = []
    for verse in ps.get("verses", []):
        found = [m.group(1).lower() for m in LEXICAL_RE.finditer(verse.get("text", ""))]
        if found:
            form_counts.update(found)
            matches.append({"number": verse["number"], "text": verse["text"], "forms": found})
    if not matches:
        continue
    analysis = analyses[key]
    themes = analysis.get("themes", [])
    lexical_candidates.append({
        "recordId": analysis["recordId"],
        "archangel": ps["archangel"],
        "book": ps["book"],
        "number": ps["number"],
        "title": ps["title"],
        "lexicalOccurrenceCount": sum(len(m["forms"]) for m in matches),
        "matchingVerses": matches,
        "alreadyExactAnge": any(t.get("themeId") == TARGET for t in themes),
        "currentThemes": themes,
        "fullVerses": ps.get("verses", []),
    })

neighbor_ids = []
for tid, count in sorted(all_theme_ids.items()):
    labels = sorted(x for x in all_theme_labels[tid] if x)
    token = norm(tid)
    label_tokens = [norm(x) for x in labels]
    if "ange" in token or any("ange" in x for x in label_tokens):
        neighbor_ids.append({"themeId": tid, "labels": labels, "psalmCount": count})

validated = load(INDEX / "theme-relations-validated.json")
relations = []
for rel in validated.get("relations", []):
    if rel.get("sourceThemeId") == TARGET or rel.get("targetThemeId") == TARGET:
        relations.append(rel)

rel_by_neighbor = defaultdict(list)
for rel in relations:
    other = rel.get("targetThemeId") if rel.get("sourceThemeId") == TARGET else rel.get("sourceThemeId")
    rel_by_neighbor[other].append(rel)
for row in neighbor_ids:
    row["validatedRelationWithAnge"] = rel_by_neighbor.get(row["themeId"], [])

report = {
    "schemaVersion": 1,
    "baseSha": "715a6db113fba20aa5deebb93385f869b0227a5f",
    "targetThemeId": TARGET,
    "rules": {
        "lexical": "Unicode word-token match, case-insensitive, forms exactly 'ange' or 'anges'; titles/notes are excluded; only canonical verse text is scanned.",
        "semantic": "lexical presence is candidate generation only; no automatic thematic attachment or semantic relation is created.",
    },
    "counts": {
        "analyzedPsalms": len(analyses),
        "corpusPsalms": len(corpus),
        "exactAngeIndexedPsalms": len(current_target),
        "lexicalCandidatePsalms": len(lexical_candidates),
        "lexicalOccurrences": sum(x["lexicalOccurrenceCount"] for x in lexical_candidates),
        "lexicalForms": dict(sorted(form_counts.items())),
    },
    "currentExactAnge": current_target,
    "lexicalCandidates": lexical_candidates,
    "lexicallyNeighboringThemes": neighbor_ids,
    "validatedRelationsInvolvingExactAnge": relations,
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report["counts"], ensure_ascii=False))
print(f"WROTE {OUT.name}")
