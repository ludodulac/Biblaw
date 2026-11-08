#!/usr/bin/env python3
"""Applique les associations thématiques justifiées par les versets du livre 12, sans altérer les psaumes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMATIC = ROOT / "data/thematic-index"
BOOK = THEMATIC / "books/book-12.json"
BASE = THEMATIC / "audits/book12-original-relations.json"
CORPUS = ROOT / "data/corpus/books/book-12"
PARTS = ROOT / "scripts/book12-work"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

book = load(BOOK)
assert book["book"]["number"] == 12 and book["book"]["archangel"] == "ouriel"
psalms = {p["number"]: p for p in book["psalmAnalyses"]}
assert sorted(psalms) == list(range(52, 78)), sorted(psalms)
if not BASE.exists():
    frozen = {str(n): {rel["themeId"]: rel for rel in p["themes"]} for n, p in psalms.items()}
    assert sum(map(len, frozen.values())) == 79, "Historical theme relation count changed"
    save(BASE, {"book": 12, "archangel": "ouriel", "originalRelationCount": 79, "psalms": frozen})
baseline = load(BASE)
assert baseline["originalRelationCount"] == 79
for n, p in psalms.items():
    original = baseline["psalms"][str(n)]
    assert len(p["themes"]) == len(original), ("unexpected preexisting changes", n)
    for tid, relation in original.items():
        assert next((x for x in p["themes"] if x["themeId"] == tid), None) == relation, ("historical changed", n, tid)

verses_for = {}
verse_total = 0
for n, p in psalms.items():
    source = load(CORPUS / f"psalm-{n:03d}.json")
    assert source["id"] == p["recordId"], (n, "record")
    assert source["archangel"] == "ouriel", (n, "archangel")
    assert source["title"] == p["title"], (n, "title")
    valid = {v["number"] for v in source["verses"]}
    assert valid == set(range(1, len(valid)+1)), n
    verses_for[n] = valid
    verse_total += len(valid)

parts = sorted(PARTS.glob("part*.json"))
assert len(parts) == 3, [str(p) for p in parts]
new_count = 0
for path in parts:
    for n, tid, refs, label, teaching, directness, importance in load(path):
        assert n in psalms
        assert refs and len(refs) == len(set(refs)) and set(refs) <= verses_for[n], (n, tid, refs)
        assert label and len(teaching) > 20
        assert not any(t["themeId"] == tid for t in psalms[n]["themes"]), (n, tid, "duplicate")
        psalms[n]["themes"].append({
            "themeId": tid,
            "label": label,
            "importance": importance,
            "directness": directness,
            "verseNumbers": refs,
            "teaching": "La Bible essénienne enseigne que " + teaching
        })
        new_count += 1
assert new_count == 314, new_count
book["method"].setdefault("themeCoverageAudits", []).append({
    "scope": "book-12-psalms-052-077",
    "reviewedOn": "2026-11-08",
    "source": "data/corpus/books/book-12/psalm-052.json through psalm-077.json",
    "approach": "conservative-editorial-verse-evidence",
    "originalRelationCount": 79,
    "addedRelationCount": new_count,
    "verifiedVerseCount": verse_total,
    "sourcePsalmsModified": False
})
book["bookSynthesis"]["centralAxis"] = (
    "Synthèse d'indexation descriptive et non exclusive : le livre 12, « Les clés du bonheur », "
    "met en relation la fidélité aux lois divines, le bonheur, l'écoute des avertissements avant "
    "l'épreuve, les actes concrets et l'accomplissement des œuvres, la libération des illusions "
    "et de la dispersion, le sens spirituel de Blanche-Neige, la pensée, le souffle, la nourriture, "
    "les engagements, l'alliance avec les règnes de la Mère et la responsabilité d'offrir un corps "
    "terrestre à la Lumière."
)
book["bookSynthesis"]["majorThemes"] = [
    "bonheur", "epreuve", "discernement", "actes", "perfection",
    "blanche-neige", "illusion", "lois-divines", "conscience",
    "pensee-respiration-nourriture", "engagement", "fidelite",
    "pouvoir-createur", "oeuvre", "karma", "simplicite-efficace",
    "quatre-elements", "guerison", "ecologie", "regnes",
    "mere", "argent", "capital-spirituel", "priere-et-reponse",
    "trois-reponses", "ronde-des-archanges", "nation-essenienne",
    "corps-de-la-lumiere", "soutien-mutuel"
]
save(BOOK, book)
print(f"BOOK12 EDITORIAL: 26 psalms, {verse_total} verses, 79 historical unchanged, {new_count} added, {79+new_count} total")
