#!/usr/bin/env node
// Single top-level Retour, stepwise hierarchical navigation and keyword wording.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
try{
  for(const width of [390,1366]){
    const page=await browser.newPage({viewport:{width,height:844}});
    const errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    const assertOneBack=async()=>{
      assert.equal(await page.locator('#faqClose').innerText(),'← Retour');
      assert.equal(await page.locator('#faqLibrary').getByRole('button',{name:/Retour/}).count(),1,
        'There must be exactly one visible FAQ Retour control');
      assert.equal(await page.locator('#faqThemeBack, #faqBack').count(),0,
        'No duplicate hidden or visible back controls should remain');
    };
    try{
      await page.goto(base,{waitUntil:'domcontentloaded'});
      await page.locator('#faqToggle').click();
      await page.locator('#faqTopicButtons button').first().waitFor({timeout:10000});
      assert.equal(await page.locator('#faqTopicButtons button').count(),11);
      await assertOneBack();
      assert.equal(await page.locator('label[for=faqSearch]').innerText(),'Rechercher un mot-clé');
      assert.match(await page.locator('#faqSearch').getAttribute('placeholder'),/Tapez un mot/);
      // Search is a keyword filter over the question titles and aliases.
      await page.locator('#faqSearch').fill('amour');
      assert.ok(await page.locator('#faqList button').count()>0,'A keyword should filter FAQ titles');
      assert.equal(await page.locator('#faqTopics').isVisible(),false);
      await assertOneBack();
      await page.locator('#faqClose').click(); // keyword results -> themes
      assert.equal(await page.locator('#faqSearch').inputValue(),'');
      assert.equal(await page.locator('#faqTopicButtons button').count(),11);

      await page.getByRole('button',{name:/^Dieu\b/}).click();
      assert.equal(await page.locator('#faqList button').count(),22);
      await assertOneBack();
      await page.locator('#faqList button').first().click();
      await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      await assertOneBack();
      await page.locator('#faqClose').click(); // answer -> same topic's questions
      assert.equal(await page.locator('#faqAnswer').isVisible(),false);
      assert.equal(await page.locator('#faqList button').count(),22);
      await assertOneBack();
      await page.locator('#faqClose').click(); // theme questions -> all themes
      assert.equal(await page.locator('#faqTopicButtons button').count(),11);
      await assertOneBack();
      await page.locator('#faqClose').click(); // all themes -> general search
      assert.equal(await page.locator('#faqLibrary').isVisible(),false);
      assert.equal(await page.locator('#faqToggle').getAttribute('aria-expanded'),'false');
      await page.locator('#faqToggle').click();
      await page.locator('#faqTopicButtons button').first().waitFor();
      await assertOneBack();
      await page.locator('#faqClose').click();
      assert.deepEqual(errors,[]);
      console.log('BIBLAW FAQ RETOUR '+width+'px PASS: one top button, keyword filtering, '+
        'answer → questions → themes → search, reopen, no JavaScript errors');
    }finally{await page.close();}
  }
}finally{await browser.close();}
