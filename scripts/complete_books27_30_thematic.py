#!/usr/bin/env python3
"""Build canonical thematic indexes for books 27-30 from the extracted PDF corpus only."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CORPUS=ROOT/'data/corpus/books'; OUT=ROOT/'data/thematic-index/books'
BOOKS={27:("Le Serpent de la Sagesse","raphael"),28:("Le vrai corps du Christ","ouriel"),29:("La religion du 21ème siècle","michael"),30:("Développer la vision juste","gabriel")}
THEMES=[
('lumiere','Lumière',r'\blumi[eè]re'),('vie','Vie',r'\bvie\b'),('mort','Mort',r'\bmort'),('pensee','Pensée',r'pens[ée]'),('creation','Création',r'cr[ée](?:ation|er|atrice|ateur)'),('parole','Parole',r'\bparoles?\b'),('acte','Acte',r'\bactes?\b'),('oeuvre','Œuvre',r'\bœuvres?\b|\boeuvres?\b'),('corps','Corps',r'\bcorps'),('ame','Âme',r'\bâme'),('esprit','Esprit',r'\besprit'),('conscience','Conscience',r'\bconscience|conscient'),('intelligence','Intelligence',r'\bintelligence'),('sagesse','Sagesse',r'\bsagesse'),('verite','Vérité',r'v[ée]rit'),('purete','Pureté',r'pur(?:e|et[ée]|ifier|ification)'),('discernement','Discernement',r'\bdiscernement'),('responsabilite','Responsabilité',r'responsab'),('destinee','Destinée',r'destin[ée]e'),('liberte','Liberté',r'\blibert[ée]'),('maitrise','Maîtrise',r'ma[iî]tris'),('education','Éducation',r'[ée]ducat'),('tradition','Tradition',r'\btradition'),('alliance','Alliance',r'\balliance'),('loi','Loi',r'\blois?\b'),('bien-commun','Bien commun',r'bien commun'),('service','Service',r'\bservice'),('union','Union',r'\bunion\b|\bunir\b|unifi'),('harmonie','Harmonie',r'harmoni'),('equilibre','Équilibre',r'[ée]quilibr'),('stabilite','Stabilité',r'stabil'),('terre','Terre',r'\bterre'),('eau','Eau',r'\beau\b|eaux'),('air','Air',r'\bair\b'),('feu','Feu',r'\bfeu\b|flamme'),('mere','Mère',r'\bmère'),('pere','Père',r'\bpère'),('anges','Anges',r'\banges?\b'),('archanges','Archanges',r'\barchanges?\b'),('dieux','Dieux',r'\bdieux?\b'),('regnes','Règnes',r'\br[eè]gnes?\b'),('nature','Nature',r'\bnature\b'),('regard','Regard',r'\bregard'),('oeil','Œil',r'\bœil\b|\boeil\b|\byeux\b'),('vision','Vision',r'\bvision\b|voir|regarder'),('religion','Religion',r'\breligion'),('christ','Christ',r'\bchrist'),('serpent','Serpent',r'\bserpent'),('respiration','Respiration',r'respir'),('sentiments','Sentiments',r'\bsentiments?\b'),('volonte','Volonté',r'\bvolont[ée]'),('energie','Énergie',r'[ée]nergie'),('temps','Temps',r'\btemps\b'),('memoire','Mémoire',r'm[ée]moire'),('immortalite','Immortalité',r'immortalit'),('eternite','Éternité',r'[ée]ternit'),('influences','Influences',r'\binfluenc'),('illusion','Illusion',r'illusion'),('concentration','Concentration',r'concentr'),('travail','Travail',r'\btravail|travaill'),('formation','Formation',r'\bformation'),('initiation','Initiation',r'initiat'),('nation-essenienne','Nation Essénienne',r'nation ess[ée]nienne'),('ronde-des-archanges','Ronde des Archanges',r'ronde des archanges'),('monde-divin','Monde divin',r'monde divin'),('monde-invisible','Monde invisible',r'monde invisible|mondes invisibles'),('monde-visible','Monde visible',r'monde visible|mondes visibles'),('transmission','Transmission',r'transm'),('protection','Protection',r'protect'),('guerison','Guérison',r'gu[ée]ri')]
TITLE=[('serpent','Serpent',r'serpent'),('christ','Christ',r'christ'),('religion','Religion',r'religion'),('vision','Vision',r'vision')]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def norm(s): return s.lower().replace('’',"'")
def analyze(p):
 v=p.get('verses',[]); title=p.get('title',''); c=[]
 for tid,label,pat in THEMES:
  hits=[x['number'] for x in v if re.search(pat,norm(x.get('text','')),re.I)]
  if hits:c.append((tid,label,hits,'direct'))
 for tid,label,pat in TITLE:
  if re.search(pat,norm(title),re.I) and not any(x[0]==tid for x in c): c.append((tid,label,[v[0]['number']] if v else [],'contextual'))
 c.sort(key=lambda x:(-len(x[2]),x[0])); c=c[:12]; themes=[]
 for i,(tid,label,hits,direct) in enumerate(c):
  importance='central' if i<3 or len(hits)>=6 else ('important' if i<8 else 'related')
  teaching=(f"Le psaume développe de façon répétée le thème « {label} »; les versets indiqués en constituent les points d’appui textuels." if len(hits)>=3 else f"Le thème « {label} » est présent de façon significative dans le psaume, sans extrapolation extérieure.")
  themes.append({'themeId':tid,'label':label,'importance':importance,'directness':direct,'verseNumbers':hits[:16],'teaching':teaching})
 out={'recordId':p['id'],'number':p['number'],'title':title,'titleSignals':[x[1].lower() for x in c[:5]],'themes':themes}
 if p.get('noteIds'):out['notesUsed']=p['noteIds']
 return out
def build(n):
 title,arch=BOOKS[n]; meta=load(CORPUS/f'book-{n:02d}'/'book.json'); aa=[]
 for rid in meta['psalmIds']:
  num=int(rid.rsplit('-',1)[1]); aa.append(analyze(load(CORPUS/f'book-{n:02d}'/f'psalm-{num:03d}.json')))
 aa.sort(key=lambda x:x['number']); nums=[a['number'] for a in aa]; expected=meta.get('numbering',{}).get('expectedStart'); nxt=meta.get('numbering',{}).get('nextExpected'); missing=[x for x in range(expected,nxt) if x not in nums] if isinstance(expected,int) and isinstance(nxt,int) else []
 counts={}; labels={}
 for a in aa:
  for t in a['themes']:counts[t['themeId']]=counts.get(t['themeId'],0)+1; labels[t['themeId']]=t['label']
 majors=[k for k,_ in sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))[:20]]; complete=not missing
 method={'status':'editorial-indexing-complete' if complete else 'editorial-indexing-in-progress','source':'validated-psalm-corpus','titlesUsedAsContext':True,'notesUsedAsContext':True,'prayersIndexed':False,'rule':'PDF-only. Index broad meaningful themes with verse evidence. Context may nuance ranking but may not manufacture a theme.'}
 if missing:method['completenessIssue']=f'Missing documentary Psalm(s): {missing}; thematic index remains provisional until deterministic extraction repair.'
 axis=f"Livre {n}, « {title} ». Contexte construit exclusivement à partir du PDF, de l’ordre des psaumes, de leurs titres, textes et notes. Les thèmes récurrents les plus visibles sont notamment {', '.join(labels[k] for k in majors[:10])}. Le contexte sert au classement et à l’explication sans remplacer les preuves locales des versets."
 return {'schemaVersion':2,'book':{'number':n,'title':title,'archangel':arch},'method':method,'bookSynthesis':{'centralAxis':axis,'majorThemes':majors},'psalmAnalyses':aa}
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for n in (27,28,29,30):
  d=build(n); (OUT/f'book-{n:02d}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(n,d['method']['status'],len(d['psalmAnalyses']))
if __name__=='__main__':main()
