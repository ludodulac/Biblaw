import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const browser=await chromium.launch({headless:true});
const url=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const sizes=[{width:1280,height:840,mobile:false},{width:390,height:844,mobile:true},{width:320,height:760,mobile:true}];
const approx=(a,b,tolerance=12)=>assert.ok(Math.abs(a-b)<=tolerance,'position changed '+a+' -> '+b);
const scrollInfo=page=>page.locator('#recordDialog').evaluate(el=>({top:el.scrollTop,height:el.scrollHeight,client:el.clientHeight,wide:el.scrollWidth>el.clientWidth+2}));
async function load(page){
  await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('1158 psaumes'),null,{timeout:90000});
}
async function browse(page,kind){
  if(!(await page.locator('#secondaryTools').evaluate(el=>el.open))){
    await page.locator('#secondaryTools summary').click();
  }
  await page.locator('[data-browse-type="'+kind+'"]').click();
  assert.equal(await page.locator('#textBrowser').getAttribute('data-record-type'),kind);
}
async function showRecord(page,id){
  const entry=page.locator('[data-browse-record="'+id+'"]');
  for(let i=0;i<30&&await entry.count()===0;i++){
    const more=page.locator('#browseMore');
    if(!(await more.isVisible()))break;
    await more.click();
  }
  assert.equal(await entry.count(),1,'Found catalogue entry '+id);
  await entry.click();
  assert.ok(await page.locator('#recordDialog').isVisible(),'opened '+id);
}
try{
  for(const view of sizes){
    const page=await browser.newPage({viewport:{width:view.width,height:view.height},isMobile:view.mobile,hasTouch:view.mobile});
    page.setDefaultTimeout(60000);
    const errors=[],privateNotes=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(r.url().includes('/data/notes/'))privateNotes.push(r.url());});
    await load(page);
    const fixture=await page.evaluate(async()=>{
      const res=await fetch('data/browser-search-catalog.json');
      if(!res.ok)throw Error('No published search catalog');
      const records=(await res.json()).records;
      const byId=new Map(records.map(r=>[r.id,r]));
      const multi=records.find(r=>r.recordType==='psalm'&&r.prayerIds?.length>=2&&
        r.prayerIds.filter(id=>byId.get(id)?.recordType==='master-prayer'&&byId.get(id).appliesToPsalmId===r.id).length>=2);
      const long=records.filter(r=>r.recordType==='psalm'&&(r.verses||[]).length>20)
        .sort((a,b)=>b.verses.length-a.verses.length)[0];
      return {psalms:records.filter(r=>r.recordType==='psalm').length,
        prayers:records.filter(r=>r.recordType==='master-prayer').length,
        notes:records.filter(r=>r.recordType==='note').length,
        multi:multi?{id:multi.id,number:multi.number,prayers:multi.prayerIds.filter(id=>byId.has(id))}:null,
        long:long?{id:long.id,count:long.verses.length,number:long.number,verse:long.verses[0].text}:null,
        pr36Length:byId.get('ouriel-book-24-prayer-036')?.text?.length};
    });
    assert.deepEqual([fixture.psalms,fixture.prayers,fixture.notes,fixture.pr36Length],[1158,677,11,1968]);
    assert.ok(fixture.multi||fixture.psalms===1158,'Real catalog has no reciprocal multiple-prayer Psalm; synthetic case will exercise it');
    assert.ok(fixture.long,'Need a long source Psalm');
    // Search -> result -> Psalm -> attached prayer -> Psalm -> original results.
    await page.locator('#modeExact').click();
    await page.locator('#query').fill('105');
    await page.locator('#searchButton').click();
    const openButton=page.locator('#results [data-open="book-17-psalm-105"]');
    await page.waitForFunction(()=>document.querySelector('#results [data-open="book-17-psalm-105"]')!==null);
    const card=openButton.locator('xpath=ancestor::article');
    await card.locator('[data-toggle-result]').click();
    await openButton.scrollIntoViewIfNeeded();
    const beforeY=await page.evaluate(()=>window.scrollY);
    const count=await page.locator('#results .result-card').count();
    await openButton.click();
    assert.ok(await page.locator('#recordDialog').isVisible());
    assert.ok(await page.locator('#browseBack').isVisible());
    assert.ok((await page.locator('#browseBack').textContent()).includes('Retour aux résultats'));
    assert.equal(await page.locator('#dialogContent [data-verified-note]').count(),1,'Only authorized Psalm 105 note');
    assert.equal(await page.locator('#dialogContent [data-note-auth="not-human"]').count(),0);
    const prayerButtons=page.locator('#dialogContent .reader-related-prayers [data-read-related]');
    assert.ok(await prayerButtons.count()>=1,'Prayer reachable without selecting prayer search filter');
    const firstPrayer=await prayerButtons.first().getAttribute('data-read-related');
    await prayerButtons.first().scrollIntoViewIfNeeded();
    const psalmScroll=(await scrollInfo(page)).top;
    await prayerButtons.first().click();
    assert.ok(await page.locator('#readerBack').isVisible(),'Prayer has return to Psalm');
    assert.ok((await page.locator('#dialogEyebrow').textContent()).includes('du psaume 105'));
    assert.equal(await page.locator('#dialogContent .reader-source [data-read-related="book-17-psalm-105"]').count(),1,'Prayer explicitly shows source Psalm');
    assert.ok((await page.locator('#dialogContent').textContent()).length>100,'Prayer body displayed');
    await page.locator('#readerBack').click();
    assert.equal(await page.locator('#dialogContent .reader-related-prayers [data-read-related="'+firstPrayer+'"]').count(),1,'Returned to same Psalm');
    approx((await scrollInfo(page)).top,psalmScroll,30);
    await page.locator('#browseBack').click();
    await page.waitForFunction(()=>!document.querySelector('#recordDialog').open);
    assert.equal(await page.locator('#query').inputValue(),'105','Search query retained');
    assert.equal(await page.locator('#results .result-card').count(),count,'Results retained');
    approx(await page.evaluate(()=>window.scrollY),beforeY,25);
    assert.equal(await openButton.evaluate(el=>el===document.activeElement),true,'Result trigger receives focus again');

    // Confirm the ten public legacy notes remain labelled, including on 320px.
    await browse(page,'note');
    await showRecord(page,'book-17-psalm-109-note-001');
    assert.equal(await page.locator('[data-note-auth="not-human"]').count(),1);
    assert.ok((await page.locator('#dialogContent').textContent()).includes('sans authentification humaine'));
    assert.equal((await scrollInfo(page)).wide,false,'No horizontal note overflow');
    await page.locator('#browseBack').click();
    await showRecord(page,'book-17-psalm-105-note-001');
    assert.equal(await page.locator('[data-note-auth="human"]').count(),1);
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="note"]').click();

    // All multiple prayers remain accessible from their original Psalm.
    await browse(page,'psalm');
    await showRecord(page,fixture.multi?.id||'book-17-psalm-105');
    const buttons=page.locator('#dialogContent .reader-related-prayers [data-read-related]');
    const actualIds=await buttons.evaluateAll(rows=>rows.map(el=>el.dataset.readRelated));
    assert.deepEqual(actualIds,fixture.multi?.prayers||['michael-book-17-prayer-001'],'All real linked prayers, no ID overwritten');
    for(const id of actualIds){
      await page.locator('[data-read-related="'+id+'"]').first().click();
      assert.ok(await page.locator('#dialogContent .prayer-block').count()>=1,'Full prayer view '+id);
      assert.ok((await page.locator('#dialogEyebrow').textContent()).includes('du psaume'),'Prayer origin '+id);
      await page.locator('#readerBack').click();
      assert.equal(await page.locator('#dialogContent [data-read-related="'+id+'"]').count(),1,'Return to multi-prayer Psalm');
    }
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="psalm"]').click();

    // Special prayer 24/36; verify full body and source round trip.
    await browse(page,'prayer');
    await showRecord(page,'ouriel-book-24-prayer-036');
    assert.ok((await page.locator('#dialogContent').textContent()).includes('Ô Père de la terre de Lumière'));
    assert.equal(await page.locator('[data-read-related="book-24-psalm-141"]').count(),1);
    await page.locator('[data-read-related="book-24-psalm-141"]').click();
    assert.ok((await page.locator('#dialogContent .verse').count())>0);
    assert.equal(await page.locator('[data-read-related="ouriel-book-24-prayer-036"]').count(),1);
    await page.locator('#readerBack').click();
    assert.ok((await page.locator('#dialogContent').textContent()).includes('Ô Père de la terre de Lumière'));
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="prayer"]').click();

    // Long Psalm and responsive layout: real scroll and source typography.
    await browse(page,'psalm');
    await showRecord(page,fixture.long.id);
    assert.equal(await page.locator('#dialogContent .verse').count(),fixture.long.count);
    assert.equal(await page.locator('#dialogContent .verse').first().locator('.verse-number').textContent(),'1');
    assert.equal(await page.locator('#dialogContent .verse').first().locator('div').last().evaluate(e=>getComputedStyle(e).whiteSpace),'pre-wrap');
    const dimensions=await scrollInfo(page);
    assert.ok(dimensions.height>dimensions.client,'Long Psalm actually scrolls');
    assert.equal(dimensions.wide,false,'No horizontal overflow on long Psalm');
    await page.locator('#recordDialog').evaluate(el=>el.scrollTop=el.scrollHeight);
    assert.ok((await scrollInfo(page)).top>0);
    assert.ok(await page.locator('#browseBack').isVisible(),'Return works after long scroll');
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="psalm"]').click();

    if(!view.mobile){
      // True keyboard activation, then keyboard return, Escape and focus restoration.
      const trigger=page.locator('#results [data-open="book-17-psalm-105"]');
      await trigger.focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#recordDialog').isVisible());
      const linked=page.locator('#dialogContent .reader-related-prayers [data-read-related]').first();
      await linked.focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#readerBack').isVisible());
      await page.locator('#readerBack').focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#dialogContent .verse').count()>0);
      await page.keyboard.press('Escape');
      await page.waitForFunction(()=>!document.querySelector('#recordDialog').open);
      assert.equal(await trigger.evaluate(el=>el===document.activeElement),true);
    }

    assert.deepEqual(privateNotes,[],'No internal notes fetched');
    assert.deepEqual(errors,[],'No JS runtime errors');
    console.log('BIBLAW-070 CHROMIUM PASS '+JSON.stringify({viewport:view.width,searchBack:true,realPrayers:actualIds.length,
      longPsalm:fixture.long.count,pr36:true,notes:true,keyboard:!view.mobile}));
    await page.close();
  }

  // There is no real Psalm with two reciprocal prayers in the present 677-prayer bundle.
  // Verify multiple prayers with browser-only response interception; NEVER commit test data.
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await page.route('**/data/browser-search-catalog.json',async route=>{
    const response=await route.fetch();
    const bundle=await response.json();
    const ps=bundle.records.find(r=>r.id==='book-17-psalm-105');
    const original=bundle.records.find(r=>r.id==='michael-book-17-prayer-001');
    assert.ok(ps&&original,'Actual 17/105 fixtures must exist');
    const duplicate={...original,id:'browser-only-second-prayer-070',number:999,
      text:'Essai browser-only de plusieurs prières indépendantes.',appliesToPsalmId:ps.id};
    ps.prayerIds.push(duplicate.id);
    bundle.records.push(duplicate);
    bundle.recordCount=bundle.records.length;
    await route.fulfill({response,body:JSON.stringify(bundle),contentType:'application/json'});
  });
  await load(page);
  await browse(page,'psalm');
  await showRecord(page,'book-17-psalm-105');
  const ids=await page.locator('.reader-related-prayers [data-read-related]').evaluateAll(a=>a.map(e=>e.dataset.readRelated));
  assert.deepEqual(ids,['michael-book-17-prayer-001','browser-only-second-prayer-070'],'Two distinct reciprocal prayer IDs');
  for(const id of ids){
    await page.locator('.reader-related-prayers [data-read-related="'+id+'"]').click();
    assert.ok(await page.locator('#dialogContent .prayer-block').count()>0,'Independent prayer '+id);
    await page.locator('#readerBack').click();
    assert.equal(await page.locator('.reader-related-prayers [data-read-related]').count(),2,'Both links retained after return');
  }
  console.log('BIBLAW-070 MULTI-PRAYER FIXTURE PASS (browser-only; no real multi-prayer pair in current bundle)');
  await page.close();
} finally {
  await browser.close();
}
