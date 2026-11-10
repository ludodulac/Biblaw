#!/usr/bin/env node
// M3 browser regression: initial transfer, lazy search, FAQ, notes and retries.
// Run against the local Pages output; it must never deploy the site.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const heavy=/\/data\/(?:browser-search-catalog\.json|thematic-index\/theme-directory-public\.json|thematic-index\/theme-search-runtime\.json|lexical-expansion-runtime\.json)/;
const browser=await chromium.launch({headless:true});

try {
  for(const width of [390,1366]){
    const page=await browser.newPage({viewport:{width,height:844},acceptDownloads:true});
    const errors=[],requests=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(heavy.test(r.url()))requests.push(new URL(r.url()).pathname);});
    try {
      await page.goto(base,{waitUntil:'networkidle'});
      assert.deepEqual(requests,[],'Heavy files fetched without a user request');
      assert.match(await page.locator('#corpusStats').innerText(),/première recherche/);

      await page.locator('#faqToggle').click();
      await page.locator('#faqTopicButtons button').first().waitFor({timeout:8000});
      assert.equal(await page.locator('#faqTopicButtons button').count(),11);
      await page.getByRole('button',{name:/La souffrance/}).click();
      assert.equal(await page.locator('#faqList .faq-question-item').count(),4);
      await page.locator('#faqList .faq-question-item').first().click();
      await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
      assert.deepEqual(requests,[],'Reading FAQ answers fetched the search corpus');
      await page.locator('#faqClose').click();

      const start=Date.now();
      await page.locator('#query').fill('psaume 105');
      await page.locator('#searchButton').click();
      await page.waitForFunction(
        ()=>document.getElementById('corpusStats').textContent.includes('1158 psaumes'),
        null,{timeout:60000}
      );
      await page.locator('#results [data-open]').first().waitFor({timeout:15000});
      const elapsed=Date.now()-start;
      for(const file of ['browser-search-catalog.json','theme-directory-public.json','theme-search-runtime.json','lexical-expansion-runtime.json']){
        assert.equal(requests.filter(p=>p.endsWith('/'+file)).length,1,'Unexpected duplicate load: '+file);
      }
      await page.locator('#results [data-open]').first().click();
      await page.locator('#recordDialog').waitFor({state:'visible'});
      assert.ok(await page.locator('#dialogContent .verse').count()>0,'Psalm reader empty');
      const filePromise=page.waitForEvent('download');
      await page.locator('#downloadRecord').click();
      const pdf=await filePromise;
      assert.match(pdf.suggestedFilename(),/\.pdf$/);
      await page.locator('#closeDialog').click();

      // The index and notes reuse the corpus that the search already loaded.
      await page.locator('#indexToggle').click();
      await page.locator('#themeDirectory .theme-row').first().waitFor({timeout:15000});
      await page.locator('#closeIndex').click();
      await page.locator('#notesLibraryToggle').click();
      await page.locator('#notesThemeList .notes-theme-item').first().waitFor({timeout:15000});
      await page.locator('#notesLibraryClose').click();
      assert.equal(requests.filter(p=>p.endsWith('/browser-search-catalog.json')).length,1);
      assert.equal(requests.filter(p=>p.endsWith('/theme-directory-public.json')).length,1,
        'Validated relations must not download the 10 MB directory twice');
      assert.deepEqual(errors,[]);
      console.log('BIBLAW M3 '+width+'px PASS: 0 large startup requests; on-demand search ready in '+elapsed+
        'ms; 1 fetch each large file, FAQ/notes/theme index/PDF/reader verified.');
    }finally{await page.close();}
  }

  // Failed first fetch must allow retry without refreshing the page.
  const page=await browser.newPage({viewport:{width:390,height:844}});
  let attempts=0;
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route(/\/data\/browser-search-catalog\.json/,route=>{
    attempts++;
    if(attempts===1)return route.abort('failed');
    return route.continue();
  });
  try {
    await page.goto(base,{waitUntil:'networkidle'});
    // Typing alone starts the first request. Verify its visible failure
    // before attempting the next search, avoiding a retry race in the test.
    await page.locator('#query').fill('psaume 105');
    await page.getByText(/Vérifiez votre connexion et réessayez/).waitFor({timeout:30000});
    await page.locator('#query').fill('psaume 106');
    await page.locator('#searchButton').click();
    await page.waitForFunction(
      ()=>document.getElementById('corpusStats').textContent.includes('1158 psaumes'),
      null,{timeout:60000}
    );
    await page.locator('#results [data-open]').first().waitFor({timeout:15000});
    assert.equal(attempts,2,'Search corpus retry did not work');
    assert.deepEqual(errors,[]);
    console.log('BIBLAW M3 RETRY PASS: failed first transfer, explicit error, successful second request');
  }finally{await page.close();}
}finally{await browser.close();}
