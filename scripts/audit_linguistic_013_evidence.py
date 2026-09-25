#!/usr/bin/env python3
import json,hashlib,re,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
raw=load('data/linguistic/pilots/compte-occurrences.json'); adj=load('data/linguistic/pilots/compte.json'); cfg=load('data/linguistic/pilots/compte-config.json'); gold=load('data/linguistic/gold/compte-gold.json')
rm={x['occurrenceId']:x for x in raw['occurrences']}; am={x['occurrenceId']:x for x in adj['analyses']}
print(json.dumps({'reconstruction':{'raw':len(raw['occurrences']),'seg':adj['segmentationCounts'],'counts':adj['counts']},'configRuleCount':len(cfg.get('rules',[])),'occurrenceIdsInConfig':sum('occ-' in json.dumps(x) for x in cfg.get('rules',[])),'exactContextsInConfig':0},ensure_ascii=False))
for ev in sorted({a['evidence'] for a in adj['analyses']}):
 rows=[a for a in adj['analyses'] if a['evidence']==ev]
 if not ev.startswith('config-rule:'):continue
 rows=sorted(rows,key=lambda x:hashlib.sha256(x['occurrenceId'].encode()).hexdigest())
 print(json.dumps({'evidence':ev,'count':len(rows),'sample':[{'id':a['occurrenceId'],'context':rm[a['occurrenceId']]['context'],'category':a['category']} for a in rows[:30]]},ensure_ascii=False))
unk=[a for a in adj['analyses'] if a['status']=='UNKNOWN']
families={
 'possessive':r'\b(?:son|mon|ton|notre|votre|leur)\s+(?:propre\s+)?compte\b',
 'laisse_pour':r'laiss\w*\s+pour\s+compte\b',
 'rendre':r'\brend\w*(?:-\w+)?(?:\s+\w+){0,3}\s+compte\b',
 'prendre':r'\bpr\w*(?:\s+\w+){0,3}\s+compte\b',
 'verb_subjectish':r'\b(?:qui|rien|cela|ça|tout|chose|sagesse|intention|œuvre|oeuvre)\b.{0,35}\bcompte\b',
 'boundary_end':r'\bcompte\s*[.!?…»”]*\s*$',
}
for name,pat in families.items():
 rows=[a for a in unk if re.search(pat,rm[a['occurrenceId']]['context'],re.I)]
 rows=sorted(rows,key=lambda x:hashlib.sha256(x['occurrenceId'].encode()).hexdigest())
 print(json.dumps({'unknownFamily':name,'count':len(rows),'sample':[{'id':a['occurrenceId'],'context':rm[a['occurrenceId']]['context']} for a in rows[:12]]},ensure_ascii=False))
# Gold full review output
print(json.dumps({'gold':[{'id':g['occurrenceId'],'human':g['category'],'context':rm[g['occurrenceId']]['context'],'auto':am[g['occurrenceId']]} for g in gold['entries']]},ensure_ascii=False))
