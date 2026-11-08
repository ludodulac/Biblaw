#!/usr/bin/env python3
"""Book 02 final audit: Psalms 11–24 verse-grounded thematic coverage.

Read-only regression gate. Historical theme relations cannot disappear. New theme links
must be unique within each Psalm, anchored in an existing canonical verse, and projected
unchanged into both theme directories. The first-ten audit remains independently checked.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/thematic-index"
CORPUS = ROOT / "data/corpus/books/book-02"
ORIGINAL = {
    11: "cycles saisons harmonie",
    12: "alliance communaute quatre-archanges guerison",
    13: "corps volonte alliance",
    14: "choix organisation-de-la-vie ame fraternite-universelle",
    15: "coeur confiance anges amour",
    16: "guerison relations eau regnes",
    17: "ame calme lac discipline-des-21-jours",
    18: "opportunite hasard vigilance",
    19: "lumiere-et-obscurite maitrise passivite",
    20: "experience-directe fruit tradition affinite",
    21: "generosite don eau amour",
    22: "travail-sur-soi connaissance-de-soi discipline message-individuel",
    23: "monde-divin incarnation paix abstraction",
    24: "amour coeur semence don",
}
ADDED = {
    11: "pensee nature influences clairvoyance respiration realisation corps monde-divin",
    12: "incarnation conscience vie-interieure celebration union amour dignite lumiere benediction chaleur actes verite",
    13: "conscience vie-interieure courage engagement conviction harmonie creation monde-divin responsabilite",
    14: "vie-interieure priere meditation protection benediction lumiere conviction monde-divin realisation semence abstraction",
    15: "peur communication-avec-le-divin monde-divin partage protection benediction semence beaute inspiration",
    16: "conscience echange equilibre purification communication nature responsabilite ame sagesse maladie nuit inspiration",
    17: "meditation priere silence connaissance-de-soi sommeil preparation concentration discernement pensee nuit experience",
    18: "conscience choix action realisation inspiration lumiere amour creation pensee",
    19: "conscience pensee lumiere ombre responsabilite inconscience pouvoir peur",
    20: "connaissance-de-soi courage ame anges sens apparence-et-verite transmission vie-interieure sagesse souffrance experience lumiere",
    21: "abondance bonte responsabilite peur partage inspiration monde-divin pensee eveil",
    22: "monde-divin ame receptivite experience sens sagesse alliance affinite verite maitrise-de-soi detachement",
    23: "travail-sur-soi calme respect purete vie-interieure alliance realisation sagesse inspiration chaleur corps",
    24: "purification mystere croissance monde-divin union pensee experience ame bonheur joie beaute grandeur benediction",
}
EVIDENCE_SENTINELS = {
    11: {1: "pensée", 4: "corps"},
    12: {3: "danses", 4: "guérison"},
    13: {4: "volonté éveillée", 7: "monde divin"},
    14: {2: "médite", 9: "semence"},
    15: {8: "Anges", 11: "fleur"},
    16: {6: "purifie", 9: "responsabilité"},
    17: {6: "21 jours", 9: "lac"},
    18: {3: "choisis l'opportunité", 5: "réalisation"},
    19: {5: "inconscience", 7: "2 forces"},
    20: {10: "propres sens", 11: "Anges"},
    21: {8: "abondance", 12: "offrir"},
    22: {4: "affinités", 8: "langage"},
    23: {11: "la paix", 14: "chaleur"},
    24: {2: "purifier", 12: "Bénédiction"},
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", str(text or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).casefold()
    value = value.replace("œ", "oe").replace("æ", "ae")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def split_themes(value: str) -> set[str]:
    return set(value.split()) if value else set()


def main() -> None:
    book = load(INDEX / "books/book-02.json")
    assert book["book"]["number"] == 2
    assert len(book["psalmAnalyses"]) == 24
    assert set(ORIGINAL) == set(ADDED) == set(EVIDENCE_SENTINELS) == set(range(11, 25))

    directory = load(INDEX / "theme-directory.json")
    public = load(INDEX / "theme-directory-public.json")
    runtime = load(INDEX / "theme-search-runtime.json")
    canonical = {t["id"]: t for t in directory["themes"]}
    exposed = {t["id"]: t for t in public["themes"]}
    assert set(canonical) == set(exposed)
    assert len(canonical) == directory["themeCount"] == public["themeCount"] == runtime["themeCount"]
    assert len(canonical) >= 1265, len(canonical)

    first_ten = book["method"]["themeCoverageAudits"]
    assert len(first_ten) == 2
    assert [r["scope"] for r in first_ten] == [
        "book-02-psalms-001-010",
        "book-02-psalms-011-024",
    ]
    assert first_ten[0]["originalRelationCount"] == 38
    assert first_ten[0]["addedRelationCount"] == 105

    old_total = new_total = verse_total = 0
    for n in range(11, 25):
        a = book["psalmAnalyses"][n - 1]
        src = load(CORPUS / f"psalm-{n:03d}.json")
        assert a["number"] == n
        assert a["recordId"] == src["id"] == f"book-02-psalm-{n:03d}"
        assert a["title"] == src["title"]
        verses = {v["number"]: v["text"] for v in src["verses"]}
        verse_total += len(verses)
        for vno, needle in EVIDENCE_SENTINELS[n].items():
            assert normalize(needle) in normalize(verses[vno]), (n, vno, needle)

        prior = split_themes(ORIGINAL[n])
        added = split_themes(ADDED[n])
        assert not prior.intersection(added), n
        rels = a["themes"]
        by_id = {r["themeId"]: r for r in rels}
        assert len(rels) == len(by_id), (n, "duplicate relation")
        assert set(by_id) == prior.union(added), (n, sorted(set(by_id) ^ (prior | added)))
        old_total += len(prior)
        new_total += len(added)
        for id_, relation in by_id.items():
            refs = relation["verseNumbers"]
            assert refs and all(v in verses for v in refs), (n, id_, refs)
            assert relation["importance"] in {"central", "important", "related"}
            assert relation["directness"] in {"direct", "symbolic", "contextual", "editorial", "indirect"}
            assert relation["teaching"]
            if id_ in added:
                assert relation["teaching"].startswith("La Bible essénienne enseigne que "), (n, id_)
            for themes in (canonical, exposed):
                assert id_ in themes, (n, id_, "not in public directory")
                occurrences = [o for o in themes[id_]["occurrences"] if o["recordId"] == src["id"]]
                assert len(occurrences) == 1, (n, id_, "missing or duplicate in index")
                for field in ("importance", "teaching", "verseNumbers"):
                    assert occurrences[0][field] == relation[field], (n, id_, field, "projection drift")

    assert old_total == 52, old_total
    assert new_total == 145, new_total
    assert verse_total == 138, verse_total
    assert first_ten[1]["originalRelationCount"] == old_total
    assert first_ten[1]["addedRelationCount"] == new_total
    assert first_ten[1]["verifiedVerseCount"] == verse_total
    assert first_ten[1]["sourcePsalmsModified"] is False
    assert runtime["aliases"]["saisons"]["themeIds"] == ["saisons"]
    assert "guerison" in runtime["aliases"]["guerison"]["themeIds"]
    assert "discernement" in runtime["aliases"]["discernement"]["themeIds"]

    print(
        "BOOK 02 FULLY REVIEWED: last 14 Psalms, 138 unchanged verses, 52 untouched "
        "canonical relations + 145 evidenced additions; complete published theme "
        "projections checked without semantic auto-merge."
    )


if __name__ == "__main__":
    main()
