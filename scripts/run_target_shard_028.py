#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path

EXT_POS_MAP = {"VERB":"VERB","NOUN":"NOUN","ADJ":"ADJ","ADV":"ADV","AUX":"VERB"}

def spacy_run(rows):
    import spacy
    import fr_core_news_sm
    nlp = fr_core_news_sm.load(disable=["ner"])
    texts = [x["modelText"] for x in rows]
    results = {}
    for x, doc in zip(rows, nlp.pipe(texts, batch_size=64)):
        matches = [t for t in doc if t.idx == x["modelStart"] and t.idx + len(t.text) == x["modelEnd"]]
        if len(matches) != 1:
            results[x["occurrenceId"]] = {
                "alignmentStatus":"ALIGNMENT_FAILURE",
                "externalLemma":None,
                "externalPOS":None,
                "projectedPOS":None,
                "alignmentEvidence":{"matchCount":len(matches)},
            }
        else:
            t = matches[0]
            results[x["occurrenceId"]] = {
                "alignmentStatus":"ALIGNED",
                "externalLemma":t.lemma_ or None,
                "externalPOS":t.pos_ or None,
                "projectedPOS":EXT_POS_MAP.get(t.pos_),
                "alignmentEvidence":{
                    "matchCount":1,
                    "tokenText":t.text,
                    "start":t.idx,
                    "end":t.idx + len(t.text),
                },
            }
    return results, spacy.__version__, fr_core_news_sm.__version__

def stanza_run(rows):
    import stanza
    model_dir = os.environ["STANZA_RESOURCES_DIR"]
    nlp = stanza.Pipeline(
        "fr",
        dir=model_dir,
        processors="tokenize,mwt,pos,lemma",
        package="default",
        download_method=None,
        use_gpu=False,
        verbose=False,
    )
    results = {}
    batch = 128
    for start in range(0, len(rows), batch):
        chunk = rows[start:start+batch]
        docs = nlp([stanza.Document([], text=x["modelText"]) for x in chunk])
        for x, doc in zip(chunk, docs):
            matches = []
            for sent in doc.sentences:
                for tok in sent.tokens:
                    if tok.start_char == x["modelStart"] and tok.end_char == x["modelEnd"] and len(tok.words) == 1:
                        matches.append((tok, tok.words[0]))
            if len(matches) != 1:
                results[x["occurrenceId"]] = {
                    "alignmentStatus":"ALIGNMENT_FAILURE",
                    "externalLemma":None,
                    "externalPOS":None,
                    "projectedPOS":None,
                    "alignmentEvidence":{"matchCount":len(matches)},
                }
            else:
                tok, w = matches[0]
                results[x["occurrenceId"]] = {
                    "alignmentStatus":"ALIGNED",
                    "externalLemma":w.lemma or None,
                    "externalPOS":w.upos or None,
                    "projectedPOS":EXT_POS_MAP.get(w.upos),
                    "alignmentEvidence":{
                        "matchCount":1,
                        "tokenText":tok.text,
                        "start":tok.start_char,
                        "end":tok.end_char,
                    },
                }
        print(f"STANZA_PROGRESS = {min(start+batch,len(rows))}/{len(rows)}", flush=True)
    return results, stanza.__version__

def classify(row, spa, sta):
    reasons = []
    if row.get("apostrophe") or row.get("hyphenAdjacency"):
        reasons.append("BOUNDARY_INVARIANT_FAILURE")

    sa = spa["alignmentStatus"] == "ALIGNED"
    ta = sta["alignmentStatus"] == "ALIGNED"
    if not sa:
        reasons.append("SPACY_ALIGNMENT_FAILURE")
    if not ta:
        reasons.append("STANZA_ALIGNMENT_FAILURE")

    if not sa and not ta:
        return "UNKNOWN", sorted(set(reasons))

    if sa != ta:
        return "REVIEW_QUEUE", sorted(set(reasons))

    # Both aligned.
    sl = spa.get("externalLemma") or ""
    tl = sta.get("externalLemma") or ""
    lemma_agree = sl.casefold() == tl.casefold()
    if not lemma_agree:
        reasons.append("LEMMA_DISAGREEMENT")

    sp = spa.get("projectedPOS")
    tp = sta.get("projectedPOS")
    if sp is None:
        reasons.append("SPACY_POS_UNPROJECTABLE")
    if tp is None:
        reasons.append("STANZA_POS_UNPROJECTABLE")

    if sp is not None and tp is not None and sp != tp:
        reasons.append("POS_DISAGREEMENT_AFTER_PROJECTION")

    if reasons and (
        "LEMMA_DISAGREEMENT" in reasons
        or "POS_DISAGREEMENT_AFTER_PROJECTION" in reasons
        or "BOUNDARY_INVARIANT_FAILURE" in reasons
    ):
        return "REVIEW_QUEUE", sorted(set(reasons))

    if sp is None or tp is None:
        return "UNKNOWN", sorted(set(reasons))

    # Both engines agree in the BIBLAW lexical namespace.
    if not lemma_agree:
        return "REVIEW_QUEUE", sorted(set(reasons))

    morph_lemma = row["uniqueMorphologyLemma"]
    morph_pos = row["uniqueMorphologyBiblawPOS"]
    # 025 only casefolds the contextual spaCy/Stanza agreement. The final
    # confirmation against Morphalou keeps exact lemma identity.
    if sl != morph_lemma or sp != morph_pos:
        reasons.append("MORPHOLOGY_CONTEXT_MISMATCH")
        return "REVIEW_QUEUE", sorted(set(reasons))

    if reasons:
        reasons.append("OTHER")
        return "REVIEW_QUEUE", sorted(set(reasons))

    return "MACHINE_SAFE", ["TRIPLE_EVIDENCE_PASS"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = payload["rows"]

    spa, spacy_version, spacy_model_version = spacy_run(rows)
    sta, stanza_version = stanza_run(rows)

    assert spacy_version == "3.8.16", spacy_version
    assert spacy_model_version == "3.8.0", spacy_model_version
    assert stanza_version == "1.14.0", stanza_version

    out = []
    status_counts = Counter()
    reason_counts = Counter()
    for row in rows:
        a = spa[row["occurrenceId"]]
        b = sta[row["occurrenceId"]]
        status, reasons = classify(row, a, b)
        status_counts[status] += 1
        if status != "MACHINE_SAFE":
            reason_counts.update(reasons)
        item = {
            "occurrenceId":row["occurrenceId"],
            "surface":row["surface"],
            "normalizedForm":row["normalizedForm"],
            "spacy":a,
            "stanza":b,
            "uniqueMorphologyLemma":row["uniqueMorphologyLemma"],
            "uniqueMorphologyBiblawPOS":row["uniqueMorphologyBiblawPOS"],
            "status028":status,
            "reasonCodes":reasons,
        }
        if status == "MACHINE_SAFE":
            item["predictedLemma"] = a["externalLemma"]
            item["predictedBiblawLexicalPOS"] = a["projectedPOS"]
        else:
            item["predictedLemma"] = None
            item["predictedBiblawLexicalPOS"] = None
        out.append(item)

    result = {
        "mission":"BIBLAW-LEXICAL-INDUSTRIALIZATION-028-GHA",
        "shard":payload["shard"],
        "inputCount":len(rows),
        "engineVersions":{
            "spacy":spacy_version,
            "fr_core_news_sm":spacy_model_version,
            "stanza":stanza_version,
            "stanzaResourcesVersion":"1.14.0",
            "processors":"tokenize,mwt,pos,lemma",
        },
        "statusCounts":dict(sorted(status_counts.items())),
        "nonSafeReasonCounts":dict(sorted(reason_counts.items())),
        "rows":sorted(out, key=lambda r:r["occurrenceId"]),
    }
    Path(args.output).write_text(
        json.dumps(result, ensure_ascii=False, separators=(",",":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "shard":payload["shard"],
        "inputCount":len(rows),
        "statusCounts":dict(status_counts),
        "nonSafeReasonCounts":dict(reason_counts),
    }, sort_keys=True))

if __name__ == "__main__":
    main()
