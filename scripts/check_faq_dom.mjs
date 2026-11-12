#!/usr/bin/env node
// Integration smoke for the real FAQ loader: 95 visible questions, 424 clickable citations,
// index -> answer -> canonical Psalm -> back, and FAQ PDF export.
import assert from 'node:assert/strict';
import {readFile, readdir} from 'node:fs/promises';
import {join, dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {runInNewContext} from 'node:vm';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const recordDir=join(root,'data/corpus/books');
const records=[];
for(const entry of await readdir(recordDir,{withFileTypes:true})){
  if(!entry.isDirectory()||!/^book-\d\d$/.test(entry.name))continue;
  for(const name of await readdir(join(recordDir,entry.name))){
    if(!/^psalm-\d{3}\.json$/.test(name))continue;
    records.push(JSON.parse(await readFile(join(recordDir,entry.name,name),'utf8')));
  }
}
assert.equal(records.length,1158,'Unexpected canonical corpus count');
let printed=0, opened=0, exported=0;
function elt(tag='div'){
  const node={
    tagName:tag.toLowerCase(),textContent:'',className:'',hidden:false,disabled:false,value:'',
    title:'',type:'',onclick:null,children:[],attrs:{},classSet:new Set(),
    replaceChildren(...x){this.children=x;},
    append(...x){this.children.push(...x);},
    setAttribute(k,v){this.attrs[k]=String(v);},
    focus(){},addEventListener(){}, 
  };
  node.classList={add:k=>node.classSet.add(k),remove:k=>node.classSet.delete(k),
    contains:k=>node.classSet.has(k)};
  return node;
}
const needed=['faqStatus','faqList','faqIndex','faqAnswer','faqAnswerTitle',
  'faqAnswerBody','faqClose','faqPdf','faqPrint','faqLibrary','faqToggle',
  'faqSearch','faqSearchStatus'];
const nodes=Object.fromEntries(needed.map(k=>[k,elt()]));
nodes.faqLibrary.hidden=true;
nodes.faqAnswer.hidden=true;
const document={
  body:elt('body'),
  getElementById(id){assert.ok(nodes[id],'Unknown DOM node '+id);return nodes[id];},
  createElement:elt,
  createTextNode(text){const node=elt('#text');node.textContent=text;return node;}
};
const window={scrollY:0,scrollTo(){},print(){printed++;}};
const BiblawPDF={download(o){assert.equal(o.recordType,'faq');assert.ok(o.id&&o.title&&o.text);exported++;}};
const fetch=async url=>{
  const relative=String(url).split('?')[0];
  assert.match(relative,/^data\/faq-[\w-]+\.json$/);
  const value=JSON.parse(await readFile(join(root,relative),'utf8'));
  return {ok:true,json:async()=>value};
};
const ctx={document,window,fetch,BiblawPDF,console,Map,Set,Number,String,
  Boolean,Array,Error,JSON};
ctx.globalThis=ctx;
const source=await readFile(join(root,'js/biblaw-faq.js'),'utf8');
runInNewContext(source,ctx,{filename:'js/biblaw-faq.js'});
assert.ok(ctx.BiblawFAQ?.init,'FAQ API not registered');
ctx.BiblawFAQ.setOpenPsalm(ref=>{
  assert.ok(ref.recordId&&ref.archangel&&ref.verses.length>0);
  opened++;
});
assert.equal(await ctx.BiblawFAQ.init(records),true,'FAQ data load failed');
assert.equal(nodes.faqStatus.textContent,'','FAQ load produced an error');
assert.equal(nodes.faqList.children.length,95,'Wrong index count');
ctx.BiblawFAQ.open();
assert.equal(nodes.faqLibrary.hidden,false);
let questionCount=0,linkCount=0;
for(const item of nodes.faqList.children){
  assert.equal(item.tagName,'button','Unexpected question index element');
  assert.equal(typeof item.onclick,'function');
  item.onclick();
  assert.equal(nodes.faqIndex.hidden,true);
  assert.equal(nodes.faqAnswer.hidden,false);
  assert.ok(nodes.faqAnswerTitle.textContent,'Missing answer heading');
  const buttons=nodes.faqAnswerBody.children.filter(n=>n.tagName==='button');
  assert.ok(buttons.length>=3,'FAQ answer has fewer than three links');
  for(const btn of buttons){
    assert.equal(btn.disabled,false,'Unclickable citation in '+nodes.faqAnswerTitle.textContent);
    assert.equal(typeof btn.onclick,'function');
    assert.match(btn.title,/Lire Psaume/);
    btn.onclick();
    linkCount++;
  }
  questionCount++;
  nodes.faqClose.onclick();
  assert.equal(nodes.faqIndex.hidden,false);
  assert.equal(nodes.faqAnswer.hidden,true);
}
assert.equal(questionCount,95);
assert.equal(linkCount,424);
assert.equal(opened,424);
nodes.faqList.children.at(-1).onclick();
nodes.faqPdf.onclick();
assert.equal(exported,1,'PDF export did not trigger');
nodes.faqPrint.onclick();
assert.equal(printed,1,'Print button did not trigger');
nodes.faqClose.onclick(); // answer → question list
nodes.faqClose.onclick(); // question list → main search
assert.equal(nodes.faqLibrary.hidden,true);
console.log('BIBLAW FAQ UI smoke OK: '+questionCount+' answers opened, '+linkCount+
  ' active canonical citation buttons tested, PDF and print actions tested.');
