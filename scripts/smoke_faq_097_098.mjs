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
const f097=JSON.parse(read('data/faq-097.json'));
const f098=JSON.parse(read('data/faq-098.json'));
const books090=JSON.parse(read('data/faq-090-books.json'));
const books091=JSON.parse(read('data/faq-091-books.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
assert.equal(f097.questions.length,8);
assert.equal(f098.questions.length,13);
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-097.json"'));
assert.ok(read('scripts/build_pages_site.py').includes('"data/faq-098.json"'));
assert.ok(read('index.html').includes('biblaw-faq.js?v=098'));

class Element {
  constructor(tag='div'){
    this.tag=tag;this.children=[];this.hidden=false;this.disabled=false;
    this.textContent='';this.focused=false;this.attrs={};
  }
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
    if(url.includes('faq-090-books'))return books090;
    if(url.includes('faq-091-books'))return books091;
    if(url.includes('faq-092.json'))return f092;
    if(url.includes('faq-093.json'))return f093;
    if(url.includes('faq-094.json'))return f094;
    if(url.includes('faq-095.json'))return f095;
    if(url.includes('faq-096.json'))return f096;
    if(url.includes('faq-097.json'))return f097;
    if(url.includes('faq-098.json'))return f098;
    let m=url.match(/faq-090-([1-5])\.json/);
    if(m)return f090[+m[1]-1];
    m=url.match(/faq-091-([1-9])\.json/);
    assert.ok(m,'Unexpected FAQ resource: '+url);
    return f091[+m[1]-1];
  }}),
  BiblawPDF:{download:x=>downloads.push(x)},
  window:{scrollY:110,scrollTo({top}){this.scrollY=top}}
};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
context.BiblawFAQ.setOpenPsalm(ref=>opened.push(ref));
assert.equal(await context.BiblawFAQ.init(corpus.records),true,'All 102 Q&A should load');
context.BiblawFAQ.open();
assert.ok(classes.has('view-faq'));
assert.equal(get('faqList').children.length,102);
assert.equal(get('faqList').children[0].children[0].textContent,base.questions[0].title);
assert.equal(get('faqList').children[80].children[0].textContent,f096.questions[13].title);
assert.equal(get('faqList').children[88].children[0].textContent,f097.questions[7].title);

const a=[3,3,3,4,3,3,4,4],b=[3,3,3,3,3,3,3,3,3,3,3,3,6];
const cases=[...f097.questions.map((q,i)=>({q,n:a[i],index:81+i,group:17,sub:i})),
             ...f098.questions.map((q,i)=>({q,n:b[i],index:89+i,group:18,sub:i}))];
let count=0;
const unique=new Set();
for(const {q,n,index,group,sub} of cases){
  get('faqList').children[index].onclick();
  assert.equal(get('faqAnswerTitle').textContent,q.title);
  assert.equal(get('faqAnswer').hidden,false);
  const nodes=get('faqAnswerBody').children;
  const plain=q.answer.replace(/\*\*([^*\n]+)\*\*/g,'$1');
  assert.equal(nodes.map(x=>x.textContent).join(''),plain,'No author words removed or reordered');
  const links=nodes.filter(x=>x.tag==='button');
  assert.equal(links.length,n);
  assert.equal(links.filter(x=>x.disabled).length,0);
  if(group===18&&sub===12){
    const headings=nodes.filter(x=>x.tag==='strong');
    assert.equal(headings.length,3);
    assert.deepEqual(headings.map(x=>x.textContent),[
      'Les repas peuvent devenir un exercice de gratitude et de conscience.',
      "La marche peut devenir un exercice d'attention et de présence.",
      'La parole peut devenir un exercice de vérité et de maîtrise intérieure.'
    ]);
    assert.ok(plain.includes('La parole peut devenir un exercice de vérité'));
  }
  let scroll=1000+index*60;
  for(let j=0;j<links.length;j++){
    const button=links[j];
    context.window.scrollY=scroll;
    button.onclick();
    const ref=opened.at(-1);
    const record=corpus.records.find(r=>r.id===ref.recordId);
    assert.ok(record&&record.recordType==='psalm');
    assert.ok(ref.verses.length>0&&ref.verses.every(v=>record.verses.some(x=>+x.number===v)));
    unique.add(ref.recordId);
    if(group===17&&sub===1&&j===1)
      assert.deepEqual(Array.from(ref.verses),[
        ...Array.from({length:13},(_,i)=>i+1),...Array.from({length:9},(_,i)=>i+22)
      ]);
    if(group===18&&sub===12&&j===4){
      assert.equal(ref.archangel,'michael','Michael and Gabriel psalm 165 must not be confused');
      assert.equal(ref.recordId,'book-25-psalm-165');
    }
    context.window.scrollY=0;
    context.BiblawFAQ.restoreAfterPsalm();
    assert.equal(context.window.scrollY,scroll);
    assert.equal(button.focused,true);
    assert.equal(get('faqAnswer').hidden,false);
    scroll+=5;count++;
  }
  get('faqPdf').onclick();
  assert.equal(downloads.at(-1).recordType,'faq');
  assert.equal(downloads.at(-1).title,q.title);
  assert.equal(downloads.at(-1).text,plain);
  get('faqBack').onclick();
  assert.equal(get('faqIndex').hidden,false);
}
assert.equal(count,69);
assert.equal(unique.size,42);
assert.equal(downloads.length,21);
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);
console.log('FAQ 097+098 PASS: 102 Q&A, 21 original articles, 69 verified links, 42 sources, proper bold subheadings, 21 PDFs and return navigation');
