import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const base=JSON.parse(read('data/faq-public-085.json'));
const old=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const b090=JSON.parse(read('data/faq-090-books.json'));
const next=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const b091=JSON.parse(read('data/faq-091-books.json'));
const addon092=JSON.parse(read('data/faq-092.json'));
const addon093=JSON.parse(read('data/faq-093.json'));
const addon094=JSON.parse(read('data/faq-094.json'));
const addon095=JSON.parse(read('data/faq-095.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(base.questions.length,25);
assert.equal(next.length,9);
assert.equal(Object.keys(b091.verifiedPsalms).length,24);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-091-9.json"'));
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=91);
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
const pdf=[],sourceCalls=[],classNames=new Set();
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
    if(url.includes('faq-090-books'))return b090;
    if(url.includes('faq-091-books'))return b091;
    if(url.includes('faq-092.json'))return addon092;
    if(url.includes('faq-093.json'))return addon093;
    if(url.includes('faq-094.json'))return addon094;
    if(url.includes('faq-095.json'))return addon095;
    let m=url.match(/faq-090-([1-5])\.json/);
    if(m)return old[+m[1]-1];
    m=url.match(/faq-091-([1-9])\.json/);
    assert.ok(m,'Unexpected FAQ resource '+url);
    return next[+m[1]-1];
  }}),
  BiblawPDF:{download:x=>pdf.push(x)},
  window:{scrollY:40,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>sourceCalls.push(ref));
assert.equal(await context.BiblawFAQ.init(corpus.records),true,'39-question FAQ must load');
context.BiblawFAQ.open();
assert.ok(classNames.has('view-faq'));
assert.equal(get('faqList').children.length,67);
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);
let linkCount=0,uniquePsalms=new Set();
for(let i=0;i<9;i++){
  get('faqList').children[30+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,next[i].title);
  assert.equal(get('faqAnswer').hidden,false);
  const links=get('faqAnswerBody').children.filter(x=>x.tag==='button');
  const expected=i===0?3:4;
  assert.equal(links.length,expected,'All citation references '+(i+1));
  assert.equal(links.filter(x=>x.disabled).length,0,'Every Psalm source is valid');
  let pos=180+i*90;
  for(const link of links){
    context.window.scrollY=pos;
    link.onclick();
    const ref=sourceCalls.at(-1);
    uniquePsalms.add(ref.recordId);
    const record=corpus.records.find(x=>x.id===ref.recordId);
    assert.ok(record&&record.recordType==='psalm');
    assert.ok(ref.verses.length>0);
    assert.ok(ref.verses.every(v=>record.verses.some(y=>+y.number===v)));
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,pos);
    assert.equal(link.focused,true);
    assert.equal(get('faqAnswer').hidden,false);
    linkCount++;
    pos+=3;
  }
  get('faqPdf').onclick();
  assert.equal(pdf.at(-1).recordType,'faq');
  assert.equal(pdf.at(-1).title,next[i].title);
  assert.equal(pdf.at(-1).text,next[i].answer,'PDF uses exact source answer');
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(linkCount,35);
assert.equal(uniquePsalms.size,24);
assert.equal(pdf.length,9);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 091 PASS: 39 questions, 35 verified links across 24 Psalms, nine complete PDFs, scroll/return retained');
