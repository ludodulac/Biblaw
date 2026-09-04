(() => {
  const $ = id => document.getElementById(id);
  const paths = [
    'data/corpus/michael/psalm-026.json', 'data/corpus/michael/psalm-105.json',
    'data/corpus/gabriel/psalm-112.json', 'data/corpus/gabriel/psalm-182.json',
    'data/corpus/raphael/psalm-104.json', 'data/corpus/ouriel/psalm-105.json',
    'data/prayers/michael-book-17-prayer-001.json', 'data/prayers/gabriel-book-18-prayer-001.json',
    'data/prayers/gabriel-book-26-prayer-066.json', 'data/prayers/raphael-book-19-prayer-003.json',
    'data/prayers/ouriel-book-20-prayer-002.json', 'data/notes/michael-psalm-143-note-002.json',
    'data/notes/michael-psalm-105-note-001.json', 'data/notes/gabriel-psalm-112-note-001.json',
    'data/notes/gabriel-psalm-182-note-001.json', 'data/notes/raphael-psalm-104-note-001.json',
    'data/themes/chouette.json'
  ];
  const state = { mode: 'themes', records: [], theme: null, sense: '', active: null };
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/\s+/g, ' ').trim();
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const text = r => [r.title, r.summary, r.text, ...(r.verses || []).map(v => v.text), ...(r.conceptIds || [])].filter(Boolean).join(' ');
  const selectedTypes = () => new Set([...document.querySelectorAll('[name=sourceType]:checked')].map(x => x.value));
  const label = r => r.recordType === 'psalm' ? `Psaume ${r.number} · ${r.archangel}` : r.recordType === 'master-prayer' ? `Prière ${r.number} · ${r.archangel}` : `Note · ${r.archangel}`;

  async function load() {
    try {
      const loaded = await Promise.all(paths.map(path => fetch(path).then(r => { if (!r.ok) throw Error(path); return r.json(); })));
      state.theme = loaded.find(r => r.id === 'theme-chouette'); state.records = loaded.filter(r => r.recordType);
      const prayers = new Map(state.records.filter(r => r.recordType === 'master-prayer').map(r => [r.appliesToPsalmId, r]));
      state.records.filter(r => r.recordType === 'psalm').forEach(r => { if (prayers.has(r.id)) r.attachedPrayer = prayers.get(r.id); });
      const psalms = state.records.filter(r => r.recordType === 'psalm'), verses = psalms.reduce((n, r) => n + (r.verses || []).length, 0);
      const prayerCount = state.records.filter(r => r.recordType === 'master-prayer').length;
      const noteCount = state.records.filter(r => r.recordType === 'note').length + psalms.reduce((n, r) => n + (r.notes || []).length, 0);
      $('corpusStats').textContent = `${psalms.length} psaumes pilotes · ${verses} versets · ${prayerCount} prières · ${noteCount} notes reliées`;
      themes(); search();
    } catch { $('results').innerHTML = '<div class="empty">Le corpus ne peut pas être chargé. Ouvrez Biblaw depuis son adresse web.</div>'; }
  }
  function matches(query) {
    const terms = norm(query).split(' ').filter(Boolean), allowed = selectedTypes(), a = $('archangelFilter').value;
    return state.records.filter(r => allowed.has(type(r)) && (!a || r.archangel === a)).map(record => ({ record, score: terms.filter(t => norm(text(record)).includes(t)).length / Math.max(1, terms.length) })).filter(x => x.score > 0);
  }
  function search() {
    const query = $('query').value.trim(); if (!query) return render([]);
    const owl = ['chouette', 'vision nocturne', 'imperfection'].some(t => norm(query).includes(norm(t)));
    $('ambiguityPanel').hidden = !(state.mode === 'themes' && owl && state.theme);
    if (owl && state.mode === 'themes') {
      senses(); const ids = new Set(state.theme.evidence.map(e => e.recordId)); let items = state.records.filter(r => ids.has(r.id)).map(record => ({ record, score: 1 }));
      if (['owl-animal', 'owl-symbolic-vision'].includes(state.sense)) items = items.filter(x => x.record.id === 'michael-psalm-026');
      if (state.sense === 'owl-michael-totem') items = items.filter(x => x.record.recordType === 'note'); return render(items);
    }
    render(matches(query).sort((a, b) => b.score - a.score));
  }
  function senses() {
    $('senseChoices').innerHTML = state.theme.senses.map(s => `<button class="sense-button ${state.sense === s.id ? 'selected' : ''}" data-sense="${esc(s.id)}"><strong>${esc(s.label)}</strong><span>${esc(s.definition)}</span></button>`).join('');
    document.querySelectorAll('[data-sense]').forEach(b => b.onclick = () => { state.sense = b.dataset.sense; senses(); search(); });
  }
  function summary(r) { return r.recordType === 'psalm' ? (r.id === 'michael-psalm-026' ? state.theme.subthemes.map(x => x.summary).join(' ') : r.verses.slice(0, 2).map(v => v.text).join(' ')) : r.summary || (r.text || '').slice(0, 280); }
  function render(items) {
    $('resultCount').textContent = `${items.length} résultat${items.length > 1 ? 's' : ''}`;
    if (!items.length) { $('results').innerHTML = '<div class="empty">Aucun passage indexé ne correspond encore à cette recherche.</div>'; return; }
    $('results').innerHTML = items.map(({ record: r }) => { const tags = r.id === 'michael-psalm-026' ? state.theme.subthemes.map(x => x.label) : (r.conceptIds || []), pages = r.source?.printedPages || (r.source?.printedPage ? [r.source.printedPage] : []); return `<article class="result-card"><div class="result-topline"><div><div class="result-doc">${esc(label(r))}</div><h3>${esc(r.title || (r.recordType === 'master-prayer' ? `Prière ${r.number}` : 'Note associée'))}</h3></div><strong class="score">Pilote</strong></div><div class="result-meta">${pages.length ? `Page${pages.length > 1 ? 's ' : ' '}${pages.join('–')}` : 'Référence structurée'}</div><p class="result-summary">${esc(summary(r))}</p><div class="tags">${tags.slice(0, 6).map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div><div class="result-actions">${r.recordType === 'psalm' ? `<a class="secondary" href="Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf#page=${pages[0] || 1}" target="_blank">Voir dans le PDF</a>` : ''}<button class="primary" data-open="${esc(r.id)}">Consulter</button></div></article>`; }).join('');
    document.querySelectorAll('[data-open]').forEach(b => b.onclick = () => open(b.dataset.open));
  }
  function open(id) {
    const r = state.records.find(x => x.id === id); if (!r) return; state.active = r; $('dialogEyebrow').textContent = label(r); $('dialogTitle').textContent = r.title || (r.recordType === 'master-prayer' ? `Prière ${r.number}` : 'Note associée');
    if (r.recordType === 'psalm') $('dialogContent').innerHTML = r.verses.map(v => `<div class="verse"><div class="verse-number">${v.number}</div><div>${v.speakerId ? `<span class="speaker">${esc(v.speakerId.replaceAll('-', ' '))} · ${esc(v.speechRole || '')}</span>` : ''}${esc(v.text)}</div></div>`).join('') + (r.attachedPrayer ? `<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${esc(r.attachedPrayer.text)}</section>` : '');
    else $('dialogContent').innerHTML = `<div class="prayer-block">${esc(r.text || r.summary || '')}</div>`; $('recordDialog').showModal();
  }
  function activeText() { const r = state.active; if (!r) return ''; let out = `${r.title || `Prière ${r.number}`}\n\n`; out += r.verses ? r.verses.map(v => `${v.number}. ${v.text}`).join('\n\n') : r.text || r.summary || ''; if (r.attachedPrayer) out += `\n\nPrière ${r.attachedPrayer.number}\n\n${r.attachedPrayer.text}`; return out; }
  function themes() { const labels = [state.theme.label, ...state.theme.subthemes.map(x => x.label)]; $('themeDirectory').innerHTML = labels.map(x => `<button class="theme-chip" data-theme="${esc(x)}">${esc(x)}</button>`).join(''); document.querySelectorAll('[data-theme]').forEach(b => b.onclick = () => { $('query').value = b.dataset.theme === state.theme.label ? 'chouette' : b.dataset.theme; $('themesPanel').hidden = true; search(); }); }
  function mode(m) { state.mode = m; $('modeThemes').classList.toggle('active', m === 'themes'); $('modeExact').classList.toggle('active', m === 'exact'); $('modeHelp').textContent = m === 'themes' ? 'Retrouve les sens, sous-thèmes et passages déjà reliés éditorialement.' : 'Recherche uniquement les mots ou la phrase dans les textes déjà extraits.'; search(); }
  $('searchButton').onclick = search; $('query').onkeydown = e => { if (e.key === 'Enter') search(); }; $('archangelFilter').onchange = search; document.querySelectorAll('[name=sourceType]').forEach(x => x.onchange = search);
  $('modeThemes').onclick = () => mode('themes'); $('modeExact').onclick = () => mode('exact'); $('themesToggle').onclick = () => { $('themesPanel').hidden = !$('themesPanel').hidden; }; $('closeThemes').onclick = () => { $('themesPanel').hidden = true; };
  $('closeAmbiguity').onclick = () => { state.sense = ''; $('ambiguityPanel').hidden = true; render(matches($('query').value)); }; $('closeDialog').onclick = () => $('recordDialog').close(); $('printRecord').onclick = () => print();
  $('downloadRecord').onclick = () => { const blob = new Blob([activeText()], { type: 'text/plain;charset=utf-8' }), a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `${state.active?.id || 'biblaw'}.txt`; a.click(); URL.revokeObjectURL(a.href); };
  load();
})();
