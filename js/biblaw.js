(() => {
  const $ = id => document.getElementById(id);
  const state = { mode: 'themes', records: [], themes: [], themeDirectory: [], theme: null, sense: '', active: null };
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/\s+/g, ' ').trim();
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const text = r => [r.title, r.summary, r.text, ...(r.verses || []).map(v => v.text), ...(r.conceptIds || [])].filter(Boolean).join(' ');
  const selectedTypes = () => new Set([...document.querySelectorAll('[name=sourceType]:checked')].map(x => x.value));
  const archangelName = value => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[value] || value || '');
  const label = r => r.recordType === 'psalm' ? `Psaume ${r.number} · ${archangelName(r.archangel)}` : r.recordType === 'master-prayer' ? `Prière ${r.number} · ${archangelName(r.archangel)}` : `Note · ${archangelName(r.archangel)}`;
  const importanceLabel = value => ({ central: 'Central', important: 'Important', related: 'Lié' }[value] || 'Indexé');

  async function load() {
    try {
      const [catalog, directory] = await Promise.all([
        fetch('data/catalog.json').then(r => { if (!r.ok) throw Error('catalog'); return r.json(); }),
        fetch('data/thematic-index/theme-directory.json').then(r => { if (!r.ok) throw Error('theme-directory'); return r.json(); })
      ]);
      const loaded = await Promise.all(catalog.records.map(path => fetch(path).then(r => { if (!r.ok) throw Error(path); return r.json(); })));
      state.themes = loaded.filter(r => r.recordType === 'theme');
      state.theme = state.themes.find(r => r.id === 'theme-chouette') || null;
      state.themeDirectory = directory.themes || [];
      state.records = loaded.filter(r => r.recordType && r.recordType !== 'theme' && r.recordType !== 'book');
      const prayers = new Map(state.records.filter(r => r.recordType === 'master-prayer').map(r => [r.appliesToPsalmId, r]));
      state.records.filter(r => r.recordType === 'psalm').forEach(r => { if (prayers.has(r.id)) r.attachedPrayer = prayers.get(r.id); });
      const psalms = state.records.filter(r => r.recordType === 'psalm'), verses = psalms.reduce((n, r) => n + (r.verses || []).length, 0);
      const prayerCount = state.records.filter(r => r.recordType === 'master-prayer').length;
      const noteCount = state.records.filter(r => r.recordType === 'note').length + psalms.reduce((n, r) => n + (r.notes || []).length, 0);
      $('corpusStats').textContent = `${psalms.length} psaumes · ${verses} versets · ${prayerCount} prières · ${noteCount} notes reliées`;
      themes(); search();
    } catch (error) {
      console.error(error);
      $('results').innerHTML = '<div class="empty">Le corpus ne peut pas être chargé. Ouvrez Biblaw depuis son adresse web.</div>';
    }
  }

  function matches(query) {
    const terms = norm(query).split(' ').filter(Boolean), allowed = selectedTypes(), a = $('archangelFilter').value;
    return state.records
      .filter(r => allowed.has(type(r)) && (!a || r.archangel === a))
      .map(record => ({ record, score: terms.filter(t => norm(text(record)).includes(t)).length / Math.max(1, terms.length) }))
      .filter(x => x.score > 0);
  }

  function findIndexedTheme(query) {
    const q = norm(query);
    if (!q) return null;
    const exact = state.themeDirectory.find(t => q === norm(t.label) || q === norm(t.id));
    if (exact) return exact;
    const candidates = state.themeDirectory.filter(t => norm(t.label).includes(q) || q.includes(norm(t.label)));
    return candidates.sort((a, b) => Math.abs(norm(a.label).length - q.length) - Math.abs(norm(b.label).length - q.length))[0] || null;
  }

  function thematicItems(theme) {
    const allowed = selectedTypes();
    if (!allowed.has('psalm')) return [];
    const a = $('archangelFilter').value;
    const byId = new Map(state.records.filter(r => r.recordType === 'psalm').map(r => [r.id, r]));
    return (theme.occurrences || [])
      .filter(o => !a || o.archangel === a)
      .map(o => ({ record: byId.get(o.recordId), score: o.score || 1, thematic: o }))
      .filter(x => x.record);
  }

  function search() {
    const query = $('query').value.trim();
    if (!query) return render([]);

    const owl = state.theme && [state.theme.label, ...(state.theme.searchTerms || []), ...(state.theme.subthemes || []).map(x => x.label)].some(t => norm(query).includes(norm(t)) || norm(t).includes(norm(query)));
    $('ambiguityPanel').hidden = !(state.mode === 'themes' && owl && state.theme?.senses?.length);
    if (owl && state.mode === 'themes' && state.theme) {
      senses();
      const ids = new Set((state.theme.evidence || []).map(e => e.recordId));
      let items = state.records.filter(r => ids.has(r.id)).map(record => ({ record, score: 1 }));
      if (['owl-animal', 'owl-symbolic-vision'].includes(state.sense)) items = items.filter(x => x.record.id === 'michael-psalm-026');
      if (state.sense === 'owl-michael-totem') items = items.filter(x => x.record.recordType === 'note');
      return render(items);
    }

    if (state.mode === 'themes') {
      const indexed = findIndexedTheme(query);
      if (indexed) return render(thematicItems(indexed), indexed);
    }
    render(matches(query).sort((a, b) => b.score - a.score));
  }

  function senses() {
    if (!state.theme?.senses) return;
    $('senseChoices').innerHTML = state.theme.senses.map(s => `<button class="sense-button ${state.sense === s.id ? 'selected' : ''}" data-sense="${esc(s.id)}"><strong>${esc(s.label)}</strong><span>${esc(s.definition)}</span></button>`).join('');
    document.querySelectorAll('[data-sense]').forEach(b => b.onclick = () => { state.sense = b.dataset.sense; senses(); search(); });
  }

  function summary(r) {
    return r.recordType === 'psalm'
      ? (r.id === 'michael-psalm-026' && state.theme ? state.theme.subthemes.map(x => x.summary).join(' ') : (r.verses || []).slice(0, 2).map(v => v.text).join(' '))
      : r.summary || (r.text || '').slice(0, 280);
  }

  function recordPages(r) {
    return r.source?.pdfPages || r.source?.printedPages || (r.source?.printedPage ? [r.source.printedPage] : []);
  }

  function render(items, indexedTheme = null) {
    $('resultCount').textContent = indexedTheme
      ? `${items.length} psaume${items.length > 1 ? 's' : ''} indexé${items.length > 1 ? 's' : ''} · ${indexedTheme.label}`
      : `${items.length} résultat${items.length > 1 ? 's' : ''}`;
    if (!items.length) {
      $('results').innerHTML = '<div class="empty">Aucun passage indexé ne correspond encore à cette recherche et aux filtres sélectionnés.</div>';
      return;
    }
    $('results').innerHTML = items.map(({ record: r, thematic }) => {
      const tags = thematic
        ? [indexedTheme?.label, ...(thematic.directness ? [thematic.directness === 'symbolic' ? 'Symbolique' : 'Direct'] : [])].filter(Boolean)
        : (r.id === 'michael-psalm-026' && state.theme ? state.theme.subthemes.map(x => x.label) : (r.conceptIds || []));
      const pages = recordPages(r);
      const meta = thematic
        ? `${thematic.bookTitle || `Livre ${thematic.bookNumber}`} · ${thematic.verseNumbers?.length ? `verset${thematic.verseNumbers.length > 1 ? 's' : ''} ${thematic.verseNumbers.join(', ')}` : 'psaume entier'}`
        : (pages.length ? `Page${pages.length > 1 ? 's ' : ' '}${pages.join('–')}` : 'Référence structurée');
      const description = thematic?.teaching || summary(r);
      return `<article class="result-card"><div class="result-topline"><div><div class="result-doc">${esc(label(r))}</div><h3>${esc(r.title || (r.recordType === 'master-prayer' ? `Prière ${r.number}` : 'Note associée'))}</h3></div><strong class="score">${esc(thematic ? importanceLabel(thematic.importance) : 'Texte')}</strong></div><div class="result-meta">${esc(meta)}</div><p class="result-summary">${esc(description)}</p><div class="tags">${tags.slice(0, 6).map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div><div class="result-actions">${r.recordType === 'psalm' ? `<a class="secondary" href="Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf#page=${pages[0] || 1}" target="_blank">Voir dans le PDF</a>` : ''}<button class="primary" data-open="${esc(r.id)}">Consulter</button></div></article>`;
    }).join('');
    document.querySelectorAll('[data-open]').forEach(b => b.onclick = () => open(b.dataset.open));
  }

  function open(id) {
    const r = state.records.find(x => x.id === id);
    if (!r) return;
    state.active = r;
    $('dialogEyebrow').textContent = label(r);
    $('dialogTitle').textContent = r.title || (r.recordType === 'master-prayer' ? `Prière ${r.number}` : 'Note associée');
    if (r.recordType === 'psalm') {
      $('dialogContent').innerHTML = (r.verses || []).map(v => `<div class="verse"><div class="verse-number">${v.number}</div><div>${v.speakerId ? `<span class="speaker">${esc(v.speakerId.replaceAll('-', ' '))} · ${esc(v.speechRole || '')}</span>` : ''}${esc(v.text)}</div></div>`).join('') + (r.attachedPrayer ? `<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${esc(r.attachedPrayer.text)}</section>` : '');
    } else {
      $('dialogContent').innerHTML = `<div class="prayer-block">${esc(r.text || r.summary || '')}</div>`;
    }
    $('recordDialog').showModal();
  }

  function activeText() {
    const r = state.active;
    if (!r) return '';
    let out = `${r.title || `Prière ${r.number}`}\n\n`;
    out += r.verses ? r.verses.map(v => `${v.number}. ${v.text}`).join('\n\n') : r.text || r.summary || '';
    if (r.attachedPrayer) out += `\n\nPrière ${r.attachedPrayer.number}\n\n${r.attachedPrayer.text}`;
    return out;
  }

  function themes() {
    const entries = [...state.themeDirectory].sort((a, b) => a.label.localeCompare(b.label, 'fr', { sensitivity: 'base' }));
    $('indexCount').textContent = `${entries.length} thèmes indexés.`;
    $('themeDirectory').innerHTML = entries.map(x => `<button class="theme-chip theme-main" data-theme="${esc(x.label)}" title="${x.occurrenceCount} occurrence${x.occurrenceCount > 1 ? 's' : ''} indexée${x.occurrenceCount > 1 ? 's' : ''}">${esc(x.label)}</button>`).join('');
    document.querySelectorAll('[data-theme]').forEach(b => b.onclick = () => {
      $('query').value = b.dataset.theme;
      mode('themes');
      closeIndex();
      search();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  function openIndex() { $('indexPanel').hidden = false; $('indexBackdrop').hidden = false; $('indexToggle').setAttribute('aria-expanded', 'true'); document.body.classList.add('index-open'); }
  function closeIndex() { $('indexPanel').hidden = true; $('indexBackdrop').hidden = true; $('indexToggle').setAttribute('aria-expanded', 'false'); document.body.classList.remove('index-open'); }
  function mode(m) {
    state.mode = m;
    $('modeThemes').classList.toggle('active', m === 'themes');
    $('modeExact').classList.toggle('active', m === 'exact');
    $('modeHelp').textContent = m === 'themes' ? 'Retrouve les thèmes constitués éditorialement et les psaumes classés par importance.' : 'Recherche uniquement les mots ou la phrase dans les textes déjà extraits.';
    search();
  }

  $('searchButton').onclick = search;
  $('query').onkeydown = e => { if (e.key === 'Enter') search(); };
  $('archangelFilter').onchange = search;
  document.querySelectorAll('[name=sourceType]').forEach(x => x.onchange = search);
  $('modeThemes').onclick = () => mode('themes');
  $('modeExact').onclick = () => mode('exact');
  $('indexToggle').onclick = () => $('indexPanel').hidden ? openIndex() : closeIndex();
  $('closeIndex').onclick = closeIndex;
  $('indexBackdrop').onclick = closeIndex;
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('indexPanel').hidden) closeIndex(); });
  $('closeAmbiguity').onclick = () => { state.sense = ''; $('ambiguityPanel').hidden = true; render(matches($('query').value)); };
  $('closeDialog').onclick = () => $('recordDialog').close();
  $('printRecord').onclick = () => print();
  $('downloadRecord').onclick = () => {
    const blob = new Blob([activeText()], { type: 'text/plain;charset=utf-8' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${state.active?.id || 'biblaw'}.txt`;
    a.click();
    URL.revokeObjectURL(a.href);
  };
  load();
})();
