import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const base=JSON.parse(read('data/faq-public-085.json'));
const f090=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const f091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const f092=JSON.parse(read('data/faq-092.json'));
const f093=JSON.parse(read('data/faq-093.json'));
const f094=JSON.parse(read('data/faq-094.json'));
const f095=JSON.parse(read('data/faq-095.json'));
const f096=JSON.parse(read('data/faq-096.json'));
const addon097=JSON.parse(read('data/faq-097.json'));
const addon098=JSON.parse(read('data/faq-098.json'));
const addon099=JSON.parse(read('data/faq-099.json'));
const routing099=JSON.parse(read('data/faq-099-routing.json'));
const books090=JSON.parse(read('data/faq-090-books.json'));
const books091=JSON.parse(read('data/faq-091-books.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(base.questions.length,25);
assert.equal(f096.questions.length,14);
assert.equal(Object.keys(f096.verifiedPsalms).length,28);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-096.json"'));
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=96);
assert.ok(read('css/biblaw-light.css').includes('white-space:pre-wrap'));

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
const pdf=[],opened=[],classes=new Set();
const document={
  getElementById:get,
  createElement:tag=>new Element(tag),
  createTextNode:t=>Object.assign(new Element('text'),{textContent:t}),
  body:{classList:{add:x=>classes.add(x),remove:x=>classes.delete(x)}}
};
const context={
  document,Blob,console,
  fetch:async url=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return base;
    if(url.includes('faq-090-books'))return books090;
    if(url.includes('faq-091-books'))return books091;
    if(url.includes('faq-092.json'))return f092;
    if(url.includes('faq-093.json'))return f093;
    if(url.includes('faq-094.json'))return f094;
    if(url.includes('faq-095.json'))return f095;
    if(url.includes('faq-096.json'))return f096;
    if(url.includes('faq-097.json'))return addon097;
    if(url.includes('faq-098.json'))return addon098;
    if(url.includes('faq-099.json'))return addon099;
    if(url.includes('faq-099-routing.json'))return routing099;
    let m=url.match(/faq-090-([1-5])\.json/);
    if(m)return f090[+m[1]-1];
    m=url.match(/faq-091-([1-9])\.json/);
    assert.ok(m,'Unexpected FAQ resource: '+url);
    return f091[+m[1]-1];
  }}),
  BiblawPDF:{download:request=>pdf.push(request)},
  window:{scrollY:70,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('scripts/fixtures/faq-loader-before-100.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>opened.push(ref));
assert.equal(await context.BiblawFAQ.init(corpus.records),true,'All 81 questions loaded');
context.BiblawFAQ.open();
assert.ok(classes.has('view-faq'));
assert.equal(get('faqList').children.length,105);
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);
assert.equal(get('faqList').children[66].children[0].textContent,f095.questions[6].title);
const expected=[4,4,4,4,4,4,4,4,7,6,4,4,6,5];
let links=0;const unique=new Set();
for(let i=0;i<14;i++){
  const q=f096.questions[i];
  get('faqList').children[67+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,q.title);
  assert.equal(get('faqAnswer').hidden,false);
  const nodes=get('faqAnswerBody').children;
  assert.equal(nodes.map(x=>x.textContent).join(''),q.answer,'No changes to article words or paragraphs');
  const buttons=nodes.filter(x=>x.tag==='button');
  assert.equal(buttons.length,expected[i],'Each citation is clickable');
  assert.equal(buttons.filter(x=>x.disabled).length,0,'No invalid references');
  let scroll=240+i*66;
  for(let j=0;j<buttons.length;j++){
    const b=buttons[j];
    context.window.scrollY=scroll;
    b.onclick();
    const ref=opened.at(-1);
    const source=corpus.records.find(x=>x.id===ref.recordId);
    assert.ok(source&&source.recordType==='psalm');
    assert.ok(ref.verses.length>0);
    assert.ok(ref.verses.every(n=>source.verses.some(v=>+v.number===n)));
    unique.add(ref.recordId);
    if(i===0&&j===1)
      assert.deepEqual(Array.from(ref.verses),[...Array.from({length:14},(_,k)=>k+1),...Array.from({length:14},(_,k)=>k+22)]);
    if(i===7&&j===0)
      assert.deepEqual(Array.from(ref.verses),[4,5,6,7,8,9,10,11]);
    if(i===13&&j===4)
      assert.deepEqual(Array.from(ref.verses),[8,9,10,11,12,13,14,15]);
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,scroll);
    assert.equal(b.focused,true);
    assert.equal(get('faqAnswer').hidden,false);
    links++;scroll+=5;
  }
  get('faqPdf').onclick();
  assert.equal(pdf.at(-1).recordType,'faq');
  assert.equal(pdf.at(-1).title,q.title);
  assert.equal(pdf.at(-1).text,q.answer,'All words exported to PDF');
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(links,64);
assert.equal(unique.size,28);
assert.equal(pdf.length,14);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 096 PASS: 81 questions, 14 owner texts, 64 verified Psalm links, 28 canonical sources, PDF and return navigation');
