#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

POS_MAP = {
    "Nom commun": "NOUN",
    "Adjectif qualificatif": "ADJ",
    "Adverbe": "ADV",
    "Verbe": "VERB",
}
EXT_POS_MAP = {"VERB":"VERB","NOUN":"NOUN","ADJ":"ADJ","ADV":"ADV","AUX":"VERB"}

EXPECTED = {
    "total_forms": 22784,
    "total_tokens": 1565921,
    "missing_forms": 4782,
    "unresolved_only_forms": 68,
    "has_unresolved_competitor_forms": 185,
    "multiple_resolved_forms": 6555,
    "unique_resolved_forms": 11194,
    "eligible_forms": 10444,
    "eligible_tokens": 216012,
    "general_machine_safe_025": 972,
}

def norm(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold()

def dash(ch: str) -> bool:
    return bool(ch) and unicodedata.category(ch) == "Pd"

def oid_hash(oid: str) -> str:
    return hashlib.sha256(oid.encode("utf-8")).hexdigest()

def load_occ_module(root: Path):
    p = root / "scripts" / "build_linguistic_occurrence_index.py"
    spec = importlib.util.spec_from_file_location("occ028", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def iter_tokens(root: Path, occ):
    catalog = json.loads((root / "data" / "catalog.json").read_text(encoding="utf-8"))
    for rel in catalog["records"]:
        p = root / rel
        if not p.exists():
            raise RuntimeError(f"missing catalog record: {rel}")
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not occ.searchable(rel, obj):
            continue
        bn, pn = occ.meta(obj)
        for field, vn, text in occ.fields(obj):
            for m in occ.TOKEN_RE.finditer(text):
                surface = m.group()
                n = occ.norm(surface)
                st, en = m.span()
                occurrence_id = occ.oid(obj["id"], field, vn, st, en)
                yield {
                    "occurrenceId": occurrence_id,
                    "recordId": obj["id"],
                    "recordType": obj.get("recordType"),
                    "bookNumber": bn,
                    "psalmNumber": pn,
                    "verseNumber": vn,
                    "field": field,
                    "surface": surface,
                    "normalizedForm": n,
                    "startOffset": st,
                    "endOffset": en,
                    "apostrophe": ("'" in surface or "’" in surface),
                    "hyphenAdjacency": dash(text[st-1] if st else "") or dash(text[en] if en < len(text) else ""),
                    "text": text,
                }

def parse_morphalou(zip_path: Path, wanted_forms: set[str]):
    raw_count = Counter()
    candidates: dict[str, set[tuple[str,str]]] = defaultdict(set)
    unresolved: dict[str, set[str]] = defaultdict(set)

    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if n.endswith("Morphalou3.1_CSV.csv")]
        if len(names) != 1:
            raise RuntimeError(f"expected exactly one Morphalou CSV, got {names}")
        with zf.open(names[0]) as raw, io.TextIOWrapper(raw, encoding="utf-8-sig", newline="") as f:
            started = False
            current_lemma = ""
            current_category = ""
            for line in f:
                if not started:
                    if line.startswith("GRAPHIE;ID;CATÉGORIE;"):
                        started = True
                    continue
                row = next(csv.reader([line], delimiter=";"))
                if len(row) < 10:
                    continue
                if row[0]:
                    current_lemma = row[0]
                if row[2]:
                    current_category = row[2]
                lemma = row[0] or current_lemma
                category = row[2] or current_category
                flexion = row[9]
                if not lemma or not flexion:
                    continue
                key = norm(flexion)
                if key not in wanted_forms:
                    continue
                raw_count[key] += 1
                mapped = POS_MAP.get(category)
                if mapped is None:
                    unresolved[key].add(category)
                else:
                    candidates[key].add((lemma, mapped))
    return raw_count, candidates, unresolved

def morphology_status(form: str, raw_count, candidates, unresolved):
    raw = raw_count.get(form, 0)
    cands = candidates.get(form, set())
    unr = unresolved.get(form, set())
    if raw == 0:
        return "MISSING"
    if not cands:
        return "UNRESOLVED_ONLY"
    if unr:
        return "HAS_UNRESOLVED_COMPETITOR"
    if len(cands) >= 2:
        return "MULTIPLE_RESOLVED"
    if len(cands) == 1:
        return "UNIQUE_RESOLVED"
    raise AssertionError(form)

def reconstruct_general_safe_025(bench020, raw_count, candidates, unresolved):
    safe = []
    for row in bench020["occurrences"]:
        if row.get("sampleSource") != "GENERAL_10000":
            continue
        if row.get("apostrophe") or row.get("hyphenAdjacency"):
            continue
        a = row["spacy"]; b = row["stanza"]
        if a.get("alignmentStatus") != "ALIGNED" or b.get("alignmentStatus") != "ALIGNED":
            continue
        la = a.get("externalLemma") or ""
        lb = b.get("externalLemma") or ""
        if la.casefold() != lb.casefold():
            continue
        pa = EXT_POS_MAP.get(a.get("externalPOS"))
        pb = EXT_POS_MAP.get(b.get("externalPOS"))
        if pa is None or pb is None or pa != pb:
            continue
        form = row["normalizedFormBiblaw"]
        if morphology_status(form, raw_count, candidates, unresolved) != "UNIQUE_RESOLVED":
            continue
        morph_lemma, morph_pos = next(iter(candidates[form]))
        if la.casefold() != morph_lemma.casefold() or pa != morph_pos:
            continue
        safe.append({
            "occurrenceId": row["occurrenceId"],
            "predictedLemma": la,
            "predictedBiblawLexicalPOS": pa,
            "normalizedForm": form,
        })
    return safe

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--morphalou", required=True)
    ap.add_argument("--benchmark020", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    outdir = Path(args.outdir)
    shards_dir = outdir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    occ = load_occ_module(root)

    freq = Counter()
    apostrophe_present = defaultdict(bool)
    hyphen_observed = defaultdict(bool)
    surface_variants = defaultdict(set)
    total_tokens = 0
    for x in iter_tokens(root, occ):
        total_tokens += 1
        f = x["normalizedForm"]
        freq[f] += 1
        apostrophe_present[f] = apostrophe_present[f] or x["apostrophe"]
        hyphen_observed[f] = hyphen_observed[f] or x["hyphenAdjacency"]
        surface_variants[f].add(x["surface"])

    forms = set(freq)
    assert len(forms) == EXPECTED["total_forms"], (len(forms), EXPECTED["total_forms"])
    assert total_tokens == EXPECTED["total_tokens"], (total_tokens, EXPECTED["total_tokens"])

    raw_count, candidates, unresolved = parse_morphalou(Path(args.morphalou), forms)

    status_counts = Counter()
    status_token_counts = Counter()
    statuses = {}
    for f in forms:
        s = morphology_status(f, raw_count, candidates, unresolved)
        statuses[f] = s
        status_counts[s] += 1
        status_token_counts[s] += freq[f]

    expected_status_counts = {
        "MISSING": EXPECTED["missing_forms"],
        "UNRESOLVED_ONLY": EXPECTED["unresolved_only_forms"],
        "HAS_UNRESOLVED_COMPETITOR": EXPECTED["has_unresolved_competitor_forms"],
        "MULTIPLE_RESOLVED": EXPECTED["multiple_resolved_forms"],
        "UNIQUE_RESOLVED": EXPECTED["unique_resolved_forms"],
    }
    assert dict(status_counts) == expected_status_counts, (dict(status_counts), expected_status_counts)

    eligible = {
        f for f in forms
        if statuses[f] == "UNIQUE_RESOLVED"
        and not apostrophe_present[f]
        and not hyphen_observed[f]
    }
    eligible_tokens = sum(freq[f] for f in eligible)
    assert len(eligible) == EXPECTED["eligible_forms"], (len(eligible), EXPECTED["eligible_forms"])
    assert eligible_tokens == EXPECTED["eligible_tokens"], (eligible_tokens, EXPECTED["eligible_tokens"])

    benchmark020 = json.loads(Path(args.benchmark020).read_text(encoding="utf-8"))
    safe025 = reconstruct_general_safe_025(benchmark020, raw_count, candidates, unresolved)
    assert len(safe025) == EXPECTED["general_machine_safe_025"], len(safe025)
    frozen200 = sorted(safe025, key=lambda r: oid_hash(r["occurrenceId"]))[:200]
    assert frozen200[0]["occurrenceId"] == "occ-e947ea3d9cdb4537f31daaba"
    assert frozen200[-1]["occurrenceId"] == "occ-969d2cc89a63f21f5714ac93"
    (outdir / "replay-027.json").write_text(
        json.dumps({"count":200, "items":frozen200}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    shard_rows = [[] for _ in range(16)]
    target_count = 0
    for x in iter_tokens(root, occ):
        f = x["normalizedForm"]
        if f not in eligible:
            continue
        assert not x["apostrophe"]
        assert not x["hyphenAdjacency"]
        cands = candidates[f]
        assert len(cands) == 1
        morph_lemma, morph_pos = next(iter(cands))
        st, en, text = x["startOffset"], x["endOffset"], x["text"]
        left = max(0, st - 300)
        right = min(len(text), en + 300)
        row = {
            "occurrenceId": x["occurrenceId"],
            "recordId": x["recordId"],
            "recordType": x["recordType"],
            "bookNumber": x["bookNumber"],
            "psalmNumber": x["psalmNumber"],
            "verseNumber": x["verseNumber"],
            "field": x["field"],
            "surface": x["surface"],
            "normalizedForm": f,
            "startOffset": st,
            "endOffset": en,
            "modelText": text[left:right],
            "modelStart": st - left,
            "modelEnd": en - left,
            "apostrophe": x["apostrophe"],
            "hyphenAdjacency": x["hyphenAdjacency"],
            "uniqueMorphologyLemma": morph_lemma,
            "uniqueMorphologyBiblawPOS": morph_pos,
        }
        shard = int(hashlib.sha256(x["occurrenceId"].encode("utf-8")).hexdigest(), 16) % 16
        shard_rows[shard].append(row)
        target_count += 1

    assert target_count == EXPECTED["eligible_tokens"], target_count
    assert sum(len(s) for s in shard_rows) == EXPECTED["eligible_tokens"]
    assert len({r["occurrenceId"] for s in shard_rows for r in s}) == EXPECTED["eligible_tokens"]

    for i, rows in enumerate(shard_rows):
        rows.sort(key=lambda r: r["occurrenceId"])
        p = shards_dir / f"shard-{i:02d}.json"
        p.write_text(json.dumps({"shard":i,"count":len(rows),"rows":rows}, ensure_ascii=False, separators=(",",":"), sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "mission": "BIBLAW-LEXICAL-INDUSTRIALIZATION-028-GHA",
        "sourceBaseline": "5c755358f5cda20db52a2d748cbb2664a1831dcc",
        "morphalouSha256": "4fc815cbf17aecdf1b47f6bbc263489a460fd8d11ae17e6b522336c72bd0e333",
        "totalForms": len(forms),
        "totalCorpusTokens": total_tokens,
        "statusFormCounts": dict(sorted(status_counts.items())),
        "statusTokenCounts": dict(sorted(status_token_counts.items())),
        "uniqueResolvedNoBoundaryRiskForms": len(eligible),
        "futureContextAnalysisEligibleForms": len(eligible),
        "futureContextAnalysisEligibleTokenOccurrences": eligible_tokens,
        "generalMachineSafe025Reconstructed": len(safe025),
        "frozenReplay027Count": len(frozen200),
        "shardCounts": [len(x) for x in shard_rows],
    }
    (outdir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
