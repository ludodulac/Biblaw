import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const base=JSON.parse(read('data/faq-public-085.json'));
const prev090=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const prev091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const books090=JSON.parse(read('data/faq-090-books.json'));
const books091=JSON.parse(read('data/faq-091-books.json'));
const addon=JSON.parse(read('data/faq-092.json'));
const addon093=JSON.parse(read('data/faq-093.json'));
const addon094=JSON.parse(read('data/faq-094.json'));
const addon095=JSON.parse(read('data/faq-095.json'));
const addon096=JSON.parse(read('data/faq-096.json'));
const addon097=JSON.parse(read('data/faq-097.json'));
const addon098=JSON.parse(read('data/faq-098.json'));
const addon099=JSON.parse(read('data/faq-099.json'));
const routing099=JSON.parse(read('data/faq-099-routing.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(base.questions.length,25);
assert.equal(addon.questions.length,10);
assert.equal(Object.keys(addon.verifiedPsalms).length,16);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-092.json"'));
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=92);

class Element {
  constructor(tag='div'){this.tag=tag;this.children=[];this.hidden=false;this.disabled=false;this.textContent='';this.attrs={};this.focused=false;}
  replaceChildren(...items){this.children=items;}
  append(...items){this.children.push(...items);}
  setAttribute(k,v){this.attrs[k]=v;}
  focus(){this.focused=true;}
}
const elements=new Map(),get=id=>{
  if(!elements.has(id))elements.set(id,new Element());
  return elements.get(id);
};
const pdf=[],psalmCalls=[],classNames=new Set();
const document={
  getElementById:get,
  createElement:tag=>new Element(tag),
  createTextNode:text=>Object.assign(new Element('text'),{textContent:text}),
  body:{classList:{add:x=>classNames.add(x),remove:x=>classNames.delete(x)}}
};
const context={
  document,Blob,console,
  fetch:async url=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return base;
    if(url.includes('faq-090-books'))return books090;
    if(url.includes('faq-091-books'))return books091;
    if(url.includes('faq-092.json'))return addon;
    if(url.includes('faq-093.json'))return addon093;
    if(url.includes('faq-094.json'))return addon094;
    if(url.includes('faq-095.json'))return addon095;
    if(url.includes('faq-096.json'))return addon096;
    if(url.includes('faq-097.json'))return addon097;
    if(url.includes('faq-098.json'))return addon098;
    if(url.includes('faq-099.json'))return addon099;
    if(url.includes('faq-099-routing.json'))return routing099;
    let match=url.match(/faq-090-([1-5])\.json/);
    if(match)return prev090[Number(match[1])-1];
    match=url.match(/faq-091-([1-9])\.json/);
    assert.ok(match,'Unexpected FAQ resource '+url);
    return prev091[Number(match[1])-1];
  }}),
  BiblawPDF:{download:x=>pdf.push(x)},
  window:{scrollY:40,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>psalmCalls.push(ref));
assert.equal(await context.BiblawFAQ.init(corpus.records),true,'49-question FAQ must load');
context.BiblawFAQ.open();
assert.ok(classNames.has('view-faq'));
assert.equal(get('faqList').children.length,105);
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);

let count=0;
const unique=new Set();
for(let i=0;i<10;i++){
  get('faqList').children[39+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,addon.questions[i].title);
  assert.equal(get('faqAnswer').hidden,false);
  const links=get('faqAnswerBody').children.filter(x=>x.tag==='button');
  assert.equal(links.length,3,'All citations in question '+(i+1));
  assert.equal(links.filter(x=>x.disabled).length,0);
  let scroll=180+i*90;
  for(const link of links){
    context.window.scrollY=scroll;
    link.onclick();
    const ref=psalmCalls.at(-1);
    unique.add(ref.recordId);
    const source=corpus.records.find(x=>x.id===ref.recordId);
    assert.ok(source&&source.recordType==='psalm');
    assert.ok(ref.verses.length);
    assert.ok(ref.verses.every(v=>source.verses.some(y=>+y.number===v)));
    if(i===7&&link===links[0])
      assert.deepEqual(Array.from(ref.verses),[6,7,8,9,19,20,21,22,23]);
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,scroll);
    assert.equal(link.focused,true);
    assert.equal(get('faqAnswer').hidden,false);
    count++;scroll+=3;
  }
  get('faqPdf').onclick();
  assert.equal(pdf.at(-1).recordType,'faq');
  assert.equal(pdf.at(-1).title,addon.questions[i].title);
  assert.equal(pdf.at(-1).text,addon.questions[i].answer);
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(count,30);
assert.equal(unique.size,16);
assert.equal(pdf.length,10);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 092 PASS: 49 questions, 30 citations linked to 16 Psalms, all ten PDFs and return positions');
