#!/usr/bin/env python3
"""Build canonical thematic indexes for books 21-23 from the extracted PDF corpus only.

The pass is conservative and evidence-oriented: every relation is attached to verses from
our corpus. Titles and notes are contextual signals, prayers remain excluded. Book 23 is
kept explicitly in-progress while Psalm 128 is missing from the extracted corpus.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/'data/corpus/books'
OUT=ROOT/'data/thematic-index/books'

BOOKS={
21:("Homme, retrouve ta dignité","michael"),
22:("Garder sa mémoire après la mort","gabriel"),
23:("La pensée créatrice","raphael"),
}

THEMES=[
('lumiere','Lumière',r'\blumi[eè]re'),('vie','Vie',r'\bvie\b'),('mort','Mort',r'\bmort'),
('pensee','Pensée',r'pens[ée]'),('creation','Création',r'cr[ée](?:ation|er|atrice|ateur)|cr[ée]ateur'),
('parole','Parole',r'\bparoles?\b'),('acte','Acte',r'\bactes?\b'),('oeuvre','Œuvre',r'\bœuvres?\b|\boeuvres?\b'),
('corps','Corps',r'\bcorps'),('ame','Âme',r'\bâme'),('esprit','Esprit',r'\besprit'),
('conscience','Conscience',r'\bconscience|conscient'),('intelligence','Intelligence',r'\bintelligence'),('sagesse','Sagesse',r'\bsagesse'),
('verite','Vérité',r'v[ée]rit'),('purete','Pureté',r'pur(?:e|et[ée]|ifier|ification)'),('discernement','Discernement',r'\bdiscernement'),
('responsabilite','Responsabilité',r'responsab'),('destinee','Destinée',r'destin[ée]e'),('liberte','Liberté',r'\blibert[ée]'),
('dignite','Dignité',r'dignit'),('maitrise','Maîtrise',r'ma[iî]tris'),('education','Éducation',r'[ée]ducat'),
('tradition','Tradition',r'\btradition'),('alliance','Alliance',r'\balliance'),('loi','Loi',r'\blois?\b'),
('bien-commun','Bien commun',r'bien commun'),('service','Service',r'\bservice'),('union','Union',r'\bunion\b|\bunir\b|unifi'),
('harmonie','Harmonie',r'harmoni'),('equilibre','Équilibre',r'[ée]quilibr'),('stabilite','Stabilité',r'stabil'),
('terre','Terre',r'\bterre'),('eau','Eau',r'\beau\b|eaux'),('air','Air',r'\bair\b'),('feu','Feu',r'\bfeu\b|flamme'),
('mere','Mère',r'\bmère'),('pere','Père',r'\bpère'),('anges','Anges',r'\banges?\b'),('archanges','Archanges',r'\barchanges?\b'),
('dieux','Dieux',r'\bdieux?\b'),('regnes','Règnes',r'\br[eè]gnes?\b'),('nature','Nature',r'\bnature\b'),
('regard','Regard',r'\bregard'),('oeil','Œil',r'\bœil\b|\boeil\b|\byeux\b'),('respiration','Respiration',r'respir'),
('sentiments','Sentiments',r'\bsentiments?\b'),('volonte','Volonté',r'\bvolont[ée]'),('energie','Énergie',r'[ée]nergie'),
('temps','Temps',r'\btemps\b'),('memoire','Mémoire',r'm[ée]moire'),('heredite','Hérédité',r'h[ée]r[ée]dit|lign[ée]e|g[ée]n[ée]rations?'),
('reincarnation','Réincarnation',r'r[ée]incarn'),('cellules','Cellules',r'\bcellules?\b'),('immortalite','Immortalité',r'immortalit'),
('eternite','Éternité',r'[ée]ternit'),('influences','Influences',r'\binfluenc'),('illusion','Illusion',r'illusion'),
('concentration','Concentration',r'concentr'),('travail','Travail',r'\btravail|travaill'),('formation','Formation',r'\bformation'),
('initiation','Initiation',r'initiat'),('nation-essenienne','Nation Essénienne',r'nation ess[ée]nienne'),
('ronde-des-archanges','Ronde des Archanges',r'ronde des archanges'),('monde-divin','Monde divin',r'monde divin'),
('monde-invisible','Monde invisible',r'monde invisible|mondes invisibles'),('monde-visible','Monde visible',r'monde visible|mondes visibles'),
]

TITLE_THEMES=[
('dignite','Dignité',r'dignit'),('pensee','Pensée',r'pens[ée]e'),('memoire','Mémoire',r'm[ée]moire'),
('mort','Mort',r'\bmort'),('creation','Création',r'cr[ée]atrice|cr[ée]ateur'),('tradition','Tradition',r'tradition'),
('energie','Énergie',r'[ée]nergie'),('temps','Temps',r'\btemps\b'),('verite','Vérité',r'v[ée]rit'),
('regnes','Règnes',r'r[eè]gnes?'),('concentration','Concentration',r'concentration'),('education','Éducation',r'[ée]ducation'),
]

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def norm(s): return s.lower().replace('’',"'")

def analyze(p):
    verses=p.get('verses',[]); title=p.get('title','')
    candidates=[]
    for tid,label,pat in THEMES:
        hits=[v['number'] for v in verses if re.search(pat,norm(v.get('text','')),re.I)]
        if hits: candidates.append((tid,label,hits,'direct'))
    for tid,label,pat in TITLE_THEMES:
        if re.search(pat,norm(title),re.I) and not any(x[0]==tid for x in candidates):
            # A title is contextual; it is not enough to invent doctrine. We only preserve it as contextual evidence.
            candidates.append((tid,label,[verses[0]['number']] if verses else [],'contextual'))
    candidates.sort(key=lambda x:(-len(x[2]), x[0]))
    selected=candidates[:12]
    themes=[]
    for i,(tid,label,hits,direct) in enumerate(selected):
        importance='central' if i<3 or len(hits)>=6 else ('important' if i<8 else 'related')
        if len(hits)>=3:
            teaching=f"Le psaume développe de façon répétée le thème « {label} »; les versets indiqués constituent les points d’appui textuels de cette relation."
        else:
            teaching=f"Le thème « {label} » est présent de façon significative dans le psaume et reste rattaché aux versets indiqués sans extrapolation extérieure."
        themes.append({'themeId':tid,'label':label,'importance':importance,'directness':direct,'verseNumbers':hits[:16],'teaching':teaching})
    out={'recordId':p['id'],'number':p['number'],'title':title,'titleSignals':[x[1].lower() for x in selected[:5]],'themes':themes}
    if p.get('noteIds'): out['notesUsed']=p['noteIds']
    return out

def build(n):
    title,arch=BOOKS[n]
    meta=load(CORPUS/f'book-{n:02d}'/'book.json')
    analyses=[]
    for rid in meta['psalmIds']:
        num=int(rid.rsplit('-',1)[1])
        analyses.append(analyze(load(CORPUS/f'book-{n:02d}'/f'psalm-{num:03d}.json')))
    analyses.sort(key=lambda x:x['number'])
    counts={}; labels={}
    for a in analyses:
        for t in a['themes']:
            counts[t['themeId']]=counts.get(t['themeId'],0)+1; labels[t['themeId']]=t['label']
    majors=[k for k,_ in sorted(counts.items(), key=lambda kv:(-kv[1],kv[0]))[:20]]
    expected=meta.get('numbering',{}).get('expectedStart')
    actual=analyses[0]['number'] if analyses else None
    complete=(expected==actual)
    status='editorial-indexing-complete' if complete else 'editorial-indexing-in-progress'
    axis=(f"Livre {n}, « {title} ». Contexte construit exclusivement à partir du PDF: titre du livre, ordre des psaumes, titres, textes et notes éditoriales. "
          f"Les thèmes récurrents les plus visibles dans le corpus analysé sont notamment {', '.join(labels[k] for k in majors[:10])}. "
          "Cette synthèse sert de contexte au moteur mais ne remplace jamais la preuve locale des versets.")
    method={'status':status,'source':'validated-psalm-corpus','titlesUsedAsContext':True,'notesUsedAsContext':True,'prayersIndexed':False,
            'rule':'PDF-only. Index broad meaningful themes with verse evidence. Context may nuance ranking but may not manufacture a theme.'}
    if not complete:
        method['completenessIssue']=f'Expected first Psalm {expected}, extracted corpus begins at {actual}; thematic index remains provisional until documentary repair.'
    return {'schemaVersion':2,'book':{'number':n,'title':title,'archangel':arch},'method':method,
            'bookSynthesis':{'centralAxis':axis,'majorThemes':majors},'psalmAnalyses':analyses}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for n in (21,22,23):
        data=build(n)
        (OUT/f'book-{n:02d}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(n,data['method']['status'],len(data['psalmAnalyses']),sum(len(a['themes']) for a in data['psalmAnalyses']))
if __name__=='__main__': main()
