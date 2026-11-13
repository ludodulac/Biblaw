import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read = path => readFileSync(new URL('../' + path, import.meta.url), 'utf8');
const html = read('index.html');
const editorial = JSON.parse(read('data/animals-editorial.json'));
const bundle = JSON.parse(read('data/browser-search-catalog.json'));
const byId = new Map(bundle.records.map(record => [record.id, record]));
assert.equal(bundle.records.filter(r => r.recordType === 'psalm').length, 1158);
for (const id of ['animalsToggle', 'animalsLibrary', 'animalsFamilyButtons', 'animalAnswerText',
                  'animalReferences', 'animalAllMentions', 'animalsBack']) {
  assert.equal(html.split('id="' + id + '"').length - 1, 1, 'Unique UI element ' + id);
}
assert.ok(html.includes('js/biblaw-animals.js'));
assert.ok(html.includes('css/biblaw-animals.css'));
assert.ok(read('scripts/build_pages_site.py').includes('animals-public.json'));
const published = JSON.parse(read('data/animals-public.json'));
assert.equal(published.entries.length, editorial.entries.length);
assert.ok(published.entries.some(e => e.category === 'totem' && e.label === 'Licorne'));
assert.ok(published.entries.some(e => e.category === 'other' && e.label === 'Perroquet'));
for (const entry of published.entries) {
  assert.ok(entry.occurrences.length > 0, 'Actual verse occurrences ' + entry.label);
  for (const reference of [...entry.sources, ...entry.occurrences]) {
    const record = byId.get(reference.recordId);
    assert.ok(record && record.recordType === 'psalm');
    assert.equal(reference.archangel, record.archangel);
    assert.equal(reference.number, record.number);
    assert.ok(reference.verses.every(v => record.verses.some(x => x.number === v)),
      'Exact verses for ' + entry.label);
  }
}

class Element {
  constructor() {
    this.children = []; this.hidden = false; this.textContent = '';
    this.disabled = false; this.events = {}; this.attributes = {};
    this.open = false; this.childElementCount = 0;
  }
  append(...items) { this.children.push(...items); this.childElementCount = this.children.length; }
  replaceChildren(...items) { this.children = items; this.childElementCount = items.length; }
  addEventListener(name, callback) { this.events[name] = callback; }
  setAttribute(name, value) { this.attributes[name] = value; }
  focus() { this.focused = true; }
  click() { const handler = this.events.click || this.onclick; if (handler) return handler(); }
}
const elements = new Map();
const get = id => { if (!elements.has(id)) elements.set(id, new Element()); return elements.get(id); };
get('animalsLibrary').hidden = true;
const classes = new Set(), exported = [];
const window = {scrollY: 200, scrollTo({top}) {this.scrollY = top;}};
const document = {
  getElementById: get,
  createElement: () => new Element(),
  body: {classList: {add: c => classes.add(c), remove: c => classes.delete(c)}}
};
const context = {
  document, window, console,
  BiblawPDF: {download: record => exported.push(record)},
  fetch: async url => {
    assert.ok(url.includes('animals-public.json'));
    return {ok: true, json: async () => published};
  },
};
context.globalThis = context;
vm.runInNewContext(read('js/biblaw-animals.js'), context, {timeout: 10000});
let opened;
context.BiblawAnimals.setCorpusLoading(async () => true);
context.BiblawAnimals.setRecords(bundle.records);
context.BiblawAnimals.setOpenPsalm(ref => {opened = ref;});
await context.BiblawAnimals.open();
assert.equal(get('animalsLibrary').hidden, false);
assert.ok(classes.has('view-animals'));
assert.equal(get('animalsFamilyButtons').children.length, 2);
get('animalsFamilyButtons').children[0].click();
assert.equal(get('animalsDirectory').hidden, false);
assert.ok(get('animalsList').children.length >= 15);
const first = get('animalsList').children[0];
first.click();
assert.equal(get('animalsAnswer').hidden, false);
assert.ok(get('animalAnswerText').textContent.length > 20);
assert.ok(get('animalReferences').children[0].children.length > 0);
const link = get('animalReferences').children[0].children[0];
window.scrollY = 354;
await link.click();
assert.ok(opened.recordId && opened.verses.length > 0, 'Linked reader opens actual psalm');
window.scrollY = 0;
context.BiblawAnimals.restoreAfterPsalm();
assert.equal(window.scrollY, 354);
assert.equal(link.focused, true);
get('animalPdf').click();
assert.equal(exported.length, 1);
assert.ok(exported[0].text.includes('Versets à l’appui'));
get('animalsBack').click();
assert.equal(get('animalsDirectory').hidden, false);
get('animalsBack').click();
assert.equal(get('animalsFamilies').hidden, false);
get('animalsFamilyButtons').children[1].click();
assert.equal(get('animalsDirectory').hidden, false);
get('animalsBack').click();
get('animalsBack').click();
assert.equal(get('animalsLibrary').hidden, true);
assert.ok(!classes.has('view-animals'));
console.log('Animals site: corpus, two categories, ' + published.entries.length + ' entries, verse links, back, PDF OK.');
