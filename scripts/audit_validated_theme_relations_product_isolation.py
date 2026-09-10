#!/usr/bin/env python3
"""Prove validated semantic relations affect presentation only, never search resolution or ranking."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data/thematic-index/theme-relations-validated.json"
CANONICAL_MARKER = "theme-relations-validated.json"
PUBLIC_MARKER = "theme-relations-public.json"

SEARCH_CONSUMERS = [
    ROOT / "js/biblaw.js",
    ROOT / "scripts/build_browser_search_catalog.py",
    ROOT / "scripts/build_public_theme_directory.py",
    ROOT / "scripts/build_thematic_directory.py",
    ROOT / "scripts/build_thematic_search_index.py",
    ROOT / "scripts/build_thematic_connections.py",
    ROOT / "scripts/build_thematic_search_runtime.py",
    ROOT / "scripts/rebuild_thematic_derivatives.py",
    ROOT / "scripts/run_canonical_thematic_pipeline.py",
]
PRESENTATION_BUILDER = ROOT / "scripts/build_public_theme_relations.py"
PRESENTATION_CLIENT = ROOT / "js/theme-relations.js"


def main() -> None:
    store = json.loads(STORE.read_text(encoding="utf-8"))
    assert store.get("publicSearchEffect") is False
    assert store.get("generated") is False

    consumers = []
    for path in SEARCH_CONSUMERS:
        assert path.exists(), f"missing public search sentinel: {path.relative_to(ROOT)}"
        text = path.read_text(encoding="utf-8")
        if CANONICAL_MARKER in text or PUBLIC_MARKER in text:
            consumers.append(str(path.relative_to(ROOT)))

    assert not consumers, (
        "validated relations unexpectedly consumed by public search path: "
        + ", ".join(consumers)
    )

    assert PRESENTATION_BUILDER.exists()
    builder_text = PRESENTATION_BUILDER.read_text(encoding="utf-8")
    assert CANONICAL_MARKER in builder_text, "presentation builder must derive from canonical approved relations"

    assert PRESENTATION_CLIENT.exists()
    client_text = PRESENTATION_CLIENT.read_text(encoding="utf-8")
    assert PUBLIC_MARKER in client_text, "presentation client must consume only the public derivative"
    assert CANONICAL_MARKER not in client_text, "presentation client must never fetch canonical editorial evidence"

    print(
        "Validated relation boundary OK: "
        f"{len(store.get('relations', []))} approved relation(s); "
        "0 search consumers; 1 derived presentation path"
    )


if __name__ == "__main__":
    main()
