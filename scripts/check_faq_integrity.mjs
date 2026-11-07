#!/usr/bin/env node
// BIBLAW: protect the public FAQ loader against broken or unclickable Psalm references.
// This validates metadata and passage availability, not the doctrinal interpretation.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname, join, resolve} from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json = async path => JSON.parse(await readFile(join(root, path), 'utf8'));
const script = await readFile(join(root, 'js/biblaw-faq.js'), 'utf8');
const citation = /\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)/g;
const groups = [
  {name:'090', files:[1,2,3,4,5].map(n=>'data/faq-090-'+n+'.json'), book:'data/faq-090-books.json', expected:[4,4,4,4,4]},
  {name:'091', files:[1,2,3,4,5,6,7,8,9].map(n=>'data/faq-091-'+n+'.json'), book:'data/faq-091-books.json', expected:[3,4,4,4,4,4,4,4,4]},
  {name:'092', files:['data/faq-092.json'], expected:Array(10).fill(3)},
  {name:'093', files:['data/faq-093.json'], expected:Array(5).fill(3)},
  {name:'094', files:['data/faq-094.json'], expected:[3,3,3,3,3,4]},
  {name:'095', files:['data/faq-095.json'], expected:[3,3,3,3,4,4,5]},
  {name:'096', files:['data/faq-096.json'], expected:[4,4,4,4,4,4,4,4,7,6,4,4,6,5]},
  {name:'097', files:['data/faq-097.json'], expected:[3,3,3,4,3,3,4,4]},
  {name:'098', files:['data/faq-098.json'], expected:[3,5,4,4,5,5,4,5,5,5,5,6,18]}
];
assert.ok(script.includes('i===0?3:4'), 'Loader citation counts 091 have drifted');
for(const key of ['096','098']) {
  const group = groups.find(g=>g.name===key);
  assert.ok(script.includes('const expected'+key+'='+JSON.stringify(group.expected)+';'),
    'Loader citation counts '+key+' have drifted');
}
const passageCache = new Map();
async function checkPsalm(ref, owner) {
  assert.match(ref.recordId, /^book-\d{2}-psalm-\d{3}$/);
  if(!passageCache.has(ref.recordId)){
    const p='data/corpus/books/'+ref.recordId.slice(0,7)+'/'+ref.recordId.slice(8)+'.json';
    passageCache.set(ref.recordId, await json(p));
  }
  const psalm = passageCache.get(ref.recordId);
  assert.equal(psalm.id, ref.recordId, owner+' wrong psalm ID');
  assert.equal(psalm.recordType,'psalm', owner+' wrong record type');
  assert.equal(psalm.archangel,ref.archangel, owner+' wrong Archange');
  assert.equal(Number(psalm.number),ref.number, owner+' wrong psalm number');
  assert.ok(ref.verses.length>0, owner+' has no verse numbers');
  for(const v of ref.verses) {
    assert.ok(psalm.verses.some(x=>Number(x.number)===v),owner+' missing verse '+v+' in '+ref.recordId);
  }
}
function parse(match, books) {
  const number=Number(match[1]);
  const archangel=match[2].normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const book=books[archangel+':'+number];
  assert.ok(Number.isInteger(book), 'Psalm absent from verified book map: '+match[0]);
  const verses=[];
  const tail=match[3].replace(/(\d+)\s+à\s+(\d+)/g,(_,a,b)=>{
    const start=Number(a),end=Number(b);
    assert.ok(end>=start&&end-start<=100,'Invalid verse range: '+match[0]);
    for(let n=start;n<=end;n++)verses.push(n);
    return '';
  });
  for(const matchDigit of tail.matchAll(/\d+/g))verses.push(Number(matchDigit[0]));
  const unique=[...new Set(verses)].sort((a,b)=>a-b);
  assert.ok(unique.length>0,'No verses: '+match[0]);
  return {label:match[0],recordId:'book-'+String(book).padStart(2,'0')+
    '-psalm-'+String(number).padStart(3,'0'),archangel,number,verses:unique};
}
const ids=new Set();
let total=0;
let linked=0;
function register(q) {
  assert.ok(q.id&&q.title&&q.answer,'Missing FAQ fields');
  assert.ok(!ids.has(q.id),'Duplicate FAQ ID: '+q.id);
  assert.doesNotMatch(q.answer,/\(psaume[^)]*;\s*psaume[^)]*\)/i,
    'Multiple Psalms hidden in one unclickable citation: '+q.id);
  ids.add(q.id); total++;
  assert.doesNotMatch(q.answer,/sur le plan scientifique|pas une preuve scientifique|ne constitue pas une preuve scientifique|scientifiquement démontr[ée]/i,
    'Extraneous scientific qualification in '+q.id);
}
const base=await json('data/faq-public-085.json');
assert.equal(base.version,5);
assert.equal(base.questions.length,25);
for(const q of base.questions){
  register(q);
  assert.ok(Array.isArray(q.references),'Missing declared references in '+q.id);
  const citations=[...q.answer.matchAll(citation)];
  assert.equal(citations.length,q.references.length,'Citation count mismatch '+q.id);
  assert.equal(q.answer.split('(psaume ').length-1,citations.length,'Unparseable citation '+q.id);
  let cursor=0;
  for(let i=0;i<q.references.length;i++){
    const ref=q.references[i];
    assert.equal(ref.label,citations[i][0],'Citation mismatch or order in '+q.id);
    const at=q.answer.indexOf(ref.label,cursor);
    assert.ok(at>=cursor,'Unclickable citation '+q.id);
    cursor=at+ref.label.length;
    await checkPsalm(ref,q.id);
    linked++;
  }
}
for(const group of groups) {
  const docs=await Promise.all(group.files.map(json));
  const questions=docs.flatMap(d=>d.questions||[d]);
  assert.equal(questions.length,group.expected.length,'Wrong question count '+group.name);
  const bookMap=group.book?(await json(group.book)).verifiedPsalms:docs[0].verifiedPsalms;
  assert.ok(bookMap,'Missing book map '+group.name);
  for(let i=0;i<questions.length;i++){
    const q=questions[i];
    register(q);
    const citations=[...q.answer.matchAll(citation)];
    assert.equal(citations.length,group.expected[i],'Citation count mismatch '+q.id);
    assert.equal(q.answer.split('(psaume ').length-1,citations.length,'Unparseable citation '+q.id);
    for(const m of citations){
      const ref=parse(m,bookMap);
      await checkPsalm(ref,q.id);
      linked++;
    }
  }
}
assert.equal(total,102,'Wrong FAQ question total');
console.log('BIBLAW FAQ OK: '+total+' distinct answers, '+linked+
  ' clickable Psalm references, '+passageCache.size+' distinct canonical Psalm records.');
