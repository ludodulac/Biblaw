(() => {
  const $ = id => document.getElementById(id);
  const state = { mode: 'themes', records: [], recordById: new Map(), psalmsByNumber: new Map(), normalizedFragmentsById: new Map(), themeDirectory: [], themeById: new Map(), themesByRecord: new Map(), lexicalExpansionGroups: [], lexicalExpansionByForm: new Map(), semanticBrowserRuntime: null, semanticTargetsByForm: new Map(), semanticSelection: null, grammarByForm: new Map(), grammarSelection: null, runtime: null, themeEngine: null, active: null, resolvedThemes: [], noteThemes: [], noteReferences: [], selectedNoteTheme: null, readerPart:'both', readerHtml:null, autocompleteIndex:null, corpusReady:false, corpusPromise:null, pendingSearch:false, bibleThemesSorted:null, bibleThemeDirectoryScroll:0, bibleThemeSelected:null, bibleThemeRequestId:0, archivedNotes:null, archivedNoteById:new Map(), archivedNoteLoading:null, notesTab:'archive' };
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
  function activeExpansionForms(){ const expansionRequested=state.mode==='exact'&&$('includeWordForms')?.checked; return expansionRequested?expansionFormsFor($('query')?.value||''):[]; }
  function updateExpansionControl(){ const option=$('exactExpansionOption'),checkbox=$('includeWordForms'); if(!option||!checkbox)return; const key=state.mode==='exact'?singleWordQueryKey($('query')?.value||''):null,expansions=key?expansionFormsFor(key):[]; const analyses=state.grammarByForm.get(key)||[]; const available=Boolean(key&&expansions.length); const enabled=available&&!(state.mode==='exact'&&$('primarySearch').classList.contains('advanced-visible')); option.hidden=!enabled; checkbox.disabled=!enabled; const label=option.querySelector('label span'); if(label){ const pos=analyses.length===1?analyses[0].partOfSpeech:null; label.textContent=pos==='NOUN'?'Inclure singulier et pluriel vérifiés':pos==='VERB'?'Inclure les formes verbales vérifiées':'Inclure les formes morphologiques vérifiées'; } if(!enabled)checkbox.checked=false; }
  const queryTerms = () => {
    const values=[$('query')?.value,$('query2')?.value];
    const terms=new Set(values.flatMap(value=>norm(value).split(' ')).filter(Boolean));
    for(const value of values){
      const equivalent=BiblawAutocomplete.otherNumericForm(value);
      if(equivalent&&!norm(equivalent).includes(' '))terms.add(norm(equivalent));
    }
    for(const form of activeExpansionForms())terms.add(form);
    return terms;
  };
  const highlighted = value => { const terms=queryTerms(); if(!terms.size)return esc(value); return String(value||'').split(/([\p{L}\p{N}œŒæÆ’'-]+)/gu).map(part=>terms.has(norm(part))?`<mark class="search-hit">${esc(part)}</mark>`:esc(part)).join(''); };
  const modeAwareText = value => state.mode==='exact' ? highlighted(value) : esc(value);
  const type = r => r.recordType === 'master-prayer' ? 'prayer' : r.recordType;
  const textFragments = r => r.recordType === 'psalm' ? [r.title, ...(r.verses || []).map(v => v.text)].filter(Boolean) : [r.title, r.text, r.summary].filter(Boolean);
  const literalIncludes = (value, query) => literalOccurrenceCount({id:'__temporary',_literal:value},query)>0;
  const literalOccurrenceCount = (r, query) => {
    const needle=norm(query); if(!needle)return 0;
    // Numeric equivalence is exact: 4 <-> quatre, never 4 <-> 40 or 80.
    const numeric=BiblawAutocomplete.numericValue(query);
    if(numeric!==null&&needle!=='un'){
      const original=r._literal!==undefined?[r._literal]:textFragments(r);
      return BiblawAutocomplete.countNumericOccurrences(original,query);
    }
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
  const activateThemeMode = () => { state.mode='themes'; $('primarySearch').classList.remove('advanced-visible'); $('query2').value=''; $('query2').placeholder='Deuxième thème à croiser'; $('query2').setAttribute('aria-label','Thème 2 facultatif'); $('query').setAttribute('aria-label','Votre recherche'); $('advancedSearchToggle').textContent='Croiser 2 thèmes'; $('advancedSearchToggle').setAttribute('aria-expanded','false'); $('dualExactHelp').hidden=true; document.querySelectorAll('[name=sourceType]').forEach(box=>{box.checked=box.value==='psalm';}); $('scopeInfo').hidden=true; state.semanticSelection=null; state.grammarSelection=null; $('modeThemes').classList.add('active'); $('modeExact').classList.remove('active'); $('primarySearch').classList.remove('exact-mode'); $('query2').disabled=false; $('advancedSearchToggle').hidden=false; $('query').placeholder='Ex. Saint-Esprit, amour, psaume 105'; $('modeHelp').textContent='Chercher dans les thèmes indexés des psaumes.'; hideAmbiguity(); updateExpansionControl(); };
  const activateExactMode = () => { state.mode='exact'; $('modeExact').classList.add('active'); $('modeThemes').classList.remove('active'); $('primarySearch').classList.add('exact-mode'); $('primarySearch').classList.remove('advanced-visible'); $('query2').disabled=true; $('query2').value=''; $('advancedSearchToggle').hidden=false; $('advancedSearchToggle').setAttribute('aria-expanded','false'); $('advancedSearchToggle').textContent='Croiser 2 mots'; $('query2').placeholder='Deuxième mot · ex. amour'; $('query2').setAttribute('aria-label','Deuxième mot pour départager'); $('query').setAttribute('aria-label','Premier mot prioritaire'); $('dualExactHelp').hidden=true; $('query').placeholder='Ex. Saint-Esprit, vie, amour'; $('modeHelp').textContent='Chercher les mots exacts dans les textes.'; hideAmbiguity(); hideTransverseNavigation(); updateExpansionControl(); };

  // 082: Six suggestions maximum, sourced from the already-public corpus.
  const suggestionFields={query:'searchSuggestions',query2:'searchSuggestions2'};
  function closeSuggestions(fieldName){
    const box=$(suggestionFields[fieldName]),field=$(fieldName);
    if(!box||!field)return;
    box.hidden=true;box.replaceChildren();field.setAttribute('aria-expanded','false');
  }
  function closeAllSuggestions(){closeSuggestions('query');closeSuggestions('query2');}
  function offerSuggestions(fieldName){
    const box=$(suggestionFields[fieldName]),field=$(fieldName),index=state.autocompleteIndex;
    if(!box||!field||!index||field.disabled||!field.value.trim()||
       field.value.includes('+')){closeSuggestions(fieldName);return;}
    const available=index.suggestions(field.value,state.mode,selectedTypes(),
      $('archangelFilter').value,state.themeDirectory,state.recordById,6);
    if(!available.length){closeSuggestions(fieldName);return;}
    box.replaceChildren();
    for(const option of available){
      const button=document.createElement('button');button.type='button';
      button.className='search-suggestion';button.setAttribute('role','option');
      const label=document.createElement('span');
      label.className='suggestion-label';label.textContent=option.label;
      const kind=document.createElement('span');
      kind.className='suggestion-kind';kind.textContent=option.kind==='theme'?'Thème':'Mot';
      button.append(label,kind);
      button.addEventListener('click',()=>{
        if(option.kind==='word'&&state.mode!=='exact'){
          activateExactMode();
          if(fieldName==='query2')setAdvancedSearch(true);
        }
        if(option.kind==='theme'&&state.mode!=='themes')activateThemeMode();
        $(fieldName).value=option.value;
        $(fieldName).focus({preventScroll:true});
        closeAllSuggestions();
      });
      button.addEventListener('keydown',event=>{
        if(event.key==='Escape'){
          event.preventDefault();closeAllSuggestions();field.focus({preventScroll:true});
        }else if(event.key==='ArrowDown'){
          event.preventDefault();(button.nextElementSibling||field).focus({preventScroll:true});
        }else if(event.key==='ArrowUp'){
          event.preventDefault();(button.previousElementSibling||field).focus({preventScroll:true});
        }
      });
      box.append(button);
    }
    box.hidden=false;field.setAttribute('aria-expanded','true');
  }
  function bindSuggestions(){
    for(const fieldName of Object.keys(suggestionFields)){
      $(fieldName).addEventListener('input',()=>offerSuggestions(fieldName));
      $(fieldName).addEventListener('focus',()=>offerSuggestions(fieldName));
      $(fieldName).addEventListener('keydown',event=>{
        if(event.key==='Escape')closeAllSuggestions();
        if(event.key==='ArrowDown'){
          const box=$(suggestionFields[fieldName]);
          if(!box.hidden){
            event.preventDefault();box.querySelector('button')?.focus({preventScroll:true});
          }
        }
      });
    }
    // Les suggestions sont dans le flux sur mobile. Ne pas les retirer
    // dès pointerdown : leur disparition déplace le bouton Rechercher avant
    // pointerup, et le clic aboutit sur le panneau au lieu du bouton.
    document.addEventListener('click',event=>{
      if(!event.target.closest('.query-stack'))closeAllSuggestions();
    });
  }
  function indexPublicWords(){
    const index=BiblawAutocomplete.createIndex(),records=state.records;
    let cursor=0;
    function batch(){
      const next=Math.min(records.length,cursor+45);
      for(;cursor<next;cursor++)index.addRecord(records[cursor]);
      if(cursor<records.length)setTimeout(batch,0);
      else{
        state.autocompleteIndex=index;
        if(document.activeElement===$('query'))offerSuggestions('query');
        if(document.activeElement===$('query2'))offerSuggestions('query2');
      }
    }
    setTimeout(batch,0);
  }
  // Load large documentary data only when the visitor actually needs search,
  // theme-directory browsing, notes, or a cited Psalm. FAQ themes and answers
  // keep their own lightweight path. Concurrent gestures share one promise.
  function ensureCorpusReady(){
    if(state.corpusReady)return Promise.resolve(true);
    if(state.corpusPromise)return state.corpusPromise;
    $('corpusStats').textContent='Chargement du corpus documentaire…';
    state.corpusPromise=load().then(ready=>{
      if(ready){
        state.corpusReady=true;
        if(state.pendingSearch){
          state.pendingSearch=false;
          executeSearch(); // Always use the latest query and filters.
        }
      }
      return ready;
    }).finally(()=>{
      if(!state.corpusReady)state.corpusPromise=null; // allow a retry
    });
    return state.corpusPromise;
  }

  async function yieldToBrowser(){
    // Give mobile browsers a paint opportunity between costly indexing batches.
    await new Promise(resolve=>setTimeout(resolve,0));
  }
  async function load() {
    try {
      const [bundle, directory, runtime, lexicalExpansion, semanticBrowserRuntime, grammarBrowserRuntime, noteThemesIndex, semanticNavigation] = await Promise.all([
        fetch('data/browser-search-catalog.json').then(r => { if (!r.ok) throw Error('browser-search-catalog'); return r.json(); }),
        fetch('data/thematic-index/theme-directory-public.json').then(r => { if (!r.ok) throw Error('theme-directory'); return r.json(); }),
        fetch('data/thematic-index/theme-search-runtime.json').then(r => { if (!r.ok) throw Error('theme-search-runtime'); return r.json(); }),
        fetch('data/lexical-expansion-runtime.json').then(r => { if (!r.ok) throw Error('lexical-expansion-runtime'); return r.json(); }),
        Promise.resolve({targets:[]}),
        fetch('data/linguistic-grammar-browser-runtime.json').then(r => { if (!r.ok) throw Error('linguistic-grammar-browser-runtime'); return r.json(); }),
        fetch('data/note-themes-public-073.json?v=079').then(r => { if (!r.ok) throw Error('note-themes-public-073'); return r.json(); }),
        fetch('data/thematic-index/theme-semantic-navigation-public.json').then(r => { if (!r.ok) throw Error('theme-semantic-navigation-public'); return r.json(); })
      ]);
      $('corpusStats').textContent='Préparation des index de recherche…';
      await yieldToBrowser();
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
      if(semanticNavigation.schemaVersion!==1||
         semanticNavigation.purpose!=='explicit-related-theme-discovery-not-canonical-synonymy'||
         semanticNavigation.canonicalThemeCount!==state.themeDirectory.length||
         semanticNavigation.createsPsalmRelations!==false||
         semanticNavigation.semanticMerging!==false)
        throw Error('La navigation par mots associés est incohérente avec les thèmes canoniques.');
      state.themeEngine = BiblawThemeEngine.create(state.themeDirectory, state.runtime, semanticNavigation);
      state.records = bundle.records || [];
      state.recordById = new Map(state.records.map(r => [r.id, r]));
      // No note becomes public through classification: all IDs must already exist in browser catalog.
      const publishedNotes = new Set(state.records.filter(r => type(r)==='note').map(r=>r.id));
      if (publishedNotes.size!==11 || noteThemesIndex.publicNoteCount!==11) throw Error('Public note count mismatch');
      if (noteThemesIndex.version!==2) throw Error('Outdated note subjects index');
      const noteThemes = noteThemesIndex.themes || [];
      const noteReferences = noteThemesIndex.referenceNotes || [];
      if (!noteThemes.length || noteThemes.some(t=>!t.label||!Array.isArray(t.noteIds)||!t.noteIds.length||t.noteIds.some(id=>!publishedNotes.has(id)))) throw Error('Invalid public note-theme allowlist');
      if (!Array.isArray(noteReferences)||noteReferences.some(x=>!x.id||!x.label||!publishedNotes.has(x.id))) throw Error('Invalid public note references');
      const themedNotes = new Set(noteThemes.flatMap(t=>t.noteIds));
      const referenceIds = new Set(noteReferences.map(n=>n.id));
      if (themedNotes.size!==noteThemesIndex.themedNoteCount || referenceIds.size!==noteReferences.length ||
          [...referenceIds].some(id=>themedNotes.has(id)) ||
          new Set([...themedNotes,...referenceIds]).size!==publishedNotes.size ||
          [...publishedNotes].some(id=>!themedNotes.has(id)&&!referenceIds.has(id))) throw Error('Some public notes unaccounted for');
      state.noteThemes = noteThemes.slice().sort((a,b)=>a.label.localeCompare(b.label,'fr',{sensitivity:'base'}));
      state.noteReferences = noteReferences;
      renderNoteThemeDirectory();

      state.psalmsByNumber = new Map();
      state.normalizedFragmentsById = new Map();
      for (let i=0;i<state.records.length;i++) {
        const r=state.records[i];
        state.normalizedFragmentsById.set(r.id,textFragments(r).map(norm).filter(Boolean));
        if (r.recordType === 'psalm') { const number=Number(r.number), list=state.psalmsByNumber.get(number)||[]; list.push(r); state.psalmsByNumber.set(number,list); }
        if((i+1)%48===0)await yieldToBrowser();
      }
      state.themesByRecord = new Map();
      for (let i=0;i<state.themeDirectory.length;i++) {
        const theme=state.themeDirectory[i];
        for(const occurrence of theme.occurrences||[]){
          const list=state.themesByRecord.get(occurrence.recordId)||[];
          list.push({id:theme.id,label:theme.label,importance:occurrence.importance,score:occurrence.score||0});
          state.themesByRecord.set(occurrence.recordId,list);
        }
        if((i+1)%48===0)await yieldToBrowser();
      }
      for (const list of state.themesByRecord.values()) list.sort((a,b)=>importanceRank(a.importance)-importanceRank(b.importance)||a.label.localeCompare(b.label,'fr')||a.id.localeCompare(b.id,'fr'));
      const prayers = new Map(state.records.filter(r => r.recordType === 'master-prayer').map(r => [r.appliesToPsalmId, r]));
      state.records.filter(r => r.recordType === 'psalm').forEach(r => { if (prayers.has(r.id)) r.attachedPrayer = prayers.get(r.id); });
      const psalms = state.records.filter(r => r.recordType === 'psalm'), verses = psalms.reduce((n, r) => n + (r.verses || []).length, 0);
      $('corpusStats').textContent = `${psalms.length} psaumes · ${verses} versets · ${state.themeDirectory.length} thèmes indexés`;
      $('indexCount').textContent=`${state.themeDirectory.length} thèmes indexés`;
      updateExpansionControl();
      indexPublicWords();
      // Supply the records only after the search engine is ready.
      // FAQ topics and answers already work independently before this point.
      BiblawFAQ.setRecords(state.records);
      document.dispatchEvent(new CustomEvent('biblaw:corpus-ready',{
        detail:{themes:state.themeDirectory}
      }));
      return true;
    } catch (error) {
      console.error(error);
      $('corpusStats').textContent='Corpus indisponible. Relancez une recherche pour réessayer.';
      $('resultCount').textContent='';
      $('results').innerHTML = '<div class="empty" role="status">Le corpus ne peut pas être chargé. Vérifiez votre connexion et réessayez.</div>';
      return false;
    }
  }

  function matches(query) { const allowed=selectedTypes(),a=$('archangelFilter').value; return state.records.filter(r=>allowed.has(type(r))&&(!a||r.archangel===a)).map(record=>({record,score:1,occurrenceCount:literalOccurrenceCount(record,query)})).filter(item=>item.occurrenceCount>0); }
  // 081: Literal pair ranking reuses the certified word-boundary counter and active source filters.
  function splitExactWordPair(value) {
    const parts=String(value||'').split('+');
    if(parts.length!==2)return null;
    const first=parts[0].trim(),second=parts[1].trim();
    return first&&second?[first,second]:null;
  }
  function rankExactWordPairs(firstWord,secondWord) {
    const secondCounts=new Map(matches(secondWord).map(item=>[item.record.id,item.occurrenceCount]));
    return matches(firstWord)
      .filter(item=>secondCounts.has(item.record.id))
      .map(item=>({...item,secondaryOccurrenceCount:secondCounts.get(item.record.id)}))
      .sort((a,b)=>b.occurrenceCount-a.occurrenceCount||
        b.secondaryOccurrenceCount-a.secondaryOccurrenceCount||
        (Number(a.record.number)||Number.MAX_SAFE_INTEGER)-(Number(b.record.number)||Number.MAX_SAFE_INTEGER)||
        String(a.record.id).localeCompare(String(b.record.id),'fr'));
  }
  function mergeExpansionMatches(items,query,matchSource=matches){ const forms=activeExpansionForms(); if(!forms.length||!singleWordQueryKey(query))return items; const byId=new Map(items.map(item=>[item.record.id,item])); for(const form of forms)for(const item of matchSource(form)){ const current=byId.get(item.record.id); if(current)current.occurrenceCount+=item.occurrenceCount; else byId.set(item.record.id,item); } items.splice(0,items.length,...byId.values()); return items; }
  function psalmNumberMatches(number) { if(!selectedTypes().has('psalm'))return []; const a=$('archangelFilter').value; return (state.psalmsByNumber.get(number)||[]).filter(r=>!a||r.archangel===a).sort((x,y)=>(x.book?.number||9999)-(y.book?.number||9999)||String(x.id).localeCompare(String(y.id),'fr')).map(record=>({record,score:1,numberLookup:true})); }
  function textualPsalmMatches(query) { return matches(query).filter(x=>x.record.recordType==='psalm'); }
  function resolveIndexedThemes(query) { return state.themeEngine?.resolveIndexedThemes(query) || []; }
  const composeThemeQueryNotions = query => BiblawThemeEngine.composeThemeQueryNotions(query);
  const themeQueryNotions = query => BiblawThemeEngine.themeQueryNotions(query);
  function suggestIndexedThemes(query) { return state.themeEngine?.suggestIndexedThemes(query) || []; }
  function thematicItems(themes, ignoreFilters=false) {
    if (!ignoreFilters && !selectedTypes().has('psalm')) return [];
    const a=ignoreFilters?'':$('archangelFilter').value,merged=new Map();
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
  function ambiguityChoice(theme, target) { const count=theme.occurrenceCount||theme.occurrences?.length||0; return `<button class="sense-button" data-ambiguity-target="${target}" data-theme-id="${esc(theme.id)}"><strong>${esc(theme.label)}</strong><span>${count} psaume${count>1?'s':''}</span></button>`; }
  function showDualAmbiguity(queryA, resolvedA, queryB, resolvedB) {
    hideTransverseNavigation();
    const blocks=[];
    if(resolvedA.length!==1) blocks.push(`<div class="ambiguity-group"><div class="context-label">Thème 1 · ${esc(queryA)}</div>${resolvedA.length?resolvedA.map(t=>ambiguityChoice(t,'query')).join(''):'<div class="muted">Aucun thème canonique ne correspond exactement à ce champ.</div>'}</div>`);
    if(resolvedB.length!==1) blocks.push(`<div class="ambiguity-group"><div class="context-label">Thème 2 · ${esc(queryB)}</div>${resolvedB.length?resolvedB.map(t=>ambiguityChoice(t,'query2')).join(''):'<div class="muted">Aucun thème canonique ne correspond exactement à ce champ.</div>'}</div>`);
    $('suggestionKicker').textContent='Croiser deux thèmes'; $('suggestionTitle').textContent='Choisissez les deux thèmes'; $('senseChoices').innerHTML=blocks.join('');
    $('senseChoices').querySelectorAll('[data-ambiguity-target]').forEach(btn=>btn.onclick=()=>{ const theme=state.themeById.get(btn.dataset.themeId); if(!theme)return; $(btn.dataset.ambiguityTarget).value=theme.label; search(); });
    $('ambiguityPanel').hidden=false;
  }
  function showSingleThemeAmbiguity(resolvedThemes) {
    state.resolvedThemes=resolvedThemes;
    if(resolvedThemes.length<=1){hideAmbiguity();return;}
    $('suggestionKicker').textContent='Précisez votre choix'; $('suggestionTitle').textContent='Quel thème recherchez-vous ?';
    $('senseChoices').innerHTML=resolvedThemes.map(theme=>ambiguityChoice(theme,'query')).join('');
    $('senseChoices').querySelectorAll('[data-ambiguity-target]').forEach(btn=>btn.onclick=()=>{const theme=state.themeById.get(btn.dataset.themeId);if(!theme)return;$('query').value=theme.label;search();});
    $('ambiguityPanel').hidden=false;
  }
  function showThemeSuggestions(themes) {
    state.resolvedThemes=themes;
    $('suggestionKicker').textContent='Plusieurs possibilités'; $('suggestionTitle').textContent='Choisissez un thème';
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
    if(!theme)return; activateThemeMode(); $('query').value=theme.label; $('query2').value=''; if($('recordDialog').open)$('recordDialog').close();
    const thematic=thematicItems([theme]), textual=textualPsalmMatches(theme.label); hideAmbiguity(); showTransverseNavigation(theme);
    publishPresentationState({kind:'canonical-theme',theme:{id:theme.id,label:theme.label},psalmCount:thematic.length});
    showSearchView();render(thematic,[theme],{textualCount:textual.length});requestAnimationFrame(focusSearchOutcome);
  }

  // 080: Some Android keyboards can insert a complete word twice on commit/refocus.
  // Correct only an entire single-word repetition, without touching phrases.
  function repeatedWholeWordCorrection(value) {
    const trimmed=String(value||'').trim();
    const chars=Array.from(trimmed.normalize('NFC'));
    if(chars.length<8||chars.length>80||chars.length%2!==0)return null;
    const half=chars.length/2;
    const first=chars.slice(0,half).join(''),second=chars.slice(half).join('');
    if(!/^[\p{L}\p{M}]+$/u.test(first))return null;
    return first.toLocaleLowerCase('fr')===second.toLocaleLowerCase('fr')?first:null;
  }
  function correctMobileQueryDuplicate() {
    const field=$('query'),fixed=repeatedWholeWordCorrection(field?.value);
    if(fixed===null||!field)return false;
    field.value=fixed;
    return true;
  }

  function search(){
    if(!state.corpusReady){
      if(!$('query').value.trim()){
        state.pendingSearch=false;
        return executeSearch();
      }
      state.pendingSearch=true;
      $('resultCount').textContent='Chargement…';
      $('results').innerHTML='<div class="empty" role="status">Chargement des textes nécessaires à la recherche…</div>';
      // Do not disable buttons: the latest query or filter wins during loading.
      void ensureCorpusReady();
      return;
    }
    return executeSearch();
  }
  function executeSearch(){
    closeAllSuggestions();
    correctMobileQueryDuplicate();
    // Keep the visible expression intact: the + is typed in the SAME field.
    const rawQuery=$('query').value.trim();
    const plusPair=splitExactWordPair(rawQuery);
    if(plusPair && state.mode!=='exact')activateExactMode();
    const query=plusPair?plusPair[0]:rawQuery,query2=plusPair?plusPair[1]:'';
    if(/\+\s*$/.test(rawQuery)){
      hideAmbiguity();hideTransverseNavigation();
      return render([],null,{dualExactPending:true});
    }
    const semanticKey=singleWordQueryKey(query);
    if(state.semanticSelection&&semanticKey!==state.semanticSelection.normalizedForm)state.semanticSelection=null;
    updateExpansionControl();
    if(!query){hideAmbiguity();hideTransverseNavigation();publishPresentationState({kind:'no-result'});return render([]);}
    const psalmNumber=parsePsalmNumberQuery(query);
    if(psalmNumber!==null && !query2 && state.mode==='themes'){ hideAmbiguity();hideTransverseNavigation();publishPresentationState({kind:'other'}); return render(psalmNumberMatches(psalmNumber),null,{numberLookup:true,psalmNumber}); }
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
      if(!resolved.length){
        const related=state.themeEngine?.relatedThemesForQuery(query)||[];
        if(related.length){
          hideAmbiguity();hideTransverseNavigation();
          const thematic=thematicItems(related);
          const textual=textualPsalmMatches(query);
          publishPresentationState({kind:'related-theme-discovery',
            themes:related.map(theme=>({id:theme.id,label:theme.label})),
            psalmCount:thematic.length});
          return render(thematic,related,{relatedDiscovery:true,
            relatedQuery:query,relatedThemes:related,textualCount:textual.length});
        }
      }
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
    if(plusPair){
      $('includeWordForms').checked=false;
      $('exactExpansionOption').hidden=true;
      if(!query2){hideAmbiguity();return render([],null,{dualExactPending:true});}
      hideAmbiguity();
      return render(rankExactWordPairs(query,query2),null,{exactSearch:true,dualExactQueries:[query,query2]});
    }
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
  function exactVerses(r,dualWords=null){ if(r.recordType!=='psalm'||!r.verses?.length)return''; const query=$('query').value; if(!norm(query))return'';
    if(Array.isArray(dualWords)&&dualWords.length===2){
      const chosen=r.verses.filter(v=>dualWords.some(word=>literalIncludes(v.text,word))).slice(0,4);
      if(!chosen.length)return'';
      return `<div class="theme-context exact-context"><div class="context-label">Passages où apparaît au moins un des deux mots</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${highlighted(v.text)}</span></div>`).join('')}</div>`;
    }
    const semantic=semanticSelectionContext(query); let chosen; if(semantic){ const row=(semantic.sense.records||[]).find(item=>item[0]===r.id); const wanted=new Set((row?.[2]||[]).map(Number)); chosen=r.verses.filter(v=>wanted.has(Number(v.number))).slice(0,4); } else { const expansion=activeExpansionForms(); chosen=r.verses.filter(v=>literalIncludes(v.text,query)||expansion.some(form=>literalIncludes(v.text,form))).slice(0,4); } if(!chosen.length)return''; return `<div class="theme-context exact-context"><div class="context-label">Passage${chosen.length>1?'s':''} où la recherche apparaît</div>${chosen.map(v=>`<div class="context-verse"><strong>${esc(v.number)}</strong><span>${highlighted(v.text)}</span></div>`).join('')}</div>`; }
  function relatedThemes(r,matchedThemes){ const matched=new Set((matchedThemes||[]).map(x=>x.id)); return (state.themesByRecord.get(r.id)||[]).filter(t=>!matched.has(t.id)).slice(0,12); }
  function themeTags(themes){ if(!themes.length)return '<span class="muted inline-empty">Aucun autre thème indexé.</span>'; return `<span class="inline-themes">${themes.map(t=>`<button class="theme-text-link" data-related-theme="${esc(t.id)}">${esc(t.label)}</button>`).join('<span class="theme-separator">·</span>')}</span>`; }
  function bindThemeLinks(root=document){ root.querySelectorAll('[data-related-theme]').forEach(b=>b.onclick=()=>navigateToTheme(state.themeById.get(b.dataset.relatedTheme))); }
  function dualThemeReasons(r, themeMatches){ return `<div class="theme-reasons">${themeMatches.map(({theme,thematic})=>`<section class="theme-reason"><div class="theme-reason-head"><strong>${esc(theme.label)}</strong><span class="score">${esc(importanceLabel(thematic.importance))}</span></div><p class="result-summary">${modeAwareText(thematic.teaching||'')}</p>${contextualVerses(r,thematic)}</section>`).join('')}</div>`; }

  function resultDetailsBody(r,{thematic,matchedThemes,numberLookup,themeMatches,companion}) {
    const related=(thematic||themeMatches)?relatedThemes(r,matchedThemes):[];
    const textualThemes=!thematic&&!themeMatches&&companion?.textualFallback?(state.themesByRecord.get(r.id)||[]):[];
    const relatedBlock=(thematic||themeMatches)?`<div class="related-themes compact-related"><span class="related-label">Autres thèmes dans ce psaume :</span> ${themeTags(related)}</div>`:textualThemes.length?`<div class="related-themes compact-related"><span class="related-label">Thèmes canoniques indexés dans ce psaume :</span> ${themeTags(textualThemes)}</div>`:'';
    const exactBlock=!thematic&&!themeMatches&&!numberLookup?exactVerses(r,companion?.dualExactQueries):'';
    const singleThemeBody=thematic&&!themeMatches?`<div class="context-label theme-found">THÈME INDEXÉ · ${esc((matchedThemes||[]).map(x=>x.label).join(' · '))}</div><p class="result-summary">${modeAwareText(thematic.teaching||summary(r))}</p>${contextualVerses(r,thematic)}`:'';
    const dualBody=themeMatches?dualThemeReasons(r,themeMatches):'';
    const fallbackBody=!thematic&&!themeMatches?`<p class="result-summary">${modeAwareText(summary(r))}</p>${exactBlock}`:'';
    return (dualBody||singleThemeBody||fallbackBody)+relatedBlock;
  }

  function render(items,indexedThemes=null,companion=null){
    document.body.classList.toggle('has-query',Boolean($('query').value.trim()));
    const themeLabels=Array.isArray(indexedThemes)?indexedThemes.map(t=>t.label):indexedThemes?[indexedThemes.label]:[];
    $('resultCount').textContent=companion?.dualExactQueries?`${items.length} texte${items.length>1?'s':''} avec les deux mots`:companion?.dualExactPending?'Deuxième mot à saisir':companion?.grammarSearch?`${items.length} textes`:companion?.suggestionPending?'Choisissez un thème':companion?.dualPending?'Choisissez 2 thèmes':companion?.numberLookup?`${items.length} psaume${items.length>1?'s':''} trouvé${items.length>1?'s':''}`:companion?.unresolvedTheme?'Aucun thème trouvé':themeLabels.length?`${items.length} psaume${items.length>1?'s':''} trouvé${items.length>1?'s':''}`:`${items.length} résultat${items.length>1?'s':''}`;
    const textualNotice=!companion?.dualTheme&&themeLabels.length===1&&companion?.textualCount>0?`<div class="search-scope-note"><div><strong>Aussi dans le texte</strong><span>${companion.textualCount} psaume${companion.textualCount>1?'s':''} contiennent ce mot ou cette expression.</span></div><button class="secondary" data-show-text-search>Voir les occurrences</button></div>`:'';
    const relatedNotice=companion?.relatedDiscovery?
      '<section class="search-scope-note related-discovery"><div><strong>Thèmes associés à « '+
      esc(companion.relatedQuery)+' »</strong><span>Ces pistes proviennent des thèmes déjà indexés. '+
      'Ce ne sont pas des synonymes certains ni de nouvelles associations entre psaumes.</span></div>'+
      '<div class="related-discovery-themes">'+companion.relatedThemes.map(t=>
        '<button class="theme-text-link" type="button" data-related-theme="'+esc(t.id)+'">'+
        esc(t.label)+'</button>').join('')+'</div>'+
      (companion.textualCount>0?'<button class="secondary" type="button" data-show-text-search>'+
        'Voir aussi les occurrences du mot</button>':'')+'</section>':'';
    const unresolvedNotice=companion?.unresolvedTheme?`<div class="search-scope-note"><div><strong>Aucun thème indexé ne correspond à cette recherche</strong><span>${companion?.textualAvailable?'Le mot ou l’expression apparaît cependant dans le corpus.':'Aucune occurrence textuelle exacte ne correspond non plus avec les filtres sélectionnés.'}</span></div>${companion?.textualAvailable?'<button class="secondary" data-show-text-search>Voir les occurrences</button>':''}</div>`:'';
    if(!items.length){ const emptyNumber=companion?.numberLookup?`<div class="empty">Aucun psaume numéro ${esc(companion.psalmNumber)} ne correspond aux filtres sélectionnés.</div>`:''; const dualEmpty=companion?.dualTheme?'<div class="empty">Aucun psaume n’est actuellement indexé sous les deux thèmes.</div>':''; const suggestionPending=companion?.suggestionPending?'<div class="empty">Plusieurs thèmes correspondent à votre recherche. Choisissez celui qui vous intéresse ci-dessus.</div>':''; const pending=companion?.dualPending?'<div class="empty">Choisissez une correspondance canonique pour chaque thème afin de calculer l’intersection documentaire.</div>':''; const wordEmpty=companion?.dualExactQueries?'<div class="empty">Aucun texte ne contient les deux mots dans les catégories sélectionnées.</div>':companion?.dualExactPending?'<div class="empty">Saisissez les deux mots pour lancer cette recherche.</div>':''; $('results').innerHTML=relatedNotice+(emptyNumber||dualEmpty||suggestionPending||pending||wordEmpty||unresolvedNotice||(textualNotice+'<div class="empty">Aucun passage indexé ne correspond encore à cette recherche et aux filtres sélectionnés.</div>'));bindThemeLinks($('results'));bindTextSearchLink();return; }
    $('results').innerHTML=relatedNotice+unresolvedNotice+textualNotice+items.map(({record:r,thematic,matchedThemes,numberLookup,themeMatches,occurrenceCount,secondaryOccurrenceCount})=>{
      const bookMeta=r.book?.number?`Livre ${r.book.number}${r.book.title?` · ${r.book.title}`:''}`:'';
      const status=companion?.dualExactQueries?`${companion.dualExactQueries[0]} : ${occurrenceCount} · ${companion.dualExactQueries[1]} : ${secondaryOccurrenceCount}`:companion?.exactSearch?`${occurrenceCount} occurrence${occurrenceCount>1?'s':''}`:themeMatches?'Deux thèmes':thematic?importanceLabel(thematic.importance):numberLookup?'Numéro':companion?.textualFallback?'Occurrence du terme':'Texte';
      const details=resultDetailsBody(r,{thematic,matchedThemes,numberLookup,themeMatches,companion});
      const title=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:'Note associée');
      return `<article class="result-card result-card-compact${companion?.dualExactQueries?' result-card-dual-exact':''}">
        <button class="result-summary-toggle" type="button" data-open="${esc(r.id)}" aria-label="Lire ${esc(r.title||'ce texte')}">
          <span class="result-identity"><span class="result-doc">${esc(label(r))}</span><span class="result-title">${modeAwareText(r.title)}</span><span class="result-meta">${esc(bookMeta||'Corpus structuré')}</span></span>
          <span class="result-status"><strong class="score">${esc(status)}</strong><span class="result-chevron" aria-hidden="true">›</span></span>
        </button>
        <button class="result-more-toggle" type="button" data-toggle-result aria-expanded="false">Extrait et thèmes ⌄</button>
        <div class="result-details" hidden>${details}<div class="result-actions"><button class="primary" data-open="${esc(r.id)}">${thematic||themeMatches?'Voir le psaume source':'Voir'}</button></div></div>
      </article>`;
    }).join('');
    document.querySelectorAll('[data-toggle-result]').forEach(button=>button.onclick=()=>{ const details=button.nextElementSibling; const open=button.getAttribute('aria-expanded')==='true'; button.setAttribute('aria-expanded',String(!open)); details.hidden=open; });
    document.querySelectorAll('[data-open]').forEach(b=>b.onclick=e=>{e.stopPropagation();open(b.dataset.open);}); bindThemeLinks($('results')); bindTextSearchLink();
  }
  function bindTextSearchLink(){ const button=document.querySelector('[data-show-text-search]'); if(button)button.onclick=()=>{ activateExactMode(); search(); window.scrollTo({top:$('results').offsetTop-90,behavior:'smooth'}); }; }
  // 073: Independent navigation, restricted to the eleven published note IDs.
  // 079: Topics are subjects evidenced in public note text, not book/verse references.
  // The complete archive contains machine-extracted notes which have NOT been
  // editorially verified. It is a separate, transparently labelled reading
  // view, not an extension of the 11 authenticated public-note allowlist.
  function renderArchivedNotes(){
    if(!state.archivedNotes)return;
    const query=norm($('notesArchiveSearch').value||'');
    const book=Number($('notesArchiveBook').value||0);
    const shown=state.archivedNotes.filter(note=>
      (!book||note.bookNumber===book)&&
      (!query||norm([note.text,'Livre '+note.bookNumber,'Psaume '+note.psalmNumber,
        'Note '+note.noteNumber,note.archangel].join(' ')).includes(query)));
    $('notesArchiveCount').textContent=shown.length+' note'+(shown.length>1?'s':'')+
      (query||book?' trouvée'+(shown.length>1?'s':''):' parmi 280 notes extraites')+
      ' · '+shown.filter(n=>n.publicationStatus==='published').length+' déjà publiée'+
      (shown.filter(n=>n.publicationStatus==='published').length>1?'s':'')+'.';
    const target=$('notesArchiveList'),frag=document.createDocumentFragment();
    const byBook=new Map();
    for(const note of shown){
      const bucket=byBook.get(note.bookNumber)||[];
      bucket.push(note);byBook.set(note.bookNumber,bucket);
    }
    for(const [number,notes] of [...byBook].sort((a,b)=>a[0]-b[0])){
      const group=document.createElement('details');
      group.className='notes-archive-book';
      group.open=Boolean(query||book);
      const heading=document.createElement('summary');
      heading.textContent='Livre '+number+' — '+notes.length+' note'+(notes.length>1?'s':'');
      group.append(heading);
      const grid=document.createElement('div');grid.className='notes-archive-cards';
      for(const note of notes){
        const button=document.createElement('button');
        button.type='button';button.className='notes-record-item notes-archive-item';
        button.setAttribute('data-archived-note-id',note.id);
        const heading=document.createElement('strong');
        heading.textContent='Psaume '+note.psalmNumber+' · Note '+note.noteNumber+
          (note.appliesTo?.verse?' · Verset '+note.appliesTo.verse:'');
        const status=document.createElement('span');
        status.className='notes-review-status '+(note.publicationStatus==='published'?
          'notes-review-published':'notes-review-pending');
        status.textContent=note.publicationStatus==='published'?'Déjà publiée':'Transcription à vérifier';
        const excerpt=document.createElement('span');excerpt.className='notes-record-preview';
        const plain=note.text.replace(/\s+/g,' ').trim();
        excerpt.textContent=plain.length>158?
          plain.slice(0,158).replace(/\s+\S*$/,'').trimEnd()+'…':plain;
        const source=document.createElement('span');source.className='notes-record-location';
        source.textContent='Document source : page PDF '+note.sourcePdfPage;
        button.append(heading,status,excerpt,source);
        button.addEventListener('click',()=>open(note.id));
        grid.append(button);
      }
      group.append(grid);frag.append(group);
    }
    if(!shown.length){
      const empty=document.createElement('p');empty.className='empty';
      empty.textContent='Aucune note ne correspond à cette recherche.';
      frag.append(empty);
    }
    target.replaceChildren(frag);
  }
  function loadArchivedNotes(){
    if(state.archivedNotes)return Promise.resolve(true);
    if(state.archivedNoteLoading)return state.archivedNoteLoading;
    $('notesArchiveCount').textContent='Chargement des 280 notes extraites…';
    state.archivedNoteLoading=fetch('data/notes-extracted-public.json?v=133')
      .then(response=>{
        if(!response.ok)throw Error('notes-extracted-public');
        return response.json();
      }).then(archive=>{
        if(archive.schemaVersion!==1||
           archive.purpose!=='public-navigation-of-archived-note-extractions-not-documentary-validation'||
           archive.archiveCount!==280||archive.alreadyPublishedCount!==11||
           archive.needsReviewCount!==269||archive.bookCount!==41||
           !Array.isArray(archive.notes)||archive.notes.length!==280)
          throw Error('Index des notes incomplet : aucune transcription provisoire ne doit être présentée comme validée.');
        const ids=new Set();
        for(const note of archive.notes){
          if(!note.id||ids.has(note.id)||note.recordType!=='note'||
             !note.text||!['published','unverified'].includes(note.publicationStatus))
            throw Error('Note archivée manquante, dupliquée ou mal identifiée.');
          ids.add(note.id);
        }
        state.archivedNotes=archive.notes;
        state.archivedNoteById=new Map(archive.notes.map(note=>[note.id,note]));
        const books=[...new Set(archive.notes.map(note=>note.bookNumber))].sort((a,b)=>a-b);
        const filter=$('notesArchiveBook');
        filter.replaceChildren();
        const all=document.createElement('option');all.value='';all.textContent='Tous les livres';
        filter.append(all);
        for(const n of books){
          const option=document.createElement('option');option.value=String(n);
          option.textContent='Livre '+n+' ('+archive.perBookCounts[String(n)]+' notes)';
          filter.append(option);
        }
        renderArchivedNotes();return true;
      }).catch(error=>{
        console.error(error);
        $('notesArchiveCount').textContent='Les notes n’ont pas pu être chargées. Fermez puis rouvrez « Notes » pour réessayer.';
        return false;
      }).finally(()=>{state.archivedNoteLoading=null;});
    return state.archivedNoteLoading;
  }
  function showNotesTab(tab){
    const published=tab==='published';
    state.notesTab=published?'published':'archive';
    $('notesAllToggle').setAttribute('aria-pressed',String(!published));
    $('notesPublishedToggle').setAttribute('aria-pressed',String(published));
    $('notesArchivePanel').hidden=published;
    $('notesPublishedInfo').hidden=!published;
    if(!published){
      $('notesThemePicker').hidden=true;
      $('notesThemeResults').hidden=true;
      void loadArchivedNotes();
      return;
    }
    returnToNoteThemes(false);
    if(state.corpusReady)renderNoteThemeDirectory();
    else {
      $('notesThemeList').textContent='Chargement des 11 notes déjà publiées…';
      void ensureCorpusReady().then(ok=>{
        if($('notesLibrary').hidden||state.notesTab!=='published')return;
        if(ok)renderNoteThemeDirectory();
        else $('notesThemeList').textContent='Notes publiées indisponibles. Vous pouvez revenir aux 280 notes extraites.';
      });
    }
  }
  function noteCard(record,titleOverride='') {
    if (!record || type(record)!=='note') return null;
    const id=record.id,parts=id.split('-');
    const context=parts.length===6?'Livre '+Number(parts[1])+' · Psaume '+Number(parts[3])+' · Note '+Number(parts[5]):'Note';
    const button=document.createElement('button');
    button.type='button';button.className='notes-record-item';
    const heading=document.createElement('strong');
    heading.textContent=titleOverride||'Lire la note';
    const location=document.createElement('span');
    location.className='notes-record-location';location.textContent=context;
    const body=document.createElement('span');
    body.className='notes-record-preview';
    const text=String(record.text||record.summary||'').replace(/\s+/g,' ').trim();
    if (text) {
      const sample=text.length>145?text.slice(0,145).replace(/\s+\S*$/,'').trimEnd()+'…':text;
      body.textContent=sample;
    }
    const action=document.createElement('span');
    action.className='notes-open-action';action.textContent='Ouvrir la note →';
    button.append(heading,location,body,action);
    button.addEventListener('click',()=>open(id));
    return button;
  }
  function renderNoteThemeDirectory() {
    const list=$('notesThemeList'),needle=norm($('notesThemeFilter').value||'');
    list.replaceChildren();
    for (const theme of state.noteThemes.filter(t=>!needle||norm(t.label).includes(needle))) {
      const button=document.createElement('button');
      button.type='button';button.className='notes-theme-item';
      button.textContent=theme.label+' ('+theme.noteIds.length+')';
      button.addEventListener('click',()=>openNoteTheme(theme));
      list.append(button);
    }
    if (!list.children.length) {
      const empty=document.createElement('p');empty.className='muted';empty.textContent='Aucun sujet trouvé.';list.append(empty);
    }
    // Cross-references are navigable, but never advertised as thematic subjects.
    const refSection=$('notesReferenceSection'),refList=$('notesReferenceList');
    refList.replaceChildren();
    for (const ref of state.noteReferences.filter(r=>!needle||norm(r.label).includes(needle))) {
      const record=state.recordById.get(ref.id);
      const card=noteCard(record,ref.label);
      if (card) refList.append(card);
    }
    refSection.hidden=!refList.children.length;
  }
  function openNoteTheme(theme) {
    state.selectedNoteTheme=theme.label;
    $('notesThemePicker').hidden=true;$('notesThemeResults').hidden=false;
    $('notesSelectedTheme').textContent=theme.label+' — '+theme.noteIds.length+' note'+(theme.noteIds.length>1?'s':'');
    const list=$('notesResultList');list.replaceChildren();
    for (const id of theme.noteIds) {
      const record=state.recordById.get(id);
      const card=noteCard(record);
      if (card) list.append(card);
    }
  }
  function returnToNoteThemes(shouldFocus=true) {
    state.selectedNoteTheme=null;$('notesThemeResults').hidden=true;$('notesThemePicker').hidden=false;
    if(shouldFocus===true)$('notesThemeFilter').focus({preventScroll:true});
  }
  function showSearchView() {
    closeBibleThemes();
    BiblawFAQ.close();
    $('faqToggle').setAttribute('aria-expanded','false');
    document.body.classList.remove('view-notes');
    $('notesLibrary').hidden=true;
    $('notesLibraryToggle').setAttribute('aria-expanded','false');
  }
  function toggleNotesLibrary(forceClose=false) {
    const panel=$('notesLibrary'),show=!forceClose&&panel.hidden;
    if (!show) {
      showSearchView();
      $('notesLibraryToggle').focus({preventScroll:true});
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    BiblawFAQ.close();
    $('faqToggle').setAttribute('aria-expanded','false');
    $('notesThemeFilter').value='';
    $('notesArchiveSearch').value='';
    $('notesArchiveBook').value='';
    panel.hidden=false;
    document.body.classList.add('view-notes');
    $('notesLibraryToggle').setAttribute('aria-expanded','true');
    showNotesTab('archive');
    window.scrollTo({top:0,behavior:'smooth'});
  }
  function focusSearchOutcome() {
    const target=$('ambiguityPanel').hidden?document.querySelector('.results-section'):$('ambiguityPanel');
    if (target)target.scrollIntoView({behavior:'smooth',block:'start'});
  }
  function open(id, citedVerses=null){
    const r=state.recordById.get(id)||state.archivedNoteById.get(id);if(!r)return;
    const targetVerses=Array.isArray(citedVerses)&&r.recordType==='psalm'?new Set(citedVerses.map(Number)):null;
    const fromFAQ=Boolean(targetVerses?.size);
    state.active=r;
    $('dialogEyebrow').textContent=label(r);
    $('dialogTitle').textContent=r.title||(r.recordType==='master-prayer'?`Prière ${r.number}`:r.recordType==='note'&&r.bookNumber?
      'Note '+r.noteNumber+' · Livre '+r.bookNumber+' · Psaume '+r.psalmNumber:'Note associée');
    const hasPrayer=r.recordType==='psalm'&&Boolean(r.attachedPrayer?.text);
    state.readerPart=fromFAQ?'psalm':hasPrayer?'both':'psalm';
    $('faqReturnFromPsalm').hidden=!fromFAQ;
    $('faqVerseContext').hidden=!fromFAQ;
    $('faqVerseContext').textContent=fromFAQ?'Versets cités dans la réponse : '+[...targetVerses].join(', '):'';
    $('readerChoice').hidden=!hasPrayer;
    document.querySelectorAll('[name=readerPart]').forEach(input=>{input.checked=input.value===state.readerPart;});
    $('readerExportStatus').hidden=true;
    if(r.recordType==='psalm'){
      const verses=(r.verses||[]).map(v=>`<div class="verse${targetVerses?.has(Number(v.number))?' faq-cited-verse':''}" data-verse="${esc(v.number)}"><div class="verse-number">${v.number}</div><div>${v.speakerId?`<span class="speaker">${esc(v.speakerId.replaceAll('-',' '))} · ${esc(v.speechRole||'')}</span>`:''}${modeAwareText(v.text)}</div></div>`).join('');
      const themesBlock=`<section class="related-themes dialog-themes"><div class="context-label">Thèmes présents dans ce psaume</div>${themeTags(state.themesByRecord.get(r.id)||[])}</section>`;
      const prayerBlock=hasPrayer?`<section class="prayer-block"><h3>Prière ${r.attachedPrayer.number}</h3>${modeAwareText(r.attachedPrayer.text)}</section>`:'';
      state.readerHtml={psalm:verses+themesBlock,prayer:prayerBlock};
    }else{
      const preliminary=r.publicationStatus==='unverified';
      const source=r.sourcePdfPage?
        '<p class="notes-source-reference">Source : Bible essénienne · PDF page '+r.sourcePdfPage+
        ' · <a href="Bible%20ess%C3%A9nienne%20(class%C3%A9e%20par%20livres).pdf#page='+r.sourcePdfPage+
        '" target="_blank" rel="noopener">Voir la page du document</a></p>':'';
      const warning=preliminary?
        '<p class="notes-review-warning" role="note"><strong>Transcription automatique à vérifier.</strong> '+
        'Ce texte peut comporter des erreurs. Consultez le document d’origine avant de le citer.</p>':'';
      state.readerHtml={psalm:warning+source+'<div class="prayer-block">'+modeAwareText(r.text||r.summary||'')+'</div>',prayer:''};
    }
    renderReader();
    $('recordDialog').showModal();
    if(fromFAQ)requestAnimationFrame(()=>{
      const first=$('dialogContent').querySelector('.faq-cited-verse');
      first?.scrollIntoView({block:'center',behavior:'instant'});
    });
  }
  function renderReader(){
    const visible=state.readerPart, parts=state.readerHtml||{psalm:'',prayer:''};
    $('dialogContent').innerHTML=(visible!=='prayer'?parts.psalm:'')+(visible!=='psalm'?parts.prayer:'');
    bindThemeLinks($('dialogContent'));
    $('dialogContent').scrollTop=0;
  }
  function activeText(){
    const r=state.active;if(!r)return'';
    if(r.recordType==='psalm'){
      const psalm=state.readerPart!=='prayer'?(r.verses||[]).map(v=>`${v.number}. ${v.text}`).join('\n'):'';
      const prayer=state.readerPart!=='psalm'&&r.attachedPrayer?.text?`Prière ${r.attachedPrayer.number}\n\n${r.attachedPrayer.text}`:'';
      return [psalm,prayer].filter(Boolean).join('\n\n');
    }
    return r.text||r.summary||'';
  }
  // 106: The bottom-page A–Z directory is a view over the SAME validated
  // themeDirectory, thematicItems() and Psalm reader used by normal search.
  // It never rebuilds an independent thematic corpus or invents relevance.
  function bibleThemeLetter(label){
    const first=String(label||'').trim().normalize('NFD')
      .replace(/[\u0300-\u036f]/g,'').charAt(0).toUpperCase();
    return /^[A-Z]$/.test(first)?first:'0–9';
  }
  function setBibleThemesStatus(message){
    $('bibleThemesStatus').textContent=message;
    $('bibleThemesStatus').hidden=!message;
  }
  function renderBibleThemesAlphabetical(){
    if(!state.bibleThemesSorted){
      state.bibleThemesSorted=[...state.themeDirectory].sort((a,b)=>
        a.label.localeCompare(b.label,'fr',{sensitivity:'base',numeric:true})||
        a.id.localeCompare(b.id,'fr'));
    }
    const query=norm($('bibleThemesFilter').value);
    const shown=query?state.bibleThemesSorted.filter(t=>norm(t.label).includes(query)):state.bibleThemesSorted;
    $('bibleThemesCount').textContent=shown.length+' thème'+(shown.length>1?'s':'')+
      (query?' trouvé'+(shown.length>1?'s':'')+' sur '+state.bibleThemesSorted.length:' indexés');
    let letter='',html='',letters=[];
    for(const theme of shown){
      const group=bibleThemeLetter(theme.label);
      if(group!==letter){
        letter=group;letters.push(group);
        html+='<h3 class="bible-themes-letter" id="bible-themes-letter-'+esc(group)+'">'+esc(group)+'</h3>';
      }
      html+='<button type="button" data-bible-theme-id="'+esc(theme.id)+'"><span><strong>'+
        esc(theme.label)+'</strong><small>'+Number(theme.occurrenceCount||theme.occurrences?.length||0)+
        ' psaumes indexés</small></span><span aria-hidden="true">›</span></button>';
    }
    $('bibleThemesDirectory').innerHTML=html||'<p class="empty">Aucun thème ne correspond à cette recherche.</p>';
    $('bibleThemesLetters').hidden=Boolean(query);
    $('bibleThemesLetters').innerHTML=query?'':letters.map(l=>
      '<button type="button" data-bible-theme-letter="'+esc(l)+'" aria-label="Aller à la lettre '+esc(l)+'">'+
      esc(l)+'</button>').join('');
  }
  function selectBibleTheme(theme){
    if(!state.corpusReady)return;
    state.bibleThemeDirectoryScroll=window.scrollY;
    state.bibleThemeSelected=theme.id;
    const items=thematicItems([theme],true).sort((a,b)=>
      importanceRank(a.thematic?.importance)-importanceRank(b.thematic?.importance)||
      (b.thematic?.score||0)-(a.thematic?.score||0)||
      Number(a.record.number)-Number(b.record.number)||
      a.record.id.localeCompare(b.record.id,'fr'));
    $('bibleThemeSelected').textContent=theme.label;
    $('bibleThemeResultCount').textContent=items.length+' psaume'+(items.length>1?'s':'')+' pour ce thème.';
    const groups=new Map();
    for(const item of items){
      const rank=importanceLabel(item.thematic?.importance);
      if(!groups.has(rank))groups.set(rank,[]);
      groups.get(rank).push(item);
    }
    let html='';
    for(const [rank,entries] of groups){
      html+='<h4 class="bible-theme-group-heading">'+esc(rank)+' — '+entries.length+
        ' psaume'+(entries.length>1?'s':'')+'</h4>';
      for(const item of entries){
        const r=item.record;
        const book=r.book?.number?'Livre '+r.book.number+' · ':'';
        html+='<button type="button" data-bible-theme-psalm="'+esc(r.id)+'"><span><strong>Psaume '+
          esc(r.number)+' — '+esc(r.title||'Sans titre')+'</strong><small>'+
          esc(book+archangelName(r.archangel))+'</small></span>'+
          '<span class="bible-theme-psalm-rank">'+esc(rank)+' ›</span></button>';
      }
    }
    $('bibleThemePsalmList').innerHTML=html||'<p class="empty">Aucun psaume indexé pour ce thème.</p>';
    $('bibleThemesIndex').hidden=true;
    $('bibleThemeResults').hidden=false;
    setBibleThemesStatus('');
    window.scrollTo({top:0,behavior:'instant'});
    $('bibleThemeSelected').focus({preventScroll:true});
  }
  function closeBibleThemes(){
    state.bibleThemeRequestId++;
    $('bibleThemesLibrary').hidden=true;
    $('bibleThemesToggle').setAttribute('aria-expanded','false');
    document.body.classList.remove('view-bible-themes');
  }
  function openBibleThemes(){
    showSearchView();
    const id=++state.bibleThemeRequestId;
    $('bibleThemesLibrary').hidden=false;
    document.body.classList.add('view-bible-themes');
    $('bibleThemesToggle').setAttribute('aria-expanded','true');
    $('bibleThemesFilter').value='';
    state.bibleThemeSelected=null;
    $('bibleThemesIndex').hidden=false;
    $('bibleThemeResults').hidden=true;
    window.scrollTo({top:0,behavior:'instant'});
    if(state.corpusReady){
      renderBibleThemesAlphabetical();setBibleThemesStatus('');
    }else{
      $('bibleThemesDirectory').replaceChildren();
      $('bibleThemesLetters').replaceChildren();
      $('bibleThemesCount').textContent='';
      setBibleThemesStatus('Chargement des thèmes de la Bible…');
      void ensureCorpusReady().then(ok=>{
        if(id!==state.bibleThemeRequestId||$('bibleThemesLibrary').hidden)return;
        if(ok){renderBibleThemesAlphabetical();setBibleThemesStatus('');}
        else setBibleThemesStatus('Impossible de charger les thèmes. Appuyez sur Retour puis réessayez.');
      });
    }
  }
  function backFromBibleThemes(){
    if(!$('bibleThemeResults').hidden){
      const id=state.bibleThemeSelected;
      state.bibleThemeSelected=null;
      $('bibleThemeResults').hidden=true;
      $('bibleThemesIndex').hidden=false;
      window.scrollTo({top:state.bibleThemeDirectoryScroll,behavior:'instant'});
      const button=[...$('bibleThemesDirectory').querySelectorAll('[data-bible-theme-id]')]
        .find(b=>b.dataset.bibleThemeId===id);
      button?.focus({preventScroll:true});
      return;
    }
    closeBibleThemes();
    window.scrollTo({top:0,behavior:'instant'});
    $('bibleThemesToggle').focus({preventScroll:true});
  }
  $('bibleThemesToggle').onclick=openBibleThemes;
  $('bibleThemesBack').onclick=backFromBibleThemes;
  $('bibleThemesFilter').oninput=()=>{if(state.corpusReady)renderBibleThemesAlphabetical();};
  $('bibleThemesLetters').onclick=event=>{
    const button=event.target.closest('[data-bible-theme-letter]');
    if(!button)return;
    const letter=button.dataset.bibleThemeLetter;
    const heading=[...$('bibleThemesDirectory').querySelectorAll('.bible-themes-letter')]
      .find(h=>h.textContent===letter);
    heading?.scrollIntoView({behavior:'instant',block:'start'});
  };
  $('bibleThemesDirectory').onclick=event=>{
    const button=event.target.closest('[data-bible-theme-id]');
    if(!button)return;
    const theme=state.themeById.get(button.dataset.bibleThemeId);
    if(theme)selectBibleTheme(theme);
  };
  $('bibleThemePsalmList').onclick=event=>{
    const button=event.target.closest('[data-bible-theme-psalm]');
    if(button&&state.recordById.has(button.dataset.bibleThemePsalm))
      open(button.dataset.bibleThemePsalm);
  };

  function renderThemeDirectory(){ const needle=norm($('themeFilter').value); const visible=needle?state.themeDirectory.filter(t=>norm(t.label).includes(needle)||norm(t.id).includes(needle)):state.themeDirectory; $('indexCount').textContent=needle?`${visible.length} thème${visible.length>1?'s':''} sur ${state.themeDirectory.length}`:`${state.themeDirectory.length} thèmes indexés`; $('themeDirectory').innerHTML=visible.length?visible.map(t=>`<button class="theme-row" data-directory-theme="${esc(t.id)}"><span><strong>${esc(t.label)}</strong><small>${t.occurrenceCount} psaume${t.occurrenceCount>1?'s':''}</small></span><span aria-hidden="true">›</span></button>`).join(''):'<div class="empty">Aucun thème ne correspond à ce filtre.</div>'; $('themeDirectory').querySelectorAll('[data-directory-theme]').forEach(b=>b.onclick=()=>{const t=state.themeById.get(b.dataset.directoryTheme);if(t){closeIndex();navigateToTheme(t);}}); }
  function openIndex(){
    $('indexPanel').hidden=false;
    $('indexBackdrop').hidden=false;
    $('indexToggle').setAttribute('aria-expanded','true');
    if(state.corpusReady)renderThemeDirectory();
    else {
      $('indexCount').textContent='Chargement des thèmes du corpus…';
      $('themeDirectory').replaceChildren();
      void ensureCorpusReady().then(ok=>{
        if($('indexPanel').hidden)return;
        if(ok)renderThemeDirectory();
        else $('indexCount').textContent='Index indisponible. Fermez puis réessayez.';
      });
    }
    requestAnimationFrame(()=>$('themeFilter').focus());
  }
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
  function choosePopularQuestion(question){ if(!question)return; $('query').value=question.text; $('query2').value=''; activateThemeMode(); closePopularQuestions();showSearchView();search();requestAnimationFrame(focusSearchOutcome); }

  // 084: Adding a term never opens another field or an explanation panel.
  // The two-word priority ranking still uses rankExactWordPairs().
  const setAdvancedSearch = open => {
    $('primarySearch').classList.remove('advanced-visible');
    $('advancedSearchToggle').hidden=true;
    $('advancedSearchToggle').setAttribute('aria-expanded','false');
    $('query2').value='';
    $('query2').disabled=true;
    $('dualExactHelp').hidden=true;
    updateExpansionControl();
  };
  $('addQueryTerm').onclick=()=>{
    const field=$('query'),current=field.value.trim();
    if(!current){field.focus({preventScroll:true});return;}
    // Only two terms in the current priority-ranking logic.
    if(current.includes('+')){
      field.focus({preventScroll:true});
      field.setSelectionRange(field.value.length,field.value.length);
      return;
    }
    if(state.mode!=='exact')activateExactMode();
    field.value=current+' + ';
    closeAllSuggestions();
    field.focus({preventScroll:true});
    field.setSelectionRange(field.value.length,field.value.length);
  };
  $('searchButton').onclick=()=>{showSearchView();search();if($('query').value.trim())requestAnimationFrame(focusSearchOutcome);}; $('query').addEventListener('keydown',e=>{if(e.key==='Enter'){showSearchView();search();if($('query').value.trim())requestAnimationFrame(focusSearchOutcome);}}); $('query').addEventListener('input',handleExactQueryInput);
  $('query').addEventListener('input',()=>{
    if($('query').value.trim())void ensureCorpusReady();
  });
  $('query').addEventListener('change',correctMobileQueryDuplicate);
  $('query').addEventListener('blur',correctMobileQueryDuplicate);
  $('query').addEventListener('focus',correctMobileQueryDuplicate);
  $('query').addEventListener('compositionend',()=>setTimeout(correctMobileQueryDuplicate,0)); $('query2').addEventListener('keydown',e=>{if(e.key==='Enter'){search();requestAnimationFrame(focusSearchOutcome);}}); document.querySelectorAll('[name=sourceType]').forEach(x=>x.onchange=()=>{if(x.checked&&x.value!=='psalm'&&state.mode==='themes')activateExactMode();const selected=selectedTypes();$('scopeInfo').hidden=state.mode==='themes'&&selected.size>0;$('scopeInfo').textContent=selected.size?'Recherche par mots dans les catégories cochées.':'Sélectionnez au moins un type de texte.';search();}); $('archangelFilter').onchange=search; $('includeWordForms').onchange=search;
  $('modeThemes').onclick=()=>{activateThemeMode();search();}; $('modeExact').onclick=()=>{activateExactMode();$('scopeInfo').hidden=false;$('scopeInfo').textContent='Recherche par mots dans les catégories cochées.';search();}; $('closeAmbiguity').onclick=hideAmbiguity;
  $('popularQuestionsToggle').onclick=openPopularQuestions; $('closePopularQuestions').onclick=closePopularQuestions; $('popularQuestionsBackdrop').onclick=closePopularQuestions; $('popularQuestionsBack').onclick=renderPopularQuestionFamilies;
  $('indexToggle').onclick=()=>{$('indexPanel').hidden?openIndex():closeIndex();}; $('themeFilter').oninput=()=>{if(state.corpusReady)renderThemeDirectory();}; $('closeIndex').onclick=closeIndex; $('indexBackdrop').onclick=closeIndex; $('closeDialog').onclick=()=>$('recordDialog').close(); $('printRecord').onclick=()=>window.print(); $('downloadRecord').onclick=()=>{
    if(!state.active)return;
    const status=$('readerExportStatus');status.hidden=true;
    try{
      const scope=state.active.recordType==='psalm'?(state.active.attachedPrayer?.text?state.readerPart:'psalm'):'both';
      BiblawPDF.download(state.active,scope);
    }catch(error){
      status.textContent='Téléchargement impossible : '+String(error?.message||error);
      status.hidden=false;
    }
  };
  document.querySelectorAll('[name=readerPart]').forEach(x=>x.onchange=()=>{if(!x.checked||!state.active?.attachedPrayer?.text)return;state.readerPart=x.value;renderReader();});
  BiblawFAQ.setOpenPsalm(ref=>open(ref.recordId,ref.verses));
  $('faqToggle').addEventListener('click',()=>{
    showSearchView();
    BiblawFAQ.open();
    $('faqToggle').setAttribute('aria-expanded','true');
  });
  $('faqReturnFromPsalm').onclick=()=>$('recordDialog').close();
  $('recordDialog').addEventListener('close',()=>{
    BiblawFAQ.restoreAfterPsalm();
    $('faqReturnFromPsalm').hidden=true;
  });
  $('notesLibraryToggle').addEventListener('click',()=>toggleNotesLibrary());
  $('notesLibraryClose').addEventListener('click',()=>{
    if(state.notesTab==='published'){
      if(!$('notesThemeResults').hidden){returnToNoteThemes();return;}
      showNotesTab('archive');return;
    }
    toggleNotesLibrary(true);
  });
  $('notesAllToggle').onclick=()=>showNotesTab('archive');
  $('notesPublishedToggle').onclick=()=>showNotesTab('published');
  $('notesArchiveSearch').addEventListener('input',()=>{if(state.archivedNotes)renderArchivedNotes();});
  $('notesArchiveBook').addEventListener('change',()=>{if(state.archivedNotes)renderArchivedNotes();});
  $('notesThemeFilter').addEventListener('input',renderNoteThemeDirectory);

  bindSuggestions();
  // A function deliberately defers the expensive load until a Psalm is opened.
  BiblawFAQ.setCorpusLoading(ensureCorpusReady);
})();