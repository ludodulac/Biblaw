/* Minimal source/DOM checks for the public concrete-object directory. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve, dirname} from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = path => readFileSync(resolve(root, path), 'utf8');
const index = read('index.html');
const browserJs = read('js/biblaw.js');
const directoryJs = read('js/biblaw-objects.js');
const publicData = JSON.parse(read('_site/data/objects-public.json'));
const bundle = JSON.parse(read('data/browser-search-catalog.json'));
const psalms = new Map(bundle.records.filter(r => r.recordType === 'psalm')
  .map(r => [r.id, r]));

assert.equal(publicData.schemaVersion, 1);
assert.equal(publicData.psalmCount, 1158);
assert.equal(psalms.size, 1158);
assert.ok(publicData.testedObjectNames > 150);
assert.ok(publicData.entries.length > 20);
assert.ok(publicData.entries.filter(x => x.verseCount).length > 20);
assert.ok(publicData.categories.length >= 6);
assert.ok(index.includes('js/biblaw-objects.js') && index.includes('css/biblaw-objects.css'));
assert.ok(browserJs.includes('BiblawObjects?.setOpenPsalm'));
assert.ok(browserJs.includes('BiblawObjects?.setCorpusLoading'));
assert.ok(directoryJs.includes('source.recordId') && directoryJs.includes('verse.number'));
assert.ok(!directoryJs.includes('innerHTML'), 'Do not inject untrusted Psalm excerpts as HTML');
for (const id of [
  'objectsToggle', 'objectsLibrary', 'objectsBack', 'objectsFilter',
  'objectsCategory', 'objectsDirectory', 'objectsDetail', 'objectsName',
  'objectsCategoryName', 'objectsSummary', 'objectsReferences', 'objectsList',
  'objectsStatus', 'objectsCount', 'objectsMethod'
]) {
  assert.equal(index.split('id="' + id + '"').length - 1, 1,
    'Missing or duplicate object UI id: ' + id);
}
const lookup = new Map(publicData.entries.map(entry => [entry.id, entry]));
assert.equal(lookup.size, publicData.entries.length, 'Duplicated object entry');
for (const mandatory of ['avion', 'cerf-volant']) assert.ok(lookup.has(mandatory));
let links = 0;
for (const entry of publicData.entries) {
  assert.ok(publicData.categories.includes(entry.category), 'Unknown category');
  assert.equal(entry.psalmCount, entry.sources.length);
  const seen = new Set();
  let count = 0;
  for (const source of entry.sources) {
    const psalm = psalms.get(source.recordId);
    assert.ok(psalm, 'Noncanonical Psalm reference: ' + source.recordId);
    assert.equal(source.book, psalm.book.number);
    assert.equal(source.psalm, psalm.number);
    assert.equal(source.archangel, psalm.archangel);
    for (const verse of source.verses) {
      assert.ok(psalm.verses.some(v => v.number === verse.number));
      const key = source.recordId + ':' + verse.number;
      assert.ok(!seen.has(key), 'Repeated verse in the same object: ' + key);
      seen.add(key);
      assert.ok(verse.excerpt && verse.excerpt.length <= 250);
      count++;
    }
  }
  assert.equal(entry.verseCount, count, 'Incorrect verse counter: ' + entry.label);
  links += count;
}
assert.ok(links > 50, 'Insufficient linked object references');
console.log('Objets Biblaw : contrôle DOM et références PASS — ' +
  publicData.entries.length + ' entrées, ' + links + ' références vérifiées.');
