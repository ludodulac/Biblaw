/* Biblaw — documentary directory of historical teachers named in the Psalms. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {
    entries: null, loading: null, current: null, lastScroll: 0,
    lastLink: null, requestId: 0, openPsalm: null, corpusLoading: null,
    recordsReady: false
  };
  const archangel = value => ({
    michael: 'Michaël', gabriel: 'Gabriel',
    raphael: 'Raphaël', ouriel: 'Ouriel'
  })[value] || value || '';

  function status(message) {
    $('mastersStatus').textContent = message || '';
    $('mastersStatus').hidden = !message;
  }
  function toTop() { window.scrollTo({top: 0, behavior: 'instant'}); }
  function count(value, noun) {
    return value + ' ' + noun + (value > 1 ? 's' : '');
  }
  function element(tag, className, content) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined) node.textContent = content;
    return node;
  }
  function masterButton(entry) {
    const button = element('button', 'faq-question-item masters-person');
    button.type = 'button';
    const content = element('span', 'faq-question-title');
    content.append(element('strong', 'masters-person-name', entry.label));
    content.append(element('small', 'masters-person-count',
      entry.verseCount ? count(entry.psalmCount, 'psaume') + ' · ' +
        count(entry.verseCount, 'verset') : 'Aucune mention explicite trouvée'));
    button.append(content, element('span', 'faq-chevron', '›'));
    button.addEventListener('click', () => showMaster(entry));
    return button;
  }
  function directory() {
    state.current = null;
    ++state.requestId;
    $('mastersDirectory').hidden = false;
    $('mastersDetail').hidden = true;
    const query = $('mastersFilter').value.trim().normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const shown = state.entries.filter(entry =>
      entry.label.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .toLowerCase().includes(query));
    $('mastersCount').textContent = count(shown.length, 'maître') +
      ' répertorié' + (shown.length > 1 ? 's' : '') + '.';
    const list = $('mastersList');
    list.replaceChildren();
    for (const entry of shown) list.append(masterButton(entry));
    if (!shown.length) list.append(element('p', 'masters-empty',
      'Aucun maître pour cette recherche.'));
  }
  async function openVerse(source, verse, button) {
    state.lastLink = button;
    state.lastScroll = window.scrollY;
    const request = state.requestId;
    try {
      if (typeof state.openPsalm !== 'function')
        throw Error('Le lecteur des psaumes est indisponible.');
      if (!state.recordsReady) {
        status('Chargement du psaume…');
        if (!state.corpusLoading || !await state.corpusLoading())
          throw Error('Impossible de charger le corpus des psaumes.');
      }
      if (request !== state.requestId || $('mastersLibrary').hidden) return;
      status('');
      state.openPsalm({recordId: source.recordId, verses: [verse.number]});
    } catch (error) {
      if (request === state.requestId && !$('mastersLibrary').hidden)
        status(error.message || 'Impossible d’ouvrir ce psaume.');
      console.error(error);
    }
  }
  function verseCard(source, verse) {
    const row = element('div', 'masters-verse');
    row.append(element('p', 'masters-excerpt', '« ' + verse.excerpt + ' »'));
    const link = element('button', 'faq-psalm-link masters-reference',
      'Lire le psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ', verset ' + verse.number);
    link.type = 'button';
    link.addEventListener('click', () => openVerse(source, verse, link));
    row.append(link);
    return row;
  }
  function sourceCard(source) {
    const card = element('section', 'masters-source');
    card.append(element('h4', 'masters-source-name',
      'Psaume ' + source.psalm + ' de ' + archangel(source.archangel) +
      ' · Livre ' + source.book));
    const [first, ...others] = source.verses;
    card.append(verseCard(source, first));
    if (others.length) {
      const more = element('details', 'masters-more');
      more.append(element('summary', '', 'Voir ' + count(others.length, 'autre verset') +
        ' de ce psaume'));
      const list = element('div', 'masters-more-list');
      more.append(list);
      more.addEventListener('toggle', () => {
        if (more.open && !list.childElementCount) {
          for (const verse of others) list.append(verseCard(source, verse));
        }
      });
      card.append(more);
    }
    return card;
  }
  function showMaster(entry) {
    state.lastScroll = window.scrollY;
    state.current = entry;
    ++state.requestId;
    $('mastersDirectory').hidden = true;
    $('mastersDetail').hidden = false;
    $('masterName').textContent = entry.label;
    $('mastersSummary').textContent = entry.verseCount ?
      'Le nom de ' + entry.label + ' apparaît dans ' +
      count(entry.psalmCount, 'psaume') + ' (' +
      count(entry.verseCount, 'verset') + '). Chaque extrait renvoie directement au texte.' :
      'Aucune mention explicite de ce nom n’a été trouvée dans les 1 158 psaumes examinés.';
    const list = $('mastersReferences');
    list.replaceChildren();
    for (const source of entry.sources) list.append(sourceCard(source));
    toTop();
    $('masterName').focus({preventScroll: true});
  }
  async function load() {
    if (state.entries) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/masters-public.json?v=001').then(async response => {
      if (!response.ok) throw Error('Répertoire des maîtres indisponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || data.psalmCount !== 1158 ||
        !Array.isArray(data.entries) || data.entries.length < 4)
        throw Error('Répertoire des maîtres incomplet.');
      state.entries = data.entries;
      $('mastersMethod').textContent = data.method;
      return true;
    }).catch(error => {
      status(error.message || 'Erreur de chargement.');
      console.error(error);
      return false;
    }).finally(() => { state.loading = null; });
    return state.loading;
  }
  async function open() {
    const token = ++state.requestId;
    $('mastersLibrary').hidden = false;
    $('mastersDirectory').hidden = false;
    $('mastersDetail').hidden = true;
    document.body.classList.add('view-masters');
    $('mastersToggle').setAttribute('aria-expanded', 'true');
    status('Recherche dans les psaumes…');
    toTop();
    const ready = await load();
    if (token !== state.requestId || $('mastersLibrary').hidden) return;
    if (ready) {
      status('');
      directory();
    }
  }
  function close() {
    ++state.requestId;
    state.current = null;
    $('mastersLibrary').hidden = true;
    document.body.classList.remove('view-masters');
    $('mastersToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      directory();
      window.scrollTo({top: state.lastScroll, behavior: 'instant'});
    } else {
      close();
      toTop();
      $('mastersToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('mastersLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  $('mastersBack').addEventListener('click', back);
  $('mastersFilter').addEventListener('input', () => {
    if (state.entries) directory();
  });
  globalThis.BiblawMasters = Object.freeze({
    open, close, restoreAfterPsalm,
    setCorpusLoading(callback) { state.corpusLoading = callback; },
    setOpenPsalm(callback) { state.openPsalm = callback; },
    setRecords(records) {
      state.recordsReady = Array.isArray(records) && records.some(r => r.recordType === 'psalm');
    }
  });
})();