#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, os, unicodedata, heapq
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASELINE='5c755358f5cda20db52a2d748cbb2664a1831dcc'
SOURCE_HEAD='2713bc892b9ce0830c08aa3211d04adc92ecec18'
OUT=ROOT/'biblaw-lemma-pos-benchmark-020.json'; DIS=ROOT/'biblaw-lemma-pos-disagreements-020.json'
SAMPLE_N=10000; KNOWN={'porte','suis','compte','garde','bien'}
spec=importlib.util.spec_from_file_location('occ',ROOT/'scripts/build_linguistic_occurrence_index.py')
occ=importlib.util.module_from_spec(spec); spec.loader.exec_module(occ)
def dash(ch): return bool(ch) and unicodedata.category(ch)=='Pd'
def case_class(s):
    if s.islower(): return 'LOWER'
    if s.isupper(): return 'UPPER'
    if s[:1].isupper() and s[1:].islower(): return 'TITLE'
    return 'MIXED'
def band(n):
    if n>=1000:return 'VERY_FREQUENT_1000_PLUS'
    if n>=100:return 'FREQUENT_100_999'
    if n>=10:return 'MEDIUM_10_99'
    return 'RARE_1_9'
def stable_score(oid): return int(hashlib.sha256(oid.encode()).hexdigest(),16)
def iter_tokens():
    cat=json.loads(occ.CATALOG.read_text(encoding='utf-8'))
    for rel in cat['records']:
        p=ROOT/rel
        if not p.exists(): raise RuntimeError(f'missing {rel}')
        obj=json.loads(p.read_text(encoding='utf-8'))
        if not occ.searchable(rel,obj): continue
        bn,pn=occ.meta(obj)
        for field,vn,text in occ.fields(obj):
            for m in occ.TOKEN_RE.finditer(text):
                s=m.group(); n=occ.norm(s); st,en=m.span(); oid=occ.oid(obj['id'],field,vn,st,en)
                yield {'occurrenceId':oid,'recordId':obj['id'],'recordType':obj.get('recordType'),'bookNumber':bn,'psalmNumber':pn,'verseNumber':vn,'field':field,'surface':s,'normalizedForm':n,'startOffset':st,'endOffset':en,'apostrophe':("'" in s or '’' in s),'hyphenAdjacency':dash(text[st-1] if st else '') or dash(text[en] if en<len(text) else ''),'caseClass':case_class(s),'text':text}
def sample():
    freq=Counter(x['normalizedForm'] for x in iter_tokens()); reservoirs=defaultdict(list); known={}; CAP=32
    for x in iter_tokens():
        x['frequencyBand']=band(freq[x['normalizedForm']]); sig=(x['frequencyBand'],str(x['apostrophe']),str(x['hyphenAdjacency']),x['caseClass'],str(x['bookNumber']),x['field'],str(x['recordType']))
        h=reservoirs[sig]; item=(-stable_score(x['occurrenceId']),x['occurrenceId'],x)
        if len(h)<CAP: heapq.heappush(h,item)
        elif item>h[0]: heapq.heapreplace(h,item)
        if x['normalizedForm'] in KNOWN: known[x['occurrenceId']]=x
    queues={k:sorted((z[2] for z in v),key=lambda x:(stable_score(x['occurrenceId']),x['occurrenceId'])) for k,v in reservoirs.items()}
    keys=sorted(queues,key=lambda k:tuple(k)); selected=[]; seen=set(); idx=defaultdict(int)
    while len(selected)<SAMPLE_N:
        progressed=False
        for k in keys:
            i=idx[k]
            if i<len(queues[k]):
                x=queues[k][i]; idx[k]+=1; progressed=True
                if x['occurrenceId'] not in seen:
                    selected.append(x); seen.add(x['occurrenceId'])
                    if len(selected)==SAMPLE_N: break
        if not progressed: break
    if len(selected)!=SAMPLE_N: raise RuntimeError(f'sample only {len(selected)}')
    return freq,selected,[x for oid,x in sorted(known.items()) if oid not in seen]
def load_repo_gold():
    out={}
    for name in ['porte','suis','compte','garde']:
        p=ROOT/f'data/linguistic/gold/{name}-gold.json'; data=json.loads(p.read_text(encoding='utf-8'))
        for e in data['entries']:
            lemma=e.get('lemma'); pos=e.get('partOfSpeech')
            out[e['occurrenceId']]={'source':p.as_posix().replace(ROOT.as_posix()+'/',''),'lemma':lemma if lemma else 'NOT_DIRECTLY_COMPARABLE','pos':pos if pos else 'NOT_DIRECTLY_COMPARABLE'}
    return out
def spacy_run(rows):
    import spacy, fr_core_news_sm
    nlp=fr_core_news_sm.load(disable=['ner']); results={}; texts=[x['text'] for x in rows]
    for x,doc in zip(rows,nlp.pipe(texts,batch_size=64)):
        matches=[t for t in doc if t.idx==x['startOffset'] and t.idx+len(t.text)==x['endOffset']]
        if len(matches)!=1: results[x['occurrenceId']]={'alignmentStatus':'ALIGNMENT_FAILURE','externalLemma':None,'externalPOS':None,'externalMorphology':None}
        else:
            t=matches[0]; results[x['occurrenceId']]={'alignmentStatus':'ALIGNED','externalLemma':t.lemma_ or None,'externalPOS':t.pos_ or None,'externalMorphology':str(t.morph) or None}
    return results,spacy.__version__,fr_core_news_sm.__version__
def stanza_run(rows):
    import stanza
    model_dir=os.environ.get('STANZA_RESOURCES_DIR',str(ROOT/'.stanza_resources_020'))
    nlp=stanza.Pipeline('fr',dir=model_dir,processors='tokenize,mwt,pos,lemma',package='default',download_method=None,use_gpu=False,verbose=False); results={}
    BATCH=128
    for start in range(0,len(rows),BATCH):
        chunk=rows[start:start+BATCH]
        docs=nlp([stanza.Document([],text=x['text']) for x in chunk])
        for x,doc in zip(chunk,docs):
            matches=[]
            for sent in doc.sentences:
                for tok in sent.tokens:
                    if tok.start_char==x['startOffset'] and tok.end_char==x['endOffset'] and len(tok.words)==1: matches.append(tok.words[0])
            if len(matches)!=1: results[x['occurrenceId']]={'alignmentStatus':'ALIGNMENT_FAILURE','externalLemma':None,'externalPOS':None,'externalMorphology':None}
            else:
                w=matches[0]; results[x['occurrenceId']]={'alignmentStatus':'ALIGNED','externalLemma':w.lemma or None,'externalPOS':w.upos or None,'externalMorphology':w.feats or None}
        print(f'STANZA_PROGRESS = {min(start+BATCH,len(rows))}/{len(rows)}',flush=True)
    return results,stanza.__version__
def main():
    freq,general,supp=sample(); gold=load_repo_gold(); rows=general+supp; by={}; ordered=[]
    for x in rows:
        if x['occurrenceId'] not in by: by[x['occurrenceId']]=x; ordered.append(x)
    spa,sv,smv=spacy_run(ordered); sta,stv=stanza_run(ordered)
    bench=[]; disag=[]; metrics=Counter(); bands=defaultdict(Counter); special=defaultdict(Counter); gold_metrics=Counter()
    general_ids={x['occurrenceId'] for x in general}
    for x in ordered:
        a=spa[x['occurrenceId']]; b=sta[x['occurrenceId']]; aligned=a['alignmentStatus']=='ALIGNED' and b['alignmentStatus']=='ALIGNED'
        if a['alignmentStatus']!='ALIGNED': metrics['spacy_alignment_failure']+=1
        if b['alignmentStatus']!='ALIGNED': metrics['stanza_alignment_failure']+=1
        if aligned:
            metrics['both_aligned']+=1; la=(a['externalLemma'] or '').casefold(); lb=(b['externalLemma'] or '').casefold(); pa=a['externalPOS']; pb=b['externalPOS']
            metrics['lemma_agree' if la==lb else 'lemma_disagree']+=1; metrics['pos_agree' if pa==pb else 'pos_disagree']+=1
            bands[x['frequencyBand']]['n']+=1; bands[x['frequencyBand']]['lemmaAgree']+=int(la==lb); bands[x['frequencyBand']]['posAgree']+=int(pa==pb)
            for key,flag in [('apostrophe',x['apostrophe']),('hyphenAdjacency',x['hyphenAdjacency'])]:
                if flag: special[key]['n']+=1; special[key]['lemmaAgree']+=int(la==lb); special[key]['posAgree']+=int(pa==pb)
        g=gold.get(x['occurrenceId'])
        if g:
            if g['lemma']!='NOT_DIRECTLY_COMPARABLE':
                gold_metrics['lemmaComparable']+=1
                if a['alignmentStatus']=='ALIGNED': gold_metrics['spacyLemmaCorrect']+=int((a['externalLemma'] or '').casefold()==g['lemma'].casefold())
                if b['alignmentStatus']=='ALIGNED': gold_metrics['stanzaLemmaCorrect']+=int((b['externalLemma'] or '').casefold()==g['lemma'].casefold())
            if g['pos']!='NOT_DIRECTLY_COMPARABLE':
                gold_metrics['posComparable']+=1
                if a['alignmentStatus']=='ALIGNED': gold_metrics['spacyPosCorrect']+=int(a['externalPOS']==g['pos'])
                if b['alignmentStatus']=='ALIGNED': gold_metrics['stanzaPosCorrect']+=int(b['externalPOS']==g['pos'])
        item={'occurrenceId':x['occurrenceId'],'sampleSource':'GENERAL_10000' if x['occurrenceId'] in general_ids else 'KNOWN_FORM_SUPPLEMENT','surfaceBiblaw':x['surface'],'normalizedFormBiblaw':x['normalizedForm'],'frequencyBand':x['frequencyBand'],'apostrophe':x['apostrophe'],'hyphenAdjacency':x['hyphenAdjacency'],'recordId':x['recordId'],'bookNumber':x['bookNumber'],'psalmNumber':x['psalmNumber'],'verseNumber':x['verseNumber'],'field':x['field'],'startOffset':x['startOffset'],'endOffset':x['endOffset'],'spacy':dict(a,engine='spaCy',engineVersion=sv,model='fr_core_news_sm',modelVersion=smv),'stanza':dict(b,engine='Stanza',engineVersion=stv,model='fr/default',modelVersion='resources_1.14.0'),'existingGold':g}
        bench.append(item)
        if not aligned or (aligned and (((a['externalLemma'] or '').casefold()!=(b['externalLemma'] or '').casefold()) or a['externalPOS']!=b['externalPOS'])):
            d=dict(item); d['context']=x['text'][max(0,x['startOffset']-100):min(len(x['text']),x['endOffset']+100)]; disag.append(d)
    payload={'mission':'BIBLAW-LEXICAL-INDUSTRIALIZATION-020','sourceBaseline':BASELINE,'source019Head':SOURCE_HEAD,'executedHead':os.getenv('GITHUB_SHA','LOCAL'),'sampleAlgorithm':{'size':SAMPLE_N,'frequencyBands':['1-9','10-99','100-999','1000+'],'signature':['frequencyBand','apostrophe','hyphenAdjacency','caseClass','bookNumber','field','recordType'],'withinSignature':'smallest SHA256(occurrenceId), reservoir cap 32','selection':'lexicographically sorted signatures, deterministic round-robin until exactly 10000','modelOutputsUsedForSelection':False},'generalSampleSize':len(general),'knownFormSupplementSize':len(supp),'benchmarkOccurrenceCount':len(ordered),'engines':{'spacy':{'version':sv,'model':'fr_core_news_sm','modelVersion':smv},'stanza':{'version':stv,'model':'fr/default combined','resourcesVersion':'1.14.0'}},'morphalou':{'status':'DEFERRED','reason':'ORTOLANG resource access requires licence acceptance; no automated acceptance or circumvention in 020'},'alignmentMethod':'External native tokenization on exact canonical field text; target accepted only when exactly one external token has start/end chars identical to BIBLAW startOffset/endOffset; Stanza additionally requires exactly one Word inside Token.','metrics':dict(metrics),'agreementByFrequencyBand':{k:dict(v) for k,v in sorted(bands.items())},'specialAgreement':{k:dict(v) for k,v in special.items()},'knownGoldMetrics':dict(gold_metrics),'occurrences':bench}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); DIS.write_text(json.dumps({'mission':'020','count':len(disag),'disagreements':disag},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('GENERAL_SAMPLE_SIZE =',len(general)); print('KNOWN_FORM_SUPPLEMENT_SIZE =',len(supp)); print('BENCHMARK_OCCURRENCE_COUNT =',len(ordered))
    for k,v in sorted(metrics.items()): print(k.upper(), '=',v)
    print('KNOWN_GOLD_METRICS =',json.dumps(dict(gold_metrics),sort_keys=True)); print('AGREEMENT_BY_FREQUENCY_BAND =',json.dumps({k:dict(v) for k,v in sorted(bands.items())},sort_keys=True)); print('SPECIAL_AGREEMENT =',json.dumps({k:dict(v) for k,v in special.items()},sort_keys=True))
if __name__=='__main__': main()
