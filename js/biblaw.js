(() => {
  const $ = id => document.getElementById(id);
  const state = { mode: 'themes', records: [], themes: [], themeDirectory: [], themeById: new Map(), runtime: null, theme: null, sense: '', active: null, resolvedThemes: [] };
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae').replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/-/g, ' ').replace(/\s+/g, ' ').trim();
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const text = r => [r.title, r.summary, r.text, ...(r.verses || []).map(v => v.text), ...(r.conceptIds || [])].filter(Boolean).join(' ');
  const selectedTypes = () => new Set([...document.querySelectorAll('[name=sourceType]:checked')].map(x => x.value));
  const recordBookNumber = r => Number(r?.book?.number || r?.bookNumber || r?.source?.bookNumber || 0);
  const archangelName = value => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[value] || value || '');
  const label = r => r.recordType === 'psalm' ? `Psaume ${r.number} · ${archangelName(r.archangel)}` : r.recordType === 'master-prayer' ? `Prière ${r.number} · ${archangelName(r.archangel)}` : `Note · ${archangelName(r.archangel)}`;
  const importanceLabel = value => ({ central: 'Central', important: 'Important', related: 'Lié' }[value] || 'Indexé');

  async function load() {
    try {
      const [bundle, directory, runtime] = await Promise.all([
        fetch('data/browser-search-catalog.json').then(r => { if (!r.ok) throw Error('browser-search-catalog'); return r.json(); }),
        fetch('data/thematic-index/theme-directory.json').then(r => { if (!r.ok) throw Error('theme-directory'); return r.json(); }),
        fetch('data/thematic-index/theme-search-runtime.json').then(r => { if (!r.ok) throw Error('theme-search-runtime'); return r.json(); })
      ]);
      const loaded = bundle.records || [];
      state.themes = [];
      state.theme = null;
      state.themeDirectory = directory.themes || [];
      state.themeById = new Map(state.themeDirectory.map(t => [t.id, t]));
      state.runtime = runtime;
      state.records = loaded;
      const prayers = new Map(state.records.filter(r => r.recordType === 'master-prayer').map(r => [r.appliesToPsalmId, r]));
      state.records.filter(r => r.recordType === 'psalm').forEach(r => { if (prayers.has(r.id)) r.attachedPrayer = prayers.get(r.id); });
      const psalms = state.records.filter(r => r.recordType === 'psalm'), verses = psalms.reduce((n, r) => n + (r.verses || []).length, 0);
      const prayerCount = state.records.filter(r => r.recordType === 'master-prayer').length;
      const noteCount = state.records.filter(r => r.recordType === 'note').length + psalms.reduce((n, r) => n + (r.notes || []).length, 0);
      const books = new Map();
      psalms.forEach(r => { if (r.book?.number) books.set(Number(r.book.number), r.book.title || `Livre ${r.book.number}`); });
      $('bookFilter').innerHTML = '<option value="">Tous les livres</option>' + [...books.entries()].sort((a, b) => a[0] - b[0]).map(([number, title]) => `<option value="${number}">Livre ${number} · ${esc(title)}</option>`).join('');
      $('corpusStats').textContent = `${psalms.length} psaumes · ${verses} versets · ${prayerCount} prières · ${noteCount} notes reliées · ${state.themeDirectory.length} thèmes`;
      themes(); search();
    } catch (error) {
      console.error(error);
      $('results').innerHTML = '<div class="empty">Le corpus ne peut pas être chargé. Ouvrez Biblaw depuis son adresse web.</div>';
    }
  }

  function matches(query) {
    const terms = norm(query).split(' ').filter(Boolean), allowed = selectedTypes(), a = $('archangelFilter').value, b = Number($('bookFilter').value || 0);
    return state.records
      .filter(r => allowed.has(type(r)) && (!a || r.archangel === a) && (!b || recordBookNumber(r) === b))
      .map(record => ({ record, score: terms.filter(t => norm(text(record)).includes(t)).length / Math.max(1, terms.length) }))
      .filter(x => x.score > 0);
  }

  function resolveIndexedThemes(query) {
    const q = norm(query);
    if (!q) return [];
    const alias = state.runtime?.aliases?.[q];
    if (alias?.themeIds?.length) return alias.themeIds.map(id => state.themeById.get(id)).filter(Boolean);
    const exact = state.themeDirectory.filter(t => q === norm(t.label) || q === norm(t.id));
    if (exact.length) return exact;
    const candidates = state.themeDirectory
      .filter(t => norm(t.label).includes(q) || q.includes(norm(t.label)))
      .sort((a, b) => Math.abs(norm(a.label).length - q.length) - Math.abs(norm(b.label).length - q.length) || (b.score || 0) - (a.score || 0));
    return candidates.slice(0, 1);
  }

  function thematicItems(themes) {
    const allowed = selectedTypes();
    if (!allowed.has('psalm')) return [];
    const a = $('archangelFilter').value, b = Number($('bookFilter').value || 0);
    const byId = new Map(state.records.filter(r => r.recordType === 'psalm').map(r => [r.id, r]));
    const merged = new Map();
    for (const theme of themes) {
      for (const o of theme.occurrences || []) {
        if (a && o.archangel !== a) continue;
        if (b && Number(o.bookNumber || 0) !== b) continue;
        const record = byId.get(o.recordId);
        if (!record) continue;
        const current = merged.get(record.id) || { record, score: 0, thematic: o, matchedThemes: [] };
        current.score = Math.max(current.score, o.score || 1);
        if ((o.score || 1) > (current.thematic?.score || 0)) current.thematic = o;
        current.matchedThemes.push({ id: theme.id, label: theme.label, thematic: o });
        merged.set(record.id, current);
      }
    }
    return [...merged.values()].sort((x, y) => y.score - x.score || x.record.number - y.record.number);
  }

  function showThemeNavigation(resolvedThemes) {
    state.resolvedThemes = resolvedThemes;
    if (!resolvedThemes.length) { $('ambiguityPanel').hidden = true; return; }
    const ambiguous = resolvedThemes.length > 1;
    const seen = new Set(resolvedThemes.map(t => t.id));
    const choices = [];
    if (ambiguous) for (const theme of resolvedThemes) choices.push({ id: theme.id, label: theme.label, meta: 'Correspondance possible' });
    const neighbors = new Map();
    for (const theme of resolvedThemes) for (const link of state.runtime?.neighbors?.[theme.id] || []) {
      if (seen.has(link.themeId)) continue;
      const old = neighbors.get(link.themeId);
      if (!old || link.score > old.score) neighbors.set(link.themeId, link);
    }
    [...neighbors.values()].sort((a,b)=>b.score-a.score||b.sharedPsalmCount-a.sharedPsalmCount).slice(0, ambiguous ? 4 : 8).forEach(link => choices.push({ id: link.themeId, label: link.label, meta: `${link.sharedPsalmCount} psaume${link.sharedPsalmCount > 1 ? 's' : ''} partagé${link.sharedPsalmCount > 1 ? 's' : ''}` }));
    if (!choices.length) { $('ambiguityPanel').hidden = true; return; }
    $('suggestionKicker').textContent = ambiguous ? 'Correspondances multiples' : 'Navigation transversale';
    $('suggestionTitle').textContent = ambiguous ? 'Plusieurs thèmes correspondent à cette formulation' : 'Thèmes également présents dans ces psaumes';
    $('senseChoices').innerHTML = choices.map(c => `<button class="sense-button" data-theme-id="${esc(c.id)}"><strong>${esc(c.label)}</strong><span>${esc(c.meta)}</span></button>`).join('');
    document.querySelectorAll('[data-theme-id]').forEach(btn => btn.onclick = () => { const theme=state.themeById.get(btn.dataset.themeId); if(theme){ $('query').value=theme.label; search(); window.scrollTo({top:0,behavior:'smooth'}); } });
    $('ambiguityPanel').hidden = false;
  }

  function search() {
    const query = $('query').value.trim();
    if (!query) { $('ambiguityPanel').hidden = true; return render([]); }
    if (state.mode === 'themes') {
      const resolved = resolveIndexedThemes(query);
      if (resolved.length) { showThemeNavigation(resolved); return render(thematicItems(resolved), resolved); }
      $('ambiguityPanel').hidden = true;
    }
    render(matches(query).sort((a,b)=>b.score-a.score));
  }

  function summary(r) { return r.recordType === 'psalm' ? (r.verses || []).slice(0,2).map(v=>v.text).join(' ') : r.summary || (r.text || '').slice(0,280); }
  function recordPages(r) { return r.source?.pdfPages || r.source?.printedPages || (r.source?.printedPage ? [r.source.printedPage] : []); }
  function render(items, indexedThemes = null) {
    const themeLabels = Array.isArray(indexedThemes) ? indexedThemes.map(t=>t.label) : indexedThemes ? [indexedThemes.label] : [];
    $('resultCount').textContent = themeLabels.length ? `${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} · ${themeLabels.join(' / ')}` : `${items.length} résultat${items.length>1?'s':''}`;
    if (!items.length) { $('results').innerHTML='<div class="empty">Aucun passage indexé ne correspond encore à cette recherche et aux filtres sélectionnés.</div>'; return; }
    $('results').innerHTML = items.map(({record:r,thematic,matchedThemes}) => {
      const tags=thematic?[...new Set([...(matchedThemes||[]).map(x=>x.label),...(thematic.directness?[thematic.directness==='symbolic'?'Symbolique':'Direct']:[])])]:(r.conceptIds||[]);
      const pages=recordPages(r); const meta=thematic?`${thematic.bookTitle||`Livre ${thematic.bookNumber}`} · ${thematic.verseNumbers?.length?`verset${thematic.verseNumbers.length>1?'s':''} ${thematic.verseNumbers.join(', ')}`:'psaume entier'}`:(pages.length?`Page${pages.length>1?'s ': ' '}${pages.join('–')}`:'Référence structurée');
      const description=thematic?.teaching||summary(r);
      return `<article class="result-card"><div class="result-topline"><div><div class="result-doc">${esc(label(r))}</div><h3>${esc(r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée'))}</h3></div><strong class="score">${esc(thematic?importanceLabel(thematic.importance):'Texte')}</strong></div><div class="result-meta">${esc(meta)}</div><p class="result-summary">${esc(description)}</p><div class="tags">${tags.slice(0,8).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div><div class="result-actions">${r.recordType==='psalm'?`<a class="secondary" href="Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf#page=${pages[0]||1}" target="_blank">Voir dans le PDF</a>`:''}<button class="primary" data-open="${esc(r.id)}">Consulter</button></div></article>`;
    }).join('');
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>open(b.dataset.open));
  }
  function open(id) { const r=state.records.find(x=>x.id===id); if(!r)return; state.active=r; $('dialogEyebrow').textContent=label(r); $('dialogTitle').textContent=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée'); $('dialogContent').innerHTML=r.recordType==='psalm'?(r.verses||[]).map(v=>`<div class="verse"><div class="verse-number">${v.number}</div><div>${v.speakerId?`<span class="speaker">${esc(v.speakerId.replaceAll('-',' '))} · ${esc(v.speechRole||'')}</span>`:''}${esc(v.text)}</div></div>`).join('')+(r.attachedPrayer?`<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${esc(r.attachedPrayer.text)}</section>`:''):`<div class="prayer-block">${esc(r.text||r.summary||'')}</div>`; $('recordDialog').showModal(); }
  function activeText() { const r=state.active;if(!r)return'';let out=`${r.title||`Prière ${r.number}`}\n\n`;out+=r.verses?r.verses.map(v=>`${v.number}. ${v.text}`).join('\n'):r.text||r.summary||'';return out; }
  function themes() { $('themeDirectory').innerHTML=state.themeDirectory.map(t=>`<button class="theme-row" data-directory-theme="${esc(t.id)}"><span><strong>${esc(t.label)}</strong><small>${t.psalmCount} psaume${t.psalmCount>1?'s':''}</small></span><span>${t.totalScore}</span></button>`).join(''); $('indexCount').textContent=`${state.themeDirectory.length} thèmes indexés`; document.querySelectorAll('[data-directory-theme]').forEach(b=>b.onclick=()=>{const t=state.themeById.get(b.dataset.directoryTheme);if(t){$('query').value=t.label;closeIndex();search();}}); }
  function closeIndex(){ $('indexPanel').hidden=true;$('indexBackdrop').hidden=true;$('indexToggle').setAttribute('aria-expanded','false'); }
  $('searchButton').onclick=search; $('query').addEventListener('keydown',e=>{if(e.key==='Enter')search();}); document.querySelectorAll('[name=sourceType]').forEach(x=>x.onchange=search); $('archangelFilter').onchange=search; $('bookFilter').onchange=search;
  $('modeThemes').onclick=()=>{state.mode='themes';$('modeThemes').classList.add('active');$('modeExact').classList.remove('active');$('modeHelp').textContent='Retrouve les thèmes indexés et les psaumes classés par importance.';search();};
  $('modeExact').onclick=()=>{state.mode='exact';$('modeExact').classList.add('active');$('modeThemes').classList.remove('active');$('modeHelp').textContent='Recherche les mots présents dans le texte du corpus.';$('ambiguityPanel').hidden=true;search();};
  $('closeAmbiguity').onclick=()=>{$('ambiguityPanel').hidden=true;}; $('indexToggle').onclick=()=>{const open=$('indexPanel').hidden;$('indexPanel').hidden=!open;$('indexBackdrop').hidden=!open;$('indexToggle').setAttribute('aria-expanded',String(open));}; $('closeIndex').onclick=closeIndex;$('indexBackdrop').onclick=closeIndex;$('closeDialog').onclick=()=>$('recordDialog').close();$('printRecord').onclick=()=>window.print();$('downloadRecord').onclick=()=>{const blob=new Blob([activeText()],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${state.active?.id||'biblaw'}.txt`;a.click();URL.revokeObjectURL(a.href);};
  load();
})();
