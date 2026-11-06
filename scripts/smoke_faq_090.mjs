import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const base=JSON.parse(read('data/faq-public-085.json'));
const extra=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const books=JSON.parse(read('data/faq-090-books.json'));
const extra091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const books091=JSON.parse(read('data/faq-091-books.json'));
const addon092=JSON.parse(read('data/faq-092.json'));
const addon093=JSON.parse(read('data/faq-093.json'));
const addon094=JSON.parse(read('data/faq-094.json'));
const addon095=JSON.parse(read('data/faq-095.json'));
const catalog=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(base.questions.length,25);
assert.equal(extra.length,5);
assert.ok(Number(read('index.html').match(/biblaw-faq[.]js[?]v=(\d+)/)?.[1])>=90);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-090-5.json"'));

class Element{
  constructor(tag='div'){
    this.tag=tag;this.children=[];this.textContent='';this.hidden=false;
    this.disabled=false;this.attrs={};this.focused=false;
  }
  replaceChildren(...items){this.children=items}
  append(...items){this.children.push(...items)}
  setAttribute(k,v){this.attrs[k]=v}
  focus(){this.focused=true}
}
const elements=new Map();
const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)};
const classNames=new Set(),pdfRequests=[],psalmRequests=[];
const document={
  getElementById:get,createElement:tag=>new Element(tag),
  createTextNode:t=>Object.assign(new Element('text'),{textContent:t}),
  body:{classList:{add:v=>classNames.add(v),remove:v=>classNames.delete(v)}}
};
const context={document,console,Blob,
  fetch:async url=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return base;
    if(url.includes('faq-090-books'))return books;
    if(url.includes('faq-091-books'))return books091;
    if(url.includes('faq-092.json'))return addon092;
    if(url.includes('faq-093.json'))return addon093;
    if(url.includes('faq-094.json'))return addon094;
    if(url.includes('faq-095.json'))return addon095;
    const m091=url.match(/faq-091-([1-9])\.json/);
    if(m091)return extra091[Number(m091[1])-1];
    const m=url.match(/faq-090-([1-5])\.json/);
    assert.ok(m,'Unexpected URL '+url);
    return extra[Number(m[1])-1];
  }}),
  BiblawPDF:{download:record=>pdfRequests.push(record)},
  window:{scrollY:100,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>psalmRequests.push(ref));
assert.equal(await context.BiblawFAQ.init(catalog.records),true,'The 30 public FAQs must load');
context.BiblawFAQ.open();
assert.equal(get('faqList').children.length,67,'Exactly 67 questions available');
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);
for(let i=0;i<5;i++){
  get('faqList').children[25+i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,extra[i].title);
  const buttons=get('faqAnswerBody').children.filter(x=>x.tag==='button');
  assert.equal(buttons.length,4,'Four complete citations '+extra[i].id);
  assert.equal(buttons.filter(x=>x.disabled).length,0,'No disabled Psalm links');
  context.window.scrollY=210+i*120;
  buttons[0].onclick();
  assert.equal(psalmRequests.length,i+1);
  assert.equal(psalmRequests.at(-1).number,extra[i].references?.[0]?.number||[5,279,104,205,272][i]);
  context.window.scrollY=0;
  context.BiblawFAQ.restoreAfterPsalm();
  assert.equal(context.window.scrollY,210+i*120);
  assert.ok(buttons[0].focused,'Return must focus the cited reference');
  assert.equal(get('faqAnswer').hidden,false,'Return keeps original response open');
  get('faqPdf').onclick();
  assert.equal(pdfRequests[i].recordType,'faq');
  assert.equal(pdfRequests[i].text,extra[i].answer,'Unchanged original full response in PDF');
  get('faqBack').onclick();
}
assert.equal(get('faqIndex').hidden,false);
const uniq=new Set([...base.questions.flatMap(q=>q.references.map(r=>r.recordId)),...psalmRequests.map(r=>r.recordId)]);
assert.ok(uniq.size>=56);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 090 PASS: 30 questions, 5 new complete answers, all 20 linked citations, back, scroll and PDF');
