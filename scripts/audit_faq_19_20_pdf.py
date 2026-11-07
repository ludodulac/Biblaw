#!/usr/bin/env python3
"""Read the archived ORIGINAL Bible PDF and audit the 3 staged FAQ 19/20 answers.

Non-destructive: emits docs/FAQ-MISSION-19-20-PDF-EVIDENCE.json only in the runner.
The textual match is SOURCE integrity, NOT proof of doctrinal paraphrase fidelity.
"""
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit("pymupdf required") from exc

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
# A, B, C are the 3 draft answers in docs/FAQ-MISSION-19-20-PROJETS-2026-11-07.md.
TARGETS = [
    ("A", 37, 254, "michael", list(range(1, 16)) + list(range(21, 29))),
    ("A", 19, 106, "raphael", list(range(15, 18))),
    ("A", 44, 277, "ouriel", list(range(5, 11))),
    ("B", 7, 26, "raphael", list(range(4, 12))),
    ("B", 20, 106, "ouriel", list(range(5, 22))),
    ("B", 21, 160, "michael", list(range(2, 9)) + list(range(15, 17))),
    ("B", 4, 14, "ouriel", list(range(4, 13)) + [16]),
    ("C", 27, 177, "raphael", list(range(3, 7)) + list(range(14, 18))),
    ("C", 37, 267, "michael", list(range(3, 15)) + list(range(16, 20)) + list(range(32, 40))),
    ("C", 4, 14, "ouriel", list(range(4, 17))),
]


def norm(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def probes(text, width=7):
    words = norm(text).split()
    if not words:
        return []
    if len(words) <= width:
        return [" ".join(words)]
    return [" ".join(words[i:i+width]) for i in sorted(set((0, max(0, (len(words)-width)//2), len(words)-width)))]


def execute():
    assert PDF.is_file(), "Original PDF missing in checkout"
    doc = fitz.open(PDF)
    hash_ = hashlib.sha256(PDF.read_bytes()).hexdigest()
    cache = {}
    def page(idx):
        if idx not in cache:
            cache[idx] = norm(doc.load_page(idx).get_text("text", sort=True))
        return cache[idx]
    results = []
    consolidated = defaultdict(set)
    for group, book, num, arch, verses_requested in TARGETS:
        filename = f"data/corpus/books/book-{book:02d}/psalm-{num:03d}.json"
        canonical = json.loads((ROOT / filename).read_text(encoding="utf-8"))
        assert canonical["recordType"] == "psalm"
        assert canonical["archangel"] == arch, filename
        assert canonical["number"] == num, filename
        all_verses = {int(v["number"]):v for v in canonical["verses"]}
        for vid in verses_requested:
            assert vid in all_verses, (filename, vid)
            consolidated[(book, num, arch)].add(vid)
            v = all_verses[vid]
            pn = probes(v["text"])
            options = []
            for sp in v.get("sourcePages") or canonical["source"].get("pdfPages") or []:
                for offset in range(-6, 9):
                    idx = int(sp)-1+offset
                    if 0 <= idx < len(doc):
                        # A long verse can straddle two physical pages of the original
                        # document. Score both the single page and an adjacent page pair.
                        # Prefer a single-page proof when both contain all word segments.
                        for span in (1, 2):
                            if idx + span - 1 >= len(doc):
                                continue
                            raw = page(idx) if span == 1 else page(idx) + " " + page(idx+1)
                            score = sum(s in raw for s in pn)
                            options.append((score, -(span-1), -abs(offset), idx, span))
            best = max(options) if options else (0, 0, 0, -1, 1)
            result = {
                "group":group, "book":book, "psalm":num, "archangel":arch,
                "verse":vid, "canonical":filename, "json_pages":v.get("sourcePages",[]),
                "pdf_page":best[3]+1 if best[3]>=0 else None,
                "pdf_pages_used":list(range(best[3]+1,best[3]+best[4]+1)) if best[3]>=0 else [],
                "matched_segments":best[0], "total_segments":len(pn),
                "verified_in_original_pdf":best[0] >= 1,
                "fully_matched":best[0] == len(pn) and len(pn)>0,
            }
            results.append(result)
    # Search all pages of original PDF; not simply code-search of JSON.
    # Search terms are indicators for prioritizing human reading, not proof of absence.
    search_strings = [
        "mort imminente", "experience de mort imminente", "experiences de mort imminente",
        "mort clinique", "arret cardiaque", "retour de la mort",
        "experience aux portes de la mort", "experience apres la mort",
        "science de la mort", "cerveau cesse de fonctionner",
        "cerveau ne fonctionne plus",
    ]
    hits = {s:[] for s in search_strings}
    proximity_hits = []
    for idx in range(len(doc)):
        content = page(idx)
        for term in search_strings:
            start = content.find(term)
            if start >= 0:
                hits[term].append({"pdf_page":idx+1, "context":content[max(0,start-105):start+190]})
        # Potential thematic near hits, not explicit answer: science + death near each other.
        for match in list(re.finditer(r"\bscience\b", content))[:25]:
            neighborhood = content[max(0, match.start()-170):match.end()+170]
            if re.search(r"\bmort\b|\bau dela\b|\bcerveau\b", neighborhood):
                if len(proximity_hits) < 60:
                    proximity_hits.append({"pdf_page":idx+1,"context":neighborhood})
    # Avoid double counts in project B/C when same Ouriel 14 range.
    dedup = {}
    for r in results:
        key=(r["book"],r["psalm"],r["archangel"],r["verse"])
        dedup[key] = r
    unique=list(dedup.values())
    verified=sum(x["verified_in_original_pdf"] for x in unique)
    full=sum(x["fully_matched"] for x in unique)
    pdf_evidence = {
        "origin":"Bible essénienne (classée par livres).pdf", "pdf_pages":len(doc),
        "pdf_bytes":PDF.stat().st_size,"pdf_sha256":hash_,
        "project_psalms":len(consolidated),"project_verse_occurrences":len(results),
        "distinct_target_verses":len(unique),"distinct_verses_verified":verified,
        "distinct_verses_fully_matched":full,"unverified":[x for x in unique if not x["verified_in_original_pdf"]],
        "target_ranges": [
            {"group":g,"archangel":a,"psalm":n,"book":b,"verses":v}
            for g,b,n,a,v in TARGETS
        ],"verse_observations":unique,"explicit_term_hits":hits,"science_and_death_proximity_samples":proximity_hits,
        "limitations":[
            "Textual source comparison does not certify interpretation or editorial paraphrase.",
            "Absence of keyword hit cannot prove absence of a topic in poetic or metaphorical language.",
            "A science/death proximity match does not indicate an explicit teaching about modern science or near-death experiences."
        ]
    }
    output = ROOT / "docs/FAQ-MISSION-19-20-PDF-EVIDENCE.json"
    output.write_text(json.dumps(pdf_evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"PDF_DIRECT pages={len(doc)} bytes={PDF.stat().st_size} sha256={hash_}")
    print(f"PDF_VERIFICATION psalms={len(consolidated)} distinct_verses={len(unique)} verified={verified} full_3of3={full} occurrences={len(results)}")
    for (b,n,a),vs in sorted(consolidated.items()):
        matches=[x for x in unique if x["book"]==b and x["psalm"]==n and x["archangel"]==a]
        print("PSALM",a,n,"book",b,"verses",len(vs),
              "PASS",sum(x["verified_in_original_pdf"] for x in matches),
              "FULL",sum(x["fully_matched"] for x in matches))
    for x in unique:
        if not x["verified_in_original_pdf"]:
            print("UNVERIFIED",x["archangel"],x["psalm"],x["verse"],x["json_pages"])
    print("PDF_TERMS",json.dumps({k:len(v) for k,v in hits.items()},ensure_ascii=False))
    for term, arr in hits.items():
        for hit in arr[:8]:
            print("PDF_TERM_SAMPLE",json.dumps({"term":term,**hit},ensure_ascii=False))
    print("PDF_SCIENCE_DEATH_PROXIMITY",len(proximity_hits))
    for item in proximity_hits[:15]:
        print("PDF_PROXIMITY_SAMPLE",json.dumps(item,ensure_ascii=False))
    # Manual editorial triage of ambiguous 'science' terms in the original PDF.
    # Print context with page numbers so reviewers can distinguish Essene sacred science
    # from an external scientific statement about modern near-death experiences.
    for pg in (1067, 2045, 222, 2697):
        txt = doc.load_page(pg-1).get_text("text",sort=True)
        flat = norm(txt)
        for token in ("science", "mort", "memorial"):
            ix = flat.find(token)
            if ix >= 0:
                print("PDF_EDITORIAL_CONTEXT",json.dumps({
                    "pdf_page":pg,"token":token,"excerpt":flat[max(0,ix-230):ix+680]
                },ensure_ascii=False))
                break
    further_terms = [
        "sortie du corps", "sortie hors du corps", "hors de son corps",
        "revenu de la mort", "revenus de la mort", "revenu d entre les morts",
        "mort apparente", "proche de la mort", "pres de la mort",
        "ressuscite apres", "coma", "recit de mort imminente",
        "resuscitation", "decorporation"
    ]
    for term in further_terms:
        ph = []
        for idx in range(len(doc)):
            t = page(idx)
            loc = t.find(term)
            if loc >= 0:
                ph.append({"pdf_page":idx+1,"excerpt":t[max(0,loc-140):loc+250]})
        print("PDF_NDE_VARIANT",json.dumps({"term":term,"count":len(ph),"examples":ph[:3]},ensure_ascii=False))

    print("PDF_EVIDENCE_FILE",str(output.relative_to(ROOT)))
    doc.close()
    return 0 if verified == len(unique) else 1

if __name__ == "__main__":
    sys.exit(execute())
