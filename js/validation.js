(() => {
  const $ = id => document.getElementById(id), pdf = 'Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf';
  const representativePilots = new Set(['gabriel-psalm-112', 'raphael-psalm-104', 'ouriel-psalm-105', 'gabriel-psalm-182']);
  const state = { records: new Map(), active: null };
  const checks = [['sequence', 'Tous les numéros de versets sont présents et dans le bon ordre.'], ['speakers', 'Les paroles de l’Archange et les questions d’Olivier sont bien distinguées.'], ['prayer', 'La prière est bien celle placée immédiatement après ce psaume.'], ['notes', 'Les appels de notes et leur rattachement au verset sont exacts.'], ['source', 'Les pages, le livre, le titre et les dates éventuelles concordent avec le PDF.']];
  const esc = v => String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const angel = v => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[v] || v);
  const key = suffix => `biblaw-review:${state.active.psalm.id}:${suffix}`;

  async function load() {
    const catalog = await fetch('data/catalog.json').then(r => { if (!r.ok) throw Error('catalog'); return r.json(); });
    const docs = await Promise.all(catalog.records.map(path => fetch(path).then(r => { if (!r.ok) throw Error(path); return r.json(); })));
    const prayers = new Map(docs.filter(x => x.recordType === 'master-prayer').map(x => [x.appliesToPsalmId, x]));
    const notes = docs.filter(x => x.recordType === 'note');
    docs.filter(x => x.recordType === 'psalm' && ((x.archangel === 'michael' && x.book?.number === 17) || representativePilots.has(x.id))).sort((a, b) => a.book.number - b.book.number || a.number - b.number).forEach(psalm => {
      state.records.set(psalm.id, { psalm, prayer: prayers.get(psalm.id), notes: notes.filter(note => note.appliesTo?.recordId === psalm.id) });
    });
    $('recordSelect').innerHTML = [...state.records.values()].map(({ psalm }) => `<option value="${psalm.id}">${angel(psalm.archangel)} · Psaume ${psalm.number} — ${esc(psalm.title)}</option>`).join('');
    $('recordSelect').onchange = () => render($('recordSelect').value); $('saveReview').onclick = saveReview; $('copyReview').onclick = copyReview; render('michael-psalm-105');
  }
  function render(id) {
    state.active = state.records.get(id); const { psalm, prayer, notes } = state.active, pages = psalm.source.printedPages;
    $('recordSelect').value = id; $('sourceLink').href = `${pdf}#page=${pages[0]}`;
    $('validationStats').innerHTML = [[psalm.verses.length, 'versets'], [(psalm.dialogueSegments || []).length, 'question(s)'], [notes.length, 'note(s)'], [prayer ? `N° ${prayer.number}` : '—', 'prière rattachée']].map(([v, l]) => `<div class="stat-card"><strong>${v}</strong><span>${l}</span></div>`).join('');
    const corpusValidated = psalm.validation?.status === 'validated';
    $('recordHeader').innerHTML = `<div class="record-title"><span class="status-pill">${corpusValidated ? 'Validé dans GitHub' : 'À valider humainement'}</span><h2>${angel(psalm.archangel)} · Psaume ${psalm.number}</h2><p>Livre ${psalm.book.number} — ${esc(psalm.book.title)} · pages ${pages.join('–')}</p><h3>${esc(psalm.title)}</h3></div>`;
    const dialogue = psalm.dialogueSegments || [];
    $('dialogueNotice').innerHTML = dialogue.length ? `<div class="dialogue-notice">${dialogue.map(d => d.numbering === 'numbered-verse' ? `Question d’Olivier conservée comme verset ${d.verseNumber}.` : `Question éditoriale non numérotée placée après le verset ${d.positionAfterVerse}.`).join(' ')}</div>` : '';
    $('verses').innerHTML = psalm.verses.map(v => {
      const interludes = dialogue.filter(d => d.numbering === 'unnumbered-interlude' && d.positionAfterVerse === v.number).map(d => `<div class="interlude"><strong>${esc(d.editorialCue)}</strong>${esc(d.text)}</div>`).join('');
      const speaker = v.speakerId === 'olivier-manitara' ? 'Olivier Manitara · question' : `${angel(psalm.archangel)} · ${v.speechRole === 'answer' ? 'réponse' : 'enseignement'}`;
      return `<div class="validation-verse ${v.speechRole === 'question' ? 'question' : ''}"><div class="verse-number">${v.number}</div><div><span class="speaker">${speaker}</span>${esc(v.text)}</div></div>${interludes}`;
    }).join('');
    $('notes').innerHTML = notes.length ? `<section class="record-section"><h3>Notes rattachées</h3>${notes.map(n => `<div class="note-card"><strong>Verset ${n.appliesTo.verse || '—'} · appel ${n.appliesTo.marker}</strong><p>${esc(n.text || n.summary)}</p>${(n.temporalMentions || []).map(t => `<span class="tag">${esc(t.value)}</span>`).join('')}</div>`).join('')}</section>` : '';
    $('prayer').innerHTML = prayer ? `<section class="record-section"><h3>Prière du Maître n° ${prayer.number}</h3><p class="muted">Rattachement proposé par proximité éditoriale : imprimée immédiatement après le psaume.</p><div class="prayer-text">${esc(prayer.text)}</div></section>` : '';
    $('checklist').innerHTML = checks.map(([id, label]) => `<label class="check-row"><input type="checkbox" data-check="${id}" ${localStorage.getItem(key(id)) === '1' || (localStorage.getItem(key(id)) === null && corpusValidated) ? 'checked' : ''}><span>${label}</span></label>`).join('');
    document.querySelectorAll('[data-check]').forEach(input => input.onchange = () => { $('saveStatus').textContent = 'Modifications non enregistrées.'; });
    $('reviewNote').value = localStorage.getItem(key('note')) ?? psalm.validation?.review?.note ?? ''; $('reviewNote').oninput = () => { $('saveStatus').textContent = 'Modifications non enregistrées.'; }; $('copyStatus').textContent = '';
    const saved = localStorage.getItem(key('savedAt')); $('saveStatus').textContent = saved ? `Enregistré sur cet appareil le ${new Date(saved).toLocaleString('fr-FR')}.` : (corpusValidated ? 'Cette validation est déjà inscrite dans GitHub.' : 'Pas encore enregistrée.');
  }
  function saveReview() {
    document.querySelectorAll('[data-check]').forEach(input => localStorage.setItem(key(input.dataset.check), input.checked ? '1' : '0'));
    localStorage.setItem(key('note'), $('reviewNote').value); const savedAt = new Date().toISOString(); localStorage.setItem(key('savedAt'), savedAt);
    $('saveStatus').textContent = `Enregistré sur cet appareil le ${new Date(savedAt).toLocaleString('fr-FR')}.`;
  }
  async function copyReview() {
    const { psalm } = state.active, done = checks.filter(([id]) => localStorage.getItem(key(id)) === '1').map(([, l]) => `✓ ${l}`), todo = checks.filter(([id]) => localStorage.getItem(key(id)) !== '1').map(([, l]) => `□ ${l}`);
    const report = [`Validation — ${angel(psalm.archangel)}, psaume ${psalm.number}`, ...done, ...todo, '', $('reviewNote').value.trim()].join('\n').trim();
    try { await navigator.clipboard.writeText(report); $('copyStatus').textContent = 'Compte rendu copié.'; } catch { $('copyStatus').textContent = 'Copie impossible dans ce navigateur.'; }
  }
  load().catch(() => { document.querySelector('.validation-grid').innerHTML = '<div class="empty">Impossible de charger les données de validation.</div>'; });
})();
