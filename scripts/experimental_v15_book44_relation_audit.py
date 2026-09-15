#!/usr/bin/env python3
"""Audit expérimental DIRECT/FONCTIONNEL des 65 rattachements C du livre 44."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import experimental_v15_book44 as base

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "experiments/v1_5-book-44/relation-nature-audit.json"
EXPECTED_FAMILIES = {"argent", "œuvre", "vie intérieure", "vertus", "responsabilité", "terre"}
RECOGNIZED = {"DIRECT", "FONCTIONNEL", "RESIDUEL"}
EXPECTED_ASSIGNMENTS = 65


def load() -> tuple[dict, dict, dict]:
    data = base.project()
    base.check_projection(data)
    config = base.load_consolidation(data)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    return data, config, audit


def attachment_rows(config: dict) -> list[tuple[str, str, str, str]]:
    rows = []
    for family in config["families"]:
        for function in family["functions"]:
            for member in function["members"]:
                rows.append((family["entry"], function["label"], member["recordId"], member["localId"]))
    return rows


def validate(data: dict, config: dict, audit: dict) -> dict:
    primary = {(e["recordId"], e["localId"]) for e in data["entries"]}
    rows = attachment_rows(config)
    current = {(family, record_id, local_id) for family, _, record_id, local_id in rows}
    assignments = audit.get("assignments", [])
    audited = {(a.get("family"), a.get("recordId"), a.get("localId")) for a in assignments}

    if {f["entry"] for f in config["families"]} != EXPECTED_FAMILIES:
        raise SystemExit("Le prototype C ne contient plus exactement les six familles attendues")
    if len(rows) != EXPECTED_ASSIGNMENTS or len(current) != EXPECTED_ASSIGNMENTS:
        raise SystemExit(f"Le prototype C ne contient plus exactement {EXPECTED_ASSIGNMENTS} rattachements uniques")
    if len(assignments) != EXPECTED_ASSIGNMENTS or len(audited) != EXPECTED_ASSIGNMENTS:
        raise SystemExit(f"L'audit doit qualifier exactement {EXPECTED_ASSIGNMENTS} rattachements uniques")
    if audited != current:
        missing = sorted(current - audited)
        extra = sorted(audited - current)
        raise SystemExit(f"Audit désynchronisé du prototype C; manquants={missing}, extras={extra}")
    if any((r, l) not in primary for _, _, r, l in rows):
        raise SystemExit("Référence primaire inexistante dans le prototype C")
    bad = [a for a in assignments if a.get("relationNature") not in RECOGNIZED]
    if bad:
        raise SystemExit(f"Qualification inconnue: {bad}")
    if {a["family"] for a in assignments} != EXPECTED_FAMILIES:
        raise SystemExit("L'audit ne couvre pas exactement les six familles")

    by_nature = Counter(a["relationNature"] for a in assignments)
    by_family = {}
    for family in sorted(EXPECTED_FAMILIES):
        c = Counter(a["relationNature"] for a in assignments if a["family"] == family)
        by_family[family] = {"total": sum(c.values()), **{k: c.get(k, 0) for k in ("DIRECT", "FONCTIONNEL", "RESIDUEL")}}

    subject_families = defaultdict(list)
    for a in assignments:
        subject_families[(a["recordId"], a["localId"])].append((a["family"], a["relationNature"]))
    multiple = {
        f"{record_id}/{local_id}": sorted(items)
        for (record_id, local_id), items in subject_families.items()
        if len(items) > 1
    }
    return {
        "assignmentCount": len(assignments),
        "relationNatureCounts": {k: by_nature.get(k, 0) for k in ("DIRECT", "FONCTIONNEL", "RESIDUEL")},
        "byFamily": by_family,
        "multipleAttachments": multiple,
    }


def relation_index(audit: dict) -> dict:
    return {(a["family"], a["recordId"], a["localId"]): a["relationNature"] for a in audit["assignments"]}


def consolidated_by_nature(data: dict, config: dict, audit: dict, query: str) -> list[dict]:
    q = base.normalize(query)
    by_key = {(e["recordId"], e["localId"]): e for e in data["entries"]}
    relations = relation_index(audit)
    result = []
    for family in config["families"]:
        if base.normalize(family["entry"]) != q:
            continue
        buckets = []
        for nature in ("DIRECT", "FONCTIONNEL", "RESIDUEL"):
            functions = []
            for function in family["functions"]:
                members = []
                for ref in function["members"]:
                    key = (family["entry"], ref["recordId"], ref["localId"])
                    if relations[key] != nature:
                        continue
                    e = by_key[(ref["recordId"], ref["localId"])]
                    members.append({k: e[k] for k in ("recordId", "psalmNumber", "localId", "localSubject", "verseNumbers", "evidence", "documentaryNote", "sourcePath")})
                if members:
                    functions.append({"label": function["label"], "rationale": function["rationale"], "members": members})
            if functions:
                buckets.append({"relationNature": nature, "functions": functions})
        result.append({"entry": family["entry"], "experimental": True, "relations": buckets})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("stats")
    show = sub.add_parser("show")
    show.add_argument("query")
    sub.add_parser("compare")
    args = parser.parse_args()

    data, config, audit = load()
    stats = validate(data, config, audit)

    if args.cmd in {"check", "stats"}:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif args.cmd == "show":
        print(json.dumps(consolidated_by_nature(data, config, audit, args.query), ensure_ascii=False, indent=2))
    elif args.cmd == "compare":
        queries = json.loads(base.QUERIES.read_text(encoding="utf-8"))
        report = []
        for item in queries["queries"]:
            q = item["query"]
            report.append({"query": q, "reason": item["reason"], "A_thematic": base.search_thematic(q), "B_v15_lexical": base.search_v15(data, q), "C_v15_consolidated_by_relation": consolidated_by_nature(data, config, audit, q)})
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
