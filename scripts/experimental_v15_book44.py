#!/usr/bin/env python3
"""Projection et recherche expérimentales V1.5 pour le livre 44 uniquement."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data/documentary-extractions/psalms/book-44"
EXPERIMENT_DIR = ROOT / "experiments/v1_5-book-44"
OUTPUT = EXPERIMENT_DIR / "subjects.json"
THEMATIC = ROOT / "data/thematic-index/books/book-44.json"
QUERIES = EXPERIMENT_DIR / "comparative-queries.json"
EXPECTED_PSALMS = list(range(260, 286))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold().replace("œ", "oe")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def source_paths() -> list[Path]:
    return [SOURCE_DIR / f"psalm-{n}.json" for n in EXPECTED_PSALMS]


def load_sources() -> list[dict]:
    missing = [str(p.relative_to(ROOT)) for p in source_paths() if not p.exists()]
    if missing:
        raise SystemExit("Sources V1.5 manquantes: " + ", ".join(missing))
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in source_paths()]
    for n, doc in zip(EXPECTED_PSALMS, docs):
        if doc.get("recordType") != "documentary-extraction" or doc.get("protocolVersion") != "1.5":
            raise SystemExit(f"Source inattendue pour psaume {n}")
        if doc.get("source", {}).get("psalmNumber") != n:
            raise SystemExit(f"Numéro source incohérent pour psaume {n}")
    return docs


def project() -> dict:
    docs = load_sources()
    entries = []
    for doc, path in zip(docs, source_paths()):
        src = doc["source"]
        for subject in doc.get("subjects", []):
            evidence = subject.get("evidence", [])
            local_subject = subject.get("localSubject", "")
            note = subject.get("documentaryNote", "")
            evidence_text = " ".join(e.get("quote", "") for e in evidence)
            entries.append({
                "recordId": src["recordId"],
                "psalmNumber": src["psalmNumber"],
                "localId": subject["localId"],
                "localSubject": local_subject,
                "verseNumbers": subject.get("verseNumbers", []),
                "evidence": evidence,
                "documentaryNote": note,
                "sourcePath": str(path.relative_to(ROOT)).replace("\\", "/"),
                "canonicalPath": src.get("canonicalPath"),
                "search": {
                    "localSubject": normalize(local_subject),
                    "documentaryNote": normalize(note),
                    "evidence": normalize(evidence_text),
                },
            })
    return {
        "schemaVersion": 1,
        "status": "experimental-derived-v1.5",
        "scope": {"bookNumber": 44, "psalmNumbers": EXPECTED_PSALMS},
        "sourcePattern": "data/documentary-extractions/psalms/book-44/psalm-*.json",
        "subjectCount": len(entries),
        "entries": entries,
    }


def serialize(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def check_projection(data: dict) -> None:
    docs = load_sources()
    source_count = sum(len(d.get("subjects", [])) for d in docs)
    entries = data["entries"]
    psalms = sorted({e["psalmNumber"] for e in entries})
    keys = [(e["recordId"], e["localId"]) for e in entries]
    if psalms != EXPECTED_PSALMS:
        raise SystemExit(f"Périmètre projeté incorrect: {psalms}")
    if len(entries) != source_count:
        raise SystemExit(f"Perte/invention de sujets: source={source_count}, projection={len(entries)}")
    if len(keys) != len(set(keys)):
        raise SystemExit("Clés de sujets non uniques")
    if any(not e.get("sourcePath") or not e.get("recordId") or not e.get("localId") for e in entries):
        raise SystemExit("Traçabilité incomplète")


def search_v15(data: dict, query: str) -> list[dict]:
    q = normalize(query)
    if not q:
        return []
    hits = []
    for e in data["entries"]:
        matched = []
        score = 0
        for field, weight in (("localSubject", 5), ("documentaryNote", 2), ("evidence", 1)):
            if q in e["search"][field]:
                matched.append(field)
                score += weight
        if matched:
            hits.append({"score": score, "matchedFields": matched, **{k: e[k] for k in (
                "recordId", "psalmNumber", "localId", "localSubject", "verseNumbers", "evidence", "documentaryNote", "sourcePath"
            )}})
    return sorted(hits, key=lambda x: (-x["score"], x["psalmNumber"], x["localId"]))


def search_thematic(query: str) -> list[dict]:
    data = json.loads(THEMATIC.read_text(encoding="utf-8"))
    q = normalize(query)
    hits = []
    for psalm in data.get("psalmAnalyses", []):
        for theme in psalm.get("themes", []):
            hay = normalize(" ".join([theme.get("themeId", ""), theme.get("label", ""), theme.get("teaching", "")]))
            if q and q in hay:
                hits.append({
                    "recordId": psalm.get("recordId"),
                    "psalmNumber": psalm.get("number"),
                    "themeId": theme.get("themeId"),
                    "label": theme.get("label"),
                    "importance": theme.get("importance"),
                    "directness": theme.get("directness"),
                    "verseNumbers": theme.get("verseNumbers", []),
                    "teaching": theme.get("teaching"),
                })
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("check")
    s = sub.add_parser("search"); s.add_argument("query")
    sub.add_parser("compare")
    args = parser.parse_args()

    data = project()
    check_projection(data)

    if args.cmd == "build":
        EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(serialize(data), encoding="utf-8")
        print(f"{OUTPUT.relative_to(ROOT)}: {data['subjectCount']} sujets, 26 psaumes")
    elif args.cmd == "check":
        expected = serialize(data)
        if OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("subjects.json existe mais n'est pas reproductible depuis les sources actuelles")
        print(f"OK: 26 psaumes, {data['subjectCount']} sujets primaires, traçabilité complète")
    elif args.cmd == "search":
        print(json.dumps(search_v15(data, args.query), ensure_ascii=False, indent=2))
    elif args.cmd == "compare":
        config = json.loads(QUERIES.read_text(encoding="utf-8"))
        report = []
        for item in config["queries"]:
            q = item["query"]
            report.append({"query": q, "reason": item["reason"], "v15": search_v15(data, q), "thematic": search_thematic(q)})
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
