/* Biblaw : les Anges-perles et Anges-fils selon le collier de Gabriel.
   Les citations sont des occurrences textuelles, jamais une attribution spirituelle automatique. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const s = {data:null,loading:null,perles:[],fils:[],mode:'perles',
    records:[],loadCorpus:null,openPsalm:null,selected:null,
    cache:new Map(),requestId:0,directoryScroll:0,readerScroll:0,lastLink:null};
  const archangel = key => ({michael:'Michaël',gabriel:'Gabriel',
    raphael:'Raphaël',ouriel:'Ouriel'})[key] || key || '';
  const norm = value => String(value || '').toLowerCase()
    .replace(/œ/g,'oe').replace(/æ/g,'ae').normalize('NFD')
    .replace(/[\u0300-\u036f]/g,'');
  const count = (n,term) => n + ' ' + term + (n>1?'s':'');
  function el(tag,klass,content) {
    const x=document.createElement(tag);
    if(klass)x.className=klass;
    if(content!==undefined)x.textContent=content;
    return x;
  }
  function status(value) {
    $('angelsStatus').textContent=value||'';
    $('angelsStatus').hidden=!value;
  }
  const top=()=>window.scrollTo({top:0,behavior:'instant'});
  const tick=()=>new Promise(resolve=>setTimeout(resolve,0));

  function spellings(label) {
    const word=norm(label), forms=[word];
    if(!/[sxz]$/.test(word))forms.push(word+'s');
    const extras={
      cache:['caches','cachee','cachees'],
      travail:['travaux'],sacre:['sacree','sacres','sacrees'],
      'bon sens':['bons sens'],
      'bonne disposition':['bonnes dispositions'],
      'soutien mutuel':['soutiens mutuels'],
      bien:['biens']
    };
    return [...new Set(forms.concat(extras[word]||[]))];
  }
  function regexFor(label) {
    const escape = text=>text.replace(/[|\\{}()[\]^$+*?.]/g,'\\$&');
    const terms=spellings(label).map(spelling=>spelling
      .split(/\s+/).map(escape).join('[\\s\\-\\u2010-\\u2015]+'));
    return new RegExp('(?<![a-z0-9])(?:'+terms.join('|')+')(?![a-z0-9])');
  }
  function excerpt(original,match,max=245) {
    const text=String(original||'').replace(/\s+/g,' ').trim();
    if(text.length<=max)return text;
    let position=0,i=0;
    for(;i<text.length;i++){
      const size=norm(text[i]).length;
      if(position+size>match.index)break;
      position+=size;
    }
    let begin=Math.max(0,i-75),end=Math.min(text.length,begin+max);
    begin=Math.max(0,end-max);
    if(begin){const cut=text.indexOf(' ',begin);if(cut>=0&&cut-begin<20)begin=cut+1;}
    if(end<text.length){const cut=text.lastIndexOf(' ',end);if(cut>begin&&end-cut<20)end=cut;}
    return (begin?'…':'')+text.slice(begin,end).trim()+(end<text.length?'…':'');
  }
  async function corpus() {
    if(s.records.length===1158)return true;
    if(typeof s.loadCorpus!=='function')throw Error('Corpus non disponible.');
    if(!await s.loadCorpus()||s.records.length!==1158)
      throw Error('Impossible de vérifier les 1 158 psaumes.');
    return true;
  }
  async function occurrences(entry,request) {
    if(s.cache.has(entry.label))return s.cache.get(entry.label);
    const pattern=regexFor(entry.label),out=[];
    for(let i=0;i<s.records.length;i++){
      if(request!==s.requestId)return null;
      const psalm=s.records[i],verses=[];
      for(const verse of psalm.verses||[]){
        const match=pattern.exec(norm(verse.text));
        if(match)verses.push({number:verse.number,excerpt:excerpt(verse.text,match)});
      }
      if(verses.length)out.push({recordId:psalm.id,book:psalm.book.number,
        psalm:psalm.number,archangel:psalm.archangel,verses});
      if(i%48===47){
        status('Recherche dans les psaumes… '+Math.round(100*(i+1)/1158)+' %');
        await tick();
      }
    }
    out.sort((a,b)=>a.book-b.book||a.psalm-b.psalm);
    s.cache.set(entry.label,out);
    return out;
  }
  function entries(){return s.mode==='perles'?s.perles:s.fils;}
  function directory(){
    ++s.requestId;
    s.selected=null;
    $('angelsDirectory').hidden=false;
    $('angelsDetail').hidden=true;
    const filter=norm($('angelsFilter').value.trim()),group=$('angelsGroup').value;
    const shown=entries().filter(e=>(!group||e.parentId===group)&&
      (!filter||norm(e.label).includes(filter)||norm(e.parentLabel||'').includes(filter)));
    $('angelsCount').textContent=shown.length+' sur '+entries().length+
      (s.mode==='perles'?' Anges-perles.':' Anges-fils.');
    const list=$('angelsList');
    list.replaceChildren();
    for(const entry of shown){
      const button=el('button','faq-question-item angels-item');
      button.type='button';
      const contents=el('span','faq-question-title');
      const sources=s.cache.get(entry.label);
      contents.append(el('strong','',entry.label));
      contents.append(el('small','',entry.parentLabel?
        'Ange-perle : '+entry.parentLabel+
          (sources?' · '+count(sources.length,'psaume'):''):
        entry.dates+(sources?' · '+count(sources.length,'psaume'):'')));
      button.append(contents,el('span','faq-chevron','›'));
      button.addEventListener('click',()=>{void detail(entry);});
      list.append(button);
    }
    if(!shown.length)list.append(el('p','angels-empty','Aucun résultat pour ce nom.'));
  }
  function mode(modeName){
    s.mode=modeName;
    $('angelsTitle').textContent=modeName==='perles'?
      'Les 12 Anges-perles':'Les 144 Anges-fils';
    $('angelsIntro').textContent=modeName==='perles'?
      'Choisissez un Ange-perle pour lire ses correspondances et rechercher les passages où sa vertu est nommée.':
      'Les 144 Anges-fils classés par Ange-perle. Choisissez une vertu pour retrouver les psaumes qui la nomment.';
    $('angelsGroupWrap').hidden=modeName!=='fils';
    $('angelsFilter').value='';
    $('angelsGroup').value='';
    $('angelsMethod').textContent=s.data.editorialNotice+
      ' La recherche porte sur les 1 158 psaumes canoniques et les formes grammaticales simples, sans synonymes supposés.';
    directory();
  }
  function metadata(entry){
    const box=$('angelsMetadata');
    box.replaceChildren();
    const parent=s.perles.find(p=>p.id===(entry.parentId||entry.id));
    if(!parent)return;
    if(entry.parentId)box.append(el('p','angels-parent','Ange-perle : '+parent.label));
    else{
      box.append(el('p','angels-parent',parent.dates+' · '+parent.zodiaque+' · '+parent.element));
      box.append(el('p','angels-description','Pierre : '+parent.pierre+' · Plante : '+
        parent.plante+' · Partie du corps : '+parent.partieCorps));
      box.append(el('p','angels-description','Gardiens : '+parent.gardiens));
      box.append(el('p','angels-description','Ses 12 Anges-fils : '+parent.fils.join(' · ')));
    }
    if(entry.label==='Illua')box.append(el('p','angels-warning',s.data.transcriptionNotice));
  }
  function verseCard(source,verse){
    const row=el('div','angels-verse');
    row.append(el('p','angels-excerpt','« '+verse.excerpt+' »'));
    const link=el('button','faq-psalm-link angels-reference',
      'Lire le psaume '+source.psalm+' de '+archangel(source.archangel)+
      ', verset '+verse.number);
    link.type='button';
    link.addEventListener('click',()=>void openVerse(source,verse,link));
    row.append(link);
    return row;
  }
  function psalmCard(source){
    const card=el('section','angels-source');
    card.append(el('h4','','Psaume '+source.psalm+' de '+
      archangel(source.archangel)+' · Livre '+source.book));
    card.append(verseCard(source,source.verses[0]));
    if(source.verses.length>1){
      const more=el('details','angels-more');
      more.append(el('summary','','Voir '+count(source.verses.length-1,'autre verset')));
      const inside=el('div','');
      for(const v of source.verses.slice(1))inside.append(verseCard(source,v));
      more.append(inside);
      card.append(more);
    }
    return card;
  }
  function renderSources(sources){
    const box=$('angelsReferences');
    box.replaceChildren();
    const n=sources.reduce((sum,item)=>sum+item.verses.length,0);
    $('angelsSummary').textContent=sources.length?
      '« '+s.selected.label+' » apparaît dans '+count(sources.length,'psaume')+
        ' et '+count(n,'verset')+
        '. Mentions textuelles, sans supposer que chaque passage parle d’un Ange.':
      'Aucune mention explicite de « '+s.selected.label+
        ' » dans les 1 158 psaumes. Le thème peut néanmoins y être présent autrement.';
    let position=0;
    const more=el('button','secondary angels-load-more');
    more.type='button';
    const append=()=>{
      for(const source of sources.slice(position,position+20))
        box.insertBefore(psalmCard(source),more);
      position=Math.min(position+20,sources.length);
      more.hidden=position===sources.length;
      more.textContent='Afficher '+Math.min(20,sources.length-position)+
        ' psaumes supplémentaires ('+(sources.length-position)+' restants)';
    };
    more.addEventListener('click',append);
    box.append(more);
    append();
  }
  async function detail(entry){
    s.directoryScroll=window.scrollY;
    s.selected=entry;
    const request=++s.requestId;
    $('angelsDirectory').hidden=true;
    $('angelsDetail').hidden=false;
    $('angelsName').textContent=entry.label;
    $('angelsSummary').textContent='';
    $('angelsReferences').replaceChildren();
    metadata(entry);
    top();
    $('angelsName').focus({preventScroll:true});
    status('Chargement et recherche des psaumes…');
    try{
      if(!s.cache.has(entry.label))await corpus();
      if(request!==s.requestId||$('angelsLibrary').hidden)return;
      const sources=await occurrences(entry,request);
      if(request!==s.requestId||!sources)return;
      status('');
      renderSources(sources);
    }catch(error){
      if(request===s.requestId)status(error.message||'Recherche indisponible.');
      console.error(error);
    }
  }
  async function openVerse(source,verse,button){
    s.lastLink=button;s.readerScroll=window.scrollY;
    const request=s.requestId;
    try{
      await corpus();
      if(request!==s.requestId||$('angelsLibrary').hidden)return;
      if(typeof s.openPsalm!=='function')throw Error('Lecteur indisponible.');
      s.openPsalm({recordId:source.recordId,verses:[verse.number]});
    }catch(error){
      if(request===s.requestId)status(error.message||'Lecture impossible.');
      console.error(error);
    }
  }
  async function load(){
    if(s.data)return true;
    if(s.loading)return s.loading;
    s.loading=Promise.all([
      fetch('data/anges-gabriel.json?v=001'),
      fetch('data/angels-public.json?v=001')
    ]).then(async ([response,indexResponse])=>{
      if(!response.ok||!indexResponse.ok)
        throw Error('Répertoire des Anges indisponible.');
      const [data,compiled]=await Promise.all([response.json(),indexResponse.json()]);
      if(data.schemaVersion!==1||!Array.isArray(data.perles)||
        data.perles.length!==12||data.perles.some(p=>!Array.isArray(p.fils)||p.fils.length!==12))
        throw Error('Liste des 12 × 12 Anges incomplète.');
      if(compiled.schemaVersion!==1||compiled.psalmCount!==1158||
        compiled.perlesCount!==12||compiled.filsCount!==144||
        compiled.entryCount!==156||!Array.isArray(compiled.entries)||
        compiled.entries.length!==156)
        throw Error('Index des 1 158 psaumes incomplet.');
      const allLabels=new Set(data.perles.flatMap(p=>[p.label,...p.fils]));
      if(allLabels.size!==156||new Set(compiled.entries.map(e=>e.label)).size!==156||
        compiled.entries.some(e=>!allLabels.has(e.label)||!Array.isArray(e.sources)||
          e.psalmCount!==e.sources.length))
        throw Error('Les références des Anges ne correspondent pas au collier.');
      s.data=data;s.perles=data.perles;
      for(const entry of compiled.entries)s.cache.set(entry.label,entry.sources);
      s.fils=data.perles.flatMap(parent=>parent.fils.map((label,index)=>({
        id:parent.id+'-fils-'+(index+1),label,
        parentId:parent.id,parentLabel:parent.label
      })));
      const choice=$('angelsGroup');
      choice.replaceChildren();
      const all=el('option','','Tous les Anges-perles');all.value='';choice.append(all);
      for(const p of data.perles){
        const option=el('option','',p.label);option.value=p.id;choice.append(option);
      }
      return true;
    }).catch(error=>{
      status(error.message||'Données indisponibles.');console.error(error);
      return false;
    }).finally(()=>{s.loading=null;});
    return s.loading;
  }
  async function open(modeName){
    const request=++s.requestId;
    $('angelsLibrary').hidden=false;
    document.body.classList.add('view-angels');
    $('perlesToggle').setAttribute('aria-expanded',String(modeName==='perles'));
    $('filsToggle').setAttribute('aria-expanded',String(modeName==='fils'));
    top();
    status('Chargement du collier de Gabriel…');
    const ready=await load();
    if(request!==s.requestId||$('angelsLibrary').hidden)return;
    if(ready){status('');mode(modeName);}
  }
  function close(){
    ++s.requestId;s.selected=null;
    $('angelsLibrary').hidden=true;
    document.body.classList.remove('view-angels');
    $('perlesToggle').setAttribute('aria-expanded','false');
    $('filsToggle').setAttribute('aria-expanded','false');
  }
  function back(){
    if(s.selected){
      const previous=s.directoryScroll;
      directory();status('');
      window.scrollTo({top:previous,behavior:'instant'});
    }else{
      const button=$(s.mode==='perles'?'perlesToggle':'filsToggle');
      close();top();button.focus({preventScroll:true});
    }
  }
  function restoreAfterPsalm(){
    if(!$('angelsLibrary').hidden&&s.selected){
      window.scrollTo({top:s.readerScroll,behavior:'instant'});
      s.lastLink?.focus({preventScroll:true});
    }
  }
  $('angelsBack').addEventListener('click',back);
  $('angelsFilter').addEventListener('input',()=>{if(s.data&&!s.selected)directory();});
  $('angelsGroup').addEventListener('change',()=>{if(s.data&&!s.selected)directory();});
  globalThis.BiblawAngels=Object.freeze({
    open,close,restoreAfterPsalm,
    setOpenPsalm(callback){s.openPsalm=callback;},
    setCorpusLoading(callback){s.loadCorpus=callback;},
    setRecords(records){s.records=(records||[]).filter(record=>
      record.recordType==='psalm'&&/^book-\d{2}-psalm-\d{3}$/.test(record.id));}
  });
})();
