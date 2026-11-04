#!/usr/bin/env python3
"""079: Verify note subjects against already-public note content only.

Topic labels are editorial tags justified by note text, not an authentication
of historic notes. Cross-references that contain no subject are kept separate.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def fold(value: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", str(value or "").replace("’", "'"))
        if unicodedata.category(c) != "Mn"
    ).casefold()


# Exact, documented textual evidence for every public subject label.
# A two-item list means both concepts must occur in each associated note.
EVIDENCE = {
    "Alliance théurgique": ["alliance théurgique"],
    "Ange de l’enthousiasme": ["Ange de l’enthousiasme"],
    "Ange de la maîtrise": ["Ange de la maîtrise"],
    "Ange de la paix": ["Ange de la paix"],
    "Ange de la puissance créatrice": ["Ange de la puissance créatrice"],
    "Ange de la sagesse": ["Ange de la sagesse"],
    "Ange de la subtilité": ["Ange de la subtilité"],
    "Ange de la vie": ["Ange de la vie"],
    "Animal totémique de Michaël": ["animal totémique", "Michaël"],
    "Calendrier maya et 2012": ["calendrier maya", "2012"],
    "Célébration de l’Archange Michaël": ["célébration", "Archange Michaël"],
    "Célébration de Raphaël": ["célébration", "Raphaël"],
    "Choix éditoriaux": ["nous avons préféré les conserver"],
    "Chouette": ["Chouette"],
    "Consécration à la prêtrise": ["consécration à la prêtrise"],
    "Deuxième marche de l’Initiation": ["deuxième marche de l’Initiation"],
    "Évolution de l’humanité et de la Terre": ["évolution de l’humanité", "de la terre"],
    "Flammes de la ménora": ["flamme", "ménora"],
    "Ménora": ["ménora"],
    "Nom de la Mère": ["Nom de la Mère"],
    "Premières éditions des psaumes": ["premières éditions des psaumes"],
    "Prêtrise": ["prêtrise"],
    "Prières présentées à Michaël": ["prières ont été présentées", "Michaël"],
    "Questions aux Archanges": ["questions d’Olivier Manitara aux Archanges"],
    "Ronde des Archanges": ["Ronde des Archanges"],
    "Terres esséniennes du Québec": ["terres esséniennes", "Québec"],
}

catalog = load("data/catalog.json")
public_ids = {
    Path(path).stem
    for path in catalog["records"]
    if path.startswith("data/notes/") and path.endswith(".json")
}
assert len(public_ids) == 11, "Expected exactly eleven previously public notes"

index = load("data/note-themes-public-073.json")
assert index["version"] == 2
assert index["notAnAuthentication"] is True
assert index["publicNoteCount"] == len(public_ids)
assert index["themedNoteCount"] == 10
themes = index["themes"]
labels = [t["label"] for t in themes]
assert set(labels) == set(EVIDENCE), "Unexpected, missing, or purely technical topics"
assert len(labels) == len(set(labels))
assert labels == sorted(labels, key=fold), "Topics not alphabetically ordered"
assert not any(
    re.match(r"^(versets?|psaume\s*\d+|\d{4}(?:-\d{4})?)$", label, re.I)
    for label in labels
), "Citation metadata must not masquerade as a subject"

themed_ids: set[str] = set()
summaries_only: set[str] = set()
for topic in themes:
    note_ids = topic["noteIds"]
    assert isinstance(note_ids, list) and note_ids
    assert len(note_ids) == len(set(note_ids)) == topic["count"]
    for ident in note_ids:
        assert ident in public_ids, f"Unexpected private or missing note: {ident}"
        note = load("data/notes/" + ident + ".json")
        assert note["id"] == ident and note["recordType"] == "note"
        actual = note.get("text") or note.get("summary") or ""
        assert actual, f"Missing text: {ident}"
        for phrase in EVIDENCE[topic["label"]]:
            assert fold(phrase) in fold(actual), (
                f"Unsubstantiated subject {topic['label']!r} in {ident}: {phrase!r}"
            )
        if not note.get("text"):
            summaries_only.add(ident)
        themed_ids.add(ident)

references = index["referenceNotes"]
assert references == [{
    "id": "book-17-psalm-130-note-001",
    "label": "Renvoi vers « L’heure du choix »",
}], "Only the already-public non-thematic cross-reference is allowed"
reference_ids = {x["id"] for x in references}
assert not (themed_ids & reference_ids)
assert themed_ids | reference_ids == public_ids
ref_text = load("data/notes/book-17-psalm-130-note-001.json")["text"]
assert "Voir le psaume 121" in ref_text and "L’heure du choix" in ref_text
assert len(summaries_only) == 1, "One public note still has a summary rather than a transcription"

print(
    f"079 PASS: {len(labels)} evidenced subjects, {len(themed_ids)} topical notes,"
    f" {len(reference_ids)} reference note, {len(summaries_only)} summary awaiting transcription"
)
