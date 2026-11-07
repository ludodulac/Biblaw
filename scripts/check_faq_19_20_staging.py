#!/usr/bin/env python3
"""Verify the original 19/20 drafts and public candidate are exactly identical.
This script does not deploy or modify anything."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def nfc_key(arch, psalm):
    return {"Michaël":"michael","Gabriel":"gabriel","Raphaël":"raphael","Ouriel":"ouriel"}[arch]+":"+str(psalm)
def parse_verse_ids(text):
    # Supports "1 à 9", "4, 5 et 10 à 13", "2 à 8 et 15 à 16".
    nums=set()
    range_pattern=re.compile(r"(\d+)\s+à\s+(\d+)")
    consumed=range_pattern.sub(lambda m:add_range(m,nums),text)
    nums.update(int(z) for z in re.findall(r"\d+",consumed))
    return nums

def add_range(match, numbers):
    a,b=int(match.group(1)),int(match.group(2))
    if not 0<a<=b<=500 or b-a>150:
        raise ValueError("Invalid verse range "+match.group())
    numbers.update(range(a,b+1))
    return " "

def inventory():
    base=load("data/faq-public-085.json")
    groups=list(base["questions"])
    for n in range(1,6):
        groups.append(load(f"data/faq-090-{n}.json"))
    for n in range(1,10):
        groups.append(load(f"data/faq-091-{n}.json"))
    for n in range(92,99):
        groups+=load(f"data/faq-{n:03d}.json")["questions"]
    by_id={q["id"]:q for q in groups}
    assert len(groups)==102 and len(by_id)==102, (len(groups),len(by_id))
    return by_id

def main():
    existing=inventory()
    staged=load("docs/FAQ-MISSION-19-20-STAGING.json")
    routing=load("docs/FAQ-MISSION-19-20-ROUTING.json")
    questions=staged["questions"]
    # The public 105-FAQ preview must contain the *exact* texts and Psalm map
    # verified against the PDF, never a paraphrase mutated during integration.
    candidate=load("data/faq-099.json")
    public_routes=load("data/faq-099-routing.json")
    assert candidate==staged, "Published candidate diverges from PDF-verified staging"
    expected_public_routes={
        "version":routing["version"],"summary":routing["summary"],
        "routes":[
            {key:r[key] for key in ("number","question","resolution","target_id","related_ids")}
            for r in routing["routes"]
        ]
    }
    assert public_routes==expected_public_routes, "Public routing diverges from reviewed plan"
    assert staged["version"]==1 and len(questions)==3
    new_ids={q["id"] for q in questions}
    assert len(new_ids)==3 and not new_ids.intersection(existing)
    citation=re.compile(r"\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)")
    psalm_cache={}
    total_citations=0
    all_cited_verses=set()
    for q in questions:
        body=q["answer"]
        assert q["title"] and q["id"]
        assert body.startswith("La Bible essénienne enseigne que"),q["id"]
        assert body.count("\n\n")>=3,("Not developed",q["id"])
        assert not re.search(r"pas scientifiquement d[eé]montr[eé]|selon la science moderne|en tant qu IA|ChatGPT",body,re.I)
        matches=list(citation.finditer(body))
        assert len(matches)>=4,(q["id"],len(matches))
        assert body.count("(psaume ")==len(matches),("Unparseable citation",q["id"])
        total_citations+=len(matches)
        for m in matches:
            num=int(m.group(1))
            key=nfc_key(m.group(2),num)
            assert key in staged["verifiedPsalms"],("Missing map",key)
            book=staged["verifiedPsalms"][key]
            path=f"data/corpus/books/book-{book:02d}/psalm-{num:03d}.json"
            if path not in psalm_cache:
                psalm_cache[path]=load(path)
            ps=psalm_cache[path]
            assert ps["recordType"]=="psalm" and ps["number"]==num
            assert ps["archangel"]==key.split(":")[0],(q["id"],key)
            cited=parse_verse_ids(m.group(3))
            assert cited
            available={int(v["number"]) for v in ps["verses"]}
            assert cited<=available,("Missing verses",q["id"],key,sorted(cited-available))
            all_cited_verses.update((path,v) for v in cited)
    routes=routing["routes"]
    assert len(routes)==19 and sorted(r["number"] for r in routes)==list(range(1,20))
    classifications=Counter(r["resolution"] for r in routes)
    assert classifications=={"new":3,"redirect_new":2,"reuse":12,"unsupported":2},classifications
    assert classifications==routing["summary"]
    assert {r["target_id"] for r in routes if r["resolution"]=="new"}==new_ids
    assert all(not r.get("target_id") for r in routes if r["resolution"]=="unsupported")
    for r in routes:
        assert r["question"] and r["editorial_decision"]
        t=r["target_id"]
        if r["resolution"]=="reuse":assert t in existing,(r["number"],t)
        if r["resolution"] in ("redirect_new","new"):assert t in new_ids,(r["number"],t)
        for rid in r["related_ids"]:
            assert rid in existing,(r["number"],rid)
    print(f"FAQ_19_20_STAGING_PASS existing={len(existing)} staged={len(questions)} citations={total_citations} cited_distinct_verses={len(all_cited_verses)}")
    print("FAQ_19_20_ROUTING_PASS "+str(dict(classifications)))
    print("FAQ_19_20_PUBLIC_INTEGRATION_VERIFIED: published candidate identical to verified staging; no deploy")

if __name__=="__main__":
    main()
