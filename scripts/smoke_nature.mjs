/* Documentary and UI invariants for the nature index; run after generation. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';

const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=path=>readFileSync(resolve(ROOT,path),'utf8');
const html=read('index.html');
const js=read('js/biblaw-nature.js');
const app=read('js/biblaw.js');
const lexicon=JSON.parse(read('data/nature-lexicon.json'));
const publicData=JSON.parse(read('_site/data/nature-public.json'));
const corpus=JSON.parse(read('data/browser-search-catalog.json'));
const canonical=new Map(corpus.records.filter(r=>r.recordType==='psalm').map(r=>[r.id,r]));
assert.equal(canonical.size,1158);
assert.equal(publicData.schemaVersion,1);
assert.equal(publicData.psalmCount,1158);
assert.equal(publicData.testedNames,lexicon.entries.length);
assert.ok(publicData.testedNames>130);
assert.ok(publicData.categories.length>=5);
assert.ok(publicData.entries.filter(e=>e.verseCount).length>30);
assert.ok(html.includes('Les éléments naturels dans la Bible'));
assert.ok(html.includes('css/biblaw-nature.css'));
assert.ok(html.includes('js/biblaw-nature.js'));
assert.ok(app.includes('BiblawNature?.setOpenPsalm'));
assert.ok(app.includes('BiblawNature?.setCorpusLoading'));
assert.ok(app.includes('BiblawNature?.restoreAfterPsalm'));
assert.ok(js.includes('globalThis.BiblawNature = Object.freeze({'));
assert.ok(js.includes('source.recordId')&&js.includes('verse.number'));
assert.ok(!js.includes('innerHTML'), 'Citations should use safe textContent rendering');
for(const id of ['natureToggle','natureLibrary','natureTitle','natureBack','natureStatus',
  'natureDirectory','natureDetail','natureFilter','natureCategory','natureList',
  'natureCount','natureMethod','natureName','natureCategoryName','natureSummary',
  'natureReferences']){
  assert.equal(html.split('id="'+id+'"').length-1,1,'Missing/duplicate nature UI ID: '+id);
}
const entries=new Map(publicData.entries.map(e=>[e.id,e]));
assert.equal(entries.size,publicData.entries.length,'Duplicate index entry');
for(const id of ['riviere','montagne','nuage','foret','vent','pluie'])
  assert.ok(entries.has(id),'Missing explicitly requested element: '+id);
let links=0;
for(const entry of publicData.entries){
  assert.ok(publicData.categories.includes(entry.category),'Unknown element category');
  assert.equal(entry.psalmCount,entry.sources.length);
  let verses=0;
  const seen=new Set();
  for(const source of entry.sources){
    const psalm=canonical.get(source.recordId);
    assert.ok(psalm,'Only canonical Psalms should be linked: '+source.recordId);
    assert.equal(source.archangel,psalm.archangel);
    assert.equal(source.psalm,psalm.number);
    assert.equal(source.book,psalm.book.number);
    for(const verse of source.verses){
      const key=source.recordId+':'+verse.number;
      assert.ok(!seen.has(key),'Duplicate citation: '+key);
      seen.add(key);
      assert.ok(psalm.verses.some(v=>v.number===verse.number),'Missing verse '+key);
      assert.ok(verse.excerpt.length>=3&&verse.excerpt.length<=255);
      verses++;
    }
  }
  assert.equal(entry.verseCount,verses);
  links+=verses;
}
assert.ok(links>100);
console.log('NATURE PASS : '+publicData.testedNames+' éléments recherchés, '+
  publicData.entries.filter(e=>e.verseCount).length+' trouvés, '+links+
  ' liens canoniques contrôlés.');
