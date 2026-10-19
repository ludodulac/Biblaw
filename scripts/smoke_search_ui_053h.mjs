import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const url=process.env.BIBLAW_SMOKE_URL;
const old='https://rawcdn.githack.com/ludodulac/Biblaw/25f041dc4e1780233689b6f8badd8928151b6de8/index.html';
if(!url)throw Error('BIBLAW_SMOKE_URL required');
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[-‐‑‒–’']/g,' ').replace(/\s+/g,' ').trim();
const browser=await chromium.launch({headless:true});
const sleep=ms=>new Promise(done=>setTimeout(done,ms));
async function open(address,width=390){
  const page=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const response=await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
  assert.equal(response?.status(),200,'Public document HTTP 200');
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  return {page,errors};
}
async function suggestions(page,text,{mode='exact',walk=true}={}){
  const which=mode==='exact'?'#modeExact':'#modeThemes';
  if((await page.locator(which).getAttribute('aria-pressed'))!=='true')await page.locator(which).click();
  await page.locator('#query').fill(text);
  const menu=page.locator('#themeAutocomplete'),visible=await menu.isVisible();
  const total=visible?Number(await menu.getAttribute('data-total-suggestions')||0):0;
  const found=new Map(),selector=mode==='exact'?'[data-autocomplete-word]':'[data-autocomplete-theme]';
  if(visible){
    const starts=walk?Array.from({length:Math.ceil(total/11)},(_,i)=>i*11):[0];
    for(const pos of starts){
      await menu.evaluate((box,i)=>box.scrollTop=Math.max(0,32+(i-3)*64),pos);
      await sleep(8);
      const rows=await menu.locator(selector).evaluateAll((nodes,mode)=>
        nodes.map(node=>({index:Number(node.dataset.suggestionIndex),
          word:mode==='exact'?node.dataset.autocompleteWord:node.dataset.autocompleteTheme,
          display:node.textContent})),mode);
      for(const row of rows)found.set(row.index,row);
    }
    assert.ok((await menu.locator(selector).count())<=18,'Virtualized rows remain at most 18');
    assert.ok(await menu.evaluate(node=>node.clientHeight<innerHeight/2),'Small scrollable menu');
  }
  return {total,entries:[...found.values()]};
}
async function resultIds(page,mode,word){
  const which=mode==='themes'?'#modeThemes':'#modeExact';
  if((await page.locator(which).getAttribute('aria-pressed'))!=='true')await page.locator(which).click();
  await page.locator('#query').fill(word);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}
try{
  const {page,errors}=await open(url),baseline=await open(old);
  const themeNow=await suggestions(page,'el',{mode:'themes',walk:false}),themeBefore=await suggestions(baseline.page,'el',{mode:'themes',walk:false});
  assert.equal(themeNow.total,themeBefore.total,'Mode THÈME count unchanged');
  assert.deepEqual(themeNow.entries.map(x=>x.word),themeBefore.entries.map(x=>x.word),'Mode THÈME order unchanged');
  await page.locator('#modeExact').click();
  await baseline.page.locator('#modeExact').click();
  const start=Date.now();
  await Promise.all([page,baseline.page].map(p=>p.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000})));
  const readyMs=Date.now()-start;
  const internal=await page.locator('#query').evaluate(e=>({
    hyphen:+e.dataset.hyphenSuggestionCount,
    acceptedGenitive:+e.dataset.genitiveSuggestionCount,
    rejectedGenitive:+e.dataset.rejectedGenitiveCount
  }));
  assert.ok(internal.hyphen>0&&internal.acceptedGenitive>0&&internal.rejectedGenitive>0,'Grammar audit counters');
  const queries=['soi','soi me','au','au dela','elem','qu','4','père','monde','question','qualité','aura','aurez','soit','soient','b','c','d','p','v'];
  const before={},after={};
  for(const q of queries){
    if(q.length===1&&!/^\d$/u.test(q))continue;
    before[q]=await suggestions(baseline.page,q,{walk:!['soi','au','monde'].includes(q)});
    after[q]=await suggestions(page,q,{walk:!['soi','au','monde'].includes(q)});
    console.log('053H_QUERY '+JSON.stringify({q,before:before[q].total,after:after[q].total,
      sample:after[q].entries.slice(0,20).map(x=>x.display)}));
  }
  const expected=[
    ['soi','soi-même'],['soi me','soi-même'],['au','au-delà'],
    ['au dela','au-delà'],['père','Père-Mère'],['qu','4 éléments'],
    ['4','4 éléments'],['monde','monde de l’homme'],
    ['elem','éléments de la nature']
  ];
  for(const [typed,wanted] of expected)
    assert.ok(after[typed].entries.some(x=>norm(x.display)===norm(wanted)),
      'Retain attested autonomous expression '+wanted+' for '+typed);
  const bad=['soi-même dans','soi-même est','est au-delà','qui est au-delà',
    'élément à sa','soit de nouveau','soient des éléments','aurez des réponses',
    'aura des conséquences','question de transmettre','qualité de faire','Père de la belle'];
  for(const [q,value] of Object.entries(after))
    for(const forbidden of bad)
      assert.ok(!value.entries.some(x=>norm(x.display)===norm(forbidden)),
        'Exclude unclosed phrase '+forbidden+' for '+q);
  // Candidate-independent structural audit: any remaining multiword suggestion
  // must be a closed genitive, numeric label, or a lexical hyphen group.
  const acceptedGrammar=/^\S+(?:\s+(?:de|du|des)(?:\s+(?:le|la|les))?\s+\S+)$/iu;
  for(const [query,value] of Object.entries(after)){
    for(const item of value.entries){
      const word=item.display;
      if(word.includes(' ')&&!/^\d+\s/u.test(word)&&!/(?:[-‐‑‒–])/u.test(word)){
        assert.ok(acceptedGrammar.test(word),'Unstructured multiword candidate '+word+' from '+query);
      }
    }
  }
  const unchanged={};
  for(const [mode,query] of [['exact','soi-même'],['exact','l’au-delà'],
    ['exact','soi-même dans'],['exact','élément'],['exact','4 éléments'],
    ['exact','monde'],['themes','sainte assemblée']]){
    const left=await resultIds(page,mode,query),right=await resultIds(baseline.page,mode,query);
    assert.deepEqual(left,right,'Search engine results unchanged: '+mode+' '+query);
    unchanged[mode+' '+query]=left.length;
  }
  // Manually typed phrase must remain searchable, regardless of suggestion filter.
  await page.locator('#modeExact').click();
  await page.locator('#query').fill('soi-même dans');
  await page.locator('#query').press('Enter');
  assert.equal(await page.locator('#resultsSection').isVisible(),true,'Excluded phrase remains manually searchable');

  // Select retained expression; preserve the exact corpus spelling.
  const pick=await suggestions(page,'soi me'),choice=pick.entries.find(x=>norm(x.display)===norm('soi-même'));
  assert.ok(choice,'soi-même accessible in the dropdown');
  await page.locator('#themeAutocomplete').evaluate((e,i)=>e.scrollTop=Math.max(0,32+(i-3)*64),choice.index);
  await sleep(40);
  const clicked=page.locator('#themeAutocomplete [data-autocomplete-word="'+choice.word+'"]');
  assert.ok(await clicked.count(),'hyphenated word selectable');
  await clicked.first().evaluate(button=>button.click());
  assert.equal(await page.locator('#query').inputValue(),choice.word,'Selection preserves actual spelling');
  assert.deepEqual(await page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort()),
    await resultIds(baseline.page,'exact',choice.word),'Search after selection matches baseline');

  const small=await open(url,320);
  await small.page.locator('#modeExact').click();
  await small.page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  const smallResult=await suggestions(small.page,'au dela');
  assert.ok(smallResult.entries.some(x=>norm(x.display)===norm('au-delà')),'320px retains au-delà');
  assert.deepEqual(errors,[],'No errors current');
  assert.deepEqual(baseline.errors,[],'No errors baseline');
  console.log('BIBLAW-053H LIVE MOBILE PASS '+JSON.stringify({
    url,acceptedNominalExpressions:internal.acceptedGenitive,rejectedNominalFragments:internal.rejectedGenitive,
    hyphens:internal.hyphen,readyMs,counts:Object.fromEntries(Object.keys(after).map(q=>[q,{before:before[q].total,after:after[q].total}])),
    excluded:bad,retained:expected.map(x=>x[1]),unchanged,smallMobile:'320px'
  }));
}finally{await browser.close();}
