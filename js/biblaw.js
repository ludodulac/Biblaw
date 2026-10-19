(() => {
  const $ = id => document.getElementById(id);
  const state = { mode: 'themes', records: [], recordById: new Map(), psalmsByNumber: new Map(), normalizedFragmentsById: new Map(), themeDirectory: [], themeById: new Map(), themesByRecord: new Map(), lexicalExpansionGroups: [], lexicalExpansionByForm: new Map(), semanticBrowserRuntime: null, semanticTargetsByForm: new Map(), semanticSelection: null, grammarByForm: new Map(), grammarSelection: null, runtime: null, themeEngine: null, active: null, resolvedThemes: [], hasSearched: false, suggestionEntries: [], wordEntries: [], wordKeys: new Set(), wordIndexReady:false, autocompleteItems:[], autocompleteMode:null, autocompleteWindowStart:-1 };
  const POPULAR_QUESTION_FAMILIES = [
    { id:'existence', label:'Existence, sens et raison de vivre', questions:[
      { id:'Q001', text:'Pourquoi existons-nous ?' },
      { id:'Q002', text:'Quel est le sens de la vie ?' }
    ]},
    { id:'mort', label:'Mort et après-mort', questions:[
      { id:'Q036', text:'Pourquoi avons-nous peur de mourir ?' },
      { id:'Q037', text:'Que se passe-t-il lorsque nous mourons ?' }
    ]},
    { id:'nature', label:'Nature, animaux, Terre et écologie', questions:[
      { id:'Q114', text:"Quelle est la place de l'être humain dans la nature ?" },
      { id:'Q115', text:"La nature a-t-elle une valeur indépendamment de son utilité pour l'être humain ?" }
    ]}
  ];
  const norm = value => BiblawThemeEngine.norm(value);
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  function singleWordQueryKey(value){ const key=norm(value); return key&&!key.includes(' ')?key:null; }
  function expansionFormsFor(value){ const key=singleWordQueryKey(value); if(!key)return[]; const groupIndex=state.lexicalExpansionByForm.get(key); if(groupIndex===undefined)return[]; return (state.lexicalExpansionGroups[groupIndex]||[]).filter(form=>form!==key); }
  // 052B: attested -s pairs, separate from opt-in validated morphology.
  function simplePluralFormsFor(value){
    const key=singleWordQueryKey(value);
    if(!key||key.length<3)return[];
    if(key.endsWith('s')){
      const singular=key.slice(0,-1);
      return singular.length>=3&&state.wordKeys.has(singular)?[singular]:[];
    }
    const plural=key+'s';
    return state.wordKeys.has(plural)?[plural]:[];
  }
  function activeExpansionForms(){
    if(state.mode!=='exact')return[];
    const query=$('query')?.value||'';
    const simple=$('includeSimplePlurals')?.checked?simplePluralFormsFor(query):[];
    const verified=$('includeWordForms')?.checked?expansionFormsFor(query):[];
    return [...new Set([...simple,...verified])];
  }
  function updateExpansionControl(){ const option=$('exactExpansionOption'),checkbox=$('includeWordForms'); if(!option||!checkbox)return; const key=state.mode==='exact'?singleWordQueryKey($('query')?.value||''):null,expansions=key?expansionFormsFor(key):[]; const analyses=state.grammarByForm.get(key)||[]; const available=Boolean(key&&expansions.length); const enabled=available; option.hidden=!enabled; checkbox.disabled=!enabled; const label=option.querySelector('label span'); if(label){ const pos=analyses.length===1?analyses[0].partOfSpeech:null; label.textContent=pos==='NOUN'?'Inclure singulier et pluriel vérifiés':pos==='VERB'?'Inclure les formes verbales vérifiées':'Inclure les formes morphologiques vérifiées'; } if(!enabled)checkbox.checked=false; }
  const queryTerms = () => { const terms=new Set([$('query')?.value, $('query2')?.value].flatMap(value => norm(value).split(' ')).filter(Boolean)); for(const form of activeExpansionForms())terms.add(form); return terms; };
  const highlighted = value => { const terms=queryTerms(); if(!terms.size)return esc(value); return String(value||'').split(/([\p{L}\p{N}œŒæÆ’'-]+)/gu).map(part=>terms.has(norm(part))?`<mark class="search-hit">${esc(part)}</mark>`:esc(part)).join(''); };
  const modeAwareText = value => state.mode==='exact' ? highlighted(value) : esc(value);
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const textFragments = r => r.recordType === 'psalm' ? [r.title, ...(r.verses || []).map(v => v.text)].filter(Boolean) : [r.title, r.text, r.summary].filter(Boolean);
  const literalIncludes = (value, query) => literalOccurrenceCount({id:'__temporary',_literal:value},query)>0;
  const literalOccurrenceCount = (r, query) => {
    const needle=norm(query); if(!needle)return 0;
    const fragments=r._literal!==undefined?[norm(r._literal)]:(state.normalizedFragmentsById.get(r.id)||[]);
    if(!singleWordQueryKey(query)){
      const boundedNeedle=' '+needle+' ';
      return fragments.reduce((total,fragment)=>{
        const haystack=' '+fragment+' ';let count=0,from=0,index;
        while((index=haystack.indexOf(boundedNeedle,from))!==-1){count++;from=index+boundedNeedle.length;}
        return total+count;
      },0);
    }
    return fragments.reduce((total,fragment)=>total+[...fragment.matchAll(/[\p{L}\p{N}]+(?:[’'][\p{L}\p{N}]+)*/gu)].filter(m=>m[0]===needle).length,0);
  };
  const literalTextMatch = (r, needle) => literalOccurrenceCount(r,needle)>0;
  const parsePsalmNumberQuery = value => { const match=norm(value).match(/^(?:psaume\s+)?([0-9]{1,4})$/); if(!match)return null; const number=Number(match[1]); return Number.isInteger(number)&&number>0?number:null; };
  const selectedTypes = () => new Set([...document.querySelectorAll('[name=sourceType]:checked')].map(x => x.value));
  const archangelName = value => ({ michael: 'Michaël', gabriel: 'Gabriel', raphael: 'Raphaël', ouriel: 'Ouriel' }[value] || value || '');
  const label = r => r.recordType === 'psalm' ? `Psaume ${r.number} · ${archangelName(r.archangel)}` : r.recordType === 'master-prayer' ? `Prière ${r.number} · ${archangelName(r.archangel)}` : `Note · ${archangelName(r.archangel)}`;
  const importanceLabel = value => ({ central: 'Central', important: 'Important', related: 'Lié' }[value] || 'Indexé');
  const importanceRank = value => ({ central: 0, important: 1, related: 2 }[value] ?? 3);
  const publishPresentationState = detail => document.dispatchEvent(new CustomEvent('biblaw:presentation-state', { detail }));
  const activateThemeMode = () => { state.mode='themes'; state.semanticSelection=null; state.grammarSelection=null; $('modeThemes').classList.add('active'); $('modeExact').classList.remove('active'); $('primarySearch').classList.remove('exact-mode'); $('query2').disabled=false; $('advancedSearchToggle').hidden=false; $('query').placeholder='Rechercher un thème…'; $('simplePluralOption').hidden=true; $('popularThemes').hidden=false; $('modeThemes').setAttribute('aria-pressed','true'); $('modeExact').setAttribute('aria-pressed','false'); hideThemeAutocomplete(); hideAmbiguity(); updateExpansionControl(); };
  const activateExactMode = () => { state.mode='exact'; $('modeExact').classList.add('active'); $('modeThemes').classList.remove('active'); $('primarySearch').classList.add('exact-mode'); $('primarySearch').classList.remove('advanced-visible'); $('query2').disabled=true; $('query2').value=''; $('advancedSearchToggle').hidden=true; $('advancedSearchToggle').setAttribute('aria-expanded','false'); $('advancedSearchToggle').textContent='Croiser deux thèmes'; $('query').placeholder='Rechercher des mots…'; $('simplePluralOption').hidden=false; $('popularThemes').hidden=true; $('modeThemes').setAttribute('aria-pressed','false'); $('modeExact').setAttribute('aria-pressed','true'); hideThemeAutocomplete(); hideAmbiguity(); hideTransverseNavigation(); updateExpansionControl(); };

  async function load() {
    try {
      const [bundle, directory, runtime, lexicalExpansion, semanticBrowserRuntime, grammarBrowserRuntime] = await Promise.all([
        fetch('data/browser-search-catalog.json').then(r => { if (!r.ok) throw Error('browser-search-catalog'); return r.json(); }),
        fetch('data/thematic-index/theme-directory-public.json').then(r => { if (!r.ok) throw Error('theme-directory'); return r.json(); }),
        fetch('data/thematic-index/theme-search-runtime.json').then(r => { if (!r.ok) throw Error('theme-search-runtime'); return r.json(); }),
        fetch('data/lexical-expansion-runtime.json').then(r => { if (!r.ok) throw Error('lexical-expansion-runtime'); return r.json(); }),
        Promise.resolve({targets:[]}),
        fetch('data/linguistic-grammar-browser-runtime.json').then(r => { if (!r.ok) throw Error('linguistic-grammar-browser-runtime'); return r.json(); })
      ]);
      state.themeDirectory = directory.themes || [];
      state.themeById = new Map(state.themeDirectory.map(t => [t.id, t]));
      state.runtime = runtime;
      state.lexicalExpansionGroups = lexicalExpansion.g || [];
      state.lexicalExpansionByForm = new Map();
      state.lexicalExpansionGroups.forEach((group,index)=>group.forEach(form=>state.lexicalExpansionByForm.set(form,index)));
      state.semanticBrowserRuntime = null;
      state.grammarByForm = new Map((grammarBrowserRuntime.forms||[]).map(form=>[form.normalizedForm,form.analyses]));
      state.semanticTargetsByForm = new Map();
      for(const target of [] ){ const list=state.semanticTargetsByForm.get(target.normalizedForm)||[]; list.push(target); state.semanticTargetsByForm.set(target.normalizedForm,list); }
      state.themeEngine = BiblawThemeEngine.create(state.themeDirectory, state.runtime);
      buildSuggestionLookup();
      renderPopularThemes();
      state.records = bundle.records || [];
      state.recordById = new Map(state.records.map(r => [r.id, r]));
      state.psalmsByNumber = new Map();
      state.normalizedFragmentsById = new Map();
      for (const r of state.records) {
        state.normalizedFragmentsById.set(r.id,textFragments(r).map(norm).filter(Boolean));
        if (r.recordType === 'psalm') { const number=Number(r.number), list=state.psalmsByNumber.get(number)||[]; list.push(r); state.psalmsByNumber.set(number,list); }
      }
      buildWordSuggestionLookup().catch(error=>console.error('BIBLAW suggestion index:',error));
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
      updateExpansionControl();
    } catch (error) { console.error(error); $('resultsSection').hidden=false; $('resultCount').textContent=''; $('results').innerHTML = '<div class="empty">Chargement impossible.</div>'; }
  }

  function matches(query) { const allowed=selectedTypes(),a=$('archangelFilter').value; return state.records.filter(r=>allowed.has(type(r))&&(!a||r.archangel===a)).map(record=>({record,score:1,occurrenceCount:literalOccurrenceCount(record,query)})).filter(item=>item.occurrenceCount>0); }
  function mergeExpansionMatches(items,query,matchSource=matches){ const forms=activeExpansionForms(); if(!forms.length||!singleWordQueryKey(query))return items; const byId=new Map(items.map(item=>[item.record.id,item])); for(const form of forms)for(const item of matchSource(form)){ const current=byId.get(item.record.id); if(current)current.occurrenceCount+=item.occurrenceCount; else byId.set(item.record.id,item); } items.splice(0,items.length,...byId.values()); return items; }
  function psalmNumberMatches(number) { if(!selectedTypes().has('psalm'))return []; const a=$('archangelFilter').value; return (state.psalmsByNumber.get(number)||[]).filter(r=>!a||r.archangel===a).sort((x,y)=>(x.book?.number||9999)-(y.book?.number||9999)||String(x.id).localeCompare(String(y.id),'fr')).map(record=>({record,score:1,numberLookup:true})); }
  function textualPsalmMatches(query) { return matches(query).filter(x=>x.record.recordType==='psalm'); }
  function resolveIndexedThemes(query) { return state.themeEngine?.resolveIndexedThemes(query) || []; }
  const composeThemeQueryNotions = query => BiblawThemeEngine.composeThemeQueryNotions(query);
  const themeQueryNotions = query => BiblawThemeEngine.themeQueryNotions(query);
  function suggestIndexedThemes(query) { return state.themeEngine?.suggestIndexedThemes(query) || []; }
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
  function semanticTargetsFor(value){ const key=state.mode==='exact'?singleWordQueryKey(value):null; return key?(state.semanticTargetsByForm.get(key)||[]):[]; }
  function semanticSelectionContext(value=$('query')?.value||''){
    if(!state.semanticSelection)return null;
    const key=singleWordQueryKey(value);
    if(!key||key!==state.semanticSelection.normalizedForm)return null;
    const target=(state.semanticTargetsByForm.get(key)||[]).find(item=>item.lemma===state.semanticSelection.lemma&&item.partOfSpeech===state.semanticSelection.partOfSpeech);
    const sense=target?.senses?.find(item=>item.senseId===state.semanticSelection.senseId);
    return target&&sense?{target,sense}:null;
  }
  function handleExactQueryInput(){
    if(state.mode!=='exact'){updateExpansionControl();return;}
    const key=singleWordQueryKey($('query')?.value||'');
    if(state.semanticSelection&&key!==state.semanticSelection.normalizedForm)state.semanticSelection=null;
    if(state.grammarSelection&&key!==state.grammarSelection.normalizedForm)state.grammarSelection=null;
    if(!key||(!semanticTargetsFor(key).length&&!state.grammarByForm.has(key)))hideAmbiguity();
    updateExpansionControl();
  }

  function grammarAnalysesFor(value){
    const key=state.mode==='exact'?singleWordQueryKey(value):null;
    return key?(state.grammarByForm.get(key)||[]):[];
  }
  function grammarSelectionContext(value){
    const key=singleWordQueryKey(value),selection=state.grammarSelection;
    if(!selection||selection.normalizedForm!==key)return null;
    return grammarAnalysesFor(value).find(a=>a.lemma===selection.lemma&&a.partOfSpeech===selection.partOfSpeech)||null;
  }
  function grammarMatches(analysis){
    const allowed=selectedTypes(),archangel=$('archangelFilter').value,items=[];
    for(const [recordId,occurrenceCount,verseNumbers] of analysis.records||[]){
      const record=state.recordById.get(recordId);
      if(!record||!allowed.has(type(record))||(archangel&&record.archangel!==archangel))continue;
      items.push({record,score:1,occurrenceCount,semanticVerseNumbers:verseNumbers});
    }
    return items;
  }
  function showGrammarChoices(query){
    const key=singleWordQueryKey(query),analyses=grammarAnalysesFor(query);
    if(state.mode!=='exact'||analyses.length<=1||grammarSelectionContext(query)){return false;}
    const choices=['<button class="sense-button" data-grammar-all><strong>Toutes les occurrences</strong><span>Recherche exacte sans filtre grammatical</span></button>'];
    analyses.forEach((a,i)=>choices.push(`<button class="sense-button" data-grammar-index="${i}"><strong>${esc(a.lemma.toUpperCase())} — ${a.partOfSpeech==='NOUN'?'nom':a.partOfSpeech==='VERB'?'verbe':a.partOfSpeech}</strong><span>${a.occurrenceCount} occurrences</span></button>`));
    $('suggestionKicker').textContent='Préciser la recherche';
    $('suggestionTitle').textContent=`Que recherchez-vous pour « ${query} » ?`;
    $('senseChoices').innerHTML=choices.join('');
    $('senseChoices').querySelector('[data-grammar-all]').onclick=()=>{state.grammarSelection=null;state.semanticSelection=null;search();};
    $('senseChoices').querySelectorAll('[data-grammar-index]').forEach(btn=>btn.onclick=()=>{
      const analysis=analyses[Number(btn.dataset.grammarIndex)];
      if(!analysis)return;
      state.grammarSelection={normalizedForm:key,lemma:analysis.lemma,partOfSpeech:analysis.partOfSpeech};
      const sourceTypes=new Set((analysis.records||[]).map(([id])=>state.recordById.get(id)).filter(Boolean).map(type));
      document.querySelectorAll('[name=sourceType]').forEach(input=>{if(sourceTypes.has(input.value))input.checked=true;});
      state.semanticSelection=null;
      if($('includeWordForms'))$('includeWordForms').checked=false;
      search();
    });
    $('ambiguityPanel').hidden=false;
    return true;
  }
  function semanticChoicesAllowed(query){
    const analyses=grammarAnalysesFor(query);
    if(analyses.length<=1)return true;
    const chosen=grammarSelectionContext(query);
    if(!chosen)return false;
    return semanticTargetsFor(query).some(t=>t.lemma===chosen.lemma&&t.partOfSpeech===chosen.partOfSpeech&&(t.senses||[]).length>1);
  }
  function showSemanticChoices(query){
    const key=singleWordQueryKey(query),chosen=grammarSelectionContext(query),targets=semanticTargetsFor(query).filter(t=>!chosen||(t.lemma===chosen.lemma&&t.partOfSpeech===chosen.partOfSpeech));
    if(!semanticChoicesAllowed(query)||state.mode!=='exact'||!key||!targets.length){hideAmbiguity();return false;}
    const choices=['<button class="sense-button" data-semantic-all><strong>Toutes les occurrences</strong><span>Recherche exacte sans filtre de sens</span></button>'];
    targets.forEach((target,targetIndex)=>(target.senses||[]).filter(sense=>sense.occurrenceCount>0).forEach(sense=>{
      choices.push(`<button class="sense-button" data-semantic-target-index="${targetIndex}" data-semantic-sense-id="${esc(sense.senseId)}"><strong>${esc(sense.label)}</strong><span>${sense.occurrenceCount} occurrence${sense.occurrenceCount>1?'s':''} validée${sense.occurrenceCount>1?'s':''}</span></button>`);
    }));
    const uncertain=targets.reduce((sum,target)=>sum+(target.uncertainOccurrenceCount||0),0);
    if(uncertain)choices.push(`<div class="muted">${uncertain} occurrence${uncertain>1?'s':''} validée${uncertain>1?'s':''} reste${uncertain>1?'nt':''} indéterminée${uncertain>1?'s':''}.</div>`);
    $('suggestionKicker').textContent='Préciser la recherche';
    $('suggestionTitle').textContent=`Quel sens de « ${query} » recherchez-vous ?`;
    $('senseChoices').innerHTML=choices.join('');
    $('senseChoices').querySelector('[data-semantic-all]').onclick=()=>{state.semanticSelection=null;updateExpansionControl();search();};
    $('senseChoices').querySelectorAll('[data-semantic-sense-id]').forEach(btn=>btn.onclick=()=>{
      const target=targets[Number(btn.dataset.semanticTargetIndex)],sense=target?.senses?.find(item=>item.senseId===btn.dataset.semanticSenseId);
      if(!target||!sense)return;
      state.semanticSelection={normalizedForm:key,lemma:target.lemma,partOfSpeech:target.partOfSpeech,senseId:sense.senseId};
      if($('includeWordForms'))$('includeWordForms').checked=false;
      updateExpansionControl();
      search();
    });
    $('ambiguityPanel').hidden=false;
    return true;
  }
  function semanticMatches(selection){
    const allowed=selectedTypes(),a=$('archangelFilter').value,items=[];
    for(const [recordId,occurrenceCount,verseNumbers] of selection.sense.records||[]){
      const record=state.recordById.get(recordId);
      if(!record||!allowed.has(type(record))||(a&&record.archangel!==a))continue;
      items.push({record,score:1,occurrenceCount,semanticVerseNumbers:verseNumbers||[]});
    }
    return items;
  }
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
  function showThemeSuggestions(themes) {
    state.resolvedThemes=themes;
    $('suggestionKicker').textContent='Thèmes correspondant à votre recherche'; $('suggestionTitle').textContent='Choisissez le sens qui vous intéresse';
    $('senseChoices').innerHTML=themes.map(theme=>ambiguityChoice(theme,'query')).join('');
    $('senseChoices').querySelectorAll('[data-ambiguity-target]').forEach(btn=>btn.onclick=()=>navigateToTheme(state.themeById.get(btn.dataset.themeId)));
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
    if(!theme)return; state.hasSearched=true; $('resultsSection').hidden=false; activateThemeMode(); $('query').value=theme.label; $('query2').value=''; if($('recordDialog').open)$('recordDialog').close();
    const thematic=thematicItems([theme]), textual=textualPsalmMatches(theme.label); hideAmbiguity(); showTransverseNavigation(theme);
    publishPresentationState({kind:'canonical-theme',theme:{id:theme.id,label:theme.label},psalmCount:thematic.length});
    render(thematic,[theme],{textualCount:textual.length}); window.scrollTo({top:0,behavior:'smooth'});
  }


  // 053: index only expressions copied verbatim from documentary fragments.
  // No generated/plausible language combinations; the existing consecutive-phrase search is unchanged.
  async function buildWordSuggestionLookup(){
    let chunkStart=performance.now(),lastPublishedAt=0;
    const words=new Map(),expressions=new Map();
    const connectors=new Set(['de','du','des','au','aux','a','en','et','avec','pour','sans','sur','sous','entre','par']);
    const articles=new Set(['le','la','les','l','un','une','des']);
    const numberWords=new Set(['deux','trois','quatre','cinq','six','sept','huit','neuf','dix','douze']);
    const add=(map,value)=>{
      const key=norm(value);
      if(key.length<2||!key.includes(' ')&&/^\d+$/.test(key))return;
      const display=String(value).trim(),identity=display.toLocaleLowerCase('fr');
      const old=map.get(identity);
      if(old){old.count++;return;}
      map.set(identity,{key,word:display,count:1,expression:map===expressions});
    };
    for(const record of state.records)for(const fragment of textFragments(record)){
      const source=String(fragment);
      // Apostrophes remain attached to their word, hyphens remain exact source separators.
      const tokens=[...source.matchAll(/[\p{L}\p{N}]+(?:[’'][\p{L}\p{N}]+)*/gu)].map(match=>({
        word:match[0],start:match.index,end:match.index+match[0].length,key:norm(match[0])
      }));
      for(let i=0;i<tokens.length;i++){
        // Single words continue to behave exactly as in 052B (including apostrophe components).
        for(const word of (tokens[i].word.match(/[\p{L}\p{N}]+/gu)||[])){
          const key=norm(word);
          if(key.length>=2&&!/^\d+$/.test(key))add(words,word.toLocaleLowerCase('fr'));
        }
        const first=tokens[i];
        if(first.key.length<2&&!/^\d+$/u.test(first.word)||articles.has(first.key)||connectors.has(first.key))continue;
        let hasHyphen=false;
        for(let j=i+1;j<tokens.length&&j<=i+3;j++){
          const separator=source.slice(tokens[j-1].end,tokens[j].start);
          if(!/^(?:\s+|[-‐‑–])$/u.test(separator))break; // never cross punctuation/sentences
          if(/[-‐‑–]/u.test(separator))hasHyphen=true;
          const last=tokens[j],count=j-i+1;
          if(last.key.length<2||articles.has(last.key)||connectors.has(last.key))continue;
          const numberStart=/^\d+$/u.test(first.word)||numberWords.has(first.key);
          const inner=tokens.slice(i+1,j).map(token=>token.key);
          const prepositional=count===3&&connectors.has(inner[0])||count===4&&connectors.has(inner[0])&&articles.has(inner[1]);
          // Recognizable attested compounds: hyphens, numbers, and connected noun phrases.
          if(!hasHyphen&&!numberStart&&!prepositional)continue;
          const phrase=source.slice(first.start,last.end);
          if(phrase.length<=80)add(expressions,phrase);
        }
      }
      if(performance.now()-chunkStart>12){
        // Publish real attested words progressively so typing works before the
        // entire corpus and all compound expressions have been indexed.
        if(state.mode==='exact'&&norm($('query').value).length>=2&&performance.now()-lastPublishedAt>90){
          state.wordEntries=[...words.values(),...expressions.values()];
          renderWordAutocomplete();
          lastPublishedAt=performance.now();
        }
        await new Promise(resolve=>setTimeout(resolve,0));
        chunkStart=performance.now();
      }
    }
    state.wordEntries=[...words.values(),...expressions.values()];
    state.wordKeys=new Set([...words.values()].map(entry=>entry.key));
    state.wordIndexReady=true;
    $('query').dataset.wordSuggestionsReady='true';
    if(state.mode==='exact'&&norm($('query').value).length>=2)renderThemeAutocomplete();
  }
  function findAutocompleteWords(input){
    const query=norm(input);
    if(query.length<2)return[];
    return state.wordEntries.filter(entry=>entry.key.includes(query))
      .sort((a,b)=>(a.key.startsWith(query)?0:1)-(b.key.startsWith(query)?0:1)
        ||(a.expression?1:0)-(b.expression?1:0)||b.count-a.count||a.word.localeCompare(b.word,'fr'));
  }
  function renderWordAutocomplete(){
    const query=norm($('query').value);
    if(query.length<2){hideThemeAutocomplete();return;}
    const words=findAutocompleteWords($('query').value);
    if(!state.wordIndexReady&&!words.length){
      // 053C: do not silently suppress the dropdown during progressive indexing.
      const box=$('themeAutocomplete');
      state.autocompleteItems=[];
      state.autocompleteMode=null;
      state.autocompleteWindowStart=-1;
      box.setAttribute('aria-label','Préparation des suggestions du corpus');
      box.innerHTML='<div class="autocomplete-count" role="status">Recherche des suggestions dans les psaumes…</div>';
      box.hidden=false;
      $('query').setAttribute('aria-expanded','true');
      return;
    }
    showSuggestionList(words,'words','Mots et expressions du corpus suggérés');
  }

  // 052: autocomplete only proposes labels and registered aliases from the published index.
  function buildSuggestionLookup(){
    const entries=[];
    for(const theme of state.themeDirectory)entries.push({id:theme.id,key:norm(theme.label),alias:false});
    for(const [alias,entry] of Object.entries(state.runtime?.aliases||{})){
      for(const id of entry.themeIds||[])if(state.themeById.has(id))entries.push({id,key:norm(alias),alias:true});
    }
    state.suggestionEntries=entries.filter(item=>item.key);
  }
  function findAutocompleteThemes(input){
    const query=norm(input);
    if(query.length<2)return[];
    const matches=new Map();
    for(const entry of state.suggestionEntries){
      const position=entry.key.indexOf(query);
      if(position<0)continue;
      const theme=state.themeById.get(entry.id);
      if(!theme)continue;
      const rank=(position===0?0:2)+(entry.alias?1:0);
      if(!matches.has(entry.id)||rank<matches.get(entry.id).rank)matches.set(entry.id,{theme,rank});
    }
    return [...matches.values()].sort((a,b)=>a.rank-b.rank||a.theme.label.localeCompare(b.theme.label,'fr')||a.theme.id.localeCompare(b.theme.id,'fr')).map(item=>item.theme);
  }
  // 054: every suggestion remains reachable, with only a few DOM rows rendered.
  // Rendering 8 000+ buttons at once froze Android browsers in the 053 preview.
  const AUTOCOMPLETE_ROW_HEIGHT=64;
  const AUTOCOMPLETE_HEADER_HEIGHT=32;
  const AUTOCOMPLETE_VISIBLE_ROWS=18;
  function hideThemeAutocomplete(){
    const box=$('themeAutocomplete');
    box.hidden=true;
    box.replaceChildren();
    box.removeAttribute('data-total-suggestions');
    state.autocompleteItems=[];
    state.autocompleteMode=null;
    state.autocompleteWindowStart=-1;
    $('query').setAttribute('aria-expanded','false');
  }
  function chooseAutocompleteTheme(theme){
    if(!theme)return;
    $('query').value=theme.label;
    $('query2').value='';
    hideThemeAutocomplete();
    search();
  }
  function chooseSuggestion(index){
    const item=state.autocompleteItems[index];
    if(!item)return;
    if(state.autocompleteMode==='themes'){chooseAutocompleteTheme(item);return;}
    $('query').value=item.word;
    hideThemeAutocomplete();
    search(); // The established phrase matcher still handles the entire consecutive expression.
  }
  function renderSuggestionWindow(force=false){
    const box=$('themeAutocomplete'),items=state.autocompleteItems;
    if(box.hidden||!items.length)return;
    const visibleStart=Math.floor(Math.max(0,box.scrollTop-AUTOCOMPLETE_HEADER_HEIGHT)/AUTOCOMPLETE_ROW_HEIGHT);
    const visibleEnd=Math.ceil(Math.max(0,box.scrollTop+box.clientHeight-AUTOCOMPLETE_HEADER_HEIGHT)/AUTOCOMPLETE_ROW_HEIGHT);
    const current=state.autocompleteWindowStart;
    // Preserve stable DOM nodes while a user is tapping one of the visible rows.
    // Rebuild only after scrolling beyond a buffered rendering window.
    if(!force&&current>=0&&visibleStart>=current+2&&visibleEnd<current+AUTOCOMPLETE_VISIBLE_ROWS-2)return;
    const first=Math.max(0,Math.min(Math.max(0,items.length-AUTOCOMPLETE_VISIBLE_ROWS),visibleStart-7));
    if(!force&&first===current)return;
    state.autocompleteWindowStart=first;
    const end=Math.min(items.length,first+AUTOCOMPLETE_VISIBLE_ROWS);
    const before=box.querySelector('[data-suggest-before]'),after=box.querySelector('[data-suggest-after]');
    const rows=box.querySelector('[data-suggest-rows]');
    before.style.height=(first*AUTOCOMPLETE_ROW_HEIGHT)+'px';
    after.style.height=((items.length-end)*AUTOCOMPLETE_ROW_HEIGHT)+'px';
    const wordMode=state.autocompleteMode==='words',attr=wordMode?'data-autocomplete-word':'data-autocomplete-theme';
    rows.innerHTML=items.slice(first,end).map((item,i)=>{
      const index=first+i,label=wordMode?item.word:item.label,identity=wordMode?item.word:item.id;
      return '<button type="button" role="option" data-suggestion-index="'+index+'" '+attr+'="'+esc(identity)+'" aria-selected="false" aria-posinset="'+(index+1)+'" aria-setsize="'+items.length+'" title="'+esc(label)+'">'+esc(label)+'</button>';
    }).join('');
    rows.querySelectorAll('[data-suggestion-index]').forEach(button=>{
      button.onclick=()=>chooseSuggestion(Number(button.dataset.suggestionIndex));
      button.onkeydown=event=>{
        const index=Number(button.dataset.suggestionIndex);
        if(event.key==='ArrowDown'){event.preventDefault();focusSuggestion(Math.min(items.length-1,index+1));}
        if(event.key==='ArrowUp'){event.preventDefault();index===0?$('query').focus():focusSuggestion(index-1);}
        if(event.key==='Escape'){event.preventDefault();hideThemeAutocomplete();$('query').focus();}
      };
    });
  }
  function focusSuggestion(index){
    const box=$('themeAutocomplete');
    if(box.hidden||!state.autocompleteItems.length)return;
    const y=AUTOCOMPLETE_HEADER_HEIGHT+index*AUTOCOMPLETE_ROW_HEIGHT;
    if(y<box.scrollTop+AUTOCOMPLETE_HEADER_HEIGHT)box.scrollTop=Math.max(0,y-AUTOCOMPLETE_HEADER_HEIGHT);
    else if(y+AUTOCOMPLETE_ROW_HEIGHT>box.scrollTop+box.clientHeight)box.scrollTop=y+AUTOCOMPLETE_ROW_HEIGHT-box.clientHeight;
    renderSuggestionWindow(true);
    box.querySelector('[data-suggestion-index="'+index+'"]')?.focus();
  }
  function showSuggestionList(items,mode,label){
    if(!items.length){hideThemeAutocomplete();return;}
    const box=$('themeAutocomplete');
    state.autocompleteItems=items;
    state.autocompleteMode=mode;
    state.autocompleteWindowStart=-1;
    box.setAttribute('aria-label',label);
    box.dataset.totalSuggestions=String(items.length);
    box.innerHTML='<div class="autocomplete-count" role="presentation">'+items.length.toLocaleString('fr-FR')+' suggestions · défilez pour tout voir</div><div data-suggest-before aria-hidden="true"></div><div data-suggest-rows></div><div data-suggest-after aria-hidden="true"></div>';
    box.hidden=false;
    box.scrollTop=0;
    renderSuggestionWindow(true);
    $('query').setAttribute('aria-expanded','true');
  }
  function renderThemeAutocomplete(){
    if(state.mode==='exact'){renderWordAutocomplete();return;}
    if(state.mode!=='themes'||$('query2').value.trim()){hideThemeAutocomplete();return;}
    showSuggestionList(findAutocompleteThemes($('query').value),'themes','Thèmes indexés suggérés');
  }
  $('themeAutocomplete').addEventListener('scroll',()=>renderSuggestionWindow(),{passive:true});
  function renderPopularThemes(){
    const preferred=['amour','nature','ame','guerison','equilibre'];
    const seen=new Set(),chosen=[];
    const candidates=[...preferred.map(key=>state.themeDirectory.find(theme=>norm(theme.label)===key)).filter(Boolean),...state.themeDirectory.slice().sort((a,b)=>(b.occurrenceCount||0)-(a.occurrenceCount||0)||a.label.localeCompare(b.label,'fr'))];
    for(const theme of candidates){
      if(seen.has(theme.id))continue;
      seen.add(theme.id);chosen.push(theme);
      if(chosen.length===5)break;
    }
    $('popularThemes').innerHTML=chosen.map(theme=>`<button type="button" class="popular-theme-chip" data-popular-theme="${esc(theme.id)}">${esc(theme.label)}</button>`).join('');
    $('popularThemes').querySelectorAll('[data-popular-theme]').forEach(button=>button.onclick=()=>chooseAutocompleteTheme(state.themeById.get(button.dataset.popularTheme)));
  }
  function clearSearchDisplay(){
    state.hasSearched=false;
    $('resultsSection').hidden=true;
    $('resultCount').textContent='';
    $('results').replaceChildren();
    hideAmbiguity();hideTransverseNavigation();
    publishPresentationState({kind:'no-result'});
  }
  function bindNearThemeChoices(){
    $('results').querySelectorAll('[data-near-theme]').forEach(button=>button.onclick=()=>chooseAutocompleteTheme(state.themeById.get(button.dataset.nearTheme)));
  }

  function search(){
    hideThemeAutocomplete();
    const query=$('query').value.trim(), query2=$('query2').value.trim();
    if(!query){clearSearchDisplay();return;}
    state.hasSearched=true;
    $('resultsSection').hidden=false;
    const semanticKey=singleWordQueryKey(query);
    if(state.semanticSelection&&semanticKey!==state.semanticSelection.normalizedForm)state.semanticSelection=null;
    updateExpansionControl();
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
      if(resolved.length>1){
        showSingleThemeAmbiguity(resolved); const thematic=thematicItems(resolved), textual=textualPsalmMatches(query); hideTransverseNavigation();
        publishPresentationState({kind:'ambiguous-themes',themes:resolved.map(theme=>({id:theme.id,label:theme.label}))});
        return render(thematic,resolved,{textualCount:textual.length});
      }
      const suggestions=suggestIndexedThemes(query);
      if(suggestions.length>1){ showThemeSuggestions(suggestions); hideTransverseNavigation(); publishPresentationState({kind:'ambiguous-themes',themes:suggestions.map(theme=>({id:theme.id,label:theme.label}))}); return render([],[],{suggestionPending:true}); }
      const selected=resolved[0]||(suggestions.length===1?suggestions[0]:null);
      if(selected){
        hideAmbiguity(); const thematic=thematicItems([selected]), textual=textualPsalmMatches(query); showTransverseNavigation(selected);
        publishPresentationState({kind:'canonical-theme',theme:{id:selected.id,label:selected.label},psalmCount:thematic.length});
        return render(thematic,[selected],{textualCount:textual.length});
      }
      hideAmbiguity();hideTransverseNavigation(); const textual=textualPsalmMatches(query); publishPresentationState({kind:textual.length?'textual-fallback':'no-result'}); return render([],[],{textualCount:textual.length,unresolvedTheme:true,textualAvailable:Boolean(textual.length)});
    }
    hideTransverseNavigation();publishPresentationState({kind:'other'});
    const semanticSelection=semanticSelectionContext(query);
    const grammaticalSelection=grammarSelectionContext(query);
    const exactItems=matches(query);
    // 040A: grammatical analyses inform expansion safety, never filter exact matches.
    // 040A: no semantic filtering of exact occurrences.
    mergeExpansionMatches(exactItems,query);
    exactItems.sort((a,b)=>b.occurrenceCount-a.occurrenceCount||(Number(a.record.number)||Number.MAX_SAFE_INTEGER)-(Number(b.record.number)||Number.MAX_SAFE_INTEGER)||String(a.record.id).localeCompare(String(b.record.id),'fr'));
    hideAmbiguity(); // 040A: exact results never require sense or grammar choice.
    render(exactItems,null,{exactSearch:true});
  }

  function summary(r){return r.recordType==='psalm'?(r.verses||[]).slice(0,2).map(v=>v.text).join(' '):r.summary||(r.text||'').slice(0,280);}
  function contextualVerses(r,thematic){ if(!thematic?.verseNumbers?.length||!r.verses?.length)return''; const wanted=new Set(thematic.verseNumbers.map(Number)); const chosen=r.verses.filter(v=>wanted.has(Number(v.number))).slice(0,4); if(!chosen.length)return''; return `<div class="theme-context"><div class="context-label">Passage concerné</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${esc(v.text)}</span></div>`).join('')}</div>`; }
  function exactVerses(r){ if(r.recordType!=='psalm'||!r.verses?.length)return''; const query=$('query').value; if(!norm(query))return''; const semantic=semanticSelectionContext(query); let chosen; if(semantic){ const row=(semantic.sense.records||[]).find(item=>item[0]===r.id); const wanted=new Set((row?.[2]||[]).map(Number)); chosen=r.verses.filter(v=>wanted.has(Number(v.number))).slice(0,4); } else { const expansion=activeExpansionForms(); chosen=r.verses.filter(v=>literalIncludes(v.text,query)||expansion.some(form=>literalIncludes(v.text,form))).slice(0,4); } if(!chosen.length)return''; return `<div class="theme-context exact-context"><div class="context-label">Passage${chosen.length>1?'s':''} où la recherche apparaît</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${highlighted(v.text)}</span></div>`).join('')}</div>`; }
  function relatedThemes(r,matchedThemes){ const matched=new Set((matchedThemes||[]).map(x=>x.id)); return (state.themesByRecord.get(r.id)||[]).filter(t=>!matched.has(t.id)).slice(0,12); }
  function themeTags(themes){ if(!themes.length)return '<span class="muted inline-empty">Aucun autre thème indexé.</span>'; return `<span class="inline-themes">${themes.map(t=>`<button class="theme-text-link" data-related-theme="${esc(t.id)}">${esc(t.label)}</button>`).join('<span class="theme-separator">·</span>')}</span>`; }
  function bindThemeLinks(root=document){ root.querySelectorAll('[data-related-theme]').forEach(b=>b.onclick=()=>navigateToTheme(state.themeById.get(b.dataset.relatedTheme))); }
  function dualThemeReasons(r, themeMatches){ return `<div class="theme-reasons">${themeMatches.map(({theme,thematic})=>`<section class="theme-reason"><div class="theme-reason-head"><strong>${esc(theme.label)}</strong><span class="score">${esc(importanceLabel(thematic.importance))}</span></div><p class="result-summary">${modeAwareText(thematic.teaching||'')}</p>${contextualVerses(r,thematic)}</section>`).join('')}</div>`; }

  function resultDetailsBody(r,{thematic,matchedThemes,numberLookup,themeMatches,companion}) {
    const related=(thematic||themeMatches)?relatedThemes(r,matchedThemes):[];
    const textualThemes=!thematic&&!themeMatches&&companion?.textualFallback?(state.themesByRecord.get(r.id)||[]):[];
    const relatedBlock=(thematic||themeMatches)?`<div class="related-themes compact-related"><span class="related-label">Autres thèmes dans ce psaume :</span> ${themeTags(related)}</div>`:textualThemes.length?`<div class="related-themes compact-related"><span class="related-label">Thèmes canoniques indexés dans ce psaume :</span> ${themeTags(textualThemes)}</div>`:'';
    const exactBlock=!thematic&&!themeMatches&&!numberLookup?exactVerses(r):'';
    const singleThemeBody=thematic&&!themeMatches?`<div class="context-label theme-found">THÈME INDEXÉ · ${esc((matchedThemes||[]).map(x=>x.label).join(' · '))}</div><p class="result-summary">${modeAwareText(thematic.teaching||summary(r))}</p>${contextualVerses(r,thematic)}`:'';
    const dualBody=themeMatches?dualThemeReasons(r,themeMatches):'';
    const fallbackBody=!thematic&&!themeMatches?`<p class="result-summary">${modeAwareText(summary(r))}</p>${exactBlock}`:'';
    return (dualBody||singleThemeBody||fallbackBody)+relatedBlock;
  }

  function render(items,indexedThemes=null,companion=null){
    const themeLabels=Array.isArray(indexedThemes)?indexedThemes.map(t=>t.label):indexedThemes?[indexedThemes.label]:[];
    $('resultCount').textContent=companion?.grammarSearch?`${items.reduce((n,item)=>n+item.occurrenceCount,0)} occurrences · ${items.length} textes`:companion?.suggestionPending?'Choisissez un thème':companion?.dualPending?'Intersection en attente':companion?.dualTheme?`${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} sous les deux thèmes`:companion?.numberLookup?`${items.length} psaume${items.length>1?'s':''} portant le numéro ${companion.psalmNumber}`:companion?.unresolvedTheme?'Aucun thème indexé':themeLabels.length?`${items.length} psaume${items.length>1?'s':''} indexé${items.length>1?'s':''} · classés Central, Important, puis Lié`:`${items.length} résultat${items.length>1?'s':''}`;
    const textualNotice=!companion?.dualTheme&&themeLabels.length===1&&companion?.textualCount>0?`<div class="search-scope-note"><strong>Thème indexé · ${items.length} psaumes</strong><button class="secondary" data-show-text-search>Voir les occurrences (${companion.textualCount})</button></div>`:'';
    const nearby=companion?.unresolvedTheme?findAutocompleteThemes($('query').value):[];
    const unresolvedNotice=companion?.unresolvedTheme?`<div class="search-scope-note"><strong>Aucun thème trouvé</strong><div class="near-themes">${nearby.map(theme=>`<button class="popular-theme-chip" data-near-theme="${esc(theme.id)}">${esc(theme.label)}</button>`).join('')}</div><button class="secondary" data-search-in-words>Rechercher en mots</button></div>`:'';
    if(!items.length){ const emptyNumber=companion?.numberLookup?`<div class="empty">Aucun psaume numéro ${esc(companion.psalmNumber)} ne correspond aux filtres sélectionnés.</div>`:''; const dualEmpty=companion?.dualTheme?'<div class="empty">Aucun psaume n’est actuellement indexé sous les deux thèmes.</div>':''; const suggestionPending=companion?.suggestionPending?'<div class="empty">Plusieurs thèmes correspondent à votre recherche. Choisissez celui qui vous intéresse ci-dessus.</div>':''; const pending=companion?.dualPending?'<div class="empty">Choisissez une correspondance canonique pour chaque thème afin de calculer l’intersection documentaire.</div>':''; $('results').innerHTML=emptyNumber||dualEmpty||suggestionPending||pending||unresolvedNotice||(textualNotice+'<div class="empty">Aucun passage indexé ne correspond encore à cette recherche et aux filtres sélectionnés.</div>');bindTextSearchLink();bindNearThemeChoices();return; }
    $('results').innerHTML=unresolvedNotice+textualNotice+items.map(({record:r,thematic,matchedThemes,numberLookup,themeMatches,occurrenceCount})=>{
      const bookMeta=r.book?.number?`Livre ${r.book.number}${r.book.title?` · ${r.book.title}`:''}`:'';
      const status=companion?.exactSearch?`${occurrenceCount} occurrence${occurrenceCount>1?'s':''}`:themeMatches?'Deux thèmes':thematic?importanceLabel(thematic.importance):numberLookup?'Numéro':companion?.textualFallback?'Occurrence du terme':'Texte';
      const details=resultDetailsBody(r,{thematic,matchedThemes,numberLookup,themeMatches,companion});
      const title=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée');
      return `<article class="result-card result-card-compact">
        <button class="result-summary-toggle" type="button" data-toggle-result aria-expanded="false">
          <span class="result-identity"><span class="result-doc">${esc(label(r))}</span><span class="result-title">${modeAwareText(r.title)}</span><span class="result-meta">${esc(bookMeta||'Corpus structuré')}</span></span>
          <span class="result-status"><strong class="score">${esc(status)}</strong><span class="result-chevron" aria-hidden="true">⌄</span></span>
        </button>
        <div class="result-details" hidden>${details}<div class="result-actions"><button class="primary" data-open="${esc(r.id)}">${thematic||themeMatches?'Voir le psaume source':'Voir'}</button></div></div>
      </article>`;
    }).join('');
    document.querySelectorAll('[data-toggle-result]').forEach(button=>button.onclick=()=>{ const details=button.nextElementSibling; const open=button.getAttribute('aria-expanded')==='true'; button.setAttribute('aria-expanded',String(!open)); details.hidden=open; });
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=e=>{e.stopPropagation();open(b.dataset.open);}); bindThemeLinks($('results')); bindTextSearchLink();
  }
  function bindTextSearchLink(){ const button=document.querySelector('[data-show-text-search]'); if(button)button.onclick=()=>{ activateExactMode(); search(); window.scrollTo({top:$('results').offsetTop-90,behavior:'smooth'}); }; }
  function open(id){
    const r=state.recordById.get(id);if(!r)return;state.active=r; $('dialogEyebrow').textContent=label(r);$('dialogTitle').textContent=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée');
    if(r.recordType==='psalm'){ const verses=(r.verses||[]).map(v=>`<div class="verse"><div class="verse-number">${v.number}</div><div>${v.speakerId?`<span class="speaker">${esc(v.speakerId.replaceAll('-',' '))} · ${esc(v.speechRole||'')}</span>`:''}${modeAwareText(v.text)}</div></div>`).join(''); const themesBlock=`<section class="related-themes dialog-themes"><div class="context-label">Thèmes présents dans ce psaume</div>${themeTags(state.themesByRecord.get(r.id)||[])}</section>`; $('dialogContent').innerHTML=verses+(r.attachedPrayer?`<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${modeAwareText(r.attachedPrayer.text)}</section>`:'')+themesBlock; bindThemeLinks($('dialogContent')); } else $('dialogContent').innerHTML=`<div class="prayer-block">${modeAwareText(r.text||r.summary||'')}</div>`;
    $('recordDialog').showModal();
  }
  function activeText(){ const r=state.active;if(!r)return''; const title=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée'); const header=[label(r),title]; if(r.book?.number)header.push(`Livre ${r.book.number}${r.book.title?` · ${r.book.title}`:''}`); let out=header.join('\n')+'\n\n'; if(r.verses){ out+=(r.verses||[]).map(v=>`${v.number}. ${v.text}`).join('\n'); if(r.attachedPrayer?.text)out+=`\n\nPrière ${r.attachedPrayer.number}\n\n${r.attachedPrayer.text}`; }else out+=r.text||r.summary||''; return out; }
  function renderThemeDirectory(){ const needle=norm($('themeFilter').value); const visible=needle?state.themeDirectory.filter(t=>norm(t.label).includes(needle)||norm(t.id).includes(needle)):state.themeDirectory; $('indexCount').textContent=needle?`${visible.length} thème${visible.length>1?'s':''} sur ${state.themeDirectory.length}`:`${state.themeDirectory.length} thèmes indexés`; $('themeDirectory').innerHTML=visible.length?visible.map(t=>`<button class="theme-row" data-directory-theme="${esc(t.id)}"><span><strong>${esc(t.label)}</strong><small>${t.occurrenceCount} psaume${t.occurrenceCount>1?'s':''}</small></span><span>${t.score}</span></button>`).join(''):'<div class="empty">Aucun thème ne correspond à ce filtre.</div>'; $('themeDirectory').querySelectorAll('[data-directory-theme]').forEach(b=>b.onclick=()=>{const t=state.themeById.get(b.dataset.directoryTheme);if(t){closeIndex();navigateToTheme(t);}}); }
  function openIndex(){ renderThemeDirectory(); $('indexPanel').hidden=false;$('indexBackdrop').hidden=false;$('indexToggle').setAttribute('aria-expanded','true'); requestAnimationFrame(()=>$('themeFilter').focus()); }
  function closeIndex(){$('indexPanel').hidden=true;$('indexBackdrop').hidden=true;$('indexToggle').setAttribute('aria-expanded','false');}

  function renderPopularQuestionFamilies(){
    $('popularQuestionsTitle').textContent='Choisir une famille'; $('popularQuestionsBack').hidden=true;
    $('popularQuestionsContent').innerHTML=POPULAR_QUESTION_FAMILIES.map(f=>`<button class="popular-question-row" data-popular-family="${esc(f.id)}"><strong>${esc(f.label)}</strong></button>`).join('');
    $('popularQuestionsContent').querySelectorAll('[data-popular-family]').forEach(btn=>btn.onclick=()=>openPopularQuestionFamily(btn.dataset.popularFamily));
  }
  function openPopularQuestionFamily(id){
    const family=POPULAR_QUESTION_FAMILIES.find(item=>item.id===id); if(!family)return;
    $('popularQuestionsTitle').textContent=family.label; $('popularQuestionsBack').hidden=false;
    $('popularQuestionsContent').innerHTML=family.questions.map(q=>`<button class="popular-question-row" data-popular-question="${esc(q.id)}">${esc(q.text)}</button>`).join('');
    $('popularQuestionsContent').querySelectorAll('[data-popular-question]').forEach(btn=>btn.onclick=()=>choosePopularQuestion(family.questions.find(q=>q.id===btn.dataset.popularQuestion)));
  }
  function openPopularQuestions(){ renderPopularQuestionFamilies(); $('popularQuestionsPanel').hidden=false; $('popularQuestionsBackdrop').hidden=false; $('popularQuestionsToggle').setAttribute('aria-expanded','true'); }
  function closePopularQuestions(){ $('popularQuestionsPanel').hidden=true; $('popularQuestionsBackdrop').hidden=true; $('popularQuestionsToggle').setAttribute('aria-expanded','false'); }
  function choosePopularQuestion(question){ if(!question)return; $('query').value=question.text; $('query2').value=''; activateThemeMode(); closePopularQuestions(); search(); }

  const setAdvancedSearch = open => { if(state.mode!=='themes')return; $('primarySearch').classList.toggle('advanced-visible',open); $('advancedSearchToggle').setAttribute('aria-expanded',String(open)); $('advancedSearchToggle').textContent=open?'Fermer le croisement':'Croiser deux thèmes'; if(open){$('query2').focus();}else{$('query2').value='';if(state.hasSearched)search();} };
  $('advancedSearchToggle').onclick=()=>setAdvancedSearch(!$('primarySearch').classList.contains('advanced-visible'));
  $('searchForm').addEventListener('submit',event=>{event.preventDefault();search();});
  $('query').addEventListener('input',()=>{handleExactQueryInput();renderThemeAutocomplete();});
  $('query').addEventListener('keydown',event=>{
    if(event.key==='Escape')hideThemeAutocomplete();
    if(event.key==='ArrowDown'&&!$('themeAutocomplete').hidden){event.preventDefault();focusSuggestion(0);}
  });
  // 053: close after the destination has received its click; pointerdown would collapse
  // the scrollable suggestion panel before mobile mode buttons can be activated.
  document.addEventListener('click',event=>{if(!event.target.closest('.query-stack'))hideThemeAutocomplete();});
  $('query2').addEventListener('input',hideThemeAutocomplete);
  $('results').addEventListener('click',event=>{if(event.target.closest('[data-search-in-words]')){activateExactMode();search();}});
  document.querySelectorAll('[name=sourceType]').forEach(x=>x.onchange=()=>{if(state.hasSearched)search();});
  $('archangelFilter').onchange=()=>{if(state.hasSearched)search();};
  $('includeWordForms').onchange=()=>{if(state.hasSearched)search();};
  $('includeSimplePlurals').onchange=()=>{if(state.hasSearched)search();};
  $('modeThemes').onclick=()=>{activateThemeMode();if(state.hasSearched)search();else renderThemeAutocomplete();};
  $('modeExact').onclick=()=>{activateExactMode();if(state.hasSearched)search();else renderThemeAutocomplete();}; $('closeAmbiguity').onclick=hideAmbiguity;
  $('popularQuestionsToggle').onclick=openPopularQuestions; $('closePopularQuestions').onclick=closePopularQuestions; $('popularQuestionsBackdrop').onclick=closePopularQuestions; $('popularQuestionsBack').onclick=renderPopularQuestionFamilies;
  $('indexToggle').onclick=()=>{$('indexPanel').hidden?openIndex():closeIndex();}; $('themeFilter').oninput=renderThemeDirectory; $('closeIndex').onclick=closeIndex; $('indexBackdrop').onclick=closeIndex; $('closeDialog').onclick=()=>$('recordDialog').close(); $('printRecord').onclick=()=>window.print(); $('downloadRecord').onclick=()=>{const blob=new Blob([activeText()],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${state.active?.id||'biblaw'}.txt`;a.click();URL.revokeObjectURL(a.href);};
  load();
})();