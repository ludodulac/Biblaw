#!/usr/bin/env python3
"""Build the presentation-only public view of human-approved theme relations.

The canonical editorial source keeps evidence and validation notes private to the repository layer.
This derivative exposes only relation endpoints and relation type so the browser can present an
explicit navigation aid. It must never become an input to search resolution or ranking.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "thematic-index" / "theme-relations-validated.json"
OUT = ROOT / "data" / "thematic-index" / "theme-relations-public.json"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert source.get("publicSearchEffect") is False

    relations = []
    for relation in source.get("relations", []):
        assert relation.get("relationStatus") == "relation_validated"
        assert relation.get("semanticClaim") is True
        assert relation.get("validation", {}).get("status") == "human-approved"
        relations.append({
            "sourceThemeId": relation["sourceThemeId"],
            "targetThemeId": relation["targetThemeId"],
            "relationType": relation["relationType"],
        })

    result = {
        "schemaVersion": 1,
        "generatedFrom": "data/thematic-index/theme-relations-validated.json",
        "manualEditingAllowed": False,
        "presentationOnly": True,
        "publicSearchEffect": False,
        "relationCount": len(relations),
        "relations": relations,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Built presentation-only relation view with {len(relations)} validated relations ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
