#!/usr/bin/env python3
import argparse,hashlib,json,math
from collections import Counter
from pathlib import Path
from build_linguistic_occurrence_index import ROOT,TOKEN_RE,norm,occurrences
from build_linguistic_semantic_form_runtime import obtain_morphalou,verify_source,MORPHALOU_MEMBER,POS_MAP
import csv,io,zipfile
G=ROOT/"data/linguistic/gold"; C=ROOT/"data/linguistic/sense-catalog.json"; F=ROOT/"data/linguistic-semantic-form-runtime.json"; O=ROOT/"data/linguistic/audits/sense-classifier-023a.json"
K=5; W=12; MARK="<TARGET>"
def choose_target(keys,lemma=None,pos=None):
 if (lemma is None)!=(pos is None):raise SystemExit("INCOMPLETE_TARGET_SELECTOR")
 if lemma is not None:
  if (lemma,pos) not in keys:raise SystemExit("TARGET_NOT_AVAILABLE")
  return (lemma,pos)
 if not keys:raise SystemExit("NO_ELIGIBLE_SEMANTIC_TARGET")
 if len(keys)!=1:raise SystemExit("AMBIGUOUS_SEMANTIC_TARGET")
 return next(iter(keys))
def gold_for_target(golds,key):
 return [g for g in golds if (g["target"].get("lemma"),g["target"].get("partOfSpeech"))==key]
def sources(lemma=None,pos=None):
 c=json.loads(C.read_text()); allowed={(e["lemma"],e["partOfSpeech"]):sorted(x["senseId"] for x in e["senses"]) for e in c["entries"]}
 f=json.loads(F.read_text()); targets={(x["lemma"],x["partOfSpeech"]):x for x in f["targets"]}
 golds=[json.loads(p.read_text()) for p in sorted(G.glob("*-sense-gold.json"))]
 eligible={key for key in allowed.keys()&targets.keys() if any(e.get("adjudicationStatus")=="VALIDATED" and e.get("senseId") in allowed[key] for g in gold_for_target(golds,key) for e in g.get("entries",[]))}
 key=choose_target(eligible,lemma,pos)
 rows=[];goldids=set();classes=allowed[key]
 for g in gold_for_target(golds,key):
  byid={o["occurrenceId"]:o for o in occurrences(g["target"]["normalizedForm"])}
  for e in g.get("entries",[]):
   oid=e.get("occurrenceId");goldids.add(oid)
   if e.get("adjudicationStatus")=="VALIDATED":
    if e.get("senseId") not in classes:raise SystemExit("INVALID_GOLD_SENSE_ID")
    if oid not in byid:raise SystemExit("GOLD_OCCURRENCE_NOT_FOUND")
    rows.append((key,byid[oid],e["senseId"]))
 return sorted(rows,key=lambda r:r[1]["occurrenceId"]),goldids,{key:targets[key]},classes,key
def feats(context,forms):
 ts=[norm(m.group()) for m in TOKEN_RE.finditer(context)]; fs={norm(x) for x in forms}; ts=[MARK if t in fs else t for t in ts]
 try:i=ts.index(MARK)
 except ValueError:i=len(ts)//2
 q=ts[max(0,i-W):i+W+1]; z=Counter("u:"+x for x in q if x!=MARK); z.update("b:"+a+"_"+b for a,b in zip(q,q[1:]) if MARK not in (a,b)); return z
def train(rows,classes,targets):
 d=Counter(); total=Counter(); counts={c:Counter() for c in classes}; vocab=set()
 for key,o,y in rows:
  d[y]+=1
  for f,n in feats(o["context"],targets[key]["forms"]).items(): counts[y][f]+=n; total[y]+=n; vocab.add(f)
 return d,total,counts,vocab
def pred(model,classes,f):
 d,total,counts,vocab=model; n=sum(d.values()); V=max(1,len(vocab)); raw={}
 for c in classes:
  v=math.log((d[c]+1)/(n+len(classes))); den=total[c]+V
  for x,k in f.items(): v+=k*math.log((counts[c][x]+1)/den)
  raw[c]=v
 mx=max(raw.values()); ex={c:math.exp(v-mx) for c,v in raw.items()}; z=sum(ex.values()); ps={c:ex[c]/z for c in classes}; order=sorted(classes,key=lambda c:(-ps[c],c)); return order[0],ps[order[0]]
def fold(group): return int(hashlib.sha256(group.encode()).hexdigest()[:8],16)%K
def evalm(oof,classes):
 m={a:{b:0 for b in classes} for a in classes}
 for y,p,s in oof:m[y][p]+=1
 per={}; P=[];R=[];Q=[]
 for c in classes:
  tp=m[c][c]; fp=sum(m[y][c] for y in classes if y!=c); fn=sum(m[c][p] for p in classes if p!=c); pr=tp/(tp+fp) if tp+fp else 0; re=tp/(tp+fn) if tp+fn else 0; f=2*pr*re/(pr+re) if pr+re else 0
  per[c]={"support":sum(m[c].values()),"precision":pr,"recall":re,"f1":f};P.append(pr);R.append(re);Q.append(f)
 return {"confusionMatrix":m,"accuracy":sum(y==p for y,p,_ in oof)/len(oof),"macroPrecision":sum(P)/len(P),"macroRecall":sum(R)/len(R),"macroF1":sum(Q)/len(Q),"perSenseId":per}
def policy(oof):
 best=None
 for t in sorted({s for _,_,s in oof},reverse=True):
  a=[x for x in oof if x[2]>=t]; pr=sum(y==p for y,p,_ in a)/len(a)
  if pr>=.95:
   cand=(len(a),-t,pr,t)
   if best is None or cand>best:best=cand
 return {"targetPrecision":.95,"threshold":None,"oofCount":0,"oofPrecision":None} if best is None else {"targetPrecision":.95,"threshold":best[3],"oofCount":best[0],"oofPrecision":best[2]}
def morphological_eligibility(targets):
 source=obtain_morphalou()
 try:
  verify_source(source); wanted_forms={norm(f) for t in targets.values() for f in t["forms"]}; analyses={f:set() for f in wanted_forms}
  with zipfile.ZipFile(source) as archive:
   with archive.open(MORPHALOU_MEMBER) as raw:
    rows=csv.reader(io.TextIOWrapper(raw,encoding="utf-8-sig",newline=""),delimiter=";"); header=None
    for candidate in rows:
     if len(candidate)>=3 and [cell.strip() for cell in candidate[:3]]==["GRAPHIE","ID","CATÉGORIE"]:
      header=[cell.strip() for cell in candidate]; break
    if header is None: raise SystemExit("Morphalou CSV header not found")
    graphie=[i for i,name in enumerate(header) if name=="GRAPHIE"]
    if len(graphie)<2: raise SystemExit("Morphalou inflected GRAPHIE column not found")
    lemma_i,surface_i=graphie[:2]; category_i=header.index("CATÉGORIE"); lemma=category=None
    for row in rows:
     if len(row)<=max(lemma_i,surface_i,category_i): continue
     if row[lemma_i].strip(): lemma=row[lemma_i].strip()
     if row[category_i].strip(): category=row[category_i].strip()
     surface=norm(row[surface_i].strip()) if row[surface_i].strip() else None; pos=POS_MAP.get(category or "")
     if surface in analyses and lemma and pos: analyses[surface].add((lemma,pos))
  result={}
  for key,t in targets.items():
   eligible=[]; ambiguous=[]
   for form in sorted({norm(x) for x in t["forms"]}):
    (eligible if analyses.get(form)=={key} else ambiguous).append(form)
   result[key]={"eligibleForms":eligible,"ambiguousForms":ambiguous}
  return result
 finally: source.unlink(missing_ok=True)

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--lemma",default=None)
 parser.add_argument("--pos",default=None)
 parser.add_argument("--output",type=Path,default=O)
 args=parser.parse_args()
 rows,goldids,targets,classes,selected_key=sources(args.lemma,args.pos); oof=[]
 for k in range(K):
  te=[r for r in rows if fold(r[1]["recordId"])==k]; tr=[r for r in rows if fold(r[1]["recordId"])!=k]
  if not te or set(r[2] for r in tr)!=set(classes):raise SystemExit("invalid grouped fold")
  model=train(tr,classes,targets)
  for key,o,y in te:
   p,s=pred(model,classes,feats(o["context"],targets[key]["forms"]));oof.append((y,p,s))
 ev=evalm(oof,classes); pol=policy(oof); pol["thresholdStatus"]="EXPERIMENTAL_OOF_SELECTED"; full=train(rows,classes,targets); eligibility=morphological_eligibility(targets); props=[]; excluded=0
 for key,t in sorted(targets.items()):
  seen={}
  for form in t["forms"]:
   os=occurrences(form)
   if norm(form) in eligibility[key]["eligibleForms"]:
    for o in os: seen[o["occurrenceId"]]=o
   else:
    excluded+=sum(o["occurrenceId"] not in goldids for o in os)
  for oid,o in sorted(seen.items()):
   if oid in goldids:continue
   p,s=pred(full,classes,feats(o["context"],t["forms"])); dec="AUTO_ACCEPT" if pol["threshold"] is not None and s>=pol["threshold"] else "REVIEW"
   props.append({"occurrenceId":oid,"surfaceForm":o["surfaceForm"],"proposedSenseId":p,"decision":dec,"score":round(s,6)})
 eligible=sorted({f for x in eligibility.values() for f in x["eligibleForms"]}); ambiguous=sorted({f for x in eligibility.values() for f in x["ambiguousForms"]})
 report={"schemaVersion":1,"purpose":"automatic-sense-classifier-evaluation","target":{"lemma":selected_key[0],"partOfSpeech":selected_key[1]},"evaluation":{"method":"5-fold deterministic grouped cross-validation by recordId","validatedCount":len(rows),"classes":classes,**ev},"acceptancePolicy":pol,"morphologicalEligibility":{"eligibleForms":eligible,"ambiguousForms":ambiguous,"excludedOccurrenceCount":excluded},"unseenProposals":props}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"validatedCount":len(rows),"classes":classes,"accuracy":ev["accuracy"],"macroPrecision":ev["macroPrecision"],"macroRecall":ev["macroRecall"],"macroF1":ev["macroF1"],"policy":pol,"unseenCount":len(props),"autoAccept":sum(x["decision"]=="AUTO_ACCEPT" for x in props),"review":sum(x["decision"]=="REVIEW" for x in props),"surfaceForms":sorted({x["surfaceForm"] for x in props}),"morphologicalEligibility":report["morphologicalEligibility"]},ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
