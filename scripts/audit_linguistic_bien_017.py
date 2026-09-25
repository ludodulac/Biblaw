#!/usr/bin/env python3
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SOURCE_SHA = "5c755358f5cda20db52a2d748cbb2664a1831dcc"
OUTPUT = ROOT / "bien-017-raw-observation.json"

spec = importlib.util.spec_from_file_location(
    "occurrence_index", ROOT / "scripts" / "build_linguistic_occurrence_index.py"
)
occurrence_index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(occurrence_index)

def observe(surface):
    rows = occurrence_index.occurrences(surface)
    return {
        "normalizedSurface": surface,
        "count": len(rows),
        "observedSurfaceForms": sorted({row["surfaceForm"] for row in rows}),
        "occurrences": rows,
    }

executed_head_sha = os.environ.get("GITHUB_SHA", "LOCAL")
report = {
    "purpose": "BIBLAW-PILOTE-ADVERSARIAL-BIEN-017-C raw corpus observation only",
    "BASELINE_SOURCE_SHA": BASELINE_SOURCE_SHA,
    "HARNESS_HEAD_SHA": executed_head_sha,
    "EXECUTED_HEAD_SHA": executed_head_sha,
    "corpusContract": {
        "generator": "scripts/build_linguistic_occurrence_index.py",
        "catalog": "data/catalog.json",
        "source": "canonical-catalog-records",
        "tokenization": "existing generator unchanged",
    },
    "totalsMerged": False,
    "engineClassificationRun": False,
    "bien": observe("bien"),
    "biens": observe("biens"),
}

OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"SURFACE_BIEN_COUNT = {report['bien']['count']}")
print(f"SURFACE_BIENS_COUNT = {report['biens']['count']}")
print("TOTALS_NOT_MERGED = YES")
print("ENGINE_CLASSIFICATION_RUN = NO")
print(f"BASELINE_SOURCE_SHA = {BASELINE_SOURCE_SHA}")
print(f"EXECUTED_HEAD_SHA = {executed_head_sha}")
