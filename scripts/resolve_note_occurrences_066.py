#!/usr/bin/env python3
"""Compatibilité de notes : regroupe par pied imprimé sans élire un ID ni effacer un composite."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/notes/physical-occurrences-066.json"
def note_path(note_id):
    parts = note_id.split("-")
    if len(parts) != 6 or parts[0] != "book" or parts[2] != "psalm" or parts[4] != "note" or not all(parts[i].isdigit() for i in (1,3,5)):
        raise ValueError("Invalid note ID: " + note_id)
    return ROOT / "data/notes/books" / ("book-" + parts[1]) / (note_id + ".json")
def load_note(note_id):
    note = json.loads(note_path(note_id).read_text(encoding="utf-8"))
    if note.get("id") != note_id:
        raise ValueError("ID mismatch: " + note_id)
    return note
def load_groups():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != 1:
        raise ValueError("Unknown compatibility version")
    groups, seen = manifest["groups"], set()
    for g in groups:
        a, b = g["members"]
        if a == b or a in seen or b in seen:
            raise ValueError("Duplicate member: " + a + " / " + b)
        seen.update((a, b))
        na, nb = load_note(a), load_note(b)
        if any(n["source"]["pdfPage"] != g["pdfPage"] for n in (na, nb)):
            raise ValueError("Printed page mismatch")
        ta, tb = na["text"], nb["text"]
        if g["relation"] == "identical-text":
            if ta != tb: raise ValueError("Text not identical: " + g["occurrenceId"])
        elif g["relation"] == "short-text-prefix-of-composite":
            if not (ta.startswith(tb) or tb.startswith(ta)): raise ValueError("Prefix mismatch: " + g["occurrenceId"])
        else:
            raise ValueError("Unknown relation")
    return groups
def resolve(note_ids):
    groups = load_groups()
    lookup = {member: g for g in groups for member in g["members"]}
    result, visited = [], set()
    for id_ in note_ids:
        group = lookup.get(id_)
        key = group["occurrenceId"] if group else id_
        if key in visited: continue
        visited.add(key)
        members = group["members"] if group else [id_]
        result.append({"physicalId":key,"memberRecords":{m:load_note(m) for m in members}})
    return result
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--ids", nargs="*")
    args = parser.parse_args()
    groups = load_groups()
    if args.check: print(f"PASS {len(groups)} pieds / {sum(len(g['members']) for g in groups)} IDs originaux préservés")
    if args.ids: print(json.dumps(resolve(args.ids),ensure_ascii=False,indent=2))
    if not (args.check or args.ids): parser.print_help()
