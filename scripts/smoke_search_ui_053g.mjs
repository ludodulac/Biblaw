import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL;
const previous='https://rawcdn.githack.com/ludodulac/Biblaw/18acbf8b96d38a5da2c59e3cf2e51119e29b034f/index.html';
if(!url)throw Error('BIBLAW_SMOKE_URL required');
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/-/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const browser=await chromium.launch({headless:true});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function visit(address,width=390){
  const page=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const res=await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
  assert.equal(res?.status(),200,'Public preview reachable');
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent?.includes('psaumes'),null,{timeout:90000});
  return {page,errors};
}
async function entries(page,term,mode='words'){
  const modeSelector=mode==='themes'?'#modeThemes':'#modeExact';
  if((await page.locator(modeSelector).getAttribute('aria-pressed'))!=='true')await page.locator(modeSelector).click();
  await page.locator('#query').fill(term);
  const box=page.locator('#themeAutocomplete');
  const visible=await box.isVisible();
  const total=visible?Number(await box.getAttribute('data-total-suggestions')):0;
  const all=new Map(),selector=mode==='words'?'[data-autocomplete-word]':'[data-autocomplete-theme]';
  if(visible){
    for(let i=0;i<total;i+=10){
      await box.evaluate((node,index)=>{node.scrollTop=Math.max(0,32+(index-3)*64)},i);
      await sleep(10);
      for(const e of await box.locator(selector).evaluateAll(nodes=>nodes.map(n=>({index:Number(n.dataset.suggestionIndex),word:n.textContent,label:n.dataset.autocompleteWord||n.dataset.autocompleteTheme}))))
        all.set(e.index,e);
    }
    assert.ok((await box.locator(selector).count())<=18,'max 18 virtual rows at '+term);
    assert.ok(await box.evaluate(node=>node.clientHeight<innerHeight/2),'mobile list remains compact');
  }
  return {term,total,found:[...all.values()].sort((a,b)=>a.index-b.index)};
}
async function resultIds(page,mode,term){
  const button=mode==='themes'?'#modeThemes':'#modeExact';
  if((await page.locator(button).getAttribute('aria-pressed'))!=='true')await page.locator(button).click();
  await page.locator('#query').fill(term);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}
try{
  const {page,errors}=await visit(url);
  const original=await visit(previous);
  const themesNow=await entries(page,'el','themes');
  const themesOld=await entries(original.page,'el','themes');
  assert.equal(themesNow.total,themesOld.total,'THEME unchanged count');
  assert.deepEqual(themesNow.found.slice(0,15).map(x=>x.label),themesOld.found.slice(0,15).map(x=>x.label),'THEME unchanged order');
  await page.locator('#modeExact').click();
  await original.page.locator('#modeExact').click();
  await Promise.all([page,original.page].map(p=>p.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000})));
  const count=Number(await page.locator('#query').getAttribute('data-hyphen-suggestion-count'));
  assert.ok(count>0,'Lexical hyphen index audit count published');

  const attestations=await page.evaluate(async()=>{
    const data=await(await fetch('data/browser-search-catalog.json')).json();
    const sources=(data.records||[]).flatMap(r=>r.recordType==='psalm'?[r.title,...(r.verses||[]).map(v=>v.text)]:[r.title,r.text,r.summary]).filter(Boolean);
    const variants=['au-delà','Père-Mère','soi-même','arc-en-ciel','celui-ci'];
    const matched=new Map(),characters=new Set();
    const hyphenTokens=/[\p{L}\p{N}]+(?:[’'][\p{L}\p{N}]+)*(?:[-‐‑‒–][\p{L}\p{N}]+(?:[’'][\p{L}\p{N}]+)*)+/gu;
    for(const source of sources){
      for(const word of String(source).match(hyphenTokens)||[]){
        matched.set(word,(matched.get(word)||0)+1);
        for(const ch of word)if(/[-‐‑‒–]/u.test(ch))characters.add(ch);
      }
    }
    return {rawUnique:matched.size,rawExamples:[...matched].sort((a,b)=>b[1]-a[1]).slice(0,40),
      variants:Object.fromEntries(variants.map(variant=>[variant,[...matched.keys()].filter(k=>k.toLowerCase()===variant.toLowerCase())])),
      glyphs:[...characters]};
  });
  console.log('053G_SOURCE_AUDIT '+JSON.stringify(attestations));
  console.log('053G_ACCEPTED_COMPOUNDS '+count);

  const queries=['au','au-','au-d','père','soi','arc','celui','element','quatre'];
  const results={};
  for(const term of queries){
    const value=await entries(page,term);
    results[term]=value;
    console.log('053G_SUGGEST '+JSON.stringify({term,total:value.total,hyphens:value.found.filter(x=>/[-‐‑‒–]/u.test(x.word)).slice(0,35).map(x=>x.word)}));
    assert.ok(value.found.every(x=>norm(x.word).startsWith(norm(term))||
      (/^\d+\s/u.test(x.word)&&/^[a-z]/u.test(norm(term)))),'No fragment/unrelated words for '+term);
  }
  for(const [candidate,searches] of [['au-delà',['au','au-','au-d']],['Père-Mère',['père']],['soi-même',['soi']],['arc-en-ciel',['arc']],['celui-ci',['celui']]]){
    if(attestations.variants[candidate].length){
      const actual=attestations.variants[candidate][0];
      for(const term of searches)assert.ok(results[term].found.some(x=>x.word===actual),
        'Attested lexical compound '+actual+' must be suggested from '+term);
      console.log('053G_ATTESTED_LEXICAL_COMPOUND '+actual+' via '+searches.join(','));
    }else console.log('053G_ABSENT_FROM_CORPUS '+candidate);
  }
  const example=(attestations.variants['au-delà']||[])[0]||
    (attestations.variants['soi-même']||[])[0]||
    (attestations.variants['Père-Mère']||[])[0];
  if(example){
    const first=norm(example).split(' ')[0];
    await page.locator('#query').fill(first);
    const positions=results[first]?.found|| (await entries(page,first)).found;
    const pick=positions.find(item=>item.word===example);
    assert.ok(pick,'Selected source-attested hyphenated compound is available');
    await page.locator('#themeAutocomplete').evaluate((node,i)=>node.scrollTop=Math.max(0,32+(i-3)*64),pick.index);
    await sleep(50);
    const chosen=page.locator('#themeAutocomplete [data-autocomplete-word]').filter({hasText:example}).first();
    assert.ok(await chosen.count(),'Compound button can be reached on phone');
    await chosen.evaluate(button=>button.click());
    assert.equal(await page.locator('#query').inputValue(),example,'Selecting preserves original source hyphens');
    const actual=await page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
    const same=await resultIds(original.page,'exact',example);
    assert.deepEqual(actual,same,'Click searches original compound with untouched occurrence engine');
  }
  // Fragments and numeric aliases must not regress.
  const el=results.element.found.map(x=>norm(x.word));
  for(const bad of ['élément à sa','soi et des éléments','volonté et les éléments','vitamine et élément'])
    assert.ok(!el.includes(norm(bad)),'No artificial prose fragment: '+bad);
  assert.ok(results.quatre.found.some(x=>x.word==='4 éléments'),'053F number-letter equivalence preserved');
  for(const [mode,term] of [['exact','élément'],['exact','4 éléments'],['themes','sainte assemblée']]){
    const now=await resultIds(page,mode,term),before=await resultIds(original.page,mode,term);
    assert.deepEqual(now,before,'Unchanged search results '+mode+' '+term);
  }
  const compact=await visit(url,320);
  await compact.page.locator('#modeExact').click();
  await compact.page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  const compactAu=await entries(compact.page,'au-d');
  if(attestations.variants['au-delà'].length)assert.ok(compactAu.found.some(x=>norm(x.word)===norm('au-delà')),'320px au-d');
  assert.deepEqual(errors,[],'No page JS errors');
  assert.deepEqual(original.errors,[],'Original page error-free');
  console.log('BIBLAW-053G LIVE MOBILE PASS '+JSON.stringify({url,acceptedHyphenCompounds:count,
    sourceHyphenGroups:attestations.rawUnique,glyphs:attestations.glyphs,
    attestedExamples:Object.fromEntries(Object.entries(attestations.variants).filter(([_,v])=>v.length)),
    checked:queries,smallMobile:'320px',regressions:['theme','053E fragments','053F numbers','search results']}));
}finally{await browser.close();}
