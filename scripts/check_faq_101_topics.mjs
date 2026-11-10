#!/usr/bin/env node
// 101: the public thematic FAQ must not fetch 105 articles before opening one.
import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import {join,dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {runInNewContext} from 'node:vm';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=async path=>JSON.parse(await readFile(join(root,path),'utf8'));
const index=await read('data/faq-101-index.json');
assert.equal(index.version,1);
assert.equal(index.questions.length,95);
assert.equal(index.topics.reduce((sum,t)=>sum+t.count,0),95);
assert.equal(new Set(index.questions.map(q=>q.id)).size,95);
assert.ok(index.topics.length>=10);

const records=[];
for(const dir of await readdir(join(root,'data/corpus/books'),{withFileTypes:true})){
  if(!dir.isDirectory()||!/^book-\d\d$/.test(dir.name))continue;
  const folder=join(root,'data/corpus/books',dir.name);
  for(const name of await readdir(folder)){
    if(/^psalm-\d{3}\.json$/.test(name))
      records.push(JSON.parse(await readFile(join(folder,name),'utf8')));
  }
}
assert.equal(records.length,1158);

function node(tag='div'){
  return {tagName:tag.toLowerCase(),textContent:'',hidden:false,value:'',type:'',
    children:[],onclick:null,attrs:{},className:'',
    replaceChildren(...children){this.children=children;},
    append(...children){this.children.push(...children);},
    setAttribute(key,val){this.attrs[key]=val;},focus(){},
    classList:{add(){},remove(){}}};
}
const ids=['faqStatus','faqList','faqIndex','faqAnswer','faqAnswerTitle','faqAnswerBody',
  'faqClose','faqPdf','faqPrint','faqLibrary','faqToggle','faqSearch',
  'faqSearchStatus','faqTopicButtons','faqTopics','faqSelectedTheme'];
const elements=Object.fromEntries(ids.map(id=>[id,node()]));
elements.faqLibrary.hidden=true;
let downloads=0;
const requests=[];
const document={
  body:node('body'),
  getElementById(id){assert.ok(elements[id], 'Missing FAQ DOM node: '+id);return elements[id];},
  createElement:node,
  createTextNode(text){return {...node('#text'),textContent:text};}
};
const fetch=async url=>{
  const path=String(url).split('?')[0];
  requests.push(path);
  assert.match(path,/^data\/faq-[\w-]+\.json$/);
  return {ok:true,json:()=>read(path)};
};
const ctx={document,fetch,window:{scrollY:0,scrollTo(){},print(){}},
  BiblawPDF:{download(){downloads++;}},console};
ctx.globalThis=ctx;
runInNewContext(await readFile(join(root,'js/biblaw-faq.js'),'utf8'),ctx);
ctx.BiblawFAQ.prime(records);
assert.equal(requests.length,0,'Homepage loaded an FAQ answer before opening the FAQ');
ctx.BiblawFAQ.open();
for(let i=0;i<100&&!elements.faqTopicButtons.children.length;i++)
  await new Promise(r=>setTimeout(r,5));
assert.deepEqual(requests,['data/faq-101-index.json'],
  'FAQ landing page downloaded content instead of only the thematic index');
assert.equal(elements.faqTopicButtons.children.length,index.topics.length);
assert.equal(elements.faqList.children.length,0,
  'FAQ displayed a long list of 95 questions before a topic was selected');

let answers=0,links=0;
for(const topic of index.topics){
  elements.faqTopicButtons.children.find(b=>b.children[0].textContent===topic.label).onclick();
  assert.equal(elements.faqList.children.length,topic.count,'Wrong topic count: '+topic.label);
  const buttons=[...elements.faqList.children];
  for(const button of buttons){
    await button.onclick();
    assert.equal(elements.faqAnswer.hidden,false);
    assert.equal(elements.faqIndex.hidden,true);
    assert.equal(elements.faqAnswerTitle.textContent,
      button.children[0].textContent,'Article title changed');
    const citations=elements.faqAnswerBody.children.filter(x=>x.className==='faq-psalm-link');
    assert.ok(citations.length>=3,'Missing citations: '+elements.faqAnswerTitle.textContent);
    for(const b of citations){
      assert.equal(b.disabled,false,'A cited psalm is unresolved');
      assert.equal(typeof b.onclick,'function');
    }
    answers++;
    links+=citations.length;
    elements.faqClose.onclick();
  }
  elements.faqClose.onclick();
}
assert.equal(answers,95);
assert.equal(links,424,'Deduplicated answers did not preserve every citation');
elements.faqSearch.value='Ai-je une mission particulière ?';
elements.faqSearch.oninput();
assert.equal(elements.faqList.children.length,1,'An old question alias is not searchable');
await elements.faqList.children[0].onclick();
assert.match(elements.faqAnswerTitle.textContent,/Avons-nous une mission particulière/);
assert.equal(elements.faqAnswerBody.children.filter(x=>x.className==='faq-psalm-link').length,7);
elements.faqPdf.onclick();
assert.equal(downloads,1);
elements.faqClose.onclick();
elements.faqSearch.value='Que peut nous apprendre la science sur la mort et l’au-delà ?';
elements.faqSearch.oninput();
assert.match(elements.faqSearchStatus.textContent,/Aucune réponse fondée/);
assert.equal(elements.faqList.children.length,0);
console.log('BIBLAW FAQ 101 PASS: 11 thèmes, 95 réponses en lecture différée, 424 références, aucun chargement des réponses à l’ouverture, anciennes formulations et PDF.');
