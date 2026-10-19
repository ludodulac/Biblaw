import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const live=process.env.BIBLAW_SMOKE_URL;
const baseline='https://rawcdn.githack.com/ludodulac/Biblaw/0d75b9bf44e7e188c2de333efbc7c9c74e844152/index.html';
if(!live)throw Error('BIBLAW_SMOKE_URL is required');
const browser=await chromium.launch({headless:true});
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/-/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();

async function open(url){
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(45000);
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent?.includes('psaumes'),null,{timeout:60000});
  return {page,errors};
}
const total=page=>page.locator('#themeAutocomplete').getAttribute('data-total-suggestions').then(s=>Number(s||0));

async function getVisibleEntries(page,at){
  const box=page.locator('#themeAutocomplete');
  if(at!==undefined){
    await box.evaluate((e,index)=>e.scrollTop=Math.max(0,32+(index-3)*64),at);
    await page.waitForTimeout(35);
  }
  return box.locator('[data-autocomplete-word]').evaluateAll(nodes=>nodes.map(n=>({
    index:Number(n.dataset.suggestionIndex),label:n.dataset.autocompleteWord
  })));
}
async function suggestions(page,term){
  await page.locator('#query').fill(term);
  const t=await total(page);
  assert.ok(t>0,'MOTS: suggestions for '+term);
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),true,'MOTS dropdown visible for '+term);
  assert.ok((await page.locator('#themeAutocomplete [role="option"]').count())<=18,'Only 18 DOM options at once');
  const picks=[0,Math.floor(t/4),Math.floor(t/2),Math.floor(3*t/4),Math.max(0,t-1)];
  const observed=new Map();
  for(const i of picks)for(const entry of await getVisibleEntries(page,i))observed.set(entry.index,entry.label);
  assert.ok(observed.size>=Math.min(t,3),'Can scroll and inspect entries for '+term);
  for(const label of observed.values())assert.ok(norm(label).startsWith(norm(term)),
    'Must match phrase beginning: '+term+' unexpectedly offered '+label);
  const dimensions=await page.locator('#themeAutocomplete').evaluate(e=>({
    height:e.clientHeight,scrollHeight:e.scrollHeight,viewport:innerHeight
  }));
  assert.ok(dimensions.height<dimensions.viewport/2,'Compact scrollable dropdown');
  return {total:t,sample:[...observed.values()].slice(0,8)};
}
async function searchIds(page,query,mode){
  await page.locator(mode==='themes'?'#modeThemes':'#modeExact').click();
  await page.locator('#query').fill(query);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}

try{
  const {page,errors}=await open(live);
  assert.equal(await page.locator('#modeThemes').getAttribute('aria-pressed'),'true','Theme is default');
  await page.locator('#query').fill('el');
  const themeFirst={total:Number(await page.locator('#themeAutocomplete').getAttribute('data-total-suggestions')),
    values:await page.locator('[data-autocomplete-theme]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.autocompleteTheme,label:n.textContent})))};
  assert.ok(themeFirst.total>0,'Theme autocomplete remains available');

  await page.locator('#modeExact').click();
  await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  const terms=['el','ele','elem','element','élément','éléments','père','monde'];
  const records={};
  for(const term of terms)records[term]=await suggestions(page,term);
  assert.equal(records['element'].total,records['élément'].total,'Accentless element equals élément');
  for(const term of ['el','ele','elem','element']){
    assert.ok(records[term].total>=records['élément'].total,'More characters may only narrow suggestions '+term);
  }
  // All suggestions are sourced from the entire corpus, so inspect all virtual rows for element.
  await page.locator('#query').fill('element');
  const count=await total(page),all=new Map();
  for(let i=0;i<count;i+=10)for(const entry of await getVisibleEntries(page,i))all.set(entry.index,entry.label);
  for(const label of all.values())assert.ok(norm(label).startsWith('element'),'Non-prefix expression excluded: '+label);
  assert.ok(all.size>=count-6,'Every virtual suggestion remains reachable for element');
  for(const phrase of ['4 éléments','quatre éléments','soi et des éléments','vitamine et élément','volonté et les éléments']){
    assert.ok(![...all.values()].some(s=>norm(s)===norm(phrase)),'Must not propose: '+phrase);
  }
  // The attested hyphenated expression was confirmed in the previous 053 release.
  await page.locator('#query').fill('père');
  const pèreTotal=await total(page),père=new Map();
  for(let i=0;i<pèreTotal;i+=11)for(const entry of await getVisibleEntries(page,i))père.set(entry.index,entry.label);
  assert.ok([...père.values()].some(s=>norm(s)===norm('Père-Mère')),'Père-Mère is suggested from père');
  await page.locator('#query').fill('monde');
  const mondeTotal=await total(page),monde=new Map();
  for(let i=0;i<mondeTotal;i+=11)for(const entry of await getVisibleEntries(page,i))monde.set(entry.index,entry.label);
  assert.ok([...monde.values()].some(s=>norm(s).startsWith('monde de ')),
    'Real world phrases starting with monde are preserved');
  assert.equal(await page.locator('#includeSimplePlurals').isChecked(),true,'Plural option remains checked');

  // Compare actual results against the pinned, previously tested 053C release.
  const reference=(await open(baseline)).page;
  const beforeTheme=await searchIds(reference,'sainte assemblée','themes');
  const afterTheme=await searchIds(page,'sainte assemblée','themes');
  assert.deepEqual(afterTheme,beforeTheme,'Thematic rankings and psalm IDs unchanged');
  await reference.locator('#query').fill('el');
  const earlierTheme={total:Number(await reference.locator('#themeAutocomplete').getAttribute('data-total-suggestions')),
    values:await reference.locator('[data-autocomplete-theme]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.autocompleteTheme,label:n.textContent})))};
  assert.deepEqual(themeFirst,earlierTheme,'Theme suggestion selection and order unchanged');

  for(const term of ['élément','monde','père']){
    const oldIds=await searchIds(reference,term,'words');
    const nowIds=await searchIds(page,term,'words');
    assert.deepEqual(nowIds,oldIds,'Exact psalm results unchanged: '+term);
  }
  assert.deepEqual(errors,[],'No browser runtime errors');
  console.log('BIBLAW-053D MOBILE LIVE PASS '+JSON.stringify({
    terms:records,elementPrefixResults:count,pereCompound:'Père-Mère',
    mondeStarts:mondeTotal,themeSuggestions:themeFirst.total,themePsalms:afterTheme.length,
    comparedExactSearches:['élément','monde','père'],
    previewUrl:live
  }));
  await reference.close();
}finally{await browser.close();}
