import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const original=JSON.parse(read('data/faq-public-085.json'));
const part090=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const part091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const part092=JSON.parse(read('data/faq-092.json'));
const part093=JSON.parse(read('data/faq-093.json'));
const part094=JSON.parse(read('data/faq-094.json'));
const addon095=JSON.parse(read('data/faq-095.json'));
const addon096=JSON.parse(read('data/faq-096.json'));
const addon097=JSON.parse(read('data/faq-097.json'));
const addon098=JSON.parse(read('data/faq-098.json'));
const books090=JSON.parse(read('data/faq-090-books.json'));
const books091=JSON.parse(read('data/faq-091-books.json'));
const catalog=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(part093.questions.length,5);
assert.equal(Object.keys(part093.verifiedPsalms).length,6);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-093.json"'));
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=93);
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
  createTextNode:value=>Object.assign(new Element('text'),{textContent:value}),
  body:{classList:{add:x=>classes.add(x),remove:x=>classes.delete(x)}}
};
const context={
  document,Blob,console,
  fetch:async url=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return original;
    if(url.includes('faq-090-books'))return books090;
    if(url.includes('faq-091-books'))return books091;
    if(url.includes('faq-092.json'))return part092;
    if(url.includes('faq-093.json'))return part093;
    if(url.includes('faq-094.json'))return part094;
    if(url.includes('faq-095.json'))return addon095;
    if(url.includes('faq-096.json'))return addon096;
    if(url.includes('faq-097.json'))return addon097;
    if(url.includes('faq-098.json'))return addon098;
    let match=url.match(/faq-090-([1-5])\.json/);
    if(match)return part090[Number(match[1])-1];
    match=url.match(/faq-091-([1-9])\.json/);
    assert.ok(match, 'Unrecognized FAQ source '+url);
    return part091[Number(match[1])-1];
  }}),
  BiblawPDF:{download:r=>pdf.push(r)},
  window:{scrollY:100,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>opened.push(ref));
assert.equal(await context.BiblawFAQ.init(catalog.records),true);
context.BiblawFAQ.open();
assert.ok(classes.has('view-faq'));
assert.equal(get('faqList').children.length,102);
assert.equal(get('faqList').children[0].children[0].textContent,original.questions[0].title);
assert.equal(get('faqList').children[48].children[0].textContent,part092.questions[9].title);
let refs=0,unique=new Set();
for(let i=0;i<5;i++){
  const q=part093.questions[i];
  get('faqList').children[49+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,q.title);
  assert.equal(get('faqAnswer').hidden,false);
  const nodes=get('faqAnswerBody').children;
  // Recombine text nodes and link labels: not one word of the owner's answer may disappear.
  assert.equal(nodes.map(x=>x.textContent).join(''),q.answer);
  const links=nodes.filter(x=>x.tag==='button');
  assert.equal(links.length,3);
  assert.equal(links.filter(x=>x.disabled).length,0);
  let scroll=300+i*50;
  for(const button of links){
    context.window.scrollY=scroll;
    button.onclick();
    const ref=opened.at(-1);
    const record=catalog.records.find(x=>x.id===ref.recordId);
    unique.add(ref.recordId);
    assert.ok(record&&record.recordType==='psalm');
    assert.ok(ref.verses.length>0);
    assert.ok(ref.verses.every(v=>record.verses.some(x=>+x.number===v)));
    if(i===0&&button===links[1])assert.deepEqual(Array.from(ref.verses),[3,4,5,6,15]);
    if(i===2&&button===links[2])
      assert.deepEqual(Array.from(ref.verses),[...Array.from({length:11},(_,x)=>x+15),...Array.from({length:8},(_,x)=>x+32)]);
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,scroll);
    assert.equal(button.focused,true);
    refs++;scroll+=5;
  }
  get('faqPdf').onclick();
  assert.equal(pdf.at(-1).recordType,'faq');
  assert.equal(pdf.at(-1).title,q.title);
  assert.equal(pdf.at(-1).text,q.answer);
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(refs,15);
assert.equal(unique.size,6);
assert.equal(pdf.length,5);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 093 PASS: 54 Q&A, five complete answers, 15 linked citations, six Psalms, exact display/PDF text and return positions');
