import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const browser = await chromium.launch({headless:true});
const sizes=[{width:1280,height:840,mobile:false},{width:390,height:844,mobile:true},{width:320,height:760,mobile:true}];

async function showRecord(page,id){
  for(let i=0;i<30 && await page.locator('[data-browse-record="'+id+'"]').count()===0;i++){
    const more=page.locator('#browseMore');
    if(!(await more.isVisible()))break;
    await more.click();
  }
  const row=page.locator('[data-browse-record="'+id+'"]');
  assert.equal(await row.count(),1,'Unique published browser row: '+id);
  await row.click();
  assert.ok(await page.locator('#recordDialog').isVisible(),'Record opens: '+id);
}
try{
  for(const view of sizes){
    const page=await browser.newPage({viewport:{width:view.width,height:view.height},
      isMobile:view.mobile,hasTouch:view.mobile});
    page.setDefaultTimeout(60000);
    const errors=[], unpublishedRequests=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(/\/data\/notes\//.test(r.url()))unpublishedRequests.push(r.url());});
    await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('1158 psaumes'),
      null,{timeout:90000});
    const stats=await page.evaluate(async()=>{
      const response=await fetch('data/browser-search-catalog.json');
      assert(response.ok);
      const source=(await response.json()).records;
      return {psalms:source.filter(x=>x.recordType==='psalm').length,
        prayers:source.filter(x=>x.recordType==='master-prayer').length,
        notes:source.filter(x=>x.recordType==='note').length,
        humanNotes:source.filter(x=>x.recordType==='note'&&x.validation?.status==='validated').length,
        pr36:source.find(x=>x.id==='ouriel-book-24-prayer-036')?.text?.length};
    });
    assert.deepEqual(stats,{psalms:1158,prayers:677,notes:11,humanNotes:1,pr36:1968},
      'No new note published, all prayers indexed');

    await page.locator('#secondaryTools summary').click();
    await page.locator('[data-browse-type="prayer"]').click();
    assert.equal(await page.locator('#textBrowser').getAttribute('data-total-records'),'677');
    await showRecord(page,'ouriel-book-24-prayer-036');
    assert.ok((await page.locator('#dialogContent').textContent()).includes('Ô Père de la terre de Lumière'),
      'Pr36 source body is fully reachable');
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="prayer"]').click();

    await page.locator('[data-browse-type="psalm"]').click();
    await showRecord(page,'book-17-psalm-105');
    assert.equal(await page.locator('[data-verified-note]').count(),1,
      'Only previously published human-authenticated note is attached');
    assert.equal(await page.locator('[data-verified-note]').first().getAttribute('data-verified-note'),
      'book-17-psalm-105-note-001');
    assert.equal(await page.locator('#dialogContent .verse').count(),19,
      'All original verses retained');
    assert.equal(await page.locator('#dialogContent .prayer-block').count(),0,
      'Browse does not append a prayer implicitly');
    await page.locator('#browseBack').click();
    await showRecord(page,'book-17-psalm-109');
    assert.equal(await page.locator('[data-verified-note]').count(),0,
      'Machine-validated note is not promoted to authenticated contextual display');
    await page.locator('#browseBack').click();
    await page.locator('#browseClose').click();

    await page.locator('#modeExact').click();
    await page.locator('#query').fill('lumière');
    await page.locator('#searchButton').click();
    await page.locator('#results .result-card').first().waitFor();
    assert.ok(await page.locator('#results .result-card').count()>0,'Word search returns passages');
    await page.locator('#results .result-summary-toggle').first().click();
    await page.locator('#results [data-open]').first().click();
    assert.ok(await page.locator('#recordDialog').isVisible(),'Word result opens');
    await page.locator('#closeDialog').click();
    await page.locator('#modeThemes').click();
    await page.locator('#query').fill('sainte assemblée');
    await page.locator('#searchButton').click();
    await page.locator('#results .result-card').first().waitFor();
    assert.ok(await page.locator('#results .result-card').count()>0,'Theme search returns passages');
    assert.deepEqual(errors,[],'No JavaScript exceptions');
    assert.deepEqual(unpublishedRequests,[],'No internal note files are fetched');
    console.log('BIBLAW-068 BROWSER PASS '+JSON.stringify({viewport:view.width,stats,
      searched:['lumière','sainte assemblée'],pr36:true,authenticatedNote:true}));
    await page.close();
  }
} finally {
  await browser.close();
}
