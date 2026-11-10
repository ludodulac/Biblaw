#!/usr/bin/env node
// Mission 2: real Chromium navigation tests for desktop and narrow mobile.
// M1 is the base; no published deployment is involved.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const browser=await chromium.launch({headless:true});
const url=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const numbers=[];
try{
  for(const width of [390,1366]){
    const page=await browser.newPage({viewport:{width,height:844},acceptDownloads:true});
    const errors=[],sources=[];
    page.on('pageerror',error=>errors.push(error.message));
    page.on('request',request=>{
      const match=request.url().match(/\/data\/(faq-[\w-]+\.json)/);
      if(match)sources.push(match[1]);
    });
    let releaseAnswer=null;
    await page.route(/\/data\/faq-public-085\.json/,async route=>{
      await new Promise(resolve=>{releaseAnswer=resolve;});
      await route.continue();
    });
    try{
      await page.goto(url,{waitUntil:'domcontentloaded'});
      await page.locator('#faqToggle').click();
      await page.locator('#faqTopicButtons .faq-topic-button').first().waitFor({timeout:10000});
      assert.equal(await page.locator('#faqTopicButtons .faq-topic-button').count(),11);
      assert.deepEqual(sources,['faq-101-index.json']);

      // Selecting a topic uses the already-loaded metadata and requests no answer.
      const themeTime=await page.evaluate(()=>{
        const start=performance.now();
        [...document.querySelectorAll('#faqTopicButtons button')]
          .find(button=>button.textContent.includes('La souffrance')).click();
        return performance.now()-start;
      });
      assert.equal(await page.locator('#faqList .faq-question-item').count(),4);
      assert.deepEqual(sources,['faq-101-index.json']);
      numbers.push({width,themeTime});

      // Two clicks during a deliberately stalled download: only the last
      // choice must win, without duplicate fetches or a stale answer.
      const firstRequest=page.waitForRequest(r=>/\/data\/faq-public-085\.json/.test(r.url()));
      await page.locator('#faqList .faq-question-item').nth(0).click();
      await page.getByText('Chargement de la réponse…').waitFor();
      await firstRequest;
      await page.locator('#faqList .faq-question-item').nth(1).click();
      assert.equal(sources.filter(s=>s==='faq-public-085.json').length,1);
      assert.ok(releaseAnswer,'The answer was not intercepted');
      releaseAnswer();
      await page.locator('#faqAnswerTitle').getByText('Pourquoi les êtres humains souffrent-ils ?').waitFor();
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      assert.equal(await page.locator('#faqIndex').isVisible(),false);
      assert.equal(sources.filter(s=>s==='faq-public-085.json').length,1);
      assert.equal(await page.locator('.faq-answer-nav').count(),1);
      await page.locator('.faq-answer-nav button').first().click();
      await page.locator('#faqAnswerTitle').getByText('Si Dieu existe et qu\'il est bon, pourquoi permet-il la souffrance ?').waitFor();
      assert.equal(sources.filter(s=>s==='faq-public-085.json').length,1);
      // Back to question 2: cached -> synchronous, without a "loading" flash.
      const cachedTime=await page.evaluate(()=>{
        const button=[...document.querySelectorAll('.faq-answer-nav button')]
          .find(b=>b.textContent.includes('suivante'));
        const start=performance.now();
        button.click();
        if(document.getElementById('faqStatus').textContent)
          throw Error('A cached answer displayed a loading spinner');
        if(!document.getElementById('faqAnswerTitle').textContent
          .includes('Pourquoi les êtres humains souffrent-ils'))
          throw Error('A cached answer was not shown synchronously');
        return performance.now()-start;
      });
      assert.ok(cachedTime<150,'Cached answer should be immediate: '+cachedTime+' ms');
      assert.equal(sources.filter(s=>s==='faq-public-085.json').length,1);

      // The PDF button still downloads the current complete answer.
      const downloaded=page.waitForEvent('download');
      await page.locator('#faqPdf').click();
      const pdf=await downloaded;
      assert.match(pdf.suggestedFilename(),/^Biblaw_Question_.*\.pdf$/);

      // Topic return is immediate and the index is not requested again.
      await page.locator('#faqClose').click();
      assert.equal(await page.locator('#faqList .faq-question-item').count(),4);
      await page.locator('#faqClose').click();
      assert.equal(await page.locator('#faqTopicButtons .faq-topic-button').count(),11);

      // Long topic: the original list scroll position is restored on return.
      await page.getByRole('button',{name:/^Dieu\b/}).click();
      assert.equal(await page.locator('#faqList .faq-question-item').count(),22);
      const beforeList=await page.evaluate(()=>{
        window.scrollTo({top:500,behavior:'instant'});
        const y=window.scrollY;
        document.querySelectorAll('#faqList .faq-question-item')[7].click();
        return y;
      });
      assert.ok(beforeList>100,'List must be scrollable for the restoration test');
      await page.locator('#faqAnswerTitle').waitFor();
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      const firstTitle=await page.locator('#faqAnswerTitle').innerText();
      const originalAnswerPos=await page.evaluate(()=>{
        window.scrollTo({top:450,behavior:'instant'});
        return window.scrollY;
      });
      assert.ok(originalAnswerPos>100,'Answer must be scrollable for reading position test');
      // Dispatch directly: Playwright locator.click() would first auto-scroll
      // to the bottom control and alter the reading position being measured.
      await page.evaluate(()=>[...document.querySelectorAll('.faq-answer-nav button')]
        .find(b=>b.textContent.includes('suivante')).click());
      await page.waitForFunction(title=>document.getElementById('faqAnswerTitle').textContent!==title,firstTitle);
      await page.evaluate(()=>[...document.querySelectorAll('.faq-answer-nav button')]
        .find(b=>b.textContent.includes('précédente')).click());
      await page.waitForFunction(title=>document.getElementById('faqAnswerTitle').textContent===title,firstTitle);
      assert.ok(Math.abs(await page.evaluate(()=>window.scrollY)-originalAnswerPos)<6,
        'Answer reading position was lost when returning from a neighboring question');
      await page.locator('#faqClose').click();
      assert.ok(Math.abs(await page.evaluate(()=>window.scrollY)-beforeList)<6,
        'The question list scroll position was lost');
      assert.equal(await page.locator('#faqList .faq-question-item').count(),22);

      // Search aliases are global and must survive return from the answer.
      await page.locator('#faqSearch').fill('Ai-je une mission particulière ?');
      assert.equal(await page.locator('#faqList .faq-question-item').count(),1);
      await page.locator('#faqList .faq-question-item').first().click();
      await page.locator('#faqAnswerTitle').getByText('Avons-nous une mission particulière ?').waitFor();
      await page.locator('#faqClose').click();
      assert.equal(await page.locator('#faqSearch').inputValue(),'Ai-je une mission particulière ?');
      assert.equal(await page.locator('#faqList .faq-question-item').count(),1);
      await page.locator('#faqClose').click();
      await page.locator('#faqClose').click();

      // Closed/reopened FAQ keeps the original index cached.
      await page.locator('#faqToggle').click();
      assert.equal(await page.locator('#faqTopicButtons .faq-topic-button').count(),11);
      assert.equal(sources.filter(s=>s==='faq-101-index.json').length,1);
      assert.deepEqual(errors,[],'Unexpected browser errors: '+errors.join(' | '));
      console.log('FAQ M2 '+width+'px PASS: theme '+themeTime.toFixed(1)+'ms, cached answer '+
        cachedTime.toFixed(1)+'ms; no duplicate fetch, last-click-wins, adjacent navigation, '+
        'list and reading scroll, aliases, PDF, return and reopen');
    }finally{
      releaseAnswer?.();
      await page.close();
    }
  }
  console.log('FAQ_M2_NAVIGATION_PASS '+JSON.stringify(numbers));
}finally{await browser.close();}
