#!/usr/bin/env python3
"""039F: isolated Wiktionary experiment. Outputs ONLY to --out."""
import argparse, collections, json, pathlib, re, time, urllib.parse, urllib.request, unicodedata, hashlib
from build_linguistic_occurrence_index import ROOT, CATALOG, TOKEN_RE, norm, searchable, fields, occurrences
UA="BIBLAW-039F-research/1.0 (GitHub Actions; limited experimental requests)"
API="https://fr.wiktionary.org/w/api.php"
STOP=set("avoir etre faire aller dire pouvoir vouloir savoir voir devoir prendre venir mettre donner aller aussi alors ainsi dans avec pour sans comme cette celui celles ceux leur nous vous ils elles elle lui les des une un que qui quoi dont ou mais donc car par sur sous est sont aux ses ces mon ton son nos vos leurs tout tous toute toutes plus moins tres bien pas ne se ce et en au du de la le a d y il je tu on".split())
def request(params):
    url=API+"?"+urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=20) as resp:
                status=resp.status; data=json.load(resp)
            time.sleep(1.2)
            return status,data,None
        except Exception as e:
            error=str(e);time.sleep(2*(attempt+1))
    return None,None,error
def extract(wikitext):
    # Conservative: numbered wiki definition lines only, without nested examples.
    definitions=[];pos="UNKNOWN"
    for line in wikitext.splitlines():
        if line.startswith("===") and "{{S|" in line:
            m=re.search(r"\{\{S\|([^|}]+)",line)
            if m: pos=m.group(1)
        if re.match(r"^#(?![:*#])",line):
            s=line[1:].strip()
            s=re.sub(r"\{\{[^{}]*\}\}","",s)
            s=re.sub(r"\[\[([^]|]+)\|([^]]+)\]\]",r"\2",s)
            s=re.sub(r"\[\[([^]]+)\]\]",r"\1",s)
            s=re.sub(r"<[^>]*>","",s)
            s=re.sub(r"'{2,}","",s)
            s=re.sub(r"\s+"," ",s).strip()
            if len(s)>=12 and not any(x in s for x in ("{{","}}","[[","]]")):
                definitions.append({"pos_heading":pos,"definition":s})
    return definitions[:25]
def toks(s):
    return set(re.findall(r"[a-zà-ÿ]{3,}",unicodedata.normalize("NFC",s.lower()))) - STOP
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    catalog=json.loads(CATALOG.read_text(encoding="utf8"))
    counts=collections.Counter(); examples={}
    for rel in catalog["records"]:
        if not re.fullmatch(r"data/corpus/books/book-\d+/psalm-\d+\.json",rel):continue
        obj=json.loads((ROOT/rel).read_text(encoding="utf8"))
        if not searchable(rel,obj):continue
        for _,verse,txt in fields(obj):
            for m in TOKEN_RE.finditer(txt):
                raw=m.group();word=norm(raw)
                if len(word)<5 or word in STOP or not word.isalpha() or raw[0].isupper():continue
                counts[word]+=1
                if word not in examples:examples[word]={"record":rel,"verse":verse,"context":txt[:500]}
    ranked=[(w,n) for w,n in counts.most_common() if n>=2]
    # Deterministic frequency strata; sampled forms are lemma CANDIDATES, not verified lemmes.
    bands=[ranked[:max(12,len(ranked)//10)],ranked[len(ranked)//3:len(ranked)//3+max(12,len(ranked)//10)],ranked[-max(12,len(ranked)//10):]]
    selected=[]
    for band in bands:
        for w,n in sorted(band,key=lambda x:hashlib.sha256(x[0].encode()).hexdigest()):
            if w not in {x["candidate"] for x in selected}:
                selected.append({"candidate":w,"frequency":n,"sample":examples[w]})
            if len(selected)%4==0:break
    records=[];proposals=[];errors=[]
    for item in selected:
        w=item["candidate"];status,data,error=request({"action":"query","prop":"revisions","rvprop":"content","rvslots":"main","format":"json","titles":w,"formatversion":2})
        if error:errors.append({"word":w,"error":error});records.append({**item,"definitions":[],"http_status":status});continue
        page=data.get("query",{}).get("pages",[{}])[0]
        content=page.get("revisions",[{}])[0].get("slots",{}).get("main",{}).get("content","")
        # Restrict to French section only; avoid other languages.
        m=re.search(r"^==\s*\{\{langue\|fr\}\}\s*==",content,re.M)
        if m:
            tail=content[m.end():];end=re.search(r"^==[^=]",tail,re.M)
            content=tail[:end.start()] if end else tail
        else:content=""
        defs=extract(content)
        records.append({**item,"definitions":defs,"http_status":status,"source_url":"https://fr.wiktionary.org/wiki/"+urllib.parse.quote(w),"license":"CC BY-SA 4.0; verify attribution and derivative terms before redistribution","status":"EXPERIMENTAL"})
        if len(defs)<2:continue
        # A transparent, uncalibrated overlap baseline. Abstain on ties or zero overlap.
        context=toks(item["sample"]["context"]);scores=[len(context&toks(d["definition"])) for d in defs]
        best=max(scores);winners=[i for i,s in enumerate(scores) if s==best]
        proposals.append({"candidate":w,"context":item["sample"]["context"],"record":item["sample"]["record"],"verse":item["sample"]["verse"],"candidate_scores":scores,"proposed_index":winners[0] if best>0 and len(winners)==1 else None,"decision":"EXPERIMENTAL" if best>0 and len(winners)==1 else "ABSTAIN","score_type":"shared_nonstopword_count_not_probability","status":"EXPERIMENTAL","occurrenceId":None,"occurrenceId_note":"not assigned: source sample may not map to stable occurrence index"})
    report={"source":API,"sample_size":len(selected),"lemmas_with_definitions":sum(bool(r["definitions"]) for r in records),"candidate_definitions":sum(len(r["definitions"]) for r in records),"real_contexts_scored":len(proposals),"proposals":sum(p["decision"]=="EXPERIMENTAL" for p in proposals),"abstentions":sum(p["decision"]=="ABSTAIN" for p in proposals),"quality":"QUALITY_UNVERIFIED","errors":errors,"warning":"Sample contains surface-form lemma candidates, not verified lemmes; no independent sense quality test."}
    for name,obj in [("sample-and-definitions.json",records),("contextual-proposals.json",proposals),("report.json",report)]:
        (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
