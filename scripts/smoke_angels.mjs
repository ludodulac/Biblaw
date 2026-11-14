/* Verify the 12 × 12 source list, the compiled lexical evidence, and site wiring. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=path=>readFileSync(resolve(root,path),'utf8');
const source=JSON.parse(read('data/anges-gabriel.json'));
const compiled=JSON.parse(read('_site/data/angels-public.json'));
const catalog=JSON.parse(read('data/browser-search-catalog.json'));
const html=read('index.html');
const app=read('js/biblaw.js');
const browser=read('js/biblaw-angels.js');
const stage=read('scripts/build_pages_site.py');
const psalms=new Map(catalog.records.filter(r=>r.recordType==='psalm')
  .map(record=>[record.id,record]));

assert.equal(psalms.size,1158);
assert.equal(source.schemaVersion,1);
assert.equal(source.perles.length,12);
assert.equal(compiled.schemaVersion,1);
assert.equal(compiled.psalmCount,1158);
assert.equal(compiled.perlesCount,12);
assert.equal(compiled.filsCount,144);
assert.equal(compiled.entryCount,156);
assert.equal(compiled.entries.length,156);

const labels=source.perles.flatMap(perle=>{
  assert.equal(perle.fils.length,12);
  assert.ok(perle.id&&perle.label&&perle.dates&&perle.gardiens);
  return [perle.label,...perle.fils];
});
assert.equal(new Set(labels).size,156);
assert.ok(labels.includes('Illua'));
assert.ok(source.transcriptionNotice.includes('orthographe non confirmée'));
const found=new Map(compiled.entries.map(entry=>[entry.label,entry]));
assert.equal(found.size,156);
let total=0;
for(const label of labels){
  const entry=found.get(label);
  assert.ok(entry,'Missing virtue: '+label);
  assert.equal(entry.psalmCount,entry.sources.length);
  const seen=new Set();
  for(const source of entry.sources){
    const psalm=psalms.get(source.recordId);
    assert.ok(psalm,'Non-canonical reference: '+source.recordId);
    assert.equal(source.book,psalm.book.number);
    assert.equal(source.psalm,psalm.number);
    assert.equal(source.archangel,psalm.archangel);
    for(const verse of source.verses){
      const key=source.recordId+':'+verse.number;
      assert.ok(!seen.has(key),'Duplicate reference for '+label+': '+key);
      seen.add(key);
      assert.ok(psalm.verses.some(item=>item.number===verse.number),
        'Unknown verse: '+key);
      assert.ok(verse.excerpt&&verse.excerpt.length<=250);
      ++total;
    }
  }
  assert.equal(seen.size,entry.verseCount);
}
assert.ok(total>100,'Unexpectedly few explicit matches');

for(const id of [
  'perlesToggle','filsToggle','angelsLibrary','angelsTitle',
  'angelsBack','angelsStatus','angelsDirectory','angelsDetail',
  'angelsFilter','angelsGroupWrap','angelsGroup','angelsCount',
  'angelsList','angelsMethod','angelsName','angelsMetadata',
  'angelsSummary','angelsReferences','angelsIntro'
]) assert.equal(html.split('id="'+id+'"').length-1,1,'Missing/duplicate DOM ID '+id);
for(const item of ['css/biblaw-angels.css','js/biblaw-angels.js',
  'data/anges-gabriel.json']) {
  assert.ok(stage.includes('"'+item+'"'),'Missing Pages file: '+item);
  assert.ok(html.includes(item)||item.startsWith('data/'));
}
assert.ok(stage.includes('generate_public_angels'));
assert.ok(stage.includes('data/angels-public.json'));
assert.ok(browser.includes('data/angels-public.json'));
assert.ok(browser.includes('globalThis.BiblawAngels'));
assert.ok(!browser.includes('innerHTML'), 'Psalm passages must be inserted as text');
assert.ok(app.includes('BiblawAngels?.setOpenPsalm'));
assert.ok(app.includes('BiblawAngels?.setCorpusLoading'));
assert.ok(app.includes('BiblawAngels?.restoreAfterPsalm'));
assert.ok(app.includes('BiblawAngels?.setRecords'));
console.log('ANGELS PASS: 12 Anges-perles, 144 Anges-fils, 1158 Psalms, '+
  total+' exact verse mentions verified against the corpus.');
