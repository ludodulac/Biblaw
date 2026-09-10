#!/usr/bin/env python3
"""Prove validated semantic relations remain isolated from public search."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data/thematic-index/theme-relations-validated.json"
RELATION_MARKERS = ("theme-relations-validated.json", "theme-relations-validated")

PUBLIC_CONSUMERS = [
    ROOT / "js/biblaw.js",
    ROOT / "scripts/build_browser_search_catalog.py",
    ROOT / "scripts/build_public_theme_directory.py",
    ROOT / "scripts/build_thematic_directory.py",
    ROOT / "scripts/build_thematic_search_index.py",
    ROOT / "scripts/build_thematic_connections.py",
    ROOT / "scripts/build_thematic_search_runtime.py",
    ROOT / "scripts/rebuild_thematic_derivatives.py",
    ROOT / "scripts/run_canonical_thematic_pipeline.py",
    ROOT / "scripts/build_pages_site.py",
]


def main() -> None:
    store = json.loads(STORE.read_text(encoding="utf-8"))
    assert store.get("publicSearchEffect") is False
    assert store.get("generated") is False

    consumers = []
    for path in PUBLIC_CONSUMERS:
        assert path.exists(), f"missing public consumer sentinel: {path.relative_to(ROOT)}"
        text = path.read_text(encoding="utf-8")
        if any(marker in text for marker in RELATION_MARKERS):
            consumers.append(str(path.relative_to(ROOT)))

    assert not consumers, (
        "validated relations unexpectedly consumed by public search/build path: "
        + ", ".join(consumers)
    )

    print(
        "Validated relation product isolation OK: "
        f"{len(store.get('relations', []))} approved relation(s); "
        "0 public search/build consumers"
    )


if __name__ == "__main__":
    main()
