#!/usr/bin/env python3
"""Build the public documentary-rubric projection from the editorial source."""
from __future__ import annotations

import json
from pathlib import Path

from validate_theme_rubrics import load_json, validate

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "thematic-index" / "theme-rubrics.json"
TARGET = ROOT / "data" / "thematic-index" / "theme-rubrics-public.json"


def build(data: dict) -> dict:
    validate(data)
    return {
        "schemaVersion": data["schemaVersion"],
        "generatedFrom": "data/thematic-index/theme-rubrics.json",
        "rubrics": [
            {
                "rubricId": rubric["rubricId"],
                "themeId": rubric["themeId"],
                "label": rubric["label"],
                "recordIds": rubric["recordIds"],
            }
            for rubric in data["rubrics"]
            if rubric["validationStatus"] == "validated"
        ],
    }


if __name__ == "__main__":
    output = build(load_json(SOURCE))
    TARGET.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {TARGET.relative_to(ROOT)} with {len(output['rubrics'])} validated rubric(s)")
