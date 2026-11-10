#!/usr/bin/env node
// M1: The FAQ must work on desktop and mobile while the two heavy search
// indexes are artificially held back. No published deployment is involved.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
try{
  for(const viewport of [{width:390,height:844},{width:1366,height:768}]){
    const page=await browser.newPage({viewport,acceptDownloads:true});
    const pending=[],faqRequests=[],errors=[];
    let releaseCorpus=false,signalRequest;
    const catalogRequested=new Promise(resolve=>{signalRequest=resolve;});
    page.on('pageerror',error=>errors.push(error.message));
    page.on('request',request=>{
      if(/\/data\/faq-[\w-]+\.json/.test(request.url()))faqRequests.push(request.url());
    });
    await page.route(/\/(browser-search-catalog|theme-directory-public)\.json/,async route=>{
      signalRequest();
      if(!releaseCorpus)await new Promise(resolve=>pending.push(resolve));
      await route.continue();
    });
    try{
      await page.goto(base,{waitUntil:'domcontentloaded'});
      const start=Date.now();
      await page.locator('#faqToggle').click();
      await page.locator('#faqTopicButtons .faq-topic-button').first().waitFor({timeout:8000});
      const elapsed=Date.now()-start;
      assert.equal(await page.locator('#faqTopicButtons .faq-topic-button').count(),11);
      assert.equal(await page.locator('#faqList .faq-question-item').count(),0);
      assert.equal(faqRequests.length,1,'Opening the FAQ should fetch only its thematic index');
      assert.equal(pending.length,0,'The FAQ must not request the large corpus before a Psalm click');

      await page.getByRole('button',{name:/La souffrance/i}).click();
      assert.equal(await page.locator('#faqList .faq-question-item').count(),4);
      await page.locator('#faqList .faq-question-item').first().click();
      await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      assert.ok(faqRequests.length>1,'The answer was not fetched on demand');

      const filePromise=page.waitForEvent('download');
      await page.locator('#faqPdf').click();
      const download=await filePromise;
      assert.match(download.suggestedFilename(),/^Biblaw_Question_.*\.pdf$/);

      await page.locator('#faqAnswerBody .faq-psalm-link').first().click();
      await catalogRequested;
      assert.ok(pending.length>=1,'The cited Psalm should start documentary loading');
      await page.getByText('Chargement du corpus pour ouvrir ce psaume…').waitFor();
      assert.equal(await page.locator('#recordDialog').isVisible(),false,
        'A Psalm reader appeared without the validated corpus');
      // Keep delaying until we have proved the index and answer do not wait.
      releaseCorpus=true;
      for(const release of pending.splice(0))release();
      await page.locator('#recordDialog').waitFor({state:'visible',timeout:60000});
      assert.ok(await page.locator('#dialogContent .faq-cited-verse').count()>0);
      await page.locator('#faqReturnFromPsalm').click();
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      await page.locator('#faqClose').click();
      await page.locator('#faqClose').click();
      assert.equal(await page.locator('#faqTopicButtons .faq-topic-button').count(),11);
      await page.locator('#faqClose').click();
      await page.locator('#query').fill('psaume 105');
      await page.locator('#searchButton').click();
      assert.ok(await page.locator('#results [data-open]').count()>0,
        'General search stopped working after corpus initialization');
      assert.deepEqual(errors,[],'Unexpected JavaScript errors: '+errors.join(' | '));
      console.log('FAQ M1 '+viewport.width+'px PASS; 11 topics shown in '+elapsed+
        ' ms with the documentary corpus blocked, answer/PDF/validated Psalm/back/search OK');
    }finally{
      releaseCorpus=true;
      for(const release of pending.splice(0))release();
      await page.close();
    }
  }

  // Unavailable catalog must not prevent browsing the FAQ; opening a Psalm
  // must show a clear error rather than silently discarding a click.
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.route(/\/browser-search-catalog\.json/,route=>route.abort());
  try{
    await page.goto(base,{waitUntil:'domcontentloaded'});
    await page.locator('#faqToggle').click();
    await page.locator('#faqTopicButtons .faq-topic-button').first().waitFor({timeout:8000});
    await page.getByRole('button',{name:/La souffrance/i}).click();
    await page.locator('#faqList .faq-question-item').first().click();
    await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
    await page.locator('#faqAnswerBody .faq-psalm-link').first().click();
    await page.getByText('Le corpus documentaire est indisponible. Réessayez plus tard.').waitFor();
    assert.equal(await page.locator('#recordDialog').isVisible(),false);
    assert.deepEqual(errors,[]);
    console.log('FAQ M1 failure-mode PASS: FAQ available, Psalm failure is explicit');
  }finally{await page.close();}
}finally{await browser.close();}
