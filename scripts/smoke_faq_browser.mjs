import assert from 'node:assert/strict';
import {chromium} from 'playwright';

// Browser-level integration against the exact Pages build. Mobile-size viewport.
const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},acceptDownloads:true});
const errors=[];
page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(base,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.querySelectorAll('#faqList .faq-question-item').length===95,{timeout:30000});
  assert.equal(await page.locator('#faqStatus').innerText(),'','FAQ load error');
  await page.locator('#faqToggle').click();
  assert.equal(await page.locator('#faqLibrary').isVisible(),true);
  assert.equal(await page.locator('#faqList .faq-question-item').count(),95);
  const first=page.locator('#faqList .faq-question-item').first();
  await first.click();
  assert.equal(await page.locator('#faqAnswer').isVisible(),true);
  assert.ok((await page.locator('#faqAnswerTitle').innerText()).trim());
  const refs=page.locator('#faqAnswerBody .faq-psalm-link');
  assert.ok(await refs.count()>=3,'Missing source references');
  for(let i=0;i<await refs.count();i++)assert.equal(await refs.nth(i).isEnabled(),true);
  await refs.first().click();
  assert.equal(await page.locator('#recordDialog').isVisible(),true,'Psalm reader did not open');
  assert.ok(await page.locator('#dialogContent .faq-cited-verse').count()>0,'Cited verses not highlighted');
  assert.equal(await page.locator('#faqReturnFromPsalm').isVisible(),true);
  await page.locator('#faqReturnFromPsalm').click();
  assert.equal(await page.locator('#faqAnswer').isVisible(),true);
  assert.equal(await page.locator('#recordDialog').isVisible(),false);
  const event=page.waitForEvent('download');
  await page.locator('#faqPdf').click();
  const file=await event;
  assert.match(file.suggestedFilename(),/^Biblaw_Question_.*\.pdf$/);
  await page.locator('#faqBack').click();
  assert.equal(await page.locator('#faqIndex').isVisible(),true);
  await page.locator('#faqList .faq-question-item').nth(91).click();
  assert.match(await page.locator('#faqAnswerTitle').innerText(),/repas.*marche.*parole/i);
  assert.ok(await page.locator('#faqAnswerBody strong').count()>0,'FAQ subsection headings lost');
  assert.ok(await page.locator('#faqAnswerBody .faq-psalm-link').count()>=6);
  await page.locator('#faqBack').click();
  await page.locator('#faqList .faq-question-item').last().click();
  assert.match(await page.locator('#faqAnswerTitle').innerText(),/progresser intérieurement/i);
  assert.equal(await page.locator('#faqAnswerBody .faq-psalm-link').count(),6);
  await page.locator('#faqClose').click();
  assert.equal(await page.locator('#faqLibrary').isVisible(),false);
  assert.deepEqual(errors,[],'Javascript page errors: '+errors.join(' | '));
  console.log('BIBLAW FAQ Chromium mobile smoke PASS: 95 listed, answers opened, Psalm verses highlighted, return/back, PDF download, formatted headings.');
}finally{await browser.close();}
