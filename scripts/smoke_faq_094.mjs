import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const base=JSON.parse(read('data/faq-public-085.json'));
const old090=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const old091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const old092=JSON.parse(read('data/faq-092.json'));
const old093=JSON.parse(read('data/faq-093.json'));
const newer=JSON.parse(read('data/faq-094.json'));
const addon095=JSON.parse(read('data/faq-095.json'));
const addon096=JSON.parse(read('data/faq-096.json'));
const addon097=JSON.parse(read('data/faq-097.json'));
const addon098=JSON.parse(read('data/faq-098.json'));
const addon099=JSON.parse(read('data/faq-099.json'));
const routing099=JSON.parse(read('data/faq-099-routing.json'));
const b090=JSON.parse(read('data/faq-090-books.json'));
const b091=JSON.parse(read('data/faq-091-books.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(base.questions.length,25);
assert.equal(newer.questions.length,6);
assert.equal(Object.keys(newer.verifiedPsalms).length,9);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-094.json"'));
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=94);
assert.ok(read('css/biblaw-light.css').includes('white-space:pre-wrap'));

class Element{
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
const downloads=[],opened=[],classes=new Set();
const document={
  getElementById:get,
  createElement:tag=>new Element(tag),
  createTextNode:value=>Object.assign(new Element('text'),{textContent:value}),
  body:{classList:{add:x=>classes.add(x),remove:x=>classes.delete(x)}}
};
const context={
  document,Blob,console,
  fetch:async url=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return base;
    if(url.includes('faq-090-books'))return b090;
    if(url.includes('faq-091-books'))return b091;
    if(url.includes('faq-092.json'))return old092;
    if(url.includes('faq-093.json'))return old093;
    if(url.includes('faq-094.json'))return newer;
    if(url.includes('faq-095.json'))return addon095;
    if(url.includes('faq-096.json'))return addon096;
    if(url.includes('faq-097.json'))return addon097;
    if(url.includes('faq-098.json'))return addon098;
    if(url.includes('faq-099.json'))return addon099;
    if(url.includes('faq-099-routing.json'))return routing099;
    let match=url.match(/faq-090-([1-5])\.json/);
    if(match)return old090[Number(match[1])-1];
    match=url.match(/faq-091-([1-9])\.json/);
    assert.ok(match,'Unknown FAQ data URL '+url);
    return old091[Number(match[1])-1];
  }}),
  BiblawPDF:{download:x=>downloads.push(x)},
  window:{scrollY:100,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>opened.push(ref));
assert.equal(await context.BiblawFAQ.init(corpus.records),true,'All 60 questions must load');
context.BiblawFAQ.open();
assert.ok(classes.has('view-faq'));
assert.equal(get('faqList').children.length,105);
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);
assert.equal(get('faqList').children[53].children[0].textContent,old093.questions[4].title);
let linkCount=0;
const unique=new Set();
for(let i=0;i<6;i++){
  const q=newer.questions[i];
  get('faqList').children[54+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,q.title);
  assert.equal(get('faqAnswer').hidden,false);
  const nodes=get('faqAnswerBody').children;
  assert.equal(nodes.map(x=>x.textContent).join(''),q.answer,'Full exact article text including paragraphs');
  const links=nodes.filter(x=>x.tag==='button');
  assert.equal(links.length,i===5?4:3,'All Psalm references linked');
  assert.equal(links.filter(x=>x.disabled).length,0);
  let scroll=140+i*90;
  for(const button of links){
    context.window.scrollY=scroll;
    button.onclick();
    const ref=opened.at(-1);
    const record=corpus.records.find(r=>r.id===ref.recordId);
    assert.ok(record&&record.recordType==='psalm');
    assert.ok(ref.verses.length&&ref.verses.every(n=>record.verses.some(v=>+v.number===n)));
    unique.add(ref.recordId);
    if(i===3&&button===links[0])
      assert.deepEqual(Array.from(ref.verses),[1,2,3,4,5,6,40,41,42]);
    if(i===5&&button===links[0])
      assert.deepEqual(Array.from(ref.verses),[24,25,26,27,38,39,40,41,42]);
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,scroll);
    assert.equal(button.focused,true);
    linkCount++;scroll+=5;
  }
  get('faqPdf').onclick();
  assert.equal(downloads.at(-1).recordType,'faq');
  assert.equal(downloads.at(-1).title,q.title);
  assert.equal(downloads.at(-1).text,q.answer);
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(linkCount,19);
assert.equal(unique.size,9);
assert.equal(downloads.length,6);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 094 PASS: 60 questions, six complete happiness answers, 19 correct Psalm links, six PDF exports, return navigation and paragraph integrity');
