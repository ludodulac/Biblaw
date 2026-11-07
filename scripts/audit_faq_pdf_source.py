#!/usr/bin/env python3
"""Compare sensitive FAQ Psalm citations with the archived original PDF, not a second JSON.

The semantic editorial decision still requires reading the relevant Psalm: this script
independently checks the source document matches the cited canonical verse wording.
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

try:
    import fitz
except ImportError:
    raise SystemExit("PyMuPDF is required: python -m pip install pymupdf")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Bible essénienne (classée par livres).pdf"
# The Psalm verse ranges directly relevant to the 23 edited FAQ answers.
# Tuple: book, Psalm number, verse numbers.
TARGETS = [
    (43,267,list(range(26,29))),  # Raphaël: divine intelligence
    (14,103,list(range(6,11))),   # Gabriel: knowing God
    (24,138,list(range(5,10))),    # Ouriel: reincarnation
    (31,184,list(range(10,14))),  # Raphaël: reincarnation
    (28,171,list(range(2,9))),    # Ouriel: divine creative power
    (41,274,list(range(7,10))),    # Michaël: physical and subtle senses
    (18,119,list(range(14,17))),  # Gabriel: intellect and intelligence
    (7,26,list(range(4,11))),     # Raphaël: consciousness as organ
    (20,106,list(range(11,14))),  # Ouriel: consciousness
    (37,254,list(range(7,10))),    # Michaël: consciousness
    (40,256,list(range(14,22))),  # Ouriel: soul
    (21,155,list(range(1,9))),    # Michaël: dimensions of being
    (39,249,list(range(12,19))),  # Raphaël: inner life
    (16,82,list(range(4,7))),     # Ouriel: meditation
    (3,18,list(range(2,5))),      # Raphaël: meditation
    (21,160,list(range(15,17))),  # Michaël: attention
    (25,189,list(range(15,18))),  # Michaël: concentration
    (22,156,list(range(31,34))),  # Gabriel: peace
    (29,208,list(range(11,18))),  # Michaël: calming the body
    (24,152,list(range(2,10))),    # Ouriel: discernment
    (23,134,list(range(18,26))),  # Raphaël: thought
    (26,165,list(range(36,44))),  # Gabriel: feelings
    (30,209,list(range(4,11))),   # Gabriel: love
    (36,214,list(range(12,21))),  # Ouriel: listening
    (6,28,list(range(1,6))),      # Gabriel: gratitude
    (30,197,list(range(3,7))),    # Gabriel: gratitude
    (25,171,list(range(6,9))),    # Michaël: habits
    (37,267,list(range(10,20))),  # Michaël: acts
    (21,145,list(range(10,14))),  # Michaël: work
    (10,67,list(range(5,16))),    # Gabriel: food
    (7,45,list(range(7,10))),      # Raphaël: walking
    (21,140,list(range(4,17))),   # Michaël: speech
    (32,182,list(range(29,36))),  # Ouriel: daily life
]

def normalize(value):
    value = unicodedata.normalize("NFKD", value.lower())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"(\w)-\s+(\w)", r"\1\2", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

def chunks(s, n=7):
    words = normalize(s).split()
    if len(words) < n:
        return [" ".join(words)] if words else []
    pos = sorted(set([0, (len(words)-n)//2, len(words)-n]))
    return [" ".join(words[i:i+n]) for i in pos]

def main():
    if not PDF.exists():
        print("FATAL: PDF original absent du checkout", file=sys.stderr)
        sys.exit(2)
    doc = fitz.open(PDF)
    print(f"PDF_SOURCE_OPEN pages={len(doc)} bytes={PDF.stat().st_size} targets={len(TARGETS)}")
    cache = {}
    def page(i):
        if i < 0 or i >= len(doc):
            return ""
        if i not in cache:
            cache[i] = normalize(doc.load_page(i).get_text("text", sort=True))
        return cache[i]
    observations = []
    for book, number, verse_numbers in TARGETS:
        path = ROOT / f"data/corpus/books/book-{book:02d}/psalm-{number:03d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["recordType"] == "psalm" and int(data["number"]) == number, path
        verses = {int(v["number"]): v for v in data["verses"]}
        for verse in verse_numbers:
            if verse not in verses:
                raise ValueError(f"Missing verse {verse} in {path}")
            source = verses[verse]
            source_pages = source.get("sourcePages") or []
            probes = chunks(source["text"])
            candidates = []
            for source_page in source_pages:
                for offset in range(-2,6):
                    zero_index = int(source_page)+offset
                    txt = page(zero_index)
                    hits = sum(x in txt for x in probes)
                    candidates.append((hits, offset, int(source_page), zero_index, len(txt)))
            match = max(candidates, key=lambda x: (x[0], -abs(x[1]+1))) if candidates else (0,0,0,0,0)
            observations.append({
                "book":book,"psalm":number,"archangel":data["archangel"],"verse":verse,
                "sourcePages":source_pages,"n_chunks":len(probes),"matched_chunks":match[0],
                "offset":match[1],"pdf_page":match[3]+1,"pdf_page_chars":match[4],
                "excerpt":source["text"][:100]
            })
    for r in observations:
        if r["matched_chunks"] == 0:
            p = int(r["sourcePages"][0])
            needle = normalize(r["excerpt"])
            debug = []
            for page_one_based in range(max(1,p-9), min(len(doc),p+10)):
                txt = page(page_one_based-1)
                if txt:
                    debug.append({"page":page_one_based,"chars":len(txt),
                                  "contains_start":needle[:55] in txt,
                                  "start":txt[:125]})
            print("PDF_SOURCE_DIAG "+json.dumps({"psalm":r["psalm"],
                  "verse":r["verse"],"refpage":p,"nearby":debug},ensure_ascii=False))
    statuses = Counter()
    for r in observations:
        status = "PASS" if r["n_chunks"] and r["matched_chunks"] >= 1 else "UNVERIFIED"
        statuses[status] += 1
        if status == "PASS" and r["offset"] != -1:
            statuses["PAGE_METADATA_MISMATCH"] += 1
        print(f"{status} {r['archangel']} {r['psalm']}:{r['verse']} "
              f"pdfpage={r['pdf_page']} jsonpage={r['sourcePages']} "
              f"shingles={r['matched_chunks']}/{r['n_chunks']} offset={r['offset']}")
    output = ROOT/"docs/faq-pdf-source-evidence.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({
        "pdf":PDF.name,"pdf_pages":len(doc),"target_psalms":len(TARGETS),
        "tested_verses":len(observations),"statuses":dict(statuses),
        "note":"Direct text extraction from the PDF file compared with sourcePages of the original structured verses. Not a semantic certification of FAQ paraphrases.",
        "observations":observations
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"PDF_SOURCE_RESULT {dict(statuses)} output={output.relative_to(ROOT)}")
    return 0 if statuses["UNVERIFIED"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
