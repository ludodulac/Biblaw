#!/usr/bin/env python3
"""Independent prepublication review of extracted note candidates.

Read-only against every BIBLAW source. Compares extraction candidates with:
- the canonical Psalm to which they claim to belong;
- the Psalm's reciprocal noteIds;
- the official PDF source, when readable;
- the independently catalogued/validated external notes.

NOTE: source-text similarity is an automated indicator, NOT editorial approval.
Nothing here makes a candidate publishable automatically.
"""
from __future__ import annotations

import csv
import difflib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "Bible essénienne (classée par livres).pdf"
EXTRACTED = ROOT / "data/notes/books"
CANONICAL = ROOT / "data/corpus/books"
CATALOG = ROOT / "data/catalog.json"
OUT = ROOT / "reports/notes-extraites-060"
OUT.mkdir(parents=True, exist_ok=True)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(value: str) -> str:
    t = unicodedata.normalize("NFD", str(value or "").casefold())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("œ", "oe").replace("æ", "ae")
    return " ".join(re.findall(r"[a-z0-9]+", t))


def token_windows(text: str, width=9, max_windows=24):
    words = normalized(text).split()
    if len(words) < width:
        return [tuple(words)] if words else []
    total = len(words) - width + 1
    positions = sorted(set(round(i * (total - 1) / max(1, min(total, max_windows) - 1))
                           for i in range(min(total, max_windows))))
    return [tuple(words[p:p + width]) for p in positions]


def pdf_window_coverage(text: str, source: str) -> float:
    samples = token_windows(text)
    if not samples:
        return 0.0
    haystack = " " + normalized(source) + " "
    found = sum((" " + " ".join(w) + " ") in haystack for w in samples)
    return round(found / len(samples), 3)


def expected_psalm_path(psalm_id: str) -> Path | None:
    match = re.fullmatch(r"book-(\d+)-psalm-(\d+)", psalm_id)
    if not match:
        return None
    return CANONICAL / f"book-{match.group(1)}" / f"psalm-{match.group(2)}.json"


def main():
    extracted_files = sorted(EXTRACTED.glob("book-*/*-note-*.json"))
    catalog = read(CATALOG)
    published = [p for p in catalog.get("records", []) if p.startswith("data/notes/")]
    pub_notes = {read(ROOT / p)["id"]: read(ROOT / p) for p in published}
    extracted = [read(f) for f in extracted_files]
    if len(extracted_files) != 280 or len(pub_notes) != 11:
        raise SystemExit(f"Unexpected note inventory: nested={len(extracted_files)}, published={len(pub_notes)}")
    if any("data/notes/books/" in p for p in published):
        raise SystemExit("Detected unexpected auto-integration of extracted notes. Stop.")
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("Install PyMuPDF to verify textual PDF attestation") from exc
    if not SOURCE_PDF.is_file():
        raise SystemExit("Original PDF absent; do not mark any note verified")
    doc = fitz.open(str(SOURCE_PDF))
    pdf_cache = {}
    def context_at(page_number: int) -> str:
        if not isinstance(page_number, int):
            return ""
        if page_number in pdf_cache:
            return pdf_cache[page_number]
        text = doc[page_number].get_text(sort=True) if 0 <= page_number < len(doc) else ""
        pdf_cache[page_number] = text
        return text

    canonical_cache = {}
    rows = []
    for path, note in zip(extracted_files, extracted):
        issues = []
        info = note.get("appliesTo") or {}
        note_id = str(note.get("id") or "")
        target_id = str(info.get("recordId") or "")
        target_path = expected_psalm_path(target_id)
        if not target_path or not target_path.is_file():
            issues.append("missing_canonical_psalm")
            psalm = {}
        else:
            if target_id not in canonical_cache:
                canonical_cache[target_id] = read(target_path)
            psalm = canonical_cache[target_id]
            if note_id not in (psalm.get("noteIds") or []):
                issues.append("no_reciprocal_note_id")
            if psalm.get("archangel") != note.get("archangel"):
                issues.append("archangel_mismatch")
            m = re.fullmatch(r"book-(\d+)-psalm-(\d+)-note-(\d+)", note_id)
            if m and int(m.group(1)) != int(note.get("bookNumber") or -1):
                issues.append("book_number_mismatch")
        if note_id != path.stem:
            issues.append("id_does_not_match_filename")
        if note.get("recordType") != "note":
            issues.append("record_type_not_note")
        raw_text = str(note.get("text") or "")
        text = normalized(raw_text)
        if len(text) < 12:
            issues.append("empty_or_very_short_text")
        if len(raw_text) > 1500:
            issues.append("unusually_long_note")
        if re.search(r"\b(?:autres textes|table des matieres|sommaire des textes)\b", text):
            issues.append("possible_section_text_contamination")
        if not isinstance(info.get("marker"), int) or info["marker"] <= 0:
            issues.append("invalid_source_marker")
        ordinal = re.search(r"-note-(\d+)$", note_id)
        if ordinal and isinstance(info.get("marker"), int) and int(ordinal.group(1)) != info["marker"]:
            issues.append("source_marker_differs_from_note_ordinal")
        if note.get("source", {}).get("document") != SOURCE_PDF.name:
            issues.append("different_provenance_document")
        page = note.get("source", {}).get("pdfPage")
        if not isinstance(page, int) or page < 1 or page > len(doc) + 2:
            issues.append("invalid_pdf_source_page")
        source_pages = (psalm.get("source") or {}).get("pdfPages") or []
        if source_pages and page not in {*source_pages, *(x - 1 for x in source_pages),
                                       *(x + 1 for x in source_pages)}:
            issues.append("pdf_page_outside_psalm_source")
        # Source metadata page can refer either to the printed folio or a PDF
        # page index; inspect +/- 2, record the actual best hit offset.
        best, offset, around = 0.0, None, []
        if isinstance(page, int):
            for candidate in range(page - 3, page + 2):
                around.append(context_at(candidate))
                score = pdf_window_coverage(raw_text, context_at(candidate))
                if score > best:
                    best, offset = score, candidate + 1 - page
        if best < 0.8:
            issues.append("pdf_text_not_strongly_confirmed")
        published_note = pub_notes.get(note_id)
        exact_published_copy = (published_note is not None and
                                normalized(published_note.get("text")) == text)
        if published_note and not exact_published_copy:
            issues.append("published_note_text_differs")
        record = {
            "path": str(path.relative_to(ROOT)),
            "id": note_id,
            "target_psalm": target_id,
            "pdf_page": page,
            "best_pdf_page_delta": offset,
            "pdf_text_coverage": best,
            "text_characters": len(raw_text),
            "validation_status": (note.get("validation") or {}).get("status"),
            "is_published": bool(published_note),
            "exact_text_matches_published_note": exact_published_copy,
            "has_reciprocal_note_id": note_id in (psalm.get("noteIds") or []),
            "review_flags": issues,
        }
        rows.append(record)

    # A title's metadata is not enough to label a text 'validated': all
    # machine-extracted notes remain pending editorial review.
    count = Counter(flag for row in rows for flag in row["review_flags"])
    unlisted = [r for r in rows if not r["is_published"]]
    overlap = [r for r in rows if r["is_published"]]
    structural_flags = {
        "missing_canonical_psalm", "no_reciprocal_note_id",
        "archangel_mismatch", "book_number_mismatch",
        "id_does_not_match_filename", "record_type_not_note",
        "invalid_source_marker", "different_provenance_document",
        "invalid_pdf_source_page", "pdf_page_outside_psalm_source",
        "empty_or_very_short_text", "possible_section_text_contamination",
        "published_note_text_differs",
    }
    positive = [r for r in unlisted if r["pdf_text_coverage"] >= 0.8
                and not any(flag in structural_flags for flag in r["review_flags"])]
    blockers = [r for r in unlisted if r not in positive]
    summary = {
        "total_extracted": len(rows),
        "catalog_published": len(pub_notes),
        "source_id_overlap": len(overlap),
        "unpublished_unique_extracted": len(unlisted),
        "exact_published_overlap": sum(x["exact_text_matches_published_note"] for x in overlap),
        "source_supported_candidates_pending_human_review": len(positive),
        "requires_additional_source_or_structure_review": len(blockers),
        "automatically_approved_for_publication": 0,
        "publication_changes": 0,
        "pdf_pages": len(doc),
        "review_flags": dict(count.most_common()),
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "per-note.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUT / "per-note.csv").open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "review_flags": ";".join(row["review_flags"])})
    examples = []
    for reason, n in count.most_common(12):
        identifiers = [r["id"] for r in rows if reason in r["review_flags"]][:4]
        examples.append(f"| {reason} | {n} | {', '.join(identifiers)} |")
    md = [
        "# BIBLAW — audit des 280 notes extraites (mission 060)",
        "",
        "## Périmètre et réserve",
        "",
        "Audit technique sur le PDF présent dans le dépôt et sur les références des",
        "psaumes canoniques. **Aucune note n'a été publiée.**",
        "Correspondance textuelle automatisée ne vaut pas validation éditoriale.",
        "",
        f"- Notes extraites dans les livres : **{len(rows)}**",
        f"- Notes déjà publiées par ID : **{len(overlap)}**",
        f"- Notes supplémentaires hors catalogue : **{len(unlisted)}**",
        f"- Doubles déjà publiés avec texte identique : **{summary['exact_published_overlap']}**",
        f"- Candidates avec source PDF fortement appuyée et métadonnées cohérentes : **{len(positive)}** (relecture humaine requise)",
        f"- Candidates demandant d'abord un contrôle plus poussé : **{len(blockers)}**",
        "- Publiées automatiquement : **0**",
        "",
        "## Alertes techniques (plusieurs alertes possibles par note)",
        "",
        "| Alerte | Nombre | Exemples d'identifiants |",
        "|---|---:|---|",
        *examples,
        "",
        "## Méthode",
        "",
        "Le script vérifie chaque ID, son type, le psaume canonique de rattachement,",
        "le sens de la relation noteIds, la provenance PDF et des séquences de",
        "9 mots exactement attestées près de la page indiquée (±2).",
        "La couverture >=80% est un *indice*, pas une garantie.",
        "Les indices de rubrique/table des matières, d'incohérence de source",
        "et de données suspectes déclenchent une vérification supplémentaire.",
        "Le fichier per-note.csv contient une ligne pour chaque note.",
        "",
        "**Décision :** ne pas intégrer automatiquement les 269 notes avant validation",
        "éditoriale de leur forme et de leur rattachement.",
        "",
    ]
    (OUT / "RAPPORT.md").write_text("\n".join(md), encoding="utf-8")
    print("BIBLAW-NOTES-060 " + json.dumps(summary, ensure_ascii=False))
    print("REPORT_PUBLISHED: NO; CORPUS_MODIFIED: NO")
    doc.close()


if __name__ == "__main__":
    main()
