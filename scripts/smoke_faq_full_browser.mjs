import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {chromium} from 'playwright';

// Mission 4: exercise the actual generated Pages site in desktop and phone viewports.
// This is a preview test; it never navigates to or changes the public production site.
const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const sizes=[{name:'mobile',width:390,height:844},{name:'desktop',width:1440,height:900}];
const browser=await chromium.launch({headless:true});
const results=[];
try{
 for(const size of sizes){
  const context=await browser.newContext({viewport:{width:size.width,height:size.height},acceptDownloads:true});
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('console',msg=>{if(msg.type()==='error')errors.push('console: '+msg.text());});
  try{
   await page.goto(base,{waitUntil:'networkidle'});
   await page.waitForFunction(()=>!document.getElementById('corpusStats')?.textContent.includes('Chargement'),{timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('#faqList .faq-question-item').length===95,{timeout:45000});
   assert.equal((await page.locator('#faqStatus').innerText()).trim(),'','FAQ did not load cleanly');
   await page.locator('#faqToggle').click();
   assert.equal(await page.locator('#faqLibrary').isVisible(),true);
   const rows=page.locator('#faqList .faq-question-item');
   assert.equal(await rows.count(),95);
   const titles=new Set(),linked=new Set(),pdfStats=[];
   let seen=0, links=0,openedPsalms=0,headerChecks=0;
   let biggestOverflow=0;
   for(let i=0;i<95;i++){
    const button=rows.nth(i);
    const indexTitle=(await button.locator('.faq-question-title').innerText()).trim();
    assert.ok(indexTitle,'Empty FAQ title index '+i);
    await button.click();
    assert.equal(await page.locator('#faqAnswer').isVisible(),true,'Answer not visible '+i);
    assert.equal(await page.locator('#faqIndex').isVisible(),false);
    const heading=(await page.locator('#faqAnswerTitle').innerText()).trim();
    assert.equal(heading,indexTitle,'Index/answer title mismatch '+i);
    assert.ok(!titles.has(heading),'Duplicate title '+heading);
    titles.add(heading);
    const body=page.locator('#faqAnswerBody');
    const content=(await body.innerText()).trim();
    assert.ok(content.startsWith('La Bible essénienne enseigne que'),'Incorrect editorial source attribution '+heading);
    assert.ok(content.length>200,'Answer unexpectedly short '+heading);
    const refs=body.locator('.faq-psalm-link');
    const count=await refs.count();
    assert.ok(count>=3&&count<=18,'Unexpected citation count '+count+' '+heading);
    const all=await refs.evaluateAll(nodes=>nodes.map(n=>({text:n.textContent,title:n.title,disabled:n.disabled,role:n.tagName})));
    for(const info of all){
     assert.equal(info.role,'BUTTON','Source is not a button '+heading);
     assert.equal(info.disabled,false,'Disabled Psalm source in '+heading);
     assert.match(info.title,/Lire Psaume/,'Missing Psalm link label '+heading);
     assert.match(info.text,/^\(psaume \d+/,'Unexpected source label '+heading);
     linked.add(info.text);
    }
    links+=count;
    if(i===91){
     assert.ok(await body.locator('strong').count()>=3,'Final answer subsection headings lost');
     headerChecks++;
    }
    const measure=await page.evaluate(()=>({
      documentWidth:document.documentElement.scrollWidth,viewportWidth:window.innerWidth
    }));
    biggestOverflow=Math.max(biggestOverflow,measure.documentWidth-measure.viewportWidth);
    // Reproduce actual Psalm reader and return at first, middle and final FAQ,
    // plus a sample of every twentieth answer; DOM checks cover all remaining links.
    if(i===0||i===50||i===91||i===94||i%20===0){
     for(const refIndex of [...new Set([0,count-1])]){
      await refs.nth(refIndex).click();
      assert.equal(await page.locator('#recordDialog').isVisible(),true,'Psalm reader not visible '+heading);
      assert.ok(await page.locator('#dialogContent .faq-cited-verse').count()>0,
        'Cited verses not highlighted '+heading);
      assert.equal(await page.locator('#faqReturnFromPsalm').isVisible(),true);
      await page.locator('#faqReturnFromPsalm').click();
      assert.equal(await page.locator('#recordDialog').isVisible(),false);
      assert.equal(await page.locator('#faqAnswer').isVisible(),true);
      assert.equal((await page.locator('#faqAnswerTitle').innerText()).trim(),heading,
        'Did not return to same answer');
      openedPsalms++;
     }
    }
    // Export actual PDF bytes (not only filename) for first, middle and last.
    if([0,50,94].includes(i)){
     const pending=page.waitForEvent('download');
     await page.locator('#faqPdf').click();
     const dl=await pending;
     assert.match(dl.suggestedFilename(),/^Biblaw_Question_.*\.pdf$/);
     const bytes=await readFile(await dl.path());
     assert.ok(bytes.length>350,'PDF download too small '+heading);
     assert.equal(bytes.subarray(0,5).toString(),'%PDF-','PDF magic invalid');
     pdfStats.push({question:i+1,bytes:bytes.length});
    }
    await page.locator('#faqBack').click();
    assert.equal(await page.locator('#faqIndex').isVisible(),true);
    assert.equal(await page.locator('#faqAnswer').isVisible(),false);
    seen++;
   }
   assert.equal(seen,95);
   assert.equal(links,424,'The browser must render exactly 424 working source links');
   assert.equal(titles.size,95);
   assert.equal(pdfStats.length,3);
   // Ten former duplicate question titles are now aliases of enhanced
   // composite answers, each preserving the two original teaching blocks.
   const dedupCases=[
     ['Dieu existe-t-il ?',/Dieu existe-t-il vraiment/i,7],
     ['Ai-je une mission particulière ?',/Avons-nous une mission particulière/i,7],
     ['Pourquoi certaines demandes restent-elles sans réponse ?',/Pourquoi Dieu ne répond-il pas/i,7],
     ['Les religions sont-elles toutes des chemins vers Dieu ?',/Toutes les religions conduisent-elles/i,6],
     ['Peut-on concilier une démarche scientifique avec la croyance en Dieu ?',/La science et la spiritualité/i,6],
     ['Comment cultiver sa paix intérieure ?',/Comment trouver la paix intérieure/i,9],
     ['Comment devenir véritablement heureux ?',/Qu'est-ce que le véritable bonheur/i,7],
     ["Comment développer l'amour ?",/Comment aimer véritablement/i,9],
     ['Pourquoi existons-nous ?',/Pourquoi sommes-nous sur Terre/i,6],
     ['Comment mieux me connaître et maîtriser mes pensées et mes émotions ?',/Comment mieux se connaître/i,7],
   ];
   for(const [alias,title,citationCount] of dedupCases){
     await page.locator('#faqSearch').fill(alias);
     assert.equal(await page.locator('#faqList .faq-question-item').count(),1,
       'Old question alias has no unique consolidated destination: '+alias);
     await page.locator('#faqList .faq-question-item').first().click();
     assert.match(await page.locator('#faqAnswerTitle').innerText(),title);
     assert.equal(await page.locator('#faqAnswerBody .faq-psalm-link').count(),citationCount,
       'All source citations must be retained: '+alias);
     assert.equal(await page.locator('#faqAnswerBody strong').count()>=1,true,
       'Complementary teaching subsection missing: '+alias);
     const text=await page.locator('#faqAnswerBody').innerText();
     assert.equal((text.match(/La Bible essénienne enseigne que/g)||[]).length,2,
       'One of the two original teaching texts was lost: '+alias);
     await page.locator('#faqBack').click();
   }
   await page.locator('#faqSearch').fill('');
   // 19 alternative phrasings: redirect the visitor to the unique canonical article.
   await page.locator('#faqSearch').fill('la conscience disparaît-elle lorsque le cerveau cesse de fonctionner');
   assert.equal(await page.locator('#faqList .faq-question-item').count(),1,
     'Alternate question must point to one, nonduplicated answer');
   await page.locator('#faqList .faq-question-item').first().click();
   assert.equal((await page.locator('#faqAnswerTitle').innerText()).trim(),
     'Que devient notre conscience après la mort ?');
   await page.locator('#faqBack').click();
   // A different wording reuses the existing 102-article corpus, not a copy.
   await page.locator('#faqSearch').fill('comment vivre autrement');
   assert.equal(await page.locator('#faqList .faq-question-item').count(),1,
     'Existing FAQ alias must find one destination');
   await page.locator('#faqList .faq-question-item').first().click();
   assert.match(await page.locator('#faqAnswerTitle').innerText(),/activités ordinaires/i,
     'Existing FAQ alias navigated to the wrong article');
   await page.locator('#faqBack').click();
   await page.locator('#faqSearch').fill('que nous apprennent réellement les expériences de mort imminente');
   assert.equal(await page.locator('#faqList .faq-question-item').count(),0,
     'Unsupported question must not become a false answer');
   assert.match(await page.locator('#faqSearchStatus').innerText(),/Aucune réponse fondée/);
   await page.locator('#faqSearch').fill('');
   assert.equal(await page.locator('#faqList .faq-question-item').count(),95,
     'Clearing search must restore the complete index');
   await page.locator('#faqClose').click();
   assert.equal(await page.locator('#faqLibrary').isVisible(),false,'FAQ close did not return to search');

   // Verify search number to theme replacement and optional source filters.
   await page.locator('#modeThemes').click();
   await page.locator('#query').fill('105');
   await page.locator('#searchButton').click();
   assert.equal(await page.locator('.result-card').count(),4,'Number search 105 changed');
   await page.locator('#query').fill('sainte assemblée');
   await page.locator('#searchButton').click();
   assert.equal(await page.locator('.result-card').count(),3,'Changing number to theme left stale results');
   assert.match(await page.locator('#resultCount').innerText(),/3 psaumes trouvés/);

   // Check all selectors remain usable and their values persist.
   const choices=page.locator('#sourceScope input[name="sourceType"]');
   assert.equal(await choices.count(),3);
   assert.equal(await page.locator('#archangelFilter option').count(),5);
   assert.equal(await page.locator('#notesLibraryToggle').isVisible(),true);
   assert.equal(await page.locator('#indexToggle').isVisible(),true);
   assert.equal(await page.locator('#popularQuestionsToggle').isVisible(),false);
   // Test basic alternate search modes without assuming query-specific counts.
   await page.locator('#modeExact').click();
   await page.locator('#query').fill('vie + amour');
   await page.locator('#searchButton').click();
   assert.ok((await page.locator('#results').innerText()).trim().length>0,'Exact double-word search broken');
   assert.deepEqual(errors,[],'Javascript errors: '+JSON.stringify(errors));
   results.push({viewport:size.name,width:size.width,height:size.height,questions:seen,
     citations:links,distinctRenderedCitationLabels:linked.size,psalmDialogRoundtrips:openedPsalms,
     pdfDownloads:pdfStats,subheadingChecks:headerChecks,maxHorizontalOverflowPx:biggestOverflow,
     modeSearches:'105 -> sainte assemblée -> vie + amour',javascriptErrors:errors.length});
   console.log('MISSION4_VIEWPORT_PASS='+JSON.stringify(results.at(-1)));
  }finally{await context.close();}
 }
 assert.equal(results.length,2);
 console.log('BIBLAW MISSION4 CHROMIUM PASS: 95 composite FAQs, 424 citations and 3 real PDF exports per viewport; Psalm navigation, mobile/desktop search and FAQ closure.');
}finally{await browser.close();}
