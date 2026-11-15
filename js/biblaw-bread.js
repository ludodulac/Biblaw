/* Biblaw — sélection documentaire sur le pain, le grain et la nourriture. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {
    parts: null, loading: null, current: null, requestId: 0,
    directoryScroll: 0, lastReaderScroll: 0, lastLink: null,
    openPsalm: null, corpusLoading: null, recordsReady: false,
  };
  const ARCHANGELS = ['Michaël', 'Gabriel', 'Raphaël', 'Ouriel'];
  const top = () => window.scrollTo({top: 0, behavior: 'instant'});

  function element(tag, klass, value) {
    const node = document.createElement(tag);
    if (klass) node.className = klass;
    if (value !== undefined) node.textContent = value;
    return node;
  }
  function status(value) {
    const node = $('breadStatus');
    node.textContent = value || '';
    node.hidden = !value;
  }
  function sourceLabel(recordId) {
    const match = /^book-(\d{2})-psalm-(\d{3})$/.exec(recordId);
    if (!match) return recordId;
    const book = Number(match[1]), psalm = Number(match[2]);
    return 'Psaume ' + psalm + ' de ' + ARCHANGELS[(book - 1) % 4] + ' · Livre ' + book;
  }
  function renderDirectory() {
    state.current = null;
    $('breadDirectory').hidden = false;
    $('breadDetail').hidden = true;
    $('breadBack').textContent = '← Retour';
    const list = $('breadCategories');
    list.replaceChildren();
    for (const part of state.parts) {
      const button = element('button', 'faq-question-item bread-part');
      button.type = 'button';
      const wrap = element('span', 'faq-question-title');
      wrap.append(
        element('strong', 'bread-part-name', part.label),
        element('small', 'bread-part-count',
          part.entries.length + (part.entries.length > 1 ? ' sujets' : ' sujet'))
      );
      button.append(wrap, element('span', 'faq-chevron', '›'));
      button.addEventListener('click', () => showPart(part));
      list.append(button);
    }
  }
  function referenceCard(ref) {
    const row = element('div', 'bread-reference');
    const button = element('button', 'faq-psalm-link bread-verse-link',
      'Lire ' + sourceLabel(ref.recordId) + ', ' +
      (ref.verses.length > 1 ? 'versets ' : 'verset ') + ref.verses.join(', '));
    button.type = 'button';
    button.addEventListener('click', () => openVerse(ref, button));
    row.append(button);
    return row;
  }
  function showPart(part) {
    state.directoryScroll = window.scrollY;
    state.current = part;
    ++state.requestId;
    $('breadDirectory').hidden = true;
    $('breadDetail').hidden = false;
    $('breadBack').textContent = '← Toutes les parties';
    $('breadPartTitle').textContent = part.label;
    $('breadPartIntro').textContent = part.intro;
    const list = $('breadReferences');
    list.replaceChildren();
    for (const entry of part.entries) {
      const card = element('section', 'bread-source');
      card.append(
        element('h4', 'bread-source-heading', entry.title),
        element('p', 'bread-source-summary', entry.summary)
      );
      for (const ref of entry.references) card.append(referenceCard(ref));
      list.append(card);
    }
    status('');
    top();
    $('breadPartTitle').focus({preventScroll: true});
  }
  async function openVerse(ref, button) {
    const token = state.requestId;
    state.lastLink = button;
    state.lastReaderScroll = window.scrollY;
    try {
      if (!state.openPsalm) throw Error('Le lecteur des psaumes est indisponible.');
      if (!state.recordsReady) {
        status('Chargement du psaume…');
        if (!state.corpusLoading || !await state.corpusLoading()) {
          throw Error('Impossible de charger le corpus des psaumes.');
        }
      }
      if (token !== state.requestId || $('breadLibrary').hidden) return;
      status('');
      state.openPsalm({recordId: ref.recordId, verses: ref.verses});
    } catch (error) {
      if (token === state.requestId && !$('breadLibrary').hidden)
        status(error.message || 'Impossible de lire ce verset.');
      console.error(error);
    }
  }
  async function load() {
    if (state.parts) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/bread-public.json?v=002').then(async response => {
      if (!response.ok) throw Error('Répertoire du pain indisponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || !Array.isArray(data.parts) || !data.parts.length)
        throw Error('Répertoire du pain incomplet.');
      for (const part of data.parts) {
        if (!part.label || !Array.isArray(part.entries) || !part.entries.length)
          throw Error('Partie documentaire incomplète.');
        for (const entry of part.entries) {
          if (!entry.title || !Array.isArray(entry.references) || !entry.references.length)
            throw Error('Référence documentaire incomplète.');
          for (const ref of entry.references) {
            if (!/^book-\d{2}-psalm-\d{3}$/.test(ref.recordId) ||
                !Array.isArray(ref.verses) || !ref.verses.length ||
                !ref.verses.every(v => Number.isInteger(v) && v > 0))
              throw Error('Référence de psaume invalide.');
          }
        }
      }
      state.parts = data.parts;
      $('breadMethod').textContent = data.method || '';
      return true;
    }).catch(error => {
      status(error.message || 'Impossible de charger les passages.');
      console.error(error);
      return false;
    }).finally(() => {state.loading = null;});
    return state.loading;
  }
  async function open() {
    const token = ++state.requestId;
    document.body.classList.add('view-bread');
    $('breadLibrary').hidden = false;
    $('breadToggle').setAttribute('aria-expanded', 'true');
    status('Recherche des passages consacrés au pain…');
    top();
    const ready = await load();
    if (token !== state.requestId || $('breadLibrary').hidden) return;
    if (ready) {
      status('');
      renderDirectory();
    }
  }
  function close() {
    ++state.requestId;
    state.current = null;
    $('breadLibrary').hidden = true;
    document.body.classList.remove('view-bread');
    $('breadToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      const y = state.directoryScroll;
      renderDirectory();
      window.scrollTo({top: y, behavior: 'instant'});
    } else {
      close();
      top();
      $('breadToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('breadLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastReaderScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  $('breadBack').addEventListener('click', back);
  globalThis.BiblawBread = Object.freeze({
    open, close, restoreAfterPsalm,
    setOpenPsalm(callback) {state.openPsalm = callback;},
    setCorpusLoading(callback) {state.corpusLoading = callback;},
    setRecords(records) {
      state.recordsReady = Array.isArray(records) &&
        records.some(record => record.recordType === 'psalm');
    },
  });
})();
