#!/usr/bin/env node
// Mission 100 — a reversible editorial regrouping, not deletion.
// Validate the original 105 source answers independently of the UI and
// establish a byte-for-byte proof that all 424 linked citations survive.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const json=async p=>JSON.parse(await readFile(new URL('../'+p,import.meta.url),'utf8'));
const original=[];
original.push(...(await json('data/faq-public-085.json')).questions);
for(let n=1;n<=5;n++)original.push(await json('data/faq-090-'+n+'.json'));
for(let n=1;n<=9;n++)original.push(await json('data/faq-091-'+n+'.json'));
for(let n=92;n<=99;n++)original.push(...(await json('data/faq-'+n+'.json')).questions);
const byId=new Map(original.map(q=>[q.id,q]));
assert.equal(original.length,105);
assert.equal(byId.size,105);
const directives=await json('data/faq-100-merge.json');
assert.equal(directives.version,1);
assert.equal(directives.groups.length,10);
assert.equal(directives.originalArticles,105);
assert.equal(directives.visibleArticles,95);
assert.equal(directives.originalCitationCount,424);
assert.equal(directives.visibleCitationCount,424);
const countRefs=s=>(s.match(/\(psaume\s+\d+/g)||[]).length;
const originalRefs=original.reduce((n,q)=>n+countRefs(q.answer),0);
assert.equal(originalRefs,424);
const folded=new Set(),kept=new Set(),out=[],allVisible=[];
for(const d of directives.groups){
  assert.ok(Number.isInteger(d.number)&&d.number===out.length+1);
  const main=byId.get(d.keepId),extra=byId.get(d.foldId);
  assert.ok(main&&extra&&main!==extra);
  assert.ok(!kept.has(d.keepId)&&!folded.has(d.keepId));
  assert.ok(!kept.has(d.foldId)&&!folded.has(d.foldId));
  assert.match(d.heading,/^Approfondissement/);
  assert.doesNotMatch(d.heading,/\n|\*/);
  assert.ok(main.answer.startsWith('La Bible essénienne enseigne que'));
  assert.ok(extra.answer.startsWith('La Bible essénienne enseigne que'));
  kept.add(d.keepId);folded.add(d.foldId);
  const answer=main.answer+'\n\n**'+d.heading+'**\n\n'+extra.answer;
  assert.ok(answer.startsWith(main.answer),'Main teaching not retained');
  assert.ok(answer.endsWith(extra.answer),'Complementary teaching not retained');
  assert.equal(countRefs(answer),countRefs(main.answer)+countRefs(extra.answer),
    'A Psalm reference was lost');
  out.push({main:main.title,alias:extra.title,originalRefs:countRefs(main.answer)+countRefs(extra.answer)});
  allVisible.push({id:main.id,title:main.title,answer});
}
for(const q of original){
  if(!folded.has(q.id)&&!kept.has(q.id))allVisible.push(q);
}
assert.equal(allVisible.length,95);
assert.equal(new Set(allVisible.map(q=>q.id)).size,95);
assert.equal(allVisible.reduce((n,q)=>n+countRefs(q.answer),0),424);
const routing=(await json('data/faq-099-routing.json')).routes;
for(const route of routing){
  if(route.resolution==='unsupported')continue;
  assert.ok(byId.has(route.target_id));
  const effective=directives.groups.find(d=>d.foldId===route.target_id)?.keepId||route.target_id;
  assert.ok(allVisible.some(q=>q.id===effective),
    'Original 19/20 routing now has no visible destination: '+route.question);
}
console.log('FAQ_DEDUP_100_PASS archived=105 visible=95 merged_pairs=10 original_links=424 visible_links=424 aliases_preserved=10');
for(const row of out)console.log('FAQ_DEDUP_PAIR '+JSON.stringify(row));
