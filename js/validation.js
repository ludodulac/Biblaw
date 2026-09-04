(() => {
  const $ = id => document.getElementById(id), pdf = 'Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf';
  const configs = [
    ['michael-psalm-105', 'data/corpus/michael/psalm-105.json', 'data/prayers/michael-book-17-prayer-001.json', 'data/notes/michael-psalm-105-note-001.json'],
    ['gabriel-psalm-112', 'data/corpus/gabriel/psalm-112.json', 'data/prayers/gabriel-book-18-prayer-001.json', 'data/notes/gabriel-psalm-112-note-001.json'],
    ['raphael-psalm-104', 'data/corpus/raphael/psalm-104.json', 'data/prayers/raphael-book-19-prayer-003.json', 'data/notes/raphael-psalm-104-note-001.json'],
    ['ouriel-psalm-105', 'data/corpus/ouriel/psalm-105.json', 'data/prayers/ouriel-book-20-prayer-002.json'],
    ['gabriel-psalm-182', 'data/corpus/gabriel/psalm-182.json', 'data/prayers/gabriel-book-26-prayer-066.json', 'data/notes/gabriel-psalm-182-note-001.json']
  ];
  const state = { records: new Map(), active: null };
  const checks = [['sequence', 'Tous les numéros de versets sont présents et dans le bon ordre.'], ['speakers', 'Les paroles de l’Archange et les questions d’Olivier sont bien distinguées.'], ['prayer', 'La prière est bien celle placée immédiatement après ce psaume.'], ['notes', 'Les appels de notes et leur rattachement au verset sont exacts.'], ['source', 'Les pages, le livre, le titre et les dates éventuelles concordent avec le PDF.']];
  const esc = v => String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const angel = v => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[v] || v);
  const key = suffix => `biblaw-review:${state.active.psalm.id}:${suffix}`;

  async function load() {
    for (const [id, ...paths] of configs) {
      const docs = await Promise.all(paths.map(path => fetch(path).then(r => { if (!r.ok) throw Error(path); return r.json(); })));
      state.records.set(id, { psalm: docs[0], prayer: docs.find(x => x.recordType === 'master-prayer'), notes: docs.filter(x => x.recordType === 'note') });
    }
    $('recordSelect').innerHTML = [...state.records.values()].map(({ psalm }) => `<option value="${psalm.id}">${angel(psalm.archangel)} · Psaume ${psalm.number} — ${esc(psalm.title)}</option>`).join('');
    $('recordSelect').onchange = () => render($('recordSelect').value); $('copyReview').onclick = copyReview; render(configs[0][0]);
  }
  function render(id) {
    state.active = state.records.get(id); const { psalm, prayer, notes } = state.active, pages = psalm.source.printedPages;
    $('recordSelect').value = id; $('sourceLink').href = `${pdf}#page=${pages[0]}`;
    $('validationStats').innerHTML = [[psalm.verses.length, 'versets'], [(psalm.dialogueSegments || []).length, 'question(s)'], [notes.length, 'note(s)'], [prayer ? `N° ${prayer.number}` : '—', 'prière rattachée']].map(([v, l]) => `<div class="stat-card"><strong>${v}</strong><span>${l}</span></div>`).join('');
    $('recordHeader').innerHTML = `<div class="record-title"><span class="status-pill">À valider humainement</span><h2>${angel(psalm.archangel)} · Psaume ${psalm.number}</h2><p>Livre ${psalm.book.number} — ${esc(psalm.book.title)} · pages ${pages.join('–')}</p><h3>${esc(psalm.title)}</h3></div>`;
    const dialogue = psalm.dialogueSegments || [];
    $('dialogueNotice').innerHTML = dialogue.length ? `<div class="dialogue-notice">${dialogue.map(d => d.numbering === 'numbered-verse' ? `Question d’Olivier conservée comme verset ${d.verseNumber}.` : `Question éditoriale non numérotée placée après le verset ${d.positionAfterVerse}.`).join(' ')}</div>` : '';
    $('verses').innerHTML = psalm.verses.map(v => {
      const interludes = dialogue.filter(d => d.numbering === 'unnumbered-interlude' && d.positionAfterVerse === v.number).map(d => `<div class="interlude"><strong>${esc(d.editorialCue)}</strong>${esc(d.text)}</div>`).join('');
      const speaker = v.speakerId === 'olivier-manitara' ? 'Olivier Manitara · question' : `${angel(psalm.archangel)} · ${v.speechRole === 'answer' ? 'réponse' : 'enseignement'}`;
      return `<div class="validation-verse ${v.speechRole === 'question' ? 'question' : ''}"><div class="verse-number">${v.number}</div><div><span class="speaker">${speaker}</span>${esc(v.text)}</div></div>${interludes}`;
    }).join('');
    $('notes').innerHTML = notes.length ? `<section class="record-section"><h3>Notes rattachées</h3>${notes.map(n => `<div class="note-card"><strong>Verset ${n.appliesTo.verse || '—'} · appel ${n.appliesTo.marker}</strong><p>${esc(n.text || n.summary)}</p>${(n.temporalMentions || []).map(t => `<span class="tag">${esc(t.value)}</span>`).join('')}</div>`).join('')}</section>` : '';
    $('prayer').innerHTML = prayer ? `<section class="record-section"><h3>Prière du Maître n° ${prayer.number}</h3><p class="muted">Rattachement proposé par proximité éditoriale : imprimée immédiatement après le psaume.</p><div class="prayer-text">${esc(prayer.text)}</div></section>` : '';
    $('checklist').innerHTML = checks.map(([id, label]) => `<label class="check-row"><input type="checkbox" data-check="${id}" ${localStorage.getItem(key(id)) === '1' ? 'checked' : ''}><span>${label}</span></label>`).join('');
    document.querySelectorAll('[data-check]').forEach(input => input.onchange = () => localStorage.setItem(key(input.dataset.check), input.checked ? '1' : '0'));
    $('reviewNote').value = localStorage.getItem(key('note')) || ''; $('reviewNote').oninput = () => localStorage.setItem(key('note'), $('reviewNote').value); $('copyStatus').textContent = '';
  }
  async function copyReview() {
    const { psalm } = state.active, done = checks.filter(([id]) => localStorage.getItem(key(id)) === '1').map(([, l]) => `✓ ${l}`), todo = checks.filter(([id]) => localStorage.getItem(key(id)) !== '1').map(([, l]) => `□ ${l}`);
    const report = [`Validation — ${angel(psalm.archangel)}, psaume ${psalm.number}`, ...done, ...todo, '', $('reviewNote').value.trim()].join('\n').trim();
    try { await navigator.clipboard.writeText(report); $('copyStatus').textContent = 'Compte rendu copié.'; } catch { $('copyStatus').textContent = 'Copie impossible dans ce navigateur.'; }
  }
  load().catch(() => { document.querySelector('.validation-grid').innerHTML = '<div class="empty">Impossible de charger les données de validation.</div>'; });
})();
