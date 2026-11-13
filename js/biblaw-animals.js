/* Biblaw — Animals in the Psalms. Editorial statements and links come
   from a verified, public projection of the canonical corpus. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {
    entries: [], loading: null, category: null, current: null,
    openPsalm: null, corpusLoading: null, records: new Map(),
    recordsReady: false, requestId: 0, lastLink: null,
    lastScroll: 0, indexScroll: 0
  };
  const archangel = name => ({
    michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël',
    ouriel: 'Ouriel'
  }[name] || name || '');
  const titles = {
    totem: 'Les animaux totems',
    other: 'Autres animaux'
  };
  function status(message) {
    const node = $('animalsStatus');
    node.textContent = message || '';
    node.hidden = !message;
  }
  function scrollTop() { window.scrollTo({top: 0, behavior: 'instant'}); }
  function validReference(ref) {
    const record = state.records.get(ref.recordId);
    return Boolean(record && record.recordType === 'psalm' &&
      record.archangel === ref.archangel && Number(record.number) === Number(ref.number) &&
      ref.verses.every(n => record.verses.some(v => Number(v.number) === Number(n))));
  }
  function refLabel(ref) {
    return 'Psaume ' + ref.number + ' de ' + archangel(ref.archangel) +
      ', verset' + (ref.verses.length > 1 ? 's ' : ' ') + ref.verses.join(', ');
  }
  async function openReference(ref, button) {
    if (typeof state.openPsalm !== 'function') {
      status('Le lecteur des psaumes est indisponible.'); return;
    }
    const id = state.requestId;
    const current = state.current;
    state.lastLink = button;
    state.lastScroll = window.scrollY;
    try {
      if (!state.recordsReady) {
        status('Chargement du corpus pour ouvrir le psaume…');
        if (!state.corpusLoading || !await state.corpusLoading())
          throw new Error('Corpus indisponible. Veuillez réessayer.');
      }
      if (id !== state.requestId || current !== state.current || $('animalsLibrary').hidden)
        return;
      if (!validReference(ref)) throw new Error('La référence du psaume n’est pas disponible.');
      status('');
      state.openPsalm(ref);
    } catch (error) {
      if (id === state.requestId && !$('animalsLibrary').hidden)
        status(error?.message || 'Impossible d’ouvrir le psaume.');
      console.error(error);
    }
  }
  function appendRef(container, ref) {
    const link = document.createElement('button');
    link.type = 'button';
    link.className = 'faq-psalm-link animals-reference';
    link.textContent = refLabel(ref);
    link.title = 'Lire les versets dans le psaume';
    const valid = !state.recordsReady || validReference(ref);
    link.disabled = !valid;
    if (valid) link.addEventListener('click', () => openReference(ref, link));
    container.append(link);
  }
  function appendReferenceList(parent, references) {
    const list = document.createElement('div');
    list.className = 'animals-reference-list';
    references.forEach(ref => appendRef(list, ref));
    parent.append(list);
  }
  function hideViews() {
    $('animalsFamilies').hidden = true;
    $('animalsDirectory').hidden = true;
    $('animalsAnswer').hidden = true;
  }
  function makeNavigationButton(name, action) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'faq-question-item';
    const label = document.createElement('span');
    label.className = 'faq-question-title';
    label.textContent = name;
    const arrow = document.createElement('span');
    arrow.className = 'faq-chevron';
    arrow.textContent = '›';
    arrow.setAttribute('aria-hidden', 'true');
    button.append(label, arrow);
    button.addEventListener('click', action);
    return button;
  }
  function renderFamilies() {
    state.category = null;
    state.current = null;
    state.requestId++;
    hideViews();
    $('animalsFamilies').hidden = false;
    $('animalsTitle').textContent = 'Les animaux dans la Bible';
    $('animalsFamilyButtons').replaceChildren();
    for (const category of ['totem', 'other']) {
      const count = state.entries.filter(e => e.category === category).length;
      $('animalsFamilyButtons').append(makeNavigationButton(
        titles[category] + ' (' + count + ')',
        () => renderDirectory(category)
      ));
    }
    $('animalsExplanation').textContent =
      'Les animaux totems sont ceux que les psaumes donnent en exemple. ' +
      '« Autres animaux » rassemble les comparaisons à ne pas imiter et les simples mentions ' +
      'qui ne présentent pas un comportement comme modèle. Ce classement ne juge pas les animaux.';
    status(state.loading && !state.entries.length ? 'Chargement des animaux…' : '');
    scrollTop();
  }
  function renderDirectory(category) {
    state.category = category;
    state.current = null;
    state.requestId++;
    hideViews();
    $('animalsDirectory').hidden = false;
    $('animalsTitle').textContent = titles[category];
    $('animalsDirectoryTitle').textContent = titles[category];
    const list = $('animalsList');
    list.replaceChildren();
    const selected = state.entries.filter(entry => entry.category === category);
    for (const entry of selected) {
      list.append(makeNavigationButton(entry.label, () => renderAnswer(entry)));
    }
    $('animalsDirectoryCount').textContent =
      selected.length + ' entrées, classées par ordre alphabétique.';
    status('');
    scrollTop();
  }
  function renderAnswer(entry) {
    state.indexScroll = window.scrollY;
    state.current = entry;
    state.requestId++;
    hideViews();
    $('animalsAnswer').hidden = false;
    $('animalsTitle').textContent = titles[entry.category];
    $('animalAnswerTitle').textContent = entry.label;
    $('animalAnswerText').textContent = entry.summary;
    $('animalReferences').replaceChildren();
    appendReferenceList($('animalReferences'), entry.sources);
    const details = $('animalAllMentions');
    const total = entry.occurrences.reduce((count, ref) => count + ref.verses.length, 0);
    $('animalAllMentionsLabel').textContent =
      'Toutes les mentions explicites dans les psaumes (' + total + ' versets)';
    details.open = false;
    $('animalAllMentionsList').replaceChildren();
    details.ontoggle = () => {
      if (details.open && !$('animalAllMentionsList').childElementCount)
        appendReferenceList($('animalAllMentionsList'), entry.occurrences);
    };
    scrollTop();
    $('animalAnswerTitle').focus({preventScroll: true});
  }
  async function load() {
    if (state.entries.length) return true;
    if (state.loading) return state.loading;
    state.loading = fetch('data/animals-public.json?v=001').then(async response => {
      if (!response.ok) throw new Error('Répertoire des animaux non disponible.');
      const data = await response.json();
      if (data.schemaVersion !== 1 || !Array.isArray(data.entries) ||
          data.psalmCount !== 1158) throw new Error('Répertoire des animaux invalide.');
      state.entries = data.entries;
      return true;
    }).catch(error => {
      status(error?.message || 'Impossible de charger les animaux.');
      console.error(error);
      return false;
    }).finally(() => { state.loading = null; });
    return state.loading;
  }
  async function open() {
    const id = ++state.requestId;
    $('animalsLibrary').hidden = false;
    document.body.classList.add('view-animals');
    $('animalsToggle').setAttribute('aria-expanded', 'true');
    renderFamilies();
    const ready = await load();
    if (id > state.requestId || $('animalsLibrary').hidden) return;
    if (ready) renderFamilies();
    else status('Impossible de charger les animaux. Réessayez en rouvrant cette rubrique.');
  }
  function close() {
    state.requestId++;
    state.current = null;
    state.category = null;
    $('animalsLibrary').hidden = true;
    document.body.classList.remove('view-animals');
    $('animalsToggle').setAttribute('aria-expanded', 'false');
  }
  function back() {
    if (state.current) {
      const category = state.category;
      renderDirectory(category);
      window.scrollTo({top: state.indexScroll, behavior: 'instant'});
    } else if (state.category) {
      renderFamilies();
    } else {
      close();
      scrollTop();
      $('animalsToggle').focus({preventScroll: true});
    }
  }
  function restoreAfterPsalm() {
    if ($('animalsLibrary').hidden || !state.current) return;
    window.scrollTo({top: state.lastScroll, behavior: 'instant'});
    state.lastLink?.focus({preventScroll: true});
  }
  function download() {
    const entry = state.current;
    if (!entry) return;
    const citations = entry.sources.map(ref => refLabel(ref)).join('\n');
    try {
      BiblawPDF.download({
        recordType: 'faq', id: 'animal-' + entry.id,
        title: entry.label,
        text: entry.summary + '\n\nVersets à l’appui :\n' + citations
      });
      status('');
    } catch (error) {
      status('Impossible de créer le PDF : ' + error.message);
    }
  }
  $('animalsBack').addEventListener('click', back);
  $('animalPdf').addEventListener('click', download);
  $('animalPrint').addEventListener('click', () => window.print());
  globalThis.BiblawAnimals = Object.freeze({
    open, close, restoreAfterPsalm,
    setRecords(records) {
      state.records = new Map(records.map(record => [record.id, record]));
      state.recordsReady = true;
    },
    setCorpusLoading(loader) { state.corpusLoading = loader; },
    setOpenPsalm(callback) { state.openPsalm = callback; }
  });
})();
