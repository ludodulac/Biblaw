/* Validate the magic directory against the 1,158 canonical Psalms. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';

const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=path=>readFileSync(resolve(ROOT,path),'utf8');
const html=read('_site/index.html');
const app=read('_site/js/biblaw.js');
const js=read('_site/js/biblaw-magic.js');
const document=JSON.parse(read('_site/data/magic-public.json'));
const catalog=JSON.parse(read('data/browser-search-catalog.json'));
const canonical=new Map(catalog.records.filter(r=>r.recordType==='psalm').map(r=>[r.id,r]));
assert.equal(canonical.size,1158);
assert.equal(document.schemaVersion,1);
assert.equal(document.psalmCount,1158);
assert.ok(document.parts.length>=10);
assert.ok(document.parts.at(-1).id==='toutes-les-mentions');
assert.ok(document.curatedVerseLinks>=130);
assert.ok(document.lexicalVerseLinks>=150);
assert.ok(document.lexicalPsalmCount>=20);

for (const id of ['magicToggle','magicLibrary','magicTitle','magicBack','magicStatus',
  'magicDirectory','magicCategories','magicMethod','magicDetail','magicPartTitle',
  'magicPartIntro','magicReferences']){
  assert.equal(html.split('id="'+id+'"').length-1,1,'Missing or repeated magic element: '+id);
}
assert.ok(html.includes('css/biblaw-magic.css?v=001'));
assert.ok(html.includes('js/biblaw-magic.js?v=001'));
assert.ok(app.includes('BiblawMagic?.open()'));
assert.ok(app.includes('BiblawMagic?.setCorpusLoading(ensureCorpusReady)'));
assert.ok(app.includes('BiblawMagic?.restoreAfterPsalm()'));
assert.ok(app.includes("sourceParams.get('rubrique')==='magie'"));
assert.ok(js.includes('globalThis.BiblawMagic = Object.freeze({'));
assert.ok(!js.includes('innerHTML'), 'Magic source citations must not use raw HTML injection');

let links=0,editorial=0,lexical=0;
const seenPartIds=new Set();
for(const part of document.parts){
  assert.ok(part.id&&part.label&&part.intro);
  assert.ok(!seenPartIds.has(part.id), 'Duplicate magic category '+part.id);
  seenPartIds.add(part.id);
  assert.ok(part.entries.length);
  for(const entry of part.entries){
    assert.ok(entry.title&&entry.summary&&entry.references.length);
    for(const ref of entry.references){
      const source=canonical.get(ref.recordId);
      assert.ok(source,'Missing canonical Psalm: '+ref.recordId);
      const verses=new Map(source.verses.map(v=>[v.number,v.text]));
      assert.ok(ref.verses.length>0);
      assert.equal(new Set(ref.verses).size,ref.verses.length,'Duplicate verse cited');
      for(const number of ref.verses){
        assert.ok(verses.has(number),'Missing verse '+ref.recordId+':'+number);
        links++;
        if(entry.kind==='lexical')lexical++;else editorial++;
      }
      if(ref.excerpt){
        assert.ok(ref.excerpt.length>5&&ref.excerpt.length<=224);
        const clean=ref.excerpt.replace(/^…/,'').replace(/…$/,'').replace(/\s+/g,' ').trim();
        assert.ok(ref.verses.some(n=>verses.get(n).replace(/\s+/g,' ').includes(clean)),
          'Excerpt must be lifted from a cited canonical verse: '+ref.recordId);
      }
    }
  }
}
assert.equal(document.curatedVerseLinks,editorial);
assert.equal(document.lexicalVerseLinks,lexical);
assert.equal(links,editorial+lexical);
console.log('MAGIC PASS: '+document.parts.length+' parties, '+editorial+
  ' versets thématiques et '+lexical+' mentions lexicales authentifiées.');
