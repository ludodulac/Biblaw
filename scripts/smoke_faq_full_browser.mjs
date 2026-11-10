import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const sizes=[{name:'mobile',width:390,height:844},{name:'desktop',width:1440,height:900}];
const browser=await chromium.launch({headless:true});
try{
 for(const size of sizes){
  const context=await browser.newContext({viewport:{width:size.width,height:size.height},acceptDownloads:true});
  const page=await context.newPage();
  const errors=[],faqRequests=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  page.on('request',r=>{if(/\/data\/faq-[\w-]+\.json/.test(r.url()))faqRequests.push(r.url());});
  try{
   await page.goto(base,{waitUntil:'networkidle'});
   // M3: open the public FAQ without waiting for an unrelated 22 MB corpus.
   assert.equal(faqRequests.length,0,'FAQ loaded before the visitor opened it');
   await page.locator('#faqToggle').click();
   await page.locator('#faqTopicButtons .faq-topic-button').first().waitFor();
   const topics=page.locator('#faqTopicButtons .faq-topic-button');
   assert.equal(await topics.count(),11);
   assert.equal(await page.locator('#faqList .faq-question-item').count(),0,'The initial screen should contain topics, not every question');
   assert.equal(faqRequests.length,1,'The first FAQ screen should fetch only one metadata file');
   let seen=0,links=0,psalms=0;const titles=new Set();let biggestOverflow=0;
   for(let t=0;t<11;t++){
    const topic=topics.nth(t);
    const topicLabel=await topic.locator('span').innerText();
    const topicCount=Number((await topic.locator('small').innerText()).match(/\d+/)[0]);
    await topic.click();
    const rows=page.locator('#faqList .faq-question-item');
    assert.equal(await rows.count(),topicCount,'Wrong topic: '+topicLabel);
    for(let i=0;i<topicCount;i++){
     const button=rows.nth(i),title=(await button.locator('.faq-question-title').innerText()).trim();
     await button.click();
     await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
     assert.equal(await page.locator('#faqAnswerTitle').innerText(),title);
     assert.ok(!titles.has(title),'Repeated canonical question: '+title);
     titles.add(title);
     const body=(await page.locator('#faqAnswerBody').innerText()).trim();
     assert.ok(body.startsWith('La Bible essénienne enseigne que'),'Changed source attribution: '+title);
     const refs=page.locator('#faqAnswerBody .faq-psalm-link');
     const count=await refs.count();
     assert.ok(count>=3&&count<=18,'Invalid citation count for '+title);
     const disabled=await refs.evaluateAll(nodes=>nodes.filter(n=>n.disabled).length);
     assert.equal(disabled,0,'Unresolvable Psalm citation: '+title);
     links+=count;
     const measure=await page.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
     biggestOverflow=Math.max(biggestOverflow,measure);
     if(seen===0||seen===50||seen===94){
      for(const index of [...new Set([0,count-1])]){
       await refs.nth(index).click();
       await page.locator('#recordDialog').waitFor({state:'visible',timeout:60000});
       assert.equal(await page.locator('#recordDialog').isVisible(),true);
       assert.ok(await page.locator('#dialogContent .faq-cited-verse').count()>0);
       await page.locator('#faqReturnFromPsalm').click();
       assert.equal(await page.locator('#recordDialog').isVisible(),false);
       psalms++;
      }
      const event=page.waitForEvent('download');
      await page.locator('#faqPdf').click();
      const file=await event;
      const bytes=await readFile(await file.path());
      assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
     }
     await page.locator('#faqClose').click();
     seen++;
    }
    await page.locator('#faqClose').click();
   }
   assert.equal(seen,95);
   assert.equal(titles.size,95);
   assert.equal(links,424,'All 424 citations must be retained');
   assert.ok(biggestOverflow<=12,'Horizontal overflow: '+biggestOverflow);
   const aliasCases=[
     ['Dieu existe-t-il ?',/Dieu existe-t-il vraiment/i,7],
     ['Ai-je une mission particulière ?',/Avons-nous une mission particulière/i,7],
     ['Pourquoi certaines demandes restent-elles sans réponse ?',/Pourquoi Dieu ne répond-il pas/i,7],
     ['Les religions sont-elles toutes des chemins vers Dieu ?',/Toutes les religions conduisent-elles/i,6],
     ['Peut-on concilier une démarche scientifique avec la croyance en Dieu ?',/La science et la spiritualité/i,6],
     ['Comment cultiver sa paix intérieure ?',/Comment trouver la paix intérieure/i,9],
     ['Comment devenir véritablement heureux ?',/Qu.est-ce que le véritable bonheur/i,7],
     ["Comment développer l'amour ?",/Comment aimer véritablement/i,9],
     ['Pourquoi existons-nous ?',/Pourquoi sommes-nous sur Terre/i,6],
     ['Comment mieux me connaître et maîtriser mes pensées et mes émotions ?',/Comment mieux se connaître/i,7]
   ];
   for(const [alias,canonical,count] of aliasCases){
    await page.locator('#faqSearch').fill(alias);
    assert.equal(await page.locator('#faqList .faq-question-item').count(),1,'Missing alias '+alias);
    await page.locator('#faqList .faq-question-item').first().click();
    await page.locator('#faqAnswerBody .faq-psalm-link').first().waitFor();
    assert.match(await page.locator('#faqAnswerTitle').innerText(),canonical);
    assert.equal(await page.locator('#faqAnswerBody .faq-psalm-link').count(),count);
    assert.ok(await page.locator('#faqAnswerBody strong').count()>0);
    await page.locator('#faqClose').click();
   }
   await page.locator('#faqSearch').fill('Que nous apprennent réellement les expériences de mort imminente ?');
   assert.equal(await page.locator('#faqList .faq-question-item').count(),0);
   assert.match(await page.locator('#faqSearchStatus').innerText(),/Aucune réponse fondée/);
   assert.deepEqual(errors,[],'JavaScript errors: '+errors.join(' | '));
   console.log('BIBLAW FAQ 101 '+size.name+' PASS: '+seen+' responses, '+links+' Psalm citations, 11 themes, '+psalms+' verse-view round trips, aliases and PDF.');
  }finally{await context.close();}
 }
}finally{await browser.close();}
