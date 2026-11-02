import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
const views=[{width:1280,height:840,mobile:false},{width:390,height:844,mobile:true},{width:320,height:760,mobile:true}];
const originalOrigin=new URL(base).origin;
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[’']/g,' ').replace(/[^a-z0-9\s-]/g,' ').replace(/-/g,' ').replace(/\s+/g,' ').trim();
const byId=records=>new Map(records.map(x=>[x.id,x]));

async function ready(page){
  await page.goto(base,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('1158 psaumes'),null,{timeout:90000});
}
async function toggleOptions(page){
  if(!(await page.locator('#secondaryTools').evaluate(e=>e.open)))await page.locator('#secondaryTools summary').click();
}
async function openSearchResult(page,id){
  const trigger=page.locator('#results [data-open="'+id+'"]');
  await page.waitForFunction(id=>!!document.querySelector('#results [data-open="'+id+'"]'),id);
  const card=trigger.locator('xpath=ancestor::article');
  if(await card.locator('[data-toggle-result]').getAttribute('aria-expanded')!=='true')await card.locator('[data-toggle-result]').click();
  await trigger.scrollIntoViewIfNeeded();
  await trigger.click();
  assert.ok(await page.locator('#recordDialog').isVisible(),'Open search result '+id);
  return trigger;
}
async function openBrowser(page,type,id){
  await toggleOptions(page);
  const panel=page.locator('#textBrowser');
  if(await panel.isVisible()){
    const old=await panel.getAttribute('data-record-type');
    if(old!==type)await page.locator('[data-browse-type="'+type+'"]').click();
  }else await page.locator('[data-browse-type="'+type+'"]').click();
  const entry=page.locator('[data-browse-record="'+id+'"]');
  for(let i=0;i<35&&await entry.count()===0;i++){
    const more=page.locator('#browseMore');
    if(!(await more.isVisible()))break;
    await more.click();
  }
  assert.equal(await entry.count(),1,'Unique browser row '+id);
  await entry.click();
  assert.ok(await page.locator('#recordDialog').isVisible());
  return entry;
}
async function back(page){
  await page.locator('#browseBack').click();
  await page.waitForFunction(()=>!document.querySelector('#recordDialog').open);
}
async function exact(page,q){
  await page.locator('#modeExact').click();
  await page.locator('#query').fill(q);
  await page.locator('#searchButton').click();
}
try{
  for(const view of views){
    const page=await browser.newPage({viewport:{width:view.width,height:view.height},isMobile:view.mobile,hasTouch:view.mobile});
    page.setDefaultTimeout(30000);
    const errors=[],httpErrors=[],privateRequests=[];
    page.on('pageerror',err=>errors.push(err.message));
    page.on('response',resp=>{
      const u=resp.url();
      if(u.startsWith(originalOrigin)&&resp.status()>=400)httpErrors.push({status:resp.status(),url:u});
    });
    page.on('request',req=>{if(req.url().includes('/data/notes/'))privateRequests.push(req.url());});
    await ready(page);
    const records=await page.evaluate(async()=>{
      const resp=await fetch('data/browser-search-catalog.json');
      if(!resp.ok)throw Error('Browser bundle request failed');
      return (await resp.json()).records;
    });
    const map=byId(records);
    assert.equal(records.length,1846);
    assert.deepEqual([
      records.filter(x=>x.recordType==='psalm').length,
      records.filter(x=>x.recordType==='master-prayer').length,
      records.filter(x=>x.recordType==='note').length
    ],[1158,677,11]);
    const noteStatuses=records.filter(x=>x.recordType==='note').map(x=>x.validation?.status);
    assert.equal(noteStatuses.filter(x=>x==='validated').length,1);
    assert.equal(noteStatuses.filter(x=>x!=='validated').length,10);

    // 1. Existing theme search: a returned theme index must point to a canonical Psalm.
    await page.locator('#query').fill('sainte assemblée');
    await page.locator('#searchButton').click();
    await page.locator('#results .result-card').first().waitFor();
    const themeIds=await page.locator('#results [data-open]').evaluateAll(rows=>rows.map(el=>el.dataset.open));
    assert.ok(themeIds.length>0,'Canonical theme yields results');
    for(const id of themeIds)assert.equal(map.get(id)?.recordType,'psalm','Theme points to canonical Psalm');
    assert.ok(await page.locator('#themeEntryIdentity').isVisible(),'Theme identity JS asset loaded');
    await page.locator('#indexToggle').click();
    assert.ok(await page.locator('#indexPanel').isVisible(),'Index opens');
    await page.locator('#closeIndex').click();
    assert.ok(!(await page.locator('#indexPanel').isVisible()),'Index closes');

    // 2. Word search: compare visible results and numeric counts with the public corpus.
    await exact(page,'lumière');
    await toggleOptions(page);
    if(await page.locator('#includeSimplePlurals').isVisible())
      await page.locator('#includeSimplePlurals').uncheck();
    await page.locator('#searchButton').click();
    const expected=records.filter(r=>r.recordType==='psalm'&&
      [r.title,...(r.verses||[]).map(v=>v.text)].some(t=>(' '+norm(t)+' ').includes(' lumiere '))).map(r=>r.id);
    const observed=await page.locator('#results [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
    assert.ok(expected.length>5,'Representative source search');
    assert.deepEqual([...observed].sort(),[...expected].sort(),'Full exact-result ID set matches literal source word');
    assert.ok((await page.locator('#resultCount').textContent()).includes(expected.length+' psaumes'),'Result count matches public source');
    assert.ok(await page.locator('.literal-sense-notice').isVisible(),'Literal-match meaning disclaimer');
    const first=observed[0];
    const markInput=page.locator('#results [data-open="'+first+'"]').locator('xpath=ancestor::article');
    await markInput.locator('[data-toggle-result]').click();
    const excerptMarks=await markInput.locator('.search-hit').allTextContents();
    for(const m of excerptMarks)assert.equal(norm(m),'lumiere','Only searched term highlighted');
    await openSearchResult(page,first);
    const ps=map.get(first);
    assert.equal(await page.locator('#dialogContent .verse').count(),ps.verses.length,'Full source Psalm displayed');
    const marks=await page.locator('#dialogContent .verse .search-hit').allTextContents();
    assert.ok(marks.length>0,'Literal term highlighted in reader');
    for(const m of marks)assert.equal(norm(m),'lumiere');
    const sourceText=await page.locator('#dialogContent .verse').allTextContents();
    assert.ok(sourceText.join(' ').length>100,'Text not cut');
    await back(page);
    assert.equal(await page.locator('#query').inputValue(),'lumière');

    // 3. Sense-sensitive term: explicitly show that a textual highlight is NOT a semantic classification.
    await exact(page,'bien');
    const disclaimer=page.locator('.literal-sense-notice');
    assert.ok(await disclaimer.isVisible());
    assert.ok((await disclaimer.textContent()).includes('ne valide pas leur sens'));
    await page.locator('#results .result-card').first().waitFor();
    assert.ok(await page.locator('#results .result-card').count()>0);
    const bienId=await page.locator('#results [data-open]').first().getAttribute('data-open');
    await openSearchResult(page,bienId);
    const bienMarks=await page.locator('#dialogContent .verse .search-hit').allTextContents();
    assert.ok(bienMarks.length>0);
    for(const t of bienMarks)assert.equal(norm(t),'bien');
    await back(page);
    await exact(page,'biens');
    assert.ok(await disclaimer.isVisible());
    await page.locator('#results .result-card').first().waitFor();
    // "Bien" and "biens" are not presented as semantically classified by highlighting.
    assert.ok((await disclaimer.textContent()).includes('Surlignage des mots uniquement'));

    // 4. Semantic-safety / editorial restrictions across direct browsing.
    const note=await openBrowser(page,'note','book-17-psalm-109-note-001');
    assert.ok(await page.locator('[data-note-auth="not-human"]').isVisible());
    await back(page);
    assert.ok(await note.isVisible(),'Note browser stays open');
    await page.locator('[data-browse-type="note"]').click();

    // 4b. Search source-type filters must change the *actual result set*, not only browser categories.
    await toggleOptions(page);
    await page.locator('input[name="sourceType"][value="psalm"]').uncheck();
    await page.locator('input[name="sourceType"][value="prayer"]').check();
    await exact(page,'lumière');
    const prayerResults=await page.locator('#results [data-open]').evaluateAll(rows=>rows.map(e=>e.dataset.open));
    assert.ok(prayerResults.length>0,'Search with prayer filter finds prayers');
    for(const id of prayerResults)assert.equal(map.get(id)?.recordType,'master-prayer','Prayer filter excludes Psalms');
    await page.locator('input[name="sourceType"][value="prayer"]').uncheck();
    await page.locator('input[name="sourceType"][value="note"]').check();
    await exact(page,'Nom de la Mère');
    const noteResults=await page.locator('#results [data-open]').evaluateAll(rows=>rows.map(e=>e.dataset.open));
    assert.deepEqual(noteResults,['book-17-psalm-109-note-001','book-17-psalm-122-note-001'],'Exact phrase is present in two historical notes');
    await openSearchResult(page,'book-17-psalm-109-note-001');
    assert.equal(await page.locator('[data-note-auth="not-human"]').count(),1);
    await back(page);
    await page.locator('input[name="sourceType"][value="note"]').uncheck();
    await page.locator('input[name="sourceType"][value="psalm"]').check();

    // 5. Search -> original Psalm -> authenticated note -> Psalm -> same results/focus.
    await exact(page,'105');
    const result=page.locator('#results [data-open="book-17-psalm-105"]');
    await page.waitForFunction(()=>!!document.querySelector('#results [data-open="book-17-psalm-105"]'));
    await openSearchResult(page,'book-17-psalm-105');
    assert.equal(await page.locator('[data-verified-note]').count(),1);
    assert.equal(await page.locator('[data-read-related="book-17-psalm-109-note-001"]').count(),0);
    await page.locator('[data-read-related="book-17-psalm-105-note-001"]').click();
    assert.ok(await page.locator('[data-note-auth="human"]').isVisible());
    assert.ok(await page.locator('#readerBack').isVisible());
    await page.locator('#readerBack').click();
    assert.equal(await page.locator('[data-verified-note]').count(),1,'Return to same Psalm after note');
    const prayerId=await page.locator('.reader-related-prayers [data-read-related]').first().getAttribute('data-read-related');
    await page.locator('.reader-related-prayers [data-read-related="'+prayerId+'"]').click();
    assert.ok(await page.locator('#dialogContent .prayer-block').count()>0);
    assert.ok((await page.locator('#dialogEyebrow').textContent()).includes('du psaume 105'));
    await page.locator('#readerBack').click();
    assert.equal(await page.locator('#dialogContent .verse').count(),map.get('book-17-psalm-105').verses.length);
    await back(page);
    assert.equal(await page.locator('#query').inputValue(),'105');
    assert.equal(await result.evaluate(el=>el===document.activeElement),true);

    // 6. Filter by archange on numeric Psalm query; direct prayer 24/36.
    await toggleOptions(page);
    await page.locator('#archangelFilter').selectOption('michael');
    await page.locator('#searchButton').click();
    const michael=await page.locator('#results [data-open]').evaluateAll(n=>n.map(x=>x.dataset.open));
    assert.ok(michael.length>0);
    for(const id of michael)assert.equal(map.get(id)?.archangel,'michael','Archangel filter');
    await page.locator('#archangelFilter').selectOption('gabriel');
    await page.locator('#searchButton').click();
    const gabriel=await page.locator('#results [data-open]').evaluateAll(n=>n.map(x=>x.dataset.open));
    for(const id of gabriel)assert.equal(map.get(id)?.archangel,'gabriel');
    await page.locator('#archangelFilter').selectOption('');

    const pr=await openBrowser(page,'prayer','ouriel-book-24-prayer-036');
    assert.ok((await page.locator('#dialogContent').textContent()).includes('Ô Père de la terre de Lumière'));
    assert.equal(map.get('ouriel-book-24-prayer-036').text.length,1968);
    await page.locator('[data-read-related="book-24-psalm-141"]').click();
    assert.ok(await page.locator('#dialogContent .verse').count()>0);
    await page.locator('#readerBack').click();
    assert.ok((await page.locator('#dialogContent').textContent()).includes('Ô Père de la terre de Lumière'));
    await back(page);
    assert.ok(await pr.isVisible(),'Direct prayer browser list retained');
    await page.locator('[data-browse-type="prayer"]').click();

    // 7. Long reading, keyboard/escape and mobile width without overlap.
    const long=records.filter(r=>r.recordType==='psalm').sort((a,b)=>(b.verses?.length||0)-(a.verses?.length||0))[0];
    await openBrowser(page,'psalm',long.id);
    assert.equal(await page.locator('#dialogContent .verse').count(),long.verses.length);
    const scroll=await page.locator('#recordDialog').evaluate(el=>({height:el.scrollHeight,client:el.clientHeight,width:el.scrollWidth,bodyWidth:el.clientWidth}));
    assert.ok(scroll.height>scroll.client,'Long reader is scrollable');
    assert.ok(scroll.width<=scroll.bodyWidth+2,'No horizontal reader overflow');
    await page.locator('#recordDialog').evaluate(el=>el.scrollTop=el.scrollHeight);
    assert.ok((await page.locator('#recordDialog').evaluate(el=>el.scrollTop))>0);
    await back(page);
    await page.locator('[data-browse-type="psalm"]').click();

    if(!view.mobile){
      // Actual keyboard interaction: Enter opens, Escape closes, focus restored.
      await exact(page,'105');
      const button=page.locator('#results [data-open="book-17-psalm-105"]');
      const card=button.locator('xpath=ancestor::article');
      await card.locator('[data-toggle-result]').click();
      await button.focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#recordDialog').isVisible());
      await page.locator('[data-read-related="book-17-psalm-105-note-001"]').focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('[data-note-auth="human"]').isVisible());
      await page.locator('#readerBack').focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#dialogContent .verse').count()>0);
      await page.keyboard.press('Escape');
      await page.waitForFunction(()=>!document.querySelector('#recordDialog').open);
      assert.equal(await button.evaluate(el=>document.activeElement===el),true);
    }

    assert.deepEqual(errors,[],'Browser runtime errors');
    assert.deepEqual(httpErrors,[],'All first-party CSS/JS/JSON assets reachable in preview');
    assert.deepEqual(privateRequests,[],'No private historical notes requested');
    console.log('BIBLAW-071 USER-PATH PASS '+JSON.stringify({width:view.width,themeResults:themeIds.length,literalResults:expected.length,pr36:true,
       noteRoundTrip:true,keyboard:view.mobile?'not attempted':'PASS',noMissingAssets:true}));
    await page.close();
  }
} finally {
  await browser.close();
}
