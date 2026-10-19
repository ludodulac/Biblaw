import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL;
const baseline='https://rawcdn.githack.com/ludodulac/Biblaw/c97acd8f1cf5d822dbf9f2aac04744bc26f7ff98/index.html';
if(!url)throw Error('BIBLAW_SMOKE_URL is required');
const norm=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'')
  .toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ')
  .replace(/[-‐‑‒–]/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const browser=await chromium.launch({headless:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function open(address,width=390){
  const page=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  const response=await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
  assert.equal(response?.status(),200,'Public preview reachable');
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  await page.locator('#modeExact').click();
  await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  return {page,errors};
}
async function rows(page,query,full=true){
  await page.locator('#query').fill(query);
  const box=page.locator('#themeAutocomplete');
  const total=await box.isVisible()?Number(await box.getAttribute('data-total-suggestions')||0):0;
  const found=new Map();
  const positions=full?Array.from({length:Math.ceil(total/11)},(_,i)=>i*11):[0];
  for(const i of positions){
    await box.evaluate((e,n)=>e.scrollTop=Math.max(0,32+(n-3)*64),i);
    await sleep(12);
    for(const row of await box.locator('[data-autocomplete-word]').evaluateAll(nodes=>
      nodes.map(n=>({i:Number(n.dataset.suggestionIndex),label:n.dataset.autocompleteWord}))))
      found.set(row.i,row);
  }
  assert.ok(await box.locator('[data-autocomplete-word]').count()<=18,'Bounded virtualized dropdown');
  return {total,values:[...found.values()].sort((a,b)=>a.i-b.i)};
}
async function ids(page,text){
  await page.locator('#modeExact').click();
  await page.locator('#query').fill(text);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}
try{
  const {page,errors}=await open(url);
  const checks=['4','qu','qua','quatre','40','quarante','12','dou','douze',
    '21','vingt et un','80','quatre-vingts','100','cent',
    '144','cent quarante-quatre','200','deux cents'];
  const data={};
  for(const q of checks){
    data[q]=await rows(page,q);
    console.log('053I_QUERY '+JSON.stringify({query:q,total:data[q].total,
      sample:data[q].values.slice(0,16).map(r=>r.label)}));
  }
  const has=(q,label)=>data[q].values.some(r=>norm(r.label)===norm(label));
  for(const q of ['4','qu','qua','quatre'])
    assert.ok(has(q,'4 éléments'),'Literal 4 éléments must be offered for '+q);
  assert.ok(has('4','quatre'),'Digit query finds corpus-attested spelled numeral quatre');
  assert.ok(data['4'].values.some(r=>r.label==='4'),'Digit-only original spelling is displayed');
  assert.ok(!data['4'].values.some(r=>/^40(?:\s|$)|^quarante(?:\s|$)|^quatre[- ‐‑‒–]vingt/iu.test(r.label)),
    'Numeric 4 does not match 40 or 80');
  assert.ok(!data['40'].values.some(r=>/^4(?:\s|$)|^quatre(?:\s|$)/iu.test(r.label)),
    'Numeric 40 does not match 4');

  // Verify complete source attestations BEFORE requiring any optional form.
  const source=await page.evaluate(async()=>{
    const catalog=await (await fetch('data/browser-search-catalog.json')).json();
    return (catalog.records||[]).flatMap(r=>r.recordType==='psalm'?
      [r.title,...(r.verses||[]).map(v=>v.text)]:[r.title,r.text,r.summary])
      .filter(Boolean).map(t=>String(t).normalize('NFD').replace(/[\u0300-\u036f]/g,'')
        .toLowerCase().replace(/[’']/g,' ').replace(/[-‐‑‒–]/g,' ')
        .replace(/\s+/g,' '));
  });
  const sourceContains=label=>source.some(fragment=>fragment.includes(
    String(label).normalize('NFD').replace(/[\u0300-\u036f]/g,'')
      .toLowerCase().replace(/[’']/g,' ').replace(/[-‐‑‒–]/g,' ')
      .replace(/\s+/g,' ')));
  const pairs=[['12','douze'],['21','vingt et un'],['80','quatre-vingts'],
    ['100','cent'],['144','cent quarante-quatre'],['200','deux cents']];
  for(const [digit,spoken] of pairs){
    const attested=sourceContains(spoken);
    if(attested)assert.ok(data[digit].values.some(r=>norm(r.label)===norm(spoken)),
      'Original attested written numeral must be suggested for '+digit+' : '+spoken);
    // No pair is synthesized when a written spelling is absent.
    if(!attested)assert.ok(!data[digit].values.some(r=>norm(r.label)===norm(spoken)),
      'Never invent unattested '+spoken);
    const literal=data[digit].values.filter(r=>new RegExp('^'+digit+'(?:\\s|$)').test(r.label));
    for(const entry of literal)
      assert.ok(data[spoken].values.some(r=>r.label===entry.label),
        'Digit entry matches spelled-out query '+digit+' : '+entry.label);
    console.log('053I_CORPUS_PAIR '+JSON.stringify({digit,spoken,attested,
      originalWritten:attested&&has(digit,spoken),sourceDigitLabels:literal.map(r=>r.label)}));
  }
  for(const label of ['4 éléments','quatre']){
    assert.ok(sourceContains(label),'Displayed numeral form attested literally: '+label);
  }
  // A match retains the *original* source spelling when clicked.
  const orig=await open(baseline);
  const choice=data['4'].values.find(r=>r.label==='quatre');
  await page.locator('#query').fill('4');
  await page.locator('#themeAutocomplete').evaluate((e,i)=>e.scrollTop=Math.max(0,32+(i-3)*64),choice.i);
  await sleep(50);
  const clicked=page.locator('#themeAutocomplete [data-autocomplete-word="quatre"]').first();
  assert.ok(await clicked.count(),'Original word choice reachable on mobile');
  await clicked.evaluate(button=>button.click());
  assert.equal(await page.locator('#query').inputValue(),'quatre','Label is not converted to digit');
  assert.deepEqual(await page.locator('.result-card [data-open]').evaluateAll(
    nodes=>nodes.map(n=>n.dataset.open).sort()),await ids(orig.page,'quatre'),
    'Selecting original text uses unchanged psalm search');
  assert.deepEqual(errors,[],'No browser errors');
  assert.deepEqual(orig.errors,[],'No old browser errors');
  const compact=await open(url,320);
  assert.ok((await rows(compact.page,'4')).values.some(r=>r.label==='quatre'),
    '320px digit-to-letter suggestion');
  console.log('BIBLAW-053I MOBILE PASS '+JSON.stringify({url,checked:checks,
    pairs:pairs.map(([digit,spoken])=>({digit,spoken,attested:sourceContains(spoken)})),
    noNumericConfusion:true,originalLabelSelection:true,mobile:'320px'}));
}finally{await browser.close();}
