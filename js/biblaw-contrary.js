/* Biblaw — contextual index of contrary forces / expressions from canonical Psalms. */
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
  const count = (number, singular) =>
    number + ' ' + singular + (number > 1 ? 's' : '');
  const normalize = text => (text || '').normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').toLowerCase();

  function node(tag, klass, contents) {
    const el = document.createElement(tag);
    if (klass) el.className = klass;
    if (contents !== undefined) el.textContent = contents;
    return el;
  }
  function status(message) {
    $('contraryStatus').textContent = message || '';
    $('contraryStatus').hidden = !message;
  }
  function elementButton(entry) {
    const btn = node('button', 'faq-question-item contrary-item');
    btn.type = 'button';
    const contents = node('span', 'faq-question-title');
    contents.append(node('strong', 'contrary-item-name', entry.label));
    contents.append(node('small', 'contrary-item-count',
      entry.verseCount ?
        count(entry.psalmCount, 'psaume') + ' · ' + count(entry.verseCount, 'verset') :
        'Aucune mention explicite trouvée'));
    btn.append(contents, node('span', 'faq-chevron', '›'));
    btn.addEventListener('click', () => showElement(entry));
    return btn;
  }
  function renderDirectory() {
    ++state.requestId;
    state.current = null;
    $('contraryDirectory').hidden = false;
    $('contraryDetail').hidden = true;
    const filter = normalize($('contraryFilter').value.trim());
    const category = $('contraryCategory').value;
    const entries = state.entries.filter(entry =>
      (!category || entry.category === category) &&
      (!filter || normalize(entry.label).includes(filter)));
    $('contraryCount').textContent =
      count(entries.length, 'terme') + ' · ' +
      count(state.entries.filter(e => e.verseCount).length, 'terme') +
      ' attestés dans les psaumes.';
    const list = $('contraryList');
    list.replaceChildren();
    for (const entry of entries) list.append(elementButton(entry));
    if (!entries.length) list.append(node('p', 'contrary-empty',
      'Aucun terme correspondant à cette recherche.'));
  }
  function verseButton(source, verse) {
    const button = node('button', 'faq-psalm-link contrary-verse-link',
      'Lire le psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ', verset ' + verse.number);
    button.type = 'button';
    button.addEventListener('click', () => openVerse(source, verse, button));
    return button;
  }
  function verseCard(source, verse) {
    const row = node('div', 'contrary-verse');
    row.append(node('p', 'contrary-verse-excerpt', '« ' + verse.excerpt + ' »'));
    row.append(verseButton(source, verse));
    return row;
  }
  function sourceCard(source) {
    const card = node('section', 'contrary-source');
    card.append(node('h4', 'contrary-source-heading',
      'Psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ' · Livre ' + source.book));
    const [first, ...rest] = source.verses;
    if (first) card.append(verseCard(source, first));
    if (rest.length) {
      const details = node('details', 'contrary-source-more');
      details.append(node('summary', '', 'Voir ' + count(rest.length, 'autre verset') +
        ' de ce psaume'));
      const body = node('div', 'contrary-source-more-content');
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
  function showElement(entry) {
    state.directoryScroll = window.scrollY;
    state.current = entry;
    ++state.requestId;
    $('contraryDirectory').hidden = true;
    $('contraryDetail').hidden = false;
    $('contraryName').textContent = entry.label;
    $('contraryCategoryName').textContent = entry.category;
    $('contraryDefinition').textContent = entry.definition;
    $('contrarySummary').textContent = entry.verseCount ?
      'Cette expression apparaît dans ' + count(entry.psalmCount, 'psaume') +
      ' et ' + count(entry.verseCount, 'verset') +
      '. Les extraits reproduisent les formulations des psaumes, sans interprétation imposée.' :
      'Aucune occurrence exacte de cette expression n’a été relevée parmi les 1 158 psaumes examinés.';
    const list = $('contraryReferences');
    list.replaceChildren();
    const initial = entry.sources.slice(0, 12);
    for (const source of initial) list.append(sourceCard(source));
    if (entry.sources.length > initial.length) {
      const more = node('details', 'contrary-more-sources');
      more.append(node('summary', '',
        'Voir les ' + (entry.sources.length - initial.length) + ' autres psaumes'));
      const body = node('div', 'contrary-more-content');
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
    $('contraryName').focus({preventScroll: true});
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
      if (token !== state.requestId || $('contraryLibrary').hidden) return;
      status('');
      state.openPsalm({recordId: source.recordId, verses: [verse.number]});
    } catch (error) {
      if (token === state.requestId && !$('contraryLibrary').hidden)
        status(error.message || 'Impossible d’ouvrir ce verset.');
      console.error(error);
    }
  }
  async function load() {
    if (state.entries) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/contrary-public.json?v=001').then(async response => {
      if (!response.ok) throw Error('Répertoire des termes indisponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || data.psalmCount !== 1158 ||
          !Array.isArray(data.entries) || !Array.isArray(data.categories))
        throw Error('Répertoire des termes incomplet.');
      state.entries = data.entries;
      state.categories = data.categories;
      const select = $('contraryCategory');
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
      $('contraryMethod').textContent = data.method;
      $('contraryNotice').textContent = data.notice || '';
      return true;
    }).catch(error => {
      status(error.message || 'Impossible de charger les termes.');
      console.error(error);
      return false;
    }).finally(() => { state.loading = null; });
    return state.loading;
  }
  async function open() {
    const token = ++state.requestId;
    document.body.classList.add('view-contrary');
    $('contraryLibrary').hidden = false;
    $('contraryToggle').setAttribute('aria-expanded', 'true');
    $('contraryDirectory').hidden = false;
    $('contraryDetail').hidden = true;
    status('Recherche des termes dans les psaumes…');
    toTop();
    const ready = await load();
    if (token !== state.requestId || $('contraryLibrary').hidden) return;
    if (ready) {
      status('');
      renderDirectory();
    }
  }
  function close() {
    ++state.requestId;
    state.current = null;
    $('contraryLibrary').hidden = true;
    document.body.classList.remove('view-contrary');
    $('contraryToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      const y = state.directoryScroll;
      renderDirectory();
      window.scrollTo({top: y, behavior: 'instant'});
    } else {
      close();
      toTop();
      $('contraryToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('contraryLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastReaderScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  $('contraryBack').addEventListener('click', back);
  $('contraryFilter').addEventListener('input', () => { if (state.entries) renderDirectory(); });
  $('contraryCategory').addEventListener('change', () => { if (state.entries) renderDirectory(); });
  globalThis.BiblawContrary = Object.freeze({
    open, close, restoreAfterPsalm,
    setOpenPsalm(callback) { state.openPsalm = callback; },
    setCorpusLoading(callback) { state.corpusLoading = callback; },
    setRecords(records) {
      state.recordsReady = Array.isArray(records) && records.some(r => r.recordType === 'psalm');
    },
  });
})();