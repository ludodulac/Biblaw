import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const read = path => readFileSync(new URL('../'+path, import.meta.url), 'utf8');
const html = read('index.html');
const numbers = JSON.parse(read('data/numbers-public.json'));
const corpus = JSON.parse(read('data/browser-search-catalog.json'));
const psalms = new Map(corpus.records.filter(r=>r.recordType==='psalm').map(r=>[r.id,r]));

assert.equal(numbers.schemaVersion,1);
assert.equal(numbers.psalmCount,1158);
assert.equal(psalms.size,1158);
assert.ok(numbers.entries.length>15);
assert.ok(numbers.entries.some(e=>e.value===7));
assert.ok(numbers.entries.some(e=>e.value===21));
const one=numbers.entries.find(e=>e.value===1);
assert.ok(one,'1 doit représenter l’unité, pas un article indéfini');
assert.equal(one.references.length,1,'Le simple fait de compter une chose ne suffit pas');
assert.equal(one.references[0].recordId,'book-05-psalm-028');
assert.equal(one.references[0].verse,3);
assert.match(one.summary,/unit[eé]|uni[st]/i);
assert.ok(numbers.entries.every(e=>e.title&&e.summary));
assert.ok(numbers.entries.every(e=>e.references.length>0));
assert.ok(html.includes('id="numbersToggle"') && html.includes('id="numbersLibrary"'));
assert.ok(!html.includes('numbers-site-tabs'), 'Pas d’onglet ajouté dans l’en-tête');
assert.ok(html.includes('js/biblaw-numbers.js'));
assert.ok(html.includes('css/biblaw-numbers.css'));
assert.ok(read('scripts/build_pages_site.py').includes('numbers-public.json'));
for(const id of ['numbersToggle','numbersBack','numbersFilter','numbersDurationFilter',
                 'numbersList','numberExamples','numberAllMentions','numberAllMentionsList',
                 'numbersDirectory','numbersDetail','numberPdf','numberPrint',
                 'numbersStatus','numbersMethod','numbersCount','numberTitle','numberSummary',
                 'numbersTermsDetails','numbersTermsList']){
  assert.equal(html.split('id="'+id+'"').length-1,1,'UI element '+id+' must be unique');
}
let prev=-1, links=0;
for(const entry of numbers.entries){
  assert.ok(Number.isInteger(entry.value)&&entry.value>=0&&entry.value<=9999);
  assert.ok(entry.value>prev,'Ascending numeric order');
  prev=entry.value;
  assert.equal(entry.label,String(entry.value));
  assert.ok(entry.summary.length>40);
  assert.ok(entry.title.length>4);
  assert.ok(entry.durationCount<=entry.references.length);
  const locators=new Set();
  for(const ref of entry.references){
    const p=psalms.get(ref.recordId);
    assert.ok(p,'Psaume existant '+ref.recordId);
    assert.equal(ref.archangel,p.archangel);
    assert.equal(ref.psalm,p.number);
    assert.ok(p.verses.some(v=>v.number===ref.verse));
    const key=ref.recordId+':'+ref.verse;
    assert.ok(!locators.has(key),'Pas de doublon dans le même verset');
    locators.add(key); links++;
  }
  assert.ok(entry.examples.every(ex=>locators.has(ex.recordId+':'+ex.verse)));
}
assert.ok(links>100);
assert.ok(numbers.numberTerms.every(ref=>{
  const p=psalms.get(ref.recordId);
  return p&&p.archangel===ref.archangel&&p.number===ref.psalm&&
    p.verses.some(v=>v.number===ref.verse);
}), 'Termes généraux sourcés');
const gabriel21=numbers.entries.find(e=>e.value===21);
assert.ok(gabriel21.examples.some(ref=>ref.recordId==='book-02-psalm-017'&&ref.verse===6),
  'Gabriel : méthode de 21 jours');
assert.ok(gabriel21.examples.some(ref=>ref.recordId==='book-02-psalm-017'&&ref.verse===7),
  'Gabriel : deuxième phase des 21 jours');
class Element {
  constructor(){
    this.children=[];this.hidden=false;this.textContent='';
    this.events={};this.attributes={};this.open=false;this.checked=false;
    this.childElementCount=0;this.value='';this.focused=false;
    this.className='';this.type='';this.title='';
    const names=new Set();
    this.classList={add:x=>names.add(x),remove:x=>names.delete(x),
      contains:x=>names.has(x)};
  }
  append(...args){this.children.push(...args);this.childElementCount=this.children.length;}
  replaceChildren(...args){this.children=args;this.childElementCount=this.children.length;}
  addEventListener(event,cb){this.events[event]=cb;}
  setAttribute(key,val){this.attributes[key]=val;}
  focus(){this.focused=true;}
  click(){return (this.events.click||this.onclick)?.();}
}
const nodes=new Map(), get=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
get('numbersLibrary').hidden=true;
const names=new Set(), exported=[];
const win={scrollY:0,scrollTo({top}){this.scrollY=top;}};
const doc={
  getElementById:get,createElement:()=>new Element(),
  body:{classList:{add:x=>names.add(x),remove:x=>names.delete(x)}}
};
const context={
  document:doc,window:win,console,
  BiblawPDF:{download:r=>exported.push(r)},
  fetch:async url=>{
    assert.ok(url.includes('numbers-public.json'));
    return {ok:true,json:async()=>numbers};
  }
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-numbers.js'),context,{timeout:10000});
let opened;
context.BiblawNumbers.setOpenPsalm(ref=>{opened=ref;});
context.BiblawNumbers.setCorpusLoading(async()=>true);
context.BiblawNumbers.setRecords(corpus.records);
await context.BiblawNumbers.open();
assert.equal(get('numbersLibrary').hidden,false);
assert.ok(names.has('view-numbers'));
assert.equal(get('numbersList').children.length,numbers.entries.length);
get('numbersTermsDetails').open=true;
get('numbersTermsDetails').ontoggle();
assert.equal(get('numbersTermsList').children.length,numbers.numberTerms.length);
get('numbersFilter').value='21';
get('numbersFilter').events.input();
assert.equal(get('numbersList').children.length,1,'Filtre des nombres');
assert.equal(get('numbersList').children[0].children[0].children[0].textContent,'21',
  'Le chiffre est visible directement sur le bouton cliquable');
get('numbersList').children[0].click();
assert.equal(get('numbersDetail').hidden,false);
assert.equal(get('numberTitle').textContent,'Nombre 21');
assert.ok(get('numberExamples').children.length);
const link=get('numberExamples').children[0].children[1];
win.scrollY=520;
await link.click();
assert.ok(opened.recordId&&opened.verses.length===1);
win.scrollY=0;
context.BiblawNumbers.restoreAfterPsalm();
assert.equal(win.scrollY,520);
assert.equal(link.focused,true);
get('numberAllMentions').open=true;
get('numberAllMentions').ontoggle();
assert.equal(get('numberAllMentionsList').children.length,
  numbers.entries.find(e=>e.value===21).references.length);
get('numberPdf').click();
assert.equal(exported.length,1);
assert.ok(exported[0].text.includes('Toutes les références'));
get('numbersBack').click();
assert.equal(get('numbersDirectory').hidden,false);
get('numbersDurationFilter').checked=true;
get('numbersDurationFilter').events.change();
assert.ok(get('numbersList').children.length>0);
get('numbersBack').click();
assert.equal(get('numbersLibrary').hidden,true);
assert.ok(!names.has('view-numbers'));
console.log('Biblaw NUMBERS PASS:',numbers.entries.length,'nombres /',links,
  'références / ouverture des versets, retour, PDF, filtre.');
