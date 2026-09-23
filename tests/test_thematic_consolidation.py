#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_thematic_consolidation.py"
spec = importlib.util.spec_from_file_location("thematic_consolidation", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def stats(theme_id):
    return mod.consolidate(theme_id)["documentaryStats"]

def main():
    a = mod.consolidate("mort")
    b = mod.consolidate("mort")
    assert a == b, "generation must be deterministic"
    assert a["documentaryStats"] == {
        "totalRelations": 161, "central": 64, "important": 39, "related": 58
    }
    assert len(a["candidateEssentialPsalms"]["items"]) <= 10
    assert all(x["sourceRef"]["sourceFile"] and x["sourceRef"]["recordId"] and x["sourceRef"]["verseNumbers"]
               for x in a["principalEvidence"])
    source = SCRIPT.read_text(encoding="utf-8")
    for forbidden in ("book-18-psalm-130", "book-38-psalm-254", '"Vie"', '"Corps"', '"Conscience"'):
        assert forbidden not in source, f"hardcoded documentary choice: {forbidden}"
    assert stats("amour") == {"totalRelations": 9, "central": 3, "important": 6, "related": 0}
    assert stats("justice") == {"totalRelations": 3, "central": 1, "important": 2, "related": 0}
    assert stats("travail") == {"totalRelations": 39, "central": 9, "important": 12, "related": 18}
    assert stats("pardon-et-reparation") == {"totalRelations": 1, "central": 0, "important": 1, "related": 0}
    assert len(mod.consolidate("pardon-et-reparation")["principalEvidence"]) == 1
    artifact = json.loads((ROOT / "data/experiments/thematic-consolidation/mort.json").read_text(encoding="utf-8"))
    assert artifact == a, "checked-in Mort artifact must be generator output"
    print("PASS thematic consolidation prototype")

if __name__ == "__main__":
    main()
