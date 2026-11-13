/* Biblaw — read-only number mentions documented in canonical Psalm verses. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {
    entries: [], numberTerms: [], loading: null, current: null,
    records: new Map(), recordsReady: false, corpusLoading: null, openPsalm: null,
    lastLink: null, lastScroll: 0, indexScroll: 0, requestId: 0
  };
  const archangel = name => ({
    michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel'
  }[name] || name || '');
  function status(message) {
    $('numbersStatus').textContent = message || '';
    $('numbersStatus').hidden = !message;
  }
  function refLabel(ref) {
    return 'Psaume ' + ref.psalm + ' de ' + archangel(ref.archangel) +
      ', verset ' + ref.verse;
  }
  function validRef(ref) {
    const p = state.records.get(ref.recordId);
    return Boolean(p && p.recordType === 'psalm' && p.archangel === ref.archangel &&
      Number(p.number) === Number(ref.psalm) &&
      p.verses.some(v => Number(v.number) === Number(ref.verse)));
  }
  async function openRef(ref, link) {
    const request = state.requestId, current = state.current;
    state.lastLink = link;
    state.lastScroll = window.scrollY;
    try {
      if (typeof state.openPsalm !== 'function')
        throw new Error('Le lecteur des psaumes est indisponible.');
      if (!state.recordsReady) {
        status('Chargement du corpus…');
        if (!state.corpusLoading || !await state.corpusLoading())
          throw new Error('Impossible de charger les psaumes.');
      }
      if (request !== state.requestId || current !== state.current ||
          $('numbersLibrary').hidden) return;
      if (!validRef(ref)) throw new Error('Référence introuvable dans les psaumes.');
      status('');
      state.openPsalm({recordId:ref.recordId, verses:[ref.verse]});
    } catch (error) {
      if (request === state.requestId && !$('numbersLibrary').hidden)
        status(error?.message || 'Impossible d’ouvrir le verset.');
      console.error(error);
    }
  }
  function referenceButton(ref) {
    const link = document.createElement('button');
    link.type = 'button';
    link.className = 'faq-psalm-link numbers-reference';
    link.textContent = refLabel(ref);
    link.title = 'Lire le verset dans le psaume';
    link.addEventListener('click', () => openRef(ref, link));
    return link;
  }
  function numberRow(entry) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'faq-question-item';
    const name = document.createElement('span');
    name.className = 'faq-question-title';
    const count = entry.references.length;
    name.textContent = entry.label + ' — ' + count + ' verset' + (count > 1 ? 's' : '') +
      (entry.durationCount ? ' · ' + entry.durationCount + ' mentions de durée/fois' : '');
    const arrow = document.createElement('span');
    arrow.className = 'faq-chevron';
    arrow.textContent = '›';
    arrow.setAttribute('aria-hidden','true');
    btn.append(name, arrow);
    btn.addEventListener('click', () => renderDetail(entry));
    return btn;
  }
  function renderDirectory() {
    state.current = null;
    state.requestId++;
    $('numbersDetail').hidden = true;
    $('numbersDirectory').hidden = false;
    const value = $('numbersFilter').value.trim();
    const onlyDuration = $('numbersDurationFilter').checked;
    const shown = state.entries.filter(e =>
      (!value || String(e.value).includes(value)) &&
      (!onlyDuration || e.durationCount > 0));
    $('numbersCount').textContent = shown.length + ' nombres trouvés sur ' +
      state.entries.length + ' · 1 158 psaumes examinés.';
    const list = $('numbersList');
    list.replaceChildren();
    for (const item of shown) list.append(numberRow(item));
    if (!shown.length) {
      const empty = document.createElement('p');
      empty.textContent = 'Aucun nombre pour cette recherche.';
      list.append(empty);
    }
  }
  function renderDetail(entry) {
    state.indexScroll = window.scrollY;
    state.current = entry;
    state.requestId++;
    $('numbersDirectory').hidden = true;
    $('numbersDetail').hidden = false;
    $('numberTitle').textContent = entry.value === null ? 'Les chiffres et les nombres dans les psaumes' : 'Nombre ' + entry.value;
    $('numberSummary').textContent = entry.summary;
    const sampleList = $('numberExamples');
    sampleList.replaceChildren();
    const examples = entry.examples || [];
    $('numberExamplesHeading').hidden = !examples.length;
    for (const sample of examples) {
      const block = document.createElement('div');
      block.className = 'numbers-example';
      const excerpt = document.createElement('p');
      excerpt.textContent = sample.excerpt;
      block.append(excerpt, referenceButton(sample));
      sampleList.append(block);
    }
    const details = $('numberAllMentions');
    $('numberAllMentionsList').replaceChildren();
    details.open = false;
    details.hidden = !entry.references.length;
    $('numberAllMentionsLabel').textContent = 'Toutes les références (' +
      entry.references.length + ' versets)';
    details.ontoggle = () => {
      if (!details.open || $('numberAllMentionsList').childElementCount) return;
      const target = $('numberAllMentionsList');
      for (const ref of entry.references) target.append(referenceButton(ref));
    };
    window.scrollTo({top:0,behavior:'instant'});
    $('numberTitle').focus({preventScroll:true});
  }
  async function load() {
    if (state.entries.length) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/numbers-public.json?v=001').then(async response => {
      if (!response.ok) throw new Error('Répertoire des nombres indisponible.');
      const result = await response.json();
      if (result.schemaVersion !== 1 || result.psalmCount !== 1158 ||
          !Array.isArray(result.entries) || !result.entries.length ||
          !Array.isArray(result.numberTerms))
        throw new Error('Répertoire des nombres incomplet.');
      state.entries = result.entries;
      state.numberTerms = result.numberTerms;
      $('numbersMethod').textContent = result.method;
      return true;
    }).catch(error => {
      status(error?.message || 'Chargement impossible.');
      console.error(error);
      return false;
    }).finally(() => {state.loading = null;});
    return state.loading;
  }
  async function open() {
    state.requestId++;
    $('numbersLibrary').hidden = false;
    document.body.classList.add('view-numbers');
    $('numbersTab').classList.add('active');
    $('numbersTab').setAttribute('aria-expanded', 'true');
    $('numbersDirectory').hidden = false;
    $('numbersDetail').hidden = true;
    status('Recherche des chiffres et des nombres…');
    const ready = await load();
    if ($('numbersLibrary').hidden) return;
    status(ready ? '' : 'Impossible de charger les chiffres et nombres.');
    if (ready) renderDirectory();
    window.scrollTo({top:0,behavior:'instant'});
  }
  function close() {
    state.requestId++;
    state.current = null;
    $('numbersLibrary').hidden = true;
    document.body.classList.remove('view-numbers');
    $('numbersTab').classList.remove('active');
    $('numbersTab').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      renderDirectory();
      window.scrollTo({top:state.indexScroll,behavior:'instant'});
    } else {
      close();
      window.scrollTo({top:0,behavior:'instant'});
      $('numbersTab').focus({preventScroll:true});
    }
  }
  function restoreAfterPsalm() {
    if ($('numbersLibrary').hidden || !state.current) return;
    window.scrollTo({top:state.lastScroll,behavior:'instant'});
    state.lastLink?.focus({preventScroll:true});
  }
  function download() {
    const entry = state.current;
    if (!entry) return;
    const examples = (entry.examples || []).map(e => e.excerpt + '\n' + refLabel(e)).join('\n\n');
    const references = entry.references.map(refLabel).join('\n');
    try {
      BiblawPDF.download({
        recordType:'faq',
        id:'biblaw-number-'+entry.value,
        title:entry.value === null ? 'Chiffres et nombres' : 'Nombre '+entry.label,
        text:entry.summary+'\n\nExemples relevés :\n'+examples+
          '\n\nToutes les références :\n'+references
      });
      status('');
    } catch (error) {
      status('Téléchargement PDF indisponible : '+error.message);
    }
  }
  $('numbersBack').addEventListener('click', back);
  $('numbersFilter').addEventListener('input', renderDirectory);
  $('numbersDurationFilter').addEventListener('change', renderDirectory);
  $('numberPdf').addEventListener('click', download);
  $('numberPrint').addEventListener('click', () => window.print());
  globalThis.BiblawNumbers = Object.freeze({
    open, close, restoreAfterPsalm,
    setCorpusLoading(callback) {state.corpusLoading = callback;},
    setOpenPsalm(callback) {state.openPsalm = callback;},
    setRecords(records) {
      state.records = new Map(records.map(r => [r.id, r]));
      state.recordsReady = true;
    }
  });
})();