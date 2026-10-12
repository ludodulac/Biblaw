#!/usr/bin/env python3
"""Build grammar choices from canonical occurrence pilots and supervision reviews."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/linguistic-grammar-browser-runtime.json"
REVIEWS = ROOT / "data/linguistic/review"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def build():
    forms = []
    for review_path in sorted(REVIEWS.glob("*-grammar-review-*.json")):
        review = read(review_path)
        pilot = read(ROOT / review["sourcePilot"])
        inventory = read(ROOT / review["sourceOccurrences"])
        lexicon = read(ROOT / "data/linguistic/lexicon.json")
        form = review["normalizedForm"]
        lexical = next(x for x in lexicon["entries"] if x["normalizedForm"] == form)
        allowed = {(a["lemma"], a["partOfSpeech"]) for a in lexical["possibleAnalyses"]}
        occurrences = {x["occurrenceId"]: x for x in inventory["occurrences"]}
        decisions = {x["occurrenceId"]: x for x in review["decisions"]}
        groups = defaultdict(list)
        for analysis in pilot["analyses"]:
            oid = analysis["occurrenceId"]
            if analysis["segmentation"] == "COMPOUND_ELEMENT":
                assert oid not in decisions
                continue
            decision = decisions.get(oid)
            if decision:
                assert analysis["category"] == decision["sourcePilotCategory"] == "UNKNOWN"
                lemma, pos = decision["selectedLemma"], decision["selectedPartOfSpeech"]
            else:
                if analysis["category"] in ("UNKNOWN", "AMBIGUOUS"):
                    continue
                lemma, pos = analysis["lemma"], analysis["partOfSpeech"]
            assert (lemma, pos) in allowed
            assert oid in occurrences
            groups[(lemma, pos)].append(occurrences[oid])
        analyses = []
        for (lemma, pos), rows in sorted(groups.items()):
            by_record = defaultdict(list)
            for row in rows:
                by_record[row["recordId"]].append(row)
            records = []
            for record_id, entries in sorted(by_record.items()):
                verse_numbers = sorted({int(x["verseNumber"]) for x in entries if x["verseNumber"] is not None})
                records.append([record_id, len(entries), verse_numbers])
            analyses.append({"lemma": lemma, "partOfSpeech": pos, "occurrenceCount": len(rows),
                             "occurrenceIds": sorted(x["occurrenceId"] for x in rows), "records": records})
        forms.append({"normalizedForm": form, "analyses": analyses})
    return {"v": 1, "purpose": "linguistic-grammar-browser-runtime",
            "generator": "scripts/build_linguistic_grammar_browser_runtime.py", "forms": sorted(forms, key=lambda x:x["normalizedForm"])}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(build(), ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf-8")
    print("GRAMMAR_RUNTIME_BUILD=PASS", args.output)

if __name__ == "__main__":
    main()
