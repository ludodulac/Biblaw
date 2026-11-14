#!/usr/bin/env python3
"""Build the minimal GitHub Pages payload from an explicit production allow-list.

The repository contains large canonical, audit and research artefacts that are required for CI but
not by the browser. Publishing the repository root wastes upload time and exposes internal working
files. This staging step copies only assets referenced by the public search UI and the directly
accessible editorial validation workshop.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from build_public_note_extractions import generate as generate_public_notes
from build_animals_public import generate as generate_public_animals
from build_numbers_public import generate as generate_public_numbers
from build_masters_public import generate as generate_public_masters
from build_objects_public import generate as generate_public_objects
from build_nature_public import generate as generate_public_nature
from build_contrary_public import generate as generate_public_contrary

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"

PUBLIC_FILES = (
    ".nojekyll",
    "index.html",
    "validation.html",
    "Bible essénienne (classée par livres).pdf",
    "css/biblaw.css",
    "css/biblaw-light.css",
    "css/biblaw-animals.css",
    "css/biblaw-numbers.css",
    "css/biblaw-masters.css",
    "css/biblaw-objects.css",
    "css/biblaw-nature.css",
    "css/biblaw-contrary.css",
    "css/biblaw-donations.css",
    "css/theme-entry.css",
    "css/validation.css",
    "js/theme-suggestion-engine.js",
    "js/biblaw-pdf.js",
    "js/biblaw-faq.js",
    "js/biblaw-animals.js",
    "js/biblaw-numbers.js",
    "js/biblaw-masters.js",
    "js/biblaw-objects.js",
    "js/biblaw-nature.js",
    "js/biblaw-contrary.js",
    "js/biblaw-donations.js",
    "js/biblaw-autocomplete.js",
    "js/biblaw.js",
    "js/theme-relations.js",
    "js/theme-entry.js",
    "js/theme-rubrics.js",
    "js/validation.js",
    "data/browser-search-catalog.json",
    "data/note-themes-public-073.json",
    "data/faq-public-085.json",
    "data/faq-090-1.json",
    "data/faq-090-2.json",
    "data/faq-090-3.json",
    "data/faq-090-4.json",
    "data/faq-090-5.json",
    "data/faq-090-books.json",
    "data/faq-091-1.json",
    "data/faq-091-2.json",
    "data/faq-091-3.json",
    "data/faq-091-4.json",
    "data/faq-091-5.json",
    "data/faq-091-6.json",
    "data/faq-091-7.json",
    "data/faq-091-8.json",
    "data/faq-091-9.json",
    "data/faq-091-books.json",
    "data/faq-092.json",
    "data/faq-093.json",
    "data/faq-094.json",
    "data/faq-095.json",
    "data/faq-096.json",
    "data/faq-097.json",
    "data/faq-098.json",
    "data/faq-099.json",
    "data/faq-099-routing.json",
    "data/faq-100-merge.json",
    "data/faq-101-index.json",
    "data/lexical-expansion-runtime.json",
    "data/linguistic-sense-browser-runtime.json",
    "data/linguistic-grammar-browser-runtime.json",
    "data/thematic-index/theme-directory-public.json",
    "data/thematic-index/theme-relations-public.json",
    "data/thematic-index/theme-rubrics-public.json",
    "data/thematic-index/theme-search-runtime.json",
    "data/thematic-index/theme-semantic-navigation-public.json",
)

FORBIDDEN_PREFIXES = (
    ".github/",
    "progression/",
    "scripts/",
    "schemas/",
    "data/corpus/",
    "data/prayers/",
    "data/notes/",
    "data/thematic-index/books/",
    "data/thematic-index/source-packs/",
)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    total = 0
    for relative in PUBLIC_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"Missing Pages production asset: {relative}")
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        total += target.stat().st_size

    # Publish only a carefully limited and explicitly provisional projection:
    # the original unreviewed note files remain outside Pages.
    note_archive = OUT / "data" / "notes-extracted-public.json"
    note_stats = generate_public_notes(note_archive)
    assert note_stats["archiveCount"] == 280 and note_stats["alreadyPublishedCount"] == 11

    # Only publish the checked, compact projection; keep canonical Psalms
    # and editorial working files out of the Pages bundle.
    animals_public = OUT / "data" / "animals-public.json"
    animal_stats = generate_public_animals(animals_public)
    assert animal_stats["psalmCount"] == 1158 and animal_stats["totems"] >= 15
    assert animal_stats["others"] >= 35

    # Read-only numerical directory, generated from canonical verse text.
    numbers_public = OUT / "data" / "numbers-public.json"
    number_stats = generate_public_numbers(numbers_public)
    assert number_stats["psalms"] == 1158 and number_stats["numbers"] > 15
    assert number_stats["links"] > 100

    # Every master and verse reference is drawn directly from canonical Psalms.
    masters_public = OUT / "data" / "masters-public.json"
    master_stats = generate_public_masters(masters_public)
    assert master_stats["psalms"] == 1158 and master_stats["masters"] >= 4

    # Publish only attested concrete-object names, excerpted from canonical verses.
    objects_public = OUT / "data" / "objects-public.json"
    object_stats = generate_public_objects(objects_public)
    assert object_stats["psalms"] == 1158 and object_stats["tested"] > 150
    assert object_stats["objects"] > 20 and object_stats["links"] > 50

    # Landscape, vegetation and weather mentions, each tied to a real Psalm verse.
    nature_public = OUT / "data" / "nature-public.json"
    nature_stats = generate_public_nature(nature_public)
    assert nature_stats["psalms"] == 1158 and nature_stats["tested"] > 130
    assert nature_stats["present"] > 30 and nature_stats["citations"] > 100

    # A documentary, categorised glossary of explicitly attested expressions.
    # Neutral physical phenomena (e.g. electricity) are never claimed to be evil.
    contrary_public = OUT / "data" / "contrary-public.json"
    contrary_stats = generate_public_contrary(contrary_public)
    assert contrary_stats["psalms"] == 1158 and contrary_stats["tested"] > 120
    assert contrary_stats["present"] > 20 and contrary_stats["citations"] > 60

    staged = sorted(str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file())
    assert staged == sorted((*PUBLIC_FILES, "data/notes-extracted-public.json", "data/animals-public.json", "data/numbers-public.json", "data/masters-public.json", "data/objects-public.json", "data/nature-public.json", "data/contrary-public.json")), (
        "Pages staging contains a file outside the explicit allow-list"
    )
    # The donation menu is part of the public UI. Its CSS and JS must always be deployed.
    # Without these two assets the button appears grey/unstyled and never opens.
    assert (OUT / "css" / "biblaw-donations.css").is_file(), "Donations stylesheet missing from deployed site"
    assert (OUT / "js" / "biblaw-donations.js").is_file(), "Donations script missing from deployed site"
    public_html = (OUT / "index.html").read_text(encoding="utf-8")
    assert 'id="donateDetails"' in public_html, "Donations menu missing from deployed HTML"
    assert 'biblaw-donations.css?v=002' in public_html, "Donations stylesheet must be linked in deployed HTML"
    assert 'biblaw-donations.js?v=002' in public_html, "Donations script must be linked in deployed HTML"
    assert not any(path.startswith(FORBIDDEN_PREFIXES) for path in staged), "internal repository data leaked into Pages staging"
    assert "data/thematic-index/theme-relations-validated.json" not in staged, "canonical relation evidence leaked into Pages staging"

    print(f"Pages staging OK: {len(staged)} files, {total / (1024 * 1024):.1f} MiB")
    for path in staged:
        print(f"  {path}")


if __name__ == "__main__":
    main()
