#!/usr/bin/env python3
"""Build the tiny browser lexical-expansion runtime from frozen BIBLAW evidence.

This script never runs spaCy or Stanza. It consumes the already-finalized 028
classification, the frozen 026 full-vocabulary inventory, and the exact
Morphalou 3.1 ZIP. The raw Morphalou archive is input-only and must never be
committed.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re, unicodedata, zipfile
from collections import defaultdict
from pathlib import Path

MORPHALOU_SHA256 = "4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333"
MORPHALOU_MEMBER = "Morphalou3.1_formatCSV_toutEnUn/Morphalou3.1_CSV.csv"
EXPECTED_028_MACHINE_SAFE = 193248


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def morph_norm(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def browser_key(value: str) -> str:
    value = "".join(
        ch for ch in unicodedata.normalize("NFD", str(value or ""))
        if unicodedata.category(ch) != "Mn"
    ).lower()
    value = value.replace("œ", "oe").replace("æ", "ae").replace("’", " ").replace("'", " ")
    value = re.sub(r"[^a-z0-9\s-]", " ", value).replace("-", " ")
    return re.sub(r"\s+", " ", value).strip()


def participial_pairs(scale028: dict, morphalou: Path) -> set[tuple[str, str]]:
    wanted = {
        (row["normalizedForm"], row["predictedLemma"])
        for row in scale028["rows"]
        if row["status028"] == "MACHINE_SAFE"
        and row["predictedBiblawLexicalPOS"] == "VERB"
    }
    found: set[tuple[str, str]] = set()
    with zipfile.ZipFile(morphalou) as zf:
        with zf.open(MORPHALOU_MEMBER) as raw, io.TextIOWrapper(raw, encoding="utf-8-sig", newline="") as f:
            started = False
            lemma = ""
            category = ""
            for line in f:
                if not started:
                    if line.startswith("GRAPHIE;ID;CATÉGORIE;"):
                        started = True
                    continue
                row = next(csv.reader([line], delimiter=";"))
                if len(row) < 18:
                    continue
                if row[0]:
                    lemma, category = row[0], row[2]
                elif row[2]:
                    category = row[2]
                flexion, mode = row[9], row[12]
                if not flexion or category != "Verbe":
                    continue
                pair = (morph_norm(flexion), lemma)
                if pair in wanted and mode.casefold() == "participle":
                    found.add(pair)
    return found


def build(scale028: dict, vocab026: dict, morphalou: Path) -> dict:
    if sha256_file(morphalou) != MORPHALOU_SHA256:
        raise RuntimeError("Morphalou SHA-256 mismatch: refusing source")
    if scale028.get("statusCounts", {}).get("MACHINE_SAFE") != EXPECTED_028_MACHINE_SAFE:
        raise RuntimeError("unexpected 028 MACHINE_SAFE total")
    if vocab026.get("source019", {}).get("totalCorpusTokens") != 1565921:
        raise RuntimeError("unexpected 026 corpus inventory")

    corpus_frequency_by_key: dict[str, int] = defaultdict(int)
    for row in vocab026["forms"]:
        key = browser_key(row["normalizedForm"])
        if key and " " not in key:
            corpus_frequency_by_key[key] += int(row["corpusFrequency"])

    rows_by_key: dict[str, list[dict]] = defaultdict(list)
    for row in scale028["rows"]:
        key = browser_key(row["normalizedForm"])
        if key and " " not in key:
            rows_by_key[key].append(row)

    participles = participial_pairs(scale028, morphalou)
    eligible: dict[str, tuple[str, str]] = {}
    for key, rows in rows_by_key.items():
        # Product exact matching operates on browser_key(), not raw Morphalou NFC.
        # Require complete corpus coverage at that exact browser key, so an added
        # form can never pull in a REVIEW/UNKNOWN or non-028 occurrence.
        if len(rows) != corpus_frequency_by_key.get(key, 0):
            continue
        if any(row["status028"] != "MACHINE_SAFE" for row in rows):
            continue
        groups = {(row["predictedLemma"], row["predictedBiblawLexicalPOS"]) for row in rows}
        if len(groups) != 1:
            continue
        lemma, lexical_pos = next(iter(groups))
        if lexical_pos == "VERB":
            raw_forms = {row["normalizedForm"] for row in rows}
            if any((form, lemma) in participles for form in raw_forms):
                continue
        eligible[key] = (lemma, lexical_pos)

    by_group: dict[tuple[str, str], list[str]] = defaultdict(list)
    for key, group in eligible.items():
        by_group[group].append(key)

    groups: list[list[str]] = []
    anchors: dict[str, int] = {}
    for group in sorted(by_group, key=lambda item: (item[0].casefold(), item[1])):
        keys = sorted(set(by_group[group]))
        if len(keys) < 2:
            continue
        group_index = len(groups)
        groups.append(keys)
        for key in keys:
            anchors[key] = group_index

    return {
        "v": 1,
        "s": scale028["aggregationSha256"],
        "m": MORPHALOU_SHA256,
        "i": vocab026["source019"]["sha256"],
        "n": EXPECTED_028_MACHINE_SAFE,
        "pf": len(participles),
        "g": groups,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale028", required=True)
    parser.add_argument("--vocabulary026", required=True)
    parser.add_argument("--morphalou", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    scale028 = json.loads(Path(args.scale028).read_text(encoding="utf-8"))
    vocab026 = json.loads(Path(args.vocabulary026).read_text(encoding="utf-8"))
    runtime = build(scale028, vocab026, Path(args.morphalou))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(runtime, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    anchors = sum(len(group) for group in runtime["g"])
    print(f"LEXICAL_EXPANSION_RUNTIME = PASS · {anchors} anchors · {len(runtime['g'])} groups · {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()