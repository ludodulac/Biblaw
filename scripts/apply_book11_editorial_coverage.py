#!/usr/bin/env python3
"""Applique une seule fois les associations éditoriales du livre 11 (Raphaël)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMATIC = ROOT / "data/thematic-index"
BOOK = THEMATIC / "books/book-11.json"
BASE = THEMATIC / "audits/book11-original-relations.json"
CORPUS = ROOT / "data/corpus/books/book-11"
PARTS = ROOT / "scripts/book11-work"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

book = load(BOOK)
assert book["book"]["number"] == 11 and book["book"]["archangel"] == "raphael"
psalms = {p["number"]: p for p in book["psalmAnalyses"]}
assert sorted(psalms) == list(range(49, 75)), sorted(psalms)
if not BASE.exists():
    frozen = {str(n): {rel["themeId"]: rel for rel in p["themes"]} for n, p in psalms.items()}
    assert sum(map(len, frozen.values())) == 80, "The historical baseline has changed"
    save(BASE, {"book": 11, "archangel": "raphael", "originalRelationCount": 80, "psalms": frozen})
baseline = load(BASE)
assert baseline["originalRelationCount"] == 80
for n, p in psalms.items():
    assert len(p["themes"]) == len(baseline["psalms"][str(n)]), ("unexpected pre-existing additions", n)
    for tid, relation in baseline["psalms"][str(n)].items():
        assert next((x for x in p["themes"] if x["themeId"] == tid), None) == relation, ("historical difference", n, tid)

valid_verses = {}
verse_count = 0
for n, p in psalms.items():
    source = load(CORPUS / f"psalm-{n:03d}.json")
    assert source["id"] == p["recordId"] and source["archangel"] == "raphael"
    assert source["title"] == p["title"]
    refs = {v["number"] for v in source["verses"]}
    assert refs == set(range(1, len(refs) + 1)), n
    valid_verses[n] = refs
    verse_count += len(refs)

files = sorted(PARTS.glob("part*.json"))
assert len(files) == 3, [str(p) for p in files]
relation_count = 0
for path in files:
    for n, theme_id, refs, label, teaching, directness, importance in load(path):
        assert n in psalms and set(refs) <= valid_verses[n], (n, theme_id, refs)
        assert refs and len(set(refs)) == len(refs)
        assert label.strip() and len(teaching) > 25
        assert not any(rel["themeId"] == theme_id for rel in psalms[n]["themes"]), (n, theme_id, "duplicate")
        psalms[n]["themes"].append({
            "themeId": theme_id, "label": label, "importance": importance,
            "directness": directness, "verseNumbers": refs,
            "teaching": "La Bible essénienne enseigne que " + teaching
        })
        relation_count += 1
assert relation_count == 322, relation_count
book["method"].setdefault("themeCoverageAudits", []).append({
    "scope": "book-11-psalms-049-074", "reviewedOn": "2026-11-08",
    "source": "data/corpus/books/book-11/psalm-049.json through psalm-074.json",
    "approach": "conservative-editorial-verse-evidence",
    "originalRelationCount": 80, "addedRelationCount": relation_count,
    "verifiedVerseCount": verse_count, "sourcePsalmsModified": False
})
book["bookSynthesis"]["centralAxis"] = (
    "Synthèse d'indexation descriptive, non exclusive : le livre 11 de Raphaël "
    "invite à sortir de l'illusion par une pensée claire, le discernement, le regard vrai, "
    "la subtilité des sens, la fidélité à la Lumière, l'authenticité des actes, la responsabilité "
    "des créations, la persévérance dans l'épreuve, le dialogue avec la nature et le service collectif."
)
book["bookSynthesis"]["majorThemes"] = [
    "discernement", "pensee", "pensee-creatrice", "illusion", "apparences",
    "authenticite", "responsabilite", "epreuve", "monde-invisible",
    "sens-subtils", "corps-etherique", "finesse-et-subtilite", "verite",
    "purete", "perseverance", "fidelite", "simplicite", "nature-vivante",
    "langage-des-mondes", "regard", "ronde-des-archanges", "service", "air"
]
save(BOOK, book)
print(f"BOOK11 EDITORIAL: 26 psalms, {verse_count} verses, 80 historical preserved, "
      f"{relation_count} added, {80 + relation_count} total")
