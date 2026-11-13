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
  function referenceItem(ref) {
    const item = document.createElement('div');
    item.className = 'numbers-ref-item';
    if (ref.title) {
      const phrase = document.createElement('button');
      phrase.type = 'button';
      phrase.className = 'numbers-ref-phrase';
      phrase.textContent = ref.title;
      phrase.title = 'Ouvrir le verset cité';
      phrase.addEventListener('click', () => openRef(ref, phrase));
      item.append(phrase);
    }
    // Keep the familiar source label as an independent clickable link.
    item.append(referenceButton(ref));
    return item;
  }
  function numberRow(entry) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'faq-question-item numbers-number-button';
    const name = document.createElement('span');
    name.className = 'faq-question-title';
    const count = entry.references.length;
    const number = document.createElement('strong');
    number.className = 'numbers-number';
    number.textContent = entry.label;
    const title = document.createElement('span');
    title.className = 'numbers-number-title';
    title.textContent = entry.title || 'Enseignements et pratiques';
    name.append(number, title);
    const detail = document.createElement('small');
    detail.className = 'numbers-number-context';
    detail.textContent = count + ' verset' + (count > 1 ? 's' : '') +
      (entry.durationCount ? ' · ' + entry.durationCount + ' passages liés à des durées ou cycles' : '');
    name.append(detail);
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
    $('numbersCount').textContent = shown.length + ' nombres avec un contexte d’enseignement sur ' +
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
    $('numberTitle').textContent = 'Nombre ' + entry.value;
    $('numberSummary').textContent = entry.summary || '';
    $('numberSummary').hidden = !entry.summary;

    // ONE reference list, organised by topic. No second "Toutes les
    // références" block, no "Quelques passages" repeating the same Psalms.
    // The public projection guarantees that each verse belongs to one topic.
    const topicList = $('numberTopicGroups');
    topicList.hidden = false;
    topicList.replaceChildren();
    for (const topic of entry.topics || []) {
      if (topic.references.length === 1) {
        const single = document.createElement('div');
        single.className = 'numbers-topic numbers-topic-single';
        const ref = topic.references[0];
        const isPhraseTopic = !topic.key.startsWith('extrait-');
        single.append(referenceItem(isPhraseTopic ?
          {...ref, title: topic.label} : ref));
        topicList.append(single);
        continue;
      }
      const details = document.createElement('details');
      details.className = 'numbers-topic';
      const heading = document.createElement('summary');
      const name = document.createElement('strong');
      name.textContent = topic.label;
      const count = document.createElement('span');
      count.className = 'numbers-topic-count';
      count.textContent = topic.references.length + ' verset' +
        (topic.references.length > 1 ? 's' : '');
      heading.append(name, count);
      details.append(heading);
      if (topic.summary) {
        const info = document.createElement('p');
        info.className = 'numbers-topic-summary';
        info.textContent = topic.summary;
        details.append(info);
      }
      const refs = document.createElement('div');
      refs.className = 'numbers-references';
      details.append(refs);
      details.ontoggle = () => {
        if (details.open && !refs.childElementCount)
          for (const ref of topic.references) refs.append(referenceItem(ref));
      };
      topicList.append(details);
    }
    window.scrollTo({top:0,behavior:'instant'});
    $('numberTitle').focus({preventScroll:true});
  }
  async function load() {
    if (state.entries.length) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/numbers-public.json?v=005').then(async response => {
      if (!response.ok) throw new Error('Répertoire des nombres indisponible.');
      const result = await response.json();
      if (result.schemaVersion !== 1 || result.psalmCount !== 1158 ||
          !Array.isArray(result.entries) || !result.entries.length ||
          !Array.isArray(result.numberTerms))
        throw new Error('Répertoire des nombres incomplet.');
      state.entries = result.entries;
      state.numberTerms = result.numberTerms;
      $('numbersTermsDetails').hidden = !result.numberTerms.length;
      $('numbersTermsLabel').textContent = 'Versets employant les mots « nombre », « chiffre », etc. (' +
        result.numberTerms.length + ')';
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
    $('numbersToggle').setAttribute('aria-expanded', 'true');
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
    $('numbersToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      renderDirectory();
      window.scrollTo({top:state.indexScroll,behavior:'instant'});
    } else {
      close();
      window.scrollTo({top:0,behavior:'instant'});
      $('numbersToggle').focus({preventScroll:true});
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
    // The PDF follows the exact same unique partition as the page.
    // Each verse is written once, under just one subject/phrase.
    const topics = (entry.topics || []).map(group => {
      if (group.references.length === 1) {
        const ref = group.references[0];
        const label = group.key.startsWith('extrait-') ? ref.title : group.label;
        return label + '\n' + refLabel(ref);
      }
      return group.label + '\n' + group.references.map(ref =>
        ref.title + '\n' + refLabel(ref)).join('\n\n');
    }).join('\n\n');
    try {
      BiblawPDF.download({
        recordType:'faq',
        id:'biblaw-number-'+entry.value,
        title:'Nombre '+entry.label,
        text:(entry.summary ? entry.summary+'\n\n' : '') +
          'Sujets et versets :\n'+topics
      });
      status('');
    } catch (error) {
      status('Téléchargement PDF indisponible : '+error.message);
    }
  }
  $('numbersTermsDetails').ontoggle = () => {
    if (!$('numbersTermsDetails').open || $('numbersTermsList').childElementCount) return;
    for (const ref of state.numberTerms) $('numbersTermsList').append(referenceButton(ref));
  };
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