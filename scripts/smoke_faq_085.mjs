import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const faq=JSON.parse(read('data/faq-public-085.json'));
const addon=Array.from({length:5},(_,i)=>JSON.parse(read('data/faq-090-'+(i+1)+'.json')));
const books=JSON.parse(read('data/faq-090-books.json'));
const addon091=Array.from({length:9},(_,i)=>JSON.parse(read('data/faq-091-'+(i+1)+'.json')));
const books091=JSON.parse(read('data/faq-091-books.json'));
const bundle=JSON.parse(read('data/browser-search-catalog.json'));
const html=read('index.html'),js=read('js/biblaw.js');
assert.equal(faq.questions.length,25);
assert.ok(html.includes('id="faqToggle"')&&html.includes('id="faqLibrary"')&&
  html.includes('id="faqReturnFromPsalm"')&&html.includes('id="faqAnswerBody"'));
assert.ok(js.includes("BiblawFAQ.setOpenPsalm(ref=>open(ref.recordId,ref.verses))"));
assert.ok(js.includes("first?.scrollIntoView")&&js.includes("faq-cited-verse"));
assert.ok(js.includes("BiblawFAQ.restoreAfterPsalm()"));
assert.ok(js.includes("rankExactWordPairs(query,query2)"));
assert.ok(js.includes("publishedNotes.size!==11"));

class Element {
  constructor(tag='div'){
    this.tag=tag;this.children=[];this.hidden=false;this.textContent='';
    this.disabled=false;this.attributes={};this.onclick=null;this.focused=false;
  }
  replaceChildren(...items){this.children=items;}
  append(...items){this.children.push(...items);}
  setAttribute(name,value){this.attributes[name]=value;}
  focus(){this.focused=true;}
}
const elements=new Map();
const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id);};
const classes=new Set(),printed=[];
const document={
  getElementById:get,createElement:tag=>new Element(tag),
  createTextNode:text=>new Element('text'),
  body:{classList:{add:k=>classes.add(k),remove:k=>classes.delete(k)}}
};
const context={document,console,Blob,fetch:async(url)=>({ok:true,json:async()=>{
    if(url.includes('faq-public-085'))return faq;
    if(url.includes('faq-090-books'))return books;
    if(url.includes('faq-091-books'))return books091;
    const next=url.match(/faq-091-([1-9])[.]json/);
    if(next)return addon091[Number(next[1])-1];
    const found=url.match(/faq-090-([1-5])[.]json/);
    assert.ok(found,'Unexpected FAQ data URL: '+url);
    return addon[Number(found[1])-1];
  }}),
  BiblawPDF:{download:record=>printed.push(record)},
  window:{scrollY:187,scrollTo:({top})=>{context.window.scrollY=top;}}};
context.globalThis=context;
vm.runInNewContext(read('js/biblaw-faq.js'),context,{timeout:10000});
let opened=null;
context.BiblawFAQ.setOpenPsalm(ref=>{opened=ref;});
assert.equal(await context.BiblawFAQ.init(bundle.records),true);
context.BiblawFAQ.open();
assert.ok(classes.has('view-faq'));
assert.equal(get('faqList').children.length,39);
get('faqList').children[0].onclick();
assert.equal(get('faqAnswer').hidden,false);
assert.equal(get('faqIndex').hidden,true);
assert.equal(get('faqAnswerTitle').textContent,faq.questions[0].title);
const links=get('faqAnswerBody').children.filter(el=>el.tag==='button');
assert.equal(links.length,4);
assert.equal(links.filter(el=>el.disabled).length,0);
context.window.scrollY=293;
links[0].onclick();
assert.equal(opened.recordId,'book-41-psalm-277');
assert.deepEqual(Array.from(opened.verses),[2,6]);
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,293);
assert.equal(links[0].focused,true);
assert.equal(get('faqAnswer').hidden,false,'Answer must stay open after reading Psalm');
get('faqPdf').onclick();
assert.equal(printed.length,1);
assert.equal(printed[0].recordType,'faq');
assert.equal(printed[0].title,faq.questions[0].title);
assert.equal(printed[0].text,faq.questions[0].answer);
get('faqBack').onclick();
assert.equal(get('faqIndex').hidden,false);
get('faqList').children[7].onclick(); // fourth new question: suffering can have meaning
assert.equal(get('faqAnswerTitle').textContent,faq.questions[7].title);
const newLinks=get('faqAnswerBody').children.filter(el=>el.tag==='button');
assert.equal(newLinks.length,4);
assert.equal(newLinks.filter(el=>el.disabled).length,0);
context.window.scrollY=521;
newLinks[0].onclick();
assert.equal(opened.recordId,'book-42-psalm-287');
assert.deepEqual(Array.from(opened.verses),Array.from({length:14},(_,i)=>i+1));
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,521);
assert.equal(newLinks[0].focused,true);
assert.equal(get('faqAnswer').hidden,false);
get('faqPdf').onclick();
assert.equal(printed.length,2);
assert.equal(printed[1].text,faq.questions[7].answer);
get('faqBack').onclick();
assert.equal(get('faqIndex').hidden,false);
assert.equal(get('faqAnswer').hidden,true);
get('faqList').children[12].onclick(); // The new fifth question, on reincarnation.
assert.equal(get('faqAnswerTitle').textContent,faq.questions[12].title);
const deathLinks=get('faqAnswerBody').children.filter(el=>el.tag==='button');
assert.equal(deathLinks.length,4);
assert.equal(deathLinks.filter(el=>el.disabled).length,0);
context.window.scrollY=653;
deathLinks[0].onclick();
assert.equal(opened.recordId,'book-24-psalm-138');
assert.deepEqual(Array.from(opened.verses),[1,2,3,4,5,6,7,8,9]);
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,653);
assert.equal(deathLinks[0].focused,true);
assert.equal(get('faqAnswer').hidden,false);
get('faqPdf').onclick();
assert.equal(printed.length,3);
assert.equal(printed[2].text,faq.questions[12].answer);
assert.ok(printed[2].text.includes('\n\nCependant'), 'Preserve original paragraph breaks');
get('faqBack').onclick();
assert.equal(get('faqIndex').hidden,false);
assert.equal(get('faqAnswer').hidden,true);
// New purpose-of-life question and precise verse navigation.
get('faqList').children[13].onclick();
assert.equal(get('faqAnswerTitle').textContent,faq.questions[13].title);
const purposeLinks=get('faqAnswerBody').children.filter(el=>el.tag==='button');
assert.equal(purposeLinks.length,3);
assert.equal(purposeLinks.filter(el=>el.disabled).length,0);
context.window.scrollY=471;
purposeLinks[0].onclick();
assert.equal(opened.recordId,'book-19-psalm-124');
assert.deepEqual(Array.from(opened.verses),[1,2,3,4,5,6,7,8]);
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,471);
assert.equal(purposeLinks[0].focused,true);
assert.equal(get('faqAnswer').hidden,false);
get('faqPdf').onclick();
assert.equal(printed[3].text,faq.questions[13].answer);
get('faqBack').onclick();
// Last new question has a different archangel and can be exported separately.
get('faqList').children[18].onclick();
assert.equal(get('faqAnswerTitle').textContent,faq.questions[18].title);
const endLinks=get('faqAnswerBody').children.filter(el=>el.tag==='button');
assert.equal(endLinks.length,3);
assert.equal(endLinks.filter(el=>el.disabled).length,0);
context.window.scrollY=326;
endLinks[0].onclick();
assert.equal(opened.recordId,'book-29-psalm-200');
assert.deepEqual(Array.from(opened.verses),[1,2,3]);
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,326);
assert.equal(endLinks[0].focused,true);
assert.equal(get('faqAnswer').hidden,false);
get('faqPdf').onclick();
assert.equal(printed[4].recordType,'faq');
assert.equal(printed[4].text,faq.questions[18].answer);
get('faqBack').onclick();
assert.equal(get('faqIndex').hidden,false);
assert.equal(get('faqAnswer').hidden,true);
for(let i=19;i<25;i++){
  get('faqList').children[i].onclick();
  assert.equal(get('faqAnswerTitle').textContent,faq.questions[i].title);
  const cited=get('faqAnswerBody').children.filter(el=>el.tag==='button');
  assert.equal(cited.length,4);
  assert.equal(cited.filter(el=>el.disabled).length,0);
  get('faqBack').onclick();
}
get('faqList').children[24].onclick();
const natureLinks=get('faqAnswerBody').children.filter(el=>el.tag==='button');
context.window.scrollY=815;
natureLinks[0].onclick();
assert.equal(opened.recordId,'book-41-psalm-277');
assert.deepEqual(Array.from(opened.verses),[6,7,8,9,10,11,12,13,14,15]);
context.window.scrollY=0;
context.BiblawFAQ.restoreAfterPsalm();
assert.equal(context.window.scrollY,815);
assert.equal(natureLinks[0].focused,true);
assert.equal(get('faqAnswer').hidden,false);
get('faqPdf').onclick();
assert.equal(printed[5].text,faq.questions[24].answer);
get('faqBack').onclick();
context.BiblawFAQ.close();
assert.equal(get('faqLibrary').hidden,true);

const pdfContext={Blob,document:undefined};pdfContext.globalThis=pdfContext;
vm.runInNewContext(read('js/biblaw-pdf.js'),pdfContext,{timeout:10000});
const output=pdfContext.BiblawPDF.createPDF(printed[0]);
assert.ok(output.filename.endsWith('.pdf'));
assert.equal(output.blob.type,'application/pdf');
const pdfContent=Buffer.from(await output.blob.arrayBuffer()).toString('latin1');
assert.ok(pdfContent.startsWith('%PDF-1.4'));
assert.ok(pdfContent.includes('/Type /Page'));
assert.ok(output.pages>=1);
console.log('FAQ 089 PASS: twenty-five answers, linked verses, return positions, PDFs and previous tests');
