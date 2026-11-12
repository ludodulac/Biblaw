#!/usr/bin/env node
// Actual mobile and desktop searches, from query to canonical Psalm reader.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
try{
  for(const width of [390,1366]){
    const page=await browser.newPage({viewport:{width,height:844},acceptDownloads:true});
    const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    try{
      await page.goto(base,{waitUntil:'domcontentloaded'});
      await page.locator('#query').fill('conte');
      await page.locator('#searchButton').click();
      await page.locator('#results .related-discovery').waitFor({timeout:60000});
      assert.match(await page.locator('.related-discovery').innerText(),/Thèmes associés à « conte »/);
      assert.equal(await page.locator('.related-discovery [data-related-theme]').count(),5);
      const ids=await page.locator('.related-discovery [data-related-theme]')
        .evaluateAll(ns=>ns.map(n=>n.dataset.relatedTheme));
      assert.deepEqual(ids,['blanche-neige','fees','haricot-magique','baguette-magique','licorne']);
      assert.ok(await page.locator('#results .result-card').count()>0,
        'The word conte should open actual Psalms indexed under related canonical themes');
      await page.locator('.related-discovery [data-related-theme="blanche-neige"]').click();
      assert.equal(await page.locator('#query').inputValue(),'Blanche-Neige');
      assert.ok(await page.locator('#results .result-card').count()>0);
      await page.locator('#results [data-open]').first().click();
      await page.locator('#recordDialog').waitFor({state:'visible'});
      assert.ok(await page.locator('#dialogContent .verse').count()>0);
      const downloaded=page.waitForEvent('download');
      await page.locator('#downloadRecord').click();
      assert.match((await downloaded).suggestedFilename(),/\.pdf$/);
      await page.locator('#closeDialog').click();

      for(const term of ['contes','contes de fées','légendes','merveilleux']){
        await page.locator('#query').fill(term);
        await page.locator('#searchButton').click();
        await page.locator('#results .related-discovery').waitFor();
        assert.ok(await page.locator('#results .result-card').count()>0,
          'Related search lacks canonical results: '+term);
      }
      await page.locator('#query').fill('conte');
      await page.locator('#searchButton').click();
      await page.locator('.related-discovery [data-show-text-search]').waitFor();
      await page.locator('.related-discovery [data-show-text-search]').click();
      assert.equal(await page.locator('#modeExact').evaluate(e=>e.classList.contains('active')),true,
        'Literal occurrences must remain a separate user-selected search');
      assert.equal(await page.locator('#results .related-discovery').count(),0);
      await page.locator('#modeThemes').click();
      await page.locator('#query').fill('argent');
      await page.locator('#searchButton').click();
      assert.equal(await page.locator('#results .related-discovery').count(),0,
        'Exact canonical themes must take precedence over thematic suggestions');
      await page.locator('#query').fill('assemblée');
      await page.locator('#searchButton').click();
      assert.equal(await page.locator('#results .related-discovery').count(),0,
        'The previously-prohibited assemblée to sainte assemblée leap must remain prohibited');
      assert.deepEqual(errors,[]);
      console.log('SEMANTIC_BROWSER_'+width+'_PASS: conte/contes/fées/légendes/merveilleux -> canonical Psalms, '+
        'clickable theme and reader, PDF, literal search separated, strict themes unchanged');
    }finally{await page.close();}
  }
}finally{await browser.close();}
