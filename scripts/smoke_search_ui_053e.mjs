import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL;
const beforeUrl='https://rawcdn.githack.com/ludodulac/Biblaw/18ecb534b3ec7ec4bd1aa3a4d29a212fc36c44eb/index.html';
if(!url)throw Error('BIBLAW_SMOKE_URL is required');
const browser=await chromium.launch({headless:true});
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/-/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
async function open(address){
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  return page;
}
async function getEntries(page,query){
  await page.locator('#query').fill(query);
  const box=page.locator('#themeAutocomplete');
  assert.ok(await box.isVisible(),query+' dropdown visible');
  const total=Number(await box.getAttribute('data-total-suggestions'));
  assert.ok(total>0,'Expected at least one suggestion for '+query);
  const entries=new Map();
  for(let i=0;i<total;i+=12){
    await box.evaluate((node,index)=>node.scrollTop=Math.max(0,32+64*index),i);
    await page.waitForTimeout(8);
    const subset=await box.locator('[data-autocomplete-word]').evaluateAll(nodes=>
      nodes.map(n=>({i:Number(n.dataset.suggestionIndex),label:n.dataset.autocompleteWord})));
    for(const entry of subset)entries.set(entry.i,entry.label);
  }
  assert.ok(entries.size>=total-5,'Virtual scroll permits reaching all '+total+' candidates for '+query);
  assert.ok((await box.locator('[data-autocomplete-word]').count())<=18,'Optimized 18-row virtual list');
  const values=[...entries.values()];
  assert.ok(values.every(v=>norm(v).startsWith(norm(query))),'Every candidate must begin with typed prefix: '+query);
  return {total,values};
}
async function results(page,mode,query){
  await page.locator(mode==='exact'?'#modeExact':'#modeThemes').click();
  await page.locator('#query').fill(query);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}
try{
  const page=await open(url);
  const old=await open(beforeUrl);
  // THÈME is a byte-for-byte invariant: compare behavior on both real URLs.
  await page.locator('#query').fill('el');
  await old.locator('#query').fill('el');
  const theme=await page.locator('#themeAutocomplete').evaluate(e=>({count:e.dataset.totalSuggestions,first:[...e.querySelectorAll('[data-autocomplete-theme]')].map(n=>n.dataset.autocompleteTheme)}));
  const oldTheme=await old.locator('#themeAutocomplete').evaluate(e=>({count:e.dataset.totalSuggestions,first:[...e.querySelectorAll('[data-autocomplete-theme]')].map(n=>n.dataset.autocompleteTheme)}));
  assert.deepEqual(theme,oldTheme,'THÈME suggestions identical to 053D');

  await page.locator('#modeExact').click();
  await old.locator('#modeExact').click();
  await Promise.all([page,old].map(p=>p.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000})));
  const queries=['elem','element','qu','quat','4','père','monde'];
  const actual={};
  for(const term of queries)actual[term]=await getEntries(page,term);
  const before={};
  for(const term of ['element','qu','4','père','monde']){
    // 053D deliberately suppressed single-digit suggestions. Record that baseline.
    if(term==='4'){before[term]={total:0};continue;}
    before[term]={total:Number(await (async()=>{await old.locator('#query').fill(term);return old.locator('#themeAutocomplete').getAttribute('data-total-suggestions')})())};
  }
  for(const term of ['element','elem']){
    const entries=actual[term].values;
    for(const invalid of ['élément à sa','soi et des éléments','volonté et les éléments','vitamine et élément',
      'éléments pour que','éléments de votre','éléments et tu']){
      assert.ok(!entries.some(s=>norm(s)===norm(invalid)),'Reject non-autonomous fragment '+invalid+' for '+term);
    }
  }
  assert.ok(actual.elem.values.some(s=>norm(s)==='element'),'elem offers élément');
  assert.ok(actual.elem.values.some(s=>norm(s)==='elements'),'elem offers éléments');
  assert.ok(actual.elem.values.some(s=>norm(s)==='elementaires'),'elem offers élémentaires');
  assert.ok(actual.qu.values.some(s=>norm(s)==='quatre elements'),'qu offers attested quatre éléments');
  assert.ok(actual.quat.values.some(s=>norm(s)==='quatre elements'),'quat offers attested quatre éléments');
  assert.ok(actual['4'].values.some(s=>norm(s)==='4 elements'),'4 offers attested 4 éléments despite single-digit query');
  assert.ok(actual['père'].values.some(s=>norm(s)==='pere mere'),'père offers attested Père-Mère');
  assert.ok(actual.monde.values.some(s=>norm(s)==='monde de l homme'),'monde offers attested monde de l’homme');
  const apostrophe=actual.monde.values.find(s=>norm(s)==='monde de l homme');
  assert.ok(/[’']/.test(apostrophe),'Apostrophe from corpus preserved');

  // Compare unchanged result engine on the same corpus and same option readiness.
  const psalmChecks={};
  for(const [mode,query] of [['exact','élément'],['exact','monde'],['exact','père'],['themes','sainte assemblée']]){
    const older=await results(old,mode,query);
    const current=await results(page,mode,query);
    assert.deepEqual(current,older,mode+' results unchanged: '+query);
    psalmChecks[mode+' '+query]=current.length;
  }
  console.log('BIBLAW-053E REAL MOBILE PASS '+JSON.stringify({
    head:url,before,after:Object.fromEntries(Object.entries(actual).map(([k,v])=>[k,v.total])),
    accepted:{
      elem:actual.elem.values.filter(s=>['element','elements','elementaires'].includes(norm(s))).slice(0,4),
      qu:actual.qu.values.filter(s=>norm(s)==='quatre elements'),
      four:actual['4'].values.filter(s=>norm(s)==='4 elements'),
      pere:actual['père'].values.filter(s=>norm(s)==='pere mere'),
      monde:actual.monde.values.filter(s=>norm(s)==='monde de l homme')
    },
    rejected:['élément à sa','soi et des éléments','volonté et les éléments','vitamine et élément'],
    themeUnchanged:theme.count,psalmChecks
  }));
}finally{await browser.close();}
