/* Biblaw — concrete objects explicitly named in canonical Psalms. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {
    entries: null, categories: [], loading: null, current: null,
    directoryScroll: 0, lastReaderScroll: 0, lastLink: null,
    requestId: 0, openPsalm: null, corpusLoading: null, recordsReady: false,
  };
  const archangel = name => ({
    michael: 'Michaël', gabriel: 'Gabriel',
    raphael: 'Raphaël', ouriel: 'Ouriel',
  }[name] || name || '');
  const toTop = () => window.scrollTo({top: 0, behavior: 'instant'});
  const count = (number, singular) => number + ' ' + singular + (number > 1 ? 's' : '');
  const normalize = text => (text || '').normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').toLowerCase();

  function node(tag, klass, contents) {
    const el = document.createElement(tag);
    if (klass) el.className = klass;
    if (contents !== undefined) el.textContent = contents;
    return el;
  }
  function status(message) {
    $('objectsStatus').textContent = message || '';
    $('objectsStatus').hidden = !message;
  }
  function objectButton(entry) {
    const btn = node('button', 'faq-question-item objects-item');
    btn.type = 'button';
    const contents = node('span', 'faq-question-title');
    contents.append(node('strong', 'objects-item-name', entry.label));
    contents.append(node('small', 'objects-item-count',
      entry.verseCount ?
        count(entry.psalmCount, 'psaume') + ' · ' + count(entry.verseCount, 'verset') :
        'Aucune mention explicite trouvée'));
    btn.append(contents, node('span', 'faq-chevron', '›'));
    btn.addEventListener('click', () => showObject(entry));
    return btn;
  }
  function renderDirectory() {
    ++state.requestId;
    state.current = null;
    $('objectsDirectory').hidden = false;
    $('objectsDetail').hidden = true;
    const filter = normalize($('objectsFilter').value.trim());
    const category = $('objectsCategory').value;
    const entries = state.entries.filter(entry =>
      (!category || entry.category === category) &&
      (!filter || normalize(entry.label).includes(filter)));
    $('objectsCount').textContent =
      count(entries.length, 'objet') + ' · ' +
      count(state.entries.filter(e => e.verseCount).length, 'objet') +
      ' attestés dans les psaumes.';
    const list = $('objectsList');
    list.replaceChildren();
    for (const entry of entries) list.append(objectButton(entry));
    if (!entries.length) list.append(node('p', 'objects-empty',
      'Aucun objet correspondant à cette recherche.'));
  }
  function verseButton(source, verse) {
    const button = node('button', 'faq-psalm-link objects-verse-link',
      'Lire le psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ', verset ' + verse.number);
    button.type = 'button';
    button.addEventListener('click', () => openVerse(source, verse, button));
    return button;
  }
  function verseCard(source, verse) {
    const row = node('div', 'objects-verse');
    row.append(node('p', 'objects-verse-excerpt', '« ' + verse.excerpt + ' »'));
    row.append(verseButton(source, verse));
    return row;
  }
  function sourceCard(source) {
    const card = node('section', 'objects-source');
    card.append(node('h4', 'objects-source-heading',
      'Psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ' · Livre ' + source.book));
    const [first, ...rest] = source.verses;
    if (first) card.append(verseCard(source, first));
    if (rest.length) {
      const details = node('details', 'objects-source-more');
      details.append(node('summary', '', 'Voir ' + count(rest.length, 'autre verset') +
        ' de ce psaume'));
      const body = node('div', 'objects-source-more-content');
      details.append(body);
      details.addEventListener('toggle', () => {
        if (details.open && !body.childElementCount) {
          for (const verse of rest) body.append(verseCard(source, verse));
        }
      });
      card.append(details);
    }
    return card;
  }
  function showObject(entry) {
    state.directoryScroll = window.scrollY;
    state.current = entry;
    ++state.requestId;
    $('objectsDirectory').hidden = true;
    $('objectsDetail').hidden = false;
    $('objectsName').textContent = entry.label;
    $('objectsCategoryName').textContent = entry.category;
    $('objectsSummary').textContent = entry.verseCount ?
      'Le mot désignant cet objet apparaît dans ' + count(entry.psalmCount, 'psaume') +
      ' et ' + count(entry.verseCount, 'verset') +
      '. Les extraits reproduisent le contexte où il est nommé.' :
      'Aucune mention explicite de cet objet n’a été trouvée dans les 1 158 psaumes examinés.';
    const list = $('objectsReferences');
    list.replaceChildren();
    const initial = entry.sources.slice(0, 12);
    for (const source of initial) list.append(sourceCard(source));
    if (entry.sources.length > initial.length) {
      const more = node('details', 'objects-more-sources');
      more.append(node('summary', '',
        'Voir les ' + (entry.sources.length - initial.length) + ' autres psaumes'));
      const body = node('div', 'objects-more-content');
      more.append(body);
      more.addEventListener('toggle', () => {
        if (more.open && !body.childElementCount) {
          for (const source of entry.sources.slice(initial.length))
            body.append(sourceCard(source));
        }
      });
      list.append(more);
    }
    status('');
    toTop();
    $('objectsName').focus({preventScroll: true});
  }
  async function openVerse(source, verse, button) {
    state.lastLink = button;
    state.lastReaderScroll = window.scrollY;
    const token = state.requestId;
    try {
      if (!state.openPsalm) throw Error('Le lecteur des psaumes est indisponible.');
      if (!state.recordsReady) {
        status('Chargement du psaume…');
        if (!state.corpusLoading || !await state.corpusLoading())
          throw Error('Impossible de charger les psaumes.');
      }
      if (token !== state.requestId || $('objectsLibrary').hidden) return;
      status('');
      state.openPsalm({recordId: source.recordId, verses: [verse.number]});
    } catch (error) {
      if (token === state.requestId && !$('objectsLibrary').hidden)
        status(error.message || 'Impossible d’ouvrir ce verset.');
      console.error(error);
    }
  }
  async function load() {
    if (state.entries) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/objects-public.json?v=001').then(async response => {
      if (!response.ok) throw Error('Répertoire des objets indisponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || data.psalmCount !== 1158 ||
          !Array.isArray(data.entries) || !Array.isArray(data.categories))
        throw Error('Répertoire des objets incomplet.');
      state.entries = data.entries;
      state.categories = data.categories;
      const select = $('objectsCategory');
      select.replaceChildren();
      const all = node('option', '', 'Toutes les catégories');
      all.value = '';
      select.append(all);
      for (const category of state.categories) {
        if (!state.entries.some(e => e.category === category)) continue;
        const option = node('option', '', category);
        option.value = category;
        select.append(option);
      }
      $('objectsMethod').textContent = data.method;
      return true;
    }).catch(error => {
      status(error.message || 'Impossible de charger les objets.');
      console.error(error);
      return false;
    }).finally(() => { state.loading = null; });
    return state.loading;
  }
  async function open() {
    const token = ++state.requestId;
    document.body.classList.add('view-objects');
    $('objectsLibrary').hidden = false;
    $('objectsToggle').setAttribute('aria-expanded', 'true');
    $('objectsDirectory').hidden = false;
    $('objectsDetail').hidden = true;
    status('Recherche des objets dans les psaumes…');
    toTop();
    const ready = await load();
    if (token !== state.requestId || $('objectsLibrary').hidden) return;
    if (ready) {
      status('');
      renderDirectory();
    }
  }
  function close() {
    ++state.requestId;
    state.current = null;
    $('objectsLibrary').hidden = true;
    document.body.classList.remove('view-objects');
    $('objectsToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      const y = state.directoryScroll;
      renderDirectory();
      window.scrollTo({top: y, behavior: 'instant'});
    } else {
      close();
      toTop();
      $('objectsToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('objectsLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastReaderScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  $('objectsBack').addEventListener('click', back);
  $('objectsFilter').addEventListener('input', () => { if (state.entries) renderDirectory(); });
  $('objectsCategory').addEventListener('change', () => { if (state.entries) renderDirectory(); });
  globalThis.BiblawObjects = Object.freeze({
    open, close, restoreAfterPsalm,
    setOpenPsalm(callback) { state.openPsalm = callback; },
    setCorpusLoading(callback) { state.corpusLoading = callback; },
    setRecords(records) {
      state.recordsReady = Array.isArray(records) && records.some(r => r.recordType === 'psalm');
    },
  });
})();