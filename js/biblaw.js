(() => {
  const $ = id => document.getElementById(id);
  const state = { mode: 'themes', records: [], recordById: new Map(), psalmsByNumber: new Map(), normalizedFragmentsById: new Map(), themeDirectory: [], themeById: new Map(), themesByRecord: new Map(), runtime: null, active: null, resolvedThemes: [] };
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae').replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/-/g, ' ').replace(/\s+/g, ' ').trim();
  const stripLeadingArticle = value => { const q=norm(value), parts=q.split(' ').filter(Boolean); return parts.length>1 && ['l','le','la','les','un','une','des'].includes(parts[0]) ? parts.slice(1).join(' ') : q; };
  const themeQueryForms = value => { const q=norm(value), stripped=stripLeadingArticle(q); return [...new Set([q,stripped].filter(Boolean))]; };
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const queryTerms = () => new Set([$('query')?.value, $('query2')?.value].flatMap(value => norm(value).split(' ')).filter(Boolean));
  const highlighted = value => { const terms=queryTerms(); if(!terms.size)return esc(value); return String(value||'').split(/([\p{L}\p{N}œŒæÆ’'-]+)/gu).map(part=>terms.has(norm(part))?`<mark class="search-hit">${esc(part)}</mark>`:esc(part)).join(''); };
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const textFragments = r => r.recordType === 'psalm' ? [r.title, ...(r.verses || []).map(v => v.text)].filter(Boolean) : [r.title, r.text, r.summary].filter(Boolean);
  const literalIncludes = (value, query) => { const needle=norm(query); if(!needle)return false; return ` ${norm(value)} `.includes(` ${needle} `); };
  const literalTextMatch = (r, needle) => Boolean(needle) && (state.normalizedFragmentsById.get(r.id)||[]).some(fragment => ` ${fragment} `.includes(` ${needle} `));
  const parsePsalmNumberQuery = value => { const match=norm(value).match(/^(?:psaume\s+)?([0-9]{1,4})$/); if(!match)return null; const number=Number(match[1]); return Number.isInteger(number)&&number>0?number:null; };
  const selectedTypes = () => new Set([...document.querySelectorAll('[name=sourceType]:checked')].map(x => x.value));
  const archangelName = value => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[value] || value || '');
  const label = r => r.recordType === 'psalm' ? `Psaume ${r.number} · ${archangelName(r.archangel)}` : r.recordType === 'master-prayer' ? `Prière ${r.number} · ${archangelName(r.archangel)}` : `Note · ${archangelName(r.archangel)}`;
  const importanceLabel = value => ({ central: 'Central', important: 'Important', related: 'Lié' }[value] || 'Indexé');
  const importanceRank = value => ({ central: 0, important: 1, related: 2 }[value] ?? 3);
  const publishPresentationState = detail => document.dispatchEvent(new CustomEvent('biblaw:presentation-state', { detail }));
  const activateThemeMode = () => { state.mode='themes'; $('modeThemes').classList.add('active'); $('modeExact').classList.remove('active'); $('primarySearch').classList.remove('exact-mode'); $('query2').disabled=false; $('modeHelp').textContent='Retrouve les thèmes indexés. Les psaumes sont classés Central, Important, puis Lié. Un numéro de psaume peut aussi être saisi directement.'; };
  const activateExactMode = () => { state.mode='exact'; $('modeExact').classList.add('active'); $('modeThemes').classList.remove('active'); $('primarySearch').classList.add('exact-mode'); $('query2').disabled=true; $('modeHelp').textContent='Recherche un mot ou une expression dans le texte du corpus. Un numéro de psaume peut aussi être saisi directement.'; hideAmbiguity(); hideTransverseNavigation(); };

  async function load() {
    try {
      const [bundle, directory, runtime] = await Promise.all([
        fetch('data/browser-search-catalog.json').then(r => { if (!r.ok) throw Error('browser-search-catalog'); return r.json(); }),
        fetch('data/thematic-index/theme-directory-public.json').then(r => { if (!r.ok) throw Error('theme-directory'); return r.json(); }),
        fetch('data/thematic-index/theme-search-runtime.json').then(r => { if (!r.ok) throw Error('theme-search-runtime'); return r.json(); })
      ]);
      state.themeDirectory = directory.themes || [];
      state.themeById = new Map(state.themeDirectory.map(t => [t.id, t]));
      state.runtime = runtime;
      state.records = bundle.records || [];
      state.recordById = new Map(state.records.map(r => [r.id, r]));
      state.psalmsByNumber = new Map();
      state.normalizedFragmentsById = new Map();
      for (const r of state.records) {
        state.normalizedFragmentsById.set(r.id,textFragments(r).map(norm).filter(Boolean));
        if (r.recordType === 'psalm') { const number=Number(r.number), list=state.psalmsByNumber.get(number)||[]; list.push(r); state.psalmsByNumber.set(number,list); }
      }
      state.themesByRecord = new Map();
      for (const theme of state.themeDirectory) for (const occurrence of theme.occurrences || []) {
        const list = state.themesByRecord.get(occurrence.recordId) || [];
        list.push({ id: theme.id, label: theme.label, importance: occurrence.importance, score: occurrence.score || 0 });
        state.themesByRecord.set(occurrence.recordId, list);
      }
      for (const list of state.themesByRecord.values()) list.sort((a,b)=>importanceRank(a.importance)-importanceRank(b.importance)||a.label.localeCompare(b.label,'fr')||a.id.localeCompare(b.id,'fr'));
      const prayers = new Map(state.records.filter(r => r.recordType === 'master-prayer').map(r => [r.appliesToPsalmId, r]));
      state.records.filter(r => r.recordType === 'psalm').forEach(r => { if (prayers.has(r.id)) r.attachedPrayer = prayers.get(r.id); });
      const psalms = state.records.filter(r => r.recordType === 'psalm'), verses = psalms.reduce((n, r) => n + (r.verses || []).length, 0);
      $('corpusStats').textContent = `${psalms.length} psaumes · ${verses} versets · ${state.themeDirectory.length} thèmes indexés`;
      $('indexCount').textContent=`${state.themeDirectory.length} thèmes indexés`;
      search();
    } catch (error) { console.error(error); $('results').innerHTML = '<div class="empty">Le corpus ne peut pas être chargé. Ouvrez Biblaw depuis son adresse web.</div>'; }
  }

  function matches(query) { const allowed = selectedTypes(), a = $('archangelFilter').value, needle=norm(query); return state.records.filter(r => allowed.has(type(r)) && (!a || r.archangel === a) && literalTextMatch(r, needle)).map(record => ({ record, score: 1 })); }
  function psalmNumberMatches(number) { if(!selectedTypes().has('psalm'))return []; const a=$('archangelFilter').value; return (state.psalmsByNumber.get(number)||[]).filter(r=>!a||r.archangel===a).sort((x,y)=>(x.book?.number||9999)-(y.book?.number||9999)||String(x.id).localeCompare(String(y.id),'fr')).map(record=>({record,score:1,numberLookup:true})); }
  function textualPsalmMatches(query) { return matches(query).filter(x=>x.record.recordType==='psalm'); }
  function resolveIndexedThemes(query) {
    const forms=themeQueryForms(query); if(!forms.length)return [];
    for(const q of forms){ const alias=state.runtime?.aliases?.[q]; if(alias?.themeIds?.length)return alias.themeIds.map(id=>state.themeById.get(id)).filter(Boolean); }
    for(const q of forms){ const exact=state.themeDirectory.filter(t=>q===norm(t.label)||q===norm(t.id)); if(exact.length)return exact; }
    return [];
  }
  function thematicItems(themes) {
    if (!selectedTypes().has('psalm')) return [];
    const a=$('archangelFilter').value,merged=new Map();
    for (const theme of themes) for (const o of theme.occurrences||[]) {
      if (a&&o.archangel!==a) continue;
      const record=state.recordById.get(o.recordId); if(!record||record.recordType!=='psalm') continue;
      const current=merged.get(record.id)||{record,score:0,thematic:o,matchedThemes:[]};
      const betterImportance=importanceRank(o.importance)<importanceRank(current.thematic?.importance);
      const sameImportance=importanceRank(o.importance)===importanceRank(current.thematic?.importance);
      current.score=Math.max(current.score,o.score||1);
      if(betterImportance||(sameImportance&&(o.score||1)>(current.thematic?.score||0))) current.thematic=o;
      current.matchedThemes.push({id:theme.id,label:theme.label,thematic:o}); merged.set(record.id,current);
    }
    return [...merged.values()].sort((x,y)=>importanceRank(x.thematic?.importance)-importanceRank(y.thematic?.importance)||x.record.number-y.record.number||String(x.record.id).localeCompare(String(y.record.id),'fr'));
  }
  function intersectionItems(themeA, themeB) {
    if (!selectedTypes().has('psalm')) return [];
    const a=$('archangelFilter').value;
    const occurrencesA=new Map((themeA.occurrences||[]).filter(o=>!a||o.archangel===a).map(o=>[o.recordId,o]));
    const occurrencesB=new Map((themeB.occurrences||[]).filter(o=>!a||o.archangel===a).map(o=>[o.recordId,o]));
    const items=[];
    for (const [recordId, thematicA] of occurrencesA) {
      const thematicB=occurrencesB.get(recordId); if(!thematicB)continue;
      const record=state.recordById.get(recordId); if(!record||record.recordType!=='psalm')continue;
      items.push({record, thematic:thematicA, matchedThemes:[{id:themeA.id,label:themeA.label,thematic:thematicA},{id:themeB.id,label:themeB.label,thematic:thematicB}], themeMatches:[{theme:themeA,thematic:thematicA},{theme:themeB,thematic:thematicB}]});
    }
    return items.sort((x,y)=>importanceRank(x.themeMatches[0].thematic.importance)-importanceRank(y.themeMatches[0].thematic.importance)||(y.themeMatches[0].thematic.score||0)-(x.themeMatches[0].thematic.score||0)||x.record.number-y.record.number||String(x.record.id).localeCompare(String(y.record.id),'fr'));
  }

  function hideAmbiguity(){ $('ambiguityPanel').hidden=true; $('senseChoices').innerHTML=''; }
  function ambiguityChoice(theme, target) { const count=theme.occurrenceCount||theme.occurrences?.length||0; return `<button class="sense-button" data-ambiguity-target="${target}" data-theme-id="${esc(theme.id)}"><strong>${esc(theme.label)}</strong><span>${count} psaume${count>1?'s':''} indexé${count>1?'s':''}${theme.id?` · ${esc(theme.id)}`:''}</span></button>`; }
  function showDualAmbiguity(queryA, resolvedA, queryB, resolvedB) {
    hideTransverseNavigation();
    const blocks=[];
    if(resolvedA.length!==1) blocks.push(`<div class="ambiguity-group"><div class="context-label">Thème 1 · ${esc(queryA)}</div>${resolvedA.length?resolvedA.map(t=>ambiguityChoice(t,'query')).join(''):'<div class="muted">Aucun thème canonique ne correspond exactement à ce champ.</div>'}</div>`);
    if(resolvedB.length!==1) blocks.push(`<div class="ambiguity-group"><div class="context-label">Thème 2 · ${esc(queryB)}</div>${resolvedB.length?resolvedB.map(t=>ambiguityChoice(t,'query2')).join(''):'<div class="muted">Aucun thème canonique ne correspond exactement à ce champ.</div>'}</div>`);
    $('suggestionKicker').textContent='Préciser la recherche'; $('suggestionTitle').textContent='Résolvez chaque thème avant l’intersection'; $('senseChoices').innerHTML=blocks.join('');
    $('senseChoices').querySelectorAll('[data-ambiguity-target]').forEach(btn=>btn.onclick=()=>{ const theme=state.themeById.get(btn.dataset.themeId); if(!theme)return; $(btn.dataset.ambiguityTarget).value=theme.label; search(); });
    $('ambiguityPanel').hidden=false;
  }
  function showSingleThemeAmbiguity(resolvedThemes) {
    state.resolvedThemes=resolvedThemes;
    if(resolvedThemes.length<=1){hideAmbiguity();return;}
    $('suggestionKicker').textContent='Correspondances multiples'; $('suggestionTitle').textContent='Plusieurs thèmes correspondent à cette formulation';
    $('senseChoices').innerHTML=resolvedThemes.map(theme=>ambiguityChoice(theme,'query')).join('');
    $('senseChoices').querySelectorAll('[data-ambiguity-target]').forEach(btn=>btn.onclick=()=>{const theme=state.themeById.get(btn.dataset.themeId);if(!theme)return;$('query').value=theme.label;search();});
    $('ambiguityPanel').hidden=false;
  }
  function hideTransverseNavigation(){ $('transversePanel').hidden=true; $('transversePanel').open=false; $('transverseChoices').innerHTML=''; }
  function showTransverseNavigation(theme) {
    hideTransverseNavigation(); if(!theme)return;
    const links=(state.runtime?.neighbors?.[theme.id]||[]).slice().sort((a,b)=>b.score-a.score||b.sharedPsalmCount-a.sharedPsalmCount).slice(0,8);
    if(!links.length)return;
    $('transverseChoices').innerHTML=links.map(link=>`<button class="text-link" data-transverse-theme="${esc(link.themeId)}">${esc(link.label)} <span>${link.sharedPsalmCount}</span></button>`).join('');
    $('transverseChoices').querySelectorAll('[data-transverse-theme]').forEach(btn=>btn.onclick=()=>navigateToTheme(state.themeById.get(btn.dataset.transverseTheme)));
    $('transversePanel').hidden=false;
  }
  function navigateToTheme(theme) {
    if(!theme)return; activateThemeMode(); $('query').value=theme.label; $('query2').value=''; if($('recordDialog').open)$('recordDialog').close();
    const thematic=thematicItems([theme]), textual=textualPsalmMatches(theme.label); hideAmbiguity(); showTransverseNavigation(theme);
    publishPresentationState({kind:'canonical-theme',theme:{id:theme.id,label:theme.label},psalmCount:thematic.length});
    render(thematic,[theme],{textualCount:textual.length}); window.scrollTo({top:0,behavior:'smooth'});
  }

  function search(){
    const query=$('query').value.trim(), query2=$('query2').value.trim();
    if(!query){hideAmbiguity();hideTransverseNavigation();publishPresentationState({kind:'no-result'});return render([]);}
    const psalmNumber=parsePsalmNumberQuery(query);
    if(psalmNumber!==null && !query2){ hideAmbiguity();hideTransverseNavigation();publishPresentationState({kind:'other'}); return render(psalmNumberMatches(psalmNumber),null,{numberLookup:true,psalmNumber}); }
    if(state.mode==='themes'){
      if(query2){
        const resolvedA=resolveIndexedThemes(query), resolvedB=resolveIndexedThemes(query2);
        if(resolvedA.length!==1||resolvedB.length!==1){ showDualAmbiguity(query,resolvedA,query2,resolvedB); publishPresentationState({kind:'ambiguous-themes',themes:[...resolvedA,...resolvedB].map(theme=>({id:theme.id,label:theme.label}))}); return render([],[],{dualPending:true}); }
        hideAmbiguity();hideTransverseNavigation();
        const items=intersectionItems(resolvedA[0],resolvedB[0]);
        publishPresentationState({kind:'dual-theme',themes:[{id:resolvedA[0].id,label:resolvedA[0].label},{id:resolvedB[0].id,label:resolvedB[0].label}],psalmCount:items.length});
        return render(items,[resolvedA[0],resolvedB[0]],{dualTheme:true});
      }
      const resolved=resolveIndexedThemes(query);
      if(resolved.length){
        showSingleThemeAmbiguity(resolved); const thematic=thematicItems(resolved), textual=textualPsalmMatches(query);
        if(resolved.length===1)showTransverseNavigation(resolved[0]); else hideTransverseNavigation();
        publishPresentationState(resolved.length===1 ? {kind:'canonical-theme',theme:{id:resolved[0].id,label:resolved[0].label},psalmCount:thematic.length} : {kind:'ambiguous-themes',themes:resolved.map(theme=>({id:theme.id,label:theme.label}))});
        return render(thematic,resolved,{textualCount:textual.length});
      }
      hideAmbiguity();hideTransverseNavigation(); const textual=textualPsalmMatches(query); publishPresentationState({kind:textual.length?'textual-fallback':'no-result'}); return render(textual,[],{textualCount:textual.length,unresolvedTheme:true,textualFallback:true});
    }
    hideAmbiguity();hideTransverseNavigation();publishPresentationState({kind:'other'});render(matches(query).sort((a,b)=>b.score-a.score));
  }

  function summary(r){return r.recordType==='psalm'?(r.verses||[]).slice(0,2).map(v=>v.text).join(' '):r.summary||(r.text||'').slice(0,280);}
  function contextualVerses(r,thematic){ if(!thematic?.verseNumbers?.length||!r.verses?.length)return''; const wanted=new Set(thematic.verseNumbers.map(Number)); const chosen=r.verses.filter(v=>wanted.has(Number(v.number))).slice(0,4); if(!chosen.length)return''; return `<div class="theme-context"><div class="context-label">Passage concerné</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${highlighted(v.text)}</span></div>`).join('')}</div>`; }
  function exactVerses(r){ if(r.recordType!=='psalm'||!r.verses?.length)return''; const query=$('query').value; if(!norm(query))return''; const chosen=r.verses.filter(v=>literalIncludes(v.text,query)).slice(0,4); if(!chosen.length)return''; return `<div class="theme-context exact-context"><div class="context-label">Passage${chosen.length>1?'s':''} où la recherche apparaît</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${highlighted(v.text)}</span></div>`).join('')}</div>`; }
  function relatedThemes(r,matchedThemes){ const matched=new Set((matchedThemes||[]).map(x=>x.id)); return (state.themesByRecord.get(r.id)||[]).filter(t=>!matched.has(t.id)).slice(0,12); }
  function themeTags(themes){ if(!themes.length)return '<span class="muted inline-empty">Aucun autre thème indexé.</span>'; return `<span class="inline-themes">${themes.map(t=>`<button class="theme-text-link" data-related-theme="${esc(t.id)}">${esc(t.label)}</button>`).join('<span class="theme-separator">·</span>')}</span>`; }
  function bindThemeLinks(root=document){ root.querySelectorAll('[data-related-theme]').forEach(b=>b.onclick=()=>navigateToTheme(state.themeById.get(b.dataset.relatedTheme))); }
  function dualThemeReasons(r, themeMatches){ return `<div class="theme-reasons">${themeMatches.map(({theme,thematic})=>`<section class="theme-reason"><div class="theme-reason-head"><strong>${esc(theme.label)}</strong><span class="score">${esc(importanceLabel(thematic.importance))}</span></div><p class="result-summary">${highlighted(thematic.teaching||'')}</p>${contextualVerses(r,thematic)}</section>`).join('')}</div>`; }

  function render(items,indexedThemes=null,companion=null){
    const themeLabels=Array.isArray(indexedThemes)?indexedThemes.map(t=>t.label):indexedThemes?[indexedThemes.label]:[];
    $('resultCount').textContent=companion?.dualPending?'Intersection en attente':companion?.dualTheme?`${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} sous les deux thèmes`:companion?.numberLookup?`${items.length} psaume${items.length>1?'s':''} portant le numéro ${companion.psalmNumber}`:themeLabels.length?`${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} · classés Central, Important, puis Lié`:companion?.textualFallback?`${items.length} occurrence${items.length>1?'s':''} du terme dans le corpus`:`${items.length} résultat${items.length>1?'s':''}`;
    const textualNotice=!companion?.dualTheme&&themeLabels.length===1&&companion?.textualCount>0?`<div class="search-scope-note"><div><strong>THÈME INDEXÉ</strong><span>Deux lectures de cette recherche : ${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} sous ce thème · le mot ou l’expression apparaît dans ${companion.textualCount} psaume${companion.textualCount>1?'s':''} du texte.</span></div><button class="secondary" data-show-text-search>Voir les occurrences textuelles</button></div>`:'';
    const unresolvedNotice=companion?.unresolvedTheme?`<div class="search-scope-note"><div><strong>${companion.textualFallback&&items.length?'OCCURRENCE DU TERME DANS LE CORPUS':'Aucun thème indexé ne correspond à cette recherche'}</strong><span>${companion.textualFallback&&items.length?`Aucun thème canonique ne correspond à cette recherche. ${items.length} psaume${items.length>1?'s':''} ${items.length>1?'contiennent':'contient'} néanmoins exactement le mot ou l’expression recherchée. Ces occurrences ne constituent pas un thème.`:'Aucune occurrence textuelle exacte ne correspond non plus avec les filtres sélectionnés.'}</span></div></div>`:'';
    if(!items.length){ const emptyNumber=companion?.numberLookup?`<div class="empty">Aucun psaume numéro ${esc(companion.psalmNumber)} ne correspond aux filtres sélectionnés.</div>`:''; const dualEmpty=companion?.dualTheme?'<div class="empty">Aucun psaume n’est actuellement indexé sous les deux thèmes.</div>':''; const pending=companion?.dualPending?'<div class="empty">Choisissez une correspondance canonique pour chaque thème afin de calculer l’intersection documentaire.</div>':''; $('results').innerHTML=emptyNumber||dualEmpty||pending||unresolvedNotice||(textualNotice+'<div class="empty">Aucun passage indexé ne correspond encore à cette recherche et aux filtres sélectionnés.</div>');bindTextSearchLink();return; }
    $('results').innerHTML=unresolvedNotice+textualNotice+items.map(({record:r,thematic,matchedThemes,numberLookup,themeMatches})=>{
      const bookMeta=r.book?.number?`Livre ${r.book.number}${r.book.title?` · ${r.book.title}`:''}`:'';
      const meta=thematic?`${thematic.bookTitle||`Livre ${thematic.bookNumber}`} · ${thematic.verseNumbers?.length?`verset${thematic.verseNumbers.length>1?'s':''} ${thematic.verseNumbers.join(', ')}`:'psaume entier'}`:bookMeta||'Corpus structuré';
      const related=(thematic||themeMatches)?relatedThemes(r,matchedThemes):[]; const textualThemes=!thematic&&!themeMatches&&companion?.textualFallback?(state.themesByRecord.get(r.id)||[]):[];
      const relatedBlock=(thematic||themeMatches)?`<div class="related-themes compact-related"><span class="related-label">Autres thèmes dans ce psaume :</span> ${themeTags(related)}</div>`:textualThemes.length?`<div class="related-themes compact-related"><span class="related-label">Thèmes canoniques indexés dans ce psaume :</span> ${themeTags(textualThemes)}</div>`:'';
      const exactBlock=!thematic&&!themeMatches&&!numberLookup?exactVerses(r):'';
      const status=themeMatches?'Deux thèmes':thematic?importanceLabel(thematic.importance):numberLookup?'Numéro':companion?.textualFallback?'Occurrence du terme':'Texte';
      const singleThemeBody=thematic&&!themeMatches?`<div class="context-label theme-found">THÈME INDEXÉ · ${esc((matchedThemes||[]).map(x=>x.label).join(' · '))}</div><p class="result-summary">${highlighted(thematic.teaching||summary(r))}</p>${contextualVerses(r,thematic)}`:'';
      const dualBody=themeMatches?dualThemeReasons(r,themeMatches):'';
      const fallbackBody=!thematic&&!themeMatches?`<p class="result-summary">${highlighted(summary(r))}</p>${exactBlock}`:'';
      return `<article class="result-card"><div class="result-topline"><div><div class="result-doc">${esc(label(r))}</div><h3>${highlighted(r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée'))}</h3></div><strong class="score">${esc(status)}</strong></div><div class="result-meta">${esc(bookMeta||meta)}</div>${dualBody||singleThemeBody||fallbackBody}${relatedBlock}<div class="result-actions"><button class="primary" data-open="${esc(r.id)}">${thematic||themeMatches?'Voir le psaume source':'Voir'}</button></div></article>`;
    }).join('');
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>open(b.dataset.open)); bindThemeLinks($('results')); bindTextSearchLink();
  }
  function bindTextSearchLink(){ const button=document.querySelector('[data-show-text-search]'); if(button)button.onclick=()=>{ $('secondaryTools').open=true; activateExactMode(); search(); window.scrollTo({top:$('results').offsetTop-90,behavior:'smooth'}); }; }
  function open(id){
    const r=state.recordById.get(id);if(!r)return;state.active=r; $('dialogEyebrow').textContent=label(r);$('dialogTitle').textContent=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée');
    if(r.recordType==='psalm'){ const verses=(r.verses||[]).map(v=>`<div class="verse"><div class="verse-number">${v.number}</div><div>${v.speakerId?`<span class="speaker">${esc(v.speakerId.replaceAll('-',' '))} · ${esc(v.speechRole||'')}</span>`:''}${highlighted(v.text)}</div></div>`).join(''); const themesBlock=`<section class="related-themes dialog-themes"><div class="context-label">Thèmes présents dans ce psaume</div>${themeTags(state.themesByRecord.get(r.id)||[])}</section>`; $('dialogContent').innerHTML=verses+(r.attachedPrayer?`<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${highlighted(r.attachedPrayer.text)}</section>`:'')+themesBlock; bindThemeLinks($('dialogContent')); } else $('dialogContent').innerHTML=`<div class="prayer-block">${highlighted(r.text||r.summary||'')}</div>`;
    $('recordDialog').showModal();
  }
  function activeText(){ const r=state.active;if(!r)return''; const title=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée'); const header=[label(r),title]; if(r.book?.number)header.push(`Livre ${r.book.number}${r.book.title?` · ${r.book.title}`:''}`); let out=header.join('\n')+'\n\n'; if(r.verses){ out+=(r.verses||[]).map(v=>`${v.number}. ${v.text}`).join('\n'); if(r.attachedPrayer?.text)out+=`\n\nPrière ${r.attachedPrayer.number}\n\n${r.attachedPrayer.text}`; }else out+=r.text||r.summary||''; return out; }
  function renderThemeDirectory(){ const needle=norm($('themeFilter').value); const visible=needle?state.themeDirectory.filter(t=>norm(t.label).includes(needle)||norm(t.id).includes(needle)):state.themeDirectory; $('indexCount').textContent=needle?`${visible.length} thème${visible.length>1?'s':''} sur ${state.themeDirectory.length}`:`${state.themeDirectory.length} thèmes indexés`; $('themeDirectory').innerHTML=visible.length?visible.map(t=>`<button class="theme-row" data-directory-theme="${esc(t.id)}"><span><strong>${esc(t.label)}</strong><small>${t.occurrenceCount} psaume${t.occurrenceCount>1?'s':''}</small></span><span>${t.score}</span></button>`).join(''):'<div class="empty">Aucun thème ne correspond à ce filtre.</div>'; $('themeDirectory').querySelectorAll('[data-directory-theme]').forEach(b=>b.onclick=()=>{const t=state.themeById.get(b.dataset.directoryTheme);if(t){closeIndex();navigateToTheme(t);}}); }
  function openIndex(){ renderThemeDirectory(); $('indexPanel').hidden=false;$('indexBackdrop').hidden=false;$('indexToggle').setAttribute('aria-expanded','true'); requestAnimationFrame(()=>$('themeFilter').focus()); }
  function closeIndex(){$('indexPanel').hidden=true;$('indexBackdrop').hidden=true;$('indexToggle').setAttribute('aria-expanded','false');}

  $('searchButton').onclick=search; $('query').addEventListener('keydown',e=>{if(e.key==='Enter')search();}); $('query2').addEventListener('keydown',e=>{if(e.key==='Enter')search();}); document.querySelectorAll('[name=sourceType]').forEach(x=>x.onchange=search); $('archangelFilter').onchange=search;
  $('modeThemes').onclick=()=>{activateThemeMode();search();}; $('modeExact').onclick=()=>{activateExactMode();search();}; $('closeAmbiguity').onclick=hideAmbiguity;
  $('indexToggle').onclick=()=>{$('indexPanel').hidden?openIndex():closeIndex();}; $('themeFilter').oninput=renderThemeDirectory; $('closeIndex').onclick=closeIndex; $('indexBackdrop').onclick=closeIndex; $('closeDialog').onclick=()=>$('recordDialog').close(); $('printRecord').onclick=()=>window.print(); $('downloadRecord').onclick=()=>{const blob=new Blob([activeText()],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${state.active?.id||'biblaw'}.txt`;a.click();URL.revokeObjectURL(a.href);};
  load();
})();
