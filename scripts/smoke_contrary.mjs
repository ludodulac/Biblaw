/* Verify the source integrity, UI contract and non-judgmental glossary. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=f=>readFileSync(resolve(root,f),'utf8');
const html=read('index.html');
const browser=read('js/biblaw.js');
const glossary=read('js/biblaw-contrary.js');
const vocabulary=JSON.parse(read('data/contrary-lexicon.json'));
const publicData=JSON.parse(read('_site/data/contrary-public.json'));
const catalog=JSON.parse(read('data/browser-search-catalog.json'));
const psalms=new Map(catalog.records.filter(r=>r.recordType==='psalm').map(r=>[r.id,r]));

assert.equal(psalms.size,1158);
assert.equal(publicData.psalmCount,1158);
assert.equal(publicData.schemaVersion,1);
assert.equal(publicData.testedNames,vocabulary.entries.length);
assert.ok(vocabulary.entries.length>120);
assert.ok(publicData.entries.filter(e=>e.verseCount).length>20);
assert.equal(publicData.categories.length,7);
assert.ok(publicData.notice.includes('électricité'));
assert.ok(/phénomène physique/i.test(publicData.notice));
assert.ok(publicData.method.includes('contexte'));
const found=new Map(publicData.entries.map(e=>[e.id,e]));
assert.equal(found.size,publicData.entries.length);
for(const id of ['usurpateur','tenebres','esprits-tenebreux','electricite']) {
  assert.ok(found.has(id),'Requested example missing: '+id);
}
for(const id of [
  'contraryToggle','contraryLibrary','contraryTitle','contraryBack',
  'contraryStatus','contraryDirectory','contraryDetail','contraryFilter',
  'contraryCategory','contraryList','contraryCount','contraryNotice',
  'contraryMethod','contraryName','contraryCategoryName','contraryDefinition',
  'contrarySummary','contraryReferences',
]) assert.equal(html.split('id="'+id+'"').length-1,1,'Missing/duplicate DOM id: '+id);
assert.ok(html.includes('css/biblaw-contrary.css'));
assert.ok(html.includes('js/biblaw-contrary.js'));
assert.ok(browser.includes('BiblawContrary?.setOpenPsalm'));
assert.ok(browser.includes('BiblawContrary?.restoreAfterPsalm'));
assert.ok(browser.includes('BiblawContrary?.setCorpusLoading'));
assert.ok(glossary.includes('globalThis.BiblawContrary = Object.freeze({'));
assert.ok(glossary.includes('source.recordId')&&glossary.includes('verse.number'));
assert.ok(!glossary.includes('innerHTML'),'Do not inject quoted Psalm texts as HTML');
let count=0;
for(const entry of publicData.entries) {
  assert.ok(entry.definition?.length>15,'Definition missing: '+entry.label);
  assert.ok(publicData.categories.includes(entry.category),'Unknown category: '+entry.label);
  assert.equal(entry.psalmCount,entry.sources.length,'Psalm count: '+entry.label);
  const seen=new Set();
  let local=0;
  for(const source of entry.sources) {
    const psalm=psalms.get(source.recordId);
    assert.ok(psalm,'Non-canonical Psalm: '+source.recordId);
    assert.equal(source.book,psalm.book.number);
    assert.equal(source.psalm,psalm.number);
    assert.equal(source.archangel,psalm.archangel);
    for(const verse of source.verses) {
      const key=source.recordId+':'+verse.number;
      assert.ok(!seen.has(key),'Duplicate verse for same term: '+key);
      seen.add(key);
      assert.ok(psalm.verses.some(v=>v.number===verse.number),'Missing verse '+key);
      assert.ok(verse.excerpt?.length>1&&verse.excerpt.length<=260);
      ++local;
    }
  }
  assert.equal(entry.verseCount,local);
  count+=local;
}
assert.ok(count>60);
console.log('FORCES CONTRAIRES PASS: '+publicData.testedNames+
  ' terms searched, '+publicData.entries.filter(e=>e.verseCount).length+
  ' attested, '+count+' genuine Psalm verses checked.');
