/* Biblaw — recherches sur la magie : choix éditoriaux et index lexical complet. */
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
    const node = $('magicStatus');
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
    $('magicDirectory').hidden = false;
    $('magicDetail').hidden = true;
    $('magicBack').textContent = '← Retour';
    const list = $('magicCategories');
    list.replaceChildren();
    for (const part of state.parts) {
      const button = element('button', 'faq-question-item magic-part');
      button.type = 'button';
      const wrap = element('span', 'faq-question-title');
      wrap.append(
        element('strong', 'magic-part-name', part.label),
        element('small', 'magic-part-count',
          part.entries.length + (part.entries.length > 1 ? ' sujets' : ' sujet'))
      );
      button.append(wrap, element('span', 'faq-chevron', '›'));
      button.addEventListener('click', () => showPart(part));
      list.append(button);
    }
  }
  function referenceCard(ref) {
    const row = element('div', 'magic-reference');
    const button = element('button', 'faq-psalm-link magic-verse-link',
      'Lire ' + sourceLabel(ref.recordId) + ', ' +
      (ref.verses.length > 1 ? 'versets ' : 'verset ') + ref.verses.join(', '));
    button.type = 'button';
    button.addEventListener('click', () => openVerse(ref, button));
    if (ref.excerpt) row.append(element('p', 'magic-excerpt', ref.excerpt));
    row.append(button);
    return row;
  }
  function showPart(part) {
    state.directoryScroll = window.scrollY;
    state.current = part;
    ++state.requestId;
    $('magicDirectory').hidden = true;
    $('magicDetail').hidden = false;
    $('magicBack').textContent = '← Toutes les parties';
    $('magicPartTitle').textContent = part.label;
    $('magicPartIntro').textContent = part.intro;
    const list = $('magicReferences');
    list.replaceChildren();
    for (const entry of part.entries) {
      const card = element('section', 'magic-source');
      card.append(
        element('h4', 'magic-source-heading', entry.title),
        element('p', 'magic-source-summary', entry.summary)
      );
      // Show the first citations immediately; keep longer concordance lists
      // readable on mobile by grouping the remaining sources in a disclosure.
      const immediate = entry.references.slice(0, 8);
      for (const ref of immediate) card.append(referenceCard(ref));
      if (entry.references.length > immediate.length) {
        const remainder = entry.references.slice(immediate.length);
        const more = element('details', 'magic-more');
        more.append(element('summary', '', 'Afficher ' + remainder.length +
          ' autres psaumes'));
        const container = element('div', 'magic-more-content');
        for (const ref of remainder) container.append(referenceCard(ref));
        more.append(container);
        card.append(more);
      }
      list.append(card);
    }
    status('');
    top();
    $('magicPartTitle').focus({preventScroll: true});
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
      if (token !== state.requestId || $('magicLibrary').hidden) return;
      status('');
      state.openPsalm({recordId: ref.recordId, verses: ref.verses});
    } catch (error) {
      if (token === state.requestId && !$('magicLibrary').hidden)
        status(error.message || 'Impossible de lire ce verset.');
      console.error(error);
    }
  }
  async function load() {
    if (state.parts) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/magic-public.json?v=001').then(async response => {
      if (!response.ok) throw Error('Répertoire de la magie indisponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || !Array.isArray(data.parts) || !data.parts.length)
        throw Error('Répertoire de la magie incomplet.');
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
      $('magicMethod').textContent = data.method || '';
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
    document.body.classList.add('view-magic');
    $('magicLibrary').hidden = false;
    $('magicToggle').setAttribute('aria-expanded', 'true');
    status('Recherche des passages consacrés à la magie…');
    top();
    const ready = await load();
    if (token !== state.requestId || $('magicLibrary').hidden) return;
    if (ready) {
      status('');
      renderDirectory();
    }
  }
  function close() {
    ++state.requestId;
    state.current = null;
    $('magicLibrary').hidden = true;
    document.body.classList.remove('view-magic');
    $('magicToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      const y = state.directoryScroll;
      renderDirectory();
      window.scrollTo({top: y, behavior: 'instant'});
    } else {
      close();
      top();
      $('magicToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('magicLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastReaderScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  $('magicBack').addEventListener('click', back);
  globalThis.BiblawMagic = Object.freeze({
    open, close, restoreAfterPsalm,
    setOpenPsalm(callback) {state.openPsalm = callback;},
    setCorpusLoading(callback) {state.corpusLoading = callback;},
    setRecords(records) {
      state.recordsReady = Array.isArray(records) &&
        records.some(record => record.recordType === 'psalm');
    },
  });
})();
