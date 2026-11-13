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
                  'animalReferences', 'animalNotesSection', 'animalNoteReferences',
                  'animalVerseHeading', 'animalAllMentions', 'animalsBack']) {
  assert.equal(html.split('id="' + id + '"').length - 1, 1, 'Unique UI element ' + id);
}
assert.ok(html.includes('js/biblaw-animals.js'));
assert.ok(html.includes('css/biblaw-animals.css'));
assert.ok(read('scripts/build_pages_site.py').includes('animals-public.json'));
const published = JSON.parse(read('data/animals-public.json'));
assert.equal(published.entries.length, editorial.entries.length);
assert.ok(published.entries.some(e => e.category === 'totem' && e.label === 'Licorne'));
assert.ok(published.entries.some(e => e.category === 'other' && e.label === 'Perroquet'));
const bicheTotem = published.entries.find(e => e.category === 'totem' && e.label === 'Biche');
const bicheOther = published.entries.find(e => e.category === 'other' && e.label === 'Biche');
assert.ok(bicheTotem && bicheOther, 'Biche présente dans les deux catégories');
assert.ok(bicheTotem.noteSources.some(n => n.id === 'book-14-psalm-110-note-001'));
const owl = published.entries.find(e => e.id === 'chouette');
assert.ok(owl.noteSources.some(n => n.id === 'book-21-psalm-143-note-003'));
const fox = published.entries.find(e => e.id === 'renard-autres');
assert.ok(fox && fox.sources.length === 0 && fox.occurrences.length === 0 &&
  fox.noteSources.some(n => n.id === 'book-14-psalm-095-note-001'), 'Renard seulement en note');
const snakeGeneral = published.entries.find(e => e.id === 'serpent-autres-mentions');
assert.ok(snakeGeneral && snakeGeneral.occurrences.reduce((n, r) => n + r.verses.length, 0) >= 200);
assert.ok(snakeGeneral.occurrences.some(r => r.recordId === 'book-08-psalm-030' &&
  r.verses.includes(1)), 'Serpent générique présent');
assert.ok(!snakeGeneral.occurrences.some(r => r.recordId === 'book-14-psalm-104' &&
  r.verses.includes(1)), 'Pas de doublon avec serpent de la sagesse');
for (const entry of published.entries) {
  for (const n of entry.noteSources || []) {
    const note = JSON.parse(read('data/notes/books/book-' + n.id.split('-')[1] + '/' + n.id + '.json'));
    assert.equal(note.id, n.id);
    assert.equal(note.appliesTo.recordId, n.recordId);
    assert.equal(note.source.pdfPage, n.sourcePdfPage);
    assert.equal(n.publicationStatus, 'unverified');
  }
}
assert.ok(bicheTotem.sources.some(ref => ref.recordId === 'book-14-psalm-110' &&
  ref.verses.includes(1) && ref.verses.includes(13)), 'Message de Gabriel et famille');
assert.ok(bicheOther.sources.some(ref => ref.recordId === 'book-01-psalm-012' &&
  ref.verses.includes(2)), 'Mise en garde du psaume de Michaël');
assert.ok(bicheOther.sources.some(ref => ref.recordId === 'book-19-psalm-107' &&
  ref.verses.includes(9)), 'Enseignement sur les préjugés de Raphaël');
for (const entry of published.entries) {
  assert.ok(entry.occurrences.length > 0 || (entry.noteSources || []).length > 0,
    'Actual verse or archived note occurrences ' + entry.label);
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
let opened, openedNote;
context.BiblawAnimals.setOpenNote(async id => {openedNote = id;});
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
const bicheButton = get('animalsList').children.find(x => x.children[0].textContent === 'Biche');
assert.ok(bicheButton);
bicheButton.click();
assert.equal(get('animalNotesSection').hidden, false);
assert.ok(get('animalNoteReferences').children[0].children.length > 0);
await get('animalNoteReferences').children[0].children[0].click();
assert.equal(openedNote, 'book-14-psalm-110-note-001');
get('animalsBack').click();
get('animalsBack').click();
assert.equal(get('animalsFamilies').hidden, false);
get('animalsFamilyButtons').children[1].click();
assert.equal(get('animalsDirectory').hidden, false);
const renardButton = get('animalsList').children.find(x =>
  x.children[0].textContent === 'Renard (mention en note)');
assert.ok(renardButton);
renardButton.click();
assert.equal(get('animalVerseHeading').hidden, true);
assert.equal(get('animalAllMentions').hidden, true);
assert.equal(get('animalNotesSection').hidden, false);
get('animalPdf').click();
assert.ok(exported.at(-1).text.includes('transcription à vérifier'));
get('animalsBack').click();
get('animalsBack').click();
get('animalsBack').click();
assert.equal(get('animalsLibrary').hidden, true);
assert.ok(!classes.has('view-animals'));
console.log('Animals site: corpus, two categories, ' + published.entries.length + ' entries, verse links, back, PDF OK.');
